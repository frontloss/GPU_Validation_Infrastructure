#######################################################################################################################
# @file         test_emulator_mode_enum.py
# @brief        Contains test case to apply each mode and verify them
# @details      Test Scenario:
#                   1. If XML is provided in the cmd line, apply and verify all the modes obtained from XML
# @author       Gopi Krishna
#######################################################################################################################
import logging
import os
import time
import unittest
from typing import List

from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumXMLParser
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import DisplayMode, DisplayModeBlock, bpc_mapping, ColorFormat
from Tests.Emulator.emulator_test_base import EmulatorTestBase
from Tests.PowerCons.Modules import common
from Tests.VDSC.mode_enum_verifier import ModeEnumerationVerifier


##
# @brief        This class contains a test that does Mode Enumeration and Verification by using emulator to verify
#               the applied modes
class ModeEnumAndVerifyWithEmulator(EmulatorTestBase):
    display_configuration = DisplayConfiguration()

    ##
    # @brief        This test Plugs the Display, verifies if mode enumeration is success or not, if success, test
    #               applies all the modes and verifies each mode by using the values returned by emulator
    # @return       None
    @common.configure_test(selective=['XML_MODES'])
    def t_1_mode_enum_and_verify(self):

        self.port_list = self.emulator_command_parser.port_list
        logging.info("Port List in Command Line {}".format(self.port_list))

        iteration_count = int(self.emulator_command_parser.cmd_dict["ITERATION"][0])

        xml_file_from_cmd_dict = self.emulator_command_parser.cmd_dict["XML"]
        self.xml_file = xml_file_from_cmd_dict[0] if xml_file_from_cmd_dict != "NONE" else None

        # Iterating port list
        for port_name in self.port_list:
            gfx_adapter_info = GfxAdapterInfo()
            gfx_adapter_info.gfxIndex = 'gfx_0'

            # If XML file is provided in cmd line, apply all the golden modes and verify
            if self.xml_file is not None:
                # Parse the XML file
                xml_parser = ModeEnumXMLParser(gfx_adapter_info.gfxIndex, port_name, self.xml_file)

                # Getting EDID Info
                edid = xml_parser.edid_file

                edid_path = os.path.join(TestContext.panel_input_data(), 'HDMI', edid)

                logging.info("Edid name as per XML file: {}".format(edid))

                # Plug the display
                logging.info("Plugging Display on {}".format(port_name))
                if not self.she_utility.plug(gfx_adapter_info, port_name, edid_path, None, False, None):
                    self.fail("Plug not Successful on port {}".format(port_name))

                # Construct mode tables from the xml_parser
                xml_parser.parse_and_construct_mode_tables()

                # Looping for specified number of iterations in cmdline
                for counter in range(1, iteration_count + 1):
                    logging.info("{0} Iteration Count: {1} for {2} {0}".format("*" * 20, counter, port_name))

                    # Plug the display
                    logging.info("Plugging Display on {}".format(port_name))
                    if not self.she_utility.plug(gfx_adapter_info, port_name, edid_path, None, False, None):
                        self.fail("Plug not Successful on port {}".format(port_name))

                    # Verify if all Modes are enumerated correctly
                    is_success = ModeEnumerationVerifier.verify_enumerated_modes(xml_parser.gfx_index, port_name,
                                                            xml_parser.golden_mode_dict, xml_parser.ignore_mode_dict)

                    self.assertTrue(is_success, "[Driver Issue] - Verifying Mode Enumeration Failed for {}".format(port_name))
                    logging.info("Enumerated Modes and Golden Modes are Matching")

                    # Apply each mode and verify
                    is_success = self.apply_mode_and_verify_from_emulator(gfx_adapter_info.gfxIndex, port_name,
                                                                          xml_parser.apply_mode_list)

                    self.assertTrue(is_success, "[Driver Issue] - Mode Enumeration and Verification Failed on {}".format(port_name))
                    logging.info("Mode Enumeration and Verification Successful")

                    # Unplug display
                    logging.info("Unplugging Display on {}".format(port_name))
                    if not self.she_utility.unplug(gfx_adapter_info, port_name, False, None):
                        self.fail("UnPlug not Successful on port {}".format(port_name))

            else:
                self.fail("[Test Issue] - XML file is not provided in the command line")

    ##
    # @brief        Helper function to apply and verify all modes from provided in XML
    # @param[in]    gfx_index
    # @param[in]    port_name - port which is passed in command line
    # @param[in]    apply_mode_list which is obtained after parsing the XML
    # @return       status - True if Applying Modes and Verification success, False otherwise
    def apply_mode_and_verify_from_emulator(self, gfx_index, port_name, apply_mode_list: List[DisplayModeBlock]):
        reset_bpc = False
        f_status = True
        mds_scaling = 64

        emulator_ports = self.she_utility.display_to_emulator_port_map[port_name]
        emulator_port = emulator_ports[0]

        # Iterate Through Each of the Mode in Apply Mode Dict, Apply the Mode and Verify it.
        for display_mode_block in apply_mode_list:
            mode_to_apply: DisplayMode = display_mode_block.display_mode
            ModeEnumerationVerifier.log_display_modes("APPLYING:", {mode_to_apply})

            color_format = ColorFormat(display_mode_block.display_mode_control_flags.data.color_format).name
            logging.debug("Color Format from XML {}".format(color_format))

            # 0x1 - Represents 8 BPC, if anything else we need to set bpc using reg key
            bpc = display_mode_block.display_mode_control_flags.data.bpc

            bpc_from_xml = bpc_mapping[bpc]
            logging.debug("BPC to compare from XML {}".format(bpc_from_xml))

            if bpc != 0x1:
                bpc = bpc_mapping[bpc]
                is_success = DSCHelper.set_bpc_in_registry(gfx_index, bpc)
                self.assertTrue(is_success, "[Test Issue] - Setting BPC from Registry Failed")
                reset_bpc = True

            # Applying only MDS Modes
            if mode_to_apply.scaling == mds_scaling:
                is_success: bool = self.display_configuration.set_display_mode([mode_to_apply])
                self.assertTrue(is_success, "[Driver Issue] - Display Mode Set Failure for Current Mode")

                # Delay after applying the display mode
                time.sleep(10)

                status, rgb_values = self.she_utility.read_CRC_values_from_emulator(emulator_port, 1)
                rvalue, gvalue, bvalue = rgb_values[0][0], rgb_values[0][1], rgb_values[0][2]
                logging.debug(f'RValue: {rvalue} GValue: {gvalue} BValue: {bvalue}')

                # If blankout is not observed, Go for verification
                if rvalue != "0000" or gvalue != "0000" or bvalue != "0000":
                    logging.info("PASS: Non-Zero CRC found after Applying the Mode")

                    # Get Current Mode from OS
                    current_mode = self.display_configuration.get_current_mode(mode_to_apply.targetId)

                    # Read MSA values from Emulator
                    status, msa_values = self.she_utility.read_MSA_parameters_from_emulator(emulator_port)

                    # Verifying Values obtained from OS and Emulator
                    is_success = ModeEnumAndVerifyWithEmulator.is_mode_equal(current_mode, msa_values, bpc_from_xml)
                    self.assertTrue(is_success, "[Driver Issue] - Apply Mode and Verification Failed for Current Mode")

                # If blankout is observed, Show error and go to next Mode
                elif rvalue == "0000" and gvalue == "0000" and bvalue == "0000":
                    f_status = False
                    logging.error("Blankout Observed after applying the Mode,based on emulator CRC")

            else:
                logging.error("Applying only MDS Scaling Modes. Current Mode is Non MDS")

            # Disable the registry.
            if reset_bpc:
                reset_bpc = False
                is_success = DSCHelper.enable_disable_bpc_registry(gfx_index, enable_bpc=0)
                self.assertTrue(is_success, "[Test Issue] - Failed to Disable BPC registry")

        return f_status

    ##
    # @brief        Helper function which contains verification logic for values obtained from OS and values
    #               obtained from emulator
    # @param[in]    current_mode - Mode which is applied currently
    # @param[in]    msa_values - Values which are returned from emulator
    # @param[in]    bpc_from_xml - BPC value which is obtained form xml
    # @return       status - True if Verification of values is successful, False otherwise
    @staticmethod
    def is_mode_equal(current_mode, msa_values, bpc_from_xml):
        is_success = False

        logging.info(
            "Values From Current Mode : HZRes {} VtRes {}  RR {} ".format(current_mode.HzRes, current_mode.VtRes,
                                                                          round(current_mode.refreshRate)))

        logging.info(
            "Values From Emulator : HZRes {} VtRes {} BPC {} RR {} ".format(msa_values.X_value, msa_values.Y_value,
                                                                            msa_values.BPC,
                                                                            round(msa_values.refresh_rate)))

        # Comparing data from Current Mode against the data received from Emulator
        if (current_mode.HzRes == msa_values.X_value and current_mode.VtRes == msa_values.Y_value and
                bpc_from_xml == msa_values.BPC and (
                        current_mode.refreshRate == round(msa_values.refresh_rate) or
                        current_mode.refreshRate - 1 == round(msa_values.refresh_rate) or
                        current_mode.refreshRate + 1 == round(msa_values.refresh_rate))):
            is_success = True
            logging.info("Current Mode Matches with Expected Mode")
        else:
            logging.error("Current Mode does not Match with Expected Mode")

        return is_success


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(ModeEnumAndVerifyWithEmulator))
    test_environment.TestEnvironment.cleanup(test_result)
