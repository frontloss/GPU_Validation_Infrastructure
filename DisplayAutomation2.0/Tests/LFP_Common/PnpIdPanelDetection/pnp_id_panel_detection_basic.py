########################################################################################################################
# @file         pnp_id_panel_detection_basic.py
# @brief        Test to enable LFP feature using PNP ID based Panel Detection
# @author       Tulika
########################################################################################################################
import unittest

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Modules import common
from Tests.LFP_Common.PnpIdPanelDetection.pnp_id_panel_detection_base import PnpIdPanelDetectionBase


##
# @brief        This class contains test to validate PNP ID and feature status in driver
class PnpIdPanelDetectionBasic(PnpIdPanelDetectionBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function validates PNP ID and feature status in driver
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_pnpid_basic(self):
        self.validate_feature(self)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PnpIdPanelDetectionBasic))
    test_environment.TestEnvironment.cleanup(test_result)

