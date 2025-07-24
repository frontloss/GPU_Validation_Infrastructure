#######################################################################################################################
# @file         apply_invalid_csc.py
# @addtogroup   Test_Color
# @section      apply_invalid_csc
# @remarks      @ref apply_invalid_csc.py \n
#               The test script invokes Driver Escape call to enable and apply any CSC
#               taking the csc client(Linear\Non-Linear) from the command line along with
#               the matrix also provided as part of command line. The matrix is stored in the input_csc_matrix JSON file
#               The test script performs register level verification based on the CSC client
# CommandLine:  python apply_invalid_csc.py -edp_a -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.ApplyCSC.apply_csc_base import *


class ApplyInvalidCSC(ApplyCSCBase):

    def runTest(self):

        ##
        # Apply an identity CSC at the beginning of the test
        identity_matrix = [[1, 0, 0], [0, 1, 0],[0, 0, 1]]
        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(identity_matrix))
        params = CSCPipeMatrixParams(1, csc_params)

        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                           display_index].ConnectorNPortType))
            if display in self.connected_list and \
                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                if driver_escape.apply_csc(
                        self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                        enum.OPERATION_SET, self.csc_type, params) is False:
                    logging.error("Failed to apply Identity %s CSC at the beginning of the test" % CSC_MATRIX_TYPE(
                        self.csc_type).name)
                    self.fail("Failed to apply Identity %s CSC at the beginning of the test" % CSC_MATRIX_TYPE(
                        self.csc_type).name)
                else:
                    logging.info("Successfully applied Identity %s CSC at the beginning of the test" % CSC_MATRIX_TYPE(
                        self.csc_type).name)
                    ##
                    # Verify the CSC
                    if csc_utility.verify_degamma_csc_gamma_blocks(identity_matrix, display, self.csc_type):
                        logging.info("Register level verification is SUCCESS")
                    else:
                        logging.error("Register level verification is FAILED")
                        self.fail("Register level verification is FAILED")

        ##
        # Trying to send invalid CSC matrix to the escape call
        # Expecting the Escape Call to fail, since the ValidateCSC() in driver will fail
        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(self.matrix_info))
        params = CSCPipeMatrixParams(1, csc_params)

        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                           display_index].ConnectorNPortType))
            if display in self.connected_list and \
                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                if driver_escape.apply_csc(
                        self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                        enum.OPERATION_SET, self.csc_type, params) is True:
                    logging.error("Driver applied an invalid CSC(Driver Issue)")
                    self.fail("Driver applied an invalid CSC(Driver Issue)")
                else:
                    logging.info("Driver did not apply an invalid csc.")

        ##
        # Verifying if identity CSC is persisting
        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                           display_index].ConnectorNPortType))
            if display in self.connected_list and \
                    self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                ##
                # Verify the CSC
                if csc_utility.verify_degamma_csc_gamma_blocks(identity_matrix, display, self.csc_type):
                    logging.info("Register level verification is SUCCESS")
                else:
                    logging.error("Register level verification is FAILED")
                    self.fail("Register level verification is FAILED")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
