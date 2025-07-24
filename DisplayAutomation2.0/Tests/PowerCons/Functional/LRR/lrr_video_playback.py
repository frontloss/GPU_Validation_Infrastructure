#################################################################################################################
# @file         lrr_video_playback.py
# @brief        Contains LRR video playback tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import display_power, enum
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains LRR video playback  tests
class LrrVideoPlaybackTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        This function verifies LRR with Video Play/Pause action
    # @details      In case of pause action during video-playback, VBI is not getting disabled. There is no OS
    #               policy stating that VBI should be disabled. Skipping the DRRS verification as of now.
    #               Next step will be decided based on MSFT's confirmation.
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PLAY_PAUSE"])
    # @endcond
    def t_11_power_source(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, True],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, Method.VIDEO, self.rr_switching_method, True, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR verification during video playback Play/Pause action")
        logging.info("PASS: LRR verification during video playback Play/Pause action")

    ##
    # @brief        This function verifies LRR with sleep(CS) during video playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_14_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("Power Event (CS) test scheduled on Non-CS system. Needed CS enabled system")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, True, True, display_power.PowerEvent.CS],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, lrr.Method.VIDEO, self.rr_switching_method, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR verification with Power Event (CS) during video playback")
        logging.info("PASS: LRR verification with Power Event (CS) during video playback")

    ##
    # @brief        This function verifies LRR with sleep(S3) during video playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_15_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("Power Event (S3) test scheduled on CS enabled system. Needed Non-CS system")

        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False, True, display_power.PowerEvent.S3],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, lrr.Method.VIDEO, self.rr_switching_method, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR verification with Power Event (S3) during video playback")
        logging.info("PASS: LRR verification with Power Event (S3) during video playback")

    ##
    # @brief        This function verifies LRR with hibernate during video playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_16_s4(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False, True, display_power.PowerEvent.S4],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, lrr.Method.VIDEO, self.rr_switching_method, video=self.video_file)

        if status is False:
            self.fail("FAIL: LRR verification with Power Event (S4) during video playback")
        logging.info("PASS: LRR verification with Power Event (S4) during video playback")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrVideoPlaybackTest))
    test_environment.TestEnvironment.cleanup(test_result)
