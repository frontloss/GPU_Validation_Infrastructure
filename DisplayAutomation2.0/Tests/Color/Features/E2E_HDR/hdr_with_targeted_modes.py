#######################################################################################################################
# @file                 hdr_basic.py
# @addtogroup           Test_Color
# @section              hdr_with_targeted_mode
# @remarks              @ref hdr_with_targeted_mode.py \n
#                       The test script enables HDR on the displays supporting HDR, applies specific targeted modes
#                       which is an input parameter from the test command line.
#                       Additionally, for an eDP_HDR display the script invokes the API
#                       to set the OS Brightness Slider level to a value provided in the command line.
#                       If Brightness Slider level has not been given as an input, script sets the slider
#                       to a random value other than the Current Brightness value.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python hdr_targeted_mode.py -edp_a SINK_EDP192 -TARGETEDMODE 2880x1800 -config SINGLE
# @author       Vimalesh D
#######################################################################################################################
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Verification.verify_pipe import *


class HDRTargetedModes(HDRTestBase):
    targetedMode = None
    def setUp(self):
        ##
        # Add a custom tag to parse the User requested PSR Feature
        self.custom_tags["-TARGETEDMODE"] = None
        super().setUp()
        self.targetedMode = str(self.context_args.test.cmd_params.test_custom_tags["-TARGETEDMODE"][0])

    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        logging.info("*** Step 2 : Perform Mode Switch and verify ***")
        hzres = int(self.targetedMode.split("X")[0])
        vtres = int(self.targetedMode.split("X")[1])
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    ##
                    # Store the current mode
                    mode_list = common_utility.get_modelist_subset(panel.display_and_adapterInfo, -1, -1, -1, hzres, vtres)
                    if mode_list is None:
                        logging.error("Edid not enumerated with requested timing")
                        self.fail("Edid not enumerated with requested timing")
                    for mode in mode_list:
                        common_utility.apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                   mode.scaling)

                        # Verify DSC Programming if DSC supported panel is connected
                        is_vdsc_panel = DSCHelper.is_vdsc_supported_in_panel(gfx_index, port)
                        if is_vdsc_panel is True:
                            is_success = dsc_verifier.verify_dsc_programming(gfx_index, port)
                            self.assertTrue(is_success,
                                            f"DSC Verification Failed for {port}")
                            logging.info(f"DSC Verification Successful for {port}")

                        panel_props = self.panel_props_dict[gfx_index, port]
                        event = "ModeSet_" + str(mode.HzRes) + "X" + str(mode.VtRes) + "@" + str(mode.refreshRate)
                        logging.info(
                            "Updating all color properties for Panel : {0} on Adapter : {1} attached to Pipe : {2}"
                            " after mode-set event".format(
                                port, gfx_index, panel.pipe))
                        color_properties.update_feature_caps_in_context(self.context_args)
                        if self.update_common_color_props_for_all(event) is False:
                            self.fail()
                        if panel.is_active:
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                                self.fail()
                            if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                self.fail()



    ##
    # Since the runTest would have already disabled HDR across all the panels in Step2
    # Need to only clean up by applying a Unity Gamma and Unplug of the displays
    def tearDown(self):
        ##
        # Apply Unity Gamma as part of clean-up
        gamma_utility.apply_gamma()
        ##
        # Invoking the Base class's tearDown() to perform the general clean-up activities
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables HDR on supported panels and perform verification on all panels"
        " when HDR is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)

