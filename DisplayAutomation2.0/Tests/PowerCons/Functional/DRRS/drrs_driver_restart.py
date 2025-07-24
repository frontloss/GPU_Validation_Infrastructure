#################################################################################################################
# @file         drrs_driver_restart.py
# @brief        Contains DRRS driver restart tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import display_essential
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DRRS.drrs_base import *

##
# @brief        This class contains tests to verify DRRS before and after driver restart


class DrrsDriverRestartTest(DrrsBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        This function verifies DRRS before and after driver restart
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_driver_restart(self):
        self.verify_drrs()
        for adapter in dut.adapters.values():
            html.step_start(f"Restart display driver for {adapter.name}")
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                self.fail(f"Failed to restart display driver")
            logging.info("\tPASS: Restarted display driver successfully")
            html.step_end()

            dut.refresh_panel_caps(adapter)

        self.verify_drrs()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsDriverRestartTest))
    test_environment.TestEnvironment.cleanup(test_result)
