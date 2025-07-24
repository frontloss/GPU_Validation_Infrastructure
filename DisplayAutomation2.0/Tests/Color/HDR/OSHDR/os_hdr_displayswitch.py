#######################################################################################################################
# @file         os_hdr_displayswitch.py
# @addtogroup   Test_Color
# @section      os_hdr_displayswitch
# @remarks      @ref os_hdr_displayswitch.py \n
#               Test for HDR in display switch scenario of Single, Clone, Extended for two displays
#               Basic register verification (HDR Mode in Pipe_Misc register) will be performed after display switch
#               to check the persistence of HDR.
#               To-Do : Add ETL Parsing for Metadata
# CommandLine:  python os_hdr_displayswitch.py -edp_a SINK_EDP050 -hdmi_b  SamsungJS9500_HDR.bin -config EXTENDED
#               python os_hdr_displayswitch.py -edp_a SINK_EDP050 -dp_d  Benq_SW320.bin  DP_HDR_DPCD.txt  -CONFIG
#               EXTENDED
# @author       Vimalesh D
#######################################################################################################################
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color import color_common_utility
from Tests.Color.HDR.OSHDR import os_hdr_verification


class OSHdrTestDisplaySwitch(OSHDRBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    def runTest(self):

        event_name = "Display_switch_event"
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
        # Apply 4K Modeset
        super().apply_native_mode()

        ##
        # Apply display config list
        display_config_list = [(enum.SINGLE, [self.connected_list[0]]), (enum.SINGLE, [self.connected_list[1]]),
                               (enum.CLONE, self.connected_list), (enum.EXTENDED, self.connected_list)]

        if color_common_utility.start_etl_capture("display_switch") is False:
            self.fail("GfxTrace failed to start")
        for index in range(len(display_config_list)):
            topology = display_config_list[index][0]
            displays_list = display_config_list[index][1]

            if color_common_utility.display_switch(topology, displays_list) is True:
                logging.info("Successfully applied  display configuration")

                self.enumerated_displays = self.config.get_enumerated_display_info()

                if topology != enum.CLONE:
                    current_topology = "NOTCLONE"
                else:
                    current_topology = "CLONE"
                ##
                # Verify HDR persistence after display_switch event

                if self.os_hdr_verify.verify_hdr_persistence(event_name, self.enumerated_displays, self.platform, displays_list, "NO", topology=current_topology) is False:
                    color_common_utility.stop_etl_capture("display_switch")
                    self.fail()

            else:
                self.fail("Failed to apply display configuration")

        display_switch_etl_file = color_common_utility.stop_etl_capture("display_switch")

        ##
        # Disable HDR
        self.enumerated_displays = self.config.get_enumerated_display_info()
        super().toggle_and_verify_hdr(toggle="DISABLE")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
