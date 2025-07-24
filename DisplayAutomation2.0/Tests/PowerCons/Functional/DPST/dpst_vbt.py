########################################################################################################################
# @file         dpst_vbt.py
# @brief        Test for DPST/OPST verification by fetching DPST/OPST Params from VBT
#
# @author       Ashish Tripathi
########################################################################################################################

from Libs.Core.test_env import test_environment
from Libs.Core.vbt import vbt

from Tests.PowerCons.Functional.DPST.dpst_base import *


##
# @brief        This class contains test cases for DPST/OPST with VBT
class DpstVbt(DpstBase):
    ##
    # @brief        This class method is the entry point for DPST/OPST test cases. Helps to initialize some
    #               parameters required for DPST/OPST test execution.
    # @details      This function checks for VBT version
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DpstVbt, cls).setUpClass()

        for gfx_index, adapter in dut.adapters.items():
            gfx_vbt = vbt.Vbt(gfx_index)
            if gfx_vbt.version < 228 and cls.xpst_feature == dpst.XpstFeature.DPST:
                gdhm.report_test_bug_os("[PowerCons][DPST] DPST VBT test is running on unsupported system")
                assert False, "DPST VBT test is only supported on VBT 228 onwards"
            if gfx_vbt.version < 246 and cls.xpst_feature == dpst.XpstFeature.OPST:
                gdhm.report_test_bug_os("[PowerCons][OPST] OPST VBT test is running on unsupported system")
                assert False, "OPST VBT test is only supported on VBT 246 onwards"

    ##
    # @brief        This function verifies if DPST/OPST is working as expected with VBT settings
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_dpst_vbt_dc(self):
        if self.cmd_line_param[0]['SELECTIVE'] == 'NONE':
            skip_report_generate = False
            dpst_etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)

            for adapter in dut.adapters.values():
                gfx_vbt = vbt.Vbt(adapter.gfx_index)
                for panel in adapter.panels.values():
                    # Skip the panel if not LFP
                    if panel.is_lfp is False:
                        continue
                    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
                    logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")
                    if self.xpst_feature == dpst.XpstFeature.OPST:
                        vbt_feature_status = (gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index
                        vbt_feature_aggr_level = gfx_vbt.block_44.AgressivenessProfile2[panel_index] & 0x0f
                        logging.info(
                            f"{self.xpst_feature_str} parameters from VBT [status= {vbt_feature_status}, "
                            f"aggressiveness= {vbt_feature_aggr_level}]")

                    else:
                        vbt_feature_status = (gfx_vbt.block_44.DpstEnable[0] & (1 << panel_index)) >> panel_index
                        vbt_feature_aggr_level = gfx_vbt.block_44.AggressivenessProfile[panel_index] & 0x0f
                        logging.info(f"{self.xpst_feature_str} parameters from VBT [status= {vbt_feature_status},"
                                     f" aggressiveness= {vbt_feature_aggr_level}]")

                    dut.refresh_panel_caps(adapter)
                    feature_functionality_status = dpst.verify(adapter, panel, dpst_etl_file, skip_report_generate,
                                                               self.xpst_feature, True)
                    status = dpst.verify_default_vbt(panel, self.xpst_feature, vbt_feature_status,
                                                     vbt_feature_aggr_level, feature_functionality_status)
                    if status is False:
                        self.fail("FAIL: {0} feature verification".format(self.xpst_feature_str))
                    logging.info("PASS: {0} feature verification".format(self.xpst_feature_str))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstVbt))
    test_environment.TestEnvironment.cleanup(test_result)
