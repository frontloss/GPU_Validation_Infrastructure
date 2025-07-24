########################################################################################################################
# @file         display_interop_base.py
# @brief        It contains setUp and tearDown methods of unittest framework. 
# @details      For all Display Interop tests which is derived from this, 
#               will make use of setup/teardown of this base class.
#               This script contains helper functions that will be used by BAT test scripts.
# @authors      Raghupathy, Dushyanth Kumar, Balaji Gurusamy, Sanehadeep Kaur
########################################################################################################################
import copy
import getpass
import importlib
import logging
import math
import os
import subprocess
import sys
import time
import unittest
import winreg
from tkinter import messagebox, Tk
from xml.etree import ElementTree as ET
from enum import IntEnum

import win32api
import win32con

from Libs.Core import enum, cmd_parser, window_helper, registry_access
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import ScanlineOrdering
from Libs.Core import display_essential
from Libs.Core import display_power
from Libs.Core.hw_emu.she_utility import SHE_UTILITY
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import winkb_helper
from Libs.Feature.app import AppMedia
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_audio import DisplayAudio
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from registers.mmioregister import MMIORegister

##
# Creating object for TKinter
master = Tk()
master.wm_state('iconic')

# New level of logging for Test Sequence Flow
STEP = 25
logging.addLevelName(STEP, "STEP")

##
# @brief Default duration in seconds to wait for Audio endpoint enumeration
AUDIO_ENDPOINT_ENUMERATION_DURATION = 20

Delay_After_Power_Event = 10
Delay_5_Secs = 5

TEST_SPECIFIC_BIN = os.path.join(test_context.TEST_STORE_FOLDER, "TestSpecificBin")
OPMTEST_BINARY_PATH = (TEST_SPECIFIC_BIN + "\\HDCP")


##
# @brief        Supported HDCP Types
class HDCPType(IntEnum):
    HDCP_1_4 = 0
    HDCP_2_2 = 1


##
# @brief        Display Dev Bat V1 Base class : To be used in Display DEV BAT tests
class DisplayInteropBase(unittest.TestCase):
    she_utility = SHE_UTILITY()
    display_power = display_power.DisplayPower()
    display_engine = DisplayEngine()
    display_config = DisplayConfiguration()
    display_audio = DisplayAudio()
    machine_info = SystemInfo()
    underrunstatus = UnderRunStatus()
    platform = None
    enumerated_displays = None
    display_list = []
    displays_dict = {}
    sequence_list = []
    verifiers = []
    topology = []
    enumport = []
    random_list = []
    seq_counter = 0.0
    test_sequence_format = "    Test Sequence:{seq:^5}: {msg:<35}"

    ##
    # @brief        Unit-test setup function.
    # @return       None
    def setUp(self):

        ## intializing she_utility
        self.she_utility.intialize()
        ## Custome tags- enmprt = emulator port, vrfr = type of verification, topo= topology, rndm = list of tests selected for random execution
        self.my_custom_tags = ['-enmprt', '-vrfr', '-topo', '-rndm']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)

        ##
        # Start Underrun
        self.underrunstatus.clear_underrun_registry()
        self.hdcp_type = HDCPType.HDCP_1_4

        ##
        # connected_list[] is a list of Port Names of the connected Displays
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    if not (self.display_list.__contains__(value['connector_port'])):
                        self.display_list.insert(value['index'], value['connector_port'])
                        self.displays_dict[value['connector_port']] = value['panel_index']

            if (key == 'VRFR'):
                self.verifiers = value

            if (key == 'TOPO'):
                self.topology = value

            if (key == 'RNDM'):
                self.random_list = value

            if (key == 'ENMPRT'):
                self.enumport = value

        if self.she_utility.device_connected == 1:
            for port in self.display_list:
                self.she_utility.hot_plug_unplug(self.get_display_id_SHE(port), True, 5)
                time.sleep(7)
        elif self.she_utility.device_connected == 2:
            for port in self.enumport:
                self.she_utility.hot_plug_unplug(self.get_display_id_Diempel(port), True, 5)
                time.sleep(7)
        else:
            logging.info("SHE device is not Connected")

        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        self.os_info = self.machine_info.get_os_info()
        ##
        # Pre Requisites for playing Video Clip
        self.media_file = os.path.join(test_context.TestContext.test_store(), "MPO\mpo_3840_2160_avc.mp4")
        window_helper.close_browser()
        window_helper.close_media_player()
        window_helper.kill_process_by_name("Maps.exe")

        # Remove old logs
        os.system("del hdcp_log*")
        os.system("del OPM*.log")
        logging.debug("Successfully removed previous log files")

        self.prepare_sequence()

    ##
    # @brief        Enabling Verifiers Function
    # @return       None
    def enabling_de_verifiers(self):
        if self.verifiers is not None:
            # for item in self.verifiers:
            if len(self.verifiers) == 1 and "AUTO" in self.verifiers:
                self.seq_counter += 0.1
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Verifying Display Engine"))
                self.display_engine.verify_display_engine()
                self.seq_counter += 0.1
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Verified Display Engine Successfully"))

            elif len(self.verifiers) == 2 and "MNML" not in self.verifiers:
                messagebox.showinfo("Test Display Engine", "Going to Verify DE")
                time.sleep(7)
                self.seq_counter += 0.1
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Verifying Display Engine"))
                self.display_engine.verify_display_engine()
                self.seq_counter += 0.1
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Verified Display Engine Successfully"))
                messagebox.showinfo("Test Display Engine", "DE Verified Successfully")
            else:
                pass

    ##
    # @brief        Enabling PV Verifiers
    # @param[in]    port - Graphics Port Value
    # @return       None
    def enabling_pv_verifiers(self, port):
        if self.verifiers is not None:
            if len(self.verifiers) == 1 and "AUTO" in self.verifiers:
                self.mpo_plane_verification(port)
                self.enabling_de_verifiers()
            elif len(self.verifiers) == 1 and "MANL" in self.verifiers:
                window_helper.close_media_player()
                result = messagebox.askquestion("Test Video & Audio",
                                                "Did you see Video\Audio Playback without Distortion?")
                if result == 'yes':
                    logging.info("User Input Test Video & Audio - PASS")
                else:
                    logging.error("User Input Test Video & Audio - FAIL")
                time.sleep(10)

            elif len(self.verifiers) == 2 and "MNML" not in self.verifiers:
                self.mpo_plane_verification(port)
                result = messagebox.askquestion("Test Video & Audio",
                                                "Did you see Video\Audio Playback without Distortion?")
                if result == 'yes':
                    logging.info("User Input Test Video & Audio - PASS")
                else:
                    logging.error("User Input Test Video & Audio - FAIL")
                time.sleep(10)
                self.enabling_de_verifiers()
            else:
                pass

        logging.info("Successfully Played 4K Video Clip")

    ##
    # @brief        MPO Plane Verification Function
    # @param[in]    display_port - Display Port Value
    # @return       None
    def mpo_plane_verification(self, display_port):
        plane1_pixelformat = "source_pixel_format_NV12_YUV_420"
        self.verify_planes(display_port, 'PLANE_CTL_1', plane1_pixelformat)
        time.sleep(30)
        window_helper.close_media_player()
        self.seq_counter += 0.1
        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                           msg="Successfully Verified Pixel Format Register"))

    ##
    # @brief        Enabling PV Verifiers
    # @param[in]    r
    # @param[in]    root
    # @return       d - The output dictionary
    def dictify(self, r, root=True):
        if root:
            return {r.tag: self.dictify(r, False)}
        d = copy.copy(r.attrib)
        for x in r.findall("./*"):
            if x.tag not in d:
                d[x.tag] = []
            d[x.tag].append(self.dictify(x, False))
        return d

    ##
    # @brief        create a map for the displays and sequences
    # @return       None
    def prepare_sequence(self):
        tree = ET.parse(test_context.ROOT_FOLDER + r'\Tests\Display_Config\DisplaySequence.xml')
        root = tree.getroot()
        dd = self.dictify(root)
        aa = dd["Sequences"]
        self.sequence_list = list(dict(aa['Seq1'][0]).values())[0]

    ##
    # @brief        create a map for the displays and sequences
    # @param[in]    display_str - Display specifications String
    # @return       list - A list of map of lambda
    def map_seq_displays(self, display_str):
        disp_str_list = str(display_str).split(",")
        return list(map(lambda x: self.display_list[int(x) - 1], disp_str_list))

    ##
    # @brief        Set the given config along with displays
    # @param[in]    config - String configuration
    # @param[in]    displays - List of displays
    # @return - None
    def apply_config_and_verify(self, config, displays):
        if "MANL" in self.verifiers:
            messagebox.showinfo("Test Config Switching", "Going to Switch Topology")
        if len(self.display_list) < len(displays):
            logging.info("Ignoring the config {0} in "
                         "sequence since planned test has only {1} displays".format(config,
                                                                                    str(len(self.display_list))))
        else:
            cfg = enum.SINGLE
            if config == 'SINGLE':
                cfg = enum.SINGLE
            elif config == 'CLONE':
                cfg = enum.CLONE
            elif config == 'EXTENDED':
                cfg = enum.EXTENDED
            logging.info("Setting Config {0} with Displays: {1}".format(config, displays))
            self.seq_counter += 0.1
            if self.display_config.set_display_configuration_ex(cfg, displays, self.enumerated_displays) is False:
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Failed to Apply Config Topology. Test Failed"))
                self.fail("Apply Config Failed")
            else:
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Successfully Applied Config Topology"))
                if "MANL" in self.verifiers:
                    result = messagebox.askquestion("Test Config Switching",
                                                    "Did you see Config : {} with Display(s) : {} ?".format(config,
                                                                                                            displays),
                                                    icon='warning')
                    if result == 'yes':
                        logging.info("User Input Test Config Switching - PASS")
                    else:
                        logging.error("User Input Test Config Switching - FAIL")
                self.enabling_de_verifiers()

        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief        Perform power events CS,S3 and S4
    # @param[in]    power_state - State of Power
    # @return       bool - State of triggered power event
    def trigger_powerevents_and_verify(self, power_state):
        power_state_enums = 0
        if power_state == 'CS':
            if self.display_power.is_power_state_supported(display_power.PowerEvent.CS):
                power_state_enums = display_power.PowerEvent.CS
            else:
                logging.warning("Machine Does NOT Support CS")
                return
        elif power_state == 'S3':
            if not self.display_power.is_power_state_supported(display_power.PowerEvent.CS):
                power_state_enums = display_power.PowerEvent.S3
            else:
                logging.warning("Machine Does NOT Support S3")
                return
        elif power_state == 'S4':
            power_state_enums = display_power.PowerEvent.S4
        if "MANL" in self.verifiers:
            messagebox.showinfo("Test Power State", "System is going to Enter {} Power State".format(power_state))
        self.seq_counter += 0.1
        if self.display_power.invoke_power_event(power_state_enums, 60):
            logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                               msg="Invoking {} Power Event Success".format(
                                                                   power_state)))
            time.sleep(Delay_5_Secs)
            if "MANL" in self.verifiers:
                result = messagebox.askquestion("Test Power State",
                                                "System Resume from {} Power State\n Did you see any Corruption?".format(
                                                    power_state), icon='warning')
                if result == 'yes':
                    logging.error("User Input Test Power State - FAIL")
                else:
                    logging.info("User Input Test Power State - PASS")
            self.enabling_de_verifiers()
        else:
            logging.error("Invoking {} Power Event: Failed".format(power_state))
            logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                               msg="Invoking {} Power Event: Failed".format(
                                                                   power_state)))
            return False
        time.sleep(Delay_After_Power_Event)

        self.seq_counter = math.floor(self.seq_counter)
        return True

    ##
    # @brief        Makes the list of Display
    # @param[in]    xml_list - List of XML Files
    # @return       list of map of Lambda
    def make_display_list(self, xml_list):
        return list(map(lambda x: list(dict(x).values())[0], xml_list))

    ##
    # @brief        Function to return GfxValSim driver version
    # @return       bool - state of Valsim Installed
    def is_valsim_installed(self):
        try:
            version = subprocess.check_output(
                ["powershell.exe", "Get-WmiObject -Class Win32_PnPSignedDriver ",
                 "-Filter ", "\"devicename='Intel(R) Gfx Val Simulation Driver'\"",
                 " | ", "select driverversion"],
                shell=True, universal_newlines=True)
            version_id = version.rsplit('-', 1)[1].strip()
            return True
        except:
            return False

    ##
    # @brief        Get the Display
    # @param[in]    connector_port - Graphics connector Port
    # @return       dict - Port address of Dictionary
    def get_display_id_Diempel(self, connector_port):
        return {'SHE_EDP': 0,
                'SHE_DP_1': 1,
                'SHE_DP_2': 2,
                'SHE_DP_3': 3,
                'SHE_DP_4': 4,
                'SHE_HDMI_1': 5,
                'SHE_HDMI_2': 6,
                'IO_PORT6': 7,
                'IO_PORT9': 8,
                'IO_PORT10': 9,
                'IO_PORT11': 10,
                'IO_PORT12': 11,
                'EMULATOR_PORT1': 12,
                'EMULATOR_PORT2': 13,
                'EMULATOR_PORT3': 14
                }[connector_port]

    ##
    # @brief        Get Display ID of SHE
    # @param[in]    connector_port - Port Index
    # @return       int - display id of the connector Port
    def get_display_id_SHE(self, connector_port):
        return {'DP_A': 0,
                'DP_B': 1,
                'DP_C': 1,
                'DP_F': 1,
                'HDMI_B': 5,
                'HDMI_C': 5,
                'HDMI_D': 5
                }[connector_port]

    ##
    # @brief        Unplug the displays
    # @return       void or bool
    def unplug_plug_HPD(self):
        if self.she_utility.device_connected == 1:
            self.HPD_with_SHE(1.0)
        else:
            if self.she_utility.device_connected == 2:
                self.HPD_with_SHE(2.0)
            else:
                if "MANL" in self.verifiers:
                    messagebox.showinfo("Test SHE Tool", "No SHE Tool Found, Skipping HPD Test")
                logging.warning("None Of SHE Tool is Connected, hence Unplug Displays not Possible")
                return

        return True

    ##
    # @brief        Apply modes and verify
    # @param[in]    target_id_list - Target IDs list
    # @param[in]    enumerated_displays - Mode Levels to be applied
    # @return       None
    def apply_modes_and_verify(self, target_id_list, enumerated_displays):
        supported_modes = self.display_config.get_all_supported_modes(target_id_list)
        enum_Displays = enumerated_displays
        for target_id in target_id_list:
            modes = []
            for key, values in supported_modes.items():
                if (key == target_id):
                    noOfModes = len(values)
                    modes.append(values[0])
                    modes.append(values[noOfModes // 2])
                    modes.append(values[noOfModes - 1])

            if "MANL" in self.verifiers:
                messagebox.showinfo("Test ModeSet", "Starting Display ModeSet Test\n  [MIN]\t[MID]\t[MAX]")
            for mode in modes:
                self.seq_counter += 0.1
                logging.info(mode.to_string(enum_Displays))

                self.display_config.set_display_mode([mode])
                mode_resolution = "{} x {} @ {} {}".format(mode.HzRes, mode.VtRes, mode.refreshRate,
                                                           (ScanlineOrdering(mode.scanlineOrdering)).name)
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Successfully Applied Mode : {}".format(
                                                                       mode_resolution)))
                if "MANL" in self.verifiers:
                    result = messagebox.askquestion("Test ModeSet",
                                                    "{} Applied\nDid you see any Corruption?".format(mode_resolution),
                                                    icon='warning')
                    if result == 'yes':
                        logging.error("User Input Test ModeSet - FAIL")
                    else:
                        logging.info("User Input Test ModeSet - PASS")
                self.enabling_de_verifiers()
        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief        Disable/Enable Driver and Verify it's running or not
    # @return       None
    def disable_enable_driver(self):
        if "MANL" in self.verifiers:
            messagebox.showinfo("Test Gfx Driver",
                                "Starting Gfx Driver Disable & Enable Test\nNote: Momentary Blankout Expected")
        status, reboot_required = display_essential.restart_gfx_driver()
        if status:
            logging.info("Disable & Enable Gfx Driver Successfully")
            if "MANL" in self.verifiers:
                result = messagebox.askquestion("Test Gfx Driver",
                                                "Driver Disabled & Enabled Done\nDid you see any Corruption?",
                                                icon='warning')
                if result == 'yes':
                    logging.error("User Input Test Driver - FAIL")
                else:
                    logging.info("User Input Test Driver - PASS")
        else:
            logging.error("Disable & Enable Gfx Driver Failed")
        self.seq_counter += 0.1
        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                           msg="Successfully Verified Disable\Enable Driver"))
        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief        Playing Video Clip, Mouse Move and Verifying MPO
    # @param[in]    display_port - Display Port
    # @return       None
    def play_video_clip_and_verify_mpo(self, display_port):
        if "MANL" in self.verifiers:
            messagebox.showinfo("Test Video & Audio",
                                "Starting Display Video with Audio Test, Keep Speakers Connected to Display Panel",
                                icon='warning')

        self.play_media(True)
        time.sleep(20)
        self.enabling_pv_verifiers(display_port)
        window_helper.close_media_player()
        self.seq_counter += 0.1
        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                           msg="Successfully Played 4K Video Clip"))
        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief        Verify Planes
    # @param[in]    display - Display ID
    # @param[in]    plane_ctl_reg
    # @param[in]    expected_pixel_format - Expected Pixel Format
    # @return       None
    def verify_planes(self, display, plane_ctl_reg, expected_pixel_format):
        reg_read = MMIORegister()

        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % (self.platform))
        display_base_obj = DisplayBase(display)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
        current_pipe = chr(int(current_pipe) + 65)

        plane_ctl_reg = plane_ctl_reg + '_' + current_pipe
        plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, 0x0)

        plane_enable = plane_ctl_value.__getattribute__("plane_enable")
        if (plane_enable == getattr(plane_ctl, "plane_enable_DISABLE")):
            logging.critical("Plane is not enabled")
            self.fail("Plane is not enabled")

        source_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")
        logging.info("source_pixel_format %s" % source_pixel_format)
        logging.info("expected_pixel_format %s" % expected_pixel_format)
        if (source_pixel_format == getattr(plane_ctl, expected_pixel_format)):
            logging.info("Pixel format register verification passed")
        else:
            logging.error("Pixel format register verification failed")

    ##
    # @brief        Verify Planes
    # @return       None
    def disable_push_notifications(self):
        logging.debug("Disabling Push Notifications")
        hkey = "HKEY_CURRENT_USER"
        registry_path = r"Software\Microsoft\Windows\CurrentVersion"
        cmd = "bin\subinacl"
        os.system('%s /keyreg %s\%s /grant="%s"=f' % (cmd, hkey, registry_path, getpass.getuser()))
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER, reg_path=registry_path)
        registry_access.write(args=legacy_reg_args, reg_name="PushNotifications",
                              reg_type=registry_access.RegDataType.DWORD, reg_value=0x0)

    ##
    # @brief        Play media function
    # @param[in]    bfullscreen - status of full screen
    # @return       media_window_handle - Window Media Handle
    def play_media(self, bfullscreen):
        app_media = AppMedia(self.media_file)
        app_media.open_app(bfullscreen, minimize=True)
        media_window_handle = app_media.instance

        return media_window_handle

    ##
    # @brief        Function to do Mouse Move
    # @return       bool
    def cursor_move(self):
        current = win32api.GetCursorPos()
        cx = current[0]
        cy = current[1]

        nx = 0
        ny = 0
        step_size = 10
        cursor_move_delay = 0.3
        enumerated_displays = self.display_config.get_enumerated_display_info()
        cfg_topology, display_port, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
            enumerated_displays)

        if "SINGLE" in cfg_topology:
            if "MANL" in self.verifiers:
                messagebox.showinfo("Test Cursor",
                                    "Starting Cursor Test\n[Cursor will move along border of Panel in steps of 10 Pixels]")

            target_id = self.display_config.get_target_id(display_port[0], enumerated_displays)
            current_mode = self.display_config.get_current_mode(target_id)
            hor_range = int(current_mode.HzRes / step_size)
            ver_range = int(current_mode.VtRes / step_size)

            for x in range(step_size + 1):
                win32api.SetCursorPos((int(nx), int(ny)))
                time.sleep(cursor_move_delay)
                ny = ny + ver_range

            for i in range(step_size + 1):
                win32api.SetCursorPos((int(nx), int(ny)))
                time.sleep(cursor_move_delay)
                nx = nx + hor_range

            for i in range(step_size + 1):
                win32api.SetCursorPos((int(nx), int(ny)))
                time.sleep(cursor_move_delay)
                ny = ny - ver_range

            for i in range(step_size + 2):
                win32api.SetCursorPos((int(nx), int(ny)))
                time.sleep(cursor_move_delay)
                nx = nx - hor_range

            if "MANL" in self.verifiers:
                result = messagebox.askquestion("Test Cursor", "Did you see Cursor Movement? ",
                                                icon='warning')
                if result == 'yes':
                    logging.info("User Input Cursor Move - PASS")
                else:
                    logging.error("User Input Cursor Move - FAIL")
            logging.info("Cursor Move - Successful")
        self.seq_counter += 0.1
        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                           msg="Successfully Verified Cursor Move"))
        self.enabling_de_verifiers()
        self.seq_counter = math.floor(self.seq_counter)
        return True

    ##
    # @brief        Window Rotation Function
    # @return       None
    def window_rotation(self):
        if "MANL" in self.verifiers:
            messagebox.showinfo("Test Window Rotation", "Starting Display Orientation Test\n[Rotation 90 Deg]")
        enumerated_displays = self.display_config.get_enumerated_display_info()
        cfg_topology, display_ports, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
            enumerated_displays)
        for display in display_ports:
            target_id = self.display_config.get_target_id(display, enumerated_displays)
            temp_mode = self.display_config.get_current_mode(target_id)

            temp_mode.rotation = 2
            self.display_config.set_display_mode([temp_mode])
            if "MANL" in self.verifiers:
                result = messagebox.askquestion("Test Window Rotation", "Did you see Desktop\nRotate to [90 Deg]? ",
                                                icon='warning')
                if result == 'yes':
                    logging.info("User Input Window Rotation - PASS")
                else:
                    logging.error("User Input Window Rotation - FAIL")
            time.sleep(7)
            temp_mode.rotation = 1
            self.display_config.set_display_mode([temp_mode])

            if "MANL" in self.verifiers:
                result = messagebox.askquestion("Test Window Rotation",
                                                "Did you see Desktop\nRotate to [0 Deg] Normal? ",
                                                icon='warning')
                if result == 'yes':
                    logging.info("User Input Window Rotation - PASS")
                else:
                    logging.error("User Input Window Rotation - FAIL")
        self.seq_counter += 0.1
        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                           msg="Successfully Verified Window Rotation"))
        self.enabling_de_verifiers()
        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief        Verifies audio endpoint enumeration
    # @return       None
    def verify_audio_endpoints(self):
        status = False
        second_postfix = ''

        enumerated_displays = self.display_config.get_enumerated_display_info()
        cfg_topology, display_port, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
            enumerated_displays)

        if "SINGLE" in cfg_topology:
            if "MANL" in self.verifiers:
                messagebox.showinfo("Test Audio", "Starting Display Audio EndPoints Verification")

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
                        "\tPASS: Display Audio endpoint verification passed successfully (~{0} second{1})".format(
                            sec + 1, second_postfix))
                    status = True
                    break
                time.sleep(1)

            if status is False:
                self.fail("\tDisplay Audio endpoint verification failed (~{0} seconds)".format(
                    AUDIO_ENDPOINT_ENUMERATION_DURATION))
            self.seq_counter += 0.1
            logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                               msg="Successfully Verified Audio Endpoints"))
            self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief        Basic HDCP Verification
    # @return       bool - HDCP Verification status
    def basic_hdcp_verification(self):
        status = False
        if "MANL" in self.verifiers:
            messagebox.showinfo("Test HDCP",
                                "Starting Display Content Protection Test [HDCP]\nFor Type - 0 & Type - 1 content")
        # Check tool is present or not
        # If the tool is not available exit the test
        if os.path.exists(OPMTEST_BINARY_PATH + "\\OPMTester.exe") is False:
            self.fail("OPM tool is not present")
        else:
            for index in range(1, 5):
                # Start the automation commandline
                if self.hdcp_type == HDCPType.HDCP_1_4:
                    os.system("\"" + OPMTEST_BINARY_PATH + "\\OPMTester.exe\" -type0 > hdcp_log.txt")
                else:
                    if self.hdcp_type == HDCPType.HDCP_2_2:
                        os.system(
                            "\"" + OPMTEST_BINARY_PATH + "\\OPMTester.exe\" -type1 > hdcp_log.txt")
                    else:
                        self.fail("Invalid HDCP_TYPE. Possible values for HDCP_TYPE are {0} and {1}".format(
                            HDCPType.HDCP_1_4.value, HDCPType.HDCP_2_2.value))

                time.sleep(15)

                # check the results(total, pass, fail) and display information(portId, HDCPCapability, ConnectorType)
                [display_info, test_result] = self.parse_log_file()

                for display in display_info:
                    if display['HDCPCapability'] is True:
                        if display['HDCP_TYPE'] != self.hdcp_type:
                            self.hdcp_type = 1
                            if self.hdcp_type == HDCPType.HDCP_2_2:
                                logging.info("PASS: Expected HDCP 2.2 Panel, Actual= HDCP 2.2 Panel")
                        else:
                            self.hdcp_type = 0
                            if self.hdcp_type == HDCPType.HDCP_1_4:
                                logging.info("PASS: Expected HDCP 1.4 Panel, Actual= HDCP 1.4 Panel")

                # Condition for checking test results are updated correctly
                if test_result and (test_result != False):
                    if test_result['total_test_cases'] and test_result['total_pass']:
                        if test_result['total_fail'] == '0' and \
                                (test_result['total_test_cases'] != '0') and \
                                (test_result['total_test_cases'] == test_result['total_pass']):
                            status = True
                            break
                time.sleep(15)
        return status

    ##
    # @brief        Verify HDCP
    # @return       None
    def verify_hdcp(self):
        status = self.basic_hdcp_verification()
        enumerated_displays = self.display_config.get_enumerated_display_info()
        cfg_topology, display_port, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
            enumerated_displays)

        # Verify HDCP activation/deactivation
        if len(display_port) == 1 and display_port[0] == 'DP_A':
            if status is True:
                logging.error('HDCP verification failed')
            else:
                if "MANL" in self.verifiers:
                    result = messagebox.askquestion("Test HDCP",
                                                    "HDCP Testing Done\nDid you see any Corruption or Flickering? ",
                                                    icon='warning')
                    if result == 'yes':
                        logging.error("User Input Verify HDCP - FAIL")
                    else:
                        logging.info("User Input Verify HDCP - PASS")
                logging.info('HDCP verification passed successfully')
        else:
            if status is False:
                logging.error('HDCP verification failed')
            else:
                if "MANL" in self.verifiers:
                    result = messagebox.askquestion("Test HDCP",
                                                    "HDCP Testting Done\nDid you see any Corruption or Flickering? ",
                                                    icon='warning')
                    if result == 'yes':
                        logging.error("User Input Verify HDCP - FAIL")
                    else:
                        logging.info("User Input Verify HDCP - PASS")
                logging.info('HDCP verification passed successfully')
        self.seq_counter += 0.1
        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                           msg="Successfully Verified HDCP"))
        # Remove old logs
        os.system("del hdcp_log*")
        os.system("del OPM*.log")
        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief        Parse hdcp_log.txt file, returns display_info and test_result
    # @return       (display_info,test_result) - (Display Information, Test results)
    def parse_log_file(self):
        current_line_index = 0
        is_display_info_set = False
        test_result = {}  # stores the results for test; test_result{total, fail, pass}
        display_info = []  # stores the display information for all the available displays;
        # display_info[{PortID, HDCPCapability, ConnectoryType, HDCP_TYPE}]

        ##
        # if the log file is not generated, exit
        if os.path.exists("hdcp_log.txt") is False:
            logging.debug("Log file hdcp_log.txt is not generated")
            return [False, False]

        try:
            log_file = open("hdcp_log.txt", "r")
        except IOError:
            self.fail('Failed to open hdcp_log.txt')
        else:
            lines = log_file.readlines()
            log_file.close()

        if len(lines) < 1:
            logging.debug("Log file hdcp_log.txt has no content")
            return [False, False]

        for line in lines:
            display_info_property_list = line.strip().split("\t")
            if len(display_info_property_list) < 1:
                continue

            # PortID, HDCPCapbility, HDCPLocalLevel, ConnectorType for all connected display_path
            if display_info_property_list[0] == "PortID" and is_display_info_set is False:
                next_line_index = current_line_index + 2

                display_info_property_data = lines[next_line_index].strip()
                if len(display_info_property_data) > 0:
                    while display_info_property_data[0] != '*':
                        display_info_temp = {
                            'PortID': display_info_property_data[0],
                            'HDCPCapability': False,
                            'HDCP_TYPE': None
                        }
                        if display_info_property_data.find('Not Supported') == -1:
                            display_info_temp['HDCPCapability'] = True
                            if display_info_property_data.find('HDCP_TYPE_ENFORCEMENT') == -1:
                                display_info_temp['HDCP_TYPE'] = 0
                            else:
                                display_info_temp['HDCP_TYPE'] = 1

                        display_info.append(display_info_temp)
                        next_line_index += 1
                        display_info_property_data = lines[next_line_index].strip()

                        if len(display_info_property_data) > 0:
                            continue
                        else:
                            break
                is_display_info_set = True

            # Total test cases, Total Fail, Total Pass
            if len(display_info_property_list[0]) > 0:
                if display_info_property_list[0][0] == '#':
                    result = display_info_property_list[0][2:].split(": ")
                    if result[0] == 'Total TestCases':
                        test_result['total_test_cases'] = result[1]
                    if result[0] == 'Total Pass':
                        test_result['total_pass'] = result[1]
                    if result[0] == 'Total Fail':
                        test_result['total_fail'] = result[1]

            current_line_index += 1
        return [display_info, test_result]

    ##
    # @brief        Unit-test teardown function
    # @return       None
    def tearDown(self):
        logging.info("Test Clean Up")
        window_helper.close_media_player()
        # Remove old logs
        os.system("del hdcp_log*")
        os.system("del OPM*.log")
        logging.debug("Successfully removed previous log files")

        # self.unplug_displays()
        ##
        # Check Underrun
        result = self.underrunstatus.verify_underrun()
        logging.error("UnderRun Observed")

        ##
        # Check TDR
        result = display_essential.detect_system_tdr(gfx_index='gfx_0')
        self.assertNotEquals(result, True, "Aborting Test as TDR happened while Executing Test")

    ##
    # @brief        plug_unplug with both versions of SHE Tool
    # @param[in]    SHE_device - SHE device version
    # @return       status of plug/unplug
    def HPD_with_SHE(self, SHE_device):
        selected_ports = []
        if SHE_device == 1.0:
            enumerated_displays = self.display_config.get_enumerated_display_info()
            cfg_topology, display_ports, display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex(
                enumerated_displays)
            selected_ports = display_ports
        elif SHE_device == 2.0:
            selected_ports = self.enumport
        for port in selected_ports:
            try:
                if "MANL" in self.verifiers:
                    messagebox.showinfo("Test HPD", "Starting HPD Test, Unplug followed by Plug will happen.")
                self.seq_counter += 0.1
                if self.she_utility.hot_plug_unplug(self.get_display_id_Diempel(port), False, 5):

                    logging.info("Pass: {} Unplug Successful".format(port))
                    logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                       msg="{} Unplug Successful".format(port)))
                    time.sleep(10)
                    if "MANL" in self.verifiers:
                        result = messagebox.askquestion("Test HPD", "Did you see Unplug {}?".format(port),
                                                        icon='warning')
                        if result == 'yes':
                            logging.info("User Input Test HPD - PASS")
                        else:
                            logging.error("User Input Test HPD - FAIL")
                else:
                    logging.error("Fail: {} Unplug Failed".format(port))
                    logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                       msg="{} Unplug Failed".format(port)))
                    return False

                self.seq_counter += 0.1
                if self.she_utility.hot_plug_unplug(self.get_display_id_Diempel(port), True, 5):
                    logging.info("Pass: {} PLUG Successful".format(port))
                    logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                       msg="{} Plug Successful".format(port)))
                    time.sleep(10)
                    if "MANL" in self.verifiers:
                        result = messagebox.askquestion("Test HPD", "Did you see Plug {}?".format(port),
                                                        icon='warning')
                        if result == 'yes':
                            logging.info("User Input Test HPD - PASS")
                        else:
                            logging.error("User Input Test HPD - FAIL")
                    self.enabling_de_verifiers()
                else:
                    logging.error("Fail: {} PLUG Failed".format(port))
                    logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                       msg="{} Plug Failed".format(port)))
                    return False

            except Exception as ex:
                logging.error("Exception: {}".format(ex))
                return False
        self.seq_counter = math.floor(self.seq_counter)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
