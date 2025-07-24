########################################################################################################################
# @file         virtual_display_headless.py
# @brief        Virtual Display Headless scenario is covered in below scenarios:
#               * Virtual Display verification in headless mode
#               * Virtual Display verification post hot-plug/unplug of external display
# @author       Prateek Joshi
########################################################################################################################


import sys
import unittest
import logging

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.Yangra import virtual_display_yangra_base as yangra_base

##
# @brief   It contains methods to verify virtual display in headless mode, post hot-plug/unplug of external display
class VirtualDisplayHeadless(yangra_base.VirtualDisplayYangraBase):

    ##
    # @brief        Unittest runTest function
    # @param[in]    self; Object of virtual display yangra base class
    # @return       void
    def runTest(self):
        # Debug purpose
        self.log_enumerated_status()

        # Unplug external display connected
        logging.info('Step_1: Unplug External Display'.center(yangra_base.LINE_WIDTH, '-'))
        for display in self.connected_list:
            if yangra_base.display_utility.unplug(display) is False:
                self.fail("Failed to unplug display {}".format(display))
            self.plugged_display.remove(display)
            logging.info('Successfully unplugged the display {}'.format(display))

        self.log_enumerated_status()

        # Verify virtual displays
        logging.info('Step_2: Verify Virtual Display'.center(yangra_base.LINE_WIDTH, '-'))
        self.assertEqual(self.verify_headless_virtual_display(), True, 'Failed to verify virtual display')
        logging.info('Successfully verified virtual display is enumerated')

        logging.info('Step_3: Plug External Display'.center(yangra_base.LINE_WIDTH, '-'))
        for display in self.connected_list:
            if yangra_base.display_utility.plug(display) is False:
                self.fail("Failed to plug display {}".format(display))
            self.plugged_display.append(display)
            logging.info('Successfully plugged the display {}'.format(display))

        self.log_enumerated_status()

        # Verify virtual display
        logging.info('Step_4: Verify Virtual Display'.center(yangra_base.LINE_WIDTH, '-'))
        self.assertEqual(self.verify_headless_virtual_display(), False, 'Failed to verify virtual display')
        logging.info('Successfully verified virtual display')

        # Start ETL Tracer
        if self.start_etl_capture() is False:
            self.fail("GfxTrace failed to start")

        # Restart Display driver
        status, reboot_required = display_essential.restart_gfx_driver()

        # Stop ETL Tracer
        etl_file = self.stop_etl_capture()

        # Verify VideoPresentSources reported by driver
        if self.verify_videopresentsources(etl_file) is False:
            self.fail("Driver is not reporting correct VideoPresentSources")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
