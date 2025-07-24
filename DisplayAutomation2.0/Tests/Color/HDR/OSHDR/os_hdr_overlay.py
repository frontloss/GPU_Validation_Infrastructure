#######################################################################################################################
# @file         os_hdr_overlay.py
# @addtogroup   Test_Color
# @section      os_hdr_overlay
# @remarks      @ref os_hdr_overlay.py \n
#               The test script takes the HDR display info and configuration to be applied through command line.
#               Test scripts invoke Overlay application and verifies Video Plane is disabled for display and HDR enabled
#               Basic register verification (HDR Mode in Pipe_Misc register) will be performed for persistence of HDR.
#               To-Do : Add ETL Parsing for Metadata
# CommandLine:  python os_hdr_overlay.py -edp_a SINK_EDP050 -hdmi_b  SamsungJS9500_HDR.bin -config EXTENDED
#               python os_hdr_overlay.py -edp_a SINK_EDP050 -dp_d  Benq_SW320.bin  DP_HDR_DPCD.txt  -CONFIG EXTENDED
# @author       Vimalesh D
#######################################################################################################################
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color import color_verification
from Tests.Color.HDR.OSHDR import os_hdr_verification


class OSHdrTestOverlayEvent(OSHDRBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    def runTest(self):

        event_name = "Overlay_event"
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

        if color_common_utility.start_etl_capture("Overlay") is False:
            self.fail("GfxTrace failed to start")

        status, app = color_common_utility.launch_overlay()

        if status is False:
            color_common_utility.stop_etl_capture("Overlay")
            self.fail("Failed to open overlay application")
        else:
            logging.info("Finished overlay application event")

        display_overlay_etl_file = color_common_utility.stop_etl_capture("Overlay")

        ##
        # Verify HDR persistence after overlay event
        if self.os_hdr_verify.verify_hdr_persistence(event_name, self.enumerated_displays, self.platform, self.connected_list, "YES") is False:
            self.fail("Failed to verify HDR persistence after overlay event")
        ##
        # Close the overlay application
        app.terminate()

        logging.info("Closed overlay application")

        ##
        # Disable HDR
        self.enumerated_displays = self.config.get_enumerated_display_info()
        super().toggle_and_verify_hdr(toggle="DISABLE")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
