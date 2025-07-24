########################################################################################################################
# @file         edid_mgmt_audio_endpoint.py
# @brief        Test file for covering cases where display audio endpoint is verified with edid management operations
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
from Libs.Feature.display_audio import DisplayAudio


##
# @brief - Lock display Test
class EdidMgmtAudioEndpoint(MatroxBase):
    display_audio = DisplayAudio()

    ##
    # @brief        Plug requested displays
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
    # @brief        Test audio with lock
    # @return       None
    def test_audio_with_lock(self):
        status = True
        logging.info("**************TEST AUDIO WITH LOCK**************")

        before_lock_endpoints = self.display_audio.get_audio_endpoints()
        logging.info("Display audio Encoder Enumeration status before Lock {0}".format(before_lock_endpoints))
        if before_lock_endpoints == 0:
            self.fail("No Display audio endpoints enumerated")

        status = self.display_audio.audio_verification() and status

        # Perform lock for all displays
        for key, value in self.plugged_disp_list:
            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_LOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'],
                                                  port=value['connector_port'], action=TestAction.LOCK) and status

            # Trigger verification for case locked == true
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

        after_lock_endpoints = self.display_audio.get_audio_endpoints()
        logging.info("Display audio Encoder Enumeration status after Lock {0}".format(after_lock_endpoints))

        status = self.display_audio.audio_verification() and status

        # Perform unlock for all displays
        for key, value in self.plugged_disp_list:

            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_UNLOCK as opcode with Monitor EDID
            status = self.perform_edid_management(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action=TestAction.UNLOCK) and status

            # Trigger verification for case locked == false
            status = self.verify_lock(gfx=value['gfx_index'], port=value['connector_port'], case=False) and status

        after_unlock_endpoints = self.display_audio.get_audio_endpoints()
        logging.info("Display audio Encoder Enumeration status after UnLock {0}".format(after_unlock_endpoints))

        status = self.display_audio.audio_verification() and status

        if before_lock_endpoints == after_lock_endpoints == after_unlock_endpoints:
            logging.info("PASS: Endpoint count is same before and after lock operations")
        else:
            logging.info("FAIL: Endpoint count is not same before and after lock operations!!!")
            status = False

        if not status:
            self.fail()

    ##
    # @brief        Test audio with override
    # @return       None
    def test_audio_with_override(self):
        self.skipTest("Skipping test due to known issue: https://hsdes.intel.com/appstore/article/#/16017850504")
        status = True
        logging.info("**************TEST AUDIO WITH OVERRIDE**************")

        before_override_endpoints = self.display_audio.get_audio_endpoints()
        logging.info("Display audio Encoder Enumeration status before override {0}".format(before_override_endpoints))
        if before_override_endpoints == 0:
            self.fail("No Display audio endpoints enumerated")

        status = self.display_audio.audio_verification() and status

        # Perform override for all displays
        for key, value in self.plugged_disp_list:
            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_OVERRIDE as opcode with Supplied EDID
            status = self.perform_edid_management(gfx=value['gfx_index'],
                                                  port=value['connector_port'], action=TestAction.OVERRIDE) and status

            # Trigger verification for case override == true
            status = self.verify_edid_override(gfx=value['gfx_index'], port=value['connector_port'], case=True) and status

        after_override_endpoints = self.display_audio.get_audio_endpoints()
        logging.info("Display audio Encoder Enumeration status after override {0}".format(after_override_endpoints))

        status = self.display_audio.audio_verification() and status

        # Perform edid remove for all displays
        for key, value in self.plugged_disp_list:
            # Call CAPI DD_IGCL_EDID_CONFIG_MGMT with DD_IGCL_EDID_REMOVE as opcode
            status = self.perform_edid_management(gfx=value['gfx_index'],
                                                  port=value['connector_port'], action=TestAction.REMOVE) and status

            # Trigger verification for case override == false
            status = self.verify_edid_override(gfx=value['gfx_index'],
                                               port=value['connector_port'], case=False) and status

        after_remove_endpoints = self.display_audio.get_audio_endpoints()
        logging.info("Display audio Encoder Enumeration status after remove {0}".format(after_remove_endpoints))

        status = self.display_audio.audio_verification() and status

        if before_override_endpoints == after_override_endpoints == after_remove_endpoints:
            logging.info("PASS: Endpoint count is same before and after override operations")
        else:
            logging.info("FAIL: Endpoint count is not same before and after override operations!!!")
            status = False

        if not status:
            self.fail()

    ##
    # @brief        Unplug plugged displays
    # @return       None
    def test_unplug_display(self) -> None:
        logging.info("**************TEST UNPLUG DISPLAY**************")

        # Unplug displays which have been plugged in test setup
        for key, value in self.plugged_disp_list:
            self.disp_plug_unplug(gfx=value['gfx_index'], port=value['connector_port'], action=TestAction.UNPLUG)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdidMgmtAudioEndpoint'))
    TestEnvironment.cleanup(outcome)