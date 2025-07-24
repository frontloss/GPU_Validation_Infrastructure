########################################################################################################################
# @file           virtual_display_dynamic_add_remove.py
# @brief          The script inherits setup  from the base class, writes into display driver registry path to enable dynamic virtual displays,
#                 restarts display driver to make the changes to take place.
#                * Adds virtual displays dynamically and verifies; removes all the virtual display and verifies.
#                * The teardown phase reverts back the changes in the registries.
# @author         Suraj Gaikwad, Ankurkumar G Patel
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.VirtualDisplay.virtual_display_base import *

##
# @brief     It contains methods to verify dynamic addition and removal of virtual displays
class VirtualDisplayDynamicAddRemove(VirtualDisplayBase):

    ##
    # @brief        Unittest setUp function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def setUp(self):


        # Inherit setup from the base class
        super(VirtualDisplayDynamicAddRemove, self).setUp()


        # Write into display driver registry path to enable dynamic virtual displays
        registry_key = "NumberOfVirtualDisplays"
        value = self.number_virtual_displays

        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if registry_access.write(args=reg_args, reg_name=registry_key, reg_type=registry_access.RegDataType.DWORD,
                                 reg_value=value) is False:
            self.fail("Failed to write into registry with key %s and value %s" % (registry_key, value))
        logging.debug("Successfully written into registry with key %s and value %s" % (registry_key, value))

        registry_key = "EnableDynamicVirtualDisplaySupport"
        value = 1

        if registry_access.write(args=reg_args, reg_name=registry_key, reg_type=registry_access.RegDataType.DWORD,
                                 reg_value=value) is False:
            self.fail("Failed to write into registry with key %s and value %s" % (registry_key, value))
        logging.debug("Successfully written into registry with key %s and value %s" % (registry_key, value))


        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            logging.error('Under Run observed during test execution')


        # Restart display driver to make the changes to take place
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('Failed to restart driver after writing into registry')
        logging.debug('Display driver restarted successfully')


    ##
    # @brief         Unittest runTest function
    # @param[in]     self; Object of virtual display base class
    # @return        void
    def runTest(self):

        # Set the display config as provided in command line
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.displays_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.displays_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.displays_list))

        # Add virtual displays dynamically and verify
        for count in range(self.number_virtual_displays):
            self.dynamic_add_virtual_display()

        # Remove virtual displays dynamically and verify
        for count in range(self.number_virtual_displays):
            self.dynamic_remove_virtual_display()


    ##
    # @brief        Unittest tearDown function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def tearDown(self):

        # Revert back the changes in the registries
        # Write into display driver registry path to enable dynamic virtual displays
        registry_key = "EnableDynamicVirtualDisplaySupport"
        value = 0

        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if registry_access.write(args=reg_args, reg_name=registry_key, reg_type=registry_access.RegDataType.DWORD,
                                 reg_value=value) is False:
            self.fail("Failed to write into registry with key %s and value %s" % (registry_key, value))
        logging.debug("Successfully written into registry with key %s and value %s" % (registry_key, value))

        # Inherit tearDown from the base class
        super(VirtualDisplayDynamicAddRemove, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    suite = unittest.TestLoader().loadTestsFromTestCase(VirtualDisplayDynamicAddRemove)
    result = unittest.TextTestRunner().run(suite)
    TestEnvironment.cleanup(result)
