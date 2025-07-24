########################################################################################################################
# @file         test_gaming_flip_modes_api.py
# @brief        Test calls for Gaming Flip Modes through Control Library and verifies return status of the API.
# @author       Pai, Vinayak1
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core.logger import gdhm
from Libs.Core.wrapper import control_api_args
from Libs.Core.wrapper import control_api_wrapper

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Control_API.control_api_base import testBase

##
# @brief - Test for Gaming FLip Modes
class TestGamingFlipModesAPI(testBase):

    ##
    # @brief            To get Async Flip Features
    # @param[in]        async_feature Async Flip Features
    # @return           Feature value
    @staticmethod
    def get_async_feature_value(async_feature):
        return {
            "APPLICATION_DEFAULT": control_api_args.CTL_BIT(0),
            "VSYNC_OFF": control_api_args.CTL_BIT(1),
            "VSYNC_ON": control_api_args.CTL_BIT(2),
            "SMOOTH_SYNC": control_api_args.CTL_BIT(3),
            "SPEED_FRAME": control_api_args.CTL_BIT(4),
            "CAPPED_FPS": control_api_args.CTL_BIT(5)
        }[async_feature]

    ##
    # @brief            To get app name
    # @param[in]        app_name Name of the App
    # @return           Complete Name of the Application
    @staticmethod
    def get_app_name(app_name):
        return {
            "FLIPAT": b"FlipAt.exe",
            "FLIPMODELD3D12": b"FlipModelD3D12.exe",
            "CLASSICD3D": b"Classic3DCubeApp.exe",
            "GLOBAL": b""
        }[app_name]

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Get-Set Gaming Flip modes via Control Library")

        if self.cmd_line_param['DX_APP'] != 'NONE':
            app = self.cmd_line_param['DX_APP'][0]
        else:
            app = "GLOBAL"

        if self.cmd_line_param['ASYNC_FEATURE'] != 'NONE':
            feature = self.cmd_line_param['ASYNC_FEATURE'][0]
        else:
            feature = "APPLICATION_DEFAULT"

        # Set call
        # For Global settings don't give app name in commandline
        argsSet3DFeature = control_api_args.ctl_3d_feature_getset_t()
        argsSet3DFeature.bSet = True
        argsSet3DFeature.ApplicationName = self.get_app_name(app)
        setFlipMode = self.get_async_feature_value(feature)
        logging.info(f" SET Flip Mode Value: {setFlipMode}")

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Set Gaming Flip Mode via Control Library")
            if control_api_wrapper.get_set_gaming_flip_modes(argsSet3DFeature, setFlipMode, targetid):
                logging.info("Pass:  Set Gaming Flip via Control Library")
            else:
                logging.error("Fail: Set Gaming Flip Mode via Control Library")
                gdhm.report_driver_bug_clib("Set Gaming Flip Mode Failed via Control Library for "
                                            "Application: {0} TargetId: {1}".format(
                                                argsSet3DFeature.ApplicationName, targetid
                                            ))
                self.fail("Set Gaming Flip Mode Failed via Control Library")

        # Get call
        argsGet3DFeature = control_api_args.ctl_3d_feature_getset_t()
        argsGet3DFeature.bSet = False
        argsGet3DFeature.ApplicationName = self.get_app_name(app)
        setFlipMode = self.get_async_feature_value(feature)
        logging.info(f" GET Flip Mode Value: {setFlipMode}")

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_2: Get Gaming Flip Mode via Control Library")
            if control_api_wrapper.get_set_gaming_flip_modes(argsGet3DFeature, setFlipMode, targetid):
                logging.info("Pass:  Get Gaming Flip Mode via Control Library")
            else:
                logging.error("Fail: Get Gaming Flip Mode via Control Library")
                gdhm.report_driver_bug_clib("Get Gaming Flip Mode Failed via Control Library for "
                                            "Application: {0} TargetId: {1}".format(
                                                argsGet3DFeature.ApplicationName, targetid
                                            ))
                self.fail("Get Gaming Flip Mode Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Library Get-Set Gaming Flip Mode API')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)