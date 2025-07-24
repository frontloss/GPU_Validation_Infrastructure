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
import random
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Verification.verify_pipe import *


class HDRSharpness(HDRTestBase):
    sharpness_intensity = None
    sharpness_status =  None


    def setUp(self):
        ##
        # Add a custom tag to parse the User requested PSR Feature
        self.custom_tags["-SHARPNESS_INTENSITY"] = None
        self.custom_tags["-SHARPNESS_STATUS"] = None
        super().setUp()
        self.sharpness_intensity = int(self.context_args.test.cmd_params.test_custom_tags["-SHARPNESS_INTENSITY"][0])
        self.sharpness_status = str(self.context_args.test.cmd_params.test_custom_tags["-SHARPNESS_STATUS"][0])

    def runTest(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                targetid = panel.target_id
                for intensity_value in range(0,110,10):
                ##
                #Enable Sharpness
                setSharpness = control_api_args.ctl_sharpness_settings()
                setSharpness.Size = ctypes.sizeof(setSharpness)
                setSharpness.FilterType = control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value
                setSharpness.Enable = 1
                setSharpness.Intensity = self.sharpness_intensity

                logging.info("Step_1: Set Sharpness")
                if control_api_wrapper.set_sharpness(setSharpness, targetid):
                    logging.info("Pass: Set Sharpness Intensity-{} via Control Library".format(setSharpness.Intensity))


                scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
                mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))
                # Mode_list should not be None for mode switch scenario. hardcoded to enum.MDS
                if mode_list is None:
                    mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                for mode in mode_list:
                    apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                               mode.scaling)
                    break

                getSharpness = control_api_args.ctl_sharpness_settings()
                getSharpness.Size = ctypes.sizeof(getSharpness)

                logging.info("Step_2: Get Sharpness")
                if control_api_wrapper.get_sharpness(getSharpness, targetid):
                    logging.info("Pass: Get Sharpness via Control Library")

                    logging.info("Pass: Get Sharpness Intensity-{} matched with Set Sharpness via Control Library"
                                 .format(getSharpness.Intensity))

                else:
                    logging.error("Fail: Get Sharpness via Control Library")
                    gdhm.report_driver_bug_clib("Get Sharpness Failed via Control Library for "
                                                "Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                                                .format(getSharpness.Enable,getSharpness.Intensity,getSharpness.FilterType))
                    self.fail("Get Sharpness Failed via Control Library")

        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail("HDR not enabled")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                targetid = panel.target_id
                ##
                # Enable Sharpness
                setSharpness = control_api_args.ctl_sharpness_settings()
                setSharpness.Size = ctypes.sizeof(setSharpness)
                setSharpness.FilterType = control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value
                setSharpness.Enable = 1
                setSharpness.Intensity = 85

                logging.info("Step_1: Set Sharpness")
                if control_api_wrapper.set_sharpness(setSharpness, targetid) is False:
                    self.fail("Concurrency Failed: Set Sharpness Intensity-{} via Control Library".format(setSharpness.Intensity))
                logging.info("Pass: Set Sharpness Intensity-{} via Control Library".format(setSharpness.Intensity))

        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Disable HDR on all supported panels and verify ***")
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail("HDR not enabled")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                getSharpness = control_api_args.ctl_sharpness_settings()
                getSharpness.Size = ctypes.sizeof(getSharpness)
                if control_api_wrapper.get_sharpness(getSharpness, panel.target_id):
                    logging.info("Pass: Get Sharpness via Control Library")
                    logging.info(getSharpness.Intensity)


        #Enable Sharpness
        setSharpness = control_api_args.ctl_sharpness_settings()
        setSharpness.Size = ctypes.sizeof(setSharpness)
        setSharpness.FilterType = control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value
        setSharpness.Enable = 1
        setSharpness.Intensity = 60

        logging.info("Step_1: Set Sharpness")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if control_api_wrapper.set_sharpness(setSharpness, panel.target_id):
                    logging.info("Pass: Set Sharpness Intensity-{} via Control LibraryFailed ".format(setSharpness.Intensity))

        logging.info("Pass: Set Sharpness Intensity-{} via Control Library ".format(setSharpness.Intensity))

        #Enable Sharpness
        setSharpness = control_api_args.ctl_sharpness_settings()
        setSharpness.Size = ctypes.sizeof(setSharpness)
        setSharpness.FilterType = control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value
        setSharpness.Enable = 0
        setSharpness.Intensity = 60

        logging.info("Step_1: Set Sharpness")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if control_api_wrapper.set_sharpness(setSharpness, panel.target_id):
                    logging.info("Pass: Set Sharpness Intensity-{} via Control LibraryFailed ".format(setSharpness.Intensity))

        logging.info("Pass: Set Sharpness Intensity-{} via Control LibraryFailed ".format(setSharpness.Intensity))
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
                mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))
                # Mode_list should not be None for mode switch scenario. hardcoded to enum.MDS
                if mode_list is None:
                    mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                for mode in mode_list:
                    apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                               mode.scaling)
                    break

        #Enable Sharpness
        setSharpness = control_api_args.ctl_sharpness_settings()
        setSharpness.Size = ctypes.sizeof(setSharpness)
        setSharpness.FilterType = control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value
        setSharpness.Enable = 0
        setSharpness.Intensity = 0

        logging.info("Step_1: Set Sharpness")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if control_api_wrapper.set_sharpness(setSharpness, panel.targetid):
                    logging.info("Pass: Set Sharpness Intensity-{} via Control LibraryFailed ".format(setSharpness.Intensity))
                else:
                    logging.error("Fail: Set Sharpness via Control Library")
                    self.fail("Set Sharpness via Control Library")

        logging.info("Pass: Set Sharpness Intensity-{} via Control LibraryFailed ".format(setSharpness.Intensity))


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

