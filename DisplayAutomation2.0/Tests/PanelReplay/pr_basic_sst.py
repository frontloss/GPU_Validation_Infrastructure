#################################################################################################################
# @file         pr_basic_sst.py
# @brief        implements panel replay functionality basic test. It checks if panel replay gets enabled or not
# @details      CommandLine: python -DP_B <SINK_<sinkname>> <NONPR_<nonPRsinkname>>
# @author       ashishk2
#################################################################################################################
import logging
import time
import unittest
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PanelReplay.pr_base import PrBase
from Libs.Core import reboot_helper
from Libs.Feature.display_psr import DisplayPsr
import Tests.PanelReplay.pr_base_sst as pr_sst_base
import Libs.Core.display_utility as disp_util
from Tests.PowerCons.Modules import common

##
# @brief This class contains functions that helps in validating PR enable and other basic check.
class PrBasicSST(pr_sst_base.PrBaseSST):
    ##
    # @brief    executes the actual test steps for Panel Replay Basic SST scenario.
    # @return   None
    def runTest(self):

        display_psr = DisplayPsr()
        display_psr.socwatch_check = True
        pr_base = PrBase()
        result = True
        io_request_pr = 0
        io_request = 0
        logging.info("Input Display list: {}".format(self.input_display_list))
        for display_port in self.input_display_list:
            step_count = 1

            if display_port not in self.get_display_names().keys():
                logging.info(
                    "STEP {} : Plugging Display on ".format(step_count, display_port))
                step_count += 1

                panel_index = self.get_panel_index(display_port)
                logging.info("panel_index: {}".format(panel_index))
                # Plug Display
                if disp_util.plug(port=display_port, panelindex=panel_index,
                                               dp_dpcd_model_data=None):
                    enum_display_dict = self.get_display_names()
                    logging.info(
                        "STEP {} : Verifying Display Detection --> Display {} (Target ID : {}) Plug Successful".
                        format(step_count, display_port, enum_display_dict[display_port]))
                else:
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Plug of PR capable panel failed",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("STEP {} : Verifying Display Detection -->Display {} Plug Failed".format(step_count, display_port))
                step_count += 1

                # Check if Panel Replay is supported in sink DPCD
                if not pr_base.PanelReplaySupportedinDPCD(display_port, self.platform):
                    result = False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Panel Replay support failed in PR Capable Sink",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Panel Replay is not supported in PR Supported Sink")

                if common.IS_PRE_SI:
                    # Plane enable is taking more time in PRE_SI
                    time.sleep(600)
                # Check if PR is enabled or not, after panel is plugged
                if not pr_base.isPrEnable(display_port, self.platform):
                    result = False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Panel Replay is not enabled by source",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Panel Replay is not Enabled")

                # Driver do not support PR SFSU Feature in Gen13 Platforms. This feature will be supported in Gen14 Platforms. So SF Continuous Full Frame bit is set only for Gen13 Platforms.
                if PrBase.PLATFORM_INFO['gfx_0']['name'] in ['ADLP', 'DG2']:
                    if not pr_base.isCffEnable(display_port, self.platform):
                        result = False
                        gdhm.report_bug(
                            title="[Powercons][DP_PR] Continuous Full Fetch is not enabled by source",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Continuous Full Fetch is not Enabled")

                # Check if SRD Status is programmed correctly or not after PR is enabled
                if not pr_base.getSRDStatusforPREnable(display_port, self.platform):
                    result = False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] SRD Status Verification Failed",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("SRD Status Verification Failed")

                # Check if Panel Replay is Configured in sink DPCD
                if not pr_base.PanelReplayEnabledinSinkDPCD(display_port, self.platform):
                    result = False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Panel Replay DPCD Verification Failed",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Panel Replay is not enabled in PR Supported Sink")

                # Driver do not support PR SFSU Feature in Gen13 Platforms. This feature will be supported in Gen14 Platforms. So DPCD 1B0 Selctive Fetch bit should not be set only for Gen13 Platforms.
                if PrBase.PLATFORM_INFO['gfx_0']['name'] in ['ADLP', 'DG2']:
                    if pr_base.SelectiveUpdateEnabledinSinkDPCD(display_port, self.platform):
                        result = False
                        gdhm.report_bug(
                            title="[Powercons][DP_PR] Panel Replay Selective Fetch DPCD Verification Failed",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Selective Update is enabled in PR Supported Sink")

                duration = 120
                time.sleep(1)
                ret_value_pr, io_request_pr = display_psr.get_io_bandwidth_using_socwatch(duration)
                logging.info("ret_value_pr: {} and io_bandwidth in MB for PR panel: {}".format(ret_value_pr, io_request_pr))

                non_pr_panel_index = self.get_non_pr_panel_index(display_port)

                # UnPlug Display
                if disp_util.unplug(port=display_port):
                    logging.info(
                        "STEP {} : Verifying Display Detection --> Display {} Unplug Successful".format(
                            step_count, display_port))
                else:
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Unplug of PR capable panel failed",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("STEP {} : Verifying Display Detection --> Display {} Unplug Failed".format(step_count, display_port))

                logging.info("non_pr_panel_index: {}".format(non_pr_panel_index))
                if non_pr_panel_index is not None:
                    # plug a non-pr Panel
                    if disp_util.plug(port=display_port, panelindex=non_pr_panel_index,
                                                  dp_dpcd_model_data=None):
                        enum_display_dict = self.get_display_names()
                        logging.info(
                            "STEP {} : Verifying Display Detection --> Display {} (Target ID : {}) Plug Successful".
                                format(step_count, display_port, enum_display_dict[display_port]))
                        ret_value, io_request = display_psr.get_io_bandwidth_using_socwatch(duration)
                        logging.info(
                            "ret_value: {} and io_bandwidth in MB for non PR panel: {}".format(ret_value, io_request))
                    else:
                        gdhm.report_bug(
                            title="[Powercons][DP_PR] Plug failed",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Test.DISPLAY_POWERCONS,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("STEP {} : Verifying Display Detection -->Display {} Plug Failed".format(step_count, display_port))
                    step_count += 1
                else:
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Non Pr panel index can not be empty",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Non Pr panel index can not be empty")

                # Check if Panel Replay is supported in sink DPCD
                if pr_base.PanelReplaySupportedinDPCD(display_port, self.platform):
                    result = False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Panel Replay Support Verification failed in Non-PR sink",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Panel Replay is supported in Non PR Sink")

                # Check if PR is enabled or not, after panel is plugged
                if pr_base.isPrEnable(display_port, self.platform):
                    result = False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Panel Replay is enabled by source for Non-PR Sink",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Panel Replay is Enabled in Non PR Sink")

                # Check if Panel Replay is Configured in sink DPCD
                if pr_base.PanelReplayEnabledinSinkDPCD(display_port, self.platform):
                    result = False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Panel Replay DPCD Verification Failed",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Panel Replay DPCD is enabled in Non PR Sink")

        # IO Bandwidth usage for a PR and non-PR capable panel is printed but no Power based verification
        # is implemented here

        if result is False:
            gdhm.report_bug(
                title="[Powercons][DP_PR] PR Verification Failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("PR SST verification failed")
        logging.info("PR Basic Verification Passed")
        logging.debug("Exit: PR Basic Verification")


    ##
    # @brief    Teardown function that cleanups by unplugging EFP displays
    # @return   None
    def tearDown(self):
        logging.debug("ENTRY: TearDown")

        # Unplug all EFP displays
        logging.debug("Unplugging all Displays")
        enum_display_dict = self.get_display_names()

        for display_port in enum_display_dict.keys():
            if disp_util.get_vbt_panel_type(display_port, 'gfx_0') not in \
                    [disp_util.VbtPanelType.LFP_DP, disp_util.VbtPanelType.LFP_MIPI]:
                disp_util.unplug(port=display_port)

        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PrBasicSST'))
    TestEnvironment.cleanup(outcome)
