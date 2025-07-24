#################################################################################################
# @file         lace_with_all_modes.py
# @brief        Test calls for get and set lace functionality with supported modes apply with Lace persistence
# @author       Vimalesh D
#################################################################################################
import sys
import sys
import unittest
import random

from operator import attrgetter


from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.Lace.lace_base import *


##
# @brief - Lace basic test
class LaceBasic(LACEBase):
    ##
    # @brief test_01_lace_with_mode function - Function to perform enable disable lace feature on display and
    #                                 perform register verification on all panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "Mode",
                     "Skip the  test step as the action type is not basic")
    def test_01_lace_with_mode(self):

        status = False
        mode = None
        config = display_config.DisplayConfiguration()

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: Lace was enabled and verified successfully")
                        else:
                            self.fail("Lace enable/disable with verification failed")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info(
                                "Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(
                                    panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        mode = config.get_current_mode(panel.display_and_adapterInfo)
                        supported_modes = config.get_all_supported_modes([panel.display_and_adapterInfo.TargetID])

                        for key, modes in supported_modes.items():
                            # do reverse and apply samplingmode instead of native mode
                            modes = sorted(modes, key=attrgetter('HzRes'), reverse=True)
                            for mode in modes:
                                result = config.set_display_mode([mode])
                                time.sleep(2)

                                ##
                                # verify_lace_feature
                                if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                            "LEGACY") is False:
                                    self.fail("Lace verification failed")

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Enables and Disables lace on  panels and apply Mode"
                 " and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)