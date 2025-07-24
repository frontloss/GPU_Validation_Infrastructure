########################################################################################################################
# @file         immediate_flips.py
# @brief        The script implements unittest default functions for setUp and tearDown, and  common helper functions
#               given below:
#               * Verify whether flip is asynchronous or not.
#               * Verify whether registry entry to enable immediate flips is passing or not.
#               * Verify display configuration is properly applied or not.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import os
import subprocess
import sys
import time
import unittest

from Libs.Core import cmd_parser, registry_access
from Libs.Core import display_utility
from Libs.Core import reboot_helper, enum
from Libs.Core import winkb_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Core.logger import gdhm


##
# register offset
# @brief    register offset
class Offset(object):
    MSG_FLIP_SURF_PLANE_1_A = 0x50080
    MSG_FLIP_SURF_PLANE_1_B = 0x50088
    MSG_FLIP_SURF_PLANE_1_C = 0x5008c


asynchronous_flip = 0b01

##
# @brief        Contains helper function to verify if the flip is asynchronous while playing a 3D app
class ImmediateFlips(unittest.TestCase):
    connected_list = []
    app = None

    @reboot_helper.__(reboot_helper.setup)

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if len(self.connected_list) <= 0:
            gdhm.report_bug(
                title="[Immediate Flips]Invalid displays provided in command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Minimum 1 display is required to run the test")
            self.fail()


    ##
    # @brief            Verify whether flip is asynchronous or not
    # @param[in]        display
    # @param[in]        msg_flip_reg
    # @param[in]        flip
    # @return           void
    def verify(self, display, msg_flip_reg, flip):
        display_base_obj = DisplayBase(display)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
        current_pipe = chr(int(current_pipe) + 65)
        msg_flip_surf_reg = msg_flip_reg + '_' + current_pipe
        offset = getattr(Offset, msg_flip_surf_reg)
        for i in range(10):
            msg_flip_surf_reg_value = driver_interface.DriverInterface().mmio_read(offset, 'gfx_0')
            flip = msg_flip_surf_reg_value & 0x03
            if (flip == asynchronous_flip):
                logging.info("Asynchronous Flip")
            else:
                logging.info("Not Asynchronous Flip")


    ##
    # @brief            Test before reboot
    # @return           void
    def test_before_reboot(self):
        logging.info("Before reboot")
        ##
        # to add the registry entry to enable immediate flips
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                        reg_path=r"System\CurrentControlSet\Control")
        if registry_access.write(args=legacy_reg_args, reg_name="ForceFlipTrueImmediateMode",
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=2,
                                 sub_key=r"GraphicsDrivers\Scheduler") is False:
            logging.error("Writing to the Registry Failed")

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")


    ##
    # @brief            Test after reboot
    # @return           void
    def test_after_reboot(self):
        logging.info("After reboot")
        config = DisplayConfiguration()

        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE
        ##
        # apply SINGLE display configuration across all the displays
        for display_index in range(len(self.connected_list)):
            if config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info("Successfully applied the configuration")
                ##
                # open the 3d app
                self.app = subprocess.Popen(r'TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3d.exe darken',
                                            cwd=os.path.join(TestContext.bin_store(), 'ClassicD3D'))
                time.sleep(5)
                winkb_helper.press('F5')
                ##
                # verify if the flip is asynchronous
                self.verify(self.connected_list[display_index], 'MSG_FLIP_SURF_PLANE_1', asynchronous_flip)
                time.sleep(10)

    @reboot_helper.__(reboot_helper.teardown)


    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        ##
        # close the 3d app
        self.app.terminate()
        logging.info("Test Clean Up")
        ##
        # unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ImmediateFlips'))
    TestEnvironment.cleanup(outcome)
