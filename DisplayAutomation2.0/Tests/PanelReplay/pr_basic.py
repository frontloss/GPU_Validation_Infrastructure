#################################################################################################################
# @file         pr_basic.py
# @brief        This file implements panel replay functionality basic test.
#                This test is to check if panel replay gets enabled or not.
#                The display configuration passed in commandline.
#                Sample Commandline: python pr_basic.py -dp_b
# Tests\PanelReplay\pr_basic.py -DP_C -PLUG_TOPOLOGIES MST_PR_1B1M MST_1B1M
# @author       ashishk2
#################################################################################################################
import unittest
import sys
import logging
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PanelReplay.pr_base import PrBase
from Libs.Feature.display_psr import DisplayPsr
from Libs.Core.logger import gdhm
from Tests.PowerCons.Modules import common

##
# @brief        PrFeatureBasic
class PrFeatureBasic(PrBase):

    ##
    # @brief        runTest
    # @return       None
    def runTest(self):

        display_psr = DisplayPsr()
        display_psr.socwatch_check = True

        port_type = self.mstBase.get_dp_port_from_availablelist(self._port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.mstBase.get_topology_type(self._port_index)

        # Get Topology XML file from command line
        xml_file = self.mstBase.get_xmlfile(self._port_index)

        # Get Platform name
        platform = self.mstBase.get_platform_name()

        # Function call to set MST topology
        self.mstBase.setnverifyMST(port_type, topology_type, xml_file)

        # Wait to enable panel reply
        time.sleep(15)

        display_and_adapter_info_list = self.mstBase.get_current_display_and_adapter_info_list(is_lfp_info_required=False)
        no_of_displays = len(display_and_adapter_info_list)

        # Check if Panel Replay is supported in sink DPCD
        if not self.PanelReplaySupportedinDPCD(port_type, self.platform):
            self.report_to_gdhm("[Powercons][DP_PR] Panel Replay support failed in PR Capable Sink", gdhm.Component.Test.DISPLAY_POWERCONS)
            self.fail("Panel Replay is not supported in PR Supported Sink")

        if common.IS_PRE_SI:
            # Plane enable is taking more time in PRE_SI
            time.sleep(600)
        # Check if PR is enabled or not, after panel is plugged
        if not self.isPrEnable(port_type, self.platform):
            self.report_to_gdhm("[Powercons][DP_PR] Panel Replay is not enabled by source")
            self.fail("Panel Replay is not Enabled")

        # Driver do not support PR SFSU Feature in Gen13 Platforms. This feature will be supported in Gen14 Platforms. So SF Continuous Full Frame bit is set only for Gen13 Platforms.
        if self.PLATFORM_INFO['gfx_0']['name'] in ['ADLP', 'DG2']:
            if not self.isCffEnable(port_type, self.platform):
                self.report_to_gdhm("[Powercons][DP_PR] Continuous Full Fetch is not enabled by source")
                self.fail("Continuous Full Fetch is not Enabled")

        # Check if SRD Status is programmed correctly or not after PR is enabled
        if not self.getSRDStatusforPREnable(port_type, self.platform):
            self.report_to_gdhm(("[Powercons][DP_PR] SRD Status Verification Failed"))
            self.fail("SRD Status Verification Failed")

        # Check if Panel Replay is Configured in sink DPCD
        if not self.PanelReplayEnabledinSinkDPCD(port_type, self.platform):
            self.report_to_gdhm(("[Powercons][DP_PR] Panel Replay DPCD Verification Failed"))
            self.fail("Panel Replay is not enabled in PR Supported Sink")

        # Driver do not support PR SFSU Feature in Gen13 Platforms. This feature will be supported in Gen14 Platforms. So DPCD 1B0 Selctive Fetch bit should not be set only for Gen13 Platforms.
        if self.PLATFORM_INFO['gfx_0']['name'] in ['ADLP', 'DG2']:
            if self.SelectiveUpdateEnabledinSinkDPCD(port_type, self.platform):
                self.report_to_gdhm("[Powercons][DP_PR] Panel Replay Selective Fetch DPCD Verification Failed")
                self.fail("Selective Update is enabled in PR Supported Sink")

        # unplug mst panel
        self.mstBase.set_hpd(port_type, False)

        # Plug a panel which should not support PR
        self._port_index = 1

        # Get Topology XML file from command line for non PR capable panel
        xml_file = self.mstBase.get_xmlfile(self._port_index)

        self.mstBase.setnverifyMST(port_type, topology_type, xml_file)

        # Wait to enable panel reply
        time.sleep(15)

        # Check if Panel Replay is supported in sink DPCD
        if self.PanelReplaySupportedinDPCD(port_type, self.platform):
            self.report_to_gdhm("[Powercons][DP_PR] Panel Replay Support Verification failed in Non-PR sink", gdhm.Component.Test.DISPLAY_POWERCONS)
            self.fail("Panel Replay is supported in Non PR Sink")

        # Check if PR is enabled or not, after panel is plugged
        if self.isPrEnable(port_type, self.platform):
            self.report_to_gdhm("[Powercons][DP_PR] Panel Replay is enabled by source for Non-PR Sink")
            self.fail("Panel Replay is Enabled in Non PR Sink")

        # Check if Panel Replay is Configured in sink DPCD
        if self.PanelReplayEnabledinSinkDPCD(port_type, self.platform):
            self.report_to_gdhm(("[Powercons][DP_PR] Panel Replay DPCD Verification Failed"))
            self.fail("Panel Replay DPCD is enabled in Non PR Sink")

        logging.info("PR Basic Verification Passed")
        logging.debug("Exit: PR Basic Verification")

    ##
    # @brief API to report to GDHM taking inputs as Title and GDHM component type
    # @param[in]    message
    # @param[in]    type
    # @return       None
    def report_to_gdhm(self, message, type: gdhm.Component.Driver = gdhm.Component.Driver.DISPLAY_POWERCONS):
        gdhm.report_bug(
            title=message,
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=type,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
