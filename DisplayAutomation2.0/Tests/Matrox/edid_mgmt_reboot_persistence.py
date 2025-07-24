########################################################################################################################
# @file         edid_mgmt_reboot_persistence.py
# @brief        Test file for covering cases where display is inactive or unplugged
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
class EdidMgmtRebootPersistence(MatroxBase):

    ##
    # @brief        Plug displays requested for test
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
    # @brief        Verify lock before reboot
    # @return       None
    def test_lock_before_reboot(self):
        status = True
        logging.info("**************TEST LOCK BEFORE REBOOT**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.LOCK) and status

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

        if not status:
            self.fail()

    ##
    # @brief        Perform reboot
    # @return       None
    def test_reboot_1(self):
        logging.info("**************REBOOT 1**************")

        if reboot_helper.reboot(self, 'test_lock_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Verify lock after reboot
    # @return       None
    def test_lock_after_reboot(self):
        status = True
        logging.info("**************TEST LOCK AFTER REBOOT**************")

        for key, value in self.plugged_disp_list:

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.UNLOCK) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'],
                                      case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        Verify override before reboot
    # @return       None
    def test_override_before_reboot(self):
        status = True
        logging.info("**************TEST OVERRIDE BEFORE REBOOT**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.OVERRIDE) and status

            # Trigger verification for case override == true
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=True) and status

        if not status:
            self.fail()

    ##
    # @brief        Perform reboot
    # @return       None
    def test_reboot_2(self):
        logging.info("**************REBOOT 2**************")

        if reboot_helper.reboot(self, 'test_override_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Verify override after system reboot
    # @return       None
    def test_override_after_reboot(self):
        status = True
        logging.info("**************TEST REBOOT AND THEN VERIFY OVERRIDE**************")

        for key, value in self.plugged_disp_list:
            # Trigger verification for case override == true
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_REMOVE as opcode
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.REMOVE) and status

            # Trigger verification for case override == false
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=False) and status

        if not status:
            self.fail()

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
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdidMgmtRebootPersistence'))
    TestEnvironment.cleanup(outcome)