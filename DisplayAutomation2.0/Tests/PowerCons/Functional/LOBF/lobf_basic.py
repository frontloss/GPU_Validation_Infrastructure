########################################################################################################################
# @file         lobf_basic.py
# @brief        Contains basic functional tests covering below scenarios:
#               * LOBF verification in with Non-PSR2 in SD EDP and Dual eDP combinations
# @author       Bhargav Adigarla
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LOBF.lobf_base import *
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr


##
# @brief        Contains basic LOBF tests
class LobfBasic(LobfBase):
    ##
    # @brief        This function verifies LOBF with SD and Dual edp scenarios
    # @return       None
    def t_10_basic(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if lobf.is_alpm_supported(panel):
                    if lobf.verify_restrictions(adapter, panel) is False:
                        logging.error("LOBF restrictions failed in driver")
                    if lobf.is_lobf_enabled_in_driver(adapter, panel) is False:
                        logging.error("LOBF is disabled in driver")
                    logging.info("LOBF Enabled in driver")
                    if self.method == "VIDEO":
                        etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [lobf.MEDIA_FPS, 60])
                    elif self.method == "GAME":
                        etl_file, _ = workload.run(workload.GAME_PLAYBACK,
                                                   [workload.Apps.Classic3DCubeApp, 30, True])
                        # Ensure async flips
                        if vrr.async_flips_present(etl_file) is False:
                            etl_file, _ = workload.run(workload.GAME_PLAYBACK,
                                                       [workload.Apps.MovingRectangleApp, 30, True])
                            if vrr.async_flips_present(etl_file) is False:
                                self.fail("OS is NOT sending async flips")
                    else:
                        etl_file, _ = workload.run(workload.IDLE_DESKTOP, [60])
                    if lobf.verify_lobf(adapter, panel, etl_file, self.method) is False:
                        self.fail("LOBF verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LobfBasic))
    test_environment.TestEnvironment.cleanup(test_result)