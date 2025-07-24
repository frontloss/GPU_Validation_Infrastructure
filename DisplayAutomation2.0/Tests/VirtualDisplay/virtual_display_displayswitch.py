########################################################################################################################
# @file            virtual_display_displayswitch.py
# @brief           The script  enables/disable virtual display by writing in to registry,
#                  restart the drivers and verifies virtual display.If display_list contains less than 2 displays then the test fails.
# @author          Suraj Gaikwad, Sridharan.v
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.virtual_display_base import *

##
# @brief     It contains unitest runTest function to verify virtual displays in various display configurations
class VirtualDisplayDisplaySwitch(VirtualDisplayBase):

    ##
    # @brief        Unittest runTest function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def runTest(self):

        # Enable and verify virtual displays
        self.enable_disable_virtual_display()

        if len(self.displays_list) == 1:
            self.fail("Display Switch testcase requires minimum 2 displays")

        # Enable and verify virtual displays
        self.enable_disable_virtual_display()

        config_list = display_utility.get_possible_configs(self.displays_list)

        for config, display_list in config_list.items():
            topology = eval("%s" % config)
            for displays in display_list:
                time.sleep(30)
                if self.display_config.set_display_configuration_ex(topology, displays) is False:
                    self.fail('Failed to apply display configuration %s %s' %
                              (DisplayConfigTopology(topology).name, displays))
                logging.info('Successfully applied the display configuration as %s %s' %
                             (DisplayConfigTopology(topology).name, displays))

                # Verify virtual displays
                if self.verify_virtual_display() is False:
                    self.fail('Failed to verify virtual displays')
                logging.info('Successfully verified virtual displays. Virtual displays count : %s'
                             % self.number_virtual_displays)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
