########################################################################################################################
# @file         driver_wa_ult.py
# @brief        Driver WA verification for given adapter
# @details      @ref driver_wa_ult.py <br>
#               This file checks the Driver HW WA enabled/disabled using valsim interface.
#
# @author       Chandrakanth Reddy
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core.wrapper import valsim_args

from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_environment import TestEnvironment


class DriverWaTest(unittest.TestCase):

    def runTest(self):
        driver_interface_ = driver_interface.DriverInterface()
        status = driver_interface_.get_driver_wa_table('gfx_0', valsim_args.DriverWa.Wa_14013475917)
        if status is None:
            self.fail("Failed to get Driver WA data")
        logging.info(f"Wa_14013475917 Enable = {status}")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
