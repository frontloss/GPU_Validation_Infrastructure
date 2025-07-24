########################################################################################################################
# @file          virtual_display_basic.py
# @brief         The basic test scenario involves enable/disable virtual display by writing in to registry and verification of 
#                     virtual display.
# @author        Suraj Gaikwad, Sridharan.v
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.virtual_display_base import *

##
# @brief     It contains unitest runTest function to verify virtual displays
class VirtualDisplayBasic(VirtualDisplayBase):

    ##
    # @brief        Unittest runTest function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def runTest(self):


        # Enable and verify virtual displays
        self.enable_disable_virtual_display()


        # Set the display config as provided in command line
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.displays_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.displays_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.displays_list))

        # Verify virtual displays
        if self.verify_virtual_display() is False:
            self.fail('Failed to verify virtual displays')
        logging.info('Successfully verified virtual displays. Virtual displays count : %s'
                     % self.number_virtual_displays)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
