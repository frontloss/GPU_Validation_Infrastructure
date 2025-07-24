#######################################################################################################################
# @file         os_hdr_miscellaneous.py
# @addtogroup   Test_Color
# @section      os_hdr_miscellaneous
# @remarks      @ref os_hdr_miscellaneous.py \n
#               Basic register verification (HDR Mode in Pipe_Misc register) will be performed after driver restart
#               to check the persistence of HDR in each displays
#               Monitor Turn Off-On events for edp alone to check the persistence of HDR
#               To-Do : Add ETL Parsing for Metadata
# CommandLine:  python os_hdr_miscellaneous.py -edp_a SINK_EDP050 -hdmi_b  SamsungJS9500_HDR.bin -config EXTENDED
#               python os_hdr_miscellaneous.py -edp_a SINK_EDP050 -dp_d Benq_SW320.bin  DP_HDR_DPCD.txt  -CONFIG
#               EXTENDED
# @author       Vimalesh D
#######################################################################################################################
import time

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color.HDR.OSHDR import os_hdr_verification


class OSHDRMiscellaneous(OSHDRBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    def runTest(self):

        event_name = "Monitor_TurnOff_event"
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

        ##
        # Invoke monitor turn off and on for edp
        for display in self.connected_list:
            color_common_utility.start_etl_capture("MonitorTurnOffandOnEvent")
            if display_utility.get_vbt_panel_type(display, 'gfx_0') in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                if color_common_utility.monitor_turn_off_on_events() is False:
                    color_common_utility.stop_etl_capture("MonitorTurnOffandOnEvent")
                    self.fail("Failed to invoke monitor turn off and on")
                break
            display_monitorturnoff_on_etl_file = color_common_utility.stop_etl_capture("MonitorTurnOffandOnEvent")

        ##
        # Verify HDR persistence after monitor_turn_off event
        if self.os_hdr_verify.verify_hdr_persistence(event_name, self.enumerated_displays, self.platform, self.connected_list) is False:
            self.fail("Failed to verify HDR persistence after monitor turn off and on event")

        ##
        # Restart the display driver
        restart_status, reboot_required = display_essential.restart_gfx_driver()

        self.enumerated_displays = self.config.get_enumerated_display_info()

        event_name = "Restart_display_driver_event"
        ##
        # Verify HDR persistence after restart the display driver
        if self.os_hdr_verify.verify_hdr_persistence(event_name, self.enumerated_displays, self.platform, self.connected_list) is False:
            self.fail("Failed to verify HDR persistence after driver restart")
        else:
            logging.info("HDR Persisted after driver restart")

        ##
        # Disable HDR
        self.enumerated_displays = self.config.get_enumerated_display_info()
        super().toggle_and_verify_hdr(toggle="DISABLE")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
