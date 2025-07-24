#######################################################################################################################
# @file                 test_bpc_via_regkey.py
# @addtogroup           Test_Color
# @section              test_bpc_via_regkey
# @remarks              @ref test_bpc_via_regkey.py \n
#                       The test script update BPC from List and will perform verification
# Sample CommandLines:  python Tests\Color\Features\DitheringDeepColor\test_bpc_via_regkey.py -EDP_A -DP_F SINK_DPM033
# @author       Vimalesh D
#######################################################################################################################

import sys
import logging
import unittest

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import common_utility
from Tests.Color.Common.common_utility import delete_registry
from Tests.Color.Verification import feature_basic_verify
from Tests.test_base import TestBase


##
# @brief - To perform BPC update via regkey and verification of BPC for Display Port(DP - SST/MST)
class TestBPCViaRegkey(TestBase):

    def runTest(self):
        # Plug Display for DP -SST/MST was taken care test_base
        bpc_list = [(8, "BPC8"), (10, "BPC10"), (12, "BPC12")]

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and (panel.is_lfp is False):
                    logging.info("Perform BPC Update via reg-key and Verification")
                    for bpc in range(0, len(bpc_list)):
                        if common_utility.set_bpc_registry(gfx_index, panel.display_and_adapterInfo,
                                                           int(bpc_list[bpc][0])) is False:
                            self.fail("Fail: Failed to set BPC via regkey: SelectBPCFromRegistry")
                        ##
                        # restart display driver
                        status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
                        if status is False:
                            self.fail('Fail: Failed to Restart Display driver')
                        else:
                            for port, panel in adapter.panels.items():
                                if panel.is_active:
                                    if feature_basic_verify.verify_transcoder_bpc(gfx_index, adapter.platform,
                                                                                  panel.transcoder,
                                                                                  int(bpc_list[bpc][0])) is False:
                                        self.fail("Failed to verify transcoder BPC")
                                    logging.info("Verification of Transocder BPC passed")

    ##
    # Invoke Test teardown to delete the registry
    def TearDown(self):
        logging.info("Perform registry cleanup")
        for gfx_index, adapter in self.context_args.adapters.items():
            delete_registry(gfx_index, "SelectBPCFromRegistry")
            delete_registry(gfx_index, "SelectBPC")

        # To ensure cleanup was done
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error('Failed to Restart Display driver')
            status = False
        logging.info('Display driver restarted successfully')

        ##
        # Invoking the Base class's tearDown() to perform the general clean-up activities
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
