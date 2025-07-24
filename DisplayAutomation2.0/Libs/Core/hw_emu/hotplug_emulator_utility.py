#######################################################################################################################
# @file         hotplug_emulator_utility.py
# @brief        Python wrapper exposes API's related to HW EMULATOR Utility.
# @author       Balaji Gurusamy, sanehadeep Kaur
#######################################################################################################################
import logging
import os
import xml.etree.ElementTree as Et
from Lib.enum import IntEnum  # @Todo: Override with Built-in python3 enum script path

from Libs.Core import enum
from Libs.Core.core_base import singleton
from Libs.Core.hw_emu.she_utility import SheDisplayType
from Libs.Core.test_env import test_context


##
# @brief        Defines the hardware Emulator type
class HwEmulatorType(IntEnum):
    NONE = 0
    SHE = 1


##
# @brief        CANAKIT UTILITY Class
@singleton
class HotPlugEmulatorUtility(object):

    ##
    # @brief    Constructor
    def __init__(self):
        self.hw_emulator_type = HwEmulatorType.NONE

    ##
    # @brief    Get emulator type
    # @return   None
    def __get_emulator_type(self):
        if self.hw_emulator_type != HwEmulatorType.NONE:
            return self.hw_emulator_type
        if os.path.exists(test_context.GTA_EMULATOR_CONFIG_FILE) is False:
            logging.debug("Port Mapping File ({0}) is not available".format(test_context.GTA_EMULATOR_CONFIG_FILE))
            self.hw_emulator_type = HwEmulatorType.NONE
        xml_root = Et.parse(test_context.GTA_EMULATOR_CONFIG_FILE).getroot()
        emu_handle = xml_root.findall('HotPlugEmulator')
        for handle in emu_handle:
            if handle.attrib['EmulatorName'] == "SHE" and handle.attrib['IsEmulatorConnected'] == 'TRUE':
                self.hw_emulator_type = HwEmulatorType.SHE
                break

    ##
    # @brief        Get the she display ID
    # @param[in]    connector_port - connector port type
    # @return       None
    def __she_display_id(self, connector_port):
        return {'DP_A': SheDisplayType.EDP,
                'DP_B': SheDisplayType.DP_1,
                'DP_C': SheDisplayType.DP_1,
                'DP_D': SheDisplayType.DP_1,
                'HDMI_B': SheDisplayType.HDMI_1,
                'HDMI_C': SheDisplayType.HDMI_1,
                'HDMI_D': SheDisplayType.HDMI_1
                }[connector_port]

    ##
    # @brief        Plug the display
    # @param[in]    display_port - connector port type
    # @param[in]    delay - timeout value
    # @return       bool - True or False based on request success
    def hot_plug(self, display_port, delay=0):
        if self.emulator_module is None:
            logging.error("Emulator Tool not Connected")
            return False
        else:
            return self.emulator_module.hot_plug_unplug(self.__she_display_id(display_port), True, delay)

    ##
    # @brief        Unplug the display
    # @param[in]    display_port - connector port type
    # @param[in]    delay - timeout value
    # @return       bool - True or False based on request success
    def hot_unplug(self, display_port, delay=0):
        if self.emulator_module is None:
            logging.error("Emulator Tool not Connected")
            return False
        else:
            return self.emulator_module.hot_plug_unplug(self.__she_display_id(display_port), False, delay)

    ##
    # @brief        Toggles System Power input mode based on power_source parameter.
    # @param[in]    power_source - The Power Source Information
    # @param[in]    delay - timeout value
    # @return       bool - True or False based on request success
    def acdc_switch(self, power_source, delay=0):
        if self.emulator_module is None:
            logging.error("Emulator Tool not Connected")
            return False
        else:
            return self.emulator_module.switch_powerline(power_source, delay)

    ##
    # @brief        Toggles LFP Lid switch based on action parameter.
    # @param[in]    lid_state - The State of the Lid
    # @param[in]    delay - timeout value
    # @return       bool - True or False based on request success
    def lid_switch(self, lid_state, delay=0):
        if self.emulator_module is None:
            logging.error("Emulator Tool not Connected")
            return False
        else:
            return self.emulator_module.lid_switch_button_press(lid_state, delay)
