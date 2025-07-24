################################################################################################################
# @file         mst_b2b_link_loss.py
# @brief        Verify whether Back to back(10 times) link loss is triggered and
#                   Display comes back successfully or not for DP MST config.
# @details      commandline: python.exe mst_b2b_link_loss.py \<portName> -PLUG_TOPOLOGIES \<topology name>
#               e.g. dp_mst_link_loss.py -EDP_A -DP_B -PLUG_TOPOLOGIES MST_LT_1B1M
#
#               This test_script follows:
#               1. Hot Plug MST Hub/Display
#               2. Verify if MST plug is successful and display is up.
#               3. Clear DPCD Status register ( 0x00202, 0x00203, 0x00204), required to simulate link loss scenario
#               4. Trigger SPI, required to simulate link loss scenario
#               5. Wait for some time(8 seconds) for MST display to come up after link loss or not.
#               6. Check if MST Display is Active or not, Mode set is same as before(pre SPI) or not.
#               7. Repeat step 3 to 6 as provided in the cmdline
# @author       Ashish Kumar
################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core.display_config import display_config
from Libs.Core import driver_escape
from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Tests.Display_Port.DP_LinkTraining.display_link_training_base import DisplayLinkTrainingBase
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase


##
# @brief DpMstLinkLoss Class
class MstB2BLinkLoss(DisplayPortMSTBase):

    ##
    # @brief    executes the actual test steps for DP MST Link Loss scenario.
    # @return   None
    def runTest(self):
        # Variable for DP Port Number Index
        dp_port_index = 0

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Function call to set DP1.2 topology
        self.setnverifyMST(port_type, topology_type, xml_file)

        # DPCD status Register are set to 0x00, Trigger SPI to simulating link loss scenario
        display_conf = display_config.DisplayConfiguration()

        # Get display and adapter info before applying config
        display_info_list = display_conf.get_display_and_adapter_info_ex(port_type, 'gfx_0')

        if type(display_info_list) == list:
            display_conf.set_display_configuration_ex(enum.EXTENDED, display_info_list)
        else:
            display_conf.set_display_configuration_ex(enum.SINGLE, [display_info_list])

        # Get display and adapter info after config is applied
        display_info_list = display_conf.get_display_and_adapter_info_ex(port_type, 'gfx_0')
        target_dict = {}
        if type(display_info_list) != list:
            display_info_list = [display_info_list]
        for display_info in display_info_list:
            enumerated_port_type = CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            if enumerated_port_type == port_type:
                target_id = display_info.TargetID
                is_active = display_info.adapterInfo.isActive
                if not is_active:
                    logging.error("TargetId: {} is not active".format(target_id))
                    self.fail("Failed: TargetId:{} is not active".format(target_id))
                else:
                    mode = display_conf.get_current_mode(target_id)
                    target_dict[target_id] = [is_active, mode]
                    logging.info("TargetId: {}, IsActive: {}, mode:{}".format(target_id, is_active, str(mode)))
            else:
                logging.warning("Before LinkLoss: Port type from enumerated display({}) and cmdline({}) mismatch".
                                format(enumerated_port_type, port_type))

        # Clear DPCD status Register
        dpcd_offset = 0x00202
        dpcd_status_data = [0x00, 0x00, 0x80]

        # Trigger Link Loss
        for ll_iter in range(self.linkloss_iteration):
            is_success = driver_escape.write_dpcd(display_info_list[0], dpcd_offset, dpcd_status_data)
            self.assertTrue(is_success, "Unable to write DPCD Data")

            logging.debug("Success: DPCD Write for port:{0}, Offset:{1}".format(port_type, hex(dpcd_offset)))

            # Trigger SPI
            driver_interface.DriverInterface().set_spi(display_info_list[0].adapterInfo, port_type, 'NATIVE')

            # Sleep for some time for SPI and re-link training
            time.sleep(8)

            display_info_list = display_conf.get_display_and_adapter_info_ex(port_type,'gfx_0')
            current_target_dict = {}
            if type(display_info_list) != list:
                display_info_list = [display_info_list]
            for display_info in display_info_list:
                enumerated_port_type = CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
                if enumerated_port_type == port_type:
                    target_id = display_info.TargetID
                    is_active =  display_info.adapterInfo.isActive
                    current_target_dict[target_id] = is_active
                else:
                    logging.warning("After LinkLoss[{}]: Port type from enumerated display({}) and cmdline({}) mismatch".
                                    format(ll_iter, enumerated_port_type, port_type))
            if len(target_dict.keys()) != len(current_target_dict.keys()):
                logging.error(" Enumerated displays does not match, Before: {}, After:{}".format(len(target_dict.keys()), len(current_target_dict.keys())))
                self.fail("Failed: Enumerated displays mismatch")

            else:
                logging.info("Number of Enumerated Displays matches before and after the Linkloss[Iteration:{}]"
                             .format(ll_iter))

            for curr_target_id in current_target_dict:
                if current_target_dict[curr_target_id] != target_dict[curr_target_id][0]:
                    logging.error("Display({}) is not Active after the Linkloss[Iteration:{}]".
                                  format(curr_target_id, ll_iter))
                    self.fail("Failed: After LinkLoss, TargetId:{} is not active".format(curr_target_id))

                curr_mode = display_conf.get_current_mode(curr_target_id)
                if target_dict[curr_target_id][1] != curr_mode:
                    logging.error("ModeSet before{} and after{} SPI does not match for targetId:{}".format(
                        str(target_dict[curr_target_id][1]), str(curr_mode), curr_target_id))
                    self.fail("Failed: modeset mismatch")
                else:
                    logging.info("ModeSet before{} and after{} SPI matched for targetID: {}".format(
                        str(target_dict[curr_target_id][1]), str(curr_mode), curr_target_id))

        logging.debug("Success: exiting mst_b2b_link_loss()")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
