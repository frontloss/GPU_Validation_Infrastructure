########################################################################################################################
# @file         test_device_properties_api.py
# @brief        Test calls for Device Properties API through Control Library and verifies return status of the API.
#                   * Enumerate Devices API.
#                   * Get Device Properties.
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
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.Control_API.control_api_base import testBase


##
# @brief - Verify Device Properties API Control Library Test
class testDevicePropertiesAPI(testBase):
    ##
    # @brief            Logging device properties
    # @param[in]        deviceProperties
    # @return           void
    def log_device_properties(self, deviceProperties):
        logging.info("Name {}".format(deviceProperties.name))
        logging.info("Vendor-ID {}".format(deviceProperties.pci_vendor_id))
        logging.info("Device-ID {}".format(deviceProperties.pci_device_id))
        logging.info("Rev-ID {}".format(deviceProperties.rev_id))
        logging.info(" OS specific device id {}".format(deviceProperties.pDeviceID))
        logging.info(" Device type {}".format(deviceProperties.device_type))
        logging.info(" Supported subfunction flag {}".format(deviceProperties.supported_subfunction_flags))
        logging.info(" Driver version {}".format(deviceProperties.driver_version))
        logging.info(" Firmware major version:{}, Firmware minor version:{}, Firmware build number:{} ".format(
            deviceProperties.firmware_version.major_version, deviceProperties.firmware_version.minor_version,
            deviceProperties.firmware_version.build_number))
        logging.info(" Number of EUs per sub-slice {}".format(deviceProperties.num_eus_per_sub_slice))
        logging.info(" Number of sub-slices per slice {}".format(deviceProperties.num_sub_slices_per_slice))
        logging.info(" Number of slices {}".format(deviceProperties.num_slices))
        logging.info(" Graphics Adapter Properties {}".format(deviceProperties.graphics_adapter_properties))

    ##
    # @brief            verifying device properties
    # @param[in]        deviceProperties
    # @return           void
    def verify_device_properties(self, deviceProperties):
        supportSubfunctionFlag = "{0:08b}".format(int(str(deviceProperties.supported_subfunction_flags), 16))
        supportSubfunctionFlagValue = (int(supportSubfunctionFlag) & (1 << 0))
        verify = (deviceProperties.name != None) and (deviceProperties.pci_vendor_id != 0) and (
                deviceProperties.pci_device_id != 0) and (
                         deviceProperties.pDeviceID != 0) and (deviceProperties.device_type != None) and (
                         supportSubfunctionFlagValue != 0) and (deviceProperties.driver_version != 0) and (
                         deviceProperties.firmware_version != 0) and (
                         deviceProperties.num_eus_per_sub_slice != 0) and (
                         deviceProperties.num_sub_slices_per_slice != 0) and (
                         deviceProperties.num_slices != 0) and (
                         deviceProperties.graphics_adapter_properties != 0)
        if True == verify:
            logging.info("PASS: Device Properties verification")
        else:
            logging.error("FAIL: Expected Non-zero Value Of Device Properties But Found Zero Value")
            gdhm.report_driver_bug_clib("Get Device Properties Verification Failed")
            self.fail("FAIL: Device Properties verification")

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        deviceProperties = control_api_args.ctl_device_adapter_properties()
        deviceProperties.Size = ctypes.sizeof(deviceProperties)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)
            logging.info("Step_1:Get Device Properties via Control Library")
            if control_api_wrapper.get_device_properties(deviceProperties, targetid):
                self.log_device_properties(deviceProperties)
                logging.info("Step_2: Device Properties Verification via Control Library")
                self.verify_device_properties(deviceProperties)
            else:
                gdhm.report_driver_bug_clib("Get Display Properties Failed via Control Library for targetID: {0}"
                                            .format(targetid))
                self.fail("FAIL: Get Display Properties Failed via Control Library")

            logging.info("Step_3: Generate TDR")
            VerifierCfg.tdr = Verify.SKIP
            logging.debug("TDR - under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))
            self.assertEqual(display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True), True,
                         "TDR is not generated")
            logging.info("TDR generated Successfully")

            self.assertEqual(display_essential.detect_system_tdr(gfx_index='gfx_0'), True, "TDR is not detected")
            logging.info("TDR detected Successfully")

            if display_essential.clear_tdr() is True:
                logging.info("TDR dump cleared successfully post TDR generation")

            logging.info("Step_4: Get Device Properties via Control Library")
            self.log_device_properties(deviceProperties)
            logging.info("Step_5: Device Properties Verification via Control Library")
            self.verify_device_properties(deviceProperties)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Device Properties API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)


