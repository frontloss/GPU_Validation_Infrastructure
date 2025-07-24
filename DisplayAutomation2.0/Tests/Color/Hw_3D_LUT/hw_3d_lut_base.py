######################################################################################
# \file         hw_3d_lut_base.py
# \section      hw_3d_lut_base
# \remarks      This script contains helper functions that will be used by
#               Hardware 3D LUT test scripts
# \ref          hw_3d_lut_base.py \n
# \author       Soorya R, Smitha B
######################################################################################
import datetime
import sys
import unittest

from Libs.Core import reboot_helper, cmd_parser, display_utility, enum, driver_escape, system_utility as sys_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.wrapper.driver_escape_args import DppHwLutInfo, DppHwLutOperation
from Tests.Color.color_common_utility import gdhm_report_app_color
from Tests.Color.color_verification import *

gfx_display_hwinfo = SystemInfo().get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break


class Hw3DLUTBase(unittest.TestCase):
    connected_list = []
    driver_interface_ = driver_interface.DriverInterface()
    utility = sys_utility.SystemUtility()
    config = display_config.DisplayConfiguration()
    platform = None
    internal_gfx_adapter_index = 'gfx_0'

    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        enumerated_display = self.config.get_enumerated_display_info()
        self.connected_list = [0] * enumerated_display.Count
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list[value['index']] = value['connector_port']

        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

    ##
    # Get display type from the connector port
    def get_display(self, connector_port_type):
        return {'DP_B': enum.DP_1,
                'DP_C': enum.DP_2,
                'DP_D': enum.DP_3,
                'HDMI_B': enum.HDMI_1,
                'HDMI_C': enum.HDMI_2
                }[connector_port_type]

    def get_value(self, value, start, end):
        ret_value = (value << (31 - end)) & 0xFFFFFFFF
        ret_value = (ret_value >> (31 - end + start)) & 0xFFFFFFFF
        return ret_value

    def get_current_pipe(self, display):
        display_base_obj = DisplayBase(display)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
        current_pipe_notation = chr(int(current_pipe) + 65)
        logging.info("Current pipe : Pipe %s ", current_pipe_notation)
        return current_pipe_notation

    def perform_plane_processing(self):
        logging.info("Performing plane processing")
        ##
        # These registers are used as scratch pad data storage space
        swf_offset = 0x4f080
        value = 0x3
        self.driver_interface_.mmio_write(swf_offset, value, 'gfx_0')

    def wait_for_frame_cntr_incr(self, current_pipe):
        pipe_frame_cntr_val_incr = 0
        pipe_frm_cntr = ' PIPE_FRMCNT_' + current_pipe
        instance = MMIORegister.get_instance('PIPE_FRMCNT_REGISTER', pipe_frm_cntr, platform)
        pipe_frm_cntr_offset = instance.offset
        pipe_frame_cntr = 0x70040 + (0x1000 * 1)
        pipe_frame_cntr_val_initial = self.driver_interface_.mmio_read(pipe_frm_cntr_offset, 'gfx_0')

        while pipe_frame_cntr_val_incr - pipe_frame_cntr_val_initial < 2:
            time.sleep(10)
            pipe_frame_cntr_val_incr = self.driver_interface_.mmio_read(pipe_frame_cntr, 'gfx_0')
        return

    def resetLUTReady(self, display):
        # lut_3d_ctl = importlib.import_module("registers.%s.LUT_3D_CTL_REGISTER" % (platform))
        current_pipe = self.get_current_pipe(display)
        lut_3d_ctl_reg = 'LUT_3D_CTL' + '_' + current_pipe
        instance = MMIORegister.get_instance('LUT_3D_CTL_REGISTER', lut_3d_ctl_reg, platform)
        lut_3d_ctl_reg_offset = instance.offset
        lut_ctl_val = self.driver_interface_.mmio_read(lut_3d_ctl_reg_offset, 'gfx_0') & 0xBFFFFFFF
        logging.info("Current LUT Ctrl Vlaues : %s" % hex(lut_ctl_val))

    def get_new_lut_ready_status(self, lut_reg, platform):
        instance = MMIORegister.get_instance('LUT_3D_CTL_REGISTER', lut_reg, platform)
        lut_3d_ctl_reg_offset = instance.offset
        new_lut_ready_status = (self.driver_interface_.mmio_read(lut_3d_ctl_reg_offset, 'gfx_0') >> 30) & 1
        return new_lut_ready_status

    def verify_hw_reset_status(self, lut_3d_ctl_reg, platform):
        milliseconds = 0.005
        expected_resettime_limit = 15
        status = 1
        start_time = datetime.datetime.now()
        while status != 0:  # Expecting this loop should not go infinite
            status = self.get_new_lut_ready_status(lut_3d_ctl_reg, platform)
            if status != 0:
                logging.debug(
                    "Still H/W not resetted the new_lut_ready bit, will read the status again post 5 ms")
                time.sleep(milliseconds)
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).total_seconds() * 1000  # Convert seconds to milliseconds
        if total_time > expected_resettime_limit:
            logging.info(
                "Expected: less than 15 ms and Actual time taken :{0} ms -hw failed to reset the new_lut_ready bit "
                "within 15 ms".format(total_time))
            gdhm_report_app_color(title="[COLOR][hw_3d_lut] Hardware failed to reset the new_lut_ready bit within 15 ms")
        else:
            logging.info("Expected: less than 15 ms and Actual time taken: {0} ms - hw resetted the new_lut_ready bit"
                         " within 15 ms".format(total_time))
        return status == 0

    def verify_3dlut(self, current_pipe, input_file, enable_3dlut=True):
        hw_lut_buffer_status = "NOT_LOADED"
        hw_3d_lut_status = "DISABLED"
        lut_3d_ctl_reg = 'LUT_3D_CTL' + '_' + current_pipe
        instance = MMIORegister.get_instance('LUT_3D_CTL_REGISTER', lut_3d_ctl_reg, platform)
        lut_3d_ctl_reg_offset = instance.offset

        ##
        # LUT INDEX REGISTER
        lut_index_reg = 'LUT_3D_INDEX' + '_' + current_pipe
        instance = MMIORegister.get_instance('LUT_3D_INDEX_REGISTER', lut_index_reg, platform)
        lut_index_reg_offset = instance.offset

        ##
        # LUT DATA REGISTER
        lut_data_reg = 'LUT_3D_DATA' + '_' + current_pipe
        instance = MMIORegister.get_instance('LUT_3D_DATA_REGISTER', lut_data_reg, platform)
        lut_data_reg_offset = instance.offset

        self.driver_interface_.mmio_write(lut_index_reg_offset, 0x00002000, 'gfx_0')
        lut_3d_enable = self.driver_interface_.mmio_read(lut_3d_ctl_reg_offset, 'gfx_0') >> 31
        if lut_3d_enable:
            if enable_3dlut:
                logging.info("Hw 3D LUT is enabled on pipe %c", current_pipe)
                hw_3d_lut_status = "Enabled"
                new_lut_ready_status = self.verify_hw_reset_status(lut_3d_ctl_reg, platform)
                if new_lut_ready_status is True:
                    hw_lut_buffer_status = "Finished"
                else:
                    hw_lut_buffer_status = "NOT_LOADED"
                    return hw_3d_lut_status, hw_lut_buffer_status
                prog_lut = []
                for i in range(0, 4913):
                    reg_data_offset = self.driver_interface_.mmio_read(lut_index_reg_offset, 'gfx_0') & 0xFFF
                    reg_val_lut_3d_data = self.driver_interface_.mmio_read(lut_data_reg_offset, 'gfx_0')
                    reg_blue = self.get_value(reg_val_lut_3d_data, 0, 9)
                    reg_green = self.get_value(reg_val_lut_3d_data, 10, 19)
                    reg_red = self.get_value(reg_val_lut_3d_data, 20, 29)
                    prog_lut.append(reg_red)
                    prog_lut.append(reg_green)
                    prog_lut.append(reg_blue)
                self.verify_lut_data(prog_lut, input_file)
            else:
                logging.error("Failed to disable HW3DLUT with enable status of HW_3D_LUT:%s" % enable_3dlut)
                hw_3d_lut_status = "DISABLED"
        else:
            if not enable_3dlut:
                logging.info("HW 3D LUT is disabled successfully on pipe %s" % current_pipe)
            else:
                logging.error("Hw 3D LUT is disabled on pipe %s" % current_pipe)
            hw_3d_lut_status = "DISABLED"
        self.driver_interface_.mmio_write(lut_index_reg_offset, 0x00000000, 'gfx_0')
        return hw_3d_lut_status, hw_lut_buffer_status

    def verify_lut_data(self, prog_lut, input):
        logging.info("Input file is %s" % input)
        red_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                    0x300, 0x340, 0x380, 0x3C0, 0x3FC]
        green_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                      0x300, 0x340, 0x380, 0x3C0, 0x3FC]
        blue_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                     0x300, 0x340, 0x380, 0x3C0, 0x3FC]
        ref_lut = []
        count = 0
        if (input == "CustomLUT_no_R.bin"):
            for i in range(0, 17):
                red_data[i] = 0
        elif (input == "CustomLUT_no_G.bin"):
            for i in range(0, 17):
                green_data[i] = 0
        elif (input == "CustomLUT_no_B.bin"):
            for i in range(0, 17):
                blue_data[i] = 0
        for i in range(0, 17):
            for j in range(0, 17):
                for k in range(0, 17):
                    ref_lut.append(red_data[i])
                    ref_lut.append(green_data[j])
                    ref_lut.append(blue_data[k])
                    count = count + 3
        index = 0
        for reg_val, ref_val in zip(prog_lut, ref_lut):
            if (reg_val != ref_val):
                logging.error("LUT values not matching Index : %d ProgrammedVal : %d Expected val : %d ", index,
                              reg_val, ref_val)
                self.fail()
            index += 1

    def enable_disabe_hw3dlut(self, current_pipe, target_id_list, depth_list, lut_file_list, enable_status=True):
        for index in range(0, len(target_id_list)):
            cui_dpp_hw_lut_info = DppHwLutInfo(target_id_list[index], DppHwLutOperation.UNKNOWN.value,
                                               depth_list[index])
            if cui_dpp_hw_lut_info.convert_lut_data(lut_file_list[index]) is False:
                self.fail(f'Invalid bin file path provided : {lut_file_list}!')
            else:
                if enable_status:
                    cui_dpp_hw_lut_info.opType = DppHwLutOperation.APPLY_LUT.value
                else:
                    cui_dpp_hw_lut_info.opType = DppHwLutOperation.DISABLE_LUT.value

                result = driver_escape.set_dpp_hw_lut(self.internal_gfx_adapter_index, cui_dpp_hw_lut_info)
                if result is False:
                    logging.error(f'Escape call failed : set_dpp_hw_lut() for {target_id_list[index]}')
                exec_env = sys_utility.SystemUtility().get_execution_environment_type()
                if exec_env == 'SIMENV_FULSIM':
                    self.perform_plane_processing()
                    ##
                    # Wait for the hardware to finish loading the LUT buffer into internal working RAM
                    time.sleep(120)

                elif exec_env != 'SIMENV_FULSIM' and exec_env != 'POST_SI_ENV':
                    self.wait_for_frame_cntr_incr(current_pipe)

    def gdhm_hw_3d_lut_logging_check(self, hw_3d_lut_status, hw_lut_buffer_status,pipe_status,expected_hw_3d_lut_status, expected_hw_lut_buffer_status,expected_pipe_status):
        if expected_hw_3d_lut_status is not None:
            if hw_3d_lut_status == expected_hw_3d_lut_status:
                gdhm_report_app_color(
                    title="[COLOR][hw_3d_lut]Verification of HW_3D_LUT failed due to 3D_LUT status: %s" % hw_3d_lut_status)
                return False
        if expected_hw_lut_buffer_status is not None:
            if hw_lut_buffer_status == expected_hw_lut_buffer_status:
                gdhm_report_app_color(
                    title="[COLOR][hw_3d_lut]Hardware did not load the lut buffer into internal working RAM")
                return False
        if expected_pipe_status is not None:
            if pipe_status == expected_pipe_status:
                gdhm_report_app_color(
                    title="[COLOR][hw_3d_lut]Verification of HW_3D_LUT failed due to pipe: Disabled")
                return False
        return True


    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)
