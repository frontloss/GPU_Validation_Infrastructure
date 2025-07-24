########################################################################################################################
# @file         test_i2caccess_read.py
# @brief        Test calls for I2C Read Access through Control Library and verifies return status of the API.
#                   * I2C Read Access API.
#                   * I2C Read Access with back to back reads for different address.
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
# @brief - Verify I2C Read API Control Library Test
class testI2CReadAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: I2C Read Access via Control Library")

        i2cargs = control_api_args.ctl_i2c_access_args()
        i2cargs.Size = ctypes.sizeof(i2cargs)

        i2cargs.OpType = control_api_args.ctl_operation_type.READ.value
        i2cargs.Address = 0xAB
        i2cargs.Offset = 0x51
        i2cargs.DataSize = 11
        i2cargs.Flags = 0
        logging.info("I2C Read Args\n Address-{}, Offset-{}, DataSize-{}, Flags-{}"
                     .format(i2cargs.Address, i2cargs.Offset, i2cargs.DataSize, i2cargs.Flags))

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: I2C Read Access")
            if control_api_wrapper.i2c_access(i2cargs, targetid):
                logging.info("Pass:  I2C Access via Control Library")
            else:
                logging.error("Fail: I2C Access via Control Library")
                gdhm.report_driver_bug_clib("I2C Read Access Failed via Control Library for "
                                            "OpType: {0} Address: {1} Offset: {2} TargetId: {3}"
                                            .format(i2cargs.OpType,i2cargs.Address,i2cargs.Offset,targetid))
                self.fail("I2C Read Access Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test I2C Read for Control Library Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)