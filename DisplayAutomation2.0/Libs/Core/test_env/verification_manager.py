#######################################################################################################################
# @file         verification_manager.py
# @brief        This module maintains the state of checks related to Gfx and ValSim Driver, which is utilized to handle
#               dynamic test-level scenarios. If there is a change in gfx driver, the test will invoke the update
#               interface method to skip gfx driver running status check (if valid scenario).
#               Example: Gfx driver Install-Uninstall tests will internally remove the existing gfx driver instance.
#               Here we must update the interface to skip for gfx driver check until it is re-installed.
# @author       Chandrakanth Pabolu, Kiran Kumar Lakshmanan
########################################################################################################################
import configparser
import logging
import os

from Libs import env_settings
from Libs.Core.test_env import test_context, state_machine_manager

# Store gfx driver checks to be performed in temporary INI file
TEST_CONFIG_PATH = os.path.join(test_context.LOG_FOLDER, "test_config.ini")

# INI file Sections
SECTION_VERIFICATION = 'VERIFICATION'  # Corresponds to ini file section

# INF file Options
SKIP_GFX_DRIVER_CHECK = 'skip_gfx_driver_check'  # Check that needs to be skipped


##
# @brief        Method to setup initial configuration during test environment initialize
# @return       None
def initialize() -> None:
    state_machine_manager.StateMachine().simulation_type = env_settings.get('SIMULATION', 'simulation_type').upper()
    state_machine_manager.StateMachine().skip_gfx_driver_check = __get_skip_driver_check()


##
# @brief        Update custom INI settings file with skip gfx driver check data
# @param[in]    value - True to skip gfx driver check, False otherwise
# @return       None
def configure_skip_driver_check(value: bool) -> None:
    config = configparser.ConfigParser()
    if os.path.exists(TEST_CONFIG_PATH):
        config.read(TEST_CONFIG_PATH)
    else:
        config.add_section(SECTION_VERIFICATION)
    config[SECTION_VERIFICATION][SKIP_GFX_DRIVER_CHECK] = str(value)

    logging.info(f"Writing skip_gfx_driver_check with {value} in ini file")
    with open(TEST_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
    # Todo: Remove before merge
    if os.path.exists(TEST_CONFIG_PATH):
        logging.info(f"FILE SUCCESSFULLY CREATED - {TEST_CONFIG_PATH}")
    else:
        logging.error(f"FAILED TO CREATE FILE - {TEST_CONFIG_PATH}")
    state_machine_manager.StateMachine().skip_gfx_driver_check = value
    logging.info(f"Successfully written skip_gfx_driver_check with {value} in ini file")


##
# @brief        Delete custom INI settings file
# @return       None
def cleanup_test_config() -> None:
    if os.path.exists(TEST_CONFIG_PATH):
        os.remove(TEST_CONFIG_PATH)


##
# @brief        Read from custom INI settings file
# @return       bool - True if verfication of gfx driver needs to be skipped, False otherwise
def __get_skip_driver_check() -> bool:
    # If custom INI file exists, get the skip gfx driver check settings
    if os.path.exists(TEST_CONFIG_PATH):
        config = configparser.ConfigParser()
        config.read(TEST_CONFIG_PATH)
        if config.has_option(SECTION_VERIFICATION, SKIP_GFX_DRIVER_CHECK):
            logging.info(f"skip_gfx_driver_check={config[SECTION_VERIFICATION][SKIP_GFX_DRIVER_CHECK]}")
            return config[SECTION_VERIFICATION].getboolean(SKIP_GFX_DRIVER_CHECK) is True
    return False
