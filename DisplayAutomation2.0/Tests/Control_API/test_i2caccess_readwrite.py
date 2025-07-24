########################################################################################################################
# @file         test_i2caccess_readwrite.py
# @brief        Test calls for I2C Read/Write Access through Control Library and verifies return status of the API.
#                   * I2C Write Access API.
#                   * I2C Read Access API.
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
# @brief - Verify I2C back to back WriteRead API Control Library Test
class testI2CReadWriteAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: I2C Access Write and Read back to back calls via Control Library")

        gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        gfx_adapter_index = 'gfx_0'
        adapter_info = gfx_adapter_dict[gfx_adapter_index]
        targetid = display_config.DisplayConfiguration().get_target_id(self.connected_list[0], self.enumerated_displays)

        i2cWriteArgs = control_api_args.ctl_i2c_access_args()
        i2cWriteArgs.Size = ctypes.sizeof(i2cWriteArgs)

        i2cWriteArgs.OpType = control_api_args.ctl_operation_type.WRITE.value
        i2cWriteArgs.Address = 0xA8
        i2cWriteArgs.Offset = 0x20
        i2cWriteArgs.DataSize = 1
        i2cWriteArgs.Data[0] = 0x1

        logging.info("I2C Write Args - Address-{}, Offset-{}, DataSize-{}, Flags-{}"
                     .format(i2cWriteArgs.Address, i2cWriteArgs.Offset, i2cWriteArgs.DataSize, i2cWriteArgs.Flags))

        logging.info("Step_1: I2C Access Write")
        if control_api_wrapper.i2c_access(i2cWriteArgs, targetid):
            logging.info("Pass: I2C Access Write")
        else:
            logging.error("Fail: I2C Access via Control Library")
            gdhm.report_driver_bug_clib("I2C Access Write Failed via Control Library for "
                                        "Address: {0} Offset: {1} TargetId: {2} Adapter: {3}"
                                        .format(i2cWriteArgs.Address, i2cWriteArgs.Offset,
                                        targetid, gfx_adapter_index))
            self.fail("I2C Write Access Failed via Control Library")

        i2cReadArgs = control_api_args.ctl_i2c_access_args()
        i2cReadArgs.Size = ctypes.sizeof(i2cReadArgs)
        i2cReadArgs.OpType = control_api_args.ctl_operation_type.READ.value
        i2cReadArgs.DataSize = 1
        i2cReadArgs.Offset = 0x21
        i2cReadArgs.Address = 0xA8

        logging.info("Step_2: I2C Multiple Read Access")

        if control_api_wrapper.i2c_access(i2cReadArgs, targetid):
            logging.info("Pass:  I2C Access via Control Library")
        else:
            logging.error("Fail: I2C Access via Control Library")
            gdhm.report_driver_bug_clib("I2C Read Access Failed via Control Library for "
                                        "OpType: {0} Flag: {1} TargetId: {2}"
                                        .format(i2cReadArgs.OpType, i2cReadArgs.Flags,
                                                targetid))
            self.fail("I2C Read Access Call Failed via Control Library")

        # ToDo: Despite trying multiple offsets and addresses on simulated panels, and consulting with the dev/val,
        #  we could not verify the readability of those addresses, hence disabling it.

        # if control_api_wrapper.i2c_access(i2cReadArgs, targetid):
        #     logging.info("Pass:  I2C Access via Control Library")
        # else:
        #     logging.error("Fail: I2C Access via Control Library")
        #     gdhm.report_driver_bug_clib("I2C Read Access Failed via Control Library for "
        #                                 "OpType: {0} Flag: {1} TargetId: {2}"
        #                                 .format(i2cReadArgs.OpType,i2cReadArgs.Flags,
        #                                 targetid))
        #     self.fail("I2C Read Access Call Failed via Control Library")
        #
        # for data_index in range(0, i2cWriteArgs.DataSize):
        #     if i2cWriteArgs.Data[data_index] == i2cReadArgs.Data[data_index]:
        #         logging.info("PASS: I2C Access Read-Write Data verified")
        #     elif i2cWriteArgs.Data[data_index] != i2cReadArgs.Data[data_index]:
        #         logging.error("FAIL: I2C Access Read-Write Data is not matching, Expected-{}, Actual-{}"
        #                       .format(i2cWriteArgs.Data[data_index], i2cReadArgs.Data[data_index]))
        #         gdhm.report_driver_bug_clib("I2C Access Read-Write Data is not matching, Actual-{}, Expected-{}"
        #                         .format(i2cWriteArgs.Data[data_index], i2cReadArgs.Data[data_index]))
        #         self.fail("I2C Access Read-Write Data Mismatch")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control I2C Read Library Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)