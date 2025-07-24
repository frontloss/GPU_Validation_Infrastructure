#######################################################################################################################
# @file                 hdr_basic.py
# @addtogroup           Test_Color
# @section              hdr_basic
# @remarks              @ref hdr_basic.py \n
#                       The test script enables HDR on the displays supporting HDR,
#                       which is an input parameter from the test command line.
#                       Additionally, for an eDP_HDR display the script invokes the API
#                       to set the OS Brightness Slider level to a value provided in the command line.
#                       If Brightness Slider level has not been given as an input, script sets the slider
#                       to a random value other than the Current Brightness value
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python hdr_basic.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_basic.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Verification.verify_pipe import *


class HDRBasic(HDRTestBase):

    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR/WCG on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        logging.info("*** Step 2 : Disable HDR/WCG on all supported panels and verify ***")
        ##
        # Disable HDR on all the supported panels and perform verification
        # Here the intent is that, the panels are all in SDR Mode
        if self.toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()
        ##
        # If WCG is enabled; set the
        if self.enable_wcg:
            self.enable_wcg = False

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                panel_props = color_properties.HDRProperties()
                logging.info(
                    "Initializing all color properties after disabling HDR for Panel : {0} on Adapter : {1} attached "
                    "to Pipe : {2}".format(
                        port,
                        gfx_index,
                        panel.pipe))

                if color_properties.initialize_panel_color_properties(panel.target_id, panel.pipe, gfx_index,
                                                                      panel_props) is False:
                    self.fail()

                feature = "WCG" if self.enable_wcg else "HDR"
                status, panel_props.bpc = color_etl_utility.fetch_feature_modeset_details_from_os(panel.pipe, feature)
                self.panel_props_dict[gfx_index, port] = panel_props
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

