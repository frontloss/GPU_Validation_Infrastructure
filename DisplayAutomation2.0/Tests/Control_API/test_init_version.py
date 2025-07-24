########################################################################################################################
# @file         test_init_version.py
# @brief        Control Library DLL Major and Minor version verification.
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
from Libs.Core import display_essential
from Tests.Control_API.control_api_base import testBase

##
# @brief - Verify Basic API calls Control Library Test
class testBasicAPI(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Control Library Basic")

        if (self.cmd_line_param['IGCL_MAJOR_VERSION'] is not None) and \
                (self.cmd_line_param['IGCL_MINOR_VERSION'] is not None):
            CTL_IMPL_MAJOR_VERSION = int(self.cmd_line_param['IGCL_MAJOR_VERSION'][0])
            CTL_IMPL_MINOR_VERSION = int(self.cmd_line_param['IGCL_MINOR_VERSION'][0])
        else:
            logging.error("Incorrect Command line: Test requires IGCL version to verify Major, Minor Version testing")
            self.fail()

        logging.info("Step: Close Control Library")
        if control_api_wrapper.close_ctl_api():
            logging.info("Pass: Close Control Library")
        else:
            logging.error("Fail: Close Control Library")
            gdhm.report_driver_bug_clib("Close Control Library Failed")
            self.fail("Close Control Library Failed")
        new_impl_version = control_api_args.CTL_MAKE_VERSION(CTL_IMPL_MAJOR_VERSION, CTL_IMPL_MINOR_VERSION)
        new_app_id = control_api_args.ctl_application_id_t(0x00000000, 0x0000, 0x0000, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        logging.debug("New IGCL Version {}, New App ID [Data1 {}, Data2 {}, Data3 {}]".format(
            new_impl_version, new_app_id.Data1, new_app_id.Data2, new_app_id.Data3))

        initargs = control_api_args.ctl_init_args(new_impl_version, new_app_id)
        initargs.Size = ctypes.sizeof(initargs)

        logging.info("Step: Init Control Library")
        if control_api_wrapper.init_ctl_api(initargs):
            logging.info("Pass: Init Control Library")
        else:
            logging.error("Fail: Init Control Library")
            gdhm.report_driver_bug_clib("Init Control Library Failed for "
                                        "Impl Version:{0} App_id: {1}".format(
                                            new_impl_version,new_app_id
                                        ))
            self.fail("Init Control Library Failed")

        deviceProperties = control_api_args.ctl_device_adapter_properties()
        deviceProperties.Size = ctypes.sizeof(deviceProperties)

        for display_index in range(len(self.connected_list)):
            targetid = self.display_config.get_target_id(self.connected_list[display_index],
                                                         self.enumerated_displays)

            logging.info("Step: Get Device Properties")
            if control_api_wrapper.get_device_properties(deviceProperties, targetid):
                logging.info("Pass: Device Properties")
                logging.info("Name {}".format(deviceProperties.name))
                logging.info("Vendor-ID {}".format(deviceProperties.pci_vendor_id))
                logging.info("Device-ID {}".format(deviceProperties.pci_device_id))
                logging.info("Rev-ID {}".format(deviceProperties.rev_id))
            else:
                logging.error("Fail: Device Properties")
                gdhm.report_driver_bug_clib("Get Device Properties Failed for "
                                            "TargetID: {0}".format(targetid))
                self.fail("FAIL: Device Properties")

        if control_api_wrapper.close_ctl_api():
            logging.info("PASS: Close Control Library")

            new_app_id = control_api_args.ctl_application_id_t(0x372464b5, 0xd1b4, 0x419d,
                                                      [0x82, 0xe7, 0xef, 0xe5, 0x1b, 0x84, 0xfd, 0x8b])
            new_impl_version = control_api_args.CTL_MAKE_VERSION(CTL_IMPL_MAJOR_VERSION, CTL_IMPL_MINOR_VERSION)
            initargs = control_api_args.ctl_init_args(new_impl_version, new_app_id)
            initargs.Size = ctypes.sizeof(initargs)

            logging.info("Init Control Library for DLL backward compatibility of major and minor version")

            if control_api_wrapper.init_ctl_api(initargs) is True:
                logging.info("Pass: DLL Backward Compatibility Check for Init Control Library")
            else:
                logging.error("Fail: DLL Backward Compatibility Check for Init Control Library")
                gdhm.report_driver_bug_clib("DLL Backward Compatibility Check for Init Control Library Failed for "
                                            "Impl Version:{0} App_id: {1}".format(
                    new_impl_version, new_app_id
                ))
                self.fail("DLL Backward Compatibility Check for Init Control Library Failed")
        else:
            logging.info("FAIL: Close Control Library")
            gdhm.report_driver_bug_clib("Init Control Library Failed for "
                                        "Impl Version:{0} App_id: {1}".format(
                                            new_impl_version, new_app_id
                                        ))
            self.fail("Close Control Library Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control basic Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
