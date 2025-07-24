#######################################################################################################################
# @file                 color_transforms_hdr_basic.py
# @addtogroup           Test_Color
# @section              color_transforms_hdr_basic
# @remarks              @ref color_transforms_hdr_basic.py \n
#                       The test script enables HDR on the edp_hdr display(SDP/Aux)
#                       which is an input parameter from the test command line.
#                       Test script invokes the GammaApp with a scale factor, r_factor=0.65,
#                       CSC Data is parsed from the ETL and verified with the programmed CSC coefficients.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       PipeDeGamma is verified to be disabled in HDR Mode.
#                       CSC Coefficients are compared with the reference coefficients
#                       To-Do : Add PostOffset coefficient verification
#                       PipeGamma combined with GammaWithScaleFactor is verified through ETLs
# Sample CommandLines:  python color_transforms_hdr_basic.py -hdmi_b SamsungJS9500_HDR.bin SINK_EDP50 -config SINGLE
# Sample CommandLines:  python color_transforms_hdr_basic.py -DP_D Benq_SW320.bin DP_HDR_DPCD.txt -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.HDR.eDP_HDR.edp_hdr_base import *


class ColorTransformsWithHDR(OSHDRBase):

    def runTest(self):
        ##
        # Stop the Environment ETL
        env_etl_path = color_common_utility.stop_etl_capture("Stopping_Environment_ETL_TimeStamp_")
        if etl_parser.generate_report(env_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Verify HDR Caps
        if color_parse_etl_events.fetch_and_verify_hdr_caps_from_etl() is False:
            self.fail()

        ##
        # Enable HDR
        super().toggle_and_verify_hdr(toggle="ENABLE")

        ##
        # Applying Gamma with a scalefactor of 0.65
        color_common_utility.apply_unity_gamma(r_factor=0.65)

        time.sleep(5)

        ##
        # Stop the ETL after applying Gamma
        gamma_scalefactor_etl = color_common_utility.stop_etl_capture("After_applying_gamma_with_0.65R_Scalefactor_TimeStamp_")
        if etl_parser.generate_report(gamma_scalefactor_etl) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        for display_index in range(self.enumerated_displays.Count):
            display = str(
                CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            if display in self.connected_list and self.enumerated_displays.ConnectedDisplays[display_index].IsActive:

                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID
                os_rel_lut_with_scaled_gamma = color_parse_etl_events.get_os_one_d_lut_from_etl(target_id)
                if os_rel_lut_with_scaled_gamma is False:
                    logging.error("No OneDLut Event given by OS after invoking the GammaApp with a scalefactor")
                    self.fail("No OneDLut Event given by OS after invoking the GammaApp with a scalefactor")

                ##
                # Fetch the OS CSCData in XYZFormat from the ETL
                os_relative_csc = color_parse_etl_events.get_os_csc_from_etl(target_id)
                if os_relative_csc is False:
                    self.fail("OSGivenCSCData NOT event found in ETLs (OS Issue)")

                current_pipe = color_common_utility.get_current_pipe(display)
                ##
                # Verify if PipeDegamma is disabled in HDR Mode
                if not color_common_utility.verify_degamma_enable(self.platform, current_pipe, hdr_mode=True):
                    self.fail("Register verification for Pipe DeGamma failed")
                ##
                # Verify Pipe CSC
                reference_lut = color_common_utility.generate_reference_csc_matrix(os_relative_csc, hdr_mode=True)
                programmed_lut = color_common_utility.get_csc_coeff_matrix_from_reg(self.platform, current_pipe)
                if not color_common_utility.compare_csc_coeff(reference_lut, programmed_lut):
                    self.fail("FAIL : CSC Coefficients NOT matching")
                else:
                    logging.info("SUCCESS : CSC Coefficients Match")

                ##
                # Verify Pipe Gamma Data
                if color_common_utility.fetch_ref_hdr_gamma_and_programmed_gamma_and_compare(self.platform,
                                                                                             current_pipe,
                                                                                             os_rel_lut_with_scaled_gamma,
                                                                                             color_common_constants.OS_RELATIVE_LUT_SIZE):
                    logging.info("Pipe Gamma verification after applying Gamma with scalefactor 0.65 for Red Channel is SUCCESSFUL")
                else:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR]Gamma verification failed after applying Gamma with scalefactor 0.65 for Red Channel")
                    self.fail("Pipe Gamma verification after applying Gamma with scalefactor 0.65 for Red Channel FAILED")

    def tearDown(self):
        ##
        # Apply Unity Gamma at the end of the test after disabling HDR(Done as part of OSHDR tearDown())
        color_common_utility.apply_unity_gamma()

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
