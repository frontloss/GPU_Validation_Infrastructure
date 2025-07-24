########################################################################################################################
# @file         test_i2caccess_write.py
# @brief        Test calls for I2C Write Access through Control Library and verifies return status of the API.
#                   * I2C Write Access API.
#                   * I2C Write Access with back to back writes for different address.
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
# @brief - Verify I2C Write API Control Library Test
class testI2CWriteAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: I2C Write Access via Control Library")

        i2cargs = control_api_args.ctl_i2c_access_args()
        i2cargs.Size = ctypes.sizeof(i2cargs)

        i2cargs.OpType = control_api_args.ctl_operation_type.WRITE.value
        i2cargs.Address = 0xAB
        i2cargs.Offset = 0x51
        i2cargs.DataSize = 4
        i2cargs.Flags = 0
        i2cargs.Data[0] = 0x82
        i2cargs.Data[1] = 0x01
        i2cargs.Data[2] = 0x10
        i2cargs.Data[3] = 0xAC
        logging.info("I2C Write Args\n Address-{}, Offset-{}, DataSize-{}, Flags-{}"
                     .format(i2cargs.Address, i2cargs.Offset, i2cargs.DataSize, i2cargs.Flags))

        for data_index in range(0, i2cargs.DataSize):
            logging.info("I2C Args Write Data {}".format(i2cargs.Data[data_index]))

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)

            logging.info("Step_1: I2C Access Write")
            if control_api_wrapper.i2c_access(i2cargs, targetid):
                logging.info("Pass:  I2C Access via Control Library")
            else:
                logging.error("Fail: I2C Access via Control Library")
                gdhm.report_driver_bug_clib("I2C Write Access Failed via Control Library for "
                                            "Address: {0} OpType: {1} TargetId: {2}"
                                            .format(i2cargs.Address,i2cargs.OpType,
                                            targetid))
                self.fail("I2C Access via Control Library Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control I2C Write Library Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)