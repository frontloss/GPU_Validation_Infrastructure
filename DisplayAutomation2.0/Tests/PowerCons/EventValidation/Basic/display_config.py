########################################################################################################################
# @file         display_config.py
# @details      @ref display_config.py <br>
#               This file implements display config scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################
from Libs.Core import enum
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env import test_environment

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests to verify features with display config scenario
class DisplayConfig(EventValidationBase):
    ##
    # @brief        This function verifies display config with various combinations of display modes
    # @return       None
    def test_display_config(self):

        self.lfp_panels = []
        self.external_panels = []
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    self.lfp_panels.append(panel.port)
                else:
                    self.external_panels.append(panel.port)

        disp_config_flow = [[enum.SINGLE, self.external_panels[0]],
                            [enum.EXTENDED, self.lfp_panels[0], self.external_panels[0]],
                            [enum.SINGLE, self.lfp_panels[0]],
                            [enum.EXTENDED, self.external_panels[0], self.lfp_panels[0]],
                            [enum.CLONE, self.lfp_panels[0], self.external_panels[0]],
                            [enum.SINGLE, self.external_panels[0]],
                            [enum.CLONE, self.external_panels[0], self.lfp_panels[0]],
                            [enum.SINGLE, self.lfp_panels[0]]]
        if len(self.lfp_panels) > 1:
            disp_config_flow = [[enum.SINGLE, self.external_panels[0]],
                                [enum.EXTENDED, self.lfp_panels[0], self.lfp_panels[1]],
                                [enum.EXTENDED, self.external_panels[0], self.lfp_panels[1], self.lfp_panels[0]],
                                [enum.SINGLE, self.lfp_panels[0]],
                                [enum.CLONE, self.lfp_panels[0], self.lfp_panels[1]],
                                [enum.SINGLE, self.external_panels[0]],
                                [enum.CLONE, self.lfp_panels[0], self.lfp_panels[1], self.external_panels[0]],
                                [enum.SINGLE, self.lfp_panels[0]]]

        for disp_conf in disp_config_flow:
            logging.info("Step: Setting display configuration {0} {1}".format(
                DisplayConfigTopology(disp_conf[0]).name, ' '.join(disp_conf[1:])))
            if self.display_config_.set_display_configuration_ex(disp_conf[0], disp_conf[1:]) is False:
                self.fail("Failed to set display configuration {0} {1} (Test Issue)".format(
                    DisplayConfigTopology(disp_conf[0]).name, ' '.join(disp_conf[1:])))
            logging.info("\tSet display configuration successfully")

            logging.info("Waiting for 15 seconds..")
            time.sleep(15)

        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
