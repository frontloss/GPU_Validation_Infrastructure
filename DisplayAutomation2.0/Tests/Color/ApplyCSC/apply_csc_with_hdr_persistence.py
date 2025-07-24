#######################################################################################################################
# @file         apply_csc_with_hdr_persistence.py
# @addtogroup   Test_Color
# @section      apply_csc_with_hdr_persistence
# @remarks      @ref apply_csc_with_hdr_persistence.py \n
#               The test script invokes Driver Escape call to enable and apply any CSC
#               taking the csc client(Linear\Non-Linear) from the command line along with
#               the matrix also provided as part of command line. The matrix is stored in the input_csc_matrix JSON file
#               The test script performs register level verification based on the CSC client
#               Script then enables HDR and verifies if the escape call to Apply LINEAR\NON-LINEAR csc is successful
#               then disable HDR event and performs csc verification after HDR event
# CommandLine:  python apply_csc_with_hdr_persistence.py -edp_a SINK_EDP050 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.ApplyCSC.apply_csc_base import *
from Tests.Color.HDR.OSHDR.os_hdr_base import *


class ApplyCSCWithHDRPersistence(ApplyCSCBase, OSHDRBase):

    def runTest(self):
        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(self.matrix_info))
        params = CSCPipeMatrixParams(1, csc_params)

        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                           display_index].ConnectorNPortType))
            if display in self.connected_list and \
                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                if driver_escape.apply_csc(
                        self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                        enum.OPERATION_SET, self.csc_type, params) is False:
                    logging.error("Failed to apply %s" % CSC_MATRIX_TYPE(
                        self.csc_type).name)
                    self.fail("Failed to apply %s" % CSC_MATRIX_TYPE(
                        self.csc_type).name)
                else:
                    logging.info("Successfully applied %s" % CSC_MATRIX_TYPE(
                        self.csc_type).name)

                    ##
                    # Verify the CSC
                    if csc_utility.verify_degamma_csc_gamma_blocks(self.matrix_info, display, self.csc_type):
                        logging.info("Register level verification is SUCCESS")
                    else:
                        logging.error("Register level verification is FAILED")
                        self.fail("Register level verification is FAILED")

        ##
        # Enable HDR on all the displays
        logging.info("Performing HDR Disable-Enable event")
        super().toggle_and_verify_hdr(toggle="ENABLE")

        ##
        # Apply an identity csc matrix while HDR is enabled since we expect escape call to fail if the CSC Client is LINEAR
        identity_matrix = [[1, 0, 0], [0, 1, 0],[0, 0, 1]]
        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(identity_matrix))
        params = CSCPipeMatrixParams(1, csc_params)
        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                           display_index].ConnectorNPortType))
            if display in self.connected_list and \
                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:

                if CSC_MATRIX_TYPE(self.csc_type).name == "LINEAR":
                    if driver_escape.apply_csc(self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                            enum.OPERATION_SET, self.csc_type, params) is False:
                        logging.info("Escape call to apply %s in HDR mode - Expected : NOT SUPPORTED; Actual : NOT SUPPORTED" % CSC_MATRIX_TYPE(
                            self.csc_type).name)
                    else:
                        logging.info(
                            "Escape call to apply %s in HDR mode - Expected : NOT SUPPORTED; Actual : SUPPORTED" % CSC_MATRIX_TYPE(
                                self.csc_type).name)
                        self.fail("Escape call to apply LINEAR CSC in HDR mode - Expected : NOT SUPPORTED; Actual : SUPPORTED")
                else:
                    if driver_escape.apply_csc(self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                            enum.OPERATION_SET, self.csc_type, params) is True:
                        logging.info("Escape call to apply %s in HDR mode - Expected : SUPPORTED; Actual : SUPPORTED" % CSC_MATRIX_TYPE(
                            self.csc_type).name)

                        ##
                        # Verify the CSC
                        if csc_utility.verify_degamma_csc_gamma_blocks(identity_matrix, display, self.csc_type):
                            logging.info("Register level verification is SUCCESS after applying NON-LINEAR IDENTITY CSC in HDR Mode")
                        else:
                            logging.error("Register level verification is FAILED after applying NON-LINEAR IDENTITY CSC in HDR Mode")
                            self.fail("Register level verification is FAILED after applying NON-LINEAR IDENTITY CSC in HDR Mode")

                    else:
                        logging.info(
                            "Escape call to apply %s CSC in HDR mode - Expected : SUPPORTED; Actual : NOT SUPPORTED" % CSC_MATRIX_TYPE(
                                self.csc_type).name)
                        self.fail("Escape call to apply LINEAR CSC in HDR mode - Expected : SUPPORTED; Actual : NOT SUPPORTED")

        ##
        # Disable HDR and switch to SDR Mode
        super().toggle_and_verify_hdr(toggle="DISABLE")
        if self.csc_type == "LINEAR":
            for display_index in range(self.enumerated_displays.Count):
                display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                               display_index].ConnectorNPortType))
                if display in self.connected_list and \
                        self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                    ##
                    # Verify the CSC
                    if csc_utility.verify_degamma_csc_gamma_blocks(self.matrix_info, display, self.csc_type):
                        logging.info(
                            "Register level verification is SUCCESS after applying %s CSC in SDR Mode" % CSC_MATRIX_TYPE(
                        self.csc_type).name)
                    else:
                        logging.error(
                            "Register level verification is FAILED after applying %s CSC in SDR Mode" % CSC_MATRIX_TYPE(
                        self.csc_type).name)
                        self.fail(
                            "Register level verification is FAILED in SDR Mode")
        else:
            for display_index in range(self.enumerated_displays.Count):
                display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                               display_index].ConnectorNPortType))
                if display in self.connected_list and \
                        self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                    ##
                    # Verify the CSC
                    if csc_utility.verify_degamma_csc_gamma_blocks(identity_matrix, display,
                                                                   self.csc_type):
                        logging.info("Register level verification is SUCCESS after applying NON-LINEAR IDENTITY CSC in SDR Mode")
                    else:
                        logging.error("Register level verification is FAILED after applying NON-LINEAR IDENTITY CSC in SDR Mode")
                        self.fail("Register level verification is FAILED after applying NON-LINEAR IDENTITY CSC in SDR Mode")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
