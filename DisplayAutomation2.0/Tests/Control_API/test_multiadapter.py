########################################################################################################################
# @file         test_multiadapter.py
# @brief        Test calls for Display Propeties and Device Properties API through Control Library and verifies return 
#               status of the API.
#                   * Enumerate Devices API.
#                   * Get Display Properties.
#                   * Get Device Properties.
# @author       Dheeraj Dayakaran
########################################################################################################################

import ctypes
import sys
import unittest
import logging
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.logger import gdhm
from Libs.Core.display_config import display_config
from Libs.Core import enum, winkb_helper, cmd_parser
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Tests.Control_API.test_multiadapter_base import IGCLMultiAdapterBase


##
# @brief - Test to verify IGCL in Multi-Adapter system
class IGCLMultiadapter(IGCLMultiAdapterBase):

    display_configuration = display_config.DisplayConfiguration()

    ##
    # @brief            Unit test runTest function
    # @return           void
    def runTest(self):
        connected_list = []

        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        connected_list.append((value['connector_port'], value['gfx_index']))
                if key == 'CONFIG':
                    if len(value) == len(self.display_details):
                        for i in range(0, len(self.display_details)):
                            topology = eval("enum.%s" %(value[i]))
                    else:
                        for i in range(0, len(self.display_details)):
                            topology = eval("enum.%s" % (value))

        self.enumerated_displays = self.display_configuration.get_enumerated_display_info()

        configuration, connector_port, display_and_adapter_info_list = self.display_configuration.get_current_display_configuration_ex(
        self.enumerated_displays)

        if self.display_configuration.set_display_configuration_ex(topology, display_and_adapter_info_list) is False:
            self.fail('Step %s Failed to apply display configuration %s %s' %
                (self.getStepInfo(), DisplayConfigTopology(topology).name, connector_port))
        else:
            logging.info('Step %s Successfully applied the display configuration as %s %s' %
                (self.getStepInfo(), DisplayConfigTopology(topology).name, connector_port))


        displayProperties = control_api_args.ctl_display_properties_t()
        displayProperties.Size = ctypes.sizeof(control_api_args.ctl_display_properties_t)

        device_properties = control_api_args.ctl_device_adapter_properties()
        device_properties.Size = ctypes.sizeof(device_properties)

        displayEncoderProperties = control_api_args.ctl_adapter_display_encoder_properties_t()
        displayEncoderProperties.Size = ctypes.sizeof(displayEncoderProperties)

        for gfx_index, value in self.display_details.items():
            logging.info(self.getStepInfo() + "Checking for support in connected panels: {0}: {1} ".format(
                          gfx_index, value))
            for each_port in value:
                self.target_id = self.display_configuration.get_target_id(connector_port=each_port,enumerated_displays=self.enumerated_displays,gfx_index=gfx_index.lower())
                logging.info(f"Target Id: {self.target_id}")
                logging.info(f"Display Status for {gfx_index} - {each_port} is {display_config.is_display_active(each_port,gfx_index.lower())}")
                    
                if control_api_wrapper.get_display_encoder_properties(displayEncoderProperties, self.target_id):
                    logging.info("Pass: Get Display Encoder Properties")
                    logging.info("Display WindowsDisplayEncoderID {}"
                                 .format(displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                    logging.info("EncoderConfigFlags {}".format(displayEncoderProperties.EncoderConfigFlags))
                
                if control_api_wrapper.get_display_properties(displayProperties, self.target_id):
                    logging.info("Pass: Get Display Properties")
                    logging.info("Display Target ID {}"
                                .format(displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                    logging.info("DisplayConfigFlags {}".format(displayProperties.DisplayConfigFlags))
                else:
                    logging.error("Fail: Get Display Properties")
                    gdhm.report_driver_bug_clib("Get Display Properties Failed via Control Library for TargetId: {0}".format(self.target_id))
                    self.fail("FAIL: Get Display Properties")

                logging.info("Get Device Properties")
                if control_api_wrapper.get_device_properties(device_properties, self.target_id):
                    logging.info("Pass: Device Properties")
                    logging.info("Name {}".format(device_properties.name))
                    logging.info("Vendor-ID {}".format(device_properties.pci_vendor_id))
                    logging.info("Device-ID {}".format(device_properties.pci_device_id))
                    logging.info("Rev-ID {}".format(device_properties.rev_id))
                else:
                    logging.error("Fail: Device Properties")
                    gdhm.report_driver_bug_clib("Get Device Properties Failed via Control Library for TargetId: {0}".format(self.target_id))
                    self.fail("FAIL: Device Properties")
                
                if verify(self.target_id,displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID):
                    logging.info(f"PASS: Verification passed for TargetID: {self.target_id}, Adapter: {gfx_index}")
                else:
                    logging.error(f"FAIL: Verification failed for TargetID: {self.target_id}, Adapter: {gfx_index}")


##
# @brief            Helper function for verification
# @param[in]        target_id : Target ID
# @param[in]        display_target_id : Display Target ID from Control API
# @return           True if both matches, else False
def verify(target_id,display_target_id):
    if target_id == display_target_id:
        return True
    return False


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Verify IGCL in Multi-Adapter Configuration')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)