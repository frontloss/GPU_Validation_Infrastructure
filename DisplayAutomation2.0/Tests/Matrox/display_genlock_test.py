########################################################################################################################
# @file         display_genlock_test.py
# @brief        Display Genlock operation primary use cases
# @details      This test checks enable, display and validate through DisplayGenlock Control API
# @author       diksonch
########################################################################################################################

import logging
import unittest
import time

from Tests.Matrox.display_genlock_base import Genlock
from Tests.Matrox.display_genlock_base import Action
from Tests.Matrox.matrox_base import TestAction
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import reboot_helper
from Libs.Core.display_config import display_config


##
# @brief - Genlock display Test
class DisplayGenlockTest(Genlock):
    genlock_obj = Genlock()
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
    # @brief        Validate whether genlock is possible
    # @return       None
    def test_validate(self):
        status = True
        logging.info("**************TEST GENLOCK VALIDATE**************")
        for index, (key, value) in enumerate(self.plugged_disp_list):
            status = self.perform_display_genlock(gfx=value['gfx_index'], port=value['connector_port'],
                                                action = Action.VALIDATE) and status
            status = self.verify_validate_functionality() and status
        if not status:
            self.fail()
    ##
    # @brief        Enable Genlock
    # @return       None
    def test_enable_genlock(self):
        status = True
        logging.info("**************TEST GENLOCK ENABLE**************")
        for index, (key, value) in enumerate(self.plugged_disp_list):
            status = self.perform_display_genlock(gfx=value['gfx_index'], port=value['connector_port'],
                                                   action = Action.ENABLE) and status
            status = self.verify_enable_functionality() and status
        if not status:
            self.fail()
    ##
    # @brief        Disable Genlock
    # @return       None        
    def test_disable_genlock(self):
        status = True
        logging.info("**************TEST GENLOCK DISABLE**************")
        for index, (key, value) in enumerate(self.plugged_disp_list):
            status = self.perform_display_genlock(gfx=value['gfx_index'], port=value['connector_port'],
                                                   action = Action.DISABLE) and status
            status = self.verify_disable_functionality() and status
        if not status:
            self.fail()

    ##
    # @brief        Enable Genlock for child target of combined display
    # @return       None
    def test_genlock_before_cd(self):
        if not self.is_genlock_combined_display_config():
            self.skipTest("Not a Combined display verification config")

        logging.info("**************TEST ENABLE GENLOCK BEFORE COMBINED DISPLAY ENABLE**************")

        status = True
        adaptor_info_list = []
        mcd_config_list = iter(self.mcd_config_data.values())
        cd_enable, cd_disable = next(mcd_config_list), next(mcd_config_list)

        for index, (key, value) in enumerate(self.plugged_disp_list):

            display_adaptor_info = display_config.DisplayConfiguration().\
                get_display_and_adapter_info_ex(port=value['connector_port'], gfx_index=value['gfx_index'])
            adaptor_info_list.append(display_adaptor_info)

            status = self.perform_display_genlock(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action = Action.ENABLE, display_data=adaptor_info_list[index]) and status

            status = self.verify_enable_functionality() and status

        status = self.perform_get_set_combined_display(cd_enable, adaptor_info_list) and status

        time.sleep(5)

        status = self.perform_get_set_combined_display(cd_disable, adaptor_info_list) and status

        time.sleep(5)

        for index, (key, value) in enumerate(self.plugged_disp_list):
            status = self.perform_display_genlock(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action = Action.DISABLE, display_data=adaptor_info_list[index]) and status

            status = self.verify_disable_functionality() and status

        if not status:
            self.fail("Test Genlock before combined display enable failed")

    ##
    # @brief        Enable Genlock after enabling combined display
    # @return       None
    def test_genlock_after_cd(self):
        if not self.is_genlock_combined_display_config():
            self.skipTest("Not a Combined display verification config")

        logging.info("**************TEST ENABLE GENLOCK AFTER COMBINED DISPLAY ENABLE**************")

        status = True
        adaptor_info_list = []
        mcd_config_list = iter(self.mcd_config_data.values())
        cd_enable, cd_disable = next(mcd_config_list), next(mcd_config_list)

        for index, (key, value) in enumerate(self.plugged_disp_list):

            display_adaptor_info = display_config.DisplayConfiguration(). \
                get_display_and_adapter_info_ex(port=value['connector_port'], gfx_index=value['gfx_index'])
            adaptor_info_list.append(display_adaptor_info)

        status = self.perform_get_set_combined_display(cd_enable, adaptor_info_list) and status

        time.sleep(5)

        for index, (key, value) in enumerate(self.plugged_disp_list):

            # Genlock enable is expected to fail for combined display, which is current driver policy
            # Even though test calls genlock for each display, in the DLL, genlock is applied for active display
            # Special case : If Genlock CAPI call is made for a child target which is part of collage / combined display, that is expected to work
            # Special case will only be covered in multi adaptor / MGPU SLS case, not here

            status = not(self.perform_display_genlock(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action = Action.ENABLE, display_data=adaptor_info_list[index])) and status

            status = not(self.perform_display_genlock(gfx=value['gfx_index'], port=value['connector_port'],
                                                  action = Action.DISABLE,display_data=adaptor_info_list[index])) and status

        status = self.perform_get_set_combined_display(cd_disable, adaptor_info_list) and status

        time.sleep(5)

        if not status:
            self.fail("Test Genlock after combined display enable failed")

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
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DisplayGenlockTest'))
    TestEnvironment.cleanup(outcome)
