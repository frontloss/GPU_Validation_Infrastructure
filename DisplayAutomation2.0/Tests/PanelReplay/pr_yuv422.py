#################################################################################################################
# @file         pr_yuv422.py
# @brief        implements panel replay functionality basic test with YUV422 panel. It checks if panel replay gets enabled or not
# @details      CommandLine: python -DP_B <SINK_<sinkname>> <NONPR_<nonPRsinkname>>
# @author       sharathm
#################################################################################################################
import logging
import time
import unittest

from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PanelReplay.pr_base import PrBase
from Libs.Core import reboot_helper
from Libs.Feature.display_psr import DisplayPsr
import Tests.PanelReplay.pr_base_sst as pr_yuv422_base
import Libs.Core.display_utility as disp_util
from Libs.Core import registry_access
from registers.mmioregister import MMIORegister
from Tests.PowerCons.Modules import common


##
# @brief This class contains functions that helps in validating PR enable and other basic check.
class PrBasicYUV422(pr_yuv422_base.PrBaseSST):
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
        ret_value = 0
        logging.info("Input Display list: {}".format(self.input_display_list))
        for display_port in self.input_display_list:
            step_count = 1

            if display_port not in self.get_display_names().keys():
                logging.info(
                    "STEP {} : Plugging Display on ".format(step_count, display_port))
                step_count += 1

                panel_index = self.get_panel_index(display_port)
                logging.info("panel_index: {}".format(panel_index))
                #Enable YUV422 through registry before plugging
                self.set_and_verify_yuv422_registry(enable_status=1)
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

                pipe_suffix = pr_base.getPipeSuffix(display_port)
                if pipe_suffix is not None:
                    self.verify_yuv422(pipeId=pipe_suffix)
                else:
                    result=False
                    gdhm.report_bug(
                        title="[Powercons][DP_PR] Incorrect Pipe Suffix",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_POWERCONS,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Pipe suffix is None")

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
                logging.info("ret_value_pr: {} and io_bandwidth_pr in MB: {}".format(ret_value_pr, io_request_pr))

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
                    # Enable YUV422 through registry before plugging
                    self.set_and_verify_yuv422_registry(enable_status=1)
                    # plug a non-pr Panel
                    if disp_util.plug(port=display_port, panelindex=non_pr_panel_index,
                                      dp_dpcd_model_data=None):
                        enum_display_dict = self.get_display_names()
                        logging.info(
                            "STEP {} : Verifying Display Detection --> Display {} (Target ID : {}) Plug Successful".
                                format(step_count, display_port, enum_display_dict[display_port]))

                        self.verify_yuv422(pipeId=pipe_suffix)

                        ret_value, io_request = display_psr.get_io_bandwidth_using_socwatch(duration)
                        logging.info(
                            "ret_value: {} and io_bandwidth in MB: {}".format(ret_value, io_request))
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

        if ret_value and (io_request <= io_request_pr):
            gdhm.report_bug(
                title="[Powercons][DP_PR] Memory IO request should be less for PR capable system",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Memory IO request for PR capable system is more then a non-PR system")

        if result is False:
            gdhm.report_bug(
                title="[Powercons][DP_PR] PR YUV422 Verification Failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("PR YUV422 SST verification failed")
        logging.info("PR YUV422 SST verification Passed")
        logging.debug("Exit: PR Basic YUV422 Verification")

    ##
    # @brief        Set and Verify YUV422 using Regkey
    # @param[in]    enable_status
    # @return       None
    def set_and_verify_yuv422_registry(self, enable_status):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        ##
        # Add the ForceApplyYUV422Mode through registry write
        if not registry_access.write(args=reg_args, reg_name="ForceApplyYUV422Mode",
                                     reg_type=registry_access.RegDataType.DWORD, reg_value=enable_status):
            logging.error("Failed to set the registry key to apply YUV422 mode")
            gdhm.report_bug(
                title="[Powercons][DP_PR] Registry Set Failed for YUV422",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Failed to set the registry key to apply YUV422 mode")

        ##
        # Verify if the registry key has been successfully added
        reg_value, reg_type = registry_access.read(args=reg_args, reg_name="ForceApplyYUV422Mode")
        if enable_status == reg_value:
            logging.info("Successfully set ForceApplyYUV422Mode registry key")
        else:
            gdhm.report_bug(
                title="[Powercons][DP_PR] Registry Set Failed for YUV422",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Failed to apply ForceApplyYUV422Mode")

    ##
    # @brief        Verify YUV422 in transcoder
    # @param[in]    pipeId
    # @return       None
    def verify_yuv422(self, pipeId):
        pipe_misc2_name = "PIPE_MISC2_" + pipeId
        pipe_misc2_reg = MMIORegister.read("PIPE_MISC2_REGISTER", pipe_misc2_name, self.platform)
        ##
        # Verifying if YUV422 Mode in PipeMisc2 Register is enabled
        if pipe_misc2_reg.yuv_422_mode:
            logging.info("PASS : YUV422 Mode : Expected - ENABLED; Actual - ENABLED")
        else:
            gdhm.report_bug(
                title="[Powercons][DP_PR] YUV422 Verification Failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("FAIL : YUV422 Mode : Expected - ENABLED; Actual - DISABLED")
        ##
        # Do not expect YUV420 Enable when YUV422 is enabled
        pipe_misc_name = "PIPE_MISC_" + pipeId
        pipe_misc_reg = MMIORegister.read("PIPE_MISC_REGISTER", pipe_misc_name, self.platform)

        if not pipe_misc_reg.yuv420_enable:
            logging.info("PASS : YUV420 Mode : Expected - DISABLED; Actual - DISABLED")
        else:
            gdhm.report_bug(
                title="[Powercons][DP_PR] YUV420 Verification Failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("FAIL : YUV420 Mode : Expected - DISABLED; Actual - ENABLED")

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
                self.set_and_verify_yuv422_registry(enable_status=0)
                disp_util.unplug(port=display_port)

        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PrBasicYUV422'))
    TestEnvironment.cleanup(outcome)
