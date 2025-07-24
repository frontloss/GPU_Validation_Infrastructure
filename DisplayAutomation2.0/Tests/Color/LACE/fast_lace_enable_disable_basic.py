#######################################################################################################################
# @file         fast_lace_enable_disable_basic.py
# @addtogroup   Test_Color
# @section      fast_lace_enable_disable_basic
# @remarks      @ref fast_lace_enable_disable_basic.py \n
#               The test script invokes Driver PCEscape call to enable LACE using Lux .
#               Register verification is performed to verify if LACE is enabled/disabled appropriately.
# @author       Soorya R, Smitha B
#######################################################################################################################
from Tests.Color.LACE.lace_base import *


class LACEEnableDisableBasic(LACEBase):

    def runTest(self):

        # LACE enable
        lux_val = 1500
        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[0], lux=lux_val,
                                                           lux_operation=True):
            logging.info(" Als Lux override set successfully - Lux : %d" % lux_val)

        for index in range(len(self.lfp_target_ids)):
            time.sleep(2)  # For PartA and PartB histogram load and IE programming completion
            if not verify_lace_register_programming(self.lfp_pipe_ids[index], self.lfp_target_ids[index], lux_val):
                self.fail("Verify FastLACE register programming failed for LACE Enable !!")

        # LACE disable
        lux_val = 250
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
