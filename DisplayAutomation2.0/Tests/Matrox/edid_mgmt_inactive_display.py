########################################################################################################################
# @file         edid_mgmt_inactive_display.py
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
from Libs.Core.display_config import display_config
from Libs.Core import enum


##
# @brief - Lock display Test
class EdidMgmtInactiveDisplay(MatroxBase):

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
    # @brief        Check if edid management operation for 1 target persists in display switch, for inactive display
    # @return       None
    def test_display_switch_inactive_display(self):
        # More than 1 display required for this test
        if len(self.plugged_disp_list) < 2:
            self.skipTest("2 or more displays in command line required for this test")

        status = True
        logging.info("**************TEST DISPLAY SWITCH INACTIVE DISPLAY**************")

        disp1_value = self.plugged_disp_list[0][1]
        disp2_value = self.plugged_disp_list[1][1]

        # Switch to 2nd display only
        display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(
            port=disp2_value['connector_port'], gfx_index=disp2_value['gfx_index'])
        if display_config.DisplayConfiguration().set_display_configuration_ex(enum.SINGLE, [display_data]) is False:
            logging.error("FAIL: Unable to switch to 2nd display {}".format(disp2_value['connector_port']))
            status = False
        else:
            logging.info("PASS: Switched to 2nd display {}".format(disp2_value['connector_port']))

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID on 1st inactive display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'],
                                              port=disp1_value['connector_port'], action=TestAction.LOCK) and status

        # Make all displays active again
        self.enable_plugged_disp()

        # Trigger verification for case locked == true on 1st display
        # Important : This is key verification step in this test, checking persistence after making display active
        status = self.verify_lock(gfx=disp1_value['gfx_index'],
                                  port=disp1_value['connector_port'], case=True) and status

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID on 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'],
                                              port=disp1_value['connector_port'], action=TestAction.UNLOCK) and status

        # Trigger verification for case locked == false on 1st display
        status = self.verify_lock(gfx=disp1_value['gfx_index'],
                                  port=disp1_value['connector_port'], case=False) and status

        # Switch to 2nd display only
        display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(
            port=disp2_value['connector_port'], gfx_index=disp2_value['gfx_index'])
        if display_config.DisplayConfiguration().set_display_configuration_ex(enum.SINGLE, [display_data]) is False:
            logging.error("FAIL: Unable to switch to 2nd display {}".format(disp2_value['connector_port']))
            status = False
        else:
            logging.info("PASS: Switched to 2nd display {}".format(disp2_value['connector_port']))

        # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID for 1st display
        status = self.perform_edid_management(gfx=disp1_value['gfx_index'], port=disp1_value['connector_port'],
                                              action=TestAction.OVERRIDE) and status

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
    # @brief        Perform edid management operation on aunplugged display and check persistence
    # @return       None
    def test_removed_display(self):

        # Enough to run this only for single display case
        if len(self.plugged_disp_list) != 1:
            self.skipTest("This test will run only if single display in commandline")

        status = True
        logging.info("**************TEST REMOVED DISPLAY**************")

        for key, value in self.plugged_disp_list:
            # Cache display and adaptor info data before unplugging display
            display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(
                port=value['connector_port'],
                gfx_index=value['gfx_index'])

            # Unplug display
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNPLUG)

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with MonitorEDID
            # Displaydata is the cached value of display and adaptor info including targetid
            # This CAPI lock call will fail if display is not connected, lock display only works for connected display
            status = not(self.perform_edid_management_unplugged_display(display_data=display_data,
                                                                        port=value['connector_port'],
                                                                        action=TestAction.LOCK)) and status

            # Plug back display
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.PLUG)

            # Trigger verification for case locked==true, expected to fail as lock display wont work for removed display
            status = not(self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True)) and status

            # Unplug display
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNPLUG)

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with SuppliedEDID
            # Displaydata is the cached value of display and adaptor info including targetid
            status = self.perform_edid_management_unplugged_display(display_data=display_data,
                                                                    port=value['connector_port'],
                                                                    action=TestAction.OVERRIDE) and status

            # Plug back display
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.PLUG)

            # Trigger verification for case override == true, expected to pass
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
    # @brief        Unplug displays requested for test
    # @return       None
    def test_unplug_display(self) -> None:
        logging.info("**************TEST UNPLUG DISPLAY**************")

        # Unplug displays which have been plugged in test setup
        for key, value in self.plugged_disp_list:
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNPLUG)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdidMgmtInactiveDisplay'))
    TestEnvironment.cleanup(outcome)
