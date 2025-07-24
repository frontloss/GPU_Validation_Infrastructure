########################################################################################################################
# @file         dmrrs_mode_set.py
# @brief        DMRRS_Tests
# @details      This file implements normal/ fractional DMRRS functionality check in maximum and minimum resolutions.
#               DMRRS functionality is covered both CLOCK_BASED and VRR_BASED.
#               For normal, media content namely 24fps, 25fps and 30fps videos.
#               For fractional, media content namely 23.976fps, 29.97fps and 59.94fps videos.
#
# @author       Vinod D S, Rohit Kumar
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        Contains DMRRS tests

class DmrrsModeSet(DmrrsBase):
    test_modes = {}  # {'gfx_0': {'DP_A': []}}

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any DMRRS mode set test case. Helps to initialize some of
    #               the parameters required for DMRRS mode set test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DmrrsModeSet, cls).setUpClass()

        # Prepare the test mode list
        for adapter in dut.adapters.values():
            cls.test_modes[adapter.gfx_index] = {}
            for panel in adapter.panels.values():
                modes_max_rr = common.get_display_mode(panel.target_id, refresh_rate=panel.max_rr, limit=None)
                assert modes_max_rr, "Get display modes failed (Test issue)"
                cls.test_modes[adapter.gfx_index][panel.port] = [modes_max_rr[-1], modes_max_rr[0]]

    ############################
    # Test Function
    ############################

    ##
    # @brief        This functions verifies DMRRS with mode set
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["23.976", "24", "RESOLUTION"])
    # @endcond
    def t_11_mode_set_resolution(self):
        media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
        self.verify_with_mode_set(media_fps)

    ##
    # @brief        This functions verifies DMRRS with mode set
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["25", "29.970", "RESOLUTION"])
    # @endcond
    def t_12_mode_set_resolution(self):
        media_fps = dmrrs.MediaFps.FPS_29_970 if self.is_fractional_rr else dmrrs.MediaFps.FPS_25_000
        self.verify_with_mode_set(media_fps)

    ##
    # @brief        This functions verifies DMRRS with mode set
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["30", "59.940", "RESOLUTION"])
    # @endcond
    def t_13_mode_set_resolution(self):
        media_fps = dmrrs.MediaFps.FPS_59_940 if self.is_fractional_rr else dmrrs.MediaFps.FPS_30_000
        self.verify_with_mode_set(media_fps)

    ##
    # @brief        This functions verifies DMRRS with mode set (rotation)
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["23.976", "24", "ROTATION"])
    # @endcond
    def t_14_mode_set_rotation(self):
        media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
        self.verify_with_rotation(media_fps, enum.ROTATE_180)
        self.verify_with_rotation(media_fps, enum.ROTATE_0)

    ##
    # @brief        This functions verifies DMRRS with mode set (rotation)
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["25", "29.970", "ROTATION"])
    # @endcond
    def t_15_mode_set_rotation(self):
        media_fps = dmrrs.MediaFps.FPS_29_970 if self.is_fractional_rr else dmrrs.MediaFps.FPS_25_000
        self.verify_with_rotation(media_fps, enum.ROTATE_180)
        self.verify_with_rotation(media_fps, enum.ROTATE_0)

    ##
    # @brief        This functions verifies DMRRS with mode set (rotation)
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["30", "59.940", "ROTATION"])
    # @endcond
    def t_16_mode_set_rotation(self):
        media_fps = dmrrs.MediaFps.FPS_59_940 if self.is_fractional_rr else dmrrs.MediaFps.FPS_30_000
        self.verify_with_rotation(media_fps, enum.ROTATE_180)
        self.verify_with_rotation(media_fps, enum.ROTATE_0)

    ############################
    # Helper Function
    ############################
    ##
    # @brief        This is a helper function to verify DMRRS with mode set
    # @param[in]    media_fps
    # @return       None
    def verify_with_mode_set(self, media_fps):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if len(self.test_modes[adapter.gfx_index][panel.port]) == 0:
                    self.fail("Test mode list is empty (Test issue)")

                for mode in self.test_modes[adapter.gfx_index][panel.port]:
                    html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if self.display_config_.set_display_mode([mode], False) is False:
                        self.fail("Failed to apply display mode")
                    html.step_end()

                    etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

                    self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

    ##
    # @brief        This is a helper function to verify DMRRS with rotation
    # @param[in]    media_fps
    # @param[in]    angle
    # @return       None
    def verify_with_rotation(self, media_fps, angle):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                mode = self.display_config_.get_current_mode(panel.target_id)
                mode.rotation = angle
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz {mode.rotation}")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("Failed to set display mode")
                html.step_end()

                etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsModeSet))
    test_environment.TestEnvironment.cleanup(test_result)
