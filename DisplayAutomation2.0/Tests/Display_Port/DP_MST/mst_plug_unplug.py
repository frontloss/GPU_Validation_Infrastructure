################################################################################################################
# @file          mst_plug_unplug.py
# @brief         Verify whether topology detected properly for DP port.
# @author        Praveen Bademi
################################################################################################################

import logging
import sys
import unittest

from Libs.Core import driver_escape
from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.vdsc.dsc_enum_constants import DPCDOffsets
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase


##
# @brief        This class contains runtest() method that sets and verifies the MST topology and performs FEC
#               verification if there is single MST FEC display else verification process is skipped
class DPMSTSimpleTopology(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It checks if requested port is present in free port list
    #               and fetches port type, topology type, xmlfile for 1st port index and then applies and verifies the
    #               MST topology.It performs FEC verification only if there is single MST FEC display, in 2 steps.
    #               First it checks if FEC_CAPABLE bit of Fec_Capability offset is set in dpcd register and verifies if
    #               FEC_STATUS is set by the driver.This helps to verify if FEC is enabled for FEC supported display.In
    #               the second step it verifies if FEC ready bit of FEC_configuration is set by the driver
    # @return       None
    def runTest(self):
        cls = DisplayPortMSTBase

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

        display_and_adapter_info_list = cls.get_current_display_and_adapter_info_list(is_lfp_info_required=False)
        no_of_displays = len(display_and_adapter_info_list)

        # Currently Limiting the FEC verification 1 Display since current framework doesn't have support to get the
        # pipe, ddi and transcoder in case of multiple displays connected to the branch or if the displays are in daisy
        # chained mode which is required for FEC verification.
        if no_of_displays == 1:
            is_success = cls.display_config.set_display_configuration_ex(enum.SINGLE, display_and_adapter_info_list)
            self.assertTrue(is_success, "Set Display Configuration Failed")

            link_rate: float = dpcd_helper.DPCD_getLinkRate(display_and_adapter_info_list[0].TargetID)
            logging.debug('Link Rate Trained by Driver: {}'.format(link_rate))

            # FEC Enable bit in DP_TP_CTL Register won't be set by driver for DP 2.1 displays as FEC is inherent to the
            # protocol and FEC will be enabled by the HW. Note: HW won't set this bit.
            if link_rate >= 10:
                logging.info("Skipping FEC Enable Bit (DP_TP_CTL register) Verification for DP2.1 Displays")
                return

            is_status, fec_capability = driver_escape.read_dpcd(display_and_adapter_info_list[0],
                                                                DPCDOffsets.FEC_CAPABILITY_OFFSET)
            if is_status is True:
                logging.info("FEC Capability: {}".format(fec_capability[0]))

                if fec_capability[0] & 1 == 1:
                    gfx_index = display_and_adapter_info_list[0].adapterInfo.gfxIndex
                    is_fec_enabled = DSCHelper.get_fec_status_ex(gfx_index, port_type)
                    if is_fec_enabled is False:
                        gdhm.report_bug(
                            title="[Interfaces][DP_MST] FEC is not enabled for FEC Supported Device at port {}".format(
                                port_type),
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                    self.assertTrue(is_fec_enabled, "FEC is Not Enabled for FEC Supported Device at port {}.".format(
                        port_type))

                    logging.info("FEC is Enabled for FEC Supported Display Connected at port {}".format(port_type))

                    is_fec_ready_bit_set = DSCHelper.get_fec_ready_status(display_and_adapter_info_list[0])
                    if is_fec_ready_bit_set is False:
                        gdhm.report_bug(
                            title="[Interfaces][DP_MST] FEC Ready Bit is not set by the driver",
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                    self.assertTrue(is_fec_ready_bit_set, "FEC Ready Bit is not set by the driver.")

                    logging.info("FEC Ready bit is Set in the FEC_CONFIGURATION")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
