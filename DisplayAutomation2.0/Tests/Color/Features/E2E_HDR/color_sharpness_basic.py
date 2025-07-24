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
#                        Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python hdr_targeted_mode.py -edp_a SINK_EDP192 -TARGETEDMODE 2880x1800 -config SINGLE
# @author       Vimalesh D
#######################################################################################################################
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Verification.verify_pipe import *
from Libs.Core.display_config.display_config import DisplayConfiguration


class HDRSharpness(HDRTestBase):
    sharpness_intensity = None
    sharpness_status =  None
    display_config = DisplayConfiguration()
    def setUp(self):
        ##
        # Add a custom tag to parse the User requested PSR Feature
        self.custom_tags["-SHARPNESS_INTENSITY"] = None
        self.custom_tags["-SHARPNESS_STATUS"] = None
        super().setUp()
        self.sharpness_intensity = int(self.context_args.test.cmd_params.test_custom_tags["-SHARPNESS_INTENSITY"][0])
        self.sharpness_status = str(self.context_args.test.cmd_params.test_custom_tags["-SHARPNESS_STATUS"][0])

    def runTest(self):
        ##
        # Enable Sharpness
        #Enable Sharpness
        setSharpness = control_api_args.ctl_sharpness_settings()
        setSharpness.Size = ctypes.sizeof(setSharpness)
        setSharpness.FilterType = control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value
        setSharpness.Enable = self.sharpness_status
        setSharpness.Intensity = self.sharpness_intensity

        logging.info("Step_1: Set Sharpness")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                targetid=panel.target_id
                if control_api_wrapper.set_sharpness(setSharpness, targetid):
                    logging.info("Pass: Set Sharpness Intensity-{} via Control Library".format(setSharpness.Intensity))
                else:
                    logging.error("Fail: Set Sharpness via Control Library")
                    gdhm.report_driver_bug_clib("Set Sharpness Failed via Control Library - "
                                                "Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                                                .format(setSharpness.Enable, setSharpness.Intensity, setSharpness.FilterType))
                    self.fail("Set Sharpness Failed via Control Library")
                
                # fetch all the modes supported by each of the displays connected
                supported_modes = self.display_config.get_all_supported_modes([targetid])
                for key, values in supported_modes.items():
                    mode = values[0]
                    mode.rotation = enum.ROTATE_0
                    # Apply Native mode with zero rotation
                    self.display_config.set_display_mode([mode], virtual_mode_set_aware=False, force_modeset=True)
                    logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                        mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))


                getSharpness = control_api_args.ctl_sharpness_settings()
                getSharpness.Size = ctypes.sizeof(getSharpness)

                logging.info("Step_2: Get Sharpness")
                if control_api_wrapper.get_sharpness(getSharpness, targetid):
                    logging.info("Pass: Get Sharpness via Control Library")
                    if getSharpness.Intensity == setSharpness.Intensity:
                        logging.info("Pass: Get Sharpness Intensity-{} matched with Set Sharpness via Control Library"
                                     .format(getSharpness.Intensity))
                    else:
                        gdhm.report_driver_bug_clib("Get Sharpness Intensity Failed to match Set Sharpness via Control Library "
                                                    "Expected: {0} Actual: {1}"
                                                    .format(setSharpness.Intensity, getSharpness.Intensity))
                        self.fail("Get Sharpness Intensity failed to match via Control Library")
                else:
                    logging.error("Fail: Get Sharpness via Control Library")
                    gdhm.report_driver_bug_clib("Get Sharpness Failed via Control Library for "
                                                "Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                                                .format(getSharpness.Enable,getSharpness.Intensity,getSharpness.FilterType))
                    self.fail("Get Sharpness Failed via Control Library")



if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables HDR on supported panels and perform verification on all panels"
        " when HDR is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)

