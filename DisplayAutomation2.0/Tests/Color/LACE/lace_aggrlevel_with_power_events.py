#######################################################################################################################
# @file         lace_aggrlevel_with_power_events.py
# @addtogroup   Test_Color
# @section      lace_aggrlevel_with_power_events
# @remarks      @ref lace_aggrlevel_with_power_events.py \n
#               The test script performs the driver PCEscape call to enable LACE using Lux and Aggressiveness levels
#               Test verifies persistence of LACE with power events scenarios.
# CommandLine:  python lace_aggrlevel_with_power_events.py -edp_a
# @author       Smitha B
#######################################################################################################################
import random
from Libs.Core import display_power
from Tests.Color.LACE.lace_base import *

class LACEAggrLevelWithPowerEvents(LACEBase):

    def test_before_reboot(self):
        current_pipe = get_current_pipe(self.connected_list[0])

        lux = random.randint(1000, 15000)
        aggressiveness_level = 1
        self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
        power_states_list = [display_power.PowerEvent.S3, display_power.PowerEvent.S4, display_power.PowerEvent.S5]

        for index in range(len(power_states_list)):
            if power_states_list[index] == display_power.PowerEvent.S5:
                if reboot_helper.reboot(self, 'test_after_reboot') is False:
                    self.fail("Failed to reboot the system")

            if self.display_power.invoke_power_event(power_states_list[index], 60):
                status = self.enable_pwrcons_feature()
                if status is False:
                    self.fail("Failed to Enable Lace in pc feature state")

                logging.info(
                    "Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))
                if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.target_id, lux=lux,
                                                                   lux_operation=True,
                                                                   aggressiveness_level=aggressiveness_level,
                                                                   aggressiveness_operation=True):

                    logging.info("Lux and aggressiveness levels set successfully")
                    logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
                    if self.underrun.verify_underrun():
                        logging.error("Underrun Occured")

                    self.actual_lace_status = get_actual_lace_status(current_pipe)
                    self.expected_lace_status = get_expected_lace_status(lux, aggressiveness_level)

                    if self.expected_lace_status == self.actual_lace_status:
                        logging.info("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                        logging.info("Expectation : LACE %s; Actual : LACE %s" % (
                            self.expected_lace_status, self.actual_lace_status))
                    else:
                        logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                        logging.error("Expectation : LACE %s; Actual : LACE %s" % (
                            self.expected_lace_status, self.actual_lace_status))
                        self.fail("LACE is not enabled")
                else:
                    logging.error("Failed to set lux and aggressiveness levels")
                    logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                    self.fail("Failed to set lux and aggressiveness levels")

            else:
                logging.info("Power Event: Failed")

    def test_after_reboot(self):
        logging.info("Test after Reboot")

        current_pipe = get_current_pipe(self.connected_list[0])

        self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        ##
        # Read the aggressiveness Level from registry - Driver saves it even after S5 event
        reg_value, reg_type = registry_access.read(args=reg_args, reg_name="LaceCUIAggressivenessLevel")
        if registry_access.RegDataType(reg_type).name == "BINARY":
            aggressiveness_level = int.from_bytes(reg_value, byteorder="little")
        else:
            aggressiveness_level = reg_value
        lux = 1000
        status = self.enable_pwrcons_feature()
        if status is False:
            self.fail("Failed to Enable Lace in pc feature state")

        logging.info("Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))
        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.target_id, lux=lux,
                                                           lux_operation=True,
                                                           aggressiveness_level=aggressiveness_level,
                                                           aggressiveness_operation=True):

            logging.info("Lux and aggressiveness levels set successfully")
            logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
            if self.underrun.verify_underrun():
                logging.error("Underrun Occured")

            self.actual_lace_status = get_actual_lace_status(current_pipe)
            self.expected_lace_status = get_expected_lace_status(lux, aggressiveness_level)

            if self.expected_lace_status == self.actual_lace_status:
                logging.info("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                logging.info("Expectation : LACE %s; Actual : LACE %s" % (
                    self.expected_lace_status, self.actual_lace_status))
            else:
                logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                logging.error("Expectation : LACE %s; Actual : LACE %s" % (
                    self.expected_lace_status, self.actual_lace_status))
                self.fail("LACE is not enabled")
        else:
            logging.error("Failed to set lux and aggressiveness levels")
            logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
            self.fail("Failed to set lux and aggressiveness levels")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('LACEAggrLevelWithPowerEvents'))
    TestEnvironment.cleanup(outcome)
