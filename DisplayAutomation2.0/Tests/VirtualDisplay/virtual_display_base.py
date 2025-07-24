########################################################################################################################
# @file           virtual_display_base.py
# @brief          The script accepts number of virtual displays  from the command line.
#                 The following tests can be done along  with the unittest setup and teardown function.
#                 * Verifies whether the virtual display is enabled or not.
#                 * Enables/Disable virtual display by writing in to registry, restart the driver and verify.
#                 * Dynamically adds/removes  a virtual display with default EDID and updates the virtual id list.
#                 * Checks whether the displays can be plugged and unplugged in low power state or not.
# @author         Suraj Gaikwad, Sridharan.v, Ankurkumar G Patel
# @todo Add proper mechanism for Virtual Display verification (Needs system utility display enumeration update for enumerating virtual displays)
########################################################################################################################

import logging
import sys
import time
import unittest

import win32com.client

from Libs.Core import cmd_parser, enum, registry_access, display_essential
from Libs.Core import display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower, PowerEvent
from Libs.Core.logger import gdhm
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

POWER_EVENT_DURATION = 60
DISPLAY_VIRTUAL_SUCCESS = 0x00000000

##
# @brief    Virtual Display base class for virtual display legacy tests
class VirtualDisplayBase(unittest.TestCase):
    enumerated_displays = None
    displays_list = list()
    plugged_display = list()
    power_event = PowerEvent.S3
    cs_system_expected = False
    number_virtual_displays = 3  # Default number of Virtual Displays to enumerate (if not provided as cmd args)
    custom_tags = ['-virtual_displays']
    virtual_display_ids = list()  # List to store virtual display ids globally for dynamic add/remove
    enumerated_displays_before_adding_vd = None

    display_config = DisplayConfiguration()
    display_power = DisplayPower()
    under_run_status = UnderRunStatus()

    ##
    # @brief        Unittest Setup function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def setUp(self):

        try:
            self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

            for key, value in self.cmd_line_param.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        self.displays_list.insert(value['index'], value['connector_port'])


            # Fetch number of virtual displays from command line (if provided)
            if self.cmd_line_param['VIRTUAL_DISPLAYS'] != 'NONE':
                self.number_virtual_displays = int(self.cmd_line_param['VIRTUAL_DISPLAYS'][0])
                logging.debug('Number of virtual displays provided via the command-line is : %s'
                              % self.number_virtual_displays)
            else:
                logging.debug('Value for number of virtual displays not provided in command-line. '
                              'Using the default value as : %s' % self.number_virtual_displays)

            if not 0 <= self.number_virtual_displays <= 8:
                self.fail('Invalid number of virtual displays provided')


            # Verify and plug the display
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
            logging.info('Plugged displays list : %s' % self.plugged_display)

            for count in range(len(self.displays_list)):
                is_display_found = False
                for index in range(self.enumerated_displays.Count):
                    if self.displays_list[count] == CONNECTOR_PORT_TYPE(
                            self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name:
                        is_display_found = True

                if is_display_found is False:
                    self.fail("Display %s is not plugged correctly" % self.displays_list[count])


            # Set the display config as SINGLE of the first display in command line
            if self.display_config.set_display_configuration_ex(enum.SINGLE,
                                                                [self.displays_list[0]],
                                                                self.enumerated_displays) is False:
                self.fail('Failed to set display configuration as SINGLE %s' % self.displays_list[0])
            logging.info('Successfully set the display configuration as SINGLE %s' % self.displays_list[0])

            self.enumerated_displays_before_adding_vd = self.display_config.get_enumerated_display_info().Count

        except Exception as e:

            # If any Exception happens: Call teardown and fail the test
            self.tearDown()
            self.fail(e)

    ##
    # @brief        Verifies if virtual displays are enabled properly, based on number of displays present in all configurations
    # @param[in]    self; Object of virtual display base class
    # @return       Bool; True, if verification is successful; False, otherwise
    def verify_virtual_display(self):

        # Restart display driver to make the changes to take place
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('Failed to restart driver after writing into registry')
        logging.debug('Display driver restarted successfully')

        # Get number of displays in all display configuration after adding virtual displays
        # (physical_displays + simulated_displays + virtual_displays)
        enumerated_displays_after_adding_vd = self.display_config.get_enumerated_display_info().Count

        logging.debug(
            'Number of enumerated displyas after adding Virtual displays is %s' % enumerated_displays_after_adding_vd)
        logging.debug(
            'Number of enumerated displyas before adding Virtual displays is %s' % self.enumerated_displays_before_adding_vd)
        logging.debug('Number of virtual displays present is %s' % self.number_virtual_displays)

        # Number of all enumerated displays after adding virtual displays should be equal to the number of virtual displays
        # + number of enumerated displays before adding virtual displays
        if enumerated_displays_after_adding_vd == (
                self.enumerated_displays_before_adding_vd + self.number_virtual_displays):
            return True
        gdhm.report_bug(
            title="[VirtualDisplay] Failed to enable virtual display ",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E3
        )
        logging.error('Failed to enable virtual display')
        return False

    ##
    # @brief       Enable/Disable virtual display by writing into registry and verify number of virtual display.
    #              Uses number_virtual_display variable to enable/disable number of virtual display.
    # @param[in]   self; Object of virtual display base class
    # @return      Bool; True, if enabling is successful
    def enable_disable_virtual_display(self):

        if self.number_virtual_displays < 0:
            self.fail('Number of virtual displays should be a positive integer')


        # Write into display driver registry path to enable virtual displays
        registry_key = "NumberOfVirtualDisplays"
        value = self.number_virtual_displays

        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if registry_access.write(args=reg_args, reg_name=registry_key, reg_type=registry_access.RegDataType.DWORD,
                                 reg_value=value) is False:
            self.fail("Failed to write into registry with key %s and value %s" %
                      (registry_key, value))
        logging.debug("Successfully written into registry with key %s and value %s" %
                      (registry_key, value))


        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            logging.error('Under Run observed during test execution')


        # Restart display driver to make the changes to take place
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('Failed to restart driver after writing into registry')
        logging.debug('Display driver restarted successfully')


        # Verify virtual displays
        if self.verify_virtual_display() is False:
            logging.error('Failed to verify virtual displays after restarting driver')
            return False
        logging.info('Successfully enabled/disabled virtual displays. Virtual displays count : %s'
                     % self.number_virtual_displays)
        return True

    ##
    # @brief        Dynamically adds a virtual display with default EDID and appends the virtual display id in the ids list
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def dynamic_add_virtual_display(self):

        displays_count_before_adding_vd = self.display_config.get_all_display_configuration().numberOfDisplays
        logging.debug('Number of displays before adding a Dynamic Virtual Display : %s'
                      % displays_count_before_adding_vd)

        igfxsdk = win32com.client.Dispatch("{917D8440-45E3-428F-A3FC-A61CC20E378F}")

        virtual_display_new_id = igfxsdk.Display.VirtualDisplay.Add()
        if igfxsdk.Display.VirtualDisplay.Error != DISPLAY_VIRTUAL_SUCCESS:
            gdhm.report_bug(
                title="[VirtualDisplay] CUI SDK failure, Failed to dynamically add virtual display with Display ID {0}".format(
                    virtual_display_new_id),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E3)
            self.fail(
                'CUI SDK failure. Failed to dynamically add the virtual display with Display ID : %s' % virtual_display_new_id)

        time.sleep(5)

        displays_count_after_adding_vd = self.display_config.get_all_display_configuration().numberOfDisplays
        logging.debug('Number of displays after adding a Dynamic Virtual Display : %s'
                      % displays_count_after_adding_vd)

        if displays_count_after_adding_vd != (displays_count_before_adding_vd + 1):
            gdhm.report_bug(
                title="[VirtualDisplay] Failed to add virtual display dynamically",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2)
            self.fail("Failed to add virtual display dynamically")

        self.virtual_display_ids.append(virtual_display_new_id)
        logging.info('Successfully added a virtual display dynamically with Display ID : %s' % virtual_display_new_id)

    ##
    # @brief        Dynamically removes the virtual display based on the virtual display id provided
    # @param[in]    self; Object of virtual display base class
    # @param[in]    vd_id; Id of the virtual display to be removed
    # @return       void
    def dynamic_remove_virtual_display(self, vd_id=None):

        if vd_id is None:
            # Check the virtual_display_ids global list
            if not self.virtual_display_ids:
                self.fail('Virtual Display ID not provided and the Global Virtual Display IDs list is also empty')
            # Fetch the last virtual display id from the list
            vd_id = self.virtual_display_ids[-1]

        displays_count_before_removing_vd = self.display_config.get_all_display_configuration().numberOfDisplays
        logging.debug('Number of displays before removing a Dynamic Virtual Display : %s'
                      % displays_count_before_removing_vd)

        igfxsdk = win32com.client.Dispatch("{917D8440-45E3-428F-A3FC-A61CC20E378F}")

        igfxsdk.Display.VirtualDisplay.Remove(vd_id)
        if igfxsdk.Display.VirtualDisplay.Error != DISPLAY_VIRTUAL_SUCCESS:
            gdhm.report_bug(
                title="[VirtualDisplay] CUI SDK failure, Failed to dynamically remove virtual display with Display ID {0}".format(
                    vd_id),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E3)
            self.fail('CUI SDK failure. Failed to dynamically remove the virtual display with Display ID : %s' % vd_id)

        time.sleep(5)

        displays_count_after_removing_vd = self.display_config.get_all_display_configuration().numberOfDisplays
        logging.debug('Number of displays after removing a Dynamic Virtual Display : %s'
                      % displays_count_after_removing_vd)

        if displays_count_after_removing_vd != (displays_count_before_removing_vd - 1):
            gdhm.report_bug(
                title="[VirtualDisplay] CUI SDK failure, Failed to dynamically remove virtual display with Display ID {0}".format(
                    vd_id),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2)
            self.fail("Failed to remove virtual display dynamically with Display ID : %s" % vd_id)

        self.virtual_display_ids.pop()
        logging.info('Successfully removed a virtual display dynamically with Display ID : %s' % vd_id)

    ##
    # @brief        Unittest Teardown function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def tearDown(self):
        logging.info('Test Cleanup started...')

        # Disable all virtual displays
        self.number_virtual_displays = 0
        if self.enable_disable_virtual_display() is False:
            self.fail('Failed to disable Virtual displays')
        logging.info('Virtual displays disabled successfully')

        for display in self.plugged_display:
            if display_utility.unplug(display) is False:
                self.fail("Failed to unplug display %s" % display)
            logging.info('Successfully unplugged the display %s' % display)

    ##
    # @brief        Plug displays in Low power state
    # @param[in]    self; Object of virtual display base class
    # @param[in]    plugged_display ; list that contains the displays that have been plugged
    # @param[in]    power_event; Power event to be invoked
    # @return       boolean value true or false
    def plug_display_during_low_power(self, plugged_display, power_event):
        enum_displays_before_plug = self.display_config.get_enumerated_display_info()
        display_list_after_plug = []


        # Plug display in low power state
        if display_utility.plug_display(plugged_display, self.cmd_line_param, True) is False:
            return False

        # Invoke Power Event
        result = self.display_power.invoke_power_event(power_event, POWER_EVENT_DURATION)
        self.assertEquals(result, True, 'Failed to invoke sleep state %s' % power_event)


        # Enumerated display after resuming from low power state
        enum_displays_after_plug = self.display_config.get_enumerated_display_info()
        for index in range(enum_displays_after_plug.Count):
            display_list_after_plug.insert(index, CONNECTOR_PORT_TYPE(
                enum_displays_after_plug.ConnectedDisplays[index].ConnectorNPortType).name)

        if enum_displays_after_plug.Count == enum_displays_before_plug.Count + 1 and \
                plugged_display in display_list_after_plug:
            self.plugged_display.append(plugged_display)
            return True
        else:
            return False

    ##
    # @brief        UnPlug display in Low power state
    # @param[in]    self; Object of virtual display base class
    # @param[in]    unplugged_display; name of the display that need to be unplugged
    # @param[in]    power_event; Power event to be invoked
    # @return       boolean value true or false
    def unplug_display_during_low_power(self, unplugged_display, power_event):
        enum_displays_before_unplug = self.display_config.get_enumerated_display_info()
        display_list_after_unplug = []

        logging.info("Trying to unplug display %s in low power state" % unplugged_display)


        # UnPlug display in low power state
        if display_utility.unplug(unplugged_display, True) is False:
            return False

        # Invoke Power Event
        result = self.display_power.invoke_power_event(power_event, POWER_EVENT_DURATION)
        self.assertEquals(result, True, 'Failed to invoke sleep state %s' % power_event)


        # Enumerated display after resuming from low power state
        enum_displays_after_unplug = self.display_config.get_enumerated_display_info()
        for index in range(enum_displays_after_unplug.Count):
            display_list_after_unplug.insert(index, CONNECTOR_PORT_TYPE(
                enum_displays_after_unplug.ConnectedDisplays[index].ConnectorNPortType).name)

        logging.info('Enumerated displays list after resume from low power : %s' % display_list_after_unplug)

        if (enum_displays_after_unplug.Count == enum_displays_before_unplug.Count - 1 and
                unplugged_display not in display_list_after_unplug):
            if unplugged_display in self.displays_list:
                self.plugged_display.remove(unplugged_display)
            return True
        else:
            return False
