########################################################################################################################
# @file        system_utility.py
# @brief       Python wrapper exposes API's related to System Utility DLL
# @author      Reeju Srivastava, Amanpreet Kaur Khurana, Ami Golwala, Raghupathy
########################################################################################################################
import logging
import subprocess
import time
from Lib.enum import IntEnum  # @Todo: Override with Built-in python3 enum script path

from Libs.Core import registry_access
from Libs.Core.core_base import singleton
from Libs.Core.test_env import test_context

MAX_SUPPORTED_DISPLAYS = 16
DEVICE_NAME_SIZE = 128
MAX_BUFFER_SIZE = 256
BUFFER_SIZE = 512
LAN_WARMUP_TIME = 5
RETRY_LIMIT = 1


##
# @brief        EnvironmentType Enum
class EnvironmentType(IntEnum):
    SIMENV_FULSIM = 1
    SIMENV_PIPE2D  = 2
    POST_SI_ENV  = 3


# ============================================== No New APIs to be added ==============================================

##
# @brief        SystemUtility Class
@singleton
class SystemUtility(object):

    ##
    # @brief        Enabling LAN
    # @return       bool - True if LAN is enabled successfully, False otherwise
    def enable_LAN(self):
        logging.debug("Enabling LAN")
        enable_lan = subprocess.Popen((r"powershell.exe enable-NetAdapter -name Eth* " + "-confirm:$false"),
                                      shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        # Warmup time is required for Powershell to finish and reflect network adapter changes.
        time.sleep(LAN_WARMUP_TIME)
        list_adapter = subprocess.Popen(r"powershell.exe Get-netadapter", shell=True, stdout=subprocess.PIPE,
                                        universal_newlines=True)
        if "Disabled" not in list_adapter.stdout.read():
            logging.debug("API: Enabled LAN Successfully")
            return True
        else:
            logging.warning("Failed to Enable LAN")
            return False

    ##
    # @brief        Disabling LAN
    # @return       bool - True is LAN is disabled, False otherwise
    def disable_LAN(self):
        logging.debug("Disabling LAN")
        disable_lan = subprocess.Popen((r"powershell.exe disable-NetAdapter -name Eth* " + "-confirm:$false"),
                                       shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        # Warmup time is required for Powershell to finish and reflect network adapter changes.
        time.sleep(LAN_WARMUP_TIME)
        list_adapter = subprocess.Popen(r"powershell.exe Get-netadapter", shell=True, stdout=subprocess.PIPE,
                                        universal_newlines=True)
        if "Up" not in list_adapter.stdout.read():
            logging.debug("API: Disabled LAN Successfully")
            return True
        else:
            logging.warning("Failed to Disable LAN")
            return False

    ##
    # @brief        Provide Driver type information for given Adapter
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       bool - True if Yangra driver, False otherwise
    #               WA : Currently Driver Escape call failed to get that Driver is YANGRA or LEGACY.
    #               So get the Platform name based on DeviceId and checking with list of platforms [HSW,SKL,GLK,CFL,KBL]
    def is_ddrw(self, gfx_index='gfx_0'):
        # Get Adapter Info from GFX Adapter Details ( Default it takes First Adapter Info from the list)
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        platform_name = adapter_info.get_platform_info().PlatformName
        if platform_name == 'Platform_None':
            logging.error("Platform Not found")
            return None
        if str(platform_name).upper() in ['HSW', 'SKL', 'GLK', 'CFL', 'KBL']:
            return False
        return True

    ##
    # @brief        Get the environment Details from Reading Reg key IsDisplayPreSilicon.
    # @return       str - ENVIRONMENT_TYPE enum name
    def get_execution_environment_type(self):
        # Read Reg key IsDisplayPreSilicon.
        key_name = "IsDisplayPreSilicon"
        reg_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, r"SYSTEM\Setup")
        value, reg_type = registry_access.read(args=reg_args, reg_name=key_name)
        if value in EnvironmentType.__members__.values():
            return EnvironmentType(value).name
        return EnvironmentType.POST_SI_ENV.name

# ============================================== No New APIs to be added ==============================================
