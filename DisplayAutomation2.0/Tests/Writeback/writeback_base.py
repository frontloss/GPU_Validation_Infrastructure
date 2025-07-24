########################################################################################################################
# @file         writeback_base.py
# @brief        The script parses writeback devices and number of displays from the command line.
#               The following helper functions are used for writeback verification.
# 	             1 Plug /Unplug writeback devices and verify
# 	             2 Dump buffers of all available writeback devices
#                3 Enable writeback devices in windows registry
# 	             4 Apply the display configuration on all the plugged displays
# 	             5 Set all enumerated display mode to all available displays.
# @author       Patel, Ankurkumar G
########################################################################################################################
import sys
import unittest

from Libs.Core import cmd_parser, enum, registry_access, display_essential
from Libs.Core.display_power import DisplayPower
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Core.wrapper import driver_escape_args
from Libs.Core import driver_escape
from Libs.Core.wrapper.driver_escape_args import WritebackHpd, WbBufferInfo, Region2D
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.flip import MPO
from Libs.Core import reboot_helper
from Tests.Writeback.writeback_verifier import *


##
# @brief    Writeback base class for writeback tests
class WritebackBase(unittest.TestCase):
    connected_list = []
    plugged_display = []
    platform = None
    custom_tags = {'-WB_0': '0', '-WB_1': '0'}

    disp_config = DisplayConfiguration()
    disp_power = DisplayPower()
    reg_read = MMIORegister()
    wb_verifier = WritebackVerifier()
    under_run_status = UnderRunStatus()
    test_fail_flag = False

    is_high_resolution = False
    wb_device_count = 2  # default value of wb device count is 2
    wb_device_list = list()
    cx = 1920  # 2560 # 3840
    cy = 1080  # 1600 # 2160
    wb_resolution = Region2D(cx, cy)
    wbHpdArgs = WritebackHpd(False, 0, cx, cy, False)
    mpo_flip = MPO()
    enable_gmm_regkey = True

    ##
    # @brief        Unittest setUp function
    # @param[in]    self; Object of writeback base class
    # @return       void
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags.keys())

        # Get the wb_device_list from command line
        if self.cmd_line_param['WB_0'] == [] and self.cmd_line_param['WB_1'] == 'NONE':
            self.wb_device_list = ['wb_0']
        if self.cmd_line_param['WB_0'] == [] and self.cmd_line_param['WB_1'] == []:
            self.wb_device_list = ['wb_0', 'wb_1']
        if self.cmd_line_param['WB_0'] == 'NONE' and self.cmd_line_param['WB_1'] == []:
            self.wb_device_list = ['wb_1']
        if self.cmd_line_param['WB_0'] == 'NONE' and self.cmd_line_param['WB_1'] == 'NONE':
            self.fail(
                'Invalid writeback devices provided, please provide writeback device in proper format : -WB_0/WB_1')

        # Get the number of wb devices from command line (wb_device_list)
        self.wb_device_count = len(self.wb_device_list)
        logging.debug(" wb_device_count is = %s" % self.wb_device_count)

        # validate wb device count - maximum 2 writeback devices are supported
        if not 0 < int(self.wb_device_count) <= 2:
            self.fail('Invalid number of writeback devices provided')

        # Add NonPCIGMM Regkey for DD_SURFACE_USAGE_WRITEBACK allocation
        self.mpo_flip.enable_disable_pci_segment(self.enable_gmm_regkey)

        # Disable DSB Writes for Gamma
        if PLATFORM_NAME not in DSB_WORKAROUND:
            dfc_key_name = "DisplayFeatureControl"
            ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
            dfc_default_value, dfc_type = registry_access.read(args=ss_reg_args, reg_name=dfc_key_name)

            if dfc_default_value is None:
                logging.error('Error while reading registry')
                self.fail()
            logging.debug('Initial value of registry : {0}'.format(hex(dfc_default_value)))

            # Set bit 22 to disable DSB write for Gamma
            new_value = dfc_default_value | 0x400000
            if new_value == dfc_default_value:
                logging.info('DSB Gamma already disabled in display feature control, so skipping registry write operation')
            else:
                logging.info('Disabling DSB Gamma in display feature control reg key')
                if registry_access.write(args=ss_reg_args, reg_name=dfc_key_name,
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=new_value) is False:
                    logging.error('Error while writing registry')
                    self.fail()
                logging.debug('New registry value : {0}'.format(hex(new_value)))
        else:
            logging.info("DSB writes for Gamma is not disabled for Writeback, Platform {}".format(PLATFORM_NAME))

        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        for device in self.connected_list:
            logging.debug("Device Name : %s " % device)

        logging.info("Setup: Step - Enable writeback using regkey NumberOfWritebackDevices ")
        if not self.enable_wb_devices(self.wb_device_count):
            self.fail("\tFAIL: Writeback functinality enabling Failed")
        logging.info("\tPASS: Writeback functinality enabled successfully")

    ##
    # @brief        Plug and verify writeback devices
    # @param[in]    self; Object of writeback base class
    # @return       void
    def plug_and_verify_wb_devices(self):
        logging.debug("writeback_base: plug_and_verify_wb_devices() Entry:")
        adapter_info = TestContext.get_gfx_adapter_details()['gfx_0']
        # Plug Writeback device
        for wb_device in self.wb_device_list:
            logging.debug("wb_device is : %s" % wb_device)
            logging.debug("Flag is_high_resolution is : %s" % self.is_high_resolution)
            if self.is_high_resolution and self.wb_device_count == 1:
                if wb_device == 'wb_0':
                    self.wb_resolution.cX = 3840  # 2560 1920 #
                    self.wb_resolution.cY = 2160  # 1600 1080 #
            if self.is_high_resolution and self.wb_device_count == 2:
                if wb_device == 'wb_0':
                    self.wb_resolution.cX = 2560  # 1920 # 3840 #
                    self.wb_resolution.cY = 1600  # 1080 # 2160 #
                if wb_device == 'wb_1':
                    self.wb_resolution.cX = 2560  # 1920 # 3840 #
                    self.wb_resolution.cY = 1600  # 1080 # 2160 #
            logging.info("Plug Writeback device %s" % wb_device)
            self.wbHpdArgs = driver_escape_args.WritebackHpd(True, 0, self.wb_resolution.cX, self.wb_resolution.cY, False)
            edid_path = None # Provide EDID Path if specific EDID is required for WB
            if self.wbHpdArgs.resolution.cX == 0 or self.wbHpdArgs.resolution.cX is None or \
                    self.wbHpdArgs.resolution.cY == 0 or self.wbHpdArgs.resolution.cY is None:
                logging.error("Invalid resolution provided in wb_hpd_args")
                gdhm.report_bug(
                    title="[Writeback] Invalid resolution provided in wb_hpd_args",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E3)
                return False
            if not driver_escape.plug_unplug_wb_device(adapter_info, self.wbHpdArgs, edid_path):
                logging.info("\tFAIL: Writeback device %s plug unsuccessful " % wb_device)
                gdhm.report_bug(
                    title="[Writeback] Failed to plug writeback device {0} through escape call".format(wb_device),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E3)
                return False
            # Breather Time to plug the Write-back devices
            time.sleep(1)
            logging.info("\tPASS: Writeback device %s plugged successfully" % wb_device)

        # Activate writeback devices before checking for transcoder status
        self.apply_config_on_all_devices(enum.EXTENDED)

        # Verify writeback devices are plugged
        logging.info("Step - Verify Writeback device after plug")

        if not self.wb_verifier.verify_wb_enable_sequence(self.wb_device_list):
            logging.info("\tFAIL: Writeback devices enable sequence is not fully completed")
            return False
        logging.info("\tPASS: Writeback devices enable sequence is fully completed")
        logging.debug("writeback_base: plug_and_verify_wb_devices() Exit:")
        return True

    ##
    # @brief        Unplug and verify writeback devices
    # @param[in]    self; Object of writeback base class
    # @return       void
    def unplug_and_verify_wb_devices(self):
        logging.debug("writeback_base: unplug_and_verify_wb_devices() Entry:")
        # Unplug Writeback device
        enumerated_display = self.disp_config.get_enumerated_display_info()
        adapter_info = TestContext.get_gfx_adapter_details()['gfx_0']
        for display_count in range(0, enumerated_display.Count):
            if "WD_" in str(
                    CONNECTOR_PORT_TYPE(
                        enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)):
                targetid = enumerated_display.ConnectedDisplays[display_count].TargetID
                self.wbHpdArgs = driver_escape_args.WritebackHpd(False, targetid, self.wb_resolution.cX,
                                                                 self.wb_resolution.cY, False)
                edid_path = None  # Provide EDID path if specific EDID is required for WB
                if self.wbHpdArgs.resolution.cX == 0 or self.wbHpdArgs.resolution.cX is None or \
                        self.wbHpdArgs.resolution.cY == 0 or self.wbHpdArgs.resolution.cY is None:
                    logging.error("Invalid resolution provided in wb_hpd_args")
                    gdhm.report_bug(
                        title="[Writeback] Invalid resolution provided in wb_hpd_args",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E3)
                    return False
                if not driver_escape.plug_unplug_wb_device(adapter_info, self.wbHpdArgs, edid_path):
                    logging.error("\tFAIL: Failed to Unplug writeback device with target ID : %s" %
                                  enumerated_display.ConnectedDisplays[display_count].TargetID)
                    gdhm.report_bug(title="[Writeback] Failed to unplug writeback device through escape call",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E3)
                else:
                    logging.info("\tPASS: Unplugged writeback device with target ID : %s" % targetid)

        # Verify writeback devices after unplug
        logging.info("Step - Verify Writeback device after unplug")
        time.sleep(1)
        if not self.wb_verifier.verify_wb_disable_sequence(self.wb_device_list):
            logging.info("\tFAIL: Writeback devices disable sequence is not fully completed")
            return False
        logging.info("\tPASS: Writeback devices disable sequence is fully completed")
        logging.debug("writeback_base: unplug_and_verify_wb_devices() Exit:")
        return True

    ##
    # @brief        To dump buffers of all available writeback devices
    # @param[in]    self; Object of writeback base class
    # @return       void
    def dump_buffers(self):
        logging.debug("writeback_base: dump_buffers() Entry:")
        enumerated_display = self.disp_config.get_enumerated_display_info()
        for display_count in range(0, enumerated_display.Count):
            if "WD_" in \
                    str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)):
                targetid = enumerated_display.ConnectedDisplays[display_count].TargetID
                wb_buffer_info = WbBufferInfo()
                result, wb_buffer_info = driver_escape.dump_wb_buffer(targetid, 0, wb_buffer_info, 8)
                if result is False:
                    logging.error("\tFAIL: Failed to Dump buffers for writeback device with target ID : %s" % targetid)
                    gdhm.report_bug(title="[Writeback] Failed to dump buffer for writeback device through escape call",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E3)
                    return False
                logging.info("\tPASS: Dumped buffers for writeback device with target ID : %s" % targetid)

        logging.debug("writeback_base: dump_buffers() Exit:")
        return True

    ##
    # @brief        Enable writeback devices in windows registry
    # @param[in]    self; Object of writeback base class
    # @param[in]    device_count
    # @return       True or False based on API's success.
    def enable_wb_devices(self, device_count):
        status = False
        reboot_required = False

        logging.debug("writeback_base: enable_wb_devices() Entry:")
        try:
            reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
            registry_flag = registry_access.write(args=reg_args, reg_name="NumberOfWritebackDevices",
                                                  reg_type=registry_access.RegDataType.DWORD, reg_value=device_count)
            if registry_flag:
                logging.info("Writeback feature successfully enabled in Registry")
            else:
                logging.error("Failure while creating Registry Key for writeback device")
                return False
        except EnvironmentError:
            logging.error("Environment Error occurred while writing to registry")
            return False

        # Restart driver
        status, reboot_required = display_essential.restart_gfx_driver()

        if status is False and reboot_required is True:
            if reboot_helper.reboot(self, 'test_run') is False:
                self.fail("Failed to reboot the system and Writeback functinality enabling Failed")
        elif status is False and reboot_required is False:
            self.fail("Failed to restart display driver and Writeback functinality enabling Failed")

        # Check Under-run status
        if self.under_run_status.verify_underrun() is True:
            logging.error("Under Run observed during test execution")
            return False
        logging.info("No underrun observed till writeback regkey creation")
        return True

    ##
    # @brief         Set the display config on all available displays as mentioned in config_type
    # @param[in]     self; Object of writeback base class
    # @param[in]     config_type ; mentions the configuration type of the display
    # @return        boolean value true
    def apply_config_on_all_devices(self, config_type):
        logging.debug("writeback_base: apply_config_on_all_devices() Entry:")
        connected_display_list = []
        enumerated_display = self.disp_config.get_enumerated_display_info()
        for display_count in range(0, enumerated_display.Count):
            connected_display_list.append(
                str(CONNECTOR_PORT_TYPE(
                    enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)))
            logging.debug("Connected display is %s" % str(
                CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)))

        self.assertEquals(self.disp_config.set_display_configuration_ex(config_type, connected_display_list,
                                                                        self.disp_config.get_enumerated_display_info()),
                          True, "Failed to apply display configuration")
        logging.info("\tPASS: Successfully applied Display configuration")
        logging.debug("writeback_base: apply_config_on_all_devices() Exit:")
        return True

    ##
    # @brief        Applies possible configurations
    # @param[in]    self; Object of writeback base class
    # @param[in]    connected_display is a list that has all displays
    # @return       boolean value true
    def apply_possible_configs(self, connected_display):
        logging.debug("writeback_base: apply_possible_configs() Entry:")
        config_list = []
        if len(connected_display) == 1:
            display1 = connected_display[0]

            config_list = (enum.SINGLE, [display1])

        if len(connected_display) == 2:
            display1 = connected_display[0]
            display2 = connected_display[1]

            config_list = [(enum.SINGLE, [display1]), (enum.CLONE, [display1, display2]),
                           (enum.EXTENDED, [display2, display1]), (enum.SINGLE, [display2]),
                           (enum.EXTENDED, [display1, display2]), (enum.CLONE, [display2, display1])]

        if len(connected_display) == 3:
            display1 = connected_display[0]
            display2 = connected_display[1]
            display3 = connected_display[2]

            config_list = [(enum.SINGLE, [display1]), (enum.EXTENDED, [display1, display2, display3]),
                           (enum.CLONE, [display3, display1]), (enum.CLONE, [display3, display2, display1]),
                           (enum.EXTENDED, [display1, display2]), (enum.SINGLE, [display3]),
                           (enum.CLONE, [display2, display1, display3]), (enum.EXTENDED, [display2, display3]),
                           (enum.CLONE, [display1, display3]), (enum.EXTENDED, [display2, display1, display3])]

        if len(connected_display) == 4:
            display1 = connected_display[0]
            display2 = connected_display[1]
            display3 = connected_display[2]
            display4 = connected_display[3]

            config_list = [(enum.SINGLE, [display1]), (enum.EXTENDED, [display1, display2, display3, display4]),
                           (enum.CLONE, [display3, display1]), (enum.CLONE, [display4, display3, display2, display1]),
                           (enum.EXTENDED, [display1, display2]), (enum.SINGLE, [display3]),
                           (enum.CLONE, [display2, display1, display3]), (enum.EXTENDED, [display2, display3]),
                           (enum.CLONE, [display1, display3]), (enum.EXTENDED, [display2, display1, display3])]

        for each_config in range(len(config_list)):
            if self.disp_config.set_display_configuration_ex(config_list[each_config][0],
                                                             config_list[each_config][1],
                                                             self.disp_config.get_enumerated_display_info()) is False:
                self.fail()
        logging.info("\tPASS: Successfully applied all Display configurations")
        logging.debug("writeback_base: apply_possible_configs() Exit:")
        return True

    ##
    # @brief         Sets all enumerated display modes on each of the display/writeback device
    # @param[in]     self; Object of writeback base class
    # @return        boolean value true
    def set_possible_modes(self):
        logging.debug("writeback_base: set_possible_modes() Entry:")

        # Get target ids of the displays required for modeset
        target_ids = list()

        # Pruned modes dict will contain only the MIN, MID & MAX resolutions for all the display
        pruned_modes_dict = dict()

        config = self.disp_config.get_current_display_configuration()

        for index in range(config.numberOfDisplays):
            target_ids.append(config.displayPathInfo[index].targetId)

        # Get all supported modes for all enumerated displays
        self.supported_mode_dict = self.disp_config.get_all_supported_modes(target_ids)

        for key, values in self.supported_mode_dict.items():
            test_modes_list = list()
            test_modes_list.append(values[0])
            test_modes_list.append(values[len(values) // 2])
            test_modes_list.append(values[-1])

            pruned_modes_dict[key] = test_modes_list

        # Apply display mode
        for key, values in pruned_modes_dict.items():
            for mode in values:
                logging.debug("Trying to apply display mode: %s " %
                              (mode.to_string(self.enumerated_displays)))
                if self.disp_config.set_display_mode([mode]) is False:
                    logging.error("Failed to apply display mode: %s"
                                  % mode.to_string(self.enumerated_displays))
                    self.fail()
                logging.info(
                    "\tPASS: Successfully appllied display mode: %s" % mode.to_string(self.enumerated_displays))

        logging.info("\tPASS: Successfully applied MIN, MID & MAX mode")
        logging.debug("writeback_base: set_possible_modes() Exit:")
        return True

    ##
    # @brief        Unittest tearDown function
    # @param[in]    self; Object of writeback base class
    # @return       void
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Writeback Test Clean Up")


        # Unplug writeback devices
        logging.info("Teardown - Unplug Writeback devices")
        if not self.unplug_and_verify_wb_devices():
            self.test_fail_flag = True
        logging.debug("test_fail_flag is : %s" % self.test_fail_flag)

        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            if "WD_" not in display:
                logging.info("Trying to unplug %s", display)
                display_utility.unplug(display)

        # Remove the NonPCIGMM Regkey
        self.enable_gmm_regkey = False
        self.mpo_flip.enable_disable_pci_segment(self.enable_gmm_regkey)

        # check for the failures observed during unplug of writeback devices
        if self.test_fail_flag:
            logging.info("\tFAIL: Failing the test as unplug of writeback devices failed")
            self.fail()
        logging.info("Writeback test clean up completed successfully")


if __name__ == '__main__':
    unittest.main()
