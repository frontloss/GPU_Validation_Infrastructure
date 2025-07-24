#######################################################################################################################
# @file         os_hdr_videoplayback.py
# @addtogroup   Test_Color
# @section      os_hdr_videoplayback
# @remarks      @ref os_hdr_videoplayback.py \n
#               The test script takes the HDR display info and configuration to be applied through command line.
#               And Verifies the HDR video playback.
#               Basic register verification (HDR Mode in Pipe_Misc register) will be performed.
#               To-Do : Add ETL Parsing for Metadata
# CommandLine:  python os_hdr_videoplayback.py -edp_a SINK_EDP050 -hdmi_b  SamsungJS9500_HDR.bin -config EXTENDED
#               python os_hdr_videoplayback.py -edp_a SINK_EDP050 -dp_d Benq_SW320.bin  DP_HDR_DPCD.txt -CONFIG
#               EXTENDED
# @author       Vimalesh D
#######################################################################################################################
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color.HDR.OSHDR import os_hdr_verification


class OSHdrTestVideoPlayback(OSHDRBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    def runTest(self):

        ##
        # Check Power Mode  for DC or AC to check the HDR Option temporarily disabled
        result, status = color_common_utility.check_and_apply_power_mode()
        if status:
            logging.info(result)
        else:
            self.fail(result)

        ##
        # Enable OS_HDR on all active displays
        self.enumerated_displays = self.config.get_enumerated_display_info()

        super().toggle_and_verify_hdr(toggle="ENABLE")

        time.sleep(5)

        ##
        # Apply 4K Modeset with refresh rate 60 hz.But based on supported modes it will apply,So ignoring this.
        super().apply_native_mode()

        if color_common_utility.start_etl_capture("Video_playback") is False:
            self.fail("GfxTrace failed to start")
        else:
            logging.info("Started video playback etl")
            if color_common_utility.video_play_back(is_full_screen=True) is False:
                color_common_utility.stop_etl_capture("Video_playback")
                self.fail("Failed to launch media application")
            logging.info("Ended video playback  etl")

            display_video_playback_etl_file = color_common_utility.stop_etl_capture("Video_playback")

        ##
        # Disable HDR
        self.enumerated_displays = self.config.get_enumerated_display_info()
        super().toggle_and_verify_hdr(toggle="DISABLE")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
