########################################################################################################################
# @file         test_uid.py
# @brief        Test case to verfiy configure control API for different UID.
# @author       Dheeraj Dayakaran
########################################################################################################################

import ctypes
import logging
import sys
import unittest

from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_args
from Libs.Core.wrapper import control_api_wrapper
from Tests.Control_API.control_api_base import testBase

# Platforms which are not to be included 
GEN_PUBLIC = machine_info.GEN_09_PLATFORMS + machine_info.GEN_10_PLATFORMS + machine_info.GEN_11_PLATFORMS + machine_info.GEN_11p5_PLATFORMS + machine_info.GEN_12_PLATFORMS[
                                                                                                                                               :3]
GEN_IGCC = machine_info.GEN_09_PLATFORMS + machine_info.GEN_10_PLATFORMS + machine_info.GEN_11_PLATFORMS + machine_info.GEN_11p5_PLATFORMS + machine_info.GEN_12_PLATFORMS[
                                                                                                                                             1:3]

# Current Platform name
PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName

GEN_LIST = {
    "PUBLIC": GEN_PUBLIC,
    "IGCC": GEN_IGCC,
    "OEM": GEN_PUBLIC,
}

GEN_UID = {
    "PUBLIC_UID": (0x00000000, 0x0000, 0x0000, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    "IGCC_UID": (0x372464b5, 0xd1b4, 0x419d, [0x82, 0xe7, 0xef, 0xe5, 0x1b, 0x84, 0xfd, 0x8b]),
    "OEM_UID": (0x6b6936bf, 0x1a79, 0x4d3f, [0x8d, 0xf4, 0xe8, 0xd8, 0x4e, 0x0e, 0xb6, 0x76])
}


##
# @brief - Test to verify for different UID
class verify_uid(testBase):

    ##
    # @brief            Unit test runTest function
    # @return           void
    def runTest(self):

        logging.info("Test: Control Library Application UID Test")

        if (self.cmd_line_param['UID'] != "NONE"):
            application_uid = self.cmd_line_param['UID'][0]
        else:
            self.fail("Incorrect Command line: Test requires UID Type like Public, IGCC or OEM to be given")

        logging.info("Step: Close Control Library")
        if control_api_wrapper.close_ctl_api():
            logging.info("Pass: Close Control Library")
        else:
            logging.error("Fail: Close Control Library")
            gdhm.report_driver_bug_clib("Close Control Library Failed")
            self.fail("Close Control Library Failed")

        init_uid(self, application_uid)

        device_properties = control_api_args.ctl_device_adapter_properties()
        device_properties.Size = ctypes.sizeof(device_properties)

        for display_index in range(len(self.connected_list)):
            target_id = self.display_config.get_target_id(self.connected_list[display_index],
                                                          self.enumerated_displays)

            logging.info("Step: Get Device Properties")
            if control_api_wrapper.get_device_properties(device_properties, target_id):
                logging.info("Pass: Device Properties")
                logging.info(f"Name {device_properties.name}")
                logging.info(f"Vendor-ID {device_properties.pci_vendor_id}")
                logging.info(f"Device-ID {device_properties.pci_device_id}")
                logging.info(f"Rev-ID {device_properties.rev_id}")
            else:
                gdhm.report_driver_bug_clib("Get Device Properties Failed via Control Library for "
                                        "TargetId: {0}".format(target_id))
                self.fail("Fail: Device Properties")


##
# @brief            Helper function for UID
# @param[in]        application_uid : Application UID
# @return           Application UID
def uid_helper(application_uid):
    if (application_uid + "_UID") in GEN_UID:
        return GEN_UID[application_uid + "_UID"]


##
# @brief            Helper function for init control library
# @param[in]        platform_name : Platform name
# @param[in]        application_uid : Application UID
# @return           True if success else False
def verify_init(platform_name, application_uid):
    logging.info(f"Application UID : {application_uid}")
    logging.info(f"Pass: Platform {platform_name} in supported list")
    init_args = control_api_args.ctl_init_args(application_uid=application_uid)
    init_args.Size = ctypes.sizeof(init_args)
    logging.info(f"Step: Init Control Library with uid: {application_uid}")
    if control_api_wrapper.init_ctl_api(init_args) is False:
        return False
    return True


##
# @brief            Init function for uid
# @param[in]        self : Present Instance
# @param[in]        application_uid : Application UID
# @return           Void
def init_uid(self, application_uid):
    if application_uid in GEN_LIST:
        if PLATFORM_NAME not in GEN_LIST[application_uid]:
            uid = uid_helper(application_uid)
            if verify_init(PLATFORM_NAME, uid) is False:
                self.fail(f"Fail: Init Control Library Failed for UID {uid}")
            logging.info(f"Pass: Init Control Library for UID {uid}")
        else:
            self.fail(f"Fail: Platform {PLATFORM_NAME} not in supported list.")
    else:
        self.fail("Incorrect Command line: Test needs UID input like PUBLIC, IGCC or OEM to be given")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test Purpose: Verify IGCL INIT with different Supported UIDs')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
