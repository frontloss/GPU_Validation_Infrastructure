########################################################################################################################
# @file         dmrrs_mouse_move.py
# @brief        This file contains Frame Buffer Compression functionality check after mouse moves.
#
# @author       Rohit Kumar
########################################################################################################################
from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Modules import workload

##
# @brief        Contains DMRRS tests after mouse moves


class DmrrsMouseMove(DmrrsBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function verifies DMRRS after single mouse move
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["SINGLE"])
    # @endcond
    def t_11_mouse_dc(self):
        self.verify_mouse_move()

    ##
    # @brief        This function verifies DMRRS after multiple mouse moves
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MULTIPLE"])
    # @endcond
    def t_12_mouse_dc(self):
        self.verify_mouse_move(120, 5)

    ############################
    # Helper Function
    ############################
    ##
    # @brief        This is a helper function to verify DMRRS after mouse moves
    # @param[in]    duration
    # @param[in]    mouse_move_count
    # @return       None
    def verify_mouse_move(self, duration=30, mouse_move_count=1):
        power_line_status = display_power.PowerSource.DC
        media_fps = dmrrs.MediaFps.FPS_24_000

        # Power line status switch
        if not self.display_power_.set_current_powerline_status(power_line_status):
            self.fail("Failed to switch power line status to {0} (Test Issue)".format(power_line_status.name))

        etl_file_path, _ = workload.run(
            workload.VIDEO_PLAYBACK_WITH_MOUSE_MOVE, [media_fps, duration, 5, mouse_move_count])

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsMouseMove))
    test_environment.TestEnvironment.cleanup(test_result)
