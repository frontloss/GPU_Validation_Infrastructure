#######################################################################################################################
# @file                 hdr_with_psr.py
# @addtogroup           Test_Color
# @section              hdr_with_psr
# @remarks              @ref hdr_with_psr.py \n
#                       The test script enables HDR on the LFP panels supporting HDR, which also has to be a PSR panel.
#                       Test scenario includes enabling HDR on all the panels,
#                       1. Change the Brightness through the OS Brightness Slider, the value can be input from the user.
#                       2. Idle Desktop Scenario
#                       3. VideoPlayBack Scenarios in Windowed and FullScreen Mode
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python hdr_with_psr.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_with_psr.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core import display_essential, winkb_helper
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Features.Concurrency import concurrency_utility
from Tests.PowerCons.Functional.PSR import psr


class HDRWithPSR(HDRTestBase):
    feature = None

    def setUp(self):
        ##
        # Add a custom tag to parse the User requested PSR Feature
        self.custom_tags["-PSR_VER"] = ['PSR1', 'PSR2']
        super().setUp()
        self.feature = self.context_args.test.cmd_params.test_custom_tags["-PSR_VER"][0]
        self.feature = psr.UserRequestedFeature.by_str(self.feature)

    def runTest(self):
        ##
        # Check if at least one of the panels plugged as part of command line request support PSR
        logging.info("*** Step 1 : Check if at least one panel supports PSR ***")
        num_of_psr_panels = 0
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if psr.is_feature_supported_in_panel(panel.target_id, self.feature):
                    logging.debug("{0} connected to Pipe {1} on Adapter {2} supports {3}". format(port, panel.pipe, gfx_index, self.feature))
                    num_of_psr_panels = +1

            if num_of_psr_panels == 0:
                logging.error("FAIL : At least one panel should support PSR")
                gdhm.report_driver_bug_os("[{0}] At least one panel should support PSR for Adapter: {1} "
                                        "Pipe".format(adapter.platform,gfx_index))
                self.fail()

        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 2 : Enable HDR on all supported panels and verify ***")
        ##
        # Enable HDR on all the supported panels and perform basic verification
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            return False

        ##
        # If the panel supports PSR2, then after performing all the test steps and verification
        # Disable PSR2 and perform the same scenarios and verfication with PSR1
        # Creating a counter to iterate through the same scenarios and verification twice in case of PSR2
        counter = 2 if self.feature == psr.UserRequestedFeature.PSR_2 else 1
        is_psr2 = True if counter == 2 else False
        while counter:
            ##
            # Change the brightness to any random value and verify HDR and PSR
            logging.info("*** Step 3 : Change the brightness to {0} and verify HDR and PSR ***".format(self.b3_val))
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe) and panel.is_lfp:
                        if hdr_utility.set_b3_slider_and_fetch_b3_info(panel.target_id, self.b3_val,
                                                                       self.panel_props_dict[gfx_index, port]) is False:
                            pass
                            self.fail()
                        if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                            pass
                            self.fail()

                        ##
                        # PSR Verification : Get the MMIO Dump to check if PSR was enabled after enabling HDR
                        # anytime during the course of the test execution
                        if concurrency_utility.verify_psr(gfx_index, adapter.platform, port, panel.pipe, panel.transcoder,
                                                          is_psr2, True) is False:
                            self.fail()
            ##
            # Enter idle desktop and verify HDR
            logging.info("*** Step 4 : Enter Idle Desktop scenario and verify PSR ***")
            time.sleep(5)

            ##
            # Verify PSR Feature
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if concurrency_utility.verify_psr(gfx_index, adapter.platform, port, panel.pipe, panel.transcoder, True, True) is False:
                        self.fail()

            ##
            # With Video Playback scenario
            logging.info(
                "*** Step 5 : Play Videoplayback Scenario in FullScreen and Windowed mode and verify HDR and PSR ***")
            media_path = ('Color\HDR\Video', 'RGB_Bars_video.mp4')
            video_path = os.path.join(test_context.SHARED_BINARY_FOLDER, media_path[0])
            video_file = os.path.join(video_path, media_path[1])
            media_mode = [True, False]

            ##
            # Play the VideoPlayBack scenario in FullScreen Mode and Windowed Mode
            for __ in range(len(media_mode)):
                if common_utility.launch_videoplayback(video_file, fullscreen=media_mode[__]) is False:
                    color_etl_utility.stop_etl_capture("Video_playback")
                    self.fail("Failed to launch media application")
                logging.info("Ended video playback ETL")
                for gfx_index, adapter in self.context_args.adapters.items():
                    for port, panel in adapter.panels.items():
                        panel_props = self.panel_props_dict[gfx_index, port]
                        event = "VideoPlayBack"
                        if self.update_common_color_props(event, panel.target_id, panel.pipe, panel.is_lfp, gfx_index, panel_props, False) is False:
                            self.fail()
                        if panel.is_active:
                            if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                self.fail()

                            ##
                            # Verify PSR Feature
                            if concurrency_utility.verify_psr(gfx_index, adapter.platform, port, panel.pipe, panel.transcoder,
                                                              is_psr2, True) is False:
                                self.fail()
            counter = counter - 1
            for gfx_index, adapter in self.context_args.adapters.items():
                psr_status = psr.disable(gfx_index, psr.UserRequestedFeature.PSR_1)
                if psr_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
            is_psr2 = False


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
