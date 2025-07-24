########################################################################################################################
# @file         combined_display_test.py
# @brief        EDID management operation primary use cases
# @details      This test checks lock display through EdidMgmt Control API. Requires regkey EdidMgmtEnable = 1 in
# @details      GTA config / plugin or manually before running. Supports multi display, tests displays 1 by 1
# @author       akumarv
########################################################################################################################

import logging
import unittest

from Tests.Matrox.matrox_base import MatroxBase
from Tests.Matrox.matrox_base import TestAction
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import reboot_helper


##
# @brief - Lock display Test
class MCDTest(MatroxBase):

    ##
    # @brief        Plug displays required for test
    # @return       None
    def test_plug_display(self):
        logging.info("**************TEST PLUG DISPLAY**************")

        # displays are already parsed from cmd line in matrox base class setup, plug will be performed below
        for key, value in self.plugged_disp_list:
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.PLUG)

        # If more than 1 display in command line, then apply extended on all plugged displays
        if len(self.plugged_disp_list) > 1:
            self.enable_plugged_disp()

    ##
    # @brief        Lock enable and disable basic test
    # @return       None
    def test_combined_display_basic(self):
        status = True
        logging.info("**************TEST COMBINED DISPLAY BASIC**************")

        for value in self.mcd_config_data.values():
            # Call CAPI
            status = self.perform_get_set_combined_display(value) and status

        if not status:
            self.fail("Test Combined Display Failed")

    ##
    # @brief        Unplug displays at the end of the test
    # @return       None
    def test_unplug_display(self) -> None:
        logging.info("**************TEST UNPLUG DISPLAY**************")

        # Unplug displays which have been plugged in test setup
        for key, value in self.plugged_disp_list:
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNPLUG)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('MCDTest'))
    TestEnvironment.cleanup(outcome)