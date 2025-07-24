########################################################################################################################
# @file         virtual_display_s3.py
# @brief        The script enables/disable virtual display by writing in to registry, restart the drivers and verifies
#               below.
#               * Verifies whether the system is Non-CS/CS and apply the display configuration obtained from the command
#                 line.
#               * Verifies virtual display before and after sleep event.
# @author       Suraj Gaikwad, Sridharan.V
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.display_power import PowerEvent
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.virtual_display_base import *

##
# @brief     It contains unitest runTest function to verify virtual displays after entering and resuming from S3
class VirtualDisplayS3(VirtualDisplayBase):
    ##
    # @brief        Unittest runTest function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def runTest(self):

        # Enable and verify virtual displays
        self.enable_disable_virtual_display()

        # Verify CS/Non-CS system
        if self.display_power.is_power_state_supported(PowerEvent.CS) is not self.cs_system_expected:
            self.fail("System configuration as CS = %s was not expected" % (not self.cs_system_expected))

        # Set the display config as provided in command line
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.displays_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.displays_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.displays_list))

        # Verify virtual displays before sleep event
        if self.verify_virtual_display() is False:
            self.fail('Failed to verify virtual displays before sleep event')
        logging.info('Successfully verified virtual displays before sleep event. Virtual displays count : %s'
                     % self.number_virtual_displays)

        # Invoke Sleep State
        result = self.display_power.invoke_power_event(self.power_event, POWER_EVENT_DURATION)
        self.assertEquals(result, True,
                          'Failed to invoke power event %s' % self.power_event.name)

        # Verify virtual displays after sleep event
        if self.verify_virtual_display() is False:
            self.fail('Failed to verify virtual displays after sleep event')
        logging.info('Successfully verified virtual displays after sleep event. Virtual displays count : %s'
                     % self.number_virtual_displays)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
