########################################################################################################################
# @file         dmrrs_power_event.py
# @brief        This file implements normal/ fractional DMRRS functionality check in power events.
# @details      DMRRS functionality is covered both CLOCK_BASED and VRR_BASED.
#               For normal, media content namely 24fps, 25fps and 30fps videos.
#               For fractional, media content namely 23.976fps, 29.97fps and 59.94fps videos.
#
# @author       Vinod D S, Rohit Kumar
########################################################################################################################
import time

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Modules import workload

##
# @brief        Contains DMRRS tests before/after power events


class DmrrsPowerEvent(DmrrsBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function verifies DMRRS in CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["23.976", "24", "CS"])
    # @endcond
    def t_11_power_event_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3):
            self.fail("S3 is enabled, so cannot execute CS (Planning Issue)")
        media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.CS)

    ##
    # @brief        This function verifies DMRRS in CS power event with 29.970 media fps
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["25", "29.970", "CS"])
    # @endcond
    def t_12_power_event_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3):
            self.fail("S3 is enabled, so cannot execute CS (Planning Issue)")
        media_fps = dmrrs.MediaFps.FPS_29_970 if self.is_fractional_rr else dmrrs.MediaFps.FPS_25_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.CS)

    ##
    # @brief        This function verifies DMRRS with CS power event with 30 and 59.940 media fps
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["30", "59.940", "CS"])
    # @endcond
    def t_13_power_event_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3):
            self.fail("S3 is enabled, so cannot execute CS (Planning Issue)")
        media_fps = dmrrs.MediaFps.FPS_59_940 if self.is_fractional_rr else dmrrs.MediaFps.FPS_30_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.CS)

    ##
    # @brief        This function verifies DMRRS in CS power event with 23.976 media fps
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["23.976", "24", "S3"])
    # @endcond
    def t_14_power_event_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            self.fail("CS is enabled, so cannot execute S3 (Planning Issue)")
        media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.S3)

    ##
    # @brief        This function verifies DMRRS in S3 power event with 29.970 media fps
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["25", "29.970", "S3"])
    # @endcond
    def t_15_power_event_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            self.fail("CS is enabled, so cannot execute S3 (Planning Issue)")
        media_fps = dmrrs.MediaFps.FPS_29_970 if self.is_fractional_rr else dmrrs.MediaFps.FPS_25_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.S3)

    ##
    # @brief        This function verifies DMRRS in S3 power event with 59.940 media fps
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["30", "59.940", "S3"])
    # @endcond
    def t_16_power_event_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            self.fail("CS is enabled, so cannot execute S3 (Planning Issue)")
        media_fps = dmrrs.MediaFps.FPS_59_940 if self.is_fractional_rr else dmrrs.MediaFps.FPS_30_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.S3)

    @common.configure_test(repeat=True, selective=["23.976", "24", "S4"])
    ##
    # @brief        This function verifies DMRRS in S4 power event with 23.976 media fps
    # @return       None
    def t_17_power_event_s4(self):
        media_fps = dmrrs.MediaFps.FPS_23_976 if self.is_fractional_rr else dmrrs.MediaFps.FPS_24_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.S4)

    ##
    # @brief        This function verifies DMRRS in S4 power event with 29.970 media fps
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["25", "29.970", "S4"])
    # @endcond
    def t_18_power_event_s4(self):
        media_fps = dmrrs.MediaFps.FPS_29_970 if self.is_fractional_rr else dmrrs.MediaFps.FPS_25_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.S4)

    ##
    # @brief        This function verifies DMRRS in S4 power event with 59.940 media fps
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["30", "59.940", "S4"])
    # @endcond
    def t_19_power_event_s4(self):
        media_fps = dmrrs.MediaFps.FPS_59_940 if self.is_fractional_rr else dmrrs.MediaFps.FPS_30_000
        self.verify_with_power_event(media_fps, display_power.PowerEvent.S4)

    ############################
    # Helper Function
    ############################
    ##
    # @brief        This a helper function to check DMRRS with power events
    # @param[in]    media_fps
    # @param[in]    power_event
    # @return       None
    def verify_with_power_event(self, media_fps, power_event):

        def verify(before_after):
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    logging.info("Step: Checking DMRRS with media FPS= {0} {1} {2}".format(
                        media_fps, before_after, power_event.name))
                    etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])
                    self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

        verify('before')

        # Trigger the power event
        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail("Failed to invoke power event {0}".format(power_event.name))

        time.sleep(20)
        count = int(self.cmd_line_param[0]['COUNT'][0]) if self.cmd_line_param[0]['COUNT'] != 'NONE' else 1

        for iteration in range(0, count):
            logging.info(f"Checking DMRRS with media FPS= {media_fps} in iteration #{iteration} "
                         f"with {power_event.name}")
            verify('after')


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)
