########################################################################################################################
# @file         writeback_poc_base.py
# @brief        The script accepts writeback device list  and number of devices(maximum 2 devices) from the command line.
#               The following tests can be done along  with the unittest setup and teardown function.
#               * To Plug /Unplug writeback devices and verify
#               * To enable writeback devices
# @author       Patel, Ankurkumar G
########################################################################################################################
import sys
import unittest

from Libs.Core import cmd_parser, enum, registry_access, display_essential
from Libs.Core import driver_escape
from Libs.Core.display_power import DisplayPower
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.wrapper import driver_escape_args
from Tests.Writeback.writeback_verifier import *


##
# @brief    Contains helper functions that will be used by writeback_poc_tests
class WritebackPoCBase(unittest.TestCase):
    connected_list = []
    plugged_display = []
    platform = None
    custom_tags = {'-WB_0': '0', '-WB_1': '0'}

    disp_config = DisplayConfiguration()
    disp_power = DisplayPower()
    reg_read = MMIORegister()
    wb_verifier = WritebackVerifier()
    test_fail_flag = False

    is_high_resolution = False
    wb_device_count = 2  # default value of wb device count is 2
    wb_device_list = list()

    ##
    # @brief        Unittest setUp function
    # @param[in]    self; Object of writeback_poc base class
    # @return       void
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags.keys())

        ##
        # Get the wb_device_list from command line
        if self.cmd_line_param['WB_0'] == [] and self.cmd_line_param['WB_1'] == 'NONE':
            self.wb_device_list = ['wb_0']
        if self.cmd_line_param['WB_0'] == [] and self.cmd_line_param['WB_1'] == []:
            self.wb_device_list = ['wb_0', 'wb_1']
        if self.cmd_line_param['WB_0'] == 'NONE' and self.cmd_line_param['WB_1'] == []:
            self.wb_device_list = ['wb_1']
        if self.cmd_line_param['WB_0'] == 'NONE' and self.cmd_line_param['WB_1'] == 'NONE':
            self.fail(
                'Invalid writeback devices provided, please provide  writeback device in proper format : -WB_0/WB_1')

        # Get the number of wb devices from command line (wb_device_list)
        self.wb_device_count = len(self.wb_device_list)
        logging.debug(" wb_device_count is = %s" % self.wb_device_count)

        # validate wb device count - maximum 2 writeback devices are supported
        if not 0 < int(self.wb_device_count) <= 2:
            self.fail('Invalid number of writeback devices provided')

        # Enable writeback registry "NumberOfWritebackDevices"
        logging.info("Setup: Step - Enable writeback using regkey NumberOfWritebackDevices ")
        if self.enable_wb_devices(self.wb_device_count) is False:
            self.fail("\tFAIL: Writeback functinality enabling Failed")
        logging.info("\tPASS: Writeback functinality enabled successfully")

        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        for device in self.connected_list:
            logging.debug("Device Name : %s " % device)

    ##
    # @brief        Plug and verify writeback devices
    # @param[in]    self; Object of writeback_poc base class
    # @return       boolean value true if writeback device plug is successful else false
    def plug_wb_devices(self):
        wb_hpd_args = driver_escape_args.WritebackHpd(True, 0, 1920, 1080, False)
        adapter_info = TestContext.get_gfx_adapter_details()['gfx_0']
        edid_path = None  # edid path should be given if particular edid needs to be plugged
        if edid_path is not None:
            edid_path = edid_path.encode()
        if wb_hpd_args.resolution.cX == 0 or wb_hpd_args.resolution.cX is None or \
                wb_hpd_args.resolution.cY == 0 or wb_hpd_args.resolution.cY is None:
            logging.error("Invalid resolution provided in wb_hpd_args")
            return False
        status = driver_escape.plug_unplug_wb_device(adapter_info, wb_hpd_args, edid_path)
        time.sleep(10)
        if status is False:
            logging.info("\tFAIL: Writeback device plug unsuccessful ")
            return False
        logging.info("\tPASS: Writeback device plugged successfully")
        return True

    ##
    # @brief        Unplug writeback devices
    # @param[in]    self; Object of writeback_poc base class
    # @param[in]    target; the deviceID
    # @return       boolean value true if writeback device unplug is successful else false
    def unplug_wb_devices(self, target):
        wb_hpd_args = driver_escape_args.WritebackHpd(False, target, 1920, 1080, False)
        adapter_info = TestContext.get_gfx_adapter_details()['gfx_0']
        edid_path = None  # edid path should be given if particular edid needs to be plugged
        if edid_path is not None:
            edid_path = edid_path.encode()
        if wb_hpd_args.resolution.cX == 0 or wb_hpd_args.resolution.cX is None or \
                wb_hpd_args.resolution.cY == 0 or wb_hpd_args.resolution.cY is None:
            logging.error("Invalid resolution provided in wb_hpd_args")
            return False
        status = driver_escape.plug_unplug_wb_device(adapter_info, wb_hpd_args, edid_path)

        if status is False:
            logging.info("\tFAIL: Writeback device unplug unsuccessful ")
            return False
        logging.info("\tPASS: Writeback device unplugged successfully")
        return True

    ##
    # @brief        TO enable writeback devices
    # @param[in]    self; Object of writeback_poc base class
    # @param[in]    device_count; number of devices
    # @return       boolean value if writeback devices are enabled else false
    def enable_wb_devices(self, device_count):
        logging.debug("writeback_utility: enable_wb_devices() Entry:")
        try:
            reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
            reg_value, reg_type = registry_access.read(args=reg_args, reg_name="NumberOfWritebackDevices")
            if reg_value == device_count:
                return True
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
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is True:
            logging.info("Successfully restarted Driver to set the WB devices")
        else:
            logging.error("Driver restart failed")
            return False
        logging.debug("writeback_utility: enable_wb_devices() Exit:")
        return True

    ##
    # @brief         Unplug and verify writeback devices
    # @param[in]     self; Object of writeback_poc base class
    # @return        status as true if device is unplugged properly else false
    def unplug_and_verify_wb_devices(self):
        status = True
        logging.debug("writeback_base: unplug_and_verify_wb_devices() Entry:")
        # Unplug Writeback device
        enumerated_display = self.disp_config.get_enumerated_display_info()
        for display_count in range(0, enumerated_display.Count):
            if "WD_" in str(
                    CONNECTOR_PORT_TYPE(
                        enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)):
                target = enumerated_display.ConnectedDisplays[display_count].TargetID
                status &= self.unplug_wb_devices(target)
                if status is False:
                    logging.error("\tFAIL: Failed to Unplug writeback device with target ID : %s" %
                                  enumerated_display.ConnectedDisplays[display_count].TargetID)
                else:
                    logging.info(
                        "\tPASS: Unplugged writeback device with target ID : %s" % target)
        return status

    ##
    # @brief         Unittest tearDown function
    # @param[in]     self; Object of writeback_poc base class
    # @return        void
    def tearDown(self):
        logging.info("Writeback Test Clean Up")

        # Unplug writeback devices
        logging.info("Step - Unplug Writeback devices")
        self.unplug_and_verify_wb_devices()

        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            if "WD_" not in display:
                logging.info("Trying to unplug %s", display)
                display_utility.unplug(display)

        logging.info("Writeback test clean up completed successfully")


if __name__ == '__main__':
    unittest.main()
