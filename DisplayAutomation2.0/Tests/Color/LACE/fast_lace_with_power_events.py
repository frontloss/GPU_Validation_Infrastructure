#######################################################################################################################
# @file         fast_lace_with_power_events.py
# @addtogroup   Test_Color
# @section      fast_lace_with_power_events
# @remarks      @ref fast_lace_with_power_events.py \n
#               The test script invokes Driver PCEscape call to enable LACE using Lux and invokes power events (S3/S4).
#               Register verification is performed to verify if LACE is enabled/disabled appropriately and its persistence .
# @author       Soorya R
#######################################################################################################################
from Libs.Core import display_power
from Tests.Color.LACE.lace_base import *

class LACEPowerEvents(LACEBase):

    def runTest(self):

        power_states_list = [display_power.PowerEvent.S3, display_power.PowerEvent.S4]
        # LACE enable
        lux_val = 1500
        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[0], lux=lux_val,
                                                           lux_operation=True):
            logging.info(" Als Lux override set successfully - Lux : %d" % lux_val)

        for index in range(len(self.lfp_target_ids)):
            time.sleep(2)  # For PartA and PartB histogram load and IE programming completion
            if not verify_lace_register_programming(self.lfp_pipe_ids[index], self.lfp_target_ids[index], lux_val):
                self.fail("Verify FastLACE register programming failed for LACE Enable !!")

        for index in range(len(power_states_list)):
            if self.display_power.invoke_power_event(power_states_list[index], 60):
                for index in range(len(self.lfp_target_ids)):
                    time.sleep(2)  # For PartA and PartB histogram load and IE programming completion
                    if not verify_lace_register_programming(self.lfp_pipe_ids[index], self.lfp_target_ids[index],
                                                                lux_val):
                        self.fail("Verify FastLACE register programming failed for LACE Enable !!")

        # LACE disable
        lux_val = 150
        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[0], lux=lux_val,
                                                           lux_operation=True):
            logging.info(" Als Lux override set successfully - Lux : %d" % lux_val)

        for index in range(len(self.lfp_target_ids)):
            time.sleep(2)  # For PartA and PartB histogram load and IE programming completion
            if not verify_lace_register_programming(self.lfp_pipe_ids[index], self.lfp_target_ids[index], lux_val):
                self.fail("Verify FastLACE register programming failed for LACE Disable !!")

        if self.underrun.verify_underrun():
            logging.error("Underrun Occured")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
