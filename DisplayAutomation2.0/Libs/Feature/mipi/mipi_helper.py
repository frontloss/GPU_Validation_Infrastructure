######################################################################################
# @file         mipi_helper.py
# @brief        This contains verification definitions for various MIPI modules and features.
# @details      Also contains helper functions for MIPI w.r.t reading VBT, calculations, current state, etc.
# @author       Sri Sumanth Geesala
######################################################################################

import importlib
import logging
import subprocess
import time
import math

from registers.mmioregister import MMIORegister
from Libs.Core.logger import gdhm
from Libs.Core.vbt.vbt import Vbt

VIDEO_MODE = 0
COMMAND_MODE = 1
NON_EXISTING = -1


##
# @brief Class that has operations related to MIPI display timings. It gets the timings data from VBT.
class VbtMipiTimings():

    ##
    # @brief constructor for VbtMipiTimings class
    def __init__(self):
        self.pixelClockHz = 0
        self.hactive = 0
        self.hsync_start = 0
        self.hsync_end = 0
        self.htotal = 0

        self.vactive = 0
        self.vsync_start = 0
        self.vsync_end = 0
        self.vtotal = 0

    ##
    # @brief        from VBT, calculates horizontal and vertical timings, and populates into class members.
    # @param[in]    gfx_vbt full vbt data
    # @param[in]    panel_index panel index in VBT for current MIPI panel
    # @return       None
    def get_vbt_mipi_timings(self, gfx_vbt, panel_index):

        # for VBT version >= 229, read timing information from VBT block 58
        if gfx_vbt.version >= 229:
            logging.debug(
                "Reading MIPI timings from VBT block 58, since VBT version is {0} (>=229)".format(gfx_vbt.version))
            generic_display_timing_data = gfx_vbt.block_58.GenericDisplayTimingDataEntry[panel_index]

            self.pixelClockHz = generic_display_timing_data.PixelClockKhz * 1000
            self.hactive = generic_display_timing_data.HActive
            self.hsync_start = self.hactive + generic_display_timing_data.HFrontPorch
            self.hsync_end = self.hsync_start + generic_display_timing_data.HSync
            self.htotal = self.hactive + generic_display_timing_data.HBlank

            self.vactive = generic_display_timing_data.VActive
            self.vsync_start = self.vactive + generic_display_timing_data.VFrontPorch
            self.vsync_end = self.vsync_start + generic_display_timing_data.VSync
            self.vtotal = self.vactive + generic_display_timing_data.VBlank

        # for VBT version < 229, read timing information from VBT block 42
        else:
            logging.debug(
                "Reading MIPI timings from VBT block 42, since VBT version is {0} (<229)".format(gfx_vbt.version))
            vbt_panel_data = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index]

            self.pixelClockHz = vbt_panel_data.PixelClock * 10 * 1000  # stored in units of 10 KHz in VBT
            self.hactive = (vbt_panel_data.HActiveHi << 8) | (vbt_panel_data.HActiveLo)
            hsync_offset = (vbt_panel_data.HSyncOffsetHi << 8) | (vbt_panel_data.HSyncOffsetLo)
            self.hsync_start = self.hactive + hsync_offset
            hsync_width = (vbt_panel_data.HSyncWidthHi << 8) | (vbt_panel_data.HSyncWidthLo)
            self.hsync_end = self.hsync_start + hsync_width
            hblank = (vbt_panel_data.HBlankHi << 8) | (vbt_panel_data.HBlankLo)
            self.htotal = self.hactive + hblank

            self.vactive = (vbt_panel_data.VActiveHi << 8) | (vbt_panel_data.VActiveLo)
            vsync_offset = (vbt_panel_data.VSyncOffsetHi << 4) | (vbt_panel_data.VSyncOffsetLo)
            self.vsync_start = self.vactive + vsync_offset
            vsync_width = (vbt_panel_data.VSyncWidthHi << 4) | (vbt_panel_data.VSyncWidthLo)
            self.vsync_end = self.vsync_start + vsync_width
            vblank = (vbt_panel_data.VBlankHi << 8) | (vbt_panel_data.VBlankLo)
            self.vtotal = self.vactive + vblank

    ##
    # @brief        After getting timing data from VBT, call this method to adjust the timings based on
    #               current MIPI panel type - dual link/DSC/burst mode/command mode.
    # @param[in]    mipi_helper object of MipiHelper
    # @param[in]    panel_index panel index in VBT for current MIPI panel
    # @return       None
    def adjust_timings_for_mipi_config(self, mipi_helper, panel_index):

        # if dual link, all horizontal values will be divided by 2
        if mipi_helper.dual_link:
            # HW will add overlap, SW shouldn't add it
            self.hactive = self.hactive // 2
            self.hsync_start = self.hsync_start // 2
            self.hsync_end = self.hsync_end // 2
            self.htotal = self.htotal // 2
            self.pixelClockHz = self.pixelClockHz // 2

        # if compression is enabled, HTotal, HSyncStart, and HSyncEnd should be divided by compression ratio
        if mipi_helper.DSC_enabled:
            bpc_bits = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[
                panel_index].DSCColorDepthCapabilities
            VBT_DSC_bpc = 8 if bpc_bits & 0b0010 else 10 if bpc_bits & 0b0100 else 12
            bpp_bits = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[panel_index].DSCMaximumBitsPerPixel
            VBT_DSC_bpp = 6 if bpp_bits == 0 else 8 if bpp_bits == 1 else 10 if bpp_bits == 2 else 12

            # input bits per pixel / output bits per pixel will give compression ratio
            compression_ratio = (VBT_DSC_bpc * 3) / VBT_DSC_bpp
            self.hsync_start = int(math.ceil(self.hsync_start / compression_ratio))
            self.hsync_end = int(math.ceil(self.hsync_end / compression_ratio))
            self.htotal = int(math.ceil(self.htotal / compression_ratio))
            self.pixelClockHz = int(math.ceil(self.pixelClockHz / compression_ratio))

        # for video mode's burst mode - hsync_start, hsync_end, htotal should be multiplied with burst mode ratio.
        if (mipi_helper.get_mode_of_operation(panel_index) == VIDEO_MODE and
                mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].VideoTransferMode == 0b11):
            dot_clock = self.pixelClockHz
            bpp = mipi_helper.get_bpp(panel_index)
            lane_count = mipi_helper.get_lane_count(panel_index)
            nonBurstMode_rate = (dot_clock * bpp) / (lane_count * 1.0)  # nonBurstMode_rate in Hz
            burstMode_rate = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[
                                 panel_index].RequiredBurstModeFreq * 1000.0  # burstMode_rate in Hz
            # if burstMode_rate is less than nonBurstMode_rate, treat it as non-burst mode
            if (burstMode_rate > nonBurstMode_rate):
                burst_mode_ratio = burstMode_rate / nonBurstMode_rate
                self.hsync_start = int(math.ceil(self.hsync_start * burst_mode_ratio))
                self.hsync_end = int(math.ceil(self.hsync_end * burst_mode_ratio))
                self.htotal = int(math.ceil(self.htotal * burst_mode_ratio))
                self.pixelClockHz = int(math.ceil(self.pixelClockHz * burst_mode_ratio))

        # if operating in command mode, the DSI transcoder is not responsible for the timings to the Panel,
        # but it does need to maintain some timings to the Display Engine (as below).
        if (mipi_helper.get_mode_of_operation(panel_index) == COMMAND_MODE):
            # Horizontal Total = Horizontal Active + 160
            self.htotal = self.hactive + 160
            # VBlank = ceiling( 400us / Line Time )
            line_time = mipi_helper.get_line_time(mipi_helper, panel_index, COMMAND_MODE, self.htotal)
            self.vtotal = self.vactive + int(math.ceil(400 / (line_time * 1.0)))

    ##
    # @brief        Calculates and returns the line time (in us) for this panel's timings
    # @param[in]    mipi_helper object of MipiHelper
    # @param[in]    panel_index integer value indicating panel index
    # @param[in]    mipi_mode integer value indicating video mode or command mode
    # @param[in]    htotal_cmd_mode integer value indicating htotal in case of command mode
    #               (special calculation in cmd mode). No need to pass in video mode.
    # @return       float; returns line time value in us
    def get_line_time(self, mipi_helper, panel_index, mipi_mode=VIDEO_MODE, htotal_cmd_mode=0):
        htotal = self.htotal
        vtotal = self.vtotal
        bpp = mipi_helper.get_bpp(panel_index)
        bytes_per_pixel = int(math.ceil(bpp / 8))
        lane_count = mipi_helper.get_lane_count(panel_index)

        # DSI data rate(in Hz) = (htotal * vtotal * RR * bits per pixel) / Operating Width
        if mipi_mode == COMMAND_MODE:
            dsi_data_rate = mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[
                                panel_index].RequiredBurstModeFreq * 1000
            htotal = htotal_cmd_mode
        else:
            dsi_data_rate = (htotal * vtotal * 60 * bpp) / (lane_count * 1.0)

        # Line Time = [(HTotal * Bytes per Pixel) / Operating Width] * Byte clock period
        # Byte clock period (in us) = 8 / dsi_data_rate(in Mhz)
        # Line Time(in us) = (HTotal * Bytes per Pixel * 8) / (dsi_data_rate(in Mhz) * Operating Width)
        line_time = (htotal * bytes_per_pixel * 8 * pow(10, 6)) / (dsi_data_rate * lane_count * 1.0)

        return line_time


##
# @brief Class MipiHelper that has useful APIs for calling for tests.
class MipiHelper():

    ##
    # @brief        constructor for MipiHelper class
    # @param[in]    platform platform name as string
    def __init__(self, platform):
        self.verify_fail_count = 0
        self.platform = platform
        self.panel1_index = NON_EXISTING
        self.panel2_index = NON_EXISTING
        self.dual_link = 0
        self.dual_LFP_MIPI = 0
        self.dual_LFP_MIPI_port_sync = 0
        self.DSC_enabled = 0

        self.gfx_vbt = Vbt()
        self.get_basic_mipi_caps()

    ##
    # @brief        compares the expected and actual values passed, and print PASS or FAIL log.
    # @param[in]    register register name of the current feature being verified
    # @param[in]    field field name in the register of the current feature
    # @param[in]    expected expected value (can be either number/string)
    # @param[in]    actual actual value (can be either number/string)
    # @param[in]    message any extra message to be printed in log (say, for describing current case)
    # @return       bool; returns True if comparison matched, False otherwise
    def verify_and_log_helper(self, register, field, expected, actual, message=''):
        res_template = "{res} : {register} - {field} {message} \t \t : Expected= {expected} \t Actual= {actual}"
        # e.g: 'FAIL : TRANS_HTOTAL_DSI0 - HActive - must be divisible by 4                  : Expected= 1080        Actual= 1081'

        if message != '':
            message = '- ' + message

        if actual == expected:
            logging.info(
                res_template.format(res='PASS', register=register, field=field, message=message, expected=expected,
                                    actual=actual))
            return True
        else:
            logging.error(
                res_template.format(res='FAIL', register=register, field=field, message=message, expected=expected,
                                    actual=actual))
            self.verify_fail_count += 1
            return False

    ##
    # @brief        Reads respective fields from VBT and gets the MIPI panel capabilities. Populates into class members.
    # @return       None
    def get_basic_mipi_caps(self):

        # get MIPI basic information from VBT
        # whether dual LFP MIPI (device class is 0x1400 for MIPI)
        if (self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[0].DeviceClass == 0x1400 and
                self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[1].DeviceClass == 0x1400):
            self.dual_LFP_MIPI = 1

        # panel indexes
        self.panel1_index = self.gfx_vbt.block_40.PanelType
        if self.dual_LFP_MIPI:
            self.panel2_index = self.gfx_vbt.block_40.PanelType2

        # whether dual link
        temp = self.gfx_vbt.block_52.MipiDataStructureEntry[self.panel1_index].DualLinkSupport
        if (temp == 0b01 or temp == 0b10):
            self.dual_link = 1

        # whether DSC or non-DSC configuration
        self.DSC_enabled = self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[self.panel1_index].CompressionEnable

        # if dual LFP MIPI, check whether port sync feature is enabled
        if self.dual_LFP_MIPI:
            if self.gfx_vbt.version >= 231:
                # Get LFP port sync bit from VBT based on panel
                panel1_port_sync_bit = (self.gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
                            1 << self.panel1_index)) >> self.panel1_index
                panel2_port_sync_bit = (self.gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
                            1 << self.panel2_index)) >> self.panel2_index
                if panel1_port_sync_bit == 1 and panel2_port_sync_bit == 1:
                    self.dual_LFP_MIPI_port_sync = 1
            else: # for vbt version lesser than 231 need to check block52 for port sync feature enabling
                if self.gfx_vbt.block_52.MipiDataStructureEntry[self.panel1_index].PortSyncFeature == 1 and \
                        self.gfx_vbt.block_52.MipiDataStructureEntry[self.panel2_index].PortSyncFeature == 1:
                    self.dual_LFP_MIPI_port_sync = 1

    ##
    # @brief        gets the appropriate panel index for the port
    # @param[in]    port port name of type string
    # @return       integer; returns panel index
    def get_panel_index_for_port(self, port):
        if port == "_DSI0":
            return self.panel1_index
        elif self.dual_link:
            return self.panel1_index
        else:
            return self.panel2_index

    ##
    # @brief         gets the mode of operation from VBT based on panel index
    # @param[in]     panel_index integer value indicating panel index
    # @return        integer; returns mode of operation
    def get_mode_of_operation(self, panel_index):
        mode_of_operation = NON_EXISTING
        if panel_index == NON_EXISTING:
            return NON_EXISTING

        if (self.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].VideoTransferMode != 0b00 and
                self.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].CommandMode == 0b0):
            mode_of_operation = VIDEO_MODE
        elif (self.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].CommandMode == 0b1):
            mode_of_operation = COMMAND_MODE
        else:
            gdhm.report_bug(
                title="[MIPI][VBT] Mode of operation from VBT is not correct",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Something wrong with VBT. Mode of operation is not correct.")
        return mode_of_operation

    ##
    # @brief        gets the bpp value from VBT based on panel index
    # @param[in]    panel_index integer value indicating panel index
    # @return       returns bpp (bits per pixel)
    def get_bpp(self, panel_index):
        if panel_index == NON_EXISTING:
            return NON_EXISTING

        VBT_pixel_format = self.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].VideoModeColorFormat
        if (VBT_pixel_format == 0b001):
            bpp = 16
        elif (VBT_pixel_format == 0b010 or VBT_pixel_format == 0b011):
            bpp = 18
        elif (VBT_pixel_format == 0b100):
            bpp = 24
        elif (VBT_pixel_format == 0b101):
            bpp = 30
        elif (VBT_pixel_format == 0b110):
            bpp = 36
        else:
            bpp = 0  # in case of non-video mode
        return bpp

    ##
    # @brief        gets the lane count value from VBT based on panel index
    # @param[in]    panel_index integer value indicating panel index
    # @return       integer; returns lane count
    def get_lane_count(self, panel_index):
        if panel_index == NON_EXISTING:
            return NON_EXISTING

        lane_count = self.gfx_vbt.block_52.MipiDataStructureEntry[
                         panel_index].NumberOfLanes + 1  # adding 1 since VBT stores as actual_lane_count - 1
        return lane_count

    ##
    # @brief        reads TRANS_DDI_FUNC_CTL register and returns the pipe connected to the passed DSI port.
    #               Applicable only for DSI.
    # @param[in]    port port name like '_DSI0' or '_DSI1'
    # @return       string; returns the literal of pipe connected to port
    def get_connected_pipe_to_dsi_port(self, port):

        trans_ddi_func_ctl = importlib.import_module("registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (self.platform))
        reg_ddi_func_ctl = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL" + port, self.platform)
        if reg_ddi_func_ctl.edp_dsi_input_select == getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_A"):
            return 'A'
        elif reg_ddi_func_ctl.edp_dsi_input_select == getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_B"):
            return 'B'
        elif reg_ddi_func_ctl.edp_dsi_input_select == getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_C"):
            return 'C'
        elif reg_ddi_func_ctl.edp_dsi_input_select == getattr(trans_ddi_func_ctl, "edp_dsi_input_select_PIPE_D"):
            return 'D'
        else:
            return 'None'

    ##
    # @brief        decodes the pixel format value as per Bspec.
    # @param[in]    pixel_format_decimal_value pixel format as decimal value (i.e register field value)
    # @return       string; returns the pixel format as a string
    def decode_pixel_format(self, pixel_format_decimal_value):
        if pixel_format_decimal_value == 0:
            return '16-bit RGB, 5-6-5'
        elif pixel_format_decimal_value == 1:
            return '18-bit RGB, 6-6-6 (Packed)'
        elif pixel_format_decimal_value == 2:
            return '18-bit RGB, 6-6-6 (Loose)'
        elif pixel_format_decimal_value == 3:
            return '24-bit RGB, 8-8-8'
        elif pixel_format_decimal_value == 4:
            return '30-bit RGB, 10-10-10'
        elif pixel_format_decimal_value == 5:
            return '36-bit RGB, 12-12-12'
        elif pixel_format_decimal_value == 6:
            return 'Compressed'
        else:
            return None

    ##
    # @brief        API to set brightness level (backlight) on LFP
    # @param[in]    brightness_level in percent. It takes values from 0 to 100.
    # @return        True if successful, False otherwise
    def set_lfp_brightness(self, brightness_level):
        if (brightness_level not in range(0, 101)):
            gdhm.report_bug(
                title="[MIPI][BRIGHTNESS] Invalid brightness level passed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('Invalid brightness level passed')
            return False

        # through powershell, using WMI object, set the brightness
        p = subprocess.Popen("powershell.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write("$myMonitor = get-WmiObject -Namespace root\wmi -Class WmiMonitorBrightnessMethods" + "\n")
        p.stdin.write("$myMonitor.WmiSetBrightness(0, " + str(brightness_level) + ")" + "\n")
        p.stdin.close()
        time.sleep(1)
        err = p.stderr.read()
        p.terminate()

        if (err != ''):
            logging.error(err)
            return False
        else:
            return True
