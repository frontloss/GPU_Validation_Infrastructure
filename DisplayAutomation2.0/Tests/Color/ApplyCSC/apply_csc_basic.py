#######################################################################################################################
# @file         apply_csc_basic.py
# @addtogroup   Test_Color
# @section      apply_csc_basic
# @remarks      @ref apply_csc_basic.py \n
#               The test script invokes Driver Escape call to any CSC
#               taking the csc client(Linear\Non-Linear) from the command line along with
#               the matrix also provided as part of command line among the matrices stored in the input_csc_matrix JSON file
#               The test script performs register level verification based on the CSC client
# CommandLine:  python apply_csc_basic.py -edp_a -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.ApplyCSC.apply_csc_base import *


class ApplyCSCBasic(ApplyCSCBase):

    def runTest(self):

        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(self.matrix_info))
        params = CSCPipeMatrixParams(1, csc_params)

        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
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


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
