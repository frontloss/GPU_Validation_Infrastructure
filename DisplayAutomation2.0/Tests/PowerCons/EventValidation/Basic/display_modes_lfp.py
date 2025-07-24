########################################################################################################################
# @file         display_modes_lfp.py
# @details      @ref display_modes_lfp.py <br>
#               This file implements display modes lfp scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests for events with display modes with LFP
class DisplayModesLfp(EventValidationBase):
    ##
    # @brief        This function verifies the features with display mode scenario in LFP
    # @return       None
    def test_display_modes_lfp(self):

        # Apply supported modes on all active lfp
        disp_mode_failed = False
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                mode_list = []
                rr_list = common.get_supported_refresh_rates(panel.target_id)
                if len(rr_list) > 1:
                    for rr in rr_list:
                        mode_list.append(common.get_display_mode(panel.target_id, rr))
                else:
                    mode_list = common.get_display_mode(panel.target_id, limit=2)

                for mode in mode_list:
                    logging.info("Step: Applying mode for {0} = {1}".format(panel.port, mode.to_string(enumerated_displays)))
                    if self.display_config_.set_display_mode([mode], False) is False:
                        logging.error("\tFailed to apply display mode")
                        disp_mode_failed = True
                        continue
                    logging.info("\tApplied display mode successfully")

                    logging.info("Waiting for 15 seconds..")
                    time.sleep(15)

            if disp_mode_failed is True:
                self.fail("Failed to apply display mode (Test Issue)")

            self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
