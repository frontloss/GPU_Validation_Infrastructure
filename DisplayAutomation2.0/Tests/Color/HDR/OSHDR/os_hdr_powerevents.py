#######################################################################################################################
# @file         os_hdr_powerevents.py
# @addtogroup   Test_Color
# @section      os_hdr_powerevents
# @remarks      @ref os_hdr_powerevents.py \n
#               Test for verifying the persistence of HDR after Power States S3,S4 and S5
#               To-Do : Add ETL Parsing for Metadata and Call Verification
# CommandLine:  python os_hdr_powerevents.py -edp_a SINK_EDP050 -hdmi_b  SamsungJS9500_HDR.bin -config EXTENDED
#               python os_hdr_powerevents.py -edp_a SINK_EDP050 -dp_d Benq_SW320.bin  DP_HDR_DPCD.txt -CONFIG
#               EXTENDED
# @author       vimalesh D
#######################################################################################################################
import time
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color.HDR.OSHDR import os_hdr_verification


class OSHdrTestPowerEvent(OSHDRBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()
    power_event = ""
    event_name = "Power_event"
    def test_before_reboot(self):

        power_states_list = [display_power.PowerEvent.S3, display_power.PowerEvent.S4, display_power.PowerEvent.S5]

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

        for state in power_states_list:
            self.power_event = "power_state_" + str(state)
            if color_common_utility.start_etl_capture(self.power_event) is False:
                self.fail("GfxTrace failed to start")
            if state == display_power.PowerEvent.S5:
                if reboot_helper.reboot(self, 'test_after_reboot') is False:
                    color_common_utility.stop_etl_capture(self.power_event)
                    self.fail("Failed to reboot the system")

            else:
                if color_common_utility.invoke_power_states(state) is False:
                    color_common_utility.stop_etl_capture(self.power_event)
                    self.fail("Failed to invoke power event")
                else:
                    logging.info("Finished power event")

                    ##
                    # Verify HDR persistence after power_event
                    if self.os_hdr_verify.verify_hdr_persistence(self.event_name, self.enumerated_displays, self.platform, self.connected_list) is False:
                        self.fail("Failed to verify HDR persistence after power event")
            display_reboot_etl_file = color_common_utility.stop_etl_capture(self.power_event)

    def test_after_reboot(self):

        logging.info("successfully applied power event S5 state")

        self.enumerated_displays = self.config.get_enumerated_display_info()
        ##
        # Verify PIPE_MISC for register verification
        ##
        # Verify HDR persistence after power_event
        if self.os_hdr_verify.verify_hdr_persistence(self.event_name, self.enumerated_displays, self.platform, self.connected_list) is False:
            self.fail("Failed to verify HDR persistence after power event")

        display_reboot_etl_file = color_common_utility.stop_etl_capture(self.power_event)
        ##
        # Disable HDR
        super().toggle_and_verify_hdr(toggle="DISABLE")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2, failfast=True).run(reboot_helper.get_test_suite('OSHdrTestPowerEvent'))
    TestEnvironment.cleanup(outcome)
