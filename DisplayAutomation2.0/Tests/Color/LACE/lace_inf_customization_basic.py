#######################################################################################################################
# @file         lace_min_max_inf_customization.py
# @addtogroup   Test_Color
# @section      lace_min_max_inf_customization
# @remarks      @ref lace_min_max_inf_customization.py \n
#               The test script is developed with an intent to perform validation for the RCR VSRI- and VSRI-4900 on TGL.
#               The RCR enables OEMs to customize min ambient light LUX input for LACE to kick-in instead of the hardcoded 1000nits
#               This customization, done through Driver INF,is applicable to all three Aggressiveness levels.
#
#               The "Min" value is the minimum Lux input for LACE to kick-in.
#               Registry keys to configure the "Min" value for different aggressiveness levels are :
#                   "LaceMinLuxForLowAggressiveness"
#                   "LaceMinLuxForModerateAggressiveness"
#                   "LaceMinLuxForHighAggressiveness"
#
#               The "Max" value is the maximum Lux input after which Driver does not perform any further contrast enhancement.
#               Max value is a 32Bit max value : 4294967295
#               Registry key to configure the "Max" value is:
#                   "LaceMaxLuxValue"
#               Test script invokes Driver PCEscape call to enable LACE with Lux and Aggressiveness Levels and with the registry keys
#               If the registry key customization is not there, then driver will fall back to the default T0,T1,T2 values
#               Register verification is performed to verify if LACE is enabled/disabled appropriately.
#               Test case is developed in a generic way such that it can be extended to Dual LFP scenarios as well.
# CommandLine:  python lace_min_max_inf_customization.py -edp_a
#               python lace_min_max_inf_customization.py -mipi_a
# @author       Smitha B
#######################################################################################################################
from Tests.Color.LACE.lace_base import *


class LACEMinMaxINFCustomization(LACEBase):
    def runTest(self):
        ##
        # Preparing a list of INF Customization
        min_lux_customization_list = [("LaceMinLuxForLowAggressiveness", 300),
                                      ("LaceMinLuxForModerateAggressiveness", 600),
                                      ("LaceMinLuxForHighAggressiveness", 750)]

        ##
        # Preparing a list of (Lux, Aggr_level) to verify LACE ENABLE/DISABLE appropriately as per the INF Customization
        aggr_lux_combo_list = [(301, enum.AGGR_LEVEL_LOW), (601, enum.AGGR_LEVEL_MODERATE),
                               (1501, enum.AGGR_LEVEL_HIGH), (250, enum.AGGR_LEVEL_LOW), (500, enum.AGGR_LEVEL_MODERATE),
                               (749, enum.AGGR_LEVEL_HIGH) ]

        ##
        # Iterate through all the active LFPs to write the registry key for customization
        for index in range(len(self.lfp_target_ids)):
            for min_lux in range(len(min_lux_customization_list)):
                if not perform_registry_customization(min_lux_customization_list[min_lux]):
                    logging.error("Failed to set Registry_Key %s for Lux %s" % (
                        min_lux_customization_list[min_lux][0], min_lux_customization_list[min_lux][1]))
                    self.fail()
                else:
                    logging.info("Successfully set Registry_Key %s for Lux %s" % (
                    min_lux_customization_list[min_lux][0], min_lux_customization_list[min_lux][1]))

                    ##
                    # Set the (lux, aggr_level) through driver escape
                    for aggr_lux_index in range(len(aggr_lux_combo_list)):
                        lux = aggr_lux_combo_list[aggr_lux_index][0]
                        aggressiveness_level = aggr_lux_combo_list[aggr_lux_index][1]
                        logging.info("Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))

                        if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[index],
                                                                           lux=lux,
                                                                           lux_operation=True,
                                                                           aggressiveness_level=aggressiveness_level,
                                                                           aggressiveness_operation=True):

                            logging.info("Lux and aggressiveness levels set successfully")

                            logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
                            if self.underrun.verify_underrun():
                                logging.error("Underrun Occured")

                            current_pipe = get_current_pipe(self.connected_list[index])
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
                                self.fail()
                        else:
                            logging.error("Failed to set lux and aggressiveness levels")
                            logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                            self.fail("Failed to set lux and aggressiveness levels")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
