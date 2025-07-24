########################################################################################################################
# @file         test_display_properties_api.py
# @brief        Test calls for Enumerate Display API through Control Library and verifies return status of the API.
#                   * Enumerate Devices API.
#                   * Enumerate Display API.
#                   * Get Display Properties API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core import display_essential
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase


##
# @brief - Verify Display Properties API Control Library Test
class testDisplayPropertiesAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        displayProperties = control_api_args.ctl_display_properties_t()
        displayProperties.Size = ctypes.sizeof(displayProperties)

        displayEncoderProperties = control_api_args.ctl_adapter_display_encoder_properties_t()
        displayEncoderProperties.Size = ctypes.sizeof(displayEncoderProperties)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1: Get Display Properties")
            if control_api_wrapper.get_display_properties(displayProperties, targetid):
                logging.info("Pass: Get Display Properties")
                if targetid == displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID:
                    logging.info("Display Target_ID {} verified"
                                 .format(displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                    logging.info("Display_Config_Flags {}".format(displayProperties.DisplayConfigFlags))
                    logging.info("Type {}".format(displayProperties.Type))
                    logging.info("Attached_Display_MuxType {}".format(displayProperties.AttachedDisplayMuxType))
                    logging.info("Protocol_Converter_Output {}".format(displayProperties.ProtocolConverterOutput))
                    logging.info("Protocol_Converter_Type {}".format(displayProperties.ProtocolConverterType))
                    logging.info("Feature_Enabled_Flags {}".format(displayProperties.FeatureEnabledFlags))
                    logging.info("Feature_Supported_Flags {}".format(displayProperties.FeatureSupportedFlags))
                    logging.info(
                        "Advanced_Feature_Enabled_Flags {}".format(displayProperties.AdvancedFeatureEnabledFlags))
                    logging.info("Advanced_Feature_Supported_Flags {}"
                                 .format(displayProperties.AdvancedFeatureSupportedFlags))
                    logging.info("Supported_Output_BPC_Flags {}".format(displayProperties.SupportedOutputBPCFlags))
            else:
                logging.error("Fail: Get Display Properties")
                gdhm.report_driver_bug_clib("Get Display Properties failed via Control Library for targetId: {0}".format(targetid))
                self.fail("Get Display Properties Failed")

            logging.info("Step_2: Get Display Properties back to back calls")
            if control_api_wrapper.get_display_properties(displayProperties, targetid):
                logging.info("Pass: Get Display Properties")
                logging.info("Display Target ID {}"
                             .format(displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                logging.info("DisplayConfigFlags {}".format(displayProperties.DisplayConfigFlags))
                if control_api_wrapper.get_display_encoder_properties(displayEncoderProperties, targetid):
                    logging.info("Pass: Get Display Encoder Properties")
                    logging.info("Display WindowsDisplayEncoderID {}"
                                 .format(displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                    logging.info("EncoderConfigFlags {}".format(displayEncoderProperties.EncoderConfigFlags))
            else:
                logging.error("Fail: Get Display Properties")
                gdhm.report_driver_bug_clib("Get Display Properties failed via Control Library for targetId: {0}".format(targetid))
                self.fail("Get Display Properties Failed via Control Library")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Library Display Properties API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
