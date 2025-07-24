#######################################################################################################################
# @file         lace_aggrlevel_stress.py
# @addtogroup   Test_Color
# @section      lace_aggrlevel_stress
# @remarks      @ref lace_aggrlevel_stress.py \n
#               The test script performs the driver PCEscape call to enable LACE using Lux and Aggressiveness levels
#               in a stress scenario.
#               Register verification is performed to verify if LACE is enabled/disabled appropriately.
# CommandLine:  python lace_aggrlevel_stress.py -edp_a
# @author       Smitha B
#######################################################################################################################
import random
import time
from Tests.Color.LACE.lace_base import *


class LACEAggressivenessLevelStress(LACEBase):

    def runTest(self):
        current_pipe = get_current_pipe(self.connected_list[0])
        self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
        
        is_lfp = False

        # Check if panel is lfp
        if display_utility.get_vbt_panel_type(self.connected_list[0], 'gfx_0') in \
                [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
            is_lfp = True

        if is_lfp is True:
            if self.check_primary_display(self.connected_list[0]):

                for i in range(0, 50):
                    status = self.enable_pwrcons_feature()
                    if status is False:
                        self.fail("Failed to Enable Lace in pc feature state")
                    lux = random.randint(4000, 15000)
                    aggressiveness_level = enum.AGGR_LEVEL_MODERATE
                    logging.info("Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))

                    if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.target_id, lux=lux,
                                                                       lux_operation=True,
                                                                       aggressiveness_level=aggressiveness_level    ,
                                                                       aggressiveness_operation=True):

                        logging.info("Lux and aggressiveness levels set successfully")
                        logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
                        time.sleep(2)
                        if self.underrun.verify_underrun():
                            logging.error("Underrun Occured")

                        self.expected_lace_status = get_expected_lace_status(lux, aggressiveness_level)
                        self.actual_lace_status = get_actual_lace_status(current_pipe)

                        if self.expected_lace_status == self.actual_lace_status:
                            logging.info(
                                "Expected : LACE %s; Actual : LACE %s" % (self.expected_lace_status, self.actual_lace_status))
                            logging.info("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                        else:
                            logging.error(
                                "Expected : LACE %s; Actual : LACE %s" % (self.expected_lace_status, self.actual_lace_status))
                            logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                            self.fail()
                    else:
                        logging.error("Escape call to set lux and aggressiveness level failed")
                        logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                        self.fail("Escape call to set lux and aggressiveness level failed")

            # Lace should not be enabled for 2nd LFP which is not set as primary
            else:
                logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
                if self.underrun.verify_underrun():
                    logging.error("Underrun Occured")
                time.sleep(2)

                if get_actual_lace_status(current_pipe) == "DISABLED":
                    logging.info("Expectation : LACE %s; Actual : LACE %s" % (
                        "DISABLED", get_actual_lace_status(current_pipe)))
                else:
                    logging.error("Expectation : LACE %s; Actual : LACE %s" % (
                        "ENABLED", get_actual_lace_status(current_pipe)))
                    self.fail("LACE is enabled on Pipe_{0}".format(current_pipe))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
