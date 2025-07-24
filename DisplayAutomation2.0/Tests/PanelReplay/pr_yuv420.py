#################################################################################################################
# @file         pr_yuv420.py
# @brief        implements panel replay functionality basic test with YUV420 panel.
# @details      CommandLine: python -DP_B <SINK_<sinkname>> <NONPR_<nonPRsinkname>>
# @author       sharathm
#################################################################################################################
import logging
import time
import unittest

import Libs.Core.display_utility as disp_util
from Libs.Core import reboot_helper
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PanelReplay import pr_base_sst
from Tests.PanelReplay.pr_base import PrBase, get_io_bw_using_socwatch
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister


##
# @brief This class contains functions that helps in validating PR enable and other basic check.
class PrBasicYUV420(pr_base_sst.PrBaseSST):
    ##
    # @brief    executes the actual test steps for Panel Replay Basic SST scenario.
    # @return   None
    def runTest(self):
        pr_base = PrBase()
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
                # Plug Display
                if disp_util.plug(port=display_port, panelindex=panel_index,
                                  dp_dpcd_model_data=None):
                    enum_display_dict = self.get_display_names()
                    logging.info(
                        f"STEP {step_count} : Verifying Display Detection --> Display {display_port} "
                        f"(Target ID : {enum_display_dict[display_port]}) Plug Successful")
                else:
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] Plug of PR capable panel failed")
                    self.fail(f"STEP {step_count} : Verifying Display Detection -->Display {display_port} Plug Failed")

                step_count += 1
                time.sleep(10)
                if self.apply_420_mode(display_port) is False:
                    self.fail(f"YUV420 Mode set failed")
                pipe_suffix = pr_base.getPipeSuffix(display_port)
                if pipe_suffix is not None:
                    self.verify_yuv420(pipe=pipe_suffix)
                else:
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] Incorrect Pipe Suffix")
                    self.fail("Pipe suffix is None")

                # Check if Panel Replay is supported in sink DPCD
                if not pr_base.PanelReplaySupportedinDPCD(display_port, self.platform):
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] Panel Replay support failed in PR Capable Sink")
                    self.fail("Panel Replay is not supported in PR Supported Sink")

                if common.IS_PRE_SI:
                    # Plane enable is taking more time in PRE_SI
                    time.sleep(600)
                # Check if PR is enabled or not, after panel is plugged
                if not pr_base.isPrEnable(display_port, self.platform):
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] Panel Replay is not enabled by source")
                    self.fail("Panel Replay is not Enabled")

                # Driver do not support PR SFSU Feature in Gen13 Platforms.
                # This feature will be supported in Gen14 Platforms.
                # So SF Continuous Full Frame bit is set only for Gen13 Platforms.
                if PrBase.PLATFORM_INFO['gfx_0']['name'] in ['ADLP', 'DG2']:
                    if not pr_base.isCffEnable(display_port, self.platform):
                        gdhm.report_driver_bug_pc("[Powercons][DP_PR] Continuous Full Fetch is not enabled by source")
                        self.fail("Continuous Full Fetch is not Enabled")

                # Check if SRD Status is programmed correctly or not after PR is enabled
                if not pr_base.getSRDStatusforPREnable(display_port, self.platform):
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] SRD Status Verification Failed")
                    self.fail("SRD Status Verification Failed")

                # Check if Panel Replay is Configured in sink DPCD
                if not pr_base.PanelReplayEnabledinSinkDPCD(display_port, self.platform):
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] Panel Replay DPCD Verification Failed")
                    self.fail("Panel Replay is not enabled in PR Supported Sink")

                # Driver do not support PR SFSU Feature in Gen13 Platforms.
                # This feature will be supported in Gen14 Platforms.
                # So DPCD 0x1B0h Selctive Fetch bit should not be set only for Gen13 Platforms.
                if PrBase.PLATFORM_INFO['gfx_0']['name'] in ['ADLP', 'DG2']:
                    if pr_base.SelectiveUpdateEnabledinSinkDPCD(display_port, self.platform):
                        gdhm.report_driver_bug_pc("[Powercons][DP_PR] Panel Replay Selective Fetch DPCD Verification Failed")
                        self.fail("Selective Update is enabled in PR Supported Sink")

                time.sleep(1)

                _, io_request_pr = get_io_bw_using_socwatch(duration=120)
                non_pr_panel_index = self.get_non_pr_panel_index(display_port)
                # UnPlug Display
                if disp_util.unplug(port=display_port):
                    logging.info(
                        f"STEP {step_count} : Verifying Display Detection --> Display {display_port} Unplug Successful")
                else:
                    gdhm.report_test_bug_pc("[Powercons][DP_PR] Unplug of PR capable panel failed")
                    self.fail(f"STEP {step_count} : Verifying Display Detection --> {display_port} Unplug Failed")

                logging.info("non_pr_panel_index: {}".format(non_pr_panel_index))
                if non_pr_panel_index is not None:
                    # plug a non-pr Panel
                    if disp_util.plug(port=display_port, panelindex=non_pr_panel_index,
                                      dp_dpcd_model_data=None):
                        enum_display_dict = self.get_display_names()
                        logging.info(
                            f"STEP {step_count} : Verifying Display Detection --> Display {display_port} "
                            f"(Target ID : {enum_display_dict[display_port]}) Plug Successful")
                    else:
                        gdhm.report_test_bug_pc("[Powercons][DP] Plug failed")
                        self.fail(f"STEP {step_count} : Verifying Display Detection --> {display_port} Plug Failed")
                    step_count += 1

                else:
                    gdhm.report_test_bug_pc("[Powercons][DP_PR] Non Pr panel index cannot be empty")
                    self.fail("Non Pr panel index can not be empty")
                # verify 420 mode if the panels supports YUV420 mode
                if self.apply_420_mode(display_port):
                    self.verify_yuv420(pipe_suffix)
                _, io_request = get_io_bw_using_socwatch(duration=120)

                # Check if Panel Replay is supported in sink DPCD
                if pr_base.PanelReplaySupportedinDPCD(display_port, self.platform):
                    gdhm.report_test_bug_pc("[Powercons][DP_PR] PanelReplay Support Verification failed in Non-PR sink")
                    self.fail("Panel Replay is supported in Non PR Sink")

                # Check if PR is enabled or not, after panel is plugged
                if pr_base.isPrEnable(display_port, self.platform):
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] Panel Replay is enabled by source for Non-PR Sink")
                    self.fail("Panel Replay is Enabled in Non PR Sink")

                # Check if Panel Replay is Configured in sink DPCD
                if pr_base.PanelReplayEnabledinSinkDPCD(display_port, self.platform):
                    gdhm.report_driver_bug_pc("[Powercons][DP_PR] Panel Replay DPCD Verification Failed")
                    self.fail("Panel Replay DPCD is enabled in Non PR Sink")

        if ret_value and (io_request <= io_request_pr):
            gdhm.report_driver_bug_pc("[Powercons][DP_PR] Memory IO request should be less for PR capable system")
            self.fail("Memory IO request for PR capable system is more then a non-PR system")
        logging.info("PR YUV420 SST verification Passed")
        logging.debug("Exit: PR Basic YUV420 Verification")

    ##
    # @brief        Verify YUV420 in transcoder
    # @param[in]    pipe
    # @return       None
    def verify_yuv420(self, pipe):
        pipe_misc_name = "PIPE_MISC_" + pipe
        pipe_misc_reg = MMIORegister.read("PIPE_MISC_REGISTER", pipe_misc_name, self.platform)
        ##
        # Verifying if YUV420 Mode in PipeMisc Register is enabled
        if pipe_misc_reg.yuv420_enable:
            logging.info("PASS : YUV420 Mode : Expected - ENABLED; Actual - ENABLED")
        else:
            gdhm.report_driver_bug_pc("[Powercons][DP_PR] YUV420 Verification Failed")
            self.fail("FAIL : YUV420 Mode : Expected - ENABLED; Actual - DISABLED")

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
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PrBasicYUV420'))
    TestEnvironment.cleanup(outcome)
