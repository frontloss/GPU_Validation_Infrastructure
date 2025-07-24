#######################################################################################################################
# @file         os_hdr_displayswitch_stress_multi_pipe.py
# @addtogroup   Test_Color
# @section      os_hdr_displayswitch_stress_multi_pipe.
# @remarks      @ref  os_hdr_displayswitch_stress_multi_pipe.py \n
#               The Stress test for verifying the persistence of HDR with display switch event for multiple display
#               Basic register verification (HDR Mode in Pipe_Misc register) will be performed.
#               To-Do : Add ETL Parsing for Metadata
# CommandLine:  python  os_hdr_displayswitch_stress_multi_pipe.py -edp_a SINK_EDP050 -hdmi_b  SamsungJS9500_HDR.bin
#               -config EXTENDED
#               python  os_hdr_displayswitch_stress_multi_pipe.py -edp_a SINK_EDP050 -dp_d  Benq_SW320.bin
#               DP_HDR_DPCD.txt  -CONFIG EXTENDED
# @author       Vimalesh D
#######################################################################################################################
import time
import itertools
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color.HDR.OSHDR import os_hdr_verification


class OSHdrStressDisplaySwitchEvent(OSHDRBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    def runTest(self):

        event_name = "Display_switch_stress_event"
        ##
        # Check Power Mode  for DC or AC to check the HDR Option temporarily disabled
        result, status = color_common_utility.check_and_apply_power_mode()
        if status:
            logging.info(result)
        else:
            self.fail(result)

        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]
        display_list = []
        display_config_list = []

        ##
        # Enable OS_HDR on all active displays
        self.enumerated_displays = self.config.get_enumerated_display_info()

        super().toggle_and_verify_hdr(toggle="ENABLE")

        time.sleep(5)

        ##
        # Apply 4K Modeset with refresh rate 60 hz.But based on supported modes it will apply,So ignoring this.
        super().apply_native_mode()

        for display_index in range(len(self.connected_list)):
            display_list.append(self.connected_list[display_index])

        for i in range(2, len(display_list) + 1):
            for subset in itertools.permutations(display_list, i):
                for j in range(1, len(topology_list)):
                    display_config_list.append((topology_list[0], [subset[0]]))
                    display_config_list.append((topology_list[j], list(subset)))

        for each_config in range(len(display_config_list)):
            topology = display_config_list[each_config][0]
            displays_list = display_config_list[each_config][1]

            stress_display_event = "stress_display_switch_topology"+str(topology)
            if color_common_utility.start_etl_capture(stress_display_event) is False:
                self.fail("GfxTrace failed to start")
            if color_common_utility.display_switch(topology, displays_list) is False:
                self.fail("Failed to apply display switch")
            else:
                logging.info("Finished display switch event")

                self.enumerated_displays = self.config.get_enumerated_display_info()

                if topology != enum.CLONE:
                    current_topology = "NOTCLONE"
                else:
                    current_topology = "CLONE"

                ##
                # Verify HDR persistence after display_switch event

                if self.os_hdr_verify.verify_hdr_persistence(event_name, self.enumerated_displays, self.platform, displays_list, "NO", topology=current_topology) is False:
                    color_common_utility.stop_etl_capture(stress_display_event)
                    self.fail("Failed to verify HDR persistence after display switch")

            display_switch_etl_file = color_common_utility.stop_etl_capture(stress_display_event)

        ##
        # Disable HDR
        self.enumerated_displays = self.config.get_enumerated_display_info()
        super().toggle_and_verify_hdr(toggle="DISABLE")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
