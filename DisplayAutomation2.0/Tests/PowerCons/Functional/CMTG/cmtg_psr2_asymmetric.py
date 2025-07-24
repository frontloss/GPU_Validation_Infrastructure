########################################################################################################################
# @file         cmtg_psr2_asymmetric.py
# @brief        Contains basic functional tests covering below scenarios:
#               * CMTG verification in with PSR2  in SD EDP and Dual eDP combinations
# @author       Bhargav Adigarla
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.CMTG.cmtg_base import *


##
# @brief        Contains basic CMTG tests for PSR2 asymmetric(timings configuration)
class CmtgBasic(CmtgBase):
    ##
    # @brief        This function verifies CMTG with SD and Dual edp scenarios
    # @return       None
    def t_10_basic(self):
        for adapter in dut.adapters.values():
            lfp_panels = []
            ext_panels  = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    if panel.port not in ["MIPI_A", "MIPI_C"]:
                        lfp_panels.append(panel)
                else:
                    ext_panels.append(panel)

            if len(lfp_panels) == 2:
                if cmtg.verify_cmtg_slave_status(adapter, lfp_panels[0]) and cmtg.verify_cmtg_slave_status(adapter,
                                                                                                           lfp_panels[
                                                                                                               1]):
                    self.fail("both eDPs are slave to CMTG in asymmetric configuration")

                for panel in lfp_panels:
                    if panel.psr_caps.is_psr2_supported or panel.pr_caps.is_pr_supported:
                        if cmtg.verify_cmtg_slave_status(adapter, panel):
                            if self.display_config_.set_display_configuration_ex(enum.SINGLE, panel.port) is False:
                                self.fail("Applying Display config {0} Failed"
                                          .format(str(enum.SINGLE) + " " + " ".join(str(x) for x in panel.port)))
                            if cmtg.verify(adapter, [panel]) is False:
                                self.fail("CMTG instance verification failed")
                            logging.info("CMTG instance verification successful")
                            if panel.vrr_caps.is_vrr_supported:
                                if cmtg.verify_cmtg_vrr(adapter, panel, self.method) is False:
                                    self.fail("CMTG VRR sequence verification failed")
                                logging.info("CMTG VRR sequence verification successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CmtgBasic))
    test_environment.TestEnvironment.cleanup(test_result)
