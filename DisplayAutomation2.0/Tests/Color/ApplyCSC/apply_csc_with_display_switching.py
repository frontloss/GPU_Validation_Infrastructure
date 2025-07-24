#######################################################################################################################
# @file         apply_csc_with_display_switching.py
# @addtogroup   Test_Color
# @section      apply_csc_with_display_switching
# @remarks      @ref apply_linear_csc_with_display_switching.py \n
#               The test script invokes Driver Escape call to any CSC
#               taking the csc client(Linear\Non-Linear) from the command line along with
#               the matrix also provided as part of command line among the matrices stored in the input_csc_matrix JSON file
#               and verifies the persistence of the CSC applied with different display switching scenarios
# CommandLine:  python apply_csc_with_display_switching.py -edp_a -hdmi_b -config CLONE
# @author       Smitha B
#######################################################################################################################
import itertools
from Tests.Color.ApplyCSC.apply_csc_base import *


class ApplyCSCWithDisplaySwitching(ApplyCSCBase):

    def runTest(self):
        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(self.matrix_info))
        params = CSCPipeMatrixParams(1, csc_params)

        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            if display  in self.connected_list and \
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
        # topology list to apply various configurations on the displays connected
        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]
        config_list = []

        ##
        # creating a configuration list of various topologies and the displays connected
        # ex: SINGLE Disp1, CLONE Disp1+Disp 2, SINGLE Disp2, ...
        for i in range(2, len(self.connected_list) + 1):
            for subset in itertools.permutations(self.connected_list, i):
                for j in range(1, len(topology_list)):
                    config_list.append((topology_list[0], [subset[0]]))
                    config_list.append((topology_list[j], list(subset)))

        ##
        # Apply different configurations and apply different Hue and Saturation values
        for each_config in range(len(config_list)):
            if self.config.set_display_configuration_ex(config_list[each_config][0],
                                                        config_list[each_config][1]) is True:
                logging.info("Applying a display configuration %s on %s"%(config_list[each_config][0],
                                                        config_list[each_config][1]))
                disp_list = config_list[each_config][1]
                for each_disp in range(len(disp_list)):
                    ##
                    # Verify the CSC after applying each config
                    if csc_utility.verify_degamma_csc_gamma_blocks(self.matrix_info, disp_list[each_disp], self.csc_type):
                        logging.info("Register level verification is SUCCESS after display switch event")
                    else:
                        logging.info("Register level verification FAILED after display switch event")

            else:
                logging.error("Failed to apply display configuration on %s on %s"%(config_list[each_config][0],
                                                        config_list[each_config][1]))
                self.fail("Failed to apply display configuration")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
