#######################################################################################################################
# @file         port_sync_with_vrr.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test to check whether VRR is disabled when CMTG enabled
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with VRR
class PortSyncWithVrr(PortSyncBase):

    ##
    # @brief        this function verifies port sync
    # @return       None
    def t_10_test_basic(self):
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels) is True:
                logging.info("\tPort sync programming verification successful")

                if len(self.lfp_panels) == 2:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                    if port_sync.verify_vbis(self.lfp_panels, etl_file) is False:
                        self.fail("\tPort sync VBI timing verification Failed")

                    logging.info("\tPort sync functional verification successful")
            else:
                self.fail("\tPort sync verification failed")

    ##
    # @brief        this function verifies VRR in negative scenario
    # @return       None
    def t_11_vrr_negative(self):
        for adapter in dut.adapters.values():
            etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.Classic3DCubeApp, 30, True])
            # Ensure async flips
            if vrr.async_flips_present(etl_file) is False:
                etl_file, _ = workload.run(workload.GAME_PLAYBACK, [workload.Apps.MovingRectangleApp, 30, True])
                if vrr.async_flips_present(etl_file) is False:
                    logging.warning("OS is NOT sending async flips")
                    return False
            for panel in self.lfp_panels:
                logging.info("Step: Verifying VRR for {0}".format(panel.port))
                is_os_aware_vrr = dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1
                if vrr.verify(adapter, panel, etl_file, None,
                                  negative=True, os_aware_vrr=is_os_aware_vrr, expected_vrr=False) is False:
                    self.fail("VRR is working with port sync enabled")

        logging.info("\tPASS: Negative VRR verification passed successfully with port sync")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PortSyncWithVrr))
    test_environment.TestEnvironment.cleanup(test_result)