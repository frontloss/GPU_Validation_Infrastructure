#################################################################################################################
# @file         drrs_mode_set.py
# @brief        Contains DRRS mode set tests
#
# @author       Rohit Kumar
#################################################################################################################

from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DRRS.drrs_base import *

##
# @brief        This class contains tests to verify DRRS after display modeset

class DrrsModeSetTest(DrrsBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        This function verifies DRRS after a modeset (skips current mode)
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_mode_set(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Get two supported modes with max RR
                mode_list = common.get_display_mode(panel.target_id, panel.max_rr, 2)

                for mode in mode_list:
                    # Skip to next mode if current and target modes are same
                    current_mode = self.display_config_.get_current_mode(panel.target_id)
                    if current_mode == mode:
                        continue

                    html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if self.display_config_.set_display_mode([mode], False) is False:
                        self.fail("\tFailed to apply display mode")
                    html.step_end()

                    dut.refresh_panel_caps(adapter)

                    self.verify_drrs()

    ##
    # @brief        This function verifies DRRS after a modeset
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_rr_switch(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Switch to min rr
                mode = common.get_display_mode(panel.target_id, panel.min_rr)

                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("\tFailed to apply display mode")
                html.step_end()

                # Switch to max rr
                mode = common.get_display_mode(panel.target_id, panel.max_rr)

                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("\tFailed to apply display mode")
                html.step_end()

                dut.refresh_panel_caps(adapter)

                self.verify_drrs()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsModeSetTest))
    test_environment.TestEnvironment.cleanup(test_result)
