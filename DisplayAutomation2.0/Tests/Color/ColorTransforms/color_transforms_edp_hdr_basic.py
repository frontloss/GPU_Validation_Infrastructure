#######################################################################################################################
# @file                 color_transforms_edp_hdr_basic.py
# @addtogroup           Test_Color
# @section              color_transforms_edp_hdr_basic
# @remarks              @ref color_transforms_edp_hdr_basic.py \n
#                       The test script enables HDR on the edp_hdr display(SDP/Aux)
#                       which is an input parameter from the test command line.
#                       Test script invokes the GammaApp with a scale factor, r_factor=0.5, g_factor=0.75, b_factor= 0.9
#                       CSC Data is parsed from the ETL and verified with the programmed CSC coefficients. The script
#                       invokes the MSFT API to set the OS Brightness Slider level to a brightness slider level to 15
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       PipeDeGamma is verified to be disabled in HDR Mode.
#                       CSC Coefficients are compared with the reference coefficients
#                       To-Do : Add PostOffset coefficient verification
#                       PipeGamma with PixelBoostCompensation combined with GammaWithScaleFactor is verified through ETLs
# Sample CommandLines:  python color_transforms_edp_hdr_basic.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python color_transforms_edp_hdr_basic.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.HDR.eDP_HDR.edp_hdr_base import *


class ColorTransformsWitheDPHDR(OSHDRBase, eDPHDRBase):

    def runTest(self):
        brightness_slider_level = 15
        ##
        # Stop the Environment ETL
        env_etl_path = color_common_utility.stop_etl_capture("Stopping_Environment_ETL_TimeStamp_")
        if etl_parser.generate_report(env_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Verify HDR Caps from the Environment ETL Captured
        if color_parse_etl_events.fetch_and_verify_hdr_caps_from_etl() is False:
            self.fail()

        ##
        # Enable HDR on all the active displays
        super().toggle_and_verify_hdr(toggle="ENABLE")

        ##
        # Applying Gamma with a scalefactor of r_factor=0.5, g_factor=0.75, b_factor= 0.9
        color_common_utility.apply_unity_gamma(r_factor=0.5, g_factor=0.75, b_factor= 0.9)

        time.sleep(2)

        ##
        # Stop the ETL after applying Gamma to parse the same to get the Gamma, CSC data
        gamma_scalefactor_etl = color_common_utility.stop_etl_capture("After_Gamma_with_0.5R_0.75G_0.9B_TimeStamp_")
        if etl_parser.generate_report(gamma_scalefactor_etl) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Iterate through all the active LFP displays(Applicable on Dual eDP)
        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            gfx_index = self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if display in self.connected_list and self.enumerated_displays.ConnectedDisplays[display_index].IsActive and \
                    display_utility.get_vbt_panel_type(display, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:

                ##
                # Fetch the targetID to get the Gamma and CSC data based on TargetID from the ETLs
                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID

                ##
                # Fetch the OS Relative 1DLUTData from the ETL
                os_relative_lut = color_parse_etl_events.get_os_one_d_lut_from_etl(target_id)
                if os_relative_lut is False:
                    self.fail("OSGiven1DLUT NOT event found in ETLs (OS Issue)")

                ##
                # Fetch the OS CSCData in XYZFormat from the ETL
                os_relative_csc = color_parse_etl_events.get_os_csc_from_etl(target_id)
                if os_relative_csc is False:
                    self.fail("OSGivenCSCData NOT event found in ETLs (OS Issue)")

                ##
                # Fetch the Current Pipe attached to the targetID
                current_pipe = color_common_utility.get_current_pipe(display)

                ##
                # Verify if PipeDeGamma is disabled since HDR is enabled
                if not color_common_utility.verify_degamma_enable(self.platform, current_pipe, hdr_mode=True):
                    self.fail("Register verification for Pipe DeGamma failed")

                ##
                # Verify PipeCSC programming
                reference_lut = color_common_utility.generate_reference_csc_matrix(os_relative_csc, hdr_mode=True)
                programmed_lut = color_common_utility.get_csc_coeff_matrix_from_reg(self.platform, current_pipe)
                if not color_common_utility.compare_csc_coeff(reference_lut, programmed_lut):
                    self.fail("FAIL : CSC Coefficients NOT matching")
                else:
                    logging.info("SUCCESS : CSC Coefficients Match")

                ##
                # Verify Pipe Gamma Data
                result, brightness_val_in_context, sdr_white_level_in_context = edp_hdr_utility.set_and_verify_brightness3_for_a_slider_level(
                    self.platform, current_pipe, target_id, brightness_slider_level, os_relative_lut)
                if result is False:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR]Gamma verification failed for Brightness Slider Level with GammaScaleFactors : 0.5R_0.75G_0.9B channels")
                    self.fail("Gamma verification for Brightness Slider Level %s with GammaScaleFactors : 0.5R_0.75G_0.9B channels FAILED" % brightness_slider_level)
                else:
                    logging.info("Gamma verification for Brightness Slider Level %s with GammaScaleFactors : 0.5R_0.75G_0.9B channels is SUCCESSFUL" % brightness_slider_level)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
