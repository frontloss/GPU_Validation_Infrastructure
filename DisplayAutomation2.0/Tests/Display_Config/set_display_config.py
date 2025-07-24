######################################################################################
# @file
# @section display_config
# @remarks
# <b> Test Name: SetDisplayConfig </b> <br>
# @ref set_display_config.py
# <ul>
# <li> <b> Description: </b> <br>
# @brief Common test to set display config with as per the command line parameters and verify presi crc<br>
# @details For this test using the customized edid which has only mode supported and edid_name will have mode information.
# </li>
#
# <li> <b> Execution Command(s) : </b> <br>
# <ul>
# <li> python set_display_config.py -edp_a (edid, dpcd) -dp_b (edid, dpcd)
# </li>
# <li> python set_display_config.py -edp_a (edid, dpcd) -dp_b (edid, dpcd) -hdmi_c (edid)
# </li>
# </ul>
# </li>
# @author gyd
######################################################################################
import logging
import os
import sys
import time
import unittest
from ctypes.wintypes import RGB

from Libs import env_settings
from Libs.Core import cmd_parser, display_utility, enum, display_essential
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature import crc_and_underrun_verification as underrun
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.presi import presi_crc, presi_crc_env_settings


##
# @brief SetDisplayConfig class : To be used in Set Display Config tests
class SetDisplayConfig(unittest.TestCase):
    cmd_line_param = None
    config = None
    connnector_port_list = []
    display_config = DisplayConfiguration()
    machine_info = SystemInfo()

    ##
    # @brief setUp() Run before execution of runTest()
    # @return None
    def setUp(self):
        ##
        # Parse cmd line
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                self.connnector_port_list.append(value)

        ##
        # Check required cmdline parameters are passed
        if self.cmd_line_param['CONFIG'] is None:
            logging.error("Require config single/clone/extended cmd line argument to run the test")
            self.fail("FAILED")
        # Minimum 1 display and Max 4 displays should be passed in cmd line arguments
        if 1 <= len(self.connnector_port_list) <= 4 is False:
            logging.error("Minimum 1 or Max 4 display cmd line arguments are required to run the test")
            self.fail("FAILED")

        ##
        # Start Underrun
        self.underrunstatus = underrun.UnderRunStatus()
        self.underrunstatus.clear_underrun_registry()

        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        time.sleep(30)

        ##
        # Check Underrun
        if self.underrunstatus.verify_underrun() is True:
            logging.error("Underrun observed after plugging displays.")

        ##
        # Is presi crc verification needed
        self.is_presi_crc = False
        silicon_type = env_settings.get('GENERAL', 'silicon_type')
        crc_presi_operation = env_settings.get('CRC', 'crc_presi')
        if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']
                and crc_presi_operation is not None and crc_presi_operation in ['CAPTURE', 'COMPARE']):
            self.is_presi_crc = True

        ##
        # Set background Color to Solid Color
        if self.is_presi_crc is True:
            color = RGB(20, 99, 177)  # Dark Blue
            presi_crc_env_settings.set_desktop_color(color)
            time.sleep(30)

    ##
    # @brief runTest defines the steps to be run for this test.
    # @details After setup, Execution of the test starts at this point
    # @return None
    def runTest(self):
        ##
        # Apply display configuration on the plugged displays based on command dictionary
        self.config = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        self.config_display_list = []
        for index in range(0, len(self.connnector_port_list)):
            self.config_display_list.append(self.connnector_port_list[index]['connector_port'])
        if self.display_config.set_display_configuration_ex(self.config,
                                                            self.config_display_list,
                                                            self.enumerated_displays) is False:
            self.fail('Failed to set the display configuration as %s %s' %
                      (DisplayConfigTopology(self.config).name, self.config_display_list))
        logging.info('Successfully set the display configuration as %s %s' %
                     (DisplayConfigTopology(self.config).name, self.config_display_list))

        verification_result = True
        # Display engine verification
        display_engine = DisplayEngine()
        verification_result &= display_engine.verify_display_engine()
        # CRC Verification
        verification_result &= self.verify_crc()
        if verification_result is False:
            self.fail("FAIL : Set Display Configuration Test")

    ##
    # @brief does crc check for all the active display ports
    # @return crc_status True/False
    def verify_crc(self):
        crc_status = True
        platform = None
        self.gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(self.gfx_display_hwinfo)):
            platform = self.gfx_display_hwinfo[i].DisplayAdapterName
            break
        if platform.upper() in ['TGL'] and self.is_presi_crc is True:
            crc_file_name = "%s_display_config.crc" % platform.lower()
            crc_file_path = os.path.join(test_context.TestContext.root_folder(),
                                         "Tests\\Display_Config\\crc\\%s" % crc_file_name)
            for index in range(0, len(self.connnector_port_list)):
                connector_port = self.connnector_port_list[index]['connector_port']
                edid_name = self.connnector_port_list[index]['edid_name']
                dpcd_name = self.connnector_port_list[index]['dpcd_name']
                mode_name = self.get_mode_name(connector_port, edid_name, dpcd_name)
                logging.info(" CAPTURE or VERIFY CRC For MODE %s" % mode_name)
                crc_status &= presi_crc.verify_or_capture_presi_crc(connector_port, crc_file_path, mode_name)
        return crc_status

    ##
    # @brief return the mode name based on current mode if edid is none,
    #               else returns the mode based on edid_name and dpdc_name
    # @param[in] connector_port  (Example : DP_B/HDMI_B/HDMI_C/....)
    # @param[in] edid_name EDID to be plugged
    # @param[in] dpcd_name DPCD to be used
    # @return mode_name name of the mode with Hzres Vtres and RR details present
    def get_mode_name(self, connector_port, edid_name, dpcd_name):
        mode_name = connector_port.split("_")[0]
        if edid_name is None:
            display_target_id = self.display_config.get_target_id(connector_port, self.enumerated_displays)
            current_display_mode = self.display_config.get_current_mode(display_target_id)
            mode_name += "_%s_%s_%sHz" % (str(current_display_mode.HzRes),
                                          str(current_display_mode.VtRes),
                                          str(current_display_mode.refreshRate))
        else:
            mode_name += "_%s" % edid_name.split(".")[0]
            if dpcd_name is not None:
                mode_name += "_%s" % dpcd_name.split(".")[0]
        return mode_name

    ##
    # @brief Unit-test teardown function.
    # @return None
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Check TDR
        result = display_essential.detect_system_tdr(gfx_index='gfx_0')
        self.assertNotEquals(result, True, "Aborting the test as TDR happened while executing the test")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
