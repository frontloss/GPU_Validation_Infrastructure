#######################################################################################################################
# @file         test_emulator_hdr.py
# @brief        Contains test cases to Verify HDR Data from sink side (Emulator)
# @details      Test Scenario:
#                   1. Plug the Display
#                   2. Enable HDR and verify from sink side if HDR is enabled
#                   3. Disable HDR and verify from sink side if HDR is disabled
#                   4. Unplug the Display
# @author       Gopi Krishna
#######################################################################################################################
import logging
import os
import time
import unittest

from Libs.Core import display_utility
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.test_context import TestContext
from Tests.Emulator.emulator_test_base import EmulatorTestBase
from Tests.PowerCons.Modules import common


##
# @brief        This class contains a test that does Enable/Disable of OS HDR and then gets the HDR status from
#               emulator to check if HDR content is available from the sink side or not
class HDMIHdrWithEmulator(EmulatorTestBase):

    ##
    # @brief        This test Plugs the Display, enables the HDR, gets and verifies the HDR status from emulator.
    #               Then Disables the HDR, gets and verifies HDR status from Emulator, Unplugs the display for
    #               specified number of iterations
    # @return       None
    # @cond
    @ common.configure_test(selective=['HDR'])
    # @endcond
    def t_1_enable_disable_hdr(self):

        # Gets the List of HDMI Ports that are passed in cmd line
        self.hdmi_port_list = self.emulator_command_parser.hdmi_port_list
        logging.info("HDMI Port List {}".format(self.hdmi_port_list))

        iteration_count = int(self.emulator_command_parser.cmd_dict["ITERATION"][0])

        # Iterating HDMI port list
        for hdmi_port in self.hdmi_port_list:
            emulator_ports = self.she_utility.display_to_emulator_port_map[hdmi_port]
            emulator_port = emulator_ports[0]

            # Get Panel Index from cmd line dictionary
            panel_index = self.emulator_command_parser.cmd_dict[hdmi_port]['panel_index']
            gfx_adapter_info = GfxAdapterInfo()
            gfx_adapter_info.gfxIndex = 'gfx_0'

            # Getting EDID Info as per panel index
            data = display_utility.get_panel_edid_dpcd_info(port=hdmi_port, panel_index=panel_index)
            edid = data['edid']
            edid_path = os.path.join(TestContext.panel_input_data(), 'HDMI', edid)

            logging.info("Edid name as per panel index: {}".format(edid))

            # Looping for specified number of iterations in cmdline
            for counter in range(1, iteration_count + 1):
                logging.info("{0} Iteration Count: {1} for {2} {0}".format("*" * 20, counter, hdmi_port))

                # Plug the display
                logging.info("Plugging Display on {}".format(hdmi_port))
                if not self.she_utility.plug(gfx_adapter_info, hdmi_port, edid_path, None, False, None):
                    self.fail("Plug not Successful on port {}".format(hdmi_port))

                # Enabling HDR
                logging.info("Enabling OS HDR on {}".format(hdmi_port))
                is_success = self.enable_or_disable_os_hdr(hdmi_port, True)
                self.assertTrue(is_success, "OS HDR Enable Failure on {}".format(hdmi_port))
                logging.info("OS HDR Enable Success on {}".format(hdmi_port))

                # Giving delay before reading the data from emulator
                time.sleep(3)

                # Getting HDR Status from Emulator to verify if HDR is Enabled
                status, hdr_status = self.she_utility.get_hdr_status_from_emulator(emulator_port)
                logging.info("HDR Status from Emulator: {}".format(hdr_status))

                self.assertTrue(hdr_status, "FAIL: HDR Data not received from Emulator")
                logging.info("PASS: HDR Data Received from Emulator {}".format(emulator_port))

                # Disabling HDR
                logging.info("Disabling OS HDR on {}".format(hdmi_port))
                is_success = self.enable_or_disable_os_hdr(hdmi_port, False)
                self.assertTrue(is_success, "OS HDR Disable Failure on {}".format(hdmi_port))
                logging.info("OS HDR Disable Success on {}".format(hdmi_port))

                # Giving delay before reading the data from emulator
                time.sleep(3)

                # Getting HDR Status from Emulator to verify if HDR is Disabled
                status, hdr_status = self.she_utility.get_hdr_status_from_emulator(emulator_port)
                logging.info("HDR Status from Emulator: {}".format(hdr_status))

                self.assertTrue(hdr_status, "FAIL: HDR Data received from Emulator")
                logging.info("PASS: HDR Data not Received from Emulator {}".format(emulator_port))

                # Unplug the Display
                logging.info("Unplugging Display on {}".format(hdmi_port))
                if not self.she_utility.unplug(gfx_adapter_info, hdmi_port, False, None):
                    self.fail("UnPlug not Successful on port {}".format(hdmi_port))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(HDMIHdrWithEmulator))
    test_environment.TestEnvironment.cleanup(test_result)