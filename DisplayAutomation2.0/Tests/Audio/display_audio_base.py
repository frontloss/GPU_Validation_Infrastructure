################################################################################################################################
# @file              display_audio_base.py
# @brief             AudioBase class contains the common APIs used for audio endpoint and playback verification.
#                    AudioBase provides common setUp() functions of UnitTest Framework.
# @details           Contains all verification functions of audio driver/controller. Also contains functions to invoke
#                    power event and to verify the CS/Non-CS system. It also contains functions to set display config
#                    for both MST and Non-MST cases
# @author            Sridharan.v, Kumar, Rohit
################################################################################################################################

import logging
import os
import re
import shutil
import subprocess
import sys
import time
import unittest
import tempfile
from typing import Dict

import DisplayRegs
from DisplayRegs import DisplayArgs, DisplayRegsService
from Libs.Core import display_power, cmd_parser, enum, display_utility, registry_access
from Libs.Core.display_power import MonitorPower, PowerEvent, PowerSource
from Libs.Core import system_utility as sys_utility
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, DisplayConfigTopology
from Libs.Core.display_config.display_config_struct import DisplayConfig
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import dp_mst, gfxvalsim
from Libs.Core.test_env import test_context
from Libs.Core.Verifier.common_verification_args import VerifierCfg
from Libs.Core.sw_sim import driver_interface
from Libs.Core import display_essential
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumXMLParser
from Libs.Feature import display_audio as audio
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_audio import AudioCodecDriverType, AudioControllerType, AudioPowerState
from Libs.Feature.vdsc import dsc_verifier


# POWER_EVENT_DURATION - Power event duration
POWER_EVENT_DURATION = 30
# MTO_EVENT_DURATION - Monitor turn off duration
MTO_EVENT_DURATION = 5

# AUDIO_D3_TIMEOUT - Codec/Controller D3 timeout duration
AUDIO_D3_TIMEOUT = 90

# AUDIO_ENDPOINT_ENUMERATION_DURATION - Audio endpoint enumeration duration
AUDIO_ENDPOINT_ENUMERATION_DURATION = 20

# MST_TOPOLOGY - DP1.2 MST topology
MST_TOPOLOGY = "MST"

# MST_1B_1D_XML - xml file name for 1 branch 1 MST display
MST_1B_1D_XML = "DPMST_1Branch_1MSTDisplay.xml"
# MST_1B_2D_XML - xml file name for 1 branch 2 MST displays
MST_1B_2D_XML = "DPMST_1Branch_2MSTDisplays.xml"
# MST_1B_3D_XML - xml file name for 1 branch 3 MST displays
MST_1B_3D_XML = "DPMST_1Branch_3MSTDisplays.xml"

# MST_DISPLAY_XML - xml file for sub display for DP MST topology
MST_DISPLAY_XML = "SubDisplay_DELL_U3014.xml"

# DPCD_VERSION_OFFSET - Offset for dpcd version
DPCD_VERSION_OFFSET = 0x0
# DP_HOTPLUG_GOLDEN_VALUE - Value for DP hotplug
DP_HOTPLUG_GOLDEN_VALUE = 0x00000001
# DPCD_MSTM_CAP_OFFSET - Offset to verify MST displays
DPCD_MSTM_CAP_OFFSET = 0x21
# MST_PLUG_SUCCESS - MST plug status
MST_PLUG_SUCCESS = 0
# MST_UNPLUG_SUCCESS - MST unplug status
MST_UNPLUG_SUCCESS = 4

# AUDIO_WPP_PATH - WPP log file path
AUDIO_WPP_PATH = os.path.join(test_context.TEST_STORE_FOLDER + "\\CommonBin\\CustomTraceEvents\\DAC_Tracer")
# ACX_MATTHEW_PATH - ACX log file path
ACX_MATTHEW_PATH = os.path.join(test_context.TEST_STORE_FOLDER + "\\CommonBin\\CustomTraceEvents\\ACX_Tracer")
DEVCON_EXE_PATH = test_context.TestContext.devcon_path()
# Audio supported formats
AUDIO_CHANNEL = {'channel': {2, 4, 6, 8}, 'bit_depth': {16, 24},
                 'sample_rate': {44100, 48000, 88200, 96000, 176400, 192000}}


##
# @class AudioBase
# @brief Common Base Class for Audio Test Cases
class AudioBase(unittest.TestCase):
    command_line_tags = ['-BUS_DRIVER', '-MST', '-D3', '-HOTPLUG', '-POWER_EVENT', '-ITERATION', '-VDSC', '-PLAY',
                         '-MULTI_CHANNEL', '-XML', '-POWER', '-DP2_SPLITTING']
    cmd_line_param = None

    # Playback verification
    audio_playback_config = {'channel': 2, 'bit_depth': 16, 'sample_rate': 48000}
    sgpc_supported_platforms = ['TGL', 'LKF1', 'RKL', 'ADLS', 'JSL', 'ADLP', 'EHL', 'MTL', 'RPLS', 'LNL', 'PTL']

    # Logging Info
    test_name = "Audio Test"
    step_counter = 0
    expected_audio_driver = AudioCodecDriverType.INTEL
    driver_interface_ = driver_interface.DriverInterface()
    display_list = []
    mst_gfx_list = []
    audio_endpoint_dict = {}


    # MST
    mst_displays = 0
    mst_topology_xml = None
    mst_display_xml = None
    driver_info = None
    mst_port = None
    topology = None
    mst_rad = None

    is_simbatt_enabled = False
    is_test_step = False
    d3_controller = False
    vdsc_status = False
    adsp_driver = False
    mst_status = False
    d3_status = False
    d3_codec = False
    dp2 = False

    # Hot plug / Unplug
    hotplug_status = False
    hotplug_mode = None
    hotplug_event = None
    internal_display = None
    channel = None
    bit_depth = None

    # Power Event
    power_event_status = False
    power_event_type = None
    power_event_mto = False
    power_event_str = None
    cs_enabled = None
    iterations = 1

    is_audio_driver_installed = True
    is_gfx_driver_enabled = True
    is_audio_codec_driver_enabled = True
    is_audio_controller_enabled = True
    multi_channel = True
    audio_capable = False
    sdp_splitting = False
    power_event = False
    power = ""

    enumerated_displays = None
    plugged_display = []
    plugged_display_list = []
    config_list = []
    mst_port_list = []

    system_utility = sys_utility.SystemUtility()
    display_config = disp_cfg.DisplayConfiguration()
    display_power = display_power.DisplayPower()
    display_audio = audio.DisplayAudio()
    machine_info = SystemInfo()
    display_port = None
    gfx_val_sim = None
    xml_parser = None
    mode_enum_parser_dict: Dict[str, ModeEnumXMLParser] = {}

    # WPP logging
    move_wpp_logs = False

    # Matthew logs
    move_matthew_logs = False

    # Start Matthew logs check
    start_matthew_logs = False

    # Acx error , Matthew logs
    acx_matthew_error = False

    ##
    # @brief Unit Test Setup Function
    # @return None
    def setUp(self):
        xml_file_list = []
        cmd_line_param_data = cmd_parser.parse_cmdline(sys.argv, self.command_line_tags)

        if type(cmd_line_param_data) is not list:
            cmd_line_param_data = [cmd_line_param_data]

        for element in cmd_line_param_data:
            # Except Display information, other parameters are common across all adapters,
            # since using last adapter's value
            self.cmd_line_param = element
            self.mst_port_list = []
            for key, value in self.cmd_line_param.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if value['gfx_index'] == None:
                            value['gfx_index'] = 'gfx_0'
                        self.mst_gfx_list.append(value['gfx_index'])
                if self.cmd_line_param['MST'] != 'NONE':
                    if self.cmd_line_param['MST'][0] == key:
                        self.mst_port_list.append({value['connector_port']: value})
                        continue
                if cmd_parser.display_key_pattern.match(key) is not None:
                    self.display_list.append({value['connector_port']: value})

            # XML has to be given in case of SDP Splitting
            if self.cmd_line_param['XML'] != 'NONE':
                xml_file_list = self.cmd_line_param['XML']
                self.sdp_splitting = True

            if self.cmd_line_param['POWER'] != 'NONE':
                self.power_event = True
                self.power = self.cmd_line_param['POWER'][0]

            platform = None
            adapter_dict = test_context.TestContext.get_gfx_adapter_details()
            for gfx_index in adapter_dict.keys():
                platform = self.machine_info.get_platform_details(adapter_dict[gfx_index].deviceID).PlatformName

            for display in self.mst_port_list:
                self.mst_status = True
                port_name = list(display.keys())[0]
                self.mst_port = display[port_name]['connector_port']
                if self.sdp_splitting is not True:
                    self.mst_displays = int(self.cmd_line_param['MST'][1])
                    self.mst_display_xml = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE",
                                                        MST_DISPLAY_XML)
                    if self.mst_displays == 1:
                        self.mst_topology_xml = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE",
                                                             MST_1B_1D_XML)
                    elif self.mst_displays == 2:
                        self.mst_topology_xml = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE",
                                                             MST_1B_2D_XML)
                    elif self.mst_displays == 3:
                        self.mst_topology_xml = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE",
                                                             MST_1B_3D_XML)
                    else:
                        logging.error("\tERROR: Invalid value '{0}' for '-MST'".format(self.cmd_line_param['MST'][1]))
                        self.mst_topology_xml = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE",
                                                             MST_1B_1D_XML)

                # Make sure port given for MST is free
                gfx_index = display[port_name]['gfx_index']
                if platform not in ["ELG"]:
                    if self.mst_port not in disp_cfg.get_free_ports(gfx_index.lower()):
                        gdhm.report_driver_bug_audio(
                            title="[Audio] Given MST port {0} is not free".format(self.mst_port))
                        self.fail("Given MST port {0} is not free".format(self.mst_port))

        if self.mst_status is True:
            self.display_port = dp_mst.DisplayPort()
            self.gfx_val_sim = gfxvalsim.GfxValSim()

            if self.sdp_splitting is True:

                for port, gfx_index, xml_file_name in zip(self.mst_port_list, self.mst_gfx_list, xml_file_list):
                    xml_parser = ModeEnumXMLParser(gfx_index, list(port)[0], xml_file_name)
                    # Set and verify DP MST topology
                    self.set_and_verify_mst(list(port)[0], MST_TOPOLOGY, xml_parser.mst_topology_path)
                    xml_parser.parse_and_construct_mode_tables()
                    self.mode_enum_parser_dict[list(port)[0]] = xml_parser

        if (self.mst_status is True) and (self.mst_displays > 1):
            for mst_disp in self.mst_port_list:
                self.display_list.append(mst_disp)

        self.verify_audio_driver()

        # Set VDSC based on command line
        if self.cmd_line_param['VDSC'] != 'NONE':
            if self.cmd_line_param['VDSC'][0] == 'TRUE':
                self.vdsc_status = True

        if self.cmd_line_param['MULTI_CHANNEL'] != 'NONE':
            self.multi_channel = True
            user_input = self.cmd_line_param['MULTI_CHANNEL'][0]
            self.channel = int(re.findall(r"(\d+)c", user_input, re.IGNORECASE)[0])
            self.bit_depth = int(re.findall(r"(\d+)b", user_input, re.IGNORECASE)[0])

        # ADSP/MSFT based on the command line
        if self.cmd_line_param['BUS_DRIVER'] != 'NONE':
            if self.cmd_line_param['BUS_DRIVER'][0] == 'ADSP':
                self.adsp_driver = True
            elif self.cmd_line_param['BUS_DRIVER'][0] == 'MSFT':
                self.adsp_driver = False
            else:
                gdhm.report_test_bug_audio(
                    title="[Audio] ERROR: Invalid value '{0}' for '-BUS_DRIVER'".format(self.cmd_line_param[
                                                                                            'BUS_DRIVER'][0]))
                self.fail(
                    "\tERROR: Invalid value '{0}' for '-BUS_DRIVER'".format(self.cmd_line_param['BUS_DRIVER'][0]))

        # Get topology from command line parameters
        self.topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))

        # set D3 based on the command line
        if self.cmd_line_param['D3'] != 'NONE':
            self.d3_status = True
            if 'CODEC' in self.cmd_line_param['D3'] or 'CONTROLLER' in self.cmd_line_param['D3'] or \
                    'AC' in self.cmd_line_param['D3']:
                self.d3_codec = True
                self.d3_controller = True

            if 'AC' not in self.cmd_line_param['D3']:
                # Enable Simulated Battery
                if self.display_power.enable_disable_simulated_battery(True) is False:
                    self.fail("\tFailed to enable simulated battery")
                else:
                    self.is_simbatt_enabled = True

                # Set power line status as DC
                self.set_power_line()

        # set HOTPLUG based on the command line
        if self.cmd_line_param['HOTPLUG'] != 'NONE':
            self.hotplug_status = True

            # Check for hot plug scenario with power events
            if self.cmd_line_param['HOTPLUG'][0] != 'TRUE':
                if self.cmd_line_param['HOTPLUG'][0] == 'AFTER':
                    self.hotplug_mode = 'AFTER'
                elif self.cmd_line_param['HOTPLUG'][0] == 'IN':
                    self.hotplug_mode = 'IN'
                else:
                    logging.error(
                        "\tERROR: Invalid value '{0}' for '-HOTPLUG'".format(self.cmd_line_param['HOTPLUG'][0]))
                    self.hotplug_mode = 'AFTER'

                self.power_event_status = True
                expected_cs_status = None
                if self.cmd_line_param['HOTPLUG'][1] == 'CS':
                    self.power_event_type = PowerEvent.CS
                    self.power_event_str = "CS"
                    expected_cs_status = True

                if self.cmd_line_param['HOTPLUG'][1] == 'MTO':
                    self.power_event_type = MonitorPower.OFF_ON
                    self.power_event_mto = True
                    self.power_event_str = "Monitor Turn Off"
                    expected_cs_status = False

                if self.cmd_line_param['HOTPLUG'][1] == 'S3':
                    self.power_event_type = PowerEvent.S3
                    self.power_event_str = "S3"
                    expected_cs_status = False

                if self.cmd_line_param['HOTPLUG'][1] == 'S4':
                    self.power_event_type = PowerEvent.S4
                    self.power_event_str = "S4"
                    expected_cs_status = None

                if self.cmd_line_param['HOTPLUG'][1] == 'DISABLE_ENABLE':
                    self.hotplug_event = 'DISABLE_ENABLE'
                    self.power_event_status = False

                if self.cmd_line_param['HOTPLUG'][1] == 'DISABLE_ENABLE_CTRL':
                    self.hotplug_event = 'DISABLE_ENABLE_CTRL'
                    self.power_event_status = False

                if self.cmd_line_param['HOTPLUG'][1] == 'INSTALL_UNINSTALL':
                    self.hotplug_event = 'INSTALL_UNINSTALL'
                    self.power_event_status = False

                # Make sure system CS state is as expected
                if expected_cs_status is not None:
                    self.base_verify_cs_system(expected_status=expected_cs_status)

            # Make sure all external ports are free before starting the hot-plug/unplug test
            for display in self.display_list:
                display_port = list(display.keys())[0]
                gfx_index = display[display_port]['gfx_index'].lower()
                display_port = (display[display_port]['connector_port'])

                if platform not in ["ELG"]:
                    if (display_port not in disp_cfg.get_free_ports(gfx_index)) and (
                            display_utility.get_vbt_panel_type(display_port, gfx_index) not in
                            [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]):
                        gdhm.report_test_bug_audio(
                            title="[Audio] Expected {0} port status= Free, Actual= Not Free".format(display_port))
                        self.fail("Expected {0} port status= Free, Actual= Not Free".format(display_port))

        # set POWER_EVENT based on the command line
        if self.cmd_line_param['POWER_EVENT'] != 'NONE':

            self.power_event_status = True
            expected_cs_status = False
            if self.cmd_line_param['POWER_EVENT'][0] == 'CS':
                self.power_event_type = PowerEvent.CS
                self.power_event_str = "CS"
                expected_cs_status = True

            if self.cmd_line_param['POWER_EVENT'][0] == 'MTO':
                self.power_event_type = MonitorPower.OFF_ON
                self.power_event_mto = True
                self.power_event_str = "Monitor Turn Off"
                expected_cs_status = False

            if self.cmd_line_param['POWER_EVENT'][0] == 'S3':
                self.power_event_type = PowerEvent.S3
                self.power_event_str = "S3"
                expected_cs_status = False

            if self.cmd_line_param['POWER_EVENT'][0] == 'S4':
                self.power_event_type = PowerEvent.S4
                self.power_event_str = "S4"
                expected_cs_status = None

            # Make sure system CS state is as expected
            if expected_cs_status is not None:
                self.base_verify_cs_system(expected_status=expected_cs_status)

        # set ITERATION based on the command line
        if self.cmd_line_param['ITERATION'] != 'NONE':
            if self.cmd_line_param['ITERATION'][0] and int(self.cmd_line_param['ITERATION'][0]) > 1:
                self.iterations = int(self.cmd_line_param['ITERATION'][0])

        # Enable ACX logging only if ACX supported platforms is present
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for index in adapter_dict.keys():
            dut_info = self.machine_info.get_platform_details(adapter_dict[index].deviceID)
            # ACX is not supported for EHL, since we are getting Platform name as "JSL" for EHL. Re-assign
            # platform name based on SKU name
            if dut_info.PlatformName == "JSL" and dut_info.SkuName == "EHL":
                platform = "EHL"
            else:
                platform = dut_info.PlatformName

            if platform not in self.display_audio.non_acx_platforms:
                # Pre cleanup Matthew log file
                self.acx_matthew_log_cleanup()
                # start Matthew logs.
                self.start_acx_matthew_logging()
                self.start_matthew_logs = True
                break

        # Audio Playback file
        if self.cmd_line_param['PLAY'] != 'NONE':
            VerifierCfg.audio_playback_verification = True
            user_input = self.cmd_line_param['PLAY'][0]
            audio_sample = {'channel': 0, 'bit_depth': 0, 'sample_rate': 0}

            try:
                audio_sample['channel'] = int(re.findall(r"(\d+)c", user_input, re.IGNORECASE)[0])
                audio_sample['bit_depth'] = int(re.findall(r"(\d+)b", user_input, re.IGNORECASE)[0])
                sample_rate = re.findall(r"(\d*\.?\d+)k", user_input, re.IGNORECASE)[0]
                audio_sample['sample_rate'] = int(float(sample_rate) * 1000)
            except (IndexError, ValueError):
                logging.error("Invalid Input for Parameter -play : {0}".format(user_input))
                gdhm.report_test_bug_audio(
                    title="[Audio] Invalid input parameter for -Play [(channel)c(bit_depth)b(sample_rate)k]")
                self.fail("Invalid input parameter for -Play [(channel)c(bit_depth)b(sample_rate)k]")

            self.audio_playback_config['channel'] = audio_sample['channel']
            self.audio_playback_config['bit_depth'] = audio_sample['bit_depth']
            self.audio_playback_config['sample_rate'] = audio_sample['sample_rate']

        self.audio_device_info = self.display_audio.controller_adapter
        if self.audio_device_info.status is False:
            logging.error("Unable to Find/Map Audio Controller and Gfx Display Adapter")
            self.fail("Unable to Find/Map Audio Controller and Gfx Display Adapter")

        logging.debug("Controller Information: ".format(self.audio_device_info))

        # starting Audio WPP logs.
        self.start_audio_logging()

    ##
    # @brief Start Audio Codec WPP Logging
    # @return None
    def start_audio_logging(self):
        start_audio_wpp_cmd = (AUDIO_WPP_PATH + "\\DAC_Trace.Start.bat")
        os.system(start_audio_wpp_cmd)

    ##
    # @brief Stop Audio Codec WPP Logging
    # @return None
    def stop_audio_logging(self):
        stop_audio_wpp_cmd = (AUDIO_WPP_PATH + "\\DAC_Trace.Stop.bat")
        os.system(stop_audio_wpp_cmd)

    ##
    # @brief copy WPP etl file to LOGS folder
    # @return None
    def copy_wpplogs(self):
        for _file in os.listdir(AUDIO_WPP_PATH):
            if _file == "DACTrace.etl":
                source_path = (AUDIO_WPP_PATH + "\\DACTrace.etl")
                shutil.move(source_path, test_context.LOG_FOLDER)

    ##
    # @brief Start Acx Matthew Logging
    # @return None
    def start_acx_matthew_logging(self):
        script = os.path.join(ACX_MATTHEW_PATH, 'StartAudioLogs.ps1')
        new_command = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File \"{0}\"".format(script)
        var = subprocess.Popen(new_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = var.communicate()
        Acx_error = str(err.decode())
        if Acx_error.find('Error') != -1:
            logging.warning('Start ACX DAC tracing failed')
            self.acx_matthew_error = True

    ##
    # @brief Stop Acx Matthew Logging
    # @return None
    def stop_acx_matthew_logging(self):
        script = os.path.join(ACX_MATTHEW_PATH, 'StopAudioLogs.ps1')
        new_command = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File \"{0}\"".format(script)
        var = subprocess.Popen(new_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = var.communicate()
        Acx_error = str(err.decode())
        if Acx_error.find('Error') != -1:
            logging.warning('Stop ACX DAC tracing failed')
            self.acx_matthew_error = True

    ##
    # @brief Moving Acx Matthew Logs
    # @return None
    def copy_acx_matthew_log(self):
        if 'Acx_Matthew_Log.zip' in os.listdir(ACX_MATTHEW_PATH):
            source_path = os.path.join(ACX_MATTHEW_PATH, 'Acx_Matthew_Log.zip')
            os.replace(source_path, os.path.join(test_context.LOG_FOLDER, 'Acx_Matthew_Log.zip'))
        else:
            logging.warning('Acx Matthew Log not found')

    ##
    # @brief Removing temp Matthew Logs file
    # @return None
    def acx_matthew_log_cleanup(self):
        temp_path = tempfile.gettempdir()
        try:
            if 'Acx_Matthew_Log' in os.listdir(temp_path):
                self.stop_acx_matthew_logging()
                if 'Acx_Matthew_Log' in os.listdir(temp_path):
                    os.remove(os.path.join(temp_path, 'Acx_Matthew_Log'))
            if 'Acx_Matthew_Log.zip' in os.listdir(ACX_MATTHEW_PATH):
                os.remove(os.path.join(ACX_MATTHEW_PATH, 'Acx_Matthew_Log.zip'))
            self.acx_matthew_error = False
        except Exception:
            logging.warning('Unable to clear previous mathew log session')
            self.acx_matthew_error = True

    ##
    # @brief Read ADSP Regkey to set expected audio controller
    # @return AudioControllerType Enum (INTEL / MS)
    def get_igpu_expected_audio_controller(self):

        # Same Content is enabled for both MS Bus Driver and ISST Bus driver. Verify Expected audio controller
        # based on Registry value "HKEY_CURRENT_USER\\DisplayAutomation\\ADSP\\ADSPDriverTesting"
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER, reg_path="")
        reg_value, reg_type = registry_access.read(args=legacy_reg_args, reg_name="ADSPDriverTesting",
                                                   sub_key=r"DisplayAutomation\ADSP")
        if reg_value == 1 or self.adsp_driver:
            exp_controller = AudioControllerType.INTEL
        else:
            exp_controller = AudioControllerType.MS

        return exp_controller


    ##
    # @brief Verifies expected audio codec driver is present or not
    # @return None
    def verify_audio_driver(self):
        error_check = False
        failure_msg = ""
        # Gets the audio controller type(MS/Intel). Fails the test if audio controller is None.
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()

        for gfx_index in adapter_dict.keys():
            platform = self.machine_info.get_platform_details(adapter_dict[gfx_index].deviceID).PlatformName
            sku = self.machine_info.get_platform_details(adapter_dict[gfx_index].deviceID).SkuName

            # Following Feature will differ between JSL and EHL. Since we are getting platform name as JSL for
            # both JSL and EHL, update the platform name based on SKU.
            # SGPC  = JSL: Enabled | EHL: Disabled
            # Codec = JSL: ACX     | EHL: Intel
            if platform == "JSL" and sku == "EHL":
                platform = 'EHL'

            audio_controller, device_id, version = self.display_audio.get_audio_controller(gfx_index)

            if audio_controller == AudioControllerType.NONE:
                gdhm.report_driver_bug_audio(title="[Audio] No Audio Controller loaded for {0}".format(platform))
                self.fail("No Audio Controller loaded for {0}".format(platform))

            if audio_controller == AudioControllerType.INTEL:
                oed_status, oed_version = self.display_audio.get_oed_status()
                if oed_status is not True:
                    self.fail("Intel OED Controller is not loaded/yellow bang observed")

            platform_is_dgpu = display_essential.is_discrete_graphics_driver(gfx_index)

            # dGPU supports only MS BUS driver. For iGPU, expected BUS driver will be decided based on ADSP regkey
            if platform_is_dgpu:
                expected_audio_controller = AudioControllerType.MS
            else:
                expected_audio_controller = self.get_igpu_expected_audio_controller()

            expected_audio_controller_str = audio.AudioControllerType(expected_audio_controller).name
            actual_audio_controller_str = audio.AudioControllerType(audio_controller).name

            log_str = "Audio Controller for {2} Expected: {0} Actual: {1}".format(expected_audio_controller_str,
                                                                                  actual_audio_controller_str, platform)
            if audio_controller != expected_audio_controller:
                logging.error("Fail: {0}".format(log_str))
                gdhm.report_driver_bug_audio(title="[Audio] {0}".format(log_str))
                error_check = True
                failure_msg = "Expected Audio Controller not available"

            # Verify SGPC Status
            is_sgpc_enabled = self.display_audio.is_sgpc_enabled(gfx_index)

            # Check for SGPC status and fail if not as below
            if platform in self.sgpc_supported_platforms:
                if is_sgpc_enabled is False:
                    gdhm.report_driver_bug_audio(title="[Audio] SGPC is not getting enabled in {0}".format(platform))
                    error_check = True
                    failure_msg = "\tSGPC is not getting enabled in {0}".format(platform)
            else:
                if is_sgpc_enabled is True:
                    gdhm.report_driver_bug_audio(title="[Audio] SGPC is getting enabled in {0}".format(platform))
                    error_check = True
                    failure_msg = "\tSGPC is getting enabled in {0}".format(platform)

            # Codec Verification
            # Check active panel is audio capable or not.
            active_audio_panel = False
            audio_capable = False

            if platform in ["ELG"]:
                audio_capable = True
            else:
                # Check for any active audio capable panel
                enumerated_displays = self.display_config.get_enumerated_display_info()
                for display_index in range(enumerated_displays.Count):
                    if enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                        active_audio_panel |= self.display_audio.is_audio_capable(
                            enumerated_displays.ConnectedDisplays[display_index].TargetID)
                        if active_audio_panel is True:
                            audio_capable = True

            is_audio_capable_efp_present = self.display_audio.is_external_display_present(gfx_index) and audio_capable

            actual_audio_codec = self.display_audio.get_audio_driver(gfx_index)
            actual_audio_codec_str = audio.AudioCodecDriverType(actual_audio_codec).name
            expected_audio_codec = None
            gdhm_error_msg = ""
            os_information = SystemInfo().get_os_info()
            if int(os_information.BuildNumber) > 18282 and platform in ['EHL']:
                if 'EHL' in self.display_audio.non_acx_platforms:
                    self.display_audio.non_acx_platforms.remove('EHL')

            if is_sgpc_enabled is True:
                # For EFP display, ACX Codec to be loaded for ACX Supported platforms and
                # Intel Codec to be loaded for other platforms.
                if is_audio_capable_efp_present is True:
                    if platform not in self.display_audio.non_acx_platforms:
                        expected_audio_codec = AudioCodecDriverType.ACX
                        if actual_audio_codec != expected_audio_codec:
                            gdhm_error_msg = "[Audio] ACX Audio Codec is not loaded with external panel connected"
                    else:
                        expected_audio_codec = AudioCodecDriverType.INTEL
                        if actual_audio_codec != expected_audio_codec:
                            gdhm_error_msg = "[Audio] Intel Audio Codec is not loaded with External Audio capable panel connected and Active"
                # For LFP Display, When SGPC is enabled, Audio codec should not be loaded.
                else:
                    expected_audio_codec = AudioCodecDriverType.NONE
                    if actual_audio_codec != expected_audio_codec:
                        gdhm_error_msg = "[Audio] {0} is loaded with LFP when SGPC is enabled".format(
                            actual_audio_codec_str)
            else:
                # If SGPC is not enabled. For both LFP & EFP, ACX Codec to be loaded for ACX Supported platforms and
                # Intel Codec to be loaded for other platforms.
                if is_audio_capable_efp_present is True:
                    if platform not in self.display_audio.non_acx_platforms:
                        expected_audio_codec = AudioCodecDriverType.ACX
                        if actual_audio_codec != expected_audio_codec:
                            gdhm_error_msg = "[Audio] ACX Audio Codec is not loaded with external panel connected"
                    else:
                        expected_audio_codec = AudioCodecDriverType.INTEL
                        if actual_audio_codec != expected_audio_codec:
                            gdhm_error_msg = "[Audio] Intel Audio Codec is not loaded with External Audio capable panel connected and Active"
                else:
                    if platform not in self.display_audio.non_acx_platforms:
                        expected_audio_codec = AudioCodecDriverType.ACX
                        if actual_audio_codec != expected_audio_codec:
                            gdhm_error_msg = "[Audio] ACX Audio Codec is not loaded with LFP when SGPC is disabled"
                    else:
                        expected_audio_codec = AudioCodecDriverType.INTEL
                        if actual_audio_codec != expected_audio_codec:
                            gdhm_error_msg = "[Audio] Intel Audio Codec is not loaded with LFP when SGPC is disabled"

            expected_audio_codec_str = audio.AudioCodecDriverType(expected_audio_codec).name
            audio_codec_driver_version = None

            if actual_audio_codec == AudioCodecDriverType.INTEL:
                audio_codec_driver_version = self.display_audio.get_audio_driver_version(actual_audio_codec, gfx_index)

            if audio_codec_driver_version is None:
                logging_msg = "Expected= {0} Actual= {1}".format(expected_audio_codec_str, actual_audio_codec_str)
            else:
                logging_msg = "Expected= {0} Actual= {1}  (Version: {0})".format(
                    expected_audio_codec_str, actual_audio_codec_str, audio_codec_driver_version)

            if expected_audio_codec != actual_audio_codec:
                logging.error("\tFAIL: Codec for {0} {1}".format(gfx_index, logging_msg))
                gdhm.report_driver_bug_audio(title=gdhm_error_msg)
                error_check = True
                failure_msg = gdhm_error_msg[8:]
            sgpc_status = "Enabled" if is_sgpc_enabled == 1 else "Disabled"
            logging.info(f"PLATFORM          :     {platform}")
            logging.info(f"CONTROLLER LOADED :     {audio.AudioControllerType(audio_controller).name}")
            logging.info(f"CONTROLLER DID    :     {device_id}")
            logging.info(f"SGPC STATUS       :     {sgpc_status}")
            logging.info(f"CODEC LOADED      :     {audio.AudioCodecDriverType(actual_audio_codec).name}")
            if audio.AudioCodecDriverType(actual_audio_codec).name != 'NONE':
                logging.info(f"CODEC ID          :     {self.display_audio.codec_id}")
            if audio.AudioControllerType(audio_controller).name == 'INTEL':
                logging.info(f"BUS DRIVER VERSION: {version}")
                logging.info(f"OED VERSION       : {oed_version}")
            if error_check:
                self.fail(failure_msg)

    ##
    # @brief Verifies audio endpoint enumeration
    # @return bool
    def verify_audio_playback(self):
        result_list = []
        endpoint_name_list = []
        audio_capable_displays = 0

        endpoint_name_info = subprocess.check_output([DEVCON_EXE_PATH, "status",
                                                      "MMDEVAPI\AudioEndpoints"],
                                                     universal_newlines=True)
        string = "HD Audio Driver for Display Audio"
        if re.search(r'Name', endpoint_name_info, re.I):
            lines = endpoint_name_info.split("\n")
            for line in range(len(lines)):
                if (lines[line].find(string)) != -1:
                    last_index = lines[line].find("(")
                    endpoint_name = lines[line][10:last_index - 1]
                    endpoint_name_list.append(endpoint_name)
        if len(endpoint_name_list) > 1:
            for end_name in range(len(endpoint_name_list)):
                if endpoint_name_list[end_name] == endpoint_name_list[end_name + 1]:
                    for display in self.display_list:
                        display_port = list(display.keys())[0]
                        if display_port != self.mst_port and display[display_port]['is_lfp'] is False:
                            self.base_unplug(display)
                    for display in self.display_list:
                        self.base_hot_plug(display)
                break

        # Get Connected Endpoint Name Info
        endpoint_names = []
        endpoint_name_info = subprocess.check_output([DEVCON_EXE_PATH, "status",
                                                      "MMDEVAPI\AudioEndpoints"],
                                                     universal_newlines=True)
        for line in endpoint_name_info:
            if "Name" in line and "HD Audio Driver for Display Audio" in line:
                brace_index = line.find("(")
                endpoint_names.append(line[10:brace_index - 1])


        # Get Panel Name and Port Info
        port_and_device = {}
        get_config = self.display_config.get_current_display_configuration()
        current_config = get_config.to_string(self.enumerated_displays).split(' ')
        for i in range(get_config.numberOfDisplays):
            name = get_config.displayPathInfo[i].displayAndAdapterInfo.MonitorFriendlyDeviceName
            port = current_config[i + 1]
            port_and_device[port] = name

        enum_displays = self.display_config.get_enumerated_display_info()
        if enum_displays.Count != 0:
            for i in range(enum_displays.Count):
                port = disp_cfg.cfg_enum.CONNECTOR_PORT_TYPE(enum_displays.ConnectedDisplays[i].ConnectorNPortType).name
                if enum_displays.ConnectedDisplays[i].IsActive is True:
                    display_adapter_info = enum_displays.ConnectedDisplays[i].DisplayAndAdapterInfo
                    if self.display_audio.is_audio_capable(display_adapter_info):
                        audio_capable_displays += 1

                        endpoint_name = port_and_device.get(port)
                        logging.info("\tVerifying Audio Playback for Port: {0} Audio Endpoint: {1}".format(
                            port, endpoint_name))
                        logging.info(
                            "\tAudio Playback Config: {0}-Channel {1}-BitDepth {2}Hz-SampleRate".format(
                                self.audio_playback_config['channel'],
                                self.audio_playback_config['bit_depth'],
                                self.audio_playback_config['sample_rate']))

                        status = self.display_audio.audio_playback_verification(
                            display_info=enum_displays.ConnectedDisplays[i],
                            channel=self.audio_playback_config['channel'],
                            bit_depth=self.audio_playback_config['bit_depth'],
                            sample_rate=self.audio_playback_config['sample_rate'],
                            end_point_name=endpoint_name)

                        if status:
                            result_list.append(status)
                            logging.info(f"\tPass: Audio Playback Verification success: {port}")
                        else:
                            result_list.append(status)
                            logging.info(f"\tFail: Audio Playback Verification failed: {port}")

        else:
            logging.error("No display devices found")
            return False

        if not self.mst_status and len(result_list) < audio_capable_displays:
            return False
        else:
            return True

    ##
    # @brief Verifies audio endpoint enumeration
    # @return None
    def verify_audio_endpoints(self):
        gfx_display_hwinfo = SystemInfo().get_gfx_display_hardwareinfo()

        status = False
        second_postfix = ''

        # Disable audio_verification logs
        self.display_audio.is_log_enabled = False
        for sec in range(AUDIO_ENDPOINT_ENUMERATION_DURATION):
            if sec > 1:
                second_postfix = 's'
            # Enable audio verification logs for final iteration
            if sec == (AUDIO_ENDPOINT_ENUMERATION_DURATION - 1):
                self.display_audio.is_log_enabled = True
            endpoint_status, endpoint_count = self.display_audio.audio_verification()
            if endpoint_status is True:
                logging.info(
                    "\tPASS: Display Audio endpoint verification passed successfully (~{0} second{1})".format(sec + 1,
                                                                                                              second_postfix))
                status = True
                # In Passing case, info log is not required. hence calling only incase of debug to avoid redundant calls
                if logging.root.level == logging.DEBUG:
                    self.display_audio.mmio_dumps()
                break
            time.sleep(1)

        if status is False:
            self.move_wpp_logs = True
            self.move_matthew_logs = True
            # Dumping All the Audio specific MMIO's in case of failure.
            self.display_audio.mmio_dumps()
            gdhm.report_driver_bug_audio(
                title="[Audio] Display Audio endpoint verification failed)".format(
                    AUDIO_ENDPOINT_ENUMERATION_DURATION))
            self.fail("\tDisplay Audio endpoint verification failed (~{0} seconds)".format(
                AUDIO_ENDPOINT_ENUMERATION_DURATION))

        if self.d3_codec is True or self.d3_controller is True:
            self.verify_audio_codec_d3_state()
            self.verify_audio_controller_d3_state()

        if VerifierCfg.audio_playback_verification is True:
            if endpoint_count != 0:
                playback_result = self.verify_audio_playback()
                if playback_result is True:
                    if self.d3_codec is True or self.d3_controller is True:
                        self.verify_audio_codec_d3_state()
                        self.verify_audio_controller_d3_state()
                    # Passing case->info log is not required, calling only incase of debug to avoid redundant calls
                    if logging.root.level == logging.DEBUG:
                        self.display_audio.mmio_dumps()
                else:
                    self.move_wpp_logs = True
                    self.move_matthew_logs = True
                    self.display_audio.mmio_dumps()
                    self.fail("\tDisplay Audio Playback verification failed")

    ##
    # @brief Verifies System is CS enabled or not
    # @param[in] expected_status - expected cs system status
    # @return None
    def base_verify_cs_system(self, expected_status=True):
        if expected_status is True:
            if self.display_power.is_power_state_supported(PowerEvent.CS) is True:
                logging.info("\tPASS: Expected CS System, Actual= CS System")
            else:
                self.fail("FAIL: Expected CS System, Actual= Non-CS System")
        else:
            if self.display_power.is_power_state_supported(PowerEvent.CS) is False:
                logging.info("\tPASS: Expected Non-CS System, Actual= Non-CS System")
            else:
                self.fail("FAIL: Expected Non-CS System, Actual= CS System")

    ##
    # @brief Invokes the specified power event
    # @param[in] power_event power event state to be invoked
    # @param[in] is_mto True/False for Monitor Turn Off Test Cases
    # @param[in] low_power_event True/False for low power events
    # @return None
    def base_invoke_power_event(self, power_event=PowerEvent.S3, is_mto=False, low_power_event=False):
        # Invoke Power event
        if is_mto is True:
            self.step_counter += 1
            if self.display_power.invoke_monitor_turnoff(MonitorPower.OFF_ON, MTO_EVENT_DURATION) is False:
                self.fail('Failed to invoke power event MONITOR_TURNOFF')
            else:
                logging.info("\tResumed from the power event MONITOR_TURNOFF successfully")
        else:
            self.step_counter += 1
            if self.display_power.invoke_power_event(power_event, POWER_EVENT_DURATION) is False:
                self.fail('Failed to invoke power event %s' % PowerEvent(power_event))
            else:
                logging.info("\tResumed from the power event %s successfully", power_event.name)

        # Check for codec
        self.verify_audio_driver()

    ##
    # @brief Hot plugs the given display
    # @param[in] display to be plugged in Ex: DP_C
    # @param[in] low_power  True/False for low power events
    # @param[in] is_mto True/False for monitor turn off test cases
    # @param[in] power_event power event to be triggered
    # @return bool ,True if hot plug is successful, False otherwise
    def base_hot_plug(self, display=None, low_power=False, is_mto=False, power_event=PowerEvent.S3):
        status = False
        active_audio_panel = False
        edid = None
        dpcd = None

        # Default EFP panel for DP and HDMI
        dp_edid = 'DP_3011.EDID'
        dp_dpcd = 'DP_3011_dpcd.txt'
        hdmi_edid = 'HDMI_Dell_3011.EDID'

        display_port = list(display.keys())[0]
        display_port_info = display[display_port]
        gfx_index = display_port_info['gfx_index'].lower()

        if 'HDMI' in display_port:
            if display_port_info['edid_name'] is None:
                edid = hdmi_edid
            else:
                edid = display_port_info['edid_name']
        elif 'DP' in display_port:
            if (display_port_info['edid_name'] is None) or (display_port_info['dpcd_name'] is None):
                edid = dp_edid
                dpcd = dp_dpcd
            else:
                edid = display_port_info['edid_name']
                dpcd = display_port_info['dpcd_name']

        if low_power is False:
            step_str = "\t"
            if self.is_test_step:
                step_str = "Step{0}: ".format(self.step_counter)
                self.step_counter += 1
            logging.info("{0}Hot plugging {1} panel on port {2} (Gfx: {3})".format(
                step_str, display_port.split('_')[0], display_port.split('_')[1], gfx_index))
            if display_utility.plug(port=display_port, edid=edid, dpcd=dpcd, is_low_power=low_power,
                                    port_type=display_port_info['connector_port_type'], gfx_index=gfx_index) is False:
                gdhm.report_test_bug_audio(
                    title="[Audio] Plugging of external display was unsuccessful".format(display_port))
                logging.error('Plugging of display %s was unsuccessful' % display_port)
                self.fail('Plugging of display %s was unsuccessful' % display_port)
            status = True
        else:
            if is_mto:
                if self.is_test_step is True:
                    logging.info("Step{0}: Hot plugging {1} panel on port {2} in MONITOR_TURNOFF".format(
                        self.step_counter, display_port.split('_')[0], display_port.split('_')[1]))
                    self.step_counter += 1
            else:
                if self.is_test_step is True:
                    logging.info("Step{0}: Hot plugging {1} panel on port {2} in {3}".format(
                        self.step_counter, display_port.split('_')[0], display_port.split('_')[1],
                        PowerEvent(power_event)))
                    self.step_counter += 1
            display_utility.plug(port=display_port, edid=edid, dpcd=dpcd, is_low_power=low_power,
                                 port_type=display_port_info['connector_port_type'], gfx_index=gfx_index)
            self.base_invoke_power_event(power_event=power_event, is_mto=is_mto, low_power_event=True)
            status = True

        # Check if hot plug is successful during power event
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if disp_cfg.is_display_attached(enumerated_displays, display_port, gfx_index) is False:
            gdhm.report_driver_bug_audio(
                title=f"[Audio] Plugging of external display with low_power {low_power} was unsuccessful")
            logging.error('Plugging of display {0} with low_power {1} was unsuccessful'.format(display_port, low_power))
            self.fail('Plugging of display {0} with low_power {1} was unsuccessful'.format(display_port, low_power))
        status = True

        self.print_current_topology(is_step=False)

        # For low_power = True case verify_audio_driver() is covered in base_invoke_power_event()
        if low_power is False:
            self.verify_audio_driver()

        if status is True:
            self.plugged_display.append(display)

        return status

    ##
    # @brief Unplugs the given display
    # @param[in] display (string) to be unplugged Ex: DP_C
    # @param[in] low_power True/False for low power events
    # @param[in] is_mto True/False for monitor turn off test cases
    # @param[in] power_event power event to be triggered
    # @return status True if unplug is successful, False otherwise
    def base_unplug(self, display=None, low_power=False, is_mto=False, power_event = PowerEvent.S3):
        status = False

        # Collect the display details in enumerated displays from cmdline
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        display_port = list(display.keys())[0]
        gfx_index = display[display_port]['gfx_index'].lower()

        if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                           display_utility.VbtPanelType.LFP_MIPI]:
            logging.error("\tFAIL:Unplug operation for internal display is not supported")
            return status
        if disp_cfg.is_display_attached(self.enumerated_displays, display_port, gfx_index) is False:
            logging.error("\tFAIL:%s is not plugged in", display_port)
            return status

        self.enumerated_displays = self.display_config.get_enumerated_display_info()

        step_str = "\t"
        if self.is_test_step:
            step_str = "Step{0}: ".format(self.step_counter)
            self.step_counter += 1
        for display_index in range(self.enumerated_displays.Count):
            if str(CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)) == display_port:
                try:
                    current_mode_edp = self.display_config.get_current_mode(
                        self.enumerated_displays.ConnectedDisplays[display_index].TargetID)
                    step_str += "Unplugging the panel {1} ({2}x{3}@{4}) from port {0} ({5})".format(
                        display_port, self.enumerated_displays.ConnectedDisplays[display_index].FriendlyDeviceName,
                        current_mode_edp.HzRes, current_mode_edp.VtRes, current_mode_edp.refreshRate, gfx_index)
                except Exception as e:
                    step_str += "Unplugging the panel {1} from port {0} ({2})".format(
                        display_port, self.enumerated_displays.ConnectedDisplays[display_index].FriendlyDeviceName,
                        gfx_index)
                break

        if low_power is False:
            logging.info(step_str)
            if display_utility.unplug(display_port, low_power, gfx_index=gfx_index) is False:
                gdhm.report_test_bug_audio(
                    title="[Audio] Failed to unplug display".format(display_port))
                logging.error("Failed to unplug display %s" % display_port)
                self.fail("Failed to unplug display %s" % display_port)
            status = True
        else:
            if is_mto:
                step_str += " in MONITOR_TURNOFF"
                logging.info(step_str)
            else:
                step_str += " in {0}".format(PowerEvent(power_event))
                logging.info(step_str)

            display_utility.unplug(display_port, low_power, gfx_index=gfx_index)
            self.base_invoke_power_event(power_event=power_event, is_mto=is_mto, low_power_event=True)

        # Check if hot plug is successful during power event
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if disp_cfg.is_display_attached(enumerated_displays, display_port, gfx_index) is True:
            gdhm.report_test_bug_audio(
                title=f"[Audio] Unplugging of external display with low_power {low_power} was unsuccessful")
            logging.error('Unplugging of display {0} with low_power {1} was unsuccessful'.format(display_port,
                                                                                                 low_power))
            self.fail('Unplugging of display {0} with low_power {1} was unsuccessful'.format(display_port, low_power))
        else:
            status = True

        self.print_current_topology(is_step=False)
        # For low_power = True case verify_audio_driver() is covered in base_invoke_power_event()
        if low_power is False:
            self.verify_audio_driver()

        if status is True:
            for dis in self.plugged_display:
                if isinstance(dis, dict):
                    for key, value in dis.items():
                        self.plugged_display.remove({key: value})
                elif isinstance(dis, str):
                    self.plugged_display.remove(dis)

        return status

    ##
    # @brief Helper function to print current display configuration
    # @param[in] is_step to log with/without step
    # @return None
    def print_current_topology(self, is_step=True):
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        if self.enumerated_displays.Count == 0:
            return

        get_config = self.display_config.get_current_display_configuration()
        current_config_str = get_config.to_string(self.enumerated_displays)
        current_config = current_config_str.split(' ')
        topology = current_config[0]
        for index in range(get_config.numberOfDisplays):
            current_mode = self.display_config.get_current_mode(get_config.displayPathInfo[index].targetId)
            panel_name = get_config.displayPathInfo[index].displayAndAdapterInfo.MonitorFriendlyDeviceName
            if panel_name == '':
                panel_name = 'None'
            temp = " {0} (TargetID= {1}, PanelName= \"{2}\", Res= {3}x{4}@{5})".format(
                current_config[index + 1],
                self.enumerated_displays.ConnectedDisplays[index].TargetID,
                panel_name,
                current_mode.HzRes,
                current_mode.VtRes,
                current_mode.refreshRate
            )
            topology += temp
        if self.is_test_step is True and is_step is True:
            logging.info("Step{0}: Current Topology= {1}".format(self.step_counter, topology))
            self.step_counter += 1
        if self.is_test_step is False or is_step is False:
            logging.info("\tCurrent Topology= {0}".format(topology))

    ##
    # @brief set_and_verify_MST() function call is used to build a DP1.2 Topology
    # @param[in] port_type  DP port to be used to build the topology
    # @param[in] topology_type  SST or MST
    # @param[in] xml_file topology XML file path
    # @param[in] low_power  True/False for low power events
    # @param[in] is_mto  True/False for monitor turn off test cases
    # @param[in] power_event power event to be triggered
    # @return  None
    def set_and_verify_mst(self, port_type, topology_type=MST_TOPOLOGY, xml_file=MST_1B_1D_XML, low_power=False,
                           is_mto=False, power_event=PowerEvent.S3):
        step_str = "\t"
        if self.is_test_step:
            step_str = "Step{0}: ".format(self.step_counter)
            self.step_counter += 1
        logging.info("{0}Plug and verify MST Displays".format(step_str))

        # Initialize the DP Port
        status = self.display_port.init_dp(port_type, topology_type)
        if status:
            logging.debug("\tGraphics simulation driver initialized DP object successfully")
        else:
            gdhm.report_test_bug_audio(
                title="[Audio] Graphics simulation driver failed to initialized DP object")
            logging.error("Graphics simulation driver failed to initialized DP object")
            self.fail("Graphics simulation driver failed to initialized DP object")

        if low_power is True:
            # Set HPD Data during Low Power State
            status = self.display_port.set_low_power_state(num_of_ports=1, port_type=port_type,
                                                           sink_plugreq=enum.PlugSink, plug_unplug_atsource=True,
                                                           topology_after_resume=MST_TOPOLOGY)
            if status:
                logging.debug("\tSimulation driver issued Low Power State HPD Data to Graphics driver successfully")
            else:
                gdhm.report_test_bug_audio(
                    title="[Audio] Simulation driver issue of Low Power State HPD Data to Graphics driver failed")
                logging.error("Simulation driver issue of Low Power State HPD Data to Graphics driver failed")
                self.fail("Simulation driver issue of Low Power State HPD Data to Graphics driver failed")

        # Parse and Send Topology details to Gfx Sim driver from user
        status = self.display_port.parse_send_topology(port_type, topology_type, xml_file, low_power)
        if status:
            logging.debug("\t%s data parsed and sent to simulation driver successfully" % topology_type)
        else:
            gdhm.report_driver_bug_audio(
                title="[Audio] Failed to parse and send %s data to simulation driver" % topology_type)
            self.fail("Failed to parse and send %s data to simulation driver" % topology_type)

        if low_power is False:
            # Connect DP 1.2 display(s) by issuing HPD
            status = self.display_port.set_hpd(port_type, True)
            if status:
                logging.debug("\tSimulation driver issued HPD to Graphics driver successfully")
            else:
                gdhm.report_test_bug_audio(
                    title="[Audio] Simulation driver failed to issue HPD to Graphics driver")
                logging.error("Simulation driver failed to issue HPD to Graphics driver")
                self.fail("Simulation driver failed to issue HPD to Graphics driver")
        else:
            # set DUT to Low Power State
            self.base_invoke_power_event(power_event=power_event, is_mto=is_mto, low_power_event=True)

        # Wait for the simulation driver to reflect the DP topology connection status in CUI
        time.sleep(10)

        # Verify the MST Topology being created by comparing the data provided by the user
        # and seen in CUI DP topology page
        self.verify_topology(port_type)

        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        for display_index in range(self.enumerated_displays.Count):
            if str(CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)) == self.mst_port:
                self.plugged_display.append(self.mst_port)
                try:
                    current_mode_edp = self.display_config.get_current_mode(
                        self.enumerated_displays.ConnectedDisplays[display_index].TargetID)
                    logging.info("\tPlugged the panel {1} ({2}x{3}@{4}) on port {0} successfully".format(
                        self.mst_port,
                        self.enumerated_displays.ConnectedDisplays[display_index].FriendlyDeviceName,
                        current_mode_edp.HzRes,
                        current_mode_edp.VtRes,
                        current_mode_edp.refreshRate))
                except Exception as e:
                    logging.info("\tPlugged the panel {1} on port {0} successfully".format(
                        self.mst_port,
                        self.enumerated_displays.ConnectedDisplays[display_index].FriendlyDeviceName))

        if low_power is True:
            if is_mto:
                logging.info("\tResumed from the power event MONITOR_TURNOFF successfully")
            else:
                logging.info("\tResumed from the power event %s successfully", power_event.name)

        # Read the DPCD 600h for verifying Sink detected or not
        version_reg_value = self.dpcd_read(port_type, True, 1, DPCD_MSTM_CAP_OFFSET, None, action="MST_CAP")
        if version_reg_value & 0x1 == 0x1: # Check if bit 0 is set
            logging.info("\tPASS: Expected Display Type= MST, Actual= MST")
        else:
            logging.error("Expected Display Type= MST, Actual= Non-MST")
            gdhm.report_test_bug_audio(
                title="[Audio] FAIL: Expected Display Type= MST, Actual= Non-MST")
            self.fail("FAIL: Expected Display Type= MST, Actual= Non-MST")

        logging.info(f"Enumerated displays: {self.enumerated_displays.to_string()}")
        get_config = self.display_config.get_current_display_configuration()
        current_topology = get_config.to_string(self.enumerated_displays).split(' ')
        current_topology = current_topology[0] + ' ' + ' + '.join(current_topology[1:])
        logging.info("\tCurrent Topology= %s", current_topology)

        # Verifies if codec is loaded after plug of MST displays
        self.verify_audio_driver()

    ##
    # @brief Exposed API to verify MST topology between CUI and Driver
    # @param[in] port_type - The type of port to be plugged
    # @param[in] action - plug/unplug type to be performed
    # @return None
    def verify_topology(self, port_type, action="PLUG"):
        if action not in ['PLUG', 'UNPLUG']:
            self.fail("Invalid plug action for display.")

        # Topology verification is dependant on CUI SDK API's
        if not self.system_utility.is_ddrw():
            status = self.display_port.verify_topology(port_type)

            if action == 'PLUG' and status == MST_PLUG_SUCCESS:
                logging.debug("\tPASS: MST Topology Verification passed")
            elif action == 'UNPLUG' and status == MST_UNPLUG_SUCCESS:
                logging.debug("\tPASS: MST Topology Verification passed")
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] MST Topology Verification Failed.")
                self.fail("MST Topology Verification Failed.")

        else:
            # In Yangra driver CUI is not supported hence skipping the MST topology verification

            logging.info("\t MST Topology CUI-SDK not supported on Yangra - Skipping Topology Check.")

    ##
    # @brief       verify if the connected panel is DP2.0
    # @param[in]   display - Display port connected
    # @param[in]   gfx_index - Graphics adapter index
    # @return      is_dp2p0 - True if DP2.0 else False
    def verify_dp2(self, display, gfx_index='gfx_0'):
        offset = None
        display_base_obj = display_base.DisplayBase(display, gfx_index=gfx_index)
        pipe, ddi, transcoder = display_base_obj.GetPipeDDIAttachedToPort(display, True, gfx_index)
        if pipe == 'pipe_a':
            offset = 0x600A0
        if pipe == 'pipe_b':
            offset = 0x610A0
        if pipe == 'pipe_c':
            offset = 0x620A0
        if pipe == 'pipe_d':
            offset = 0x630A0
        reg_value = self.driver_interface_.mmio_read(offset, gfx_index)
        is_dp2p0 = (reg_value & 0x80000000) >> 31
        return is_dp2p0

    ##
    # @brief Read DPCD from the offset
    # @param[in] port_type for dpcd
    # @param[in] native_dpcd_read
    # @param[in] length for dpcd argument
    # @param[in] address
    # @param[in] node_rad
    # @param[in] action
    # @return None
    def dpcd_read(self, port_type, native_dpcd_read, length, address, node_rad, action="PLUG"):
        action = action.upper()
        if action not in ['PLUG', 'VERSION', 'MST_CAP']:
            self.fail("Invalid plug action for display.")

        dpcd_flag, dpcd_reg_val = self.display_port.read_dpcd(port_type, native_dpcd_read, length, address, node_rad)
        if action == 'PLUG' and dpcd_flag:
            logging.debug("\tDPCD Read Value: %s" % (dpcd_reg_val[0]))
            reg_val = dpcd_reg_val[0] & 0x000000FF

            if reg_val == DP_HOTPLUG_GOLDEN_VALUE:
                logging.info(
                    "\tPASS: Expected Register value for DPCD=%s, Actual=%s" % (DP_HOTPLUG_GOLDEN_VALUE, reg_val))
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] FAIL: Expected Register value for DPCD=%s, Actual=%s" % (DP_HOTPLUG_GOLDEN_VALUE,
                                                                                            reg_val))
                self.fail("\tFAIL: Expected Register value for DPCD=%s, Actual=%s" % (DP_HOTPLUG_GOLDEN_VALUE, reg_val))
        elif action == 'VERSION' and dpcd_flag:
            logging.debug("\tDPCD Version Value: %x" % (dpcd_reg_val[0]))
            return dpcd_reg_val[0]
        elif action == 'MST_CAP' and dpcd_flag:
            logging.info("DPCD MST CAP offset 0x21 Value: %x" % dpcd_reg_val[0])
            return dpcd_reg_val[0]
        else:
            gdhm.report_driver_bug_audio(
                title="[Audio] Read DPCD API failed")
            self.fail("Read DPCD API failed")

    ##
    # @brief Set display configuration
    # @param[in] topology
    # @param[in] display_list
    # @return None
    def set_display_config(self, display_list, topology=enum.SINGLE):

        if topology == enum.SINGLE and len(display_list) != 1:
            gdhm.report_test_bug_audio(
                title=f"[Audio] Invalid display config {DisplayConfigTopology(topology).name} {' '.join(display_list)}")
            self.fail(f"Invalid display config {DisplayConfigTopology(topology).name} {' '.join(display_list)}")

        if topology != enum.SINGLE and len(display_list) < 2:
            gdhm.report_test_bug_audio(
                title=f"[Audio] Invalid display config {DisplayConfigTopology(topology).name} {' '.join(display_list)}")
            self.fail(f"Invalid display config {DisplayConfigTopology(topology).name} {' '.join(display_list)}")

        # Verify current configuration
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        get_config = self.display_config.get_current_display_configuration()
        current_config_str = get_config.to_string(self.enumerated_displays)

        expected_config_str = DisplayConfigTopology(topology).name + ' ' + ' '.join(display_list)
        if current_config_str == expected_config_str:
            return True
        logging.info(f"Set Topology= {expected_config_str}")

        # Check for DP MST Test
        if self.mst_status is True:

            # Display Configuration Object
            set_config = DisplayConfig()
            set_config.topology = topology
            set_config.numberOfDisplays = len(display_list)

            current_port_index = 0

            # Find the targetId for each display_port given in display_list
            for display_port in display_list:
                for display_index in range(self.enumerated_displays.Count):
                    if str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[
                                                   display_index].ConnectorNPortType)) == display_port:
                        is_target_id_present = False

                        # Check targetId is not present in set_config
                        for targetId_index in range(current_port_index):
                            if set_config.displayPathInfo[targetId_index].targetId \
                                    == self.enumerated_displays.ConnectedDisplays[display_index].TargetID:
                                is_target_id_present = True
                                break

                        # Add the targetId to set_config
                        if is_target_id_present is False:
                            set_config.displayPathInfo[current_port_index].targetId \
                                = self.enumerated_displays.ConnectedDisplays[display_index].TargetID
                            set_config.displayPathInfo[current_port_index].displayAndAdapterInfo = \
                                self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo
                            current_port_index += 1
                            break

            # Apply display configuration
            self.display_config.set_display_configuration(set_config)
            # Todo: Remove as part of VSDI-30959
            time.sleep(6)

            # Verify current configuration
            get_config = self.display_config.get_current_display_configuration()
            if get_config.equals(set_config):
                logging.info("\tPASS: Successfully applied display configuration")
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Failed to apply display configuration")
                self.fail("Failed to apply display configuration")
        else:
            # Set display configuration for non DP MST displays
            if self.display_config.set_display_configuration_ex(topology, display_list) is False:
                gdhm.report_test_bug_audio(
                    title="[Audio] Failed to apply display configuration")
                self.fail("Failed to apply display configuration")
            else:
                # Verify current configuration
                # Todo: Remove as part of VSDI-30959
                time.sleep(6)
                logging.info("\tPASS: Successfully applied display configuration")


        # Print current topology
        self.print_current_topology(is_step=False)

    ##
    # @brief set_partial_topology plug/unplug branch/display from the full topology
    # @param[in] port_type
    # @param[in] plug_flag True/False
    # @param[in] node_rad
    # @param[in] xml_file
    # @param[in] low_power
    # @param[in] is_mto
    # @param[in] power_event
    # @return None
    def set_partial_topology(self, port_type, plug_flag, node_rad, xml_file, low_power=False, is_mto=False,
                             power_event = PowerEvent.S3):

        step_str = ""
        if self.is_test_step is True:
            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            for display_index in range(self.enumerated_displays.Count):
                if str(CONNECTOR_PORT_TYPE(
                        self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)) == self.mst_port:
                    current_mode_edp = self.display_config.get_current_mode(
                        self.enumerated_displays.ConnectedDisplays[display_index].TargetID)
                    step_str = "Step{0}: Unplugging the panel {2} ({3}x{4}@{5}) from port {1}".format(
                        self.step_counter,
                        self.mst_port,
                        self.enumerated_displays.ConnectedDisplays[display_index].FriendlyDeviceName,
                        current_mode_edp.HzRes,
                        current_mode_edp.VtRes,
                        current_mode_edp.refreshRate
                    )
                    break
            self.step_counter += 1
            logging.info(step_str)

        if low_power is True:
            # Set HPD Data during Low Power State
            status = self.display_port.set_low_power_state(num_of_ports=1, port_type=port_type,
                                                           sink_plugreq=enum.PlugSink, plug_unplug_atsource=True,
                                                           topology_after_resume=MST_TOPOLOGY)
            if status:
                logging.debug("\tSimulation driver issued Low Power State HPD Data to Graphics driver successfully")
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Simulation driver issue of Low Power State HPD Data to Graphics driver failed")
                self.fail("Simulation driver issue of Low Power State HPD Data to Graphics driver failed")

            self.display_port.set_mst_partial_topology(port_type, plug_flag, node_rad, xml_file, low_power)

            # set DUT to Low Power State
            self.base_invoke_power_event(power_event=power_event, is_mto=is_mto, low_power_event=True)

            #todo verify that display is unplugged successfully
            self.plugged_display.remove(self.mst_port)
            if is_mto:
                logging.info("\tResumed from the power event MONITOR_TURNOFF successfully")
            else:
                logging.info("\tResumed from the power event %s successfully", power_event.name)
        else:
            status = self.display_port.set_mst_partial_topology(port_type, plug_flag, node_rad, xml_file, low_power)

            if status:
                if plug_flag is True:
                    logging.info("\tDisplay plugged in successfully")
                else:
                    logging.info("\tDisplay unplugged successfully")
                    self.plugged_display.remove(self.mst_port)
            else:
                if plug_flag is True:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] Simulation driver failed to plug in display")
                    self.fail("Simulation driver failed to plug in display")
                else:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] Simulation driver failed to unplug display")
                    self.fail("Simulation driver failed to unplug display")

        get_config = self.display_config.get_current_display_configuration()
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        current_topology = get_config.to_string(self.enumerated_displays).split(' ')
        current_topology = current_topology[0] + ' ' + ' + '.join(current_topology[1:])
        logging.info("\tCurrent Topology= %s", current_topology)

    ##
    # @brief get_topology_rad retrieves the RAD for port number
    # @param[in] port_type
    # @return display RAD
    def get_topology_rad(self, port_type):
        status, disp_rad = self.display_port.get_mst_topology_rad(port_type)
        if status:
            logging.debug("\tRAD Information retrieved successfully")
        else:
            gdhm.report_test_bug_audio(
                title="[Audio] Failed to retrieve RAD Information")
            logging.error("Failed to retrieve RAD Information")
            self.fail("Failed to retrieve RAD Information")

        return disp_rad

    ##
    # @brief set_power_line sets the power line status to AC/DC
    # @param[in] power_state
    # @return bool , True if operation is successful, False otherwise
    def set_power_line(self, power_state=PowerSource.DC):
        status = False
        logging.info("Setting power line status to {0}".format(power_state.name))

        # Switch power line to given state
        for count in range(0, 5):
            if self.display_power.set_current_powerline_status(power_state) is False:
                if self.is_simbatt_enabled:

                    # Disable Simulated Battery
                    if self.display_power.enable_disable_simulated_battery(False) is False:
                        self.fail("\tFailed to disable SimBatt")
                    else:
                        self.is_simbatt_enabled = False

                    # Enable Simulated Battery
                    if self.display_power.enable_disable_simulated_battery(True) is False:
                        self.fail("\tFailed to enable SimBatt")
                    else:
                        self.is_simbatt_enabled = True
            else:
                status = True
                break
        if status is False:
            self.fail("Failed to set power line status to {0}".format(power_state.name))

    ##
    # @brief verifies that audio codec is in D3 state
    # @return None
    def verify_audio_codec_d3_state(self):
        status = False

        if self.is_test_step:
            logging.info("Step{0}: Waiting for Audio Codec to enter D3".format(self.step_counter))
            self.step_counter += 1

        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for display_index in adapter_dict.keys():
            # Get the Audio Codec Power State
            audio_codec = self.display_audio.get_audio_driver(display_index)
            if audio_codec == AudioCodecDriverType.NONE:
                logging.info(
                    "\tPower state cannot be fetched since SGPC is enabled and codec wont be loaded with internal "
                    "display config")
                return
            else:
                for sec in range(AUDIO_D3_TIMEOUT):
                    # Get the Audio Codec Power State
                    audio_codec_power_state = self.display_audio.get_audio_codec_power_state(audio_codec)

                    if audio_codec_power_state == AudioPowerState.D3:
                        logging.info("\tPASS: Expected Audio Codec Power State= D3, Actual= D3 (~{0} seconds)".format(sec))
                        status = True
                        break
                    if audio_codec_power_state == AudioPowerState.UNSPECIFIED:
                        logging.error("\tUnable to get audio codec power state")
                        return
                    time.sleep(1)

                if status is False:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] FAIL: Expected Audio Codec Power State= D3, Actual= {0} (~{1} seconds)".format(
                            audio.AudioPowerState(audio_codec_power_state).name, AUDIO_D3_TIMEOUT))
                    self.fail("FAIL: Expected Audio Codec Power State= D3, Actual= {0} (~{1} seconds)".format(
                        audio.AudioPowerState(audio_codec_power_state).name, AUDIO_D3_TIMEOUT))

    ##
    # @brief verifies that audio controller is in D3 state
    # @return None
    def verify_audio_controller_d3_state(self):
        status = False

        if self.is_test_step:
            logging.info("Step{0}: Waiting for Audio Controller to enter D3".format(self.step_counter))
            self.step_counter += 1

        # Get the Audio Controller Power State
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for display_index in adapter_dict.keys():
            audio_codec = self.display_audio.get_audio_driver(display_index)
            is_sgpc_enabled = self.display_audio.is_sgpc_enabled(display_index)
            audio_controller, device_id, _ = self.display_audio.get_audio_controller(display_index)
            if audio_codec == AudioCodecDriverType.NONE:
                if is_sgpc_enabled is True:
                    logging.info("\tSkipping Codec D3 check in case of Built-in display")
                    return
            else:
                for sec in range(AUDIO_D3_TIMEOUT):
                    # Get the Audio Codec Power State
                    audio_controller_power_state = self.display_audio.get_audio_controller_power_state(
                        self.display_audio.audio_controller_name)

                    if audio_controller_power_state == 1:
                        logging.info(
                            "\tPASS: Expected Audio Controller Power State= D3, Actual= D3 (~{0} seconds)".format(sec))
                        status = True
                        break
                    time.sleep(1)

                if status is False:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] FAIL: Expected Audio Controller Power State= D3, Actual= D0 (~{0} seconds)"
                        .format(AUDIO_D3_TIMEOUT))
                    self.fail("FAIL: Expected Audio Controller Power State= D3, Actual= D0 (~{0} seconds)".format(
                        AUDIO_D3_TIMEOUT))

    ##
    # @brief install and verify the audio codec driver
    # @return None
    def install_and_verify_audio_driver(self):
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for display_index in adapter_dict.keys():
            if self.is_test_step is True:
                logging.info("Step{0}: Installing Audio Driver".format(self.step_counter))
                self.step_counter += 1
            if self.display_audio.install_audio_driver() is False:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Failed to install audio driver")
                self.fail("Failed to install audio driver")
            else:
                self.is_audio_driver_installed = True

    ##
    # @brief uninstall and verify the audio codec driver
    # @return None
    def uninstall_and_verify_audio_driver(self):
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for display_index in adapter_dict.keys():
            audio_codec = self.display_audio.get_audio_driver(display_index)
            is_sgpc_enabled = self.display_audio.is_sgpc_enabled(display_index)
            if audio_codec == AudioCodecDriverType.NONE:
                if is_sgpc_enabled is True:
                    logging.info("Codec won't load incase of built-in display")
            else:
                if self.is_test_step is True:
                    logging.info("Step{0}: Uninstalling Audio Driver".format(self.step_counter))
                    self.step_counter += 1

                if self.display_audio.uninstall_audio_driver() is False:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] Failed to uninstall audio driver")
                    self.fail("Failed to uninstall audio driver")
                else:
                    self.is_audio_driver_installed = False

    ##
    # @brief enable and verify the audio codec driver
    # @param[in] port_info - Display port info
    # @return None
    def enable_and_verify_audio_codec(self, port_info=None):
        display_gfx_index = port_info['gfx_index'].lower()
        current_audio_codec = self.display_audio.get_audio_driver(display_gfx_index)
        current_sgpc_status = self.display_audio.is_sgpc_enabled(display_gfx_index)
        if current_audio_codec == AudioCodecDriverType.NONE:
            if current_sgpc_status is True:
                logging.info("\tAudio codec won't be loaded incase of Built-in display in SGPC enabled platforms")
                return
        else:
            if self.is_test_step is True:
                logging.info("Step{0}: Enabling Audio Codec Driver".format(self.step_counter))
                self.step_counter += 1
            if self.display_audio.enable_audio_driver(display_gfx_index) is True:
                logging.info("\tPASS: Expected Audio Codec Driver status= ENABLED, Actual= ENABLED")
                self.is_audio_codec_driver_enabled = True
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Failed to enable audio codec driver")
                self.fail("Failed to enable audio codec driver")

    ##
    # @brief disable and verify the audio codec driver
    # @param[in] port_info - Display port info
    # @return None
    def disable_and_verify_audio_codec(self, port_info=None):
        # Gets the audio codec loaded
        display_gfx_index = port_info['gfx_index'].lower()
        current_audio_codec = self.display_audio.get_audio_driver(display_gfx_index)
        current_sgpc_status = self.display_audio.is_sgpc_enabled(display_gfx_index)
        if current_audio_codec == AudioCodecDriverType.NONE:
            if current_sgpc_status is True:
                logging.info("\tAudio codec won't be loaded incase of Built-in display in SGPC enabled platforms")
                return
        else:
            if self.is_test_step is True:
                logging.info("Step{0}: Disabling Audio Codec Driver".format(self.step_counter))
                self.step_counter += 1

            if self.display_audio.disable_audio_driver(display_gfx_index) is True:
                logging.info("\tPASS: Expected Audio Codec Driver status= DISABLED, Actual= DISABLED")
                self.is_audio_codec_driver_enabled = False
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Failed to disable audio codec driver")
                self.fail("Failed to disable audio codec driver")

    ##
    # @brief enable and verify the audio controller
    # @return None
    def enable_and_verify_audio_controller(self):
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for display_index in adapter_dict.keys():
            if self.is_test_step is True:
                logging.info("Step{0}: Enabling Audio Controller for {1}".format(self.step_counter, display_index))
                self.step_counter += 1

            if self.display_audio.disable_enable_audio_controller(action="enable", gfx_index=display_index) is True:
                logging.info("\tPASS: Expected Audio Controller status for {0}= ENABLED, Actual= ENABLED".format(
                    display_index))
                self.is_audio_controller_enabled = True
            else:
                logging.error("Failed to enable audio controller for {0}".format(display_index))
                gdhm.report_test_bug_audio(title="[Audio] Failed to enable audio controller for {0}"
                                           .format(display_index))
                self.fail("Failed to enable audio controller for {0}".format(display_index))

    ##
    # @brief disable and verify the audio controller
    # @return None
    def disable_and_verify_audio_controller(self):
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for display_index in adapter_dict.keys():
            if self.is_test_step is True:
                logging.info("Step{0}: Disabling Audio Controller for {1}".format(self.step_counter, display_index))
                self.step_counter += 1

            if self.display_audio.disable_enable_audio_controller(action="disable", gfx_index=display_index) is True:
                logging.info("\tPASS: Expected Audio Controller status for {0}= DISABLED, Actual= DISABLED".format(
                    display_index))
                self.is_audio_controller_enabled = False
            else:
                logging.error("Failed to disable audio controller for {0}".format(display_index))
                gdhm.report_test_bug_audio(title="[Audio] Failed to disable audio controller for {0}"
                                           .format(display_index))
                self.fail("Failed to disable audio controller for {0}".format(display_index))

    ##
    # @brief apply max mode for all displays
    # @return None
    def apply_max_mode_for_all_displays(self):
        get_config = self.display_config.get_current_display_configuration()
        for index in range(get_config.numberOfDisplays):
            target_id = get_config.displayPathInfo[index].targetId
            supported_mode_dict = self.display_config.get_all_supported_modes([target_id], sorting_flag=True)
            for target_id, supported_mode_list in supported_mode_dict.items():
                for display_mode in supported_mode_list:
                  logging.debug('HRes:{} VRes:{} RR:{} BPP:{}, SamplingMode: {}, ScanlineOrdering: {}'.format(
                      display_mode.HzRes, display_mode.VtRes, display_mode.refreshRate, display_mode.BPP,
                      display_mode.samplingMode.Value, display_mode.scanlineOrdering
                      ))
                max_mode = supported_mode_list[-1]
                is_success = self.display_config.set_display_mode([max_mode])
                if is_success is False:
                    gdhm.report_driver_bug_audio(
                        title="[Audio] FAIL: Failed to apply max mode")
                    self.fail("FAIL: Failed to apply max mode- {1}x{2}@{3} for target ID - {0}".format(target_id,
                                                                                                       max_mode.HzRes,
                                                                                                       max_mode.VtRes,
                                                                                                       max_mode.refreshRate))

                logging.info("Successfully applied max mode- {1}x{2}@{3} for target ID - {0}".format(target_id,
                                                                                                     max_mode.HzRes,
                                                                                                     max_mode.VtRes,
                                                                                                     max_mode.refreshRate))

    ##
    # @brief verify the status of VDSC for all Displays
    # @return None
    def verify_vdsc_audio(self):
        for display in self.display_list:
            display_port = list(display.keys())[0]
            if dsc_verifier.verify_dsc_programming('gfx_0', display_port) is True:
                logging.info("VDSC verification for {} Expected = PASS Actual = PASS".format(display_port))
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Incorrect DSC Programming For dsc display plugged at {}".format(display_port))
                self.fail("[Driver Issue] - Incorrect DSC Programming For dsc display plugged at {}"
                          .format(display_port))

    ##
    # @brief verify the status of VDSC for given Display
    # @param[in] display to verify VDSC
    # @return None
    def verify_vdsc_audio_single(self, display):
            display_port = display[0]
            if dsc_verifier.verify_dsc_programming('gfx_0', display_port) is True:
                logging.info("VDSC verification for {} Expected = PASS Actual = PASS".format(display_port))
            else:
                gdhm.report_driver_bug_audio(
                    title="[Audio] Incorrect DSC Programming For dsc display plugged at {}".format(display_port))
                self.fail("[Driver Issue] - Incorrect DSC Programming For dsc display plugged at {}"
                          .format(display_port))

    ##
    # @brief verify SDP Splitting
    # @param[in] display to verify splitting; DP_B/DP_A
    # @param[in] gfx_index on which display is plugged
    # @param[in] expected_sdp splitting value
    # @param[in] trans_cnt transcoder count to verify sdp splitting for enabled transcoders
    # @return None
    def verify_sdp_splitting(self, display, gfx_index, expected_sdp, trans_cnt=1):
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for index in adapter_dict.keys():
            if gfx_index == index:
                dut_info = self.machine_info.get_platform_details(adapter_dict[index].deviceID)
                sku = self.machine_info.get_platform_details(adapter_dict[gfx_index].deviceID).SkuName

        logging.info(f"No of transcoders expected to be enabled: {trans_cnt}")
        register_interface: DisplayRegsService = DisplayRegs.get_interface(dut_info.PlatformName, gfx_index)

        if trans_cnt == 1:
            actual_sdp_splitting = self.display_audio.get_sdp_splitting_status(gfx_index, dut_info.PlatformName, display)
        elif trans_cnt > 1:
            for each_trans in ['transcoder_a', 'transcoder_b', 'transcoder_c', 'transcoder_d']:
                trans_ddi_func_offsets = register_interface.get_trans_ddi_offsets(each_trans)
                value = DisplayArgs.read_register(trans_ddi_func_offsets.FuncCtrlReg, gfx_index)
                trans_enable = (value & 0x80000000) >> 31
                logging.info("{} is {}".format(each_trans, "Enabled" if trans_enable else "Disabled"))
                if trans_enable:
                    actual_sdp_splitting = self.display_audio.get_sdp_splitting_status(gfx_index, dut_info.PlatformName, display)
                    if actual_sdp_splitting:
                        logging.info(
                            "SDP Splitting is Enabled for {}".format(each_trans))
                    else:
                        gdhm.report_driver_bug_audio(
                            title="[Audio] FAIL: SDP Splitting is Disabled for {}".format(each_trans))
                        self.fail(
                            "FAIL: SDP Splitting is Disabled for {}".format(each_trans))

        logging.info(f"Expected SDP Splitting value: {expected_sdp}; Actual SDP Splitting value {actual_sdp_splitting}")

        if actual_sdp_splitting == expected_sdp:
            logging.info(
                f"PASS: Driver programmed SDP Splitting value is same as expected value for current Topology on {display} on adapter {gfx_index}")
        else:
            gdhm.report_driver_bug_audio(
                    title="[Audio] Driver programmed audio SDP splitting is mis-matching with expected value")
            self.fail(
                    "FAIL: [Driver Issue] Driver programmed SDP Splitting value is not same as expected valued ")

    ##
    # @brief        Verifies multi-channel audio playback
    # @param[in]    display - connected displays
    # @param[in]    port - Connector port of display
    # @param[in]    endpoint_name - Endpoint for playback verification
    # @return       None
    def verify_multiCh_playback(self, display, port, endpoint_name):
        for key, val in AUDIO_CHANNEL.items():
            if key == 'sample_rate':
                if self.adsp_driver:
                    if self.channel == 2 and self.bit_depth == 24:
                        val = {48000, 88200, 96000, 192000}
                    if self.channel == 6 and self.bit_depth == 16:
                        val = {44100, 48000, 96000, 192000}
                    if self.channel == 6 and self.bit_depth == 24:
                        val = {48000, 96000, 192000}
                    if self.channel == 8 and self.bit_depth == 16:
                        val = {44100, 48000, 96000, 192000}
                    if self.channel == 8 and self.bit_depth == 24:
                        val = {48000, 96000, 192000}
                    if self.channel == 4 and self.bit_depth == 16:
                        val = {44100, 48000, 88200, 96000, 192000}
                    if self.channel == 4 and self.bit_depth == 24:
                        val = {44100, 48000, 96000, 192000}
                for sample in val:
                    sample_rate = sample
                    status = self.display_audio.audio_playback_verification(display_info=display,
                                                                        channel=self.channel,
                                                                        bit_depth=self.bit_depth,
                                                                        sample_rate=sample_rate,
                                                                        end_point_name=endpoint_name)

                    if status:
                        logging.info(f'\t{self.bit_depth}bit: {self.channel}ch: {sample_rate}KHz: Pass: '
                                     f'Audio Playback Verification success for port: {port}: {endpoint_name}')
                    else:
                        logging.error(f'\t{self.bit_depth}bit: {self.channel}ch: {sample_rate}KHz: Fail: '
                                      f'Audio Playback Verification success for port: {port}: {endpoint_name}')
                        gdhm.report_driver_bug_audio(
                            title=f'[Audio] {self.bit_depth}bit: {self.channel}ch: {sample_rate}KHz: Fail: '
                                  f'Audio playback verification failed for port: {port}: {endpoint_name}')
                        self.fail(f'{self.bit_depth}bit: {self.channel}ch: {sample_rate}KHz: Fail: '
                                  f'Audio playback verification failed for port: {port}: {endpoint_name}')

