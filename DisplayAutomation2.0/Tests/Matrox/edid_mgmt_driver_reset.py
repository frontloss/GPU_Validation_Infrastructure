########################################################################################################################
# @file         edid_mgmt_driver_reset.py
# @brief        Covers cases with driver restart
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
from Libs.Core import display_essential
from Libs.Core.wrapper import control_api_wrapper


##
# @brief - Lock display Test
class EdidMgmtDriverReset(MatroxBase):

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
    # @brief        Enable lock and verify
    # @return       None
    def test_enable_lock(self):
        status = True
        logging.info("**************TEST ENABLE LOCK**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], 
                                                  port=value['connector_port'], action=TestAction.LOCK) and status

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

        if not status:
            self.fail()

    ##
    # @brief        Test driver disable - enable after lock
    # @return       None
    def test_reset_driver_after_lock(self):
        logging.info("**************TEST DRIVER RESET FOR LOCK CASE**************")

        ##
        # disable and enable gfx driver
        status, reboot_required = display_essential.restart_gfx_driver()
        if status:
            logging.info("Successfully restarted driver.")
        elif status is False and reboot_required is True:
            logging.info("\tRebooting system as requested by OS.")
            if reboot_helper.reboot(self, 'test_verify_then_disable_lock') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief        Verify lock and then unlock
    # @return       None
    def test_verify_then_disable_lock(self):
        status = True
        logging.info("**************TEST VERIFY THEN DISABLE LOCK**************")

        for key, value in self.plugged_disp_list:

            # Trigger verification for case locked == true, should persist after driver disable - enable
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], 
                                                  port=value['connector_port'], action=TestAction.UNLOCK) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        Test Override enable before driver restart
    # @return       None
    def test_enable_override(self):
        status = True
        logging.info("**************TEST ENABLE OVERRIDE**************")

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
    # @brief        Perform driver disable - enable
    # @return       None
    def test_reset_driver_after_override(self):
        logging.info("**************TEST DRIVER RESET FOR OVERRIDE CASE**************")

        ##
        # disable and enable gfx driver
        status, reboot_required = display_essential.restart_gfx_driver()
        if status:
            logging.info("Successfully restarted driver.")
        elif status is False and reboot_required is True:
            logging.info("\tRebooting system as requested by OS.")
            if reboot_helper.reboot(self, 'test_verify_then_disable_override') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief        Verify override and then remove
    # @return       None
    def test_verify_then_disable_override(self):
        status = True
        logging.info("**************TEST VERIFY THEN DISABLE OVERRIDE**************")

        for key, value in self.plugged_disp_list:
            # Trigger verification for case override == true, should persist after driver disable - enable
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
    # @brief        Unplug all plugged displays
    # @return       None
    def test_unplug_display(self) -> None:
        logging.info("**************TEST UNPLUG DISPLAY**************")

        # Unplug displays which have been plugged in test setup
        for key, value in self.plugged_disp_list:
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNPLUG)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdidMgmtDriverReset'))
    TestEnvironment.cleanup(outcome)