########################################################################################################################
# @file         test_i2caccess_blockedaddress.py
# @brief        Negative Test for I2C Read/Write Access through Control Library and verifies return status of the API.
#                   * I2C Write Access for Blocked Address.
#                   * I2C Read Access for Blocked Address.
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
# @brief - Verify I2C Write Read for Blocked Address
class testI2CBlockAddressAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: I2C Access Write and Read for Blocked Address via Control Library")

        i2cWriteArgs = control_api_args.ctl_i2c_access_args()
        i2cWriteArgs.Size = ctypes.sizeof(i2cWriteArgs)
        blocked_address_read_write_list = [0x70, 0x72, 0x74]
        blocked_address_write_list = [0xA0, 0xA2]
        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: I2C Access Write for Blocked Address")
            for index in range(0, len(blocked_address_write_list)):
                i2cWriteArgs.OpType = control_api_args.ctl_operation_type.WRITE.value
                i2cWriteArgs.Address = blocked_address_write_list[index]
                i2cWriteArgs.Offset = 0x51
                i2cWriteArgs.DataSize = 4
                i2cWriteArgs.Flags = 0
                i2cWriteArgs.Data[0] = 0x82
                i2cWriteArgs.Data[1] = 0x01
                i2cWriteArgs.Data[2] = 0x10
                i2cWriteArgs.Data[3] = 0xAC

                logging.info("I2C Write Args - Address-{}, Offset-{}, DataSize-{}, Flags-{}"
                             .format(i2cWriteArgs.Address, i2cWriteArgs.Offset,
                                     i2cWriteArgs.DataSize, i2cWriteArgs.Flags))

                if control_api_wrapper.i2c_access(i2cWriteArgs, targetid) is False:
                    logging.info("Pass: I2C Access Write Failed for Blocked Address")
                else:
                    logging.error("Fail: I2C Access write passed for Blocked Address")
                    gdhm.report_driver_bug_clib("I2C Access write passed for Blocked Address for "
                                        "Address: {0} TargetId: {1}".format(i2cWriteArgs.Address,targetid))
                    self.fail("I2C Access write passed for Blocked Address")

            i2cReadArgs = control_api_args.ctl_i2c_access_args()
            i2cReadArgs.Size = ctypes.sizeof(i2cReadArgs)
            i2cReadArgs.OpType = control_api_args.ctl_operation_type.READ.value
            i2cReadArgs.DataSize = 11
            i2cReadArgs.Flags = 0
            i2cReadArgs.Offset = 0x51

            logging.info("Step_2: I2C Read Access for Blocked Address")
            for index in range(0, len(blocked_address_read_write_list)):
                i2cReadArgs.Address = blocked_address_read_write_list[index]
                logging.info("I2C  Read Args - Address-{}, Offset-{}, DataSize-{}, Flags-{}"
                             .format(i2cReadArgs.Address, i2cReadArgs.Offset, i2cReadArgs.DataSize, i2cReadArgs.Flags))

                if control_api_wrapper.i2c_access(i2cReadArgs, targetid) is False:
                    logging.info("Pass:  I2C Access via Control Library")
                else:
                    logging.error("Fail: I2C Access via Control Library")
                    gdhm.report_driver_bug_clib("I2C Access Read via Control Library Failed for "
                                                "Address: {0} Offset: {1} Flags: {2}".format(
                                                    i2cReadArgs.Address, i2cReadArgs.Offset,i2cReadArgs.Flags
                                                ))
                    self.fail("I2C Read Access Call {} Failed via Control Library".format(index))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test I2C Read Write Access for Blocked Address')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
