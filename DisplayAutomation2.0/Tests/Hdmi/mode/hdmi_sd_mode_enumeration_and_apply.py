########################################################################################################################
# @file         hdmi_sd_mode_enumeration_and_apply.py
# @brief        This file implements the HDMI Single Display Mode Enumeration and Apply the same
# @remarks
# /ref hdmi_sd_mode_enumeration_and_apply.py /n
# 1) This test ensure Driver is Enumerating mode list properly for the given hdmi edid and
#    ensure no regressions seen in Mode Enumeration logic
#    - List of modes to be enumerated is provided in xml
#    - List of modes not supported by a platform is provided in xml
# 2) This test with apply all modes which are listed in the Apply mode table of xml provided
#    - If the Mode Name to be applied is passed in command line args,
#           this test will check Mode name exists in Apply mode table of xml provided and apply the mode
# 3) This test will verify clock, pipe, transcoder, DDI mmio registers and checks for underrun for each mode set
# 4) @todo Verify CRC
#   Command line : python Tests\Hdmi\mode\hdmi_sd_mode_enumeration_and_apply.py [HDMI_B/HDMI_C/..]
#                                                                           [EDID_MODES_XML] [MODE] [USE_BPC_REGISTRY]
#   or
#   Command line : python Tests\Hdmi\mode\hdmi_sd_mode_enumeration_and_apply.py [HDMI_B/HDMI_C/..] [EDID MODES XML]
# @author           Girish Y D
########################################################################################################################
import os
import sys

from Libs.Core import display_utility
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if not os.path.exists(root_dir):
    sys.path.append(root_dir)
from Tests.Hdmi.mode.hdmi_mode_base import *
from Tests.Hdmi.utility.edid_modes_xml_parser import *


##
# @brief        HdmiSDModeEnumerationAndApply Class
class HdmiSDModeEnumerationAndApply(HdmiModeBase):
    ##
    # @brief        setUp - will inherit the instances from the setUp() of HdmiModeBase
    # @return       None
    def setUp(self):

        super(HdmiSDModeEnumerationAndApply, self).setUp()
        self.config = display_cfg.DisplayConfiguration()
        ##
        # Check only 1 display panel input  is received in cmd line
        self.assertEqual(len(self.display_list), 1, "None or more than 1 display panel input received")

        ##
        # Abort Test, if edid modes xml is not provided in command-line
        edid_modes_xml_file_name = None
        if "EDID_MODES_XML" in self.custom_opt.keys():
            edid_modes_xml_file_name = self.custom_opt["EDID_MODES_XML"][0]
        self.assertIsNotNone(edid_modes_xml_file_name, "Aborting the test as xml file is not provided in command-line")
        self.edid_modes_xml_path = os.path.join(test_context.TestContext.root_folder(),
                                                'Tests\Hdmi\mode\edid_modes_xml',
                                                edid_modes_xml_file_name)

        # Unplug all the external displays connected apart from eDP/MIPI
        enumerated_displays = self.config.get_enumerated_display_info()
        for idx in range(enumerated_displays.Count):
            disp_config = enumerated_displays.ConnectedDisplays[idx]
            if disp_config.ConnectorNPortType not in [enum.DP_A, enum.MIPI_A, enum.MIPI_C]:
                display_port = CONNECTOR_PORT_TYPE(disp_config.ConnectorNPortType)
                display_port = str(display_port)
                result = display_utility.unplug(display_port)
                # self.assertTrue(result, "Failed to unplug simulated %s display" % display_port)
                if self.plugged_displays is not None and display_port in self.plugged_displays:
                    self.plugged_displays.remove(display_port)

        self.enumerated_displays = self.config.get_enumerated_display_info()

    ##
    # @brief        Test run
    # @return       None
    def runTest(self):
        self.run_status = True
        ##
        # Plug display
        display_panel = self.display_list[0]
        display_port = display_panel['connector_port']
        edid_file = display_panel['edid_name']
        if self.system_utility.is_ddrw():
            edid_path = os.path.join(test_context.TestContext.panel_input_data(), "HDMI",
                                     edid_file.split(".")[0] + "_SCDC." + edid_file.split(".")[1])
            if os.path.exists(edid_path):
                edid_file = edid_file.split(".")[0] + "_SCDC." + edid_file.split(".")[1]

            logging.debug("EDID File : %s" % edid_file)

        result = display_utility.plug(display_port, edid_file)
        self.assertTrue(result, "Failed to plug simulated display panel to %s" % display_port)
        # Added Delay as HDMI2.0 EDID takes long time
        time.sleep(20)

        self.enumerated_displays = self.config.get_enumerated_display_info()
        result = display_cfg.is_display_attached(self.enumerated_displays, display_port)
        self.assertTrue(result, "%s Display is not attached" % display_port)
        logging.info("PASS : Plugged display to %s" % display_port)
        self.plugged_displays.append(display_port)

        ##
        # Set Single display Display config With display passed
        result = self.display_config.set_display_configuration_ex(enum.SINGLE, [display_port], self.enumerated_displays)
        self.assertTrue(result, "Failed to perform SD config for %s " % display_port)
        logging.info("PASS : Switch to config - SD %s" % display_port)
        # Added Delay as HDMI2.0 Mode takes long time to set
        time.sleep(20)

        ##
        # Get modes from XML which are supported by platform and verify modes are enumerated by driver
        test_mode_enumeration_list = HdmiEdidModesXmlParser().get_edid_mode_enumeration_list(self.edid_modes_xml_path,
                                                                                             self.platform)
        mode_enumeration_status = self.verify_mode_enumeration(test_mode_enumeration_list, display_port)
        self.assertTrue(mode_enumeration_status, " MODE ENUMERATION VERIFICATION FAILED, skipping Apply modes")
        logging.info("MODE ENUMERATION VERIFICATION PASSED")
        self.run_status &= mode_enumeration_status

        ##
        # Get modes from xml which are not supported by platform
        # If there is unsupported modes and verify modes are not enumerated by driver
        unsupported_mode_list = HdmiEdidModesXmlParser().get_unsupported_mode_list(self.edid_modes_xml_path,
                                                                                   self.platform)
        if unsupported_mode_list is not None:
            unsupported_mode_enumeration_status = self.verify_mode_enumeration(unsupported_mode_list, display_port,
                                                                               unsupported_test=True)
            if unsupported_mode_enumeration_status is True:
                logging.info("UNSUPPORTED MODE ENUMERATION VERIFICATION PASSED")
            else:
                logging.error("UNSUPPORTED MODE ENUMERATION VERIFICATION FAILED")
            self.run_status &= unsupported_mode_enumeration_status

        ##
        # Apply the Mode
        # If "MODE" is passed as command line arguments
        # ---If "MODE" is  ALL_DEEP_COLOR_MODES, set all the modes which are listed in DeepcolorModes nodes of EDIDMODES XML
        # ---else If "MODE" is exists in apply mode list, set the  the mode
        # else
        # ---Set all Edid Modes which are in Apply mode list of EDIDMODES XML
        edid_info = HdmiEdidModesXmlParser().get_edid_info_from_xml(self.edid_modes_xml_path)
        if "MODE" in self.custom_opt.keys():
            mode_name = self.custom_opt["MODE"][0]
            if mode_name == "ALL_DEEP_COLOR_MODES":
                deep_color_mode_info_list = HdmiEdidModesXmlParser().get_apply_deep_color_mode_list(
                    self.edid_modes_xml_path, self.platform)
                self.assertIsNotNone(deep_color_mode_info_list,
                                     "Aborting the test as Deep color Modes doesn't exist in Apply Mode  table of EDID_MODES_XML")

                for test_mode_info in deep_color_mode_info_list:
                    test_mode_info.display_port = display_port
                    self.run_status &= self.set_mode_and_verify(test_mode_info, edid_info)
                    time.sleep(10)
            else:
                ##
                # Get all the modes from xml which need to be set and check mode_name exists
                # if mode_name exists set
                is_mode_exists = False
                apply_mode_list = HdmiEdidModesXmlParser().get_apply_mode_list(self.edid_modes_xml_path, self.platform)
                for test_mode_info in apply_mode_list:
                    if mode_name == test_mode_info.modeName:
                        is_mode_exists = True
                        test_mode_info.display_port = display_port
                        self.run_status &= self.set_mode_and_verify(test_mode_info, edid_info)
                        time.sleep(10)
                        break
                self.assertTrue(is_mode_exists,
                                "Aborting the test as MODE %s doesn't exist in Apply Mode table of EDID_MODES_XML" % mode_name)
        else:
            ##
            # Get edid modes from xml which need to be set and set the all modes
            apply_edid_mode_list = HdmiEdidModesXmlParser().get_apply_edid_mode_list(self.edid_modes_xml_path,
                                                                                     self.platform)
            self.assertIsNotNone(apply_edid_mode_list,
                                 "Aborting the test as apply moes doesn't exist in Apply Mode  table of EDID_MODES_XML")
            for test_mode_info in apply_edid_mode_list:
                test_mode_info.display_port = display_port
                self.run_status &= self.set_mode_and_verify(test_mode_info, edid_info)
                time.sleep(10)

        if self.run_status is False:
            self.fail("FAIL : HdmiSDModeEnumerationAndApply ")

    ##
    # @brief        Cleans up the test
    # @return       None
    def tearDown(self):
        ##
        # Unplug the displays which are plugged
        if self.plugged_displays is not None:
            for i in range(len(self.plugged_displays)):
                display_port = self.plugged_displays.pop()
                result = display_utility.unplug(display_port)
                # self.assertTrue(result, "Failed to unplug simulated %s display" % display_port)
                # TODO Remove the above commented assetTrue once api to check the presilicon or post silicon for mainline is checked in

        super(HdmiSDModeEnumerationAndApply, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
