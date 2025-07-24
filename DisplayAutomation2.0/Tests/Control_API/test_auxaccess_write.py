########################################################################################################################
# @file         test_auxaccess_write.py
# @brief        Test calls for Aux Write Access through Control Library and verifies return status of the API.
#                   * Aux Write Access API.
#                   * Aux Write Access with back to back writes for different address.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase


##
# @brief - Verify Aux Write API Control Library Test
class testAuxWriteAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Aux Write Access via Control Library")

        auxargs = control_api_args.ctl_aux_access_args()
        auxargs.Size = ctypes.sizeof(auxargs)

        auxargs.OpType = control_api_args.ctl_operation_type.WRITE.value
        auxargs.Address = 0x103  # DPCD offset for Training Lane0 Set
        auxargs.DataSize = 1
        auxargs.Flags = control_api_args.ctl_aux_flags_t.NATIVE_AUX.value
        auxargs.Data[0] = 0x01

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(targetid)

            logging.info("Step_1: Native Aux Access Write")
            if control_api_wrapper.aux_access(auxargs, display_and_adapter_info):
                logging.info("Pass:  Aux Access via Control Library")
            else:
                logging.error("Fail: Aux Access via Control Library")
                gdhm.report_driver_bug_clib(f"Aux Access failed via Control Library "
                                        "for Aux Operation Type: {0} TargetId: {1}"
                                        .format(auxargs.OpType,targetid))
                self.fail("Native Aux Access Write Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Aux Access Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
