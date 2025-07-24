########################################################################################################################
# @file         display_hpd_base.py
# @brief        This script contains helper functions that will be used by Display Hotplug Unplug test scripts
# @author       Raghupathy, Dushyanth Kumar, Balaji Gurusamy
########################################################################################################################
import logging
import os
import shutil
import time
import unittest
from collections import namedtuple

import win32com.client

from Libs import env_settings
from Libs.Core import enum, display_utility
from Libs.Core import etl_parser
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_context import TestContext, LOG_FOLDER
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core import display_power
from Libs.Core.sw_sim import driver_interface
from Libs.Core.hw_emu.hotplug_emulator_utility import HotPlugEmulatorUtility
from Libs.Feature.clock import display_clock
from Libs.Feature.display_engine.de_master_control import DisplayEngine, VerificationMethod
from Libs.Core.display_config import display_config_enums as cfg_enum

##
# @brief: Display Detection Base class : To be used in Display Detection tests
class DisplayHPDBase(unittest.TestCase):
    # to be filled in respective derived classes
    adapter_display_dict = {}
    display_data = namedtuple('Display_Data', 'port edid dpcd')
    internal_displays = ['DP_A', 'MIPI_A', 'MIPI_C']
    low_pow_state = {'CS_STATE': 0, 'S3_STATE': 1, 'S4_STATE': 2, 'MONITOR_TURNOFF': 3}
    de_flag = []
    # Object Initializing
    config = display_config.DisplayConfiguration()
    power = display_power.DisplayPower()
    hotplug_emulator_utility = HotPlugEmulatorUtility()
    display_engine = DisplayEngine()

    ##
    # @brief        This method helps to Plug given display in required low power state.
    # @param[in]    port Name of display port (ex: DP_B, HDMI_C, etc).
    # @param[in]    panel_index Index of Panel if passed(ex: DP_A_EDP001 etc).
    # @param[in]    lowpower_state Low power state required (ex: enum.POWER_STATE_CS, enum.POWER_STATE_S4, etc).
    # @param[in]    hpd_mode This define Hot plug should go through SIM or EMU.
    # @param[in]    gfx_index Graphics Adapter to perform the action on
    # @param[in]    port_connector_type port connector type eg. NATIVE, PLUS etc
    # @return       Bool. True if request is success else False.
    def plug_during_lowpower_state(self, port, panel_index=None, lowpower_state=None, hpd_mode=None, gfx_index='gfx_0', port_connector_type='NATIVE'):
        mto_result = False
        edid = None
        dpcd = None

        if hpd_mode == "SIM":
            if lowpower_state == self.low_pow_state['MONITOR_TURNOFF']:
                mto_result = self.power.invoke_monitor_turnoff(display_power.MonitorPower.OFF, 5)
            else:
                # Plug Display or Initiate Plug Sequence before system goes to Low Power State
                if display_utility.plug(port=port, port_type=port_connector_type, panelindex=panel_index, is_low_power=True, gfx_index=gfx_index):
                    logging.info(f'{port} PLUG sequence initiated')
                    if lowpower_state is None:
                        return True
                else:
                    logging.error(f'{port} Failed to Initiate PLUG Sequence')
                    return False

        elif hpd_mode == "EMU":
            if self.hotplug_emulator_utility.hot_plug(port, 20):
                logging.info(f'{port} PLUG sequence initiated')
            else:
                logging.error(f'{port} Failed to Initiate PLUG Sequence')
                return False

        else:
            logging.error("Hot Plug and UnPlug Mode Not defined in 'hpd_mode'(SIM | EMU)")
            return False

        # Enter into Low Power State
        if lowpower_state == self.low_pow_state['CS_STATE']:
            if not self.power.is_power_state_supported(display_power.PowerEvent.CS):
                logging.error("CS is not enabled in system")
                return False
            if self.power.invoke_power_event(display_power.PowerEvent.CS, 60) is False:
                return False

        elif lowpower_state == self.low_pow_state['S3_STATE']:
            if self.power.is_power_state_supported(display_power.PowerEvent.CS):
                logging.error("CS is enabled in system, Please disable CS to enter S3")
                return False
            if self.power.invoke_power_event(display_power.PowerEvent.S3, 60) is False:
                return False

        elif lowpower_state == self.low_pow_state['S4_STATE']:
            if self.power.invoke_power_event(display_power.PowerEvent.S4, 60) is False:
                return False

        elif lowpower_state == self.low_pow_state['MONITOR_TURNOFF']:
            if not self.power.is_power_state_supported(display_power.PowerEvent.CS):
                if mto_result:
                    time.sleep(50)
                    if display_utility.plug(port=port, panelindex=panel_index, is_low_power=False, gfx_index=gfx_index):
                        time.sleep(5)
                        self.wake_up_display()
                    else:
                        logging.error(f'{port} Plug on {gfx_index} Failed during Monitor Turn Off')
                        self.wake_up_display()
                        return False
                else:
                    logging.error("Monitor Turn Off Failed")
            else:
                logging.warning("Monitor Turn on\Off will not support for CS enabled SUT")

        else:
            logging.error("Invalid Power State")

        time.sleep(10)

        # perform modeset with displays in cmdline
        enumerated_displays = self.config.get_enumerated_display_info()
        config_displays = []
        display_adapter_dict = {}

        for index in range(enumerated_displays.Count):
            enum_display_gfx_index = enumerated_displays.ConnectedDisplays[
                index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            for gfx_adapter, port_list in self.adapter_display_dict.items():
                if str(CONNECTOR_PORT_TYPE(
                        enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)) in port_list and enum_display_gfx_index == gfx_adapter:
                    config_displays.append(enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo)
                    display_adapter_dict.setdefault(enum_display_gfx_index, []).append(str(CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)))

        config = enum.EXTENDED if len(config_displays) > 1 else enum.SINGLE
        is_success = self.config.set_display_configuration_ex(config, config_displays, enumerated_displays)
        self.assertTrue(is_success, "Set Display Configuration Failed")

        # Verify Display Plugged after waking up from low power state
        enumerated_displays = self.config.get_enumerated_display_info()
        logging.debug("Enumerated Display Information: %s", enumerated_displays.to_string())

        if display_config.is_display_attached(enumerated_displays, port, gfx_index):
            logging.info(f'Success : {port} is plugged in with {list(self.low_pow_state.keys())[lowpower_state]} power state on {gfx_index}')
            self.verify_display_engine(display_adapter_dict)
            return True
        else:
            logging.error(f'Failed : {port} is not plugged in with {list(self.low_pow_state.keys())[lowpower_state]} power state on {gfx_index}')
            return False

    ##
    # @brief        This method helps to Unplug given display in required low power state.
    # @param[in]    port Name of display port (ex: DP_B, HDMI_C, etc).
    # @param[in]    lowpower_state Low power state required (ex: enum.POWER_STATE_CS, enum.POWER_STATE_S4, etc).
    # @param[in]    hpd_mode This define Hot plug should go through SIM or EMU.
    # @param[in]    gfx_index Graphics Adapter to perform the action on
    # @return       Bool. True if request is success else False.
    def unplug_during_lowpower_state(self, port, lowpower_state=None, hpd_mode=None, gfx_index='gfx_0'):
        mto_result = False

        if hpd_mode == "SIM":
            if lowpower_state == self.low_pow_state['MONITOR_TURNOFF']:
                time.sleep(2)
                mto_result = self.power.invoke_monitor_turnoff(display_power.MonitorPower.OFF, 5)
            else:
                # Plug Display or Initiate Unplug Sequence before system goes to Low Power State
                if display_utility.unplug(port=port, is_low_power=True, gfx_index=gfx_index):
                    logging.info(f'{port} UN-PLUG sequence initiated on {gfx_index}')
                    if lowpower_state is None:
                        return True
                else:
                    logging.error(f'{port} failed to initiate UN-PLUG Sequence on {gfx_index}')

                    return False

        elif hpd_mode == "EMU":
            if self.hotplug_emulator_utility.hot_unplug(port, 20):
                logging.info(f'{port} UnPLUG sequence initiated on {gfx_index}')
            else:
                logging.error(f'{port} failed to initiate UnPLUG Sequence on {gfx_index}')
                return False
        else:
            logging.error("Hot Plug and UnPlug Mode Not defined in 'hpd_mode'(SIM | EMU)")
            return False

        # Enter into Low Power State
        if lowpower_state == self.low_pow_state['CS_STATE']:
            if not self.power.is_power_state_supported(display_power.PowerEvent.CS):
                logging.error("CS is not enabled in system")
                return False
            if self.power.invoke_power_event(display_power.PowerEvent.CS, 60) is False:
                return False

        elif lowpower_state == self.low_pow_state['S3_STATE']:
            if self.power.is_power_state_supported(display_power.PowerEvent.CS):
                logging.error("CS is enabled in system, Please disable CS to enter S3")
                return False
            if self.power.invoke_power_event(display_power.PowerEvent.S3, 60) is False:
                return False

        elif lowpower_state == self.low_pow_state['S4_STATE']:
            if self.power.invoke_power_event(display_power.PowerEvent.S4, 60) is False:
                return False

        elif lowpower_state == self.low_pow_state['MONITOR_TURNOFF']:
            if not self.power.is_power_state_supported(display_power.PowerEvent.CS):
                if mto_result:
                    time.sleep(30)
                    if not display_utility.unplug(port=port, is_low_power=False, gfx_index=gfx_index):
                        logging.error(f'{port} Unplug Failed during Monitor Turn Off on {gfx_index}')
                        self.wake_up_display()
                        return False
                    time.sleep(5)
                    self.wake_up_display()
                else:
                    logging.error("Monitor Turn Off Failed")
            else:
                logging.warning("Monitor Turn on\Off will not support for CS enabled SUT")

        time.sleep(10)

        topology, displays, display_adapter_list = self.config.get_current_display_configuration_ex()
        display_adapter_dict = {}
        for index in range(len(display_adapter_list)):
            if displays[index] == 'VIRTUALDISPLAY' or display_adapter_list[
                index].MonitorFriendlyDeviceName == "Raritan CIM":
                logging.info("{}-{} Detected. Skipping unplug and DE Verification for this Display".format(
                    displays[index], display_adapter_list[index].MonitorFriendlyDeviceName))
            else:
                display_adapter_dict.setdefault(display_adapter_list[index].adapterInfo.gfxIndex, []).append(displays[index])

        if not display_adapter_dict:
            return True
        enumerated_displays = self.config.get_enumerated_display_info()
        logging.debug("Enumerated Display Information: %s", enumerated_displays.to_string())

        # Verify Display Plugged after waking up from low power state
        if display_config.is_display_attached(enumerated_displays, port, gfx_index):
            logging.error(f'Failed : {port} is not unplugged on {gfx_index} after '
                          f'{list(self.low_pow_state.keys())[lowpower_state]} power state')
            return False
        else:
            logging.info(f'Success : {port} is unplugged on {gfx_index} after '
                         f'{list(self.low_pow_state.keys())[lowpower_state]} power state')
            self.verify_display_engine(display_adapter_dict)
            return True

    ##
    # @brief        This method helps to get edid and dpcd paths for given panel_index
    # @param[in]    port Name of display port (ex: DP_B, HDMI_C, etc).
    # @param[in]    panel_index Index of the panel (ex: DP_A_EDP001 etc)
    # @param[in]    is_lfp represents if the requested port is LFP or EFP
    # @return       list containing edid_path and dpcd_path if request is success else None.
    def get_edid_dpcd_paths(self, port, panel_index, is_lfp=False):

        input_data = display_utility.get_panel_edid_dpcd_info(port=port, panel_index=panel_index, is_lfp=is_lfp)
        if input_data is None:
            return None
        else:
            edid = input_data['edid']
            dpcd = input_data['dpcd']

        if 'HDMI' in port:
            if os.path.exists(os.path.join(TestContext.panel_input_data(), 'HDMI', edid)):
                root_folder = 'HDMI'
            else:
                logging.error(f'EDID File {edid} not found in HDMI sub-folder of {TestContext.panel_input_data()}')
                return None

        elif 'DP' in port:
            if os.path.exists(os.path.join(TestContext.panel_input_data(), 'eDP_DPSST', edid)):
                root_folder = 'eDP_DPSST'
            elif os.path.exists(os.path.join(TestContext.panel_input_data(), 'DP_MST_TILE', edid)):
                root_folder = 'DP_MST_TILE'
            else:
                logging.error(f'EDID File {edid} not found in [eDP_DPSST \\ DP_MST_TILE] '
                              f'sub-folder of {TestContext.panel_input_data()}')
                return None

        edid_path = os.path.join(TestContext.panel_input_data(), root_folder, edid)

        if 'HDMI' in port:
            dpcd_path = None
        else:
            dpcd_path = os.path.join(TestContext.panel_input_data(), root_folder, dpcd)
            if not os.path.exists(dpcd_path):
                logging.error(f'DPCD File Not Found : {dpcd_path}')
                return None

        return edid_path, dpcd_path

    ##
    # @brief        This method helps to Plug given display.
    # @param[in]    port - Name of display port (ex: DP_B, HDMI_C, etc).
    # @param[in]    panel_index - Index of the panel (ex: DP_A_EDP001 etc)
    # @param[in]    port_type - port connector type (e.g: NATIVE, TC, TBT)
    # @param[in]    hpd_mode - This define Hot plug should go through SIM or EMU.
    # @param[in]    she_mst_index - SHE MST index
    # @param[in]    gfx_index - Graphics Adapter to perform the action on
    # @return       Bool - True if request is success else False.
    def plug_display(self, port, panel_index=None, port_type='NATIVE', hpd_mode=None, she_mst_index=None,
                     gfx_index='gfx_0'):
        status = True

        if she_mst_index is not None:
            from Libs.Core.hw_emu.she_emulator import SheUtility
            she_utility = SheUtility()
            adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
            ret = self.get_edid_dpcd_paths(port, panel_index=panel_index, is_lfp=False)
            if ret is None:
                return False
            edid_path, dpcd_path = ret[0], ret[1]
            status = status and she_utility.plug(adapter_info, port, edid_path, dpcd_path, False, None, she_mst_index)
        elif hpd_mode == "SIM":
            status = status and display_utility.plug(port=port, port_type= port_type, panelindex=panel_index,
                                                     gfx_index=gfx_index)
        elif hpd_mode == "EMU":
            status = status and self.hotplug_emulator_utility.hot_plug(port, 0)
        else:
            logging.error("Hot Plug and UnPlug Mode Not defined in 'hpd_mode'(SIM | EMU)")
            return False

        # Check if panel came active or not by checking panel timings
        enumerated_displays = self.config.get_enumerated_display_info()
        config_displays = []
        display_adapter_dict = {}
        for index in range(enumerated_displays.Count):
            enum_display_gfx_index = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            for gfx_adapter, port_list in self.adapter_display_dict.items():
                if str(CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)) in port_list and enum_display_gfx_index == gfx_adapter:
                    config_displays.append(enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo)
                    display_adapter_dict.setdefault(enum_display_gfx_index, []).append(str(CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)))

        if self.config.set_display_configuration_ex(enum.EXTENDED if len(config_displays) > 1 else enum.SINGLE,
                                                    config_displays, enumerated_displays) is False:
            self.fail("SetDisplayConfigurationEX returned false")
        _driver_interface = driver_interface.DriverInterface()
        adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
        status = status and _driver_interface.is_panel_timings_non_zero(adapter_info, port,
                                                    she_mst_index if she_mst_index is not None else 0)

        # Verify Plugged Display is enumerated
        if status and she_mst_index is None:
            time.sleep(15)
            enumerated_displays = self.config.get_enumerated_display_info()
            logging.debug(f'Enumerated Display Information: {enumerated_displays.to_string()}')
            if display_config.is_display_attached(enumerated_displays, port, gfx_index=gfx_index) is True:
                logging.info(f'{port} PLUG Successful on {gfx_index}')
                self.verify_display_engine(display_adapter_dict)
                status = status and True
            else:
                status = False

        if not status:
            logging.error(f'{port} PLUG Failed on {gfx_index}')
        return status

    ##
    # @brief        This method helps to Unplug given display.
    # @param[in]    port - Name of display port (ex: DP_B, HDMI_C, etc).
    # @param[in]    port_type - port connector type (e.g: NATIVE, TC, TBT)
    # @param[in]    hpd_mode - This define Hot plug should go through SIM or EMU.
    # @param[in]    de_verification - True if DE Verification is required.
    # @param[in]    she_mst_index - SHE MST index
    # @param[in]    gfx_index Graphics Adapter to perform the action on
    # @return       Bool. True if request is success else False.
    def unplug_display(self, port, port_type='NATIVE', hpd_mode=None, de_verification=True, she_mst_index=None,
                       gfx_index='gfx_0'):
        status = False
        enumerated_displays = self.config.get_enumerated_display_info()
        total_displays_connected = enumerated_displays.Count

        if she_mst_index is not None:
            from Libs.Core.hw_emu.she_emulator import SheUtility
            she_utility = SheUtility()
            adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
            status = she_utility.unplug(adapter_info, port, False, None, she_mst_index)
            return status
        elif hpd_mode == "SIM":
            if display_utility.unplug(port, port_type=port_type, gfx_index=gfx_index):
                status = True
        elif hpd_mode == "EMU":
            if self.hotplug_emulator_utility.hot_unplug(port, 0):
                status = True
        else:
            logging.error("Hot Plug and UnPlug Mode Not defined in 'hpd_mode'(SIM | EMU)")
            return False

        topology, displays, display_adapter_list = self.config.get_current_display_configuration_ex()
        display_adapter_dict = {}
        for index in range(len(display_adapter_list)):
            if displays[index] == 'VIRTUALDISPLAY' or display_adapter_list[
                index].MonitorFriendlyDeviceName == "Raritan CIM":
                logging.info("{}-{} Detected. Skipping unplug and DE Verification for this Display".format(
                    displays[index], display_adapter_list[index].MonitorFriendlyDeviceName))
            else:
                display_adapter_dict.setdefault(display_adapter_list[index].adapterInfo.gfxIndex, []).append(displays[index])

        if not display_adapter_dict:
            return True
        
        # Verify if unplugged Display is not enumerated
        if status:
            time.sleep(15)
            enumerated_displays = self.config.get_enumerated_display_info()
            logging.debug(f'Enumerated Display Information: {enumerated_displays.to_string()}')
            count = enumerated_displays.Count

            # WA for DG platforms to not check unplug status due to OS behavior
            adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
            platform = adapter_info.get_platform_info().PlatformName.upper()
            if count == total_displays_connected and platform in ['DG1', 'DG2', 'ELG']:
                logging.warning("WARN: Display {} reported as still Attached. Sometimes OS doesnot update Unplug Status for last display, in case where "
                                "Virtual Display not plugged by driver. Ignoring unplug status for such cases".format(port))
                return True

            if display_config.is_display_attached(enumerated_displays, port, gfx_index=gfx_index) is False:
                logging.info(f'{port} Unplug Successful' + (f'on {gfx_index}') + (f' on mst_index {she_mst_index}'
                                                            if she_mst_index is not None else ''))
                if de_verification:
                    self.verify_display_engine(display_adapter_dict)
                else:
                    self.de_flag.append(True)
                return True      

        logging.error(f'{port} Unplug Failed on {gfx_index}')
        return False

    ##
    # @brief        This method returns currently emulated display name and target id for requested adapter.
    # @param[in]    gfx_index Graphics Adapter to perform the action on
    # @return       Dictionary. Display Name as Key and Target ID as Value.
    def get_display_names(self, gfx_index='gfx_0'):
        enum_display_dict = {}
        enumerated_displays = self.config.get_enumerated_display_info()
        for index in range(0, enumerated_displays.Count):
            port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
            gfx_adapter = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if gfx_index == gfx_adapter:
                target_id = enumerated_displays.ConnectedDisplays[index].TargetID
                enum_display_dict[port] = {target_id, gfx_adapter}

        return enum_display_dict


    ##
    # @brief        This method triggers Keyboard Event.
    # @return       Bool. True if request is success else False.
    def wake_up_display(self):
        key_board = win32com.client.Dispatch("WScript.Shell")
        key_board.SendKeys('{LEFT}')
        return True

    ##
    # @brief        This method calls de verification utility.
    # @param[in]    gfx_display_dict Adapter and display dict to verify DE
    #               e.g.{'gfx_0': ['dp_b', 'dp_c'], 'gfx_1': ['dp_b']}
    # @return       Bool.
    def verify_display_engine(self, gfx_display_dict = None):
        for adapter, displays in gfx_display_dict.items():
            adapter_info = TestContext.get_gfx_adapter_details()[adapter]
            platform = adapter_info.get_platform_info().PlatformName.upper()
            simulation_type = env_settings.get('SIMULATION', 'simulation_type')

            # skip powerwell verification for SHE emulator tests on TGL, as we saw PG status
            # is not clearing even after unplug EFP on some TGL systems
            if platform == 'TGL' and simulation_type == 'SHE':
                self.display_engine.remove_verifiers(VerificationMethod.POWERWELL)

            if bool(displays):
                # Skip DVFS verification if not enabled in below platforms
                if platform in ['MTL', 'LNL', 'PTL', 'NVL']:
                    logging.info(f"Verifying Voltage Level notified to PCode for {platform}")
                    if display_clock.DisplayClock.verify_voltage_level_notified_to_pcode(adapter, displays) is False:
                        logging.error(f"FAIL: DVFS VoltageLevel verification failed for {displays} on {adapter}")
                        gdhm.report_driver_bug_pc("[Interfaces][Display_Engine][CD Clock] Failed to verify "
                                                  "Voltage level during display detection scenario",
                                                  gdhm.ProblemClassification.FUNCTIONALITY)
                    else:
                        logging.info("PASS: DVFS VoltageLevel verification successful")
                else:
                    logging.warning(f"Skipping DVFS VoltageLevel verification for unsupported platform : {platform}.")
            else:
                logging.warning(f"No displays connected in {platform}. Skipping DVFS verification!")

            self.de_flag.append(self.display_engine.verify_display_engine(portList=displays, gfx_index=adapter))

    ##
    # @brief helper function to get stop & start ETL, and to parse ETL to get HPD live state data
    # @return dictionary of (ports : port connector types) that are enumerated in ETL
    def get_hpd_live_state_data_from_ETL(self):

        # Take ETL and parse it for HPD live state event, to find out which ports and connector types are enumerated
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer (Test Issue)")
        file_name = "GfxTrace_display_detection_" + str(time.time()) + ".etl"
        new_etl_file = os.path.join(LOG_FOLDER, file_name)

        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")

        # Rename the ETL file to avoid overwriting
        shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_etl_file)

        # Again start ETL trace
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer (Test Issue)")

        # Generate reports from ETL file using EtlParser
        if etl_parser.generate_report(new_etl_file) is False:
            self.fail("Failed to generate EtlParser report")

        # Look for HPD live state events in ETL
        hpd_live_state_output = etl_parser.get_HPD_data(etl_parser.Events.HPD_LIVE_STATE)
        if hpd_live_state_output is None:
            gdhm.report_bug(
                title="[Interfaces][Display_Config] No HPD live state events found in ETL taken during plug display",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail("\tNo HPD live state events found in ETL taken during plug display (Driver Issue)")

        PORT_CONNECTOR_TYPE_MAP = {
            "NATIVEPORT": "NATIVE",
            "TYPECPORT": "TC",
            "TBTPORT": "TBT",
        }

        enumerated_ports_from_etl = {}
        for hpd_live_state_event in hpd_live_state_output:
            enumerated_ports_from_etl[hpd_live_state_event.Port] = \
                PORT_CONNECTOR_TYPE_MAP.get(hpd_live_state_event.PortConnectorType)

        return enumerated_ports_from_etl
