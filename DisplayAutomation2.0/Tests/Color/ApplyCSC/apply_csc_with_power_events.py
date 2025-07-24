#######################################################################################################################
# @file         apply_csc_with_power_events.py
# @addtogroup   Test_Color
# @section      apply_csc_with_power_events
# @remarks      @ref lace_aggrlevel_with_power_events.py \n
#               The test script invokes Driver Escape call to any CSC
#               taking the csc client(Linear\Non-Linear) from the command line along with
#               the matrix also provided as part of command line among the matrices stored in the input_csc_matrix JSON file
#               Test verifies persistence of the applied CSC with power events scenarios(S3-S4-S5)
# CommandLine:  python apply_csc_with_power_events.py -edp_a
# @author       Smitha B
#######################################################################################################################
from Libs.Core import display_power, enum
from Tests.Color.ApplyCSC.apply_csc_base import *


class ApplyCSCWithPowerEvents(ApplyCSCBase):

    def test_before_reboot(self):
        csc_params = csc_utility.create_15_16_format_csc_matrix(deepcopy(self.matrix_info))
        params = CSCPipeMatrixParams(1, csc_params)

        for display_index in range(self.enumerated_displays.Count):
            display = str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            if display in self.connected_list and \
                        self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:

                if driver_escape.apply_csc(
                        self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                        enum.OPERATION_SET, self.csc_type, params) is False:
                    logging.error("Failed to apply CSC")
                    self.fail("Failed to apply CSC")
                else:
                    logging.info("Successfully applied %s CSC after completion of the test" % CSC_MATRIX_TYPE(
                        self.csc_type).name)

                    ##
                    # Verify the CSC
                    if csc_utility.verify_degamma_csc_gamma_blocks(self.matrix_info, display,
                                                                self.csc_type):
                        logging.info("Register level verification is SUCCESS")
                    else:
                        logging.error("Register level verification is FAILED")
                        self.fail("Register level verification is FAILED")

        ##
        # Preparing a list of power states
        power_states_list = [display_power.PowerEvent.S3, display_power.PowerEvent.S4, display_power.PowerEvent.S5]

        for index in range(len(power_states_list)):
            if power_states_list[index] == display_power.PowerEvent.S5:
                if reboot_helper.reboot(self, 'test_after_reboot') is False:
                    self.fail("Failed to reboot the system")

            if display_power.DisplayPower().invoke_power_event(power_states_list[index], 60):
                logging.info("POWER_STATE event %s SUCCESSFUL" % power_states_list[index].name)
                ##
                # Verify if the applied CSC is persisting
                for display_index in range(0, len(self.connected_list)):
                    ##
                    # Verify the CSC
                    if csc_utility.verify_degamma_csc_gamma_blocks(self.matrix_info, self.connected_list[display_index],
                                                                self.csc_type):
                        logging.info("Register level verification is SUCCESS")
                    else:
                        logging.error("Register level verification is FAILED")
                        self.fail("Register level verification is FAILED")
            else:
                logging.info("POWER_STATE event %s FAILED" % power_states_list[index].name)

    def test_after_reboot(self):
        for display_index in range(0, len(self.connected_list)):
            ##
            # Verify the CSC
            if csc_utility.verify_degamma_csc_gamma_blocks(self.matrix_info, self.connected_list[display_index],
                                                        self.csc_type):
                logging.info("Register level verification is SUCCESS")
            else:
                logging.error("Register level verification is FAILED")
                self.fail("Register level verification is FAILED")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.runner.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ApplyCSCWithPowerEvents'))
    TestEnvironment.cleanup(outcome)
