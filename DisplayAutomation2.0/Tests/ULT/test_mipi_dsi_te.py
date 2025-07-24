######################################################################################
# @file    test_mipi_dsi_te.py
# @brief   This script is to generate MIPI te
# @author  Chandrakanth Pabolu
######################################################################################
import unittest
import time
import logging
from Libs.Core.enum import *
from Libs.Core.sw_sim.driver_interface import DriverInterface
from Libs.Core.test_env.test_environment import *
from Libs.Core.system_utility import *
from Libs.Core.test_env.test_context import *
from Libs.Feature.crc_and_underrun_verification import *
from registers.mmioregister import MMIORegister
from Libs.Core.sw_sim.gfxvalsim import *

##
# @brief This class helps to generate mipi te for the adapter passed
class TestTe(unittest.TestCase):

    ##
    # @brief        This class method is the entry point for test_mipi_dsi_te.
    # @return       pass
    def setUp(self):
        pass

    ##
    # @brief        Teardown function
    # @return       pass
    def tearDown(self):
        pass

    ##
    # @brief        This function helps to run test which will generate mipi te
    # @return       True if pass; False otherwise
    def runTest(self):
        gfx_adapter = TestContext.get_gfx_adapter_details()['gfx_0']
        # ret = valsim_obj.generate_mipi_te(gfx_adapter, 1)
        # logging.info('set_te status for port {0} = {1}'.format('DSI_0', ret))
        # time.sleep(1)

        # send 1 for DSI_0, or 2 for DSI_1
        ret = DriverInterface().generate_mipi_te(gfx_adapter, 2)
        logging.info('set_te status for port {0} = {1}'.format('DSI_1', ret))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
