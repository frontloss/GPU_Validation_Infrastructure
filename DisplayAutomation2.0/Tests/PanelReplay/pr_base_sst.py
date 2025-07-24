#################################################################################################################
# @file         pr_base_sst.py
# @brief        implements panel replay helper functions.
# @author       ashishk2
#################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser
from Libs.Core import display_essential
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Tests.PowerCons.Functional.PSR import pr


##
# @brief This class contains functions that helps in validating PR enable and other basic check.
class PrBaseSST(unittest.TestCase):
    config = DisplayConfiguration()
    # Platform details for all connected adapters
    PLATFORM_INFO = {
        gfx_index: {
            'gfx_index': gfx_index,
            'name': adapter_info.get_platform_info().PlatformName
        }
        for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
    }

    ##
    # @brief        This method is the entry point for PR test cases. This enables the regkey required
    #               for execution of PR tests
    # @return       None
    @classmethod
    def setUpClass(cls) -> None:
        logging.info("Enable PR in Registry")
        for gfx_index in cls.PLATFORM_INFO.values():
            status = pr.enable_for_efp(gfx_index['gfx_index'])
            if status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    assert False, "FAILED to restart the driver"
            elif status is False:
                assert False, "Failed to enable PR"
        logging.info('Successfully enabled PR in registry')

    ##
    # @brief        This method is the exit point for PR test cases. This resets the regkey changes done
    #               for execution of PR tests
    # @return       None
    @classmethod
    def tearDownClass(cls) -> None:
        logging.info("TearDown: Disable PR in Registry")
        for gfx_index in cls.PLATFORM_INFO.values():
            status = pr.disable_for_efp(gfx_index['gfx_index'])
            if status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    assert False, "FAILED to restart the driver"
            elif status is False:
                assert False, "Failed to disable PR"
        logging.info('TearDown: Successfully disabled PR in registry')

    ##
    # @brief        This class method is the entry point for PR Basic SST Scenario tests.
    #               Helps to initialize some of the parameters required for test execution.
    # @return       None
    def setUp(self):
        logging.debug("Entry: setUpClass")

        # Variable Initialization
        self.input_display_list = []
        self.panel_info = {}
        self.platform = None

        # Parse the commandline params
        cmd_line_param = cmd_parser.parse_cmdline(sys.argv)

        for key, value in cmd_line_param.items():
            key = "_".join(key.split("_")[:2])
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    if key not in self.panel_info.keys():
                        self.panel_info[key] = {}
                    if value['panel_index'] is not None:
                        self.panel_info[key].update({'panel_index': value['panel_index']})
                    if value['index'] is not None:
                        self.panel_info[key].update({'index': value['index']})
                    if value['non_pr_panel_index'] is not None:
                        self.panel_info[value['connector_port']].update({'non_pr_panel_index': value['non_pr_panel_index']})

        logging.info("Printing panel info dict: {}".format(self.panel_info))
        # input_display_list[] is a list of Port Names from user args
        self.input_display_list = cmd_parser.get_sorted_display_list(cmd_line_param)

        logging.debug("Exit: PrBase -> setUpClass")

        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for index in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[index].DisplayAdapterName)
            break

    ##
    # @brief        This method returns currently emulated display name and target id.
    # @return       Dictionary. Display Name as Key and Target ID as Value.
    def get_display_names(self):
        enum_display_dict = {}
        enumerated_displays = self.config.get_enumerated_display_info()
        for index in range(0, enumerated_displays.Count):
            port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
            target_id = enumerated_displays.ConnectedDisplays[index].TargetID
            enum_display_dict[port] = target_id
        return enum_display_dict

    ##
    # @brief        This method helps to getting panel index which was input at cmdline
    # @param[in]    display_port
    # @return       Panel Index
    def get_panel_index(self, display_port):
        if display_port in self.panel_info.keys():
            for key, value in self.panel_info[display_port].items():
                logging.info("Key and value pair is : {} and {}".format(key, value)) 
                if key == 'panel_index':
                    logging.info("Return panel_index is: {}".format(value))
                    return value
        logging.info("Return panel_index is NONE ")
        return None

    ##
    # @brief        This method helps to getting xml file which was input at cmdline
    # @param[in]    display_port the port string like DP_B, DP_C, etc
    # @return       xml file name
    def get_non_pr_panel_index(self, display_port):
        if display_port in self.panel_info.keys():
            for key, value in self.panel_info[display_port].items():
                logging.info("Key and value pair is : {} and {}".format(key, value)) 
                if key == 'non_pr_panel_index':
                    logging.info("Return non_pr_panel_index is: {}".format(value))
                    return value
        logging.info("Return non PR panel_index is NONE ")
        return None

    ##
    # @brief        This method apply 420 mode for given port
    # @param[in]    port  DP_B/DP_C
    # @return       True if successful , False otherwise
    def apply_420_mode(self, port):
        port_dict = self.get_display_names()
        supported_modes = self.config.get_all_supported_modes([port_dict[port]], pruned_mode_list=False)
        for _, modes in supported_modes.items():
            for mode in modes:
                if mode.samplingMode.yuv420:
                    status = self.config.set_mode(mode)
                    time.sleep(10)
                    if status:
                        logging.info("\tSuccessfully applied YUV420 mode")
                        return True
                    logging.error("Failed to apply YUV420 mode")
                    return False
        logging.error("YUV 420 mode not enumerated in mode list table")
        return False
