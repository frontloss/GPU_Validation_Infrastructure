########################################################################################################################
# @file          virtual_display_hotplug_unplug.py
# @brief         The script enables/disable virtual display by writing in to registry, restart the drivers,
#                removes all the internal display obtained from the display list.
#                * Remove all the displays from the setup phase and verify virtual displays.
#                * Get the connected display list and apply the display configuration obtained from the command line, verifies virtual displays.
# @author        Suraj Gaikwad, Sridharan.V
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.virtual_display_base import *

##
# @brief    It contains unitest runTest function to verify virtual displays
class VirtualDisplayHotplugUnplug(VirtualDisplayBase):

    ##
    # @brief        Unittest runTest function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def runTest(self):

        # Enable and verify virtual displays
        self.enable_disable_virtual_display()

        internal_display = None
        internal_display_list = self.display_config.get_internal_display_list(self.enumerated_displays)
        if len(internal_display_list) != 0:
            for i in range(len(internal_display_list)):
                internal_display = internal_display_list[i][1]
                break
        else:
            logging.error("Internal display interface EDP or MIPI not enumerated")
            self.fail()

        # Remove Internal display from display list
        self.displays_list.remove(internal_display)

        # Remove all the displays plugged during setup phase
        for external_display in self.displays_list:
            logging.info("Trying to unplug %s", external_display)
            if display_utility.unplug(external_display) is False:
                self.fail("Failed to unplug display %s" % external_display)
            self.enumerated_displays_before_adding_vd -= 1
            self.plugged_display.remove(external_display)

        # Verify virtual displays
        if self.verify_virtual_display() is False:
            self.fail('Failed to verify virtual displays')
        logging.info('Successfully verified virtual displays. Virtual displays count : %s'
                     % self.number_virtual_displays)

        # Connected displays list; used for applying display configurations
        config_display_list = [internal_display]

        for display in self.displays_list:

            # Plug the display and apply the configuration
            if display_utility.plug_display(display, self.cmd_line_param, False) is False:
                self.fail('Plugging of display %s was unsuccessful' % display)
            self.enumerated_displays_before_adding_vd += 1

            # Maintaining plugged_display list for unplugging displays in tearDown, in case of test failure
            self.plugged_display.append(display)
            config_display_list.append(display)

            # Set the display config as provided in command line
            topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
            if self.display_config.set_display_configuration_ex(topology, config_display_list) is False:
                self.fail('Failed to apply display configuration %s %s' %
                          (DisplayConfigTopology(topology).name, config_display_list))

            logging.info('Successfully applied the display configuration as %s %s' %
                         (DisplayConfigTopology(topology).name, config_display_list))

            # Verify virtual displays
            if self.verify_virtual_display() is False:
                self.fail('Failed to verify virtual displays')
            logging.info('Successfully verified virtual displays. Virtual displays count : %s'
                         % self.number_virtual_displays)

            # Unplug the display
            if display_utility.unplug(display) is False:
                self.fail("Failed to unplug display")
            self.enumerated_displays_before_adding_vd -= 1

            # Maintaining plugged_display list for unplugging displays in tearDown, in case of test failure
            self.plugged_display.remove(display)
            config_display_list.remove(display)

            # Apply Single display configuration
            if self.display_config.set_display_configuration_ex(enum.SINGLE, config_display_list) is False:
                self.fail('Failed to apply display configuration %s %s' %
                          (DisplayConfigTopology(topology).name, config_display_list))

            logging.info('Successfully applied the display configuration as %s %s' %
                         (DisplayConfigTopology(topology).name, config_display_list))

            # Verify virtual displays
            if self.verify_virtual_display() is False:
                self.fail('Failed to verify virtual displays')
            logging.info('Successfully verified virtual displays. Virtual displays count : %s'
                         % self.number_virtual_displays)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
