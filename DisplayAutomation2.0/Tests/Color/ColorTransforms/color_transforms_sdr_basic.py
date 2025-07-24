#######################################################################################################################
# @file                 color_transforms_sdr_basic.py.py
# @addtogroup           Test_Color
# @section              color_transforms_sdr_basic.py
# @remarks              @ref color_transforms_sdr_basic.py.py \n
#                       Test script invokes the GammaApp with a scale factor on green channel(0.5)
#                       pipe_csc(red_blue_swap) via driver escape call.
#                       Verification Details:
#                       Pipe DeGamma Enable bit and the Data is verified
#                       CSC Coefficients are compared with the reference coefficients
#                       To-Do : Add PostOffset coefficient verification
#                       Programmed PipeGamma values are compared with a static SRGB_Encode_lut multiplied with the scalefactor
# Sample CommandLines:  python color_transforms_sdr_basic.py -edp_a -config SINGLE
# Sample CommandLines:  python color_transforms_sdr_basic.py -hdmi_b -config SINGLE
# Sample CommandLines:  python color_transforms_sdr_basic.py -dp_d -config SINGLE
# Sample CommandLines:  python color_transforms_sdr_basic.py -edp_a -hdmi_b -dp_d -config CLONE
# @author       Smitha B
#######################################################################################################################
import time
from copy import deepcopy
from Libs.Core import driver_escape
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.wrapper.driver_escape_args import CSCPipeMatrixParams
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color.ApplyCSC import csc_utility
from Tests.Color.HDR.Gen11_Flip.MPO3H.HDRConstants import *


class ColorTransformsSDRBasic(ColorCommonBase):

    def runTest(self):
        red_blue_swap = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(red_blue_swap))
        params = CSCPipeMatrixParams(1, csc_params)
        ##
        # Stop the Environment ETL
        env_etl_path = color_common_utility.stop_etl_capture("Stopping_Environment_ETL_TimeStamp_")
        if etl_parser.generate_report(env_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        ##
        # Apply Unity Gamma at the beginning of the test after enabling HDR
        color_common_utility.apply_unity_gamma(g_factor=0.5)

        time.sleep(10)

        env_etl_path = color_common_utility.stop_etl_capture("After_Applying_0.5G_Gamma_TimeStamp_")
        if etl_parser.generate_report(env_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()

        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            if display in self.connected_list and self.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                ##
                # Applying Linear CSC
                if driver_escape.apply_csc(self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo, 1, 0, params) is False:
                    logging.error("Failed to apply RED_BLUE_SWAP LINEAR CSC")
                    self.fail("Failed to apply RED_BLUE_SWAP LINEAR CSC")
                else:
                    logging.info("Successfully applied RED_BLUE_SWAP LINEAR CSC")
                    current_pipe = color_common_utility.get_current_pipe(display)

                    ##
                    # Verify if PipeDeGamma is disabled since HDR is enabled
                    if not color_common_utility.verify_degamma_enable(self.platform, current_pipe, hdr_mode=False):
                        self.fail("Register verification for Pipe DeGamma failed")
                    ##
                    # Verify Pipe DeGamma Data
                    programmed_srgb_pipe_degamma_lut = color_common_utility.get_degamma_lut_from_register(self.platform, current_pipe)
                    if color_common_utility.compare_ref_and_programmed_gamma_lut(SRGB_Decode_35_Samples_16bpc, programmed_srgb_pipe_degamma_lut):
                        logging.info("Pipe DeGamma Data verification is SUCCESSFUL")
                    else:
                        logging.error("Pipe DeGamma Data verification FAILED")
                        self.fail("Pipe DeGamma Data verification FAILED")

                    ##
                    # Verify PipeCSC programming
                    programmed_lut = color_common_utility.get_csc_coeff_matrix_from_reg(self.platform, current_pipe)
                    if not color_common_utility.compare_csc_coeff(red_blue_swap, programmed_lut):
                        self.fail("FAIL : CSC Coefficients NOT matching")
                    else:
                        logging.info("SUCCESS : CSC Coefficients Match")

                    ##
                    # Verify Pipe Gamma Data
                    ref_lut = color_common_utility.generate_ref_gamma_with_scale_factor(SRGB_Encode_515_Samples_16bpc, g_factor=0.5)
                    prog_lut = color_common_utility.fetch_hdr_gamma_mmio_data_from_etl(self.platform, current_pipe, multi_segment_support=False)
                    if color_common_utility.compare_ref_and_programmed_gamma_lut(ref_lut, prog_lut):
                        logging.info("Gamma Verification after applying Gamma with scalefactor 0.5 for Green channel is SUCCESSFUL")
                    else:
                        logging.info("Gamma Verification after applying Gamma with scalefactor 0.5 for Green channel is FAILED")

    def tearDown(self):
        identity_csc = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        identity_csc_param = csc_utility.create_15_16_format_csc_matrix(deepcopy(identity_csc))
        param = CSCPipeMatrixParams(1, identity_csc_param)
        for index in range(0, len(self.connected_list)):
            if driver_escape.apply_csc(self.enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo,
                                       1, 0, param) is True:
                logging.info(
                    "Successfully applied Identity CSC after completion of the test on %s" % (self.connected_list[index]))
            else:
                logging.info("Failed to apply Identity CSC after completion of the test on %s" % (self.connected_list[index]))
                self.fail(
                    "Failed to apply Identity CSC after completion of the test on %s" % self.connected_list[index])


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
