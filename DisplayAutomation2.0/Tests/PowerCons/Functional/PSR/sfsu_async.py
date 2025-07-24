#######################################################################################################################
# @file             sfsu_async.py
# @brief            Tests for verifying SFSU with async flips
#
# @author           Chandrakanth Reddy
#######################################################################################################################

from Libs.Core.logger import html, gdhm
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.PSR.psr_base import *
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr


##
# @brief        This class contains tests for verifying Selective Fetch and Selective Update with Async flips
class Async(PsrBase):

    ##
    # @brief        This function verifies SFSU with async flips
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_verify_async(self):
        if self.feature < psr.UserRequestedFeature.PSR_2:
            self.fail("Invalid feature name passed in cmd-line. Expected = PSR2/PR Actual = {}".format(self.feature_str))
        for adapter in dut.adapters.values():
            feature, feature_str = self.get_feature(adapter)
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr2_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                status = psr.is_psr_enabled_in_driver(adapter, panel, feature)
                if feature == psr.UserRequestedFeature.PSR2_SFSU and status is False:
                    self.fail("\tSelective Fetch is disabled for {}".format(panel))
                if feature == psr.UserRequestedFeature.PSR2_FFSU and status is False:
                    self.fail("\tPSR2 Manual tracking is disabled for {}".format(panel))
                # Play the GAME
                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                etl_file, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                )
                if etl_file is None:
                    self.fail("\tFailed to get ETL file during workload")
                if vrr.async_flips_present(etl_file) is False:
                    gdhm.report_test_bug_os("[OsFeatures][VRR] OS is NOT sending async flips")
                    html.step_end()
                    self.fail("OS is NOT sending async flips")
                time.sleep(2)

                dpst_enable = is_dpst_possible(panel, self.power_source) if panel.is_lfp else False
                if panel.pr_caps.is_pr_supported and self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    if pr.verify(adapter, panel) is False:
                        self.fail("PR verification is Failed")
                if sfsu.verify_sfsu(adapter, panel, etl_file, 'ASYNC', feature, dpst_enable, True) is False:
                    self.fail(f"FAIL : {feature_str} verification with Async flips on {panel.pipe}")
                logging.info(f"PASS: {feature_str} verification with Async flips on {panel.pipe}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(Async))
    test_environment.TestEnvironment.cleanup(test_result)
