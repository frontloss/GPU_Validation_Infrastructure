########################################################################################################################
# @file         dmrrs_basic.py
# @brief      This file implements normal/ fractional DMRRS functionality check in AC and DC mode.
#               DMRRS functionality is covered both CLOCK_BASED and VRR_BASED.
#               For normal, media content namely 24fps, 25fps and 30fps videos.
#               For fractional, media content namely 23.976fps, 29.97fps and 59.94fps videos.
#
# @author       Vinod D S, Rohit Kumar
########################################################################################################################
from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        Contains basic DMRRS tests
class DmrrsBasic(DmrrsBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function to verify DMRRS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["23.976", "24", "DC"])
    # @endcond
    def t_11_basic_dc(self):
        media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
        self.verify_basic(media_fps=media_fps, power_line_status=display_power.PowerSource.DC)

    ##
    # @brief        Test function to verify DMRRS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["23.976", "24", "AC"])
    # @endcond
    def t_12_basic_ac(self):
        media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
        self.verify_basic(media_fps=media_fps, power_line_status=display_power.PowerSource.AC)

    ##
    # @brief        Test function to verify DMRRS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["25", "29.970", "DC"])
    # @endcond
    def t_13_basic_dc(self):
        media_fps = dmrrs.MediaFps.FPS_29_970 if self.is_fractional_rr else dmrrs.MediaFps.FPS_25_000
        self.verify_basic(media_fps=media_fps, power_line_status=display_power.PowerSource.DC)

    ##
    # @brief        Test function to verify DMRRS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["25", "29.970", "AC"])
    # @endcond
    def t_14_basic_ac(self):
        media_fps = dmrrs.MediaFps.FPS_29_970 if self.is_fractional_rr else dmrrs.MediaFps.FPS_25_000
        self.verify_basic(media_fps=media_fps, power_line_status=display_power.PowerSource.AC)

    ##
    # @brief        Test function to verify DMRRS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["30", "59.940", "DC"])
    # @endcond
    def t_15_basic_dc(self):
        media_fps = dmrrs.MediaFps.FPS_59_940 if self.is_fractional_rr else dmrrs.MediaFps.FPS_30_000
        self.verify_basic(media_fps=media_fps, power_line_status=display_power.PowerSource.DC)

    ##
    # @brief        Test function to verify DMRRS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["30", "59.940", "AC"])
    # @endcond
    def t_16_basic_ac(self):
        media_fps = dmrrs.MediaFps.FPS_59_940 if self.is_fractional_rr else dmrrs.MediaFps.FPS_30_000
        self.verify_basic(media_fps=media_fps, power_line_status=display_power.PowerSource.AC)

    ############################
    # Helper Function
    ############################

    ##
    # @brief        Test function to verify DMRRS
    # @param[in]    media_fps
    # @param[in]    power_line_status
    # @return       None
    def verify_basic(self, media_fps, power_line_status):

        # Power line status switch
        if not self.display_power_.set_current_powerline_status(power_line_status):
            self.fail("Failed to switch power line status to {0} (Test Issue)".format(power_line_status.name))

        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK,
                                        [media_fps, 30, False, False, None, None, True, self.is_video_loop_expected])

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps, wm_during_rr_switch=True)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsBasic))
    test_environment.TestEnvironment.cleanup(test_result)
