########################################################################################################################
# @file         test_auxaccess_readwrite.py
# @brief        Test calls for Aux Write/Read Access through Control Library and verifies return status of the API.
#                   * Aux Write Access API.
#                   * Aux Read Access API.
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
# @brief - Verify Aux WriteRead back to back calls API Control Library Test
class testAuxReadWriteAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Aux Access Write and Read back to back calls via Control Library")

        enumerated_display = display_config.DisplayConfiguration().get_enumerated_display_info()
        gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        gfx_adapter_index = 'gfx_0'
        adapter_info = gfx_adapter_dict[gfx_adapter_index]
        targetid = display_config.DisplayConfiguration().get_target_id(self.connected_list[0], enumerated_display)

        auxWriteArgs = control_api_args.ctl_aux_access_args()
        auxWriteArgs.Size = ctypes.sizeof(auxWriteArgs)

        auxWriteArgs.OpType = control_api_args.ctl_operation_type.WRITE.value
        auxWriteArgs.Address = 0x103  # DPCD offset for Training Lane0 Set
        auxWriteArgs.DataSize = 1
        auxWriteArgs.Flags = control_api_args.ctl_aux_flags_t.NATIVE_AUX.value
        auxWriteArgs.Data[0] = 0x01

        logging.info("Step_1: Aux Access Write")
        if control_api_wrapper.aux_access(auxWriteArgs, targetid):
            logging.info("Pass:  Aux Access via Control Library")
        else:
            logging.error("Fail: Aux Access via Control Library")
            gdhm.report_driver_bug_clib(f"Failed to get AUX Access via Control Library "
                                        "for Aux Operation Type: {0} TargetId: {1}"
                                        .format(auxWriteArgs.OpType,targetid))
            self.fail("FAIL: Aux Access via Control Library")

        auxReadArgs = control_api_args.ctl_aux_access_args()
        auxReadArgs.Size = ctypes.sizeof(auxReadArgs)

        auxReadArgs.OpType = control_api_args.ctl_operation_type.READ.value
        auxReadArgs.Address = 0x103  # DPCD offset for Training Lane0 Set
        auxReadArgs.DataSize = 1
        auxReadArgs.Flags = control_api_args.ctl_aux_flags_t.NATIVE_AUX.value

        logging.info("Step_2: Native Aux Access Read via Control Library")
        address_list = [0x103, 0x103, 0x103]

        for index in range(0, len(address_list)):
            auxReadArgs.Address = address_list[index]

            if control_api_wrapper.aux_access(auxReadArgs, targetid):
                logging.info("Pass:  Aux Access via Control Library")
            else:
                logging.error("Fail: Aux Access via Control Library")
                gdhm.report_driver_bug_clib(f"Aux Access failed via Control Library "
                                        "for Aux Operation Type: {0} TargetId: {1}"
                                        .format(auxReadArgs.OpType,targetid))
                self.fail("Aux Read Access Call {} Failed via Control Library".format(index))

            for data_index in range(0, auxWriteArgs.DataSize):
                if auxWriteArgs.Data[data_index] == auxReadArgs.Data[data_index]:
                    logging.info("PASS: Native Aux Access Read-Write Data verified")
                elif auxWriteArgs.Data[data_index] != auxReadArgs.Data[data_index]:
                    logging.error("FAIL: Native Aux Access Read-Write Data is not matching, Actual-{}, Expected-{}"
                                  .format(auxWriteArgs.Data[data_index], auxReadArgs.Data[data_index]))
                    gdhm.report_driver_bug_clib("Native Aux Access Read-Write Data is not matching, Actual-{0}, Expected-{1}"
                                                .format(auxWriteArgs.Data[data_index], auxReadArgs.Data[data_index]))
                    self.fail("Native Aux Read-Write Data Mismatch")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Aux Access Library Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
