########################################################################################################################
# @file         edid_mgmt_power_event.py
# @brief        Test file for covering cases where display is inactive or unplugged
# @details      This test checks lock display through EdidMgmt Control API. Requires regkey EdidMgmtEnable = 1 in
# @details      GTA config / plugin or manually before running. Supports multi display, tests displays 1 by 1
# @author       akumarv
########################################################################################################################

import logging
import unittest

from Libs.Core import display_power, enum, reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Matrox.matrox_base import MatroxBase
from Tests.Matrox.matrox_base import TestAction

##
# @brief - Lock display Test
class EdidMgmtPowerEvent(MatroxBase):

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
    # @brief        Test lock before power event
    # @return       None
    def test_lock_before_Sx(self):
        status = True
        logging.info("**************TEST LOCK BEFORE Sx**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.LOCK) and status

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

        if not status:
            self.fail()

    ##
    # @brief        Perform CS/MS if supported
    # @return       None
    def test_cs(self):
        logging.info("**************CONNECTED/MODERN STANDBY ENTRY RESUME**************")

        cs_status = display_power.DisplayPower.is_power_state_supported(display_power.PowerEvent.CS)

        if cs_status:
            # Invoke power event
            if display_power.DisplayPower.invoke_power_event(power_state=display_power.PowerEvent.CS) is False:
                self.fail("Test failed to invoke CS/MS")
            else:
                logging.info("CS resume done")
        else:
            self.skipTest("System does not support Connected Standby")

    ##
    # @brief        Perform S3 if supported
    # @return       None
    def test_s3(self):
        logging.info("**************SLEEP ENTRY RESUME**************")

        s3_status = display_power.DisplayPower.is_power_state_supported(display_power.PowerEvent.S3)

        if s3_status:
            # Invoke power event
            if display_power.DisplayPower.invoke_power_event(power_state=display_power.PowerEvent.S3) is False:
                self.fail("Test failed to invoke S3")
            else:
                logging.info("S3 resume done")
        else:
            self.skipTest("System does not support Sleep")

    ##
    # @brief        Verify lock after Sx
    # @return       None
    def test_lock_after_Sx(self):
        status = True
        logging.info("**************TEST LOCK AFTER Sx**************")

        for key, value in self.plugged_disp_list:

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNLOCK) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=False) and status

        if not status:
            self.fail()

    ##
    # @brief        Verify override before Sx
    # @return       None
    def test_override_before_Sx(self):
        status = True
        logging.info("**************TEST OVERRIDE BEFORE Sx**************")

        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.OVERRIDE) and status

            # Trigger verification for case override == true
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

        if not status:
            self.fail()

    ##
    # @brief        Perform CS/MS if supported
    # @return       None
    def test_cs_2(self):
        logging.info("**************CONNECTED/MODERN STANDBY ENTRY RESUME 2**************")

        cs_status = display_power.DisplayPower.is_power_state_supported(display_power.PowerEvent.CS)

        if cs_status:
            # Invoke power event
            if display_power.DisplayPower.invoke_power_event(power_state=display_power.PowerEvent.CS) is False:
                self.fail("Test failed to invoke CS/MS")
            else:
                logging.info("CS resume done")
        else:
            self.skipTest("System does not support Connected Standby")

    ##
    # @brief        Perform S3 if supported
    # @return       None
    def test_s3_2(self):
        logging.info("**************SLEEP ENTRY RESUME 2**************")

        s3_status = display_power.DisplayPower.is_power_state_supported(display_power.PowerEvent.S3)

        if s3_status:
            # Invoke power event
            if display_power.DisplayPower.invoke_power_event(power_state=display_power.PowerEvent.S3) is False:
                self.fail("Test failed to invoke S3")
            else:
                logging.info("S3 resume done")
        else:
            self.skipTest("System does not support Sleep")

    ##
    # @brief        Verify Override after Sx
    # @return       None
    def test_override_after_Sx(self):
        status = True
        logging.info("**************TEST OVERRIDE AFTER Sx**************")

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
    # @brief        Unplug displays plugged for test
    # @return       None
    def test_unplug_display(self) -> None:
        logging.info("**************TEST UNPLUG DISPLAY**************")

        # Unplug displays which have been plugged in test setup
        for key, value in self.plugged_disp_list:
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNPLUG)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdidMgmtPowerEvent'))
    TestEnvironment.cleanup(outcome)