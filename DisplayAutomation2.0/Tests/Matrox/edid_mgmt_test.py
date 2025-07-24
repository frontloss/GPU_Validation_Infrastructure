########################################################################################################################
# @file         edid_mgmt_test.py
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
from Libs.Core.display_config import display_config
from Libs.Core import reboot_helper
from Libs.Core import enum


##
# @brief - Lock display Test
class EdidMgmtTest(MatroxBase):

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
    def test_lock_basic(self):
        status = True
        logging.info("**************TEST LOCK DISPLAY BASIC**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.LOCK) and status

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.UNLOCK) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(port=value['connector_port'], gfx=value['gfx_index'], case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        Override and remove basic test
    # @return       None
    def test_override_basic(self):
        status = True
        logging.info("**************TEST OVERRIDE DISPLAY BASIC**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.OVERRIDE) and status

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
    # @brief        Call lock with override edid and verify CAPI flows
    # @return       None
    def test_lock_plus_override(self):
        self.skipTest("Skipped due to known issue : https://hsdes.intel.com/appstore/article/#/16017695038")
        status = True
        logging.info("**************TEST LOCK WITH OVERRIDE**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Supplied EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.LOCK_AND_OVERRIDE) and status

            # Trigger verification for case override == true
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.UNLOCK) and status

            # Trigger verification for case override == false
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=False) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        First perform lock then perform override
    # @return       None
    def test_lock_then_override(self):
        status = True
        logging.info("**************TEST LOCK AND THEN OVERRIDE**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.LOCK) and status

            # Override is expected to fail for a locked display (driver policy)
            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID
            status = not(self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                      action=TestAction.OVERRIDE)) and status

            # Trigger verification for case override == True , expected to fail
            status = not(self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                                   case=True)) and status

            # Remove is expected to fail , when override is not applied (driver policy)
            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_REMOVE as opcode, expected to fail
            status = not(self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                      action=TestAction.REMOVE)) and status

            # Trigger verification for case override == false
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=False) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.UNLOCK) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'],
                                      case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        First perform override and then lock test
    # @return       None
    def test_override_then_lock(self):
        self.skipTest("Skipped due to known issue : https://hsdes.intel.com/appstore/article/#/16017695038")
        status = True
        logging.info("**************TEST OVERRIDE AND THEN LOCK **************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.OVERRIDE) and status

            # Trigger verification for case override == true
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Supplied EDID
            # Lock call will fail if edid is already overridden (driver policy)
            status = not(self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                      action=TestAction.LOCK_AND_OVERRIDE)) and status

            # Trigger verification for case locked == true
            status = not(self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True)) and status

            # UnLock call will fail if display is not locked(driver policy)
            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = not(self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                      action=TestAction.UNLOCK)) and status

            # Trigger verification for case locked == False, default case expected to pass
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=False) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_REMOVE as opcode
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.REMOVE) and status

            # Trigger verification for case override == false
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        First perform override and then lock without override test
    # @return       None
    def test_override_then_lock_without_override(self):
        self.skipTest("Skipped due to known issue : https://hsdes.intel.com/appstore/article/#/16017695038")
        status = True
        logging.info("**************TEST OVERRIDE AND THEN LOCK WITHOUT OVERRIDE**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.OVERRIDE) and status

            # Trigger verification for case override == true
            status = self.verify_edid_override(port=value['connector_port'], gfx=value['gfx_index'],
                                               case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            # Lock (by default, with monitor edid) is expected to fail if edid is already overridden
            status = not(self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                      action=TestAction.LOCK)) and status

            # Trigger verification for case locked == true
            status = not(self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True)) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_REMOVE as opcode
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.REMOVE) and status

            # Trigger verification for case override == false
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'],
                                               case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        Check if edid management operation for 1 target does not impact another target
    # @return       None
    def test_untouched_display(self):
        # More than 1 display required for this test
        if len(self.plugged_disp_list) < 2:
            self.skipTest("2 or more displays in command line required for this test")

        status = True
        logging.info("**************TEST UNTOUCHED DISPLAY BASIC**************")

        disp1_value = self.plugged_disp_list[0][1]
        disp2_value = self.plugged_disp_list[1][1]

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID on 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.LOCK) and status

        # Trigger verification for case locked == true on 1st display
        status = self.verify_lock(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                  case=True) and status

        # Trigger verification for case locked == true on 2nd display, this is expected to fail
        # Important : This is first key verification step in this test
        status = not(self.verify_lock(gfx=disp2_value['gfx_index'], port=disp2_value['connector_port'],
                                      case=True)) and status

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID on 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.UNLOCK) and status

        # Trigger verification for case locked == false on 1st display
        status = self.verify_lock(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                  case=False) and status

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID for 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.OVERRIDE) and status

        # Trigger verification for case override == true on first display
        status = self.verify_edid_override(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                           case=True) and status

        # Trigger verification for case override == true on 2nd display, this is expected to fail
        # Important : This is other key verification step in this test
        status = not(self.verify_edid_override(gfx=disp2_value['gfx_index'], port=disp2_value['connector_port'],
                                               case=True)) and status

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_REMOVE as opcode on 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.REMOVE) and status

        # Trigger verification for case override == false on 1st display
        status = self.verify_edid_override(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                           case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        Check if edid management operation for 1 target persists in display switch
    # @return       None
    def test_display_switch(self):
        # More than 1 display required for this test
        if len(self.plugged_disp_list) < 2:
            self.skipTest("2 or more displays in command line required for this test")

        status = True
        logging.info("**************TEST DISPLAY SWITCH BASIC**************")

        disp1_value = self.plugged_disp_list[0][1]
        disp2_value = self.plugged_disp_list[1][1]

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID on 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.LOCK) and status

        # Switch to 2nd display only
        display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(
            port=disp2_value['connector_port'], gfx_index=disp2_value['gfx_index'])
        if display_config.DisplayConfiguration().set_display_configuration_ex(enum.SINGLE, [display_data]) is False:
            logging.error("FAIL: Unable to switch to 2nd display {}".format(disp2_value['connector_port']))
            status = False
        else:
            logging.info("PASS: Switched to 2nd display {}".format(disp2_value['connector_port']))

        # Make all displays active again
        self.enable_plugged_disp()

        # Trigger verification for case locked == true on 1st display
        # Important : This is key verification step in this test, checking persistence after switch
        status = self.verify_lock(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                  case=True) and status

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID on 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.UNLOCK) and status

        # Trigger verification for case locked == false on 1st display
        status = self.verify_lock(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                  case=False) and status

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID for 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.OVERRIDE) and status

        # Switch to 2nd display only
        display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(
            port=disp2_value['connector_port'], gfx_index=disp2_value['gfx_index'])
        if display_config.DisplayConfiguration().set_display_configuration_ex(enum.SINGLE, [display_data]) is False:
            logging.error("FAIL: Unable to switch to 2nd display {}".format(disp2_value['connector_port']))
            status = False
        else:
            logging.info("PASS: Switched to 2nd display {}".format(disp2_value['connector_port']))

        # Make all displays active again
        self.enable_plugged_disp()

        # Trigger verification for case override == true on 1st display
        # Important : This is other key verification step in this test, checking persistence after switch
        status = self.verify_edid_override(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                           case=True) and status

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_REMOVE as opcode on 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.REMOVE) and status

        # Trigger verification for case override == false
        status = self.verify_edid_override(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                           case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        Change display mode and check persistence of edid management operation
    # @return       None
    def test_mode_switch_basic(self):
        # Enough to run this only for single display case
        if len(self.plugged_disp_list) != 1:
            self.skipTest("This test will run only if single display in command line")

        status = True
        logging.info("**************TEST MODE SWITCH BASIC**************")

        # plugged display list has to be 1 , so loop is expected to execute only once
        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.LOCK) and status

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Switch modes on display and come back to native mode
            display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(
                port=value['connector_port'], gfx_index=value['gfx_index'])
            native_mode = display_config.DisplayConfiguration().get_current_mode(display_and_adapter_info=display_data)
            supported_mode_list = display_config.DisplayConfiguration().get_all_supported_modes(
                display_and_adapter_info_list=[display_data])
            if len(supported_mode_list) == 0:
                logging.error("Failed to retrieve supported modes for {0}".format(value['connector_port']))
            for target_id, modes in supported_mode_list.items():
                # since supported mode list was called only for 1 display, target_id key count should be only 1
                mode1 = modes[0]  # modes is a list, picking first mode from mode list
                status = display_config.DisplayConfiguration().set_display_mode(mode_list=[mode1]) and status
            status = display_config.DisplayConfiguration().set_display_mode(mode_list=[native_mode]) and status

            # Trigger verification for case locked == true, again expected to pass
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.UNLOCK) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=False) and status

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
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdidMgmtTest'))
    TestEnvironment.cleanup(outcome)