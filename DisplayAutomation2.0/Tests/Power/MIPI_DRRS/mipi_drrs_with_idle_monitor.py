######################################################################################
# @file             mipi_drrs_with_idle_monitor.py
# @addtogroup       Test_Power_DRRS
# @brief            This file contains test to verify the basic scenario of entering DRRS state for idle monitor
# @details          CommandLine:python drrs_with_idle_monitor.py -mipi_a
#                   Test will pass only if DRRS status bits are set, after idle display scenario. else fails.
# @note             Do not modify this test without consent from the author.
# @author           Kruti Vadhavaniya
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Power.MIPI_DRRS.mipi_drrs_base import *


##
# @brief        This class contains tests to verify Mipi DRRS with idle monitor
class DrrsWithIdleMonitor(MipiDrrsBase):

    ##
    # @brief        This function verifies Mipi DRRS before video playback with idle monitor
    # @return       None
    def runTest(self):
        logging.info("Verifying the seamless DRRS condition in case of Idle monitor")
        drrs_check = 1

        for display_port in self.current_connected_displays_list:
            system_refresh_rate = self.calculate_refresh_rate_from_vbt(display_port)
            logging.info(
                "System refresh rate before idle desktop for port: {0}- {1}".format(display_port, system_refresh_rate))

        self.do_idle_desktop()

        for display_port in self.current_connected_displays_list:
            expected_refresh_rate = self.gfx_vbt.block_42.SeamlessDrrsMinRR[self.panel_index]

            drrs_check &= self.check_drrs_status(display_port, expected_rr=expected_refresh_rate)

        if drrs_check == 1:
            logging.info("PASS:DRRS with idle monitor")
        else:
            logging.error("FAIL: DRRS with idle monitor")
            self.fail_count += 1


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
