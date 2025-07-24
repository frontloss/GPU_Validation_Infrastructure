#######################################################################################################################
# @file                 igcl_persistence_with_display_events.py
# @addtogroup           Test_Color
# @section              igcl_persistence_with_display_events
# @remarks              @ref igcl_persistence_with_display_events.py \n
# @brief                This scripts comprises modularized tests, where :
#                       1. test_01_hotplug_unplug() - Intends to verify HDR Persistence with HotUnplug-Plug of displays
#                       2. test_02_mode_switch() - Intends to verify HDR Persistence with various modesets
#                       3. test_03_display_switch() - Intends to verify HDR Persistence with different topologies
#                       4. test_03_video_playback() - Intends to verify HDR with Videoplayback scenario
#                       Each of the test modules perform the following :
#               		The test script enables HDR on the displays supporting HDR,
#               		which is an input parameter from the test command line.
#               		Additionally, for an eDP_HDR display the script invokes the API
#               		to set the OS Brightness Slider level to a value provided in the command line.
#               		If Brightness Slider level has not been given as an input, script sets the slider
#               		to a random value other than the Current Brightness value
#               		Verification Details:
#               		The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#               		Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#               		Pipe_Misc register is also verified for HDR_Mode
#               		Plane and Pipe Verification is performed by iterating through each of the displays
#               		Metadata verification, by comparing the Default and Flip Metadata is performed,
#               		along with register verification
# Sample CommandLines:  python hdr_persistence_with_display_events.py -edp_a SINK_EDP050
#                       -hdmi_b SamsungJS9500_HDR.bin -scenario HOTPLUG_UNPLUG
#                       python igcl_persistence_with_display_events.py -edp_a SINK_EDP050 -scenario MODE_SWITCH
#                       python igcl_persistence_with_display_events.py -edp_a SINK_EDP050 -dp_d -scenario DISPLAY_SWITCH
#                       python igcl_persistence_with_display_events.py -edp_a SINK_EDP050 -dp_d -scenario VIDEO_PLAYBACK
#
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.Igcl_Set_Cc_Blk.igcl_color_test_base import *


class IGCLVerifyFtrSDRMode(IGCLColorTestBase):

    def runTest(self):
        self.prepare_color_properties()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                    self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
