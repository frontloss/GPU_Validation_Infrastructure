########################################################################################################################
# @file         cmtg_game_video.py
# @brief        Contains Game and Video sequence test:
#               * CMTG and VRR verification with Game and then Video
# @author       Bhargav Adigarla
########################################################################################################################
import logging
from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.CMTG.cmtg_base import *


##
# @brief        Contains basic CMTG tests
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

            if len(lfp_panels) == 1:
                if lfp_panels[0].psr_caps.is_psr2_supported or lfp_panels[0].pr_caps.is_pr_supported:
                    if cmtg.verify(adapter, lfp_panels) is False:
                        self.fail("CMTG verification failed")
                    logging.info("CMTG verification successful")
                    if lfp_panels[0].vrr_caps.is_vrr_supported:
                        if cmtg.verify_cmtg_vrr(adapter, lfp_panels[0], 'GAME') is False:
                            self.fail("CMTG VRR sequence verification failed with Game workload")
                        logging.info("CMTG VRR sequence verification successful with Game workload")
                        if cmtg.verify_cmtg_vrr(adapter, lfp_panels[0], 'VIDEO') is False:
                            self.fail("CMTG VRR sequence verification with video workload")
                        logging.info("CMTG VRR sequence verification successful with video workload")
                else:
                    status = cmtg.verify_cmtg_status(adapter)
                    if adapter.name in common.PRE_GEN_15_PLATFORMS:
                        if status:
                            self.fail("CMTG enabled in non-PSR2 panel")
                        logging.info("CMTG is not enabled in non PSR2 panel as expected")
                    # GEN15+ CMTG will be enabled on non-PSR panel as well
                    else:
                        if status is False:
                            self.fail("CMTG not enabled in non-PSR2 panel")
                        logging.info("CMTG enabled in non PSR2 panel as expected")

            if len(lfp_panels) == 2:
                for panel in lfp_panels:
                    if panel.psr_caps.is_psr2_supported or panel.pr_caps.is_pr_supported:
                        if self.display_config_.set_display_configuration_ex(enum.SINGLE, panel.port) is False:
                            self.fail("Applying Display config {0} Failed"
                                      .format(str(enum.SINGLE) + " " + " ".join(str(x) for x in panel.port)))
                        if cmtg.verify_cmtg_slave_status(adapter, panel) is True:
                            if cmtg.verify(adapter, [panel]) is False:
                                self.fail("CMTG verification failed")
                            logging.info("CMTG verification successful")
                            if panel.vrr_caps.is_vrr_supported:
                                if cmtg.verify_cmtg_vrr(adapter, panel, 'GAME') is False:
                                    self.fail("CMTG VRR sequence verification failed with Game workload")
                                logging.info("CMTG VRR sequence verification successful with Game workload")
                                if cmtg.verify_cmtg_vrr(adapter, panel, 'VIDEO') is False:
                                    self.fail("CMTG VRR sequence verification with video workload")
                                logging.info("CMTG VRR sequence verification successful with video workload")
                    else:
                        status = cmtg.verify_cmtg_status(adapter)
                        if adapter.name in common.PRE_GEN_15_PLATFORMS:
                            if status:
                                self.fail("CMTG enabled in non-PSR2 panel")
                            logging.info("CMTG is not enabled in non PSR2 panel as expected")
                        # GEN15+ CMTG will be enabled on non-PSR panel as well
                        else:
                            if status is False:
                                self.fail("CMTG not enabled in non-PSR2 panel")
                            logging.info("CMTG enabled in non PSR2 panel as expected")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CmtgBasic))
    test_environment.TestEnvironment.cleanup(test_result)
