#################################################################################################################
# @file         drrs_display_switching.py
# @brief        Contains DRRS display switching tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DRRS.drrs_base import *

##
# @brief        This class contains tests to verify DRRS after display switching


class DrrsDisplaySwitchingTest(DrrsBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        This is a helper function used to set different display configurations for the tests
    def _verification_steps(self):
        status = True
        for adapter in dut.adapters.values():
            display_list = []
            lfp_ports = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    display_list.append(panel.display_info.DisplayAndAdapterInfo)
                    lfp_ports.append(panel.port)

            if adapter.lfp_count == 1:
                html.step_start(f"Setting display configuration: SINGLE {lfp_ports}")
                if self.display_config_.set_display_configuration_ex(enum.SINGLE, display_list) is False:
                    self.fail("Failed to apply display configuration")
            else:
                html.step_start(f"Setting display configuration: EXTENDED {lfp_ports}")
                if self.display_config_.set_display_configuration_ex(enum.EXTENDED, display_list) is False:
                    self.fail("Failed to apply display configuration")
            html.step_end()

            dut.refresh_panel_caps(adapter)

            self.verify_drrs()

        return status

    ##
    # @brief        This function verifies DRRS after switching from CLONE/EXTENDED to SINGLE mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_single_idle(self):
        # From Clone/Extended to Single
        if self._verification_steps() is False:
            self.fail("DRRS verification failed after switching from CLONE/EXTENDED to SINGLE")

    ##
    # @brief        This function verifies DRRS after switching from SINGLE external to SINGLE eDP
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_external_to_edp(self):
        # From Single external to Single eDP
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    continue
                html.step_start("Setting display configuration: SINGLE {0}".format(panel.port))
                if self.display_config_.set_display_configuration_ex(
                        enum.SINGLE, [panel.display_info.DisplayAndAdapterInfo]) is False:
                    self.fail("Failed to apply display configuration")
                html.step_end()
                break

        if self._verification_steps() is False:
            self.fail("DRRS verification failed after switching from SINGLE external to SINGLE eDP")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsDisplaySwitchingTest))
    test_environment.TestEnvironment.cleanup(test_result)
