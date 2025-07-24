###################################################################################################
# @file         lace_aggrlevel_with_display_switching.py
# @addtogroup   Test_Color
# @section      lace_aggrlevel_with_display_switching
# @remarks      @ref lace_aggrlevel_with_display_switching.py \n
#               The test script performs the driver PCEscape call to enable LACE using Lux and
#               Aggressiveness levels
#               Test verifies persistence of LACE with display switching scenarios.
# CommandLine:  python lace_aggrlevel_with_display_switching.py -edp_a -hdmi_b
# @author       Smitha B
###################################################################################################
from Tests.Color.LACE.lace_base import *


class LACEAggrLevelWithDisplaySwitching(LACEBase):

    def runTest(self):
        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE
        lux = 0
        aggressiveness_level = 0

        ##
        # Apply SINGLE display configuration
        if self.config.set_display_configuration_ex(topology, [self.connected_list[0]]) is True:
            logging.info("Successfully applied SINGLE DISPLAY configuration")
            time.sleep(2)
            lux = 20000
            aggressiveness_level = 1
            
            current_pipe = get_current_pipe(self.connected_list[0])
            self.target_id = self.config.get_target_id(self.connected_list[0], self.enumerated_displays)
            
            is_lfp = False
            # Check if panel is lfp
            if display_utility.get_vbt_panel_type(self.connected_list[0], 'gfx_0') in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                is_lfp = True
            
            if is_lfp is True:
                if self.check_primary_display(self.connected_list[0]):
                    logging.info("Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))
                    if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.target_id, lux=lux,
                                                                       lux_operation=True,
                                                                       aggressiveness_level=aggressiveness_level,
                                                                       aggressiveness_operation=True):

                        logging.info("Lux and aggressiveness levels set successfully")
                        logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
                        if self.underrun.verify_underrun():
                            logging.error("Underrun Occured")
                        time.sleep(2)

                        current_pipe = get_current_pipe(self.connected_list[0])
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
                    
        ##
        # Apply DDC
        # Expectation : LACE will be enabled on eDP only.
        topology = enum.CLONE
        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied CLONE DISPLAY configuration on %s" % self.connected_list)
            time.sleep(2)

            for index in range(len(self.connected_list)):
                ##
                # This check has been added to handle Dual eDP/Mipi scenarios where LACE is
                # expected to be enabled on both.
                if display_utility.get_vbt_panel_type(self.connected_list[index], 'gfx_0') in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                    current_pipe = get_current_pipe(self.connected_list[0])
                    self.actual_lace_status = get_actual_lace_status(current_pipe)
                    self.expected_lace_status = "ENABLED"
                    if self.expected_lace_status == self.actual_lace_status:
                        logging.info("LACE is ENABLED on LFP in DDC")
                        logging.info(
                            "Expectation : LACE %s; Actual : LACE %s" % (
                                self.expected_lace_status, self.actual_lace_status))
                    else:
                        logging.error(
                            "Expectation : LACE %s; Actual : LACE %s" % (
                                self.expected_lace_status, self.actual_lace_status))
                        logging.error("LACE is expected to be ENABLED on LFP in DDC")
                        self.fail("LACE is expected to be ENABLED on LFP in DDC")

        ##
        # Apply SD external display
        topology = enum.SINGLE
        if self.config.set_display_configuration_ex(topology, [self.connected_list[1]]) is True:
            logging.info("Successfully applied SINGLE display configuration on %s" % self.connected_list[1])
        else:
            logging.error("Failed to apply SINGLE display configuration on %s" % self.connected_list[1])

        ##
        # Switch back to SINGLE Display - LACE should get enabled
        # Expectation : LACE should persist after Display Switching.
        topology = enum.SINGLE
        if self.config.set_display_configuration_ex(topology, [self.connected_list[0]]) is True:
            logging.info("Successfully applied SINGLE DISPLAY configuration on %s" % self.connected_list[0])
            time.sleep(5)
            current_pipe = get_current_pipe(self.connected_list[0])

            self.actual_lace_status = get_actual_lace_status(current_pipe)
            self.expected_lace_status = get_expected_lace_status(lux, aggressiveness_level)
            if self.expected_lace_status == self.actual_lace_status:
                logging.info(
                    "Expectation : LACE %s; Actual : LACE %s" % (self.expected_lace_status, self.actual_lace_status))
            else:
                logging.error("LACE is expected to be ENABLED after switching back to SD configuration")
                logging.error(
                    "Expectation : LACE %s; Actual : LACE %s" % (self.expected_lace_status, self.actual_lace_status))
                self.fail("LACE is expected to be ENABLED after switching back to SD configuration")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
