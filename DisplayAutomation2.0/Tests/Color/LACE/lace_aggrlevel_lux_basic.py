#######################################################################################################################
# @file         lace_aggrlevel_lux_basic.py
# @addtogroup   Test_Color
# @section      lace_aggrlevel_lux_basic
# @remarks      @ref lace_aggrlevel_lux_basic.py \n
#               The test script invokes Driver PCEscape call to enable LACE using Lux and Aggressiveness Levels.
#               Test script iterates through a list where the AggrLevel and the corresponding Lux value which enables
#               LACE is captured.
#               Register verification is performed to verify if LACE is enabled/disabled appropriately.
# CommandLine:  python lace_aggrlevel_lux_basic.py -edp_a
# @author       Smitha B
#######################################################################################################################
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Color.LACE.lace_base import *
import time


class LACEAggrLevelLuxBasic(LACEBase):

    def runTest(self):
        for panel_index in range(len(self.connected_list)):

            self.target_id = self.config.get_target_id(self.connected_list[panel_index], self.enumerated_displays)
            current_pipe = get_current_pipe(self.connected_list[panel_index])
            
            is_lfp = False
            # Check if panel is lfp
            if display_utility.get_vbt_panel_type(self.connected_list[panel_index], 'gfx_0') in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                is_lfp = True

            if is_lfp is True:
                if self.check_primary_display(self.connected_list[panel_index]):
                    ##
                    # Iterate through the basic lux-aggr_level threshold at which LACE is expected to get enabled.
                    aggr_lux_combo_list = [(3501, enum.AGGR_LEVEL_MODERATE), (10000, enum.AGGR_LEVEL_MODERATE),
                                           (25000, enum.AGGR_LEVEL_MODERATE)]

                    for index in range(len(aggr_lux_combo_list)):
                        lux = aggr_lux_combo_list[index][0]
                        aggressiveness_level = aggr_lux_combo_list[index][1]

                        logging.info("Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))

                        status = self.enable_pwrcons_feature()
                        if status is False:
                            self.fail("Failed to Enable Lace in pc feature state")

                        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.target_id, lux=lux,
                                                                           lux_operation=True,
                                                                           aggressiveness_level=aggressiveness_level,
                                                                           aggressiveness_operation=True):

                            logging.info("Lux and aggressiveness levels set successfully")
                            logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
                            if self.underrun.verify_underrun():
                                logging.error("Underrun Occured")
                            time.sleep(2)

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

                            logging.error("Expectation : LACE %s; Actual : LACE %s" % (
                                self.expected_lace_status, self.actual_lace_status))
                            self.fail("LACE is not enabled")

                        # Verify DSC Programming if DSC supported panel is connected
                        is_vdsc_panel = DSCHelper.is_vdsc_supported_in_panel("gfx_0", self.connected_list[panel_index])
                        if is_vdsc_panel is True:
                            is_success = dsc_verifier.verify_dsc_programming("gfx_0", self.connected_list[panel_index])
                            self.assertTrue(is_success, f"DSC Verification Failed for {self.connected_list[panel_index]}")
                            logging.info(f"DSC Verification Successful for {self.connected_list[panel_index]}")

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
                        self.fail("LACE is enabled on Pipe_{0}" .format(current_pipe))
                    

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
