########################################################################################################################
# @file         hdmi_mode_base.py
# @brief        It contains setUp and tearDown methods of unittest framework. In setUp,
#               we parse command_line arguments and then runTest() in the test script gets executed
#               In tearDown, Test clean up will take place.
# @author       Girish Y D
########################################################################################################################
from __future__ import division

import logging
import os
import sys
import time
import unittest
from ctypes.wintypes import RGB

from Libs import env_settings
from Libs.Core import cmd_parser, driver_escape, registry_access, display_essential
from Libs.Core import enum
from Libs.Core import system_utility as system_util
from Libs.Core.display_config import display_config as display_cfg
from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine import de_base_interface
from Libs.Feature.display_engine.de_master_control import DisplayEngine, VerificationMethod
from Libs.Feature.presi import presi_crc
from Libs.Feature.presi import presi_crc_env_settings
from Tests.Hdmi.utility.edid_mode_info import *
from Tests.Hdmi.verification.verify_helper import verify_register_programming


##
# @brief        HdmiModeBase Class
class HdmiModeBase(unittest.TestCase):
    my_custom_tags = ['-EDID_MODES_XML', '-MODE', '-PLATFORM', '-USE_BPC_REGISTRY', '-SKU']
    is_ycbcr_enabled = False

    # Color Format to BPP map
    colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25), ('RGB_12', 1.5),
                                  ('YUV444_8', 1), ('YUV444_10', 1.25), ('YUV444_12', 1.5),
                                  ('YUV420_8', 0.5), ('YUV420_10', 0.625), ('YUV420_12', 0.75)])

    ##
    # initialise the command line arguments to None
    cmd_args = None

    ###
    # display_list[] is list of displays passed in cmd line args
    display_list = []

    ##
    # List of plugged displays during execution
    plugged_displays = []

    ##
    # initialise platform as None
    platform = None

    ##
    # @brief       setUp function initialises the object and process the cmd line parameters.
    # @return      None
    def setUp(self):
        ##
        # Create DisplayConfiguration object
        self.display_config = display_cfg.DisplayConfiguration()
        ##
        # Create SystemUtility object
        self.system_utility = system_util.SystemUtility()

        ##
        # Create UnderRunStatus object
        self.under_run_status = UnderRunStatus()

        ##
        # Create SystemInfo Object
        self.machine_info = SystemInfo()

        ##
        # get  current enumerated  displays
        self.enumerated_displays = self.display_config.get_enumerated_display_info()

        ##
        # call get_gfx_display_hardware_info() to get the platform type from SystemInfo
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName)
            break

        ##
        # Process Command Line Arguments
        self.process_cmdline(self.my_custom_tags)

        if "PLATFORM" in self.custom_opt.keys():
            self.platform = self.custom_opt["PLATFORM"][0]

        if self.platform == 'ICLLP':
            self.platform = 'ICL'

        ##
        # Determine whether all display Ports passed in cmd line args available or not
        result = self.is_display_ports_supported(self.display_list)
        self.assertTrue(result, "Environment failure: all display ports passed in cmd line not available")

        ##
        # Start monitoring under-run
        self.under_run_status.clear_underrun_registry()

    ##
    # @brief        process_cmdline() processes the cmdline parameters.
    # @param[in]    custom_tags - Custom Tag
    # @return       None
    def process_cmdline(self, custom_tags):
        self.cmd_args = sys.argv
        self.cmd_dict = cmd_parser.parse_cmdline(self.cmd_args, custom_tags)
        self.config = self.cmd_dict['CONFIG']
        self.custom_opt = {}
        temp_custom_tags = []
        for custom_tag in custom_tags:
            temp_custom_tags.append(custom_tag[1:])

        for key, value in self.cmd_dict.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                self.display_list.append(value)
            elif key in temp_custom_tags and value != 'NONE':
                self.custom_opt[key] = value

    ##
    # @brief        Verify is display ports are available.
    # @param[in]    display_list - List of displays
    # @return       display_ports_supported_status - True is all hdmi ports mentioned in cmd line args is available
    def is_display_ports_supported(self, display_list):
        display_ports_supported_status = True
        port_list = display_cfg.get_supported_ports().keys()
        for display_panel in display_list:
            display_port = display_panel['connector_port']
            dispaly_port_supported = False
            for port in port_list:
                if display_port in port:
                    dispaly_port_supported = True
                    continue
            if dispaly_port_supported is True:
                logging.info("%s is Available", display_port)
            else:
                display_ports_supported_status &= False
                logging.error("ERROR: %s is not supported , If platform supports , check the VBT options",
                              display_port)
        return display_ports_supported_status

    ##
    # @brief        set_bpc_registry
    # @param[in]    bits_per_color - Bits per color specification
    # @param[in]    bpc_driver_hack_method - BPC Selection
    # @return       None
    def set_bpc_registry(self, bits_per_color, bpc_driver_hack_method="SelectBPC"):
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        if self.system_utility.is_ddrw():
            if bpc_driver_hack_method == "SelectBPC":
                key_name = "SelectBPC"
                value = 1
                if registry_access.write(args=ss_reg_args, reg_name=key_name,
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=value) is False:
                    self.fail()

                key_name = "SelectBPCFromRegistry"
                value = int(bits_per_color)
                if registry_access.write(args=ss_reg_args, reg_name=key_name,
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=value) is False:
                    self.fail()
        else:
            if bpc_driver_hack_method == "SelectBPC":
                key_name = "SelectBPCFromRegistry"
                value = 1
                if registry_access.write(args=ss_reg_args, reg_name=key_name,
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=value) is False:
                    self.fail()

                key_name = "SelectBPC"
                value = int(bits_per_color)
                if registry_access.write(args=ss_reg_args, reg_name=key_name,
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=value) is False:
                    self.fail()

            if bpc_driver_hack_method == "SelectMaxDisplayBPC":
                key_name = "SelectMaxDisplayBPC"
                value = '\1'
                if registry_access.write(args=ss_reg_args, reg_name=key_name,
                                         reg_type=registry_access.RegDataType.BINARY, reg_value=bytes(value)) is False:
                    self.fail()

    ##
    # @brief        clean bpc driver hack method registry
    # @return       None
    def clean_bpc_registry(self):
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        key_name = "SelectBPCFromRegistry"

        if registry_access.delete(args=ss_reg_args, reg_name=key_name) is False:
            self.fail()

        key_name = "SelectBPC"
        if registry_access.delete(args=ss_reg_args, reg_name=key_name) is False:
            self.fail()

        key_name = "SelectMaxDisplayBPC"
        if registry_access.delete(args=ss_reg_args, reg_name=key_name) is False:
            self.fail()

    ##
    # @brief        function calculates and returns Symbol clock Frequency
    #               for HDMI based on pixel format and Bites Per Color
    # @param[in]    pixel_clock_mhz - Pixel Clock in Mhz
    # @param[in]    pixel_format -  format of the pixels
    # @param[in]    bits_per_color - number of bits per colour
    # @return       symbol_clock_freq - Symbol Frequency
    def get_expected_symbol_clock_freq(self, pixel_clock_mhz, pixel_format, bits_per_color):
        color_format_value = str(pixel_format) + '_' + str(bits_per_color)
        color_divider = list(self.colorFormatDictionary.values())[
            list(self.colorFormatDictionary).index(color_format_value)]
        symbol_clock_freq = (pixel_clock_mhz * color_divider)
        return symbol_clock_freq

    ##
    # @brief        checks test_mode_list are enumerated by driver for the the display,
    #                   If unsupported_test param is False
    #               checks test_mode_list are not enumerated by driver for the the display,
    #                   If unsupported_test param is True
    # @param[in]    test_mode_list - is list of TestModeInfo()
    # @param[in]    display_port - Display Port
    # @param[in]    unsupported_test - Unsupported Test status
    # @return       bool -  If unsupported_test paramm is False;  returns True If modes are enumerated else false
    #                       If unsupported_test paramm is True;  returns True If modes are not enumerated  else false
    def verify_mode_enumeration(self, test_mode_list, display_port, unsupported_test=False):
        supported_string = "SUPPORTED"
        if unsupported_test is True:
            supported_string = "UNSUPPORTED"
        logging.info(
            "***%s MODE ENUMERATION VERIFICATION START FOR %s**************" % (supported_string, display_port))
        mode_enumeration_status = True
        if test_mode_list is None:
            mode_enumeration_status = False
            logging.error("FAIL : Test mode list in None")
        else:
            ##
            # Get the display Target ID
            display_target_id = self.display_config.get_target_id(display_port, self.enumerated_displays)

            ##
            # Get Supported /Enumerated Modes by driver for the display
            supported_mode_list = self.display_config.get_all_supported_modes([display_target_id], False)
            self.assertIsNotNone(supported_mode_list, "Modes query failed for %s " % display_port)
            driver_mode_list = supported_mode_list[display_target_id]

            for test_mode in test_mode_list:

                is_test_mode_enumerated = False
                for driver_mode in driver_mode_list:
                    if (int(test_mode.HzRes) == driver_mode.HzRes
                            and int(test_mode.VtRes) == driver_mode.VtRes
                            and int(test_mode.BPP) == driver_mode.BPP
                            and int(test_mode.refreshRate) == driver_mode.refreshRate
                            and int(test_mode.scanlineOrdering) == driver_mode.scanlineOrdering
                            and int(test_mode.scaling) == driver_mode.scaling
                            and int(test_mode.rotation) == driver_mode.rotation):
                        is_test_mode_enumerated = True
                        break
                if unsupported_test is True:
                    if is_test_mode_enumerated is False:
                        logging.info("PASS : Unsupported Mode NOT Enumerated : %s", test_mode)
                    else:
                        mode_enumeration_status = False
                        logging.error("FAIL : Unsupported Mode Enumerated : %s", test_mode)
                else:
                    if is_test_mode_enumerated is True:
                        logging.info("PASS : Mode Enumerated : %s", test_mode)
                    else:
                        mode_enumeration_status = False
                        logging.error("FAIL : Mode NOT Enumerated : %s", test_mode)
        logging.info("***%s MODE ENUMERATION VERIFICATION END FOR %s**************" % (supported_string, display_port))

        return mode_enumeration_status

    ##
    # @brief        sets the mode for display_port and checks pixel clock , does registers verification
    # @param[in]    test_mode_info - of Type TestModeInfo()
    # @param[in]    edid_info - of type HdmiEDIDInfo()
    # @return       bool - True if mode set and verify is passed else False
    def set_mode_and_verify(self, test_mode_info, edid_info):
        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.info("****************** SET MODE AND VERIFY *********************************************************")
        logging.info("SETTING BELOW %s_%sBPC MODE", test_mode_info.sourcePixelFormat, test_mode_info.sourceBPC)
        logging.info("%s", test_mode_info)

        silicon_type = env_settings.get('GENERAL', 'silicon_type')
        crc_presi_operation = env_settings.get('CRC', 'crc_presi')
        if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']
                and crc_presi_operation is not None and crc_presi_operation in ['CAPTURE', 'COMPARE']):
            color = RGB(20, 99, 177)  # Dark Blue
            presi_crc_env_settings.set_desktop_color(color)
            # presi_crc_env_settings.set_desktop_bg()
            time.sleep(30)

        ##
        # Get the expected symbol clock frequency based or pixelformat and Bits per color
        test_mode_info.expectedSymbolClockMHz = self.get_expected_symbol_clock_freq(
            test_mode_info.expectedPixelClockMHz,
            test_mode_info.expectedPixelFormat, test_mode_info.expectedBPC)

        ##
        # Get the display Target ID
        display_target_id = self.display_config.get_target_id(test_mode_info.display_port, enumerated_displays)

        ##
        # Create a object of DisplayMode() to be set from test_mode_info of Type TestModeInfo()
        display_mode = DisplayMode()
        display_mode.targetId = display_target_id
        display_mode.HzRes = int(test_mode_info.HzRes)
        display_mode.VtRes = int(test_mode_info.VtRes)
        display_mode.BPP = int(test_mode_info.BPP)
        display_mode.refreshRate = int(test_mode_info.refreshRate)
        display_mode.scanlineOrdering = int(test_mode_info.scanlineOrdering)
        display_mode.scaling = int(test_mode_info.scaling)
        display_mode.rotation = int(test_mode_info.rotation)

        ##
        # if source pixel format is YUV444, enable YcBcR
        # else make sure that YcBcr is disabled for RGB and YUV420 modes before setting the RGB or YUV420 modes
        ycbcr_supported = driver_escape.is_ycbcr_supported(display_target_id)
        if test_mode_info.sourcePixelFormat == "YUV444":
            if ycbcr_supported == 0:
                self.fail("YcBcr is not supported by %s EDID" % test_mode_info.display_port)
            ycbcr_enable_disable_status = driver_escape.configure_ycbcr(display_target_id, True)
            self.assertTrue(ycbcr_enable_disable_status, "YcBcR is not enabled for %s" % test_mode_info.display_port)
            logging.info("YcBCR Enabled for dislpay %s" % test_mode_info.display_port)
            self.is_ycbcr_enabled = True
        else:
            if ycbcr_supported:
                ycbcr_enable_disable_status = driver_escape.configure_ycbcr(display_target_id, False)
                self.assertTrue(ycbcr_enable_disable_status,
                                "YcBcR is not disabled for %s" % test_mode_info.display_port)

        self.clean_bpc_registry()
        driver_hack_method_to_set_bpc = "SelectBPC"
        self.set_bpc_registry(test_mode_info.sourceBPC, driver_hack_method_to_set_bpc)
        set_display_mode_status = self.display_config.set_display_mode([display_mode])

        # Check for the Post Silicon Execution Environment
        # If true execute the driver disable/enable
        if (self.system_utility.get_execution_environment_type() is not None
                and self.system_utility.get_execution_environment_type() not in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]):
            result, reboot_required = display_essential.restart_gfx_driver()
            self.assertEquals(result, True, "Display driver disable-enable failed")

        ##
        # Verify Mode
        if set_display_mode_status is True:
            current_display_mode = self.display_config.get_current_mode(display_target_id)
            if current_display_mode.status is enum.DISPLAY_CONFIG_SUCCESS:
                logging.info("Current applied mode is %s", current_display_mode.to_string(enumerated_displays))
                ##
                # Verify the current mode is set as expected
                if (display_mode == current_display_mode) is True and (
                        current_display_mode.pixelClock_Hz // (10 ** 6)) == int(test_mode_info.expectedPixelClockMHz):
                    logging.info("PASS : Current applied mode matches with expected mode to be set")

                    if self.platform.upper() in ['JSL', 'TGL', 'RYF', 'RKL']:
                        display_port_list = [test_mode_info.display_port]
                        display_pipe_list = [de_base_interface.DisplayPipe(display_port=test_mode_info.display_port,
                                                                           pipe_color_space=test_mode_info.expectedPixelFormat,
                                                                           hres=test_mode_info.HzRes,
                                                                           vres=test_mode_info.VtRes,
                                                                           )]
                        display_transcoder_list = []
                        LTE340MhzScramble = 0
                        if edid_info.LTE340MhzScramble is True:
                            LTE340MhzScramble = 1
                        if (test_mode_info.Hactive == 0 or test_mode_info.Vactive == 0 or
                                test_mode_info.Htotal == 0 or test_mode_info.Vtotal == 0 or
                                test_mode_info.refreshRate == 0 or test_mode_info.expectedPixelClockMHz == 0.0):
                            display_transcoder_list.append(
                                de_base_interface.DisplayTranscoder(display_port=test_mode_info.display_port,
                                                                    bpc=test_mode_info.expectedBPC,
                                                                    LTE340MhzScramble=LTE340MhzScramble))
                        else:
                            display_transcoder_list.append(
                                de_base_interface.DisplayTranscoder(display_port=test_mode_info.display_port,
                                                                    hactive=test_mode_info.Hactive,
                                                                    vactive=test_mode_info.Vactive,
                                                                    htotal=test_mode_info.Htotal,
                                                                    vtotal=test_mode_info.Vtotal,
                                                                    rrate=test_mode_info.refreshRate,
                                                                    bpc=test_mode_info.expectedBPC,
                                                                    LTE340MhzScramble=LTE340MhzScramble))

                        display_engine = DisplayEngine()
                        display_engine.remove_verifiers(VerificationMethod.POWERWELL)
                        display_engine.remove_verifiers(VerificationMethod.WATERMARK)
                        set_display_mode_status = display_engine.verify_display_engine(portList=display_port_list,
                                                                                       pipeList=display_pipe_list,
                                                                                       transcoderList=display_transcoder_list)
                    else:
                        set_display_mode_status &= verify_register_programming(test_mode_info, edid_info)

                    is_underrun_observed = self.under_run_status.verify_underrun()
                    if is_underrun_observed is True:
                        set_display_mode_status = False

                    logging.info("Calling CAPTURE or VERIFY CRC ")
                    set_display_mode_status &= self.verify_crc(test_mode_info)

                    # logging.info("Taking the Plane Processing Dumps")
                    # mmio_write(0x4f080, 1)
                    # logging.info("Completed Taking Plane Processing Dumps")

                else:
                    set_display_mode_status &= False
                    logging.error("Current applied mode doesn't match with expected mode to be set")
            else:
                set_display_mode_status &= False
                logging.error("Failed to get current mode for display %s",
                              current_display_mode.to_string(enumerated_displays))

        ##
        # Disable YcBcr , before proceeding  further; else next mode set will be YUV444
        if self.is_ycbcr_enabled is True:
            self.assertTrue(driver_escape.configure_ycbcr(display_target_id, False),
                            "Failed Disable Ycbcr for %s" % test_mode_info.display_port)

        if set_display_mode_status is False:
            logging.error("FAIL: Failed to set display mode %s" % test_mode_info)
        else:
            logging.info("PASS : Apply Mode : %s" % test_mode_info)
        logging.info("****************** SET MODE AND VERIFY END******************************************************")
        return set_display_mode_status

    ##
    # TODO: Currently, more clarification and rework is needed on the CRC Verification mechanism.
    # @brief        does crc check
    # @param[in]    test_mode_info - Test mode Information
    # @return       crc_status - CRC Status value
    def verify_crc(self, test_mode_info):
        crc_status = True
        if self.platform in ['LKF1', 'TGL']:
            silicon_type = env_settings.get('GENERAL', 'silicon_type')
            crc_presi_operation = env_settings.get('CRC', 'crc_presi')
            if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']
                    and crc_presi_operation is not None and crc_presi_operation in ['CAPTURE', 'COMPARE']):
                crc_file_name = "%s_hdmi_modes.crc" % self.platform.lower()
                crc_file_path = os.path.join(test_context.TestContext.root_folder(),
                                             "Tests\\Hdmi\\mode\crc\\%s" % crc_file_name)
                # mode_name , Example : "CEA_VIC1_RGB_8BPC_1920_1080_60p"
                mode_name_prefix = "CEA_VIC%d" % (int(test_mode_info.vic))
                if test_mode_info.edidModeCategory != "CEA":
                    mode_name_prefix = test_mode_info.edidModeCategory
                RROTATION_DICT_TEMP = {0: 'UNKNOWN_Deg', 1: '0Deg', 2: '90Deg', 3: '180Deg',
                                       4: '270Deg'}
                mode_name = "%s_%s_%sBPC_%d_%d_%d%s_%s_%s" % (mode_name_prefix,
                                                              test_mode_info.expectedPixelFormat,
                                                              test_mode_info.expectedBPC,
                                                              int(test_mode_info.HzRes),
                                                              int(test_mode_info.VtRes),
                                                              int(test_mode_info.refreshRate),
                                                              RSCANLINE_DICT[
                                                                  test_mode_info.scanlineOrdering][0],
                                                              RSCALING_DICT[test_mode_info.scaling],
                                                              RROTATION_DICT_TEMP[test_mode_info.rotation]
                                                              )
                logging.info(" CAPTURE or VERIFY CRC For MODE %s" % mode_name)
                crc_status &= presi_crc.verify_or_capture_presi_crc(test_mode_info.display_port, crc_file_path,
                                                                    mode_name)
        return crc_status

    ##
    # @brief        Cleans up the test
    # @return       None
    def tearDown(self):
        ##
        # Clean up BPC Registry
        self.clean_bpc_registry()

        logging.info("Test Clean Up")


if __name__ == '__main__':
    unittest.main()
