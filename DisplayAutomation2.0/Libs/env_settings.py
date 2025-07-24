#######################################################################################################################
# @file          env_settings.py
# @brief         This class will help in parsing the configuration file.
#                Exposes below API's
#                   get - Read the section and key value from config.ini
#                   set - Update a key value for a particular section in config.ini
# @author        Bharath Venkatesh, Beeresh
#######################################################################################################################

import configparser
import json
import logging
import os
import shutil
import stat
import struct
import subprocess
import sys
import time
import traceback
import unittest
from types import TracebackType

from Libs.Core import cmd_parser
from Libs.Core import registry_access
from Libs.Core import system_utility
from Libs.Core import test_header
from Libs.Core.gta import bullseye_manager
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger
from Libs.Core.test_env import test_context

__DEFAULT_ADAPTER = 'gfx_0'
ACTIVE_CONFIG_FILE = os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini")
REGISTRY_BACKUP_FILE = os.path.join(test_context.TEST_TEMP_FOLDER, "registry_backup.json")
DEFAULT_CONFIG_FILE = os.path.join(test_context.ROOT_FOLDER, "Libs\\Core\\test_env\\config.ini")


##
# @brief        Global Exception Handler
# @param[in]    expection_type - Exception Type
# @param[in]    value - Value of the exception
# @param[in]    tb - TracebackType
def __global_exception_handler(expection_type, value: str, tb: TracebackType) -> None:
    logging.error(value)
    logging.error(''.join(traceback.format_tb(tb)))


##
# @brief        Provide DoD driver information
# @return       bool - True if DoD driver path False if not DoD driver path None otherwise
def is_dod_driver_path() -> bool:
    key_name = "WinDoD"
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services")
    value, data_type = registry_access.read(args=reg_args, reg_name=key_name, sub_key=r"igfx\Parameters")
    if value is not None:
        return True if value == 1 else False if value == 0 else None
    return False


##
# @brief        Helper Function for Enable and Disable DoD
# @details      TBD : Need to add support for handling Multi Adapter
# @param[in]    enable - Parameter to enable switch DoD path. True to enable DoD, False to disable DoD
# @return       bool - True if reg_write and driver restart is True, False otherwise
def switch_dod_path(enable: bool) -> bool:
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                             reg_path=r"SYSTEM\CurrentControlSet\Services")
    reg_write = registry_access.write(args=reg_args, reg_name="WinDoD", reg_type=registry_access.RegDataType.DWORD,
                                      reg_value=1 if enable else 0, sub_key=r"igfx\Parameters")
    if not reg_write:
        logging.warning("DoD switching failed!!")

    return reg_write


##
# @brief        Configure Windod
# @param[in]    action - action to be performed
# @return       None
def configure_windod(action: str) -> None:
    yangra_subkey = r"igfxn\Parameters"
    legacy_subkey = r"igfx\Parameters"
    sub_key = yangra_subkey if system_utility.SystemUtility().is_ddrw() is True else legacy_subkey
    action = action.upper()
    key_name = "WinDoD"
    if action == "ENABLE":
        key_value = 1
    elif action == "DISABLE":
        key_value = 0
    else:
        logging.error("configure_windod Invalid action provided")
        return
    reg_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services")
    reg_write = registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                      reg_value=key_value, sub_key=sub_key)
    if not reg_write:
        logging.error("DoD switching failed!!")


##
# @brief        Configure Forced Virtual Display
# @param[in]    action - action to be performed
# @return       None
def configure_force_virtual_display(action: str) -> None:
    action = action.upper()
    key_name = "ForceVirtualDisplay"
    value = 0
    status = False
    if action == "ENABLE":
        value = 1

    legacy_registry_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, "SOFTWARE\\Intel\\KMD")
    status = registry_access.write(legacy_registry_args, key_name, registry_access.RegDataType.DWORD, value)
    if status is False:
        logging.error("Failed to write registry to configure force virtual display on base platform")
    else:
        logging.info("Successfully configured force virtual display on base platform")

    for gfx_index in test_context.TestContext.get_gfx_adapter_details().keys():
        ss_registry_args = registry_access.StateSeparationRegArgs(gfx_index)
        status = registry_access.write(ss_registry_args, key_name, registry_access.RegDataType.DWORD, value)
        if status is False:
            logging.error("Failed to write registry to configure force virtual display")
        else:
            logging.info("Successfully configured force virtual display")


##
# @brief        Configure bullseye Feature
# @param[in]    action - action to be performed
# @return       None
def configure_bullseye_feature(action: str) -> None:
    action = action.upper()
    operation = False

    if action == "ENABLE":
        operation = True

    bullseye_manager.configure_bullseye_coverage(operation)


##
# @brief        Configure Simulation Type
# @param[in]    action - action to be performed
# @return       None
def configure_simulation_type(action: str) -> None:
    from Libs.Core.sw_sim import gfxvalsim
    action = action.upper()
    if action == "HYBRID":
        gfxvalsim.GfxValSim().configure_feature(__DEFAULT_ADAPTER, gfxvalsim.GFXVALSIM_FEATURE_HYBRID_SIMULATION, True)
    else:
        gfxvalsim.GfxValSim().configure_feature(__DEFAULT_ADAPTER, gfxvalsim.GFXVALSIM_FEATURE_HYBRID_SIMULATION, False)


##
# @brief        Configure Sink Simulation
# @param[in]    action - action to be performed
# @return       None
def configure_sink_simulation(action: str) -> None:
    from Libs.Core.sw_sim import gfxvalsim
    action = action.upper()
    if action == "ENABLE":
        logging.debug("sink_simulation is enabled by default")
        gfxvalsim.GfxValSim().configure_feature(__DEFAULT_ADAPTER, gfxvalsim.GFXVALSIM_FEATURE_SINK_SIMULATION,
                                                False)  # 1 to enable sink simulation
        return True
    elif action == "DISABLE":
        gfxvalsim.GfxValSim().configure_feature(__DEFAULT_ADAPTER, gfxvalsim.GFXVALSIM_FEATURE_SINK_SIMULATION,
                                                True)  # 1 to enable sink simulation
    else:
        logging.warning("Invalid action ")


##
# @brief        Configure State Seperation
# @param[in]    action - action to be performed
# @return       None
def configure_state_separation(action: str) -> None:
    action = action.upper()
    key_name = "EnableStateSeparation"
    if action == "ENABLE":
        key_value = 1
    elif action == "DISABLE":
        key_value = 0
    else:
        logging.error("configure_state_separation Invalid action provided")
        return
    legacy_registry_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                         reg_path=r"SYSTEM\CurrentControlSet\Services")
    reg_write = registry_access.write(args=legacy_registry_args, reg_name=key_name,
                                      reg_type=registry_access.RegDataType.DWORD, reg_value=key_value,
                                      sub_key=r"igfx\Parameters")
    if not reg_write:
        logging.error("state separation registry update failed!")


##
# @brief        Configure MST Sideband Message Multiplier
# @param[in]    action - action to be performed
# @return       None
def configure_mst_sideband_message_multiplier(action: str) -> None:
    action = action.upper()
    key_name = "SideMsgEventReplyDelayMultiplier"
    value = 1
    if action == "ENABLE":
        value = 10000

    for gfx_index in test_context.TestContext.get_gfx_adapter_details().keys():
        ss_registry_args = registry_access.StateSeparationRegArgs(gfx_index)
        status = registry_access.write(ss_registry_args, key_name, registry_access.RegDataType.DWORD, value)
        if status is False:
            logging.error("Failed to write registry to configure Sideband Message Event Reply Multiplier")
        else:
            logging.info("Successfully configured Sideband Message Event Reply Multiplier")


##
# @brief        Configure Registry Values
# @param[in]    registry_key - registry key
# @param[in]    bit_field - To update bit field
# @param[in]    value - registry value
# @param[in]    backup - backup file path
# @return       None
def configure_registry(registry_key, bit_field, value, backup):
    data_type = registry_access.RegDataType.DWORD

    for gfx_index in test_context.TestContext.get_gfx_adapter_details().keys():
        ss_registry_args = registry_access.StateSeparationRegArgs(gfx_index)
        current_value, reg_type = registry_access.read(ss_registry_args, registry_key)
        if registry_access.RegDataType.BINARY == registry_access.RegDataType(reg_type):
            current_value = struct.unpack("<L", current_value)[0]
        registry_backup = {}
        if os.path.exists(REGISTRY_BACKUP_FILE) and backup:
            with open(REGISTRY_BACKUP_FILE) as f:
                registry_backup = json.load(f)

        if registry_key not in registry_backup and backup:
            registry_backup[registry_key] = current_value
            with open(REGISTRY_BACKUP_FILE, "w") as f:
                json.dump(registry_backup, f)

        if ":" == bit_field:
            if "0x" in value.lower():
                # Hex value passed in command line
                registry_value = int(value, 16)
            else:
                registry_value = int(value)
        else:
            start_index = int(bit_field.split(":")[1])
            end_index = int(bit_field.split(":")[0]) + 1
            assert end_index > start_index, "end_index must be greater or equal to start_index"
            if "0x" in value.lower():
                # Hex value passed in command line
                registry_value = int(value, 16)
            else:
                registry_value = int(value)

            mask = '0b' + ''.join(['1'] * (end_index - start_index))
            mask = list(bin((int(mask, 2) & registry_value) << start_index)[2:].zfill(32)[::-1])

            value = list(bin(current_value)[2:].zfill(32)[::-1])
            value[start_index:end_index] = mask[start_index:end_index]
            registry_value = int('0b' + ''.join(value)[::-1], 2)

        if registry_access.write(ss_registry_args, registry_key, data_type, registry_value) is False:
            logging.error(f"Registry update failed. Registry: {registry_key} Value: {registry_value}")
        else:
            logging.info(f"Registry update successful. Registry: {registry_key} Value: {registry_value}")


##
# @brief        TestEnvConfiguration Class
class TestEnvConfiguration(unittest.TestCase):
    ##
    # @note     If a tag can have only few possible values (Ex: for "sink_simulation", possible values are "enable" or
    #           "disable"), specify all these values in a list. In this case value given in command line will be
    #           validated based on this list. On the other hand, if a tag can have any value, leave the list empty. In
    #           this case, script not validate the value given in command line. (Ex: for "sim_operation_mode", possible
    #           values could be 0x40, 0x01, ...)
    CUSTOM_TAGS = {'-crc_enable': ['TRUE', 'FALSE'],
                   '-crc_stimuli': ['VIDEO', 'DIRECTXAPP'],
                   '-crc_presi': ['CAPTURE', 'COMPARE', 'NONE'],
                   '-silicon_type': ['SOC', 'SIMULATOR', 'EMULATOR'],
                   '-simulation_type': ['GFXVALSIM', 'SHE', 'MANUAL', 'NONE', 'HYBRID'],
                   '-under_run_verifier': ['ENABLE', 'DISABLE'],
                   '-windod': ['ENABLE', 'DISABLE'],
                   '-force_vd': ['ENABLE', 'DISABLE'],
                   '-bullseye': ['ENABLE', 'DISABLE'],
                   '-state_separation': ['ENABLE', 'DISABLE'],
                   '-sink_simulation': ['ENABLE', 'DISABLE'],
                   '-lfp_simulation': ['ENABLE', 'DISABLE'],
                   '-sim_operating_mode': [],
                   '-override_verifier_cfg': [],  # Do not init with any value
                   '-add_verifier_cfg': [],  # Do not init with any value
                   '-she_config': ['SHE_CFG1', 'SHE_CFG2', 'SHE_CFG3', 'SHE_CFG4', 'SHE_CFG5', 'SHE_CFG6',
                                   'SHE_CFG7', 'SHE_CFG8', 'SHE_CFG9'],
                   '-mst_sideband_multiplier': ['ENABLE', 'DISABLE'],
                   # -registry argument takes a list of (key, bit field, value) tuple
                   # Examples:
                   # -registry DisplayPcFeatureControl 20:20 1
                   # -registry FeatureTestControl 3:0 7 PsrDrrsEnable : 0x0
                   # -registry clean --> special case. to be called from tearDown.
                   '-registry': [],
                   '-collect_logs': ['TRUE', 'FALSE']
                   }

    CUSTOM_TAG_SECTION_MAP = {
        '-silicon_type': 'GENERAL',
        '-under_run_verifier': 'GENERAL',
        '-windod': 'GENERAL',
        '-force_vd': 'GENERAL',
        '-bullseye': 'GENERAL',
        '-state_separation': 'GENERAL',
        '-crc_enable': 'CRC',
        '-crc_stimuli': 'CRC',
        '-crc_presi': 'CRC',
        '-simulation_type': 'SIMULATION',
        '-sink_simulation': 'SIMULATION',
        '-lfp_simulation': 'SIMULATION',
        '-sim_operating_mode': 'SIMULATION',
        '-override_verifier_cfg': 'VERIFIER_CFG',
        '-add_verifier_cfg': 'VERIFIER_CFG',
        '-she_config': 'SIMULATION',
        '-mst_sideband_multiplier': 'GENERAL',
        '-collect_logs': 'GENERAL',
    }

    CUSTOM_TAG_ACTION_MAP = {
        '-sink_simulation': configure_sink_simulation,
        '-windod': configure_windod,
        '-state_separation': configure_state_separation,
        '-simulation_type': configure_simulation_type,
        '-force_vd': configure_force_virtual_display,
        '-bullseye': configure_bullseye_feature,
        '-mst_sideband_multiplier': configure_mst_sideband_message_multiplier,
        '-registry': configure_registry
    }
    log_folder = test_context.LOG_FOLDER

    ##
    # @brief        Setup Method
    # @return       None
    def setUp(self) -> None:
        logging.info(f"Display Automation Binary Version : {test_header.get_binary_version()}")
        logging.info("********* Configuration of config.ini started *********")
        # Reset the config.ini file every time
        # env_settings is executed
        if os.path.exists(ACTIVE_CONFIG_FILE):
            self.__remove_readonly_file(ACTIVE_CONFIG_FILE)

    ##
    # @brief        API to run Test
    # @return       None
    def runTest(self) -> None:
        cmd_line_params = cmd_parser.parse_cmdline(sys.argv, self.CUSTOM_TAGS.keys())
        for key in self.CUSTOM_TAGS.keys():
            custom_tag = key[1:].upper()
            # validate if there is appropriate value for custom tag
            if type(cmd_line_params[custom_tag]) is list and cmd_line_params[custom_tag]:
                # validate if entered value for custom tag lies within our options
                custom_tag_value = cmd_line_params[custom_tag][0]
                if len(self.CUSTOM_TAGS[key]) != 0 and custom_tag_value not in self.CUSTOM_TAGS.get(key):
                    logging.warning(
                        "Invalid value for argument {} valid options: {}".format(key, self.CUSTOM_TAGS.get(key)))
                    continue

                if custom_tag not in ["REGISTRY"]:
                    section_name = self.CUSTOM_TAG_SECTION_MAP[key]
                    set(section_name, custom_tag, custom_tag_value)

                if key in self.CUSTOM_TAG_ACTION_MAP.keys():
                    action = self.CUSTOM_TAG_ACTION_MAP[key]
                    if "REGISTRY" == custom_tag:
                        # Check if clean argument is present in command line
                        # if yes, read the backup file and restore all the registry values
                        if "CLEAN" == custom_tag_value.upper():
                            if os.path.exists(REGISTRY_BACKUP_FILE):
                                with open(REGISTRY_BACKUP_FILE) as f:
                                    registry_values = json.load(f)
                                    for reg_key, value in registry_values.items():
                                        action(reg_key, ":", str(value), False)
                        else:
                            arg_index = 0
                            assert len(cmd_line_params[
                                           custom_tag]) % 3 == 0, "Number of arguments in -registry " \
                                                                  "must be multiple of 3"
                            while arg_index < len(cmd_line_params[custom_tag]):
                                key = cmd_line_params[custom_tag][arg_index]
                                bit_field_str = cmd_line_params[custom_tag][arg_index + 1]
                                assert ":" in bit_field_str, "BitField must contain :"
                                value_str = cmd_line_params[custom_tag][arg_index + 2]
                                action(key, bit_field_str, value_str, True)
                                arg_index += 3
                    else:
                        action(custom_tag_value)
            else:
                logging.warning("Custom tag do not have pre-defined value, ignoring configuration")

    ##
    # @brief        Tear Down Function
    # @return       None
    def tearDown(self) -> None:
        logging.info("********* Configuration of config.ini completed *********")

    ##
    # @brief        API to remove Read Only files
    # @param[in]    path - Path of the file to be removed
    # @return       None
    def __remove_readonly_file(self, path: str) -> None:
        logging.debug("Deleting the stale config file at : {}".format(path))
        os.chmod(path, stat.S_IWRITE)
        os.remove(path)


##
# @brief        TestEnvConfigParser Class
# @details      Class which exposes below API's to read and write config.ini file
#               get_env_config - Get the key value from section and key name
#               set_env_config - Set the key value by providing section and key name
class TestEnvConfigParser(object):
    config = None

    ##
    # @brief        Constructor
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.__copy_config_file_if_not_exist()

        try:
            self.config.read(ACTIVE_CONFIG_FILE)
        except:
            logging.warning(f"Exception in reading {ACTIVE_CONFIG_FILE}.")
            self.__remove_readonly_file(ACTIVE_CONFIG_FILE)
            self.__copy_config_file_if_not_exist()
            self.config.read(ACTIVE_CONFIG_FILE)

    def __copy_config_file_if_not_exist(self):
        if not os.path.exists(os.path.dirname(ACTIVE_CONFIG_FILE)):
            os.makedirs(os.path.dirname(ACTIVE_CONFIG_FILE))
        if not os.path.exists(ACTIVE_CONFIG_FILE):
            logging.info("Copying config.ini file.")
            shutil.copy2(DEFAULT_CONFIG_FILE, ACTIVE_CONFIG_FILE)

    def __remove_readonly_file(self, path: str):
        logging.info("Deleting the stale config file at : {}".format(path))
        if os.path.exists(path):
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)

    ##
    # @brief        Get Sections
    # @return       config.sections - Sections Configuration
    def get_sections(self):
        return self.config.sections()

    ##
    # @brief        section Option mapping
    # @param[in]    section - section to be mapped
    # @return       dict - dictionary of mapped section
    def section_option_map(self, section: str) -> dict:
        dict1 = {}

        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
            except:
                dict1[option] = None
        return dict1

    ##
    # @brief        Update section API
    # @param[in]    section - Section to be updated
    # @param[in]    option - type of update to be performed
    # @param[in]    value - Updated value
    # @return       bool - True if updation is successful, False otherwise
    def update(self, section: str, option: str, value: str) -> bool:
        if self.config.has_option(section, option):
            os.chmod(ACTIVE_CONFIG_FILE, stat.S_IWRITE)
            cfgfile = open(ACTIVE_CONFIG_FILE, 'w')
            self.config.set(section, option, value)
            self.config.write(cfgfile)
            cfgfile.flush()
            cfgfile.close()
            return True
        else:
            return False


##
# @brief        Get Section Details
# @param[in]    section - section value
# @param[in]    key_name - key name of the portion of the detail required
# @return       section_map - Section map of the required section, None otherwise
def get(section, key_name):
    cfg = TestEnvConfigParser()
    if section not in cfg.get_sections():
        return None

    section_map = cfg.section_option_map(section)
    if key_name not in section_map.keys():
        return None
    return section_map[key_name]


##
# @brief        Set a Section
# @param[in]    section - section value
# @param[in]    key_name - key name of the portion of the detail required
# @param[in]    key_value - key value of the portion of the detail required
# @return       None
def set(section: str, key_name: str, key_value: str) -> None:
    test_cfg = TestEnvConfigParser()
    if test_cfg.update(section, key_name, key_value):
        logging.info("*** Updating config file *** [%s][%s] -> [%s]" % (section, key_name, key_value))
    else:
        logging.info("Updating config file failed due to incorrect section or option")


if __name__ == '__main__':
    from Libs.Core.test_env import test_environment

    sys.excepthook = __global_exception_handler
    test_environment.TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_environment.TestEnvironment.log_test_result(outcome.result)
    test_environment.TestEnvironment.store_cleanup_logs(status)
    display_logger._cleanup()
