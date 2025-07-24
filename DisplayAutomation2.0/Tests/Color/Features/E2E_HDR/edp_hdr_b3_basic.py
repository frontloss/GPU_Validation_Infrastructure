#######################################################################################################################
# @file                 edp_hdr_b3_basic.py
# @addtogroup           Test_Color
# @section              edp_hdr_b3_basic
# @remarks              @ref edp_hdr_b3_basic.py \n
#                       The test script enables HDR on eDP_HDR displays,
#                       which is an input parameter from the test command line.
#                       The script can handle both Aux and SDP variety of displays.
#                       The script invokes the API to set the OS Brightness Slider level
#                       to a value provided in the command line.
#                       If Brightness Slider level has not been given as an input, script sets the slider
#                       to a random value other than the Current Brightness value
#                       The script then iterates through a list of brightness levels, performing a stress test.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification; DPCD verification is performed.
#                       In case of Aux based panel, DPCD verification is performed.
# Sample CommandLines:  python edp_hdr_b3_basic.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python edp_hdr_b3_basic.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *


class edpHDRBrightness3Basic(HDRTestBase):

    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()
        metadata_scenario = color_properties.HDRMetadataScenario()
        metadata_scenario.brightness_change = 1
        logging.info("*** Step 2 : Apply a list of B3 Slider Values and Verify ***")
        brightness_change_list = [0, 15, 45, 60, 85, 100, 99, 77, 53, 37, 22, 7, 2]
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe) and panel.is_lfp:
                    for index in range(len(brightness_change_list)):
                        if hdr_utility.set_b3_slider_and_fetch_b3_info(panel.target_id, brightness_change_list[index],
                                                                       self.panel_props_dict[gfx_index, port]) is False:
                            self.fail()
                        if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                            self.fail()
        metadata_scenario.brightness_change = 0

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
