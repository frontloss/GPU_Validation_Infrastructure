########################################################################################################################
# @file         darkscreen_detection_base.py
# @brief        DarkScreenDetectionBase class contains the common APIs used for darkscreen detection.
#               DarkScreenDetectionBase provides common setUp() functions of UnitTest Framework.
# @details      Sample command: Tests\DarkScreen_Detection\Pre_Si\darkscreen_detection_singleplane.py -EDP_A
# @author       Nivetha.B
########################################################################################################################

import os
import sys
import logging
import time
import unittest
from ctypes.wintypes import RGB
from enum import IntEnum
from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import system_utility
from Libs.Core import window_helper
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.Verifier.dispdiag_verification import verify_dispdiag_intrusive_data
from Libs.Core.winkb_helper import press
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.presi import presi_crc_env_settings
from Tests.test_base import TestBase
from Tests.Color.Features.YCbCr import ycbcr
from Tests.Color.Common.color_enums import YuvSampling
from Tests.Planes.Common.hdr_base import HDRBase
from Tests.Planes.Common.mpo_base import MPOBase
from Tests.PowerCons.Modules import common

IMAGE_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, r"Color\HDR\Images")
##
# @brief        Exposed enum class for common App actions
class Color(IntEnum):
    BLACK = RGB(0, 0, 0)
    WHITE = RGB(255, 255, 255)
    RED = RGB(255, 0, 0)
    GREY = RGB(128, 128, 128)


##
# @brief - Dark screen detection Test Base
class DarkScreenDetectionBase(unittest.TestCase):
    connected_list = []
    source_id = []
    targetId = []
    displays_in_cmdline = []
    current_mode = []
    step_counter = 0
    underrun = UnderRunStatus()
    machine_info = SystemInfo()
    display_config = display_config.DisplayConfiguration()
    hdr = HDRBase()
    no_displays = 0

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info('********************* TEST  STARTS HERE **************************')
        self.exec_env = system_utility.SystemUtility().get_execution_environment_type()

        ##
        # Parse the commandlines
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)
        ##
        # Obtain display port list from the command line.
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])
                    self.displays_in_cmdline.append(value['connector_port'])

        ##
        # Verify and plug the display.
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail("Minimum 1 display is required to run the test")
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Apply Display configuration
        if len(self.connected_list) > 1:
            topology = enum.EXTENDED
            if self.display_config.set_display_configuration_ex(topology, self.connected_list) is False:
                self.fail("Step %s : Failed to apply display configuration %s %s" % (
                    (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))

            logging.info(" Step %s : Applied display configuration successfully as %s %s" % (
                (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))
            self.current_config = self.display_config.get_current_display_configuration()
            self.targetId = self.current_config.displayPathInfo[1].targetId
            self.source_id.insert(0, self.current_config.displayPathInfo[1].sourceId)
        else:
            topology = enum.SINGLE
            if self.display_config.set_display_configuration_ex(topology, self.connected_list) is False:
                self.fail("Step %s : Failed to apply display configuration %s %s" % (
                    (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))
            logging.info(" Step %s : Applied display configuration successfully as %s %s" % (
                (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))
            self.current_config = self.display_config.get_current_display_configuration()
            self.targetId = self.current_config.displayPathInfo[0].targetId
            self.source_id.insert(0, self.current_config.displayPathInfo[0].sourceId)

        # Start underrun monitor.
        if self.underrun.verify_underrun():
            self.fail("Underrun Occured")
        self.underrun.clear_underrun_registry()

    ##
    # @brief        Cleanup the plugged displays after darkscreen verification.
    # @return       None
    def tearDown(self) -> None:
        logging.info('Cleaning up the DarkScreen Detection base class.')
        for display in self.plugged_display:
            display_utility.unplug(display)

    ##
    # @brief        Verify if darkscreen is detected
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    black_bg - True if black background, False otherwise
    # @return       status
    def verify_dark_screen(self, gfx_index="gfx_0", black_bg=True):
        status = True
        environment = system_utility.SystemUtility().get_execution_environment_type()
        # If environment is Pre-si then only exercise this, on POST-SI, it is internally handled
        if environment in ["SIMENV_FULSIM"]:
            self.hdr.perform_plane_processing()
        # if wait for vbi flag is present, wait until next VBI, currently it is done only for PIPE_A, gfx_0
        if environment in ["SIMENV_PIPE2D"]:
            MPOBase().wait_for_vbi(0, gfx_index)
        scanout_state_output = verify_dispdiag_intrusive_data(gfx_index)
        # Closing the image after Intrusive data verification
        press('ALT+F4')
        for display, is_blackscreen in scanout_state_output.items():
            for disp in self.displays_in_cmdline:
                if display == disp:
                    if black_bg:
                        if is_blackscreen is False:
                            logging.error(f"FAIL: Expected: Black screen detected, Actual: Black screen is not detected"
                                          f"on {display}")
                            status = False
                        logging.info(f"PASS: Black screen is detected on {display}")
                    else:
                        if is_blackscreen:
                            logging.error(f"FAIL: Expected: No Black screen detected, Actual: Black screen is detected"
                                          f"on {display}")
                            status = False
                        logging.info(f"PASS: Black screen is not detected on {display}")
        return status

    ##
    # @brief        Set background image
    # @param[in]    image - Image to apply for background
    # @return       None
    def set_background(self, image):
        logging.info(f"Setting Desktop background")
        # set desktop background to  solid color
        press('WIN+M')
        image_file = os.path.join(IMAGE_PATH, image)
        os.system(image_file)
        time.sleep(3)
        press('SHIFT+TAB')
        press('ENTER')
        time.sleep(5)


    ##
    # @brief        Set solid background
    # @param[in]    color - Color to apply for background
    # @param[in]    plain_bg - True if hide desktop icons, False otherwise
    # @return       None
    def set_background_pre_si(self, color, plain_bg=True):
        # This function to be used only for pre-si
        logging.info(f"Setting Desktop background")
        # set desktop background to  solid color
        presi_crc_env_settings.set_desktop_color(color)
        # Keeping a timeout for pre-si as it would take long to load the data.
        time.sleep(40)
        # Hide desktop icons and show background image only
        hide_desktop_icons = True if plain_bg else False
        window_helper.hide_desktop_icons(hide_desktop_icons)
        time.sleep(20)
        window_helper.show_desktop_bg_only(True)
        time.sleep(120)

    ##
    # @brief Applies Native Mode
    # @return screen resolution
    def apply_native_mode(self):
        logging.debug("FUNC_ENTRY: apply_native_mode ")
        width, height = None, None
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            target_id = enumerated_displays.ConnectedDisplays[index].TargetID
            native_mode = self.display_config.get_native_mode(target_id)
            if native_mode is None:
                logging.error(f"Failed to get native mode for {target_id}")
                return False
            edid_hz_res = native_mode.hActive
            edid_vt_res = native_mode.vActive
            edid_RR = native_mode.refreshRate
            supported_modes = self.display_config.get_all_supported_modes([target_id])
            for key, values in supported_modes.items():
                for mode in values:
                    if mode.HzRes == edid_hz_res and mode.VtRes == edid_vt_res and mode.refreshRate == edid_RR:
                        if self.display_config.set_display_mode([mode]):
                            width, height = mode.HzRes, mode.VtRes
                            logging.info(f"Successfully applied {mode} mode")
                        else:
                            logging.error(f"Failed to apply {mode} Mode")
        return width, height

    ##
    # @brief Converts bin to png
    # @param[in] width - Horizontal resolution of screen.
    # @param[in] height - Vertical resolution of screen.
    # @param[in] input_file - Binary file to convert.
    # @return output image path
    def convert_bin_to_png(self, width, height, input_file):
        input_file = os.path.join(IMAGE_PATH, input_file)
        exe_path = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR\\BIN_to_PNG_Converter.exe')
        output_file = os.path.join(IMAGE_PATH, "black_image.png")
        commandline = exe_path + ' -i ' + input_file + ' -o ' + output_file + ' -w ' + str(width) + ' -h ' + str(height)
        os.system(commandline)
        return output_file
