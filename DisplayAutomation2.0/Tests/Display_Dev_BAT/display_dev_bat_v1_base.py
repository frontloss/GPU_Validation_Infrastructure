######################################################################################
# \file
# \remarks
# \ref display_dev_bat_v1_base.py \n
# It contains setUp and tearDown methods of unittest framework. For all Display Dev BAT tests
# which is derived from this, will make use of setup/teardown of this base class.
# This script contains helper functions that will be used by Display Dev BAT test scripts.
#
# \authors Raghupathy, Dushyanth Kumar, Balaji Gurusamy
######################################################################################
import copy
import importlib
import logging
import math
import os
import sys
import time
import unittest
from xml.etree import ElementTree as ET

import win32api

from Libs.Core import app_controls, cmd_parser, display_utility, display_essential, enum, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, ScanlineOrdering
from Libs.Core import display_power
from Libs.Core.machine_info.machine_info import SystemInfo, SystemDriverType
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Core.Verifier.common_verification_args import VerifierCfg
from registers.mmioregister import MMIORegister
from Libs.Core.logger import html

##
# New level of logging for Test Sequence Flow
STEP = 25
logging.addLevelName(STEP, "STEP")

Delay_After_Power_Event = 10
Delay_5_Secs = 5


def add_or_append(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    if value not in dictionary[key]:
        dictionary[key].append(value)


##
# Display Dev Bat V1 Base class : To be used in Display DEV BAT tests
class DisplayDevBatV1Base(unittest.TestCase):
    display_power = display_power.DisplayPower()
    display_engine = DisplayEngine()
    display_config = DisplayConfiguration()
    machine_info = SystemInfo()
    underrunstatus = UnderRunStatus()
    platform = None
    display_list = []
    displays_dict = {}
    sequence_list = []
    power_events = []
    user_mpo_events = []
    mode_level = ''
    de_result = True
    enumerated_displays = None
    seq_counter = 0.0
    de_verify = 'ON'
    test_sequence_format = "    Test Sequence:{seq:^5}: {msg:<35}"
    test_results = True
    buffer_list = []

    ##
    # Set control variable based on command line options
    environment_mode = "EMU"
    cmdline_args = sys.argv
    for arg in cmdline_args:
        if arg.upper() == "-SIM":
            environment_mode = "SIM"
            cmdline_args.remove("-SIM")
        elif arg.upper() == "-EMU":
            environment_mode = "EMU"
            cmdline_args.remove("-EMU")

    ##
    # @brief Unit-test setup function.
    # @param[in] - void
    # @return - void
    def setUp(self):

        self.my_custom_tags = ['-usr_eve', '-pwr_eve', '-mode_lvl', '-de_verify']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)

        html.step_start("Test Setup")
        ##
        # Start Underrun
        self.underrunstatus.clear_underrun_registry()

        ##
        # connected_list[] is a list of Port Names of the connected Displays
        for index in range(len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if not (self.display_list.__contains__(value['connector_port'] + " " + value["gfx_index"])):
                            self.buffer_list.append(value['connector_port'])
                            self.buffer_list.append(value['panel_index'])
                            add_or_append(self.displays_dict, value['gfx_index'], self.buffer_list)
                            self.display_list.insert(value['index'],
                                                     (value['connector_port'] + " " + value["gfx_index"]))
                            self.buffer_list = []
                if key == 'USR_EVE':
                    self.user_mpo_events = value

                if key == 'PWR_EVE':
                    self.power_events = value

                if key == 'MODE_LVL':
                    self.mode_level = value

                if key == 'DE_VERIFY':
                    self.de_verify = value

        display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for count in range(len(display_hwinfo)):
            self.platform = str(display_hwinfo[count].DisplayAdapterName).lower()
            break
        self.os_info = self.machine_info.get_os_info()

        ##
        # Pre Requisites for playing Video Clip
        self.media_2k_file = os.path.join(test_context.TestContext.test_store(), "MPO\\mpo_1920_1080_avc.mp4")
        self.media_4k_file = os.path.join(test_context.TestContext.test_store(), "MPO\\mpo_3840_2160_avc.mp4")
        window_helper.close_browser()
        window_helper.close_media_player()
        self.prepare_sequence()
        html.step_end()

    ##
    # verifying Display Engine
    def verify_display_engine(self):
        if 'OFF' not in self.de_verify:
            self.de_result &= self.display_engine.verify_display_engine()

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
    # @brief create a map for the displays and sequences
    # @param[in] - void
    # @return - Bool
    def prepare_sequence(self):
        tree = ET.parse(test_context.ROOT_FOLDER + r'\Tests\Display_Dev_BAT\DisplaySequence.xml')
        root = tree.getroot()
        dd = self.dictify(root)
        aa = dd["Sequences"]
        # Block for sequence selection according to number of displays
        if len(self.display_list) == 2:
            self.sequence_list = list(dict(aa['Seq1'][0]).values())[0]
        elif len(self.display_list) == 3:
            self.sequence_list = list(dict(aa['Seq2'][0]).values())[0]
        elif len(self.display_list) == 4:
            self.sequence_list = list(dict(aa['Seq3'][0]).values())[0]
        else:
            self.sequence_list = list(dict(aa['Seq1'][0]).values())[0]

    ##
    # @brief create a map for the displays and sequences
    # @param[in] - String : display_str
    # @return - Bool
    def map_seq_displays(self, display_str):
        disp_str_list = str(display_str).split(",")
        return list(map(lambda x: self.display_list[int(x) - 1], disp_str_list))

    ##
    # @brief Set the given config along with displays
    # @param[in] - String : config
    # @param[in] - String[] : List of displays
    # @return - None
    def apply_config_and_verify(self, config, displays, is_de_verification_needed, TopologyList):
        
        cfg = None
        html.step_start("Applying {0} Display Config on {1}".format(config, TopologyList))
        if len(self.display_list) < len(displays):
            logging.info("Ignoring the config {0} in sequence since planned test has only {1} displays".
                         format(config, str(len(self.display_list))))
        else:
            if config == 'SINGLE':
                cfg = enum.SINGLE
            elif config == 'CLONE':
                cfg = enum.CLONE
            elif config == 'EXTENDED':
                cfg = enum.EXTENDED
            self.seq_counter += 0.1
            if self.display_config.set_display_configuration_ex(cfg, displays, self.enumerated_displays) is False:
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Failed to Apply Config Topology. Test Failed"))
                html.step_end()
                self.fail("Apply Config Failed")
            else:
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Successfully Applied Config."))
                html.step_end()
                if is_de_verification_needed:
                    self.verify_display_engine()
        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief Perform power events CS,S3 and S4
    # @param[in] - void
    # @return - Bool
    def trigger_powerevents_and_verify(self):
        power_state_enums = {}
        for event in self.power_events:
            if event == 'CS':
                if self.display_power.is_power_state_supported(display_power.PowerEvent.CS):
                    power_state_enums['CS'] = display_power.PowerEvent.CS
                else:
                    logging.warning("Machine Does NOT Support CS")
            if event == 'S3':
                if not self.display_power.is_power_state_supported(display_power.PowerEvent.CS):
                    power_state_enums['S3'] = display_power.PowerEvent.S3
                else:
                    logging.warning("Machine Does NOT Support S3")
            if event == 'S4':
                power_state_enums['S4'] = display_power.PowerEvent.S4

        if power_state_enums != 0:
            for key, value in power_state_enums.items():
                self.seq_counter += 0.1
                if self.display_power.invoke_power_event(value, 60):
                    time.sleep(Delay_5_Secs)                    
                    self.verify_display_engine()
                else:
                    self.test_results &= False
                time.sleep(Delay_After_Power_Event)

        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief Unit- Unplug the displays
    # @param[in] - void
    # @return - void
    def unplug_all_external_displays(self):
        if self.enumerated_displays is None and self.enumerated_displays.Count == 0:
            logging.error("Enumerated Displays is NONE")
            self.fail("Enumerated Displays is NONE")
        internal_display_list = self.display_config.get_internal_display_list(self.enumerated_displays)
        for display in self.enumerated_displays.ConnectedDisplays:
            connector_port = CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name
            if (connector_port not in (x[1] for x in internal_display_list)) and (connector_port != 'DispNone'):
                display_utility.unplug(connector_port)

    ##
    # @brief Apply modes and verify
    # @param[in] - Adapter Info list, Enumerated Displays, Mode Levels to be applied
    # @return - None
    def apply_modes_and_verify(self, adapter_info_list, enum_displays, mode_level):
        supported_modes = self.display_config.get_all_supported_modes(adapter_info_list)
        key = None
        if "L1" in mode_level or "l1" in mode_level:
            for key, values in supported_modes.items():
                for mode in values:
                    self.seq_counter += 0.1
                    html.step_start("Applying Mode {0} x {1} @ {2}  on Target ID {3}".format(mode.HzRes, mode.VtRes, mode.refreshRate, mode.targetId))
                    logging.info(mode.to_string(enum_displays))

                    if self.display_config.set_display_mode([mode]):
                        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                           msg="Successfully Applied Mode : {} x {} @ {} {}".format(
                                                                               mode.HzRes, mode.VtRes, mode.refreshRate,
                                                                               (ScanlineOrdering(
                                                                                   mode.scanlineOrdering)).name)))
                        html.step_end()
                        self.seq_counter += 0.1
                        self.verify_display_engine()
                    else:
                        logging.error("Set display mode: Failed".format(key))
                        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                           msg="Set display mode: Failed".format(
                                                                               key)))
                        self.test_results &= False
                        html.step_end()

        elif "L0" in mode_level or "l0" in mode_level:
            for adapter_info in adapter_info_list:
                modes = []
                for key, values in supported_modes.items():
                    if key == adapter_info.TargetID:
                        no_of_modes = len(values)
                        modes.append(values[0])
                        modes.append(values[no_of_modes // 2])
                        modes.append(values[no_of_modes - 1])

                for mode in modes:
                    self.seq_counter += 0.1
                    html.step_start("Applying Mode {0} x {1} @ {2}  on Target ID {3}".format(mode.HzRes, mode.VtRes, mode.refreshRate, mode.targetId))
                    logging.info(mode.to_string(enum_displays))

                    if self.display_config.set_display_mode([mode]):
                        logging.log(
                            STEP, self.test_sequence_format.format(
                                seq=self.seq_counter,
                                msg="Successfully Applied Mode : "
                                    "{} x {} @ {} {}".format(mode.HzRes, mode.VtRes,
                                                             mode.refreshRate,
                                                             (ScanlineOrdering(mode.scanlineOrdering)).name)
                            )
                        )
                        html.step_end()
                        self.seq_counter += 0.1
                        self.verify_display_engine()
                    else:
                        logging.error("Set display mode: Failed".format(key))
                        logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                           msg="Set display mode: Failed".format(
                                                                               key)))
                        self.test_results &= False
                        html.step_end()
        else:
            logging.info("Provide Mode level as L0/L1 to Apply Mode Set")
        self.seq_counter = math.floor(self.seq_counter)

    ##
    # @brief Playing Video Clip, Mouse Move and Verifying MPO
    # @param[in] - void
    # @return - None
    def play_video_clip_and_verify_mpo(self, display_port, config):
        html.step_start("Playing Video Clip and verifying MPO")
        logging.info("********Display Port :{}********".format(display_port))
        media_file = ""
        plane1_pixelformat = ""
        for mpo_events in self.user_mpo_events:
            self.seq_counter += 0.1
            if "MPO1" in mpo_events:
                media_file = self.media_2k_file
            elif "MPO2" in mpo_events:
                media_file = self.media_4k_file
            else:
                logging.info("Provide Valid USER MPO EVENTS MPO1/MPO2")
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Provide Valid USER EVENTS as -usr_eve "
                                                                       "MPO1/MPO2 for MPO Verification"))
                self.test_results &= False

            app_controls.launch_video(media_file)
            time.sleep(30)
            # MPO plane verification not supported in CLONE Config
            if config != 'CLONE':
                plane1_pixelformat = "source_pixel_format_NV12_YUV_420"
                self.verify_planes(display_port, 'PLANE_CTL_1', plane1_pixelformat)
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Successfully Verified Pixel Format Register"))

            if self.mouse_move():
                self.seq_counter += 0.1
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Successfully Moved Cursor"))
            else:
                logging.error("Cursor Move Failed")
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter, msg="Cursor Move Failed"))
                self.test_results &= False

            time.sleep(15)
            # MPO plane verification not supported in CLONE Config
            if config != 'CLONE':
                self.verify_planes(display_port, 'PLANE_CTL_1', plane1_pixelformat)
                self.seq_counter += 0.1
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Successfully Verified Pixel Format Register"))

            if self.mouse_move():
                self.seq_counter += 0.1
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                                   msg="Successfully Moved Cursor"))
            else:
                logging.error("Cursor Move Failed")
                logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter, msg="Cursor Move Failed"))
                self.test_results &= False
            time.sleep(10)
            logging.info("Successfully Played "'"{0}"'" Video Clip".format(media_file))
            self.seq_counter += 0.1
            logging.log(STEP, self.test_sequence_format.format(seq=self.seq_counter,
                                                               msg="Successfully Played "'"{0}"'" Video Clip".format(
                                                                   media_file)))

            window_helper.close_media_player()
            # maxmize all windows after media player closed. Then only desktop not going to idle state.
            window_helper.restore_all_windows()
            html.step_end()
            self.verify_display_engine()

        self.seq_counter = math.floor(self.seq_counter)

    def verify_planes(self, display, plane_ctl_reg, expected_pixel_format):
        reg_read = MMIORegister()

        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % self.platform)
        display_base_obj = DisplayBase(display)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
        current_pipe = chr(int(current_pipe) + 65)

        plane_ctl_reg = plane_ctl_reg + '_' + current_pipe
        plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform, 0x0)

        plane_enable = plane_ctl_value.__getattribute__("plane_enable")
        if plane_enable == getattr(plane_ctl, "plane_enable_DISABLE"):
            logging.critical("Plane is not enabled")
            self.test_results &= False

        source_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")
        logging.info("source_pixel_format %s" % source_pixel_format)
        logging.info("expected_pixel_format %s" % expected_pixel_format)
        if source_pixel_format == getattr(plane_ctl, expected_pixel_format):
            logging.info("Pixel format register verification passed")
        else:
            logging.error("Pixel format register verification failed")
            self.test_results &= False

    ##
    # @brief Function to verify drivers are Enabled or Disabled
    def is_driver_running(self):
        driver_info = self.machine_info.get_driver_info(SystemDriverType.GFX)
        if driver_info.DriverInfo[0].Status == "Running":
            return True
        elif driver_info.DriverInfo[0].Status == "Offline":
            return False
        else:
            self.fail("Aborting the Test as NOT able to get the Gfx Driver Status : {}".
                      format(driver_info.DriverInfo[0].Status))

    ##
    # @brief Function to do Mouse Move
    # @param[in] - void
    # @return - Bool
    def mouse_move(self):
        current = win32api.GetCursorPos()
        cx = current[0]
        cy = current[1]

        nx = cx + 2
        ny = cy + 2

        win32api.SetCursorPos((int(nx), int(ny)))
        current = win32api.GetCursorPos()
        cx = current[0]
        cy = current[1]
        if cx == nx and cy == ny:
            logging.info("Cursor Move - Successful")
        else:
            logging.error("Cursor Move - Failed")
            return False
        return True

    # @brief Unit-test teardown function.
    # @param[in] - void
    # @return - void
    def tearDown(self):
        html.step_start("Test Clean Up")
        window_helper.close_media_player()
        if self.enumerated_displays is None:
            self.enumerated_displays = self.display_config.get_enumerated_display_info()

        if self.environment_mode == 'SIM':
            self.unplug_all_external_displays()
        ##
        # Check Underrun
        result = self.underrunstatus.verify_underrun()
        self.assertEquals(result, False, "Aborting Test as UnderRun Observed")

        ##
        # Check TDR
        result = display_essential.detect_system_tdr(gfx_index='gfx_0')
        self.assertNotEquals(result, True, "Aborting Test as TDR happened while Executing Test")
        html.step_end()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
