########################################################################################################################
# @file         cmtg_psr2_vrr.py
# @brief        Contains basic functional tests covering below scenarios:
#               * CMTG verification in with PSR2/VRR concurrency.
# @author       Bhargav Adigarla
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr
from Tests.PowerCons.Functional.CMTG.cmtg_base import *


##
# @brief        Contains basic CMTG VRR concurrency tests
class CmtgVrr(CmtgBase):

    ##
    # @brief        This function verifies CMTG with VRR panel
    # @return       None
    def t_10_basic(self):
        for adapter in dut.adapters.values():
            lfp_panels = []
            ext_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    if panel.port not in ["MIPI_A", "MIPI_C"]:
                        lfp_panels.append(panel)
                else:
                    ext_panels.append(panel)
            if len(lfp_panels) == 1:
                if lfp_panels[0].psr_caps.is_psr2_supported and lfp_panels[0].vrr_caps.is_vrr_supported:
                    if cmtg.verify(adapter, lfp_panels) is False:
                        self.fail("CMTG verification failed")
                    if cmtg.verify_cmtg_vrr(adapter, lfp_panels[0], self.method) is False:
                        self.fail("CMTG VRR sequence verification failed")
                    logging.info("CMTG VRR sequence verification successful")
                    logging.info("CMTG verification successful")
                elif not lfp_panels[0].psr_caps.is_psr2_supported and lfp_panels[0].vrr_caps.is_vrr_supported:
                    if cmtg.verify_cmtg_status(adapter):
                        self.fail("CMTG enabled in non-PSR2 panel")
                    logging.info("CMTG is not enabled in non PSR2 panel as expected")

                    etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.Classic3DCubeApp, 30, True])
                    # Ensure async flips
                    if vrr.async_flips_present(etl_file) is False:
                        etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.MovingRectangleApp, 30, True])
                        if vrr.async_flips_present(etl_file) is False:
                            logging.warning("OS is NOT sending async flips")
                            return False
                    logging.info("Step: Verifying VRR for {0}".format(lfp_panels[0].port))
                    is_os_aware_vrr = dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1
                    if vrr.verify(adapter, lfp_panels[0], etl_file, None,
                                  negative=True, os_aware_vrr=is_os_aware_vrr, expected_vrr=False) is False:
                        self.fail("VRR verification failed with non-PSR2 panel")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CmtgVrr))
    test_environment.TestEnvironment.cleanup(test_result)
