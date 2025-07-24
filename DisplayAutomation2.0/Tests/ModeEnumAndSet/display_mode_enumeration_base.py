#######################################################################################################################
# @file         display_mode_enumeration_base.py
# @brief        This file contains validation of different mode enumarations for given DP/HDMI display
# @details      display_mode_enumeration.py contains ModeEnumAndSet class which implements setUp method to setup
#               the required environment and tearDown method to reset the environment by
#               unplugging the displays, un-initialize sdk, resetting any registry values etc.
#               Also contains some helper methods and variables that are required for mode enumeration.
#
# @author       Aafiya Kaleem, Golwala Ami, Supriya Krishnamurthi
#######################################################################################################################
import ctypes
import logging
import os
import sys
import time
import unittest
from enum import Enum, IntEnum
from xml.etree import ElementTree as ET

from Libs.Core.vbt.vbt import Vbt
from Libs.Core import system_utility
from Libs.Core import cmd_parser, display_utility, display_essential, driver_escape, enum, registry_access
from Libs.Core.display_config import display_config as display_cfg
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.context import GfxDriverType
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import etl_parser
from Libs.Core.logger import etl_tracer
from Libs.Core.test_env import test_context
from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_engine.de_base import display_dip_control, display_pipe, display_transcoder, display_plane
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumHelper, DisplayModeBlock, \
    DisplayModeControlFlags
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.powercons import registry
from Libs.Feature.display_mode_enum.mode_vic_info import VIC_MODE_INFO, DEFAULT_VIC_ID
from Tests.Color.Common import color_escapes, color_mmio_interface
from Tests.Color.color_common_utility import get_platform_info, get_current_pipe
from Tests.PowerCons.Modules import common
from Tests.VBT_Overrides.vbt_override_base import *
from registers.mmioregister import MMIORegister

color_mmio_interface = color_mmio_interface.ColorMmioInterface()
system_utility_ = system_utility.SystemUtility()


##
# @brief        A class of type Enum to define color formats supported.
class COLOR_FORMAT(Enum):
    RGB = 0
    YUV420 = 1
    YUV444 = 2
    YUV422 = 3


##
# @brief        A class of type Enum to define dongle types supported.
class DONGLE_TYPE(IntEnum):
    Default = 0  # Type2Adapter
    Type1Adapter = 1
    Type2Adapter = 2
    DviAdapter = 3
    LsPconAdapter = 4
    Type2Adapter_PS8469 = 5


##
# @brief        A variable of dictionary type to define bpc mapping
bpc_mapping = dict([
    (0, 6),
    (1, 8),
    (2, 10),
    (3, 12)
])

##
# @brief        A variable of dictionary type to define bpc mapping of EDID
bpc_mapping_of_edid = dict([
    (1, 6),
    (2, 8),
    (3, 10),
    (4, 12),
    (5, 14),
    (6, 16)
])

##
# @brief        A variable of dictionary type to define bpc mapping of PCON
bpc_mapping_of_pcon = dict([
    (0, 8),
    (1, 10),
    (2, 12),
    (3, 16),
])

frl_rate_mapping = dict([
    (0, 0),
    (1, 3),
    (2, 6),
    (3, 8),
    (4, 10),
    (5, 12),
])

##
# @brief        DPCD Offsets related to PCON.
class PconDpcdOffsets:
    DFPX_CAP = 0x80
    DOWN_STREAM_PORT_PRESENT = 0x5
    ADDITIONAL_HDMI_LINK_CAPABILITY = 0x82
    PROTOCOL_CONVERTER_CONTROL_1 = 0x3051
    FRL_LINK_CONFIGURATION_1 = 0x305A


##
# @brief        Regkeys related to HDMI
class RegKeys:
    HDMI_NO_NULL_PACKET_AND_AUDIO = "HdmiNoNullPacketAndAudio"


##
# @brief        A class which has some class methods, test methods to set the environment required for the ModeEnum test
#               case to run and also contains helper methods to be used by test case.
class ModeEnumAndSetBase(unittest.TestCase):
    targetId = display = None
    edp = False
    golden_mode_list = {}
    os_mode_list = []
    unsupported_mode_list = []
    unsupported_ignoremode_list = []
    apply_mode_list = {}
    ignore_mode_list = {}
    Platform = None
    platform_type = None
    hdmi_2_1_status = None
    max_frl_rate = 0
    lanes = 0
    display_and_adapter_info = None
    default_bpc = 'BPCDEFAULT'
    default_encoding = 'DEFAULT'

    SCALE_DICT = {'UN_SP': 0, 'Center': 1, 'Stretch': 2, 'MAR': 4, 'CAR': 8, 'Default': 64}
    RSCALE_DICT = {0: 'UN_SP', 1: 'Center', 2: 'Stretch', 4: 'MAR', 8: 'CAR', 64: 'Default'}
    RROTATION_DICT = {1: '0Deg', 2: '90Deg', 3: '180Deg', 4: '270Deg'}
    SCANLINE_DICT = {'Progressive': 1, 'Interlaced': 2}

    display_config = display_cfg.DisplayConfiguration()
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
    machine_info = SystemInfo()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for ModeEnum test case. Helps to initialize some of the
    #               parameters required for test execution.
    # @return       None
    def setUp(self):
        xml_file = None
        self.custom_mode_xml_file = None
        self.dpDongle = False
        verify_dvi_mode = False
        self.frl_to_set = None
        self.default_bpc_in_registry = 8
        self.is_bpc_set_using_registry = False

        logging.info("**************MODE ENUMERATION TEST START**************")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()

        ##
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.Platform = gfx_display_hwinfo[i].DisplayAdapterName
            self.platform_type = GfxDriverType.YANGRA if system_utility_.is_ddrw() else GfxDriverType.LEGACY
            break

        ##
        # Parse the command line arguments
        self.my_custom_tags = ['-xml', '-custom_modes_xml', '-reg', '-vbt']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.display = value['connector_port']
                else:
                    self.fail("Aborting the test as display is not passed in the command line")

            if key == 'EDP_A':
                self.edp = True
            elif key == 'XML':
                if value is not None:
                    xml_file = value[0]
                else:
                    self.fail("Aborting the test as xml file is not provided in command-line")
            ##
            # Parsing command line to get xml provided for custom modes.
            elif key == 'CUSTOM_MODES_XML':
                if value is not None:
                    self.custom_mode_xml_file = value[0]
                else:
                    self.fail("Aborting the test as custom modes xml file is not provided in command-line")
            elif key == "REG" and value != 'NONE':
                if value[0].lower() == "dvimode":
                    verify_dvi_mode = True
                else:
                    gdhm.report_test_bug_di("Provided Registry Key is incorrect", gdhm.ProblemClassification.OTHER)
                    self.fail("Aborting the test as incorrect or no registry key is provided in command line")
            elif key == "VBT" and value != 'NONE':
                if value[0].upper() in vbt_context.MAX_FRL_RATE_MAPPING.keys():
                    self.frl_to_set = value[0].upper()
                else:
                    gdhm.report_test_bug_di("Provided FRL value is incorrect", gdhm.ProblemClassification.OTHER)
                    self.fail("Aborting the test as incorrect or no FRL value is provided in command line")
            else:
                ##
                # pass as nothing to execute in else condition.
                pass

        if verify_dvi_mode:
            # Hardcoding registry name
            is_enable = registry.read('gfx_0', RegKeys.HDMI_NO_NULL_PACKET_AND_AUDIO)
            # If regkey is present in cmd line and it is not enabled, fail the test
            if is_enable != 1:
                gdhm.report_test_bug_di("Provided Registry Key is not enabled", gdhm.ProblemClassification.OTHER)
                self.fail("Aborting the test as provided registry key is not enabled")

        ##
        # Check if DP++ port is enabled in the VBT
        if 'HDMI' in self.display:
            port_label = self.display.split('_')[-1]
            supported_ports = display_cfg.get_supported_ports().keys()
            if ("DP_{0}".format(port_label) in supported_ports) or (
                    "DP_{0}_++".format(port_label) in supported_ports):
                self.dpDongle = True

        ##
        # Parse XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        self.hdmi_2_1_status = root.find("./HDMI2_1")
        self.max_bitrate = root.find("./HDMI2_1/FRL/max_value")
        self.lanes = root.find("./HDMI2_1/FRL/lanes")
        self.Display = tree.getroot()
        self.edid_file = self.Display.get('EDID')
        self.dpcd_file = self.Display.get('DPCD')
        self.dongle_type = self.Display.get('DONGLE_TYPE')

        logging.debug(
            "Display : %s XML : %s Edid : %s DPCD : %s" % (self.display, xml_file, self.edid_file, self.dpcd_file))

        ##
        # Plug the EDID and DPCD extracted from the XML file
        if self.edp is False:
            if (self.dpcd_file == "NONE") and ("HDMI" in self.display) and (self.dongle_type == "Type1Adapter"):
                display_utility.plug(self.display, self.edid_file, None, False, 'NATIVE', None, False, 'gfx_0', None,
                                     int(DONGLE_TYPE.Type1Adapter))
            elif (self.dpcd_file == "NONE") and ("HDMI" in self.display) and (self.dongle_type == "Type2Adapter"):
                display_utility.plug(self.display, self.edid_file, None, False, 'NATIVE', None, False, 'gfx_0', None,
                                     int(DONGLE_TYPE.Type2Adapter))
            elif ((self.dpcd_file == "NONE") and ("HDMI" in self.display) and (
                    self.dongle_type == "Type2Adapter_PS8469")):
                display_utility.plug(self.display, self.edid_file, None, False, 'NATIVE', None, False, 'gfx_0', None,
                                     int(DONGLE_TYPE.Type2Adapter_PS8469))
            elif self.dpcd_file == "NONE":
                display_utility.plug(self.display, self.edid_file)
            else:
                display_utility.plug(self.display, self.edid_file, self.dpcd_file)
        else:
            logging.debug("Skipping Plug call as display is eDP")

        enumerated_displays = self.display_config.get_enumerated_display_info()

        # IF HDMI Display check for HDMI 2.1
        # IF FRL is enabled in EDID then report it as HDMI 2.1
        # Get FRL rate and DSC support details
        if 'HDMI' in self.display:
            hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
            hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block('gfx_0', self.display)
            self.hdmi_2_1_status = hf_vsdb_parser.is_frl_enable
            logging.info("HDMI 2_1 Status %s" % self.hdmi_2_1_status)
            dsc_status = hf_vsdb_parser.is_dsc_supported
            if dsc_status is True:
                # If DSC is enabled, the Driver train the Link rate to the lowest of FRL mode Link rate and the DSC mode
                # FRL Link rate
                self.max_frl_rate = min(hf_vsdb_parser.dsc_max_frl_rate[0], hf_vsdb_parser.max_frl_rate[0])
                if self.max_frl_rate == hf_vsdb_parser.dsc_max_frl_rate[0]:
                    self.lanes = hf_vsdb_parser.dsc_max_frl_rate[1]
                else:
                    self.lanes = hf_vsdb_parser.max_frl_rate[1]
            else:
                self.max_frl_rate, self.lanes = hf_vsdb_parser.max_frl_rate

        # Limit HDMI2.1 FRL from VBT
        if self.frl_to_set is not None:

            if 'HDMI' in self.display and not self.hdmi_2_1_status:
                gdhm.report_test_bug_di("FRL is not supported in non HDMI2.1 displays")
                self.fail("FRL is not supported in non HDMI2.1 displays")
            else:
                status = self.set_hdmi_2_1_frl_rate_in_vbt(self.display, self.frl_to_set)
                self.assertTrue(status, "Set FRL rate in VBT Failed")
                logging.info("Set FRL rate in VBT successful")

        ##
        # Get Target-ID, display_and_adapter_info for connected port
        for display_index in range(enumerated_displays.Count):
            port = (CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name
            if port == self.display:
                self.targetId = enumerated_displays.ConnectedDisplays[display_index].TargetID
                self.display_and_adapter_info = enumerated_displays.ConnectedDisplays[
                    display_index].DisplayAndAdapterInfo
        logging.info("INFO : Target-id for %s - %s" % (self.display, self.targetId))
        if self.targetId is None:
            logging.error("FAIL : No target-id found for %s. Check if display is connected" % self.display)
            self.fail()

        ##
        # Apply SD configuration for self.display
        if self.display_config.set_display_configuration_ex(enum.SINGLE, [self.display], enumerated_displays) is False:
            self.fail()

        # Set Default BPC and Default Encoding using escape call in setup.
        if "HDMI" in self.display:
            status = color_escapes.set_bpc_encoding(self.display_and_adapter_info, self.default_bpc, self.default_encoding,
                                                    self.platform_type, False, feature="ModeEnum")
            if not status:
                gdhm.report_test_bug_os("Set BPC and Encoding using escape call Failure")
                self.fail("Set BPC and Encoding using escape call Failure")
            else:
                logging.info("Set BPC and Encoding using escape call successful")

        ##
        # Parse the XML file for EDID data
        self.parse_edid_xml(xml_file)

    ##
    # @brief        Fill golden_mode_list,ignore_mode_list,apply_mode_list
    # @param[in]    edid_xml: str
    #                    edid_xml passed as input
    # @return       None
    def parse_edid_xml(self, edid_xml):
        sup_platform = []
        ##
        # Fill the IgnoreModeIndex, ApplyModeIndex for current platform
        IgnoreModeIndex = ""
        ApplyModeIndex = ""
        platform_handle = self.Display.findall('Platform')
        ModeControlFlag = {}
        for platform in platform_handle:
            sup_platform.append(platform.get('Name'))
            if self.Platform == platform.get('Name'):
                IgnoreModeIndex = platform.find('IgnoreModeIndex').text.split(",")
                ApplyModeIndex = platform.find('ApplyModeIndex').text.split(",")
                mode_flag = platform.find('ModeControlFlag')
                custom_mode_values = []
                if mode_flag.text != 'None':
                    custom_mode_values = mode_flag.text.split(";")
                ModeControlFlag['CommonValue'] = int(mode_flag.get('CommonValue'), 16)
                for flag_value in custom_mode_values:
                    split_data = flag_value.split('=')
                    index = split_data[0].split(',')
                    # Append the multiple supported color format to the list for each modeIndex.This avoids over-writing
                    # of the supported color formats
                    for i in index:
                        if i not in ModeControlFlag.keys():
                            ModeControlFlag[i] = [int(split_data[1], 16)]
                        else:
                            ModeControlFlag[i].append(int(split_data[1], 16))

        if self.Platform not in sup_platform:
            logging.error("ERROR : XML file : %s specified is not valid for the %s platform" % (edid_xml,
                                                                                                self.Platform))
            self.fail()

        ##
        # Using driver escape to get EDID capabilities.
        edid_flag, edid_data, _ = driver_escape.get_edid_data(self.targetId)
        if not edid_flag:
            logging.error(f"Failed to get EDID data for target_id : {self.targetId}")
            assert edid_flag, "Failed to get EDID data"
        assert edid_data

        ##
        # Fill the Mode index table from GoldenModeTable
        golden_mode_handle = self.Display.findall('GoldenModeTable')
        for GoldenModeTable in golden_mode_handle:
            edid_instance_handle = GoldenModeTable.findall('EDIDInstance')
            for EDIDInstance in edid_instance_handle:
                modeIndex = EDIDInstance.get('ModeIndex')
                modeInfo = DisplayModeBlock()
                mode = DisplayMode()
                mode.targetId = self.targetId
                mode.HzRes = int(EDIDInstance.get('HActive'))
                mode.VtRes = int(EDIDInstance.get('VActive'))
                mode.refreshRate = int(EDIDInstance.get('RefreshRate'))
                mode.BPP = 4  # Assuming RGBA8888
                mode.rotation = 1
                mode.scanlineOrdering = self.SCANLINE_DICT[EDIDInstance.get('Scanline')]
                mode.scaling = self.SCALE_DICT[EDIDInstance.get('Scaling')]
                modeControlFlag = DisplayModeControlFlags()
                if modeIndex in ModeControlFlag.keys():
                    modeControlFlagList = ModeControlFlag[modeIndex]
                    for modeFlag in modeControlFlagList:
                        modeControlFlag.as_int = modeFlag
                        mode.samplingMode = ModeEnumHelper.update_sampling_mode(modeControlFlag.data, mode.samplingMode)
                else:
                    modeControlFlag.as_int = ModeControlFlag['CommonValue']
                    mode.samplingMode = ModeEnumHelper.update_sampling_mode(modeControlFlag.data, mode.samplingMode)

                ##
                # ToDO: BPC verification should be done at color format level after the structure SamplingModeBpcMask is
                #  added to _DD_CUI_ESC_CE_DATA in the driver code

                self.bpc_from_xml = bpc_mapping[modeControlFlag.data.bpc]

                # If higher BPC is requested from xml, checking whether same is supported in the EDID plugged or not.
                if self.bpc_from_xml == 10 or self.bpc_from_xml == 12:
                    is_edid_version_1_4_or_greater = False
                    # Setting BPC from EDID is supported only from EDID version 1.4.
                    # Reading 19th byte to confirm the version.
                    is_edid_version_1_4_or_greater = True if edid_data[19] > 3 else False
                    if is_edid_version_1_4_or_greater:
                        bpc_from_edid = 0
                        ##
                        # Read bits 4-6 of 20th byte of EDID to get BPC support in EDID
                        bpc_from_edid = bpc_mapping_of_edid[(edid_data[20] >> 4) & 7]
                        if bpc_from_edid >= self.bpc_from_xml:
                            logging.info("Requested BPC is supported by EDID")
                        else:
                            logging.error("BPC requested from xml is not supported in EDID. BPC requested from xml: %s"
                                          " , BPC supported in EDID: %s ", self.bpc_from_xml, bpc_from_edid)
                            self.fail()

                    self.is_bpc_set_using_registry = DSCHelper.set_bpc_in_registry('gfx_0', self.bpc_from_xml)
                    self.assertTrue(self.is_bpc_set_using_registry, "Setting Source BPC Failed.")

                # Setting color encoding as per color format given in test for HDMI displays,
                # this will be used by phy_test_mode() in DE verification.
                # Not needed for combined wire format test as it is handled during verify_combined_wire_format().
                # Not needed for HDMI 2.1 case
                # HSD-18026517689
                if 'HDMI' in self.display and 'combined_color_formats' not in edid_xml and 'CWF' not in edid_xml and self.hdmi_2_1_status is False:
                    if mode.samplingMode.yuv444 == 1:
                        self.color_mode = 'YCBCR444'
                    elif mode.samplingMode.yuv422 == 1:
                        self.color_mode = 'YCBCR422'
                    elif mode.samplingMode.yuv420 == 1:
                        self.color_mode = 'YCBCR420'
                    else:
                        self.color_mode = 'RGB'
                    if self.Platform not in common.PRE_GEN_13_PLATFORMS:
                        status = color_escapes.set_bpc_encoding(self.display_and_adapter_info,
                                                                'BPC' + str(self.bpc_from_xml),
                                                                self.color_mode,
                                                                self.platform_type,
                                                                False, feature="ModeEnum")
                    else:
                        status = True
                        if self.color_mode == "YCBCR444":
                            status = color_escapes.configure_ycbcr(self.display, self.display_and_adapter_info,
                                                                   True)

                    if not status:
                        gdhm.report_test_bug_di(
                            title=f'[Interfaces][MODE_ENUMERATION] Failed to enable {self.color_mode}'
                        )

                        self.fail("FAIL : Failed to enable {}".format(self.color_mode))
                    else:
                        logging.info("Successfully enabled {}".format(self.color_mode))

                # DP case
                elif 'DP' in self.display:
                    if mode.samplingMode.yuv422 == 1:
                        # Adding regkey to force YUV422 mode in driver
                        r_status = registry_access.write(args=self.ss_reg_args, reg_name="ForceApplyYUV422Mode",
                                                         reg_type=registry_access.RegDataType.DWORD, reg_value=1)
                        self.assertEquals(r_status, True, "Aborting the test as YUV422 Enabling is failing")

                        ##
                        # Restarting display driver
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            gdhm.report_test_bug_di(
                                title=f'[Interfaces][MODE_ENUMERATION] Failed to restart driver after setting `ForceApplyYUV422Mode` registry'
                            )
                            self.fail("Failed to restart display driver")


                mode.pixelClock_Hz = int(EDIDInstance.get('PixelCLK'))
                modeInfo.DisplayMode = mode
                modeInfo.PixelClk = int(EDIDInstance.get('PixelCLK'))
                # Checking for DP++ dongle and resetting BPC to 8 if symbol clock exceeds allowed range (300MHz)
                if ('HDMI' in self.display) and self.dpDongle and modeControlFlag.data.bpc > 1:
                    bpc_multiplier = float(bpc_mapping[modeControlFlag.data.bpc]) / float(8)
                    if (modeInfo.PixelClk * bpc_multiplier) > 300000000:
                        logging.debug(
                            "ModeIndex: {0} Pixel Clock exceeds 300MHz. Setting 8 BPC as expected".format(modeIndex))
                        modeControlFlag.data.bpc = 1  # 8 BPC
                modeInfo.DisplayModeControlFlag = modeControlFlag
                self.golden_mode_list[modeIndex] = modeInfo

        ##
        # Fill the self.ignore_mode_list
        for ignore, value in self.golden_mode_list.items():
            for index in range(0, len(IgnoreModeIndex)):
                if ((IgnoreModeIndex[index].strip() == ignore) or value.DisplayModeControlFlag.data.pixel_rep_mode or
                        (self.dpDongle and value.PixelClk > 300000000)
                        or (value.PixelClk > 165000000 and self.dongle_type == "Type1Adapter")
                        or (value.PixelClk > 300000000 and self.dongle_type == "Type2Adapter")
                        or (value.PixelClk > 300000000 and self.dongle_type == "Type2Adapter_PS8469")
                        and ("HDMI" in self.display)):
                    self.ignore_mode_list[ignore] = value

        ##
        # Update self.golden_mode_list to ignore self.ignore_mode_list entries
        for ignore, value in self.ignore_mode_list.items():
            del self.golden_mode_list[ignore]

        ##
        # Fill the self.apply_mode_list
        for apply, value in self.golden_mode_list.items():
            for index in range(0, len(ApplyModeIndex)):
                if ApplyModeIndex[index] == "*":
                    self.apply_mode_list = self.golden_mode_list
                    break
                elif ApplyModeIndex[index] == apply:
                    self.apply_mode_list[apply] = value
                else:
                    logging.debug("SKIP APPLY MODE FOR MODEINDEX : %s" % apply)

    ##
    # @brief        Update the SamplingMode string based on modes enabled in samplingMode structure
    # @param[in]    sampling_mode: SamplingMode() object
    #                    The first four bits of this object represents RGB, YUV420,YUV444, YUV422 formats respectively
    #                    These bits are set based on the color format bits obtained from mode_control_flag_data
    # @return       sampling_mode_str
    #                    returns the constructed sampling mode string
    @staticmethod
    def prepare_sampling_mode_string(sampling_mode):
        sampling_mode_str = ""
        if sampling_mode.rgb == 1:
            sampling_mode_str += 'RGB '
        if sampling_mode.yuv420 == 1:
            sampling_mode_str += 'YUV420 '
        if sampling_mode.yuv444 == 1:
            sampling_mode_str += 'YUV444 '
        if sampling_mode.yuv422 == 1:
            sampling_mode_str += 'YUV422 '

        return sampling_mode_str

    ##
    # @brief        This function fetches the colo_space of the current pipe
    # @param[in]    pipe: str
    #                   current pipe
    # @param[in]    platform : str
    #                   name of the platform
    # @param[in]    gfx_index : str
    #                   adapter index ex: gfx_0, gfx_1
    # @return       pipe_color_space : str
    #                    Returns the color space of the current pipe ex: RGB, YUV
    @staticmethod
    def get_pipe_color_output_space(pipe, platform, gfx_index):
        pipe_color_space_dict = {0: "RGB", 1: "YUV"}
        reg = MMIORegister.read("PIPE_MISC_REGISTER", "PIPE_MISC_%s" % pipe, platform, gfx_index=gfx_index)
        pipe_color_space = pipe_color_space_dict[reg.pipe_output_color_space_select]
        return pipe_color_space

    ##
    # @brief        print the DisplayMode() object
    # @param[in]    value: DisplayMode() objest
    #                    DisplayMode object to be printed
    # @param[in]    str: str
    #                    Status of DisplayMode. Values = Fail/Pass
    # @return       None
    def print_mode(self, value, str):
        scanline = "Progressive" if (value.scanlineOrdering == 1) else "Interlaced"
        scaling = self.RSCALE_DICT[value.scaling]
        rotation = self.RROTATION_DICT[value.rotation]
        sampling_mode_str = self.prepare_sampling_mode_string(value.samplingMode)

        logging.info(
            str + " : Mode - HActive : %s; VActive : %s; RefreshRate : %s; Rotation : %s; bpp : %s; Scaling : %s; "
                  "SamplingMode : %s; Scanline : %s; PixelClock : %s", value.HzRes, value.VtRes, value.refreshRate,
            rotation, 8 * value.BPP, scaling, sampling_mode_str, scanline, value.pixelClock_Hz)

    ##
    # @brief        This function fetches all the OS supported modes and stores in self.os_mode_list and prints them
    # @return       None
    def get_os_supported_modes(self):
        supported_mode_list = self.display_config.get_all_supported_modes([self.targetId], False)
        for key, values in supported_mode_list.items():
            for index in range(0, len(values)):
                mode = DisplayMode()
                mode.targetId = values[index].targetId
                mode.HzRes = values[index].HzRes
                mode.VtRes = values[index].VtRes
                mode.rotation = values[index].rotation
                mode.BPP = values[index].BPP
                mode.refreshRate = values[index].refreshRate
                mode.scanlineOrdering = values[index].scanlineOrdering
                mode.samplingMode = values[index].samplingMode
                mode.scaling = values[index].scaling
                self.os_mode_list.append(mode)

        for index in range(0, len(self.os_mode_list)):
            sampling_mode = self.prepare_sampling_mode_string(self.os_mode_list[index].samplingMode)
            scanline_ordering = "Progressive" if (self.os_mode_list[index].scanlineOrdering == 1) else "Interlaced"
            logging.debug("OS Supported Mode - HActive : %s; VActive : %s; RefreshRate : %s; Rotation : %s; BPP : %s; "
                          "Scaling : %s; samplingMode : %s; Scanline : %s", self.os_mode_list[index].HzRes,
                          self.os_mode_list[index].VtRes, self.os_mode_list[index].refreshRate,
                          self.RROTATION_DICT[self.os_mode_list[index].rotation], 8 * self.os_mode_list[index].BPP,
                          self.RSCALE_DICT[self.os_mode_list[index].scaling], sampling_mode, scanline_ordering)

    ##
    # @brief        This function verifies modes enumerated across golden_mode_list, ignore_mode_list with os_mode_list
    #               and updates unsupported_mode_list, unsupported_ignoremode_list
    # @return       verification_status : Boolean
    #                   Returns False if either supported modes are not enumerated by the driver or if modes to be
    #                   ignored are enumerated by the driver and returns True otherwise
    def verify_golden_and_ignore_modes_with_combined_wireformat(self):
        verification_status = True

        # Verify if golden mode is present in OS supported mode list or not
        for index, golden_mode in self.golden_mode_list.items():
            match = False
            for os_mode in self.os_mode_list:
                if os_mode == golden_mode.DisplayMode and \
                        os_mode.samplingMode.Value == golden_mode.DisplayMode.samplingMode.Value:
                    match = True
                    break
            if match is False:
                self.unsupported_mode_list.append(golden_mode)

        # Verify if the modes to be ignored are enumerated
        for index, ignore_mode in self.ignore_mode_list.items():
            for os_mode in self.os_mode_list:
                if os_mode == ignore_mode.DisplayMode and \
                        os_mode.samplingMode.Value == ignore_mode.DisplayMode.samplingMode.Value:
                    self.unsupported_ignoremode_list.append(ignore_mode)

        # Fail the test if driver fails to enumerate golden modes
        if len(self.unsupported_mode_list) != 0:
            gdhm.report_bug(
                title="[Interfaces][ModeEnum] Driver failed to enumerate the modes for platform: {}".format(
                    self.Platform),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : Below Modes are not enumerated by the driver for %s Platform" % self.Platform)
            for index in range(0, len(self.unsupported_mode_list)):
                self.print_mode(self.unsupported_mode_list[index].DisplayMode, "FAIL")
            verification_status = False

        # Fail the test if driver fails to ignore the enumeration of unsupported modes
        if len(self.unsupported_ignoremode_list) != 0:
            gdhm.report_bug(
                title="[Interfaces][ModeEnum] Driver failed to ignore enumeration of unsupported modes for platform:"
                      " {}".format(self.Platform),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "ERROR : Below Modes should not be enumerated by the driver for %s Platform" % self.Platform)
            for index in range(0, len(self.unsupported_ignoremode_list)):
                self.print_mode(self.unsupported_ignoremode_list[index].DisplayMode, "FAIL")
            verification_status = False

        # Verify if there are duplicate golden modes are present in OS supported mode list and check if there is
        # violation of combined mode enumeration
        for index, golden_mode in self.golden_mode_list.items():
            for os_mode in self.os_mode_list:
                if os_mode == golden_mode.DisplayMode:
                    os_mode_sampling = self.prepare_sampling_mode_string(os_mode.samplingMode)
                    golden_mode_sampling = self.prepare_sampling_mode_string(golden_mode.DisplayMode.samplingMode)
                    if os_mode_sampling == golden_mode_sampling:
                        # TODO: Duplicate entries of golden mode with same sampling mode may exist because of different
                        #  mode type like media_rr mode and edid_mode. Currently this is expected. Jira to handle this
                        #  after driver and DLL updates the logic: https://jira.devtools.intel.com/browse/VSDI-32110
                        logging.info(f"PASS: Combined wire format mode enumeration successful for Mode "
                                      f"{golden_mode.DisplayMode.HzRes}x{golden_mode.DisplayMode.VtRes} @ "
                                      f"{golden_mode.DisplayMode.refreshRate} Expected: {golden_mode_sampling} "
                                     f"Actual: {os_mode_sampling}")
                    else:
                        gdhm.report_bug(
                            title="[Interfaces][ModeEnum] Driver failed to enumerate combined wire format",
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Test.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P1,
                            exposure=gdhm.Exposure.E2
                        )
                        logging.error(f"FAIL: Combined wire format mode enumeration failed. Mode "
                                      f"{golden_mode.DisplayMode.HzRes}x{golden_mode.DisplayMode.VtRes} @ "
                                      f"{golden_mode.DisplayMode.refreshRate} is enumerated with different "
                                      f"sampling value Expected: {golden_mode_sampling} Actual: {os_mode_sampling}")
                        verification_status = False

        return verification_status

    ##
    # @brief        Verifies combined color format and enumerates the modes using golden_mode_list. It checks if the
    #               initial modeset comes up with RGB mode if it one of color formats supported by the mode. And then
    #               applies each mode with all the supported color formats one-by-one and performs DE verification.
    #               Failure of any modeset or DE verification fails the test
    # @return       None
    def verify_mode_enum_modeset_with_combined_wireformat(self):
        fail_flag = False
        clock_helper = clk_helper.ClockHelper()

        for index, ignore_mode in self.ignore_mode_list.items():
            self.print_mode(ignore_mode.DisplayMode, "IGNORE")

        for index, golden_mode in self.golden_mode_list.items():
            self.print_mode(golden_mode.DisplayMode, "PASS")

        for index, apply_mode in self.apply_mode_list.items():
            logging.info("************** ModeIndex %s : MODESET AND VERIFICATION**************" % index)
            self.print_mode(apply_mode.DisplayMode, "APPLY")

            status = self.display_config.set_display_mode([apply_mode.DisplayMode])

            if status is False:
                logging.error("ERROR : Failed to apply display mode. Exiting ...")
                fail_flag = True
            else:
                current_mode = self.display_config.get_current_mode(apply_mode.DisplayMode.targetId)
                if apply_mode.DisplayMode == current_mode:
                    logging.info("Current mode is same as Requested mode")
                else:
                    enumerated_displays = self.display_config.get_enumerated_display_info()
                    current_mode_str = current_mode.to_string(enumerated_displays)
                    applied_mode_str = apply_mode.DisplayMode.to_string(enumerated_displays)
                    gdhm.report_bug(
                        title=f"[Interfaces][ModeEnum] Targeted mode is not matching with the current mode.Current mode"
                              f" is:{current_mode_str} Targeted mode is: {applied_mode_str}",
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P1,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail(f"Targeted mode is not matching with the current mode. Current mode is:{current_mode_str}"
                              f" Targeted mode is: {applied_mode_str}")

                bpc = bpc_mapping[apply_mode.DisplayModeControlFlag.data.bpc]
                sampling_mode_list = self.prepare_sampling_mode_string(
                    apply_mode.DisplayMode.samplingMode).strip().split(' ')
                current_pipe = get_current_pipe(self.display)

                # for each mode check if default pipe color space is RGB and is present in the supported color format
                if "RGB" in sampling_mode_list:
                    color_space = self.get_pipe_color_output_space(current_pipe, self.Platform, 'gfx_0')
                    if color_space != "RGB":
                        gdhm.report_bug(
                            title=f"[Interfaces][ModeEnum] RGB is present in supported color formats of current mode "
                                  f"but was not applied",
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Test.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P1,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("RGB is present in supported color formats of current mode but was not applied")

                logging.info(f"Supported color formats: {sampling_mode_list} BPC: {bpc}")
                for color_format in sampling_mode_list:
                    logging.info(f"Verifying DE for sampling mode: {color_format}")
                    if color_format == "RGB":
                        status = color_escapes.set_bpc_encoding(apply_mode.DisplayMode.displayAndAdapterInfo,
                                                                'BPC' + str(bpc), 'RGB', self.platform_type, False, feature="ModeEnum")
                        if status is False:
                            fail_flag = True
                            logging.error("Escape call status for setting encoding as RGB failed")
                            continue

                    elif color_format == "YUV422":

                        status = color_escapes.set_bpc_encoding(apply_mode.DisplayMode.displayAndAdapterInfo,
                                                                'BPC' + str(bpc), 'YCBCR422', self.platform_type, False, feature="ModeEnum")
                        if status is False:
                            fail_flag = True
                            logging.error("Escape call status for setting encoding as YUV422 failed")
                            continue

                    elif color_format == "YUV444":

                        status = color_escapes.set_bpc_encoding(apply_mode.DisplayMode.displayAndAdapterInfo,
                                                                'BPC' + str(bpc), 'YCBCR444', self.platform_type, False, feature="ModeEnum")
                        if status is False:
                            fail_flag = True
                            logging.error("Escape call status for setting encoding as YUV444 failed")
                            continue

                    elif color_format == "YUV420":

                        status = color_escapes.set_bpc_encoding(apply_mode.DisplayMode.displayAndAdapterInfo,
                                                                'BPC' + str(bpc), 'YCBCR420', self.platform_type, False, feature="ModeEnum")
                        if status is False:
                            fail_flag = True
                            logging.error("Escape call status for setting encoding as YUV420 failed")
                            continue

                    # Test whether clock, plane, pipe, transcoder, DDI are programmed correctly
                    ports = []
                    pipe_list = []
                    transcoder_list = []
                    dip_list = []
                    ports.append(self.display)
                    pipe_list.append(display_pipe.DisplayPipe(self.display, color_format))
                    dip_list.append(display_dip_control.DisplayDIPControl(self.display, bpc))
                    transcoder_list.append(
                        display_transcoder.DisplayTranscoder(self.display, None, None, None, None, None, None, bpc,
                                                             None, color_format))

                    #
                    # Checking whether connected display is HDMI2.1 or not
                    if self.hdmi_2_1_status is True:
                        # If not HDMI2.1 display, breaking the loop and failing the test.
                        if not (clock_helper.is_hdmi_2_1(self.display, 'gfx_0')):
                            gdhm.report_bug(
                                title=f"[Interfaces][ModeEnum] Connected display is not HDMI2.1",
                                problem_classification=gdhm.ProblemClassification.OTHER,
                                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                                priority=gdhm.Priority.P1,
                                exposure=gdhm.Exposure.E2
                            )
                            logging.error("Connected display is not HDMI2.1")
                            fail_flag = True
                            break

                    display = DisplayEngine()
                    status = display.verify_display_engine(ports, None, pipe_list, transcoder_list, None, dip_list)
                    if status is False:
                        # GDHM logging is handled in the API
                        logging.error(f"DE verification failed for {ports} on 'gfx_0'")
                        fail_flag = True

            display_adapter_info = self.display_config.get_display_and_adapter_info_ex(self.display, 'gfx_0')
            # Resetting BPC and color encoding to default value supported by IGCC

            status = color_escapes.set_bpc_encoding(display_adapter_info, self.default_bpc, self.default_encoding,
                                                    self.Platform, False, feature="ModeEnum")
            self.assertTrue(status, "Failed to reset BPC and Encoding to default")

        if fail_flag is True:
            gdhm.report_bug(
                title=f"[Interfaces][ModeEnum] FAIL : display_mode_enumeration",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Escape call status for setting encoding as YUV420 failed")
            self.fail("FAIL : display_mode_enumeration")

    ##
    # @brief        Verify Mode Enumeration using golden_mode_list. If Mode Enumeration is success,
    #               Do Modeset for self.apply_mode_list, test whether clock, plane, pipe, transcoder,
    #               DDI are programmed correctly else fail the test.
    # @return       None
    def verify_mode_enum_and_modeset(self):
        match = False
        test_fail = False
        fail_flag = False
        clock_helper = clk_helper.ClockHelper()

        ##
        # Query the OS supported modes and append it to os_mode_list
        supported_mode_list = self.display_config.get_all_supported_modes([self.targetId], False)
        for key, values in supported_mode_list.items():
            for index in range(0, len(values)):
                mode = DisplayMode()
                mode.targetId = values[index].targetId
                mode.HzRes = values[index].HzRes
                mode.VtRes = values[index].VtRes
                mode.rotation = values[index].rotation
                mode.BPP = values[index].BPP
                mode.refreshRate = values[index].refreshRate
                mode.scanlineOrdering = values[index].scanlineOrdering
                mode.samplingMode = values[index].samplingMode
                mode.scaling = values[index].scaling
                self.os_mode_list.append(mode)

        ##
        # Verify Modes enumerated across golden_mode_list, ignore_mode_list with os_mode_list
        for goldenkey, goldenvalue in self.golden_mode_list.items():
            for supList in self.os_mode_list:
                if supList == goldenvalue.DisplayMode:
                    match = True
                    break
                else:
                    match = False
            if match is False:
                self.unsupported_mode_list.append(goldenvalue)

        for ignorekey, ignorevalue in self.ignore_mode_list.items():
            for ignoreList in self.os_mode_list:
                if ignoreList == ignorevalue.DisplayMode:
                    self.unsupported_ignoremode_list.append(ignorevalue)

        if len(self.unsupported_mode_list) != 0:
            gdhm.report_bug(
                title="[Interfaces][ModeEnum] Driver failed to enumerate the modes for platform: {}".format(
                    self.Platform),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : Below Modes are not enumerated by the driver for %s Platform" % self.Platform)
            for index in range(0, len(self.unsupported_mode_list)):
                self.print_mode(self.unsupported_mode_list[index].DisplayMode, "FAIL")
            self.fail("FAIL : display_mode_enumeration")

        if len(self.unsupported_ignoremode_list) != 0:
            gdhm.report_bug(
                title="[Interfaces][ModeEnum] Driver failed to ignore enumeration of unsupported modes for platform:"
                      " {}".format(self.Platform),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : Below Modes should not be enumerated by the driver for %s Platform" % self.Platform)
            for index in range(0, len(self.unsupported_ignoremode_list)):
                self.print_mode(self.unsupported_ignoremode_list[index].DisplayMode, "FAIL")
            self.fail("FAIL : display_mode_enumeration")

        for index in range(0, len(self.os_mode_list)):
            samplingMode = "RGB" if (self.os_mode_list[index].samplingMode == 1) else "YUV"
            scanlineOrdering = "Progressive" if (self.os_mode_list[index].scanlineOrdering == 1) else "Interlaced"
            logging.debug("OS Supported Mode - HActive : %s; VActive : %s; RefreshRate : %s; Rotation : %s; BPP : %s;"
                          " Scaling : %s; samplingMode : %s; Scanline : %s", self.os_mode_list[index].HzRes,
                          self.os_mode_list[index].VtRes, self.os_mode_list[index].refreshRate,
                          self.RROTATION_DICT[self.os_mode_list[index].rotation],
                          8 * self.os_mode_list[index].BPP, self.RSCALE_DICT[self.os_mode_list[index].scaling],
                          samplingMode, scanlineOrdering)

        for ignorekey, ignorevalue in self.ignore_mode_list.items():
            self.print_mode(ignorevalue.DisplayMode, "IGNORE")

        for goldenkey, goldenvalue in self.golden_mode_list.items():
            self.print_mode(goldenvalue.DisplayMode, "PASS")

        for applykey, applyvalue in self.apply_mode_list.items():
            logging.info("************** ModeIndex %s : MODESET AND VERIFICATION**************" % applykey)
            self.print_mode(applyvalue.DisplayMode, "APPLY")
            status = self.display_config.set_display_mode([applyvalue.DisplayMode])

            if status is False:
                logging.error("ERROR : Failed to apply display mode. Exiting ...")
                fail_flag = True
            else:
                current_mode = self.display_config.get_current_mode(applyvalue.DisplayMode.targetId)
                if applyvalue.DisplayMode == current_mode:
                    logging.info("Current mode is same as Requested mode")
                else:
                    enumerated_displays = self.display_config.get_enumerated_display_info()
                    logging.error("Targeted mode is not matching with the current mode. \nCurrent mode is : {} \n"
                                  "Targeted mode is: {}".format(current_mode.to_string(enumerated_displays),
                                                                applyvalue.DisplayMode.to_string(enumerated_displays)))
                    self.fail()

                bpc = list(bpc_mapping.values())[list(bpc_mapping).index(applyvalue.DisplayModeControlFlag.data.bpc)]

                display_timings = self.display_config.get_display_timings(self.display_and_adapter_info)

                # Get VIC ID of the current mode
                vic_id = ModeEnumHelper.get_vic_data(display_timings)
                send_vic_id = False

                for vic_data, vic_display_timing in VIC_MODE_INFO.items():
                    if vic_display_timing['hactive'] == applyvalue.DisplayMode.HzRes and \
                            vic_display_timing['vactive'] == applyvalue.DisplayMode.VtRes and \
                            vic_display_timing['refresh_rate'] == applyvalue.DisplayMode.refreshRate:
                        send_vic_id = True

                # Test whether clock, plane, pipe, transcoder, DDI are programmed correctly
                ports = []
                pipeList = []
                plane_list = []
                transcoderList = []
                dipList = []
                color_format = COLOR_FORMAT(applyvalue.DisplayModeControlFlag.data.color_format).name

                ports.append(self.display)
                plane_list.append(display_plane.DisplayPlane(self.display))
                pipeList.append(display_pipe.DisplayPipe(self.display, color_format))

                transcoderList.append(
                    display_transcoder.DisplayTranscoder(self.display, None, None, None, None, None, None, bpc, None,
                                                         color_format))

                # To send YUV color format in YCBCR format
                if "YUV" in color_format:
                    color_format = color_format.replace("YUV", "YCBCR")

                # For now,sending vic_id only if we are able to get vic for current mode
                # from existing VIC ID Table in mode_vic_info.py.
                # TODO: Add all VIC modes in mode_vic_info.py and remove below logic
                if send_vic_id:
                    dipList.append(display_dip_control.DisplayDIPControl(self.display, bpc, color_format=color_format, vic_id=vic_id))
                else:
                    dipList.append(display_dip_control.DisplayDIPControl(self.display, bpc, color_format=color_format))

                ##
                # Checking whether connected display is HDMI2.1 or not
                if self.hdmi_2_1_status is True:
                    ##
                    # If not HDMI2.1 display, breaking the loop and failing the test.
                    if not (clock_helper.is_hdmi_2_1(self.display, 'gfx_0')):
                        logging.error("Connected display is not HDMI2.1")
                        fail_flag = True
                        break

                # Pipe Joiner Verification
                is_pipe_joiner_required, no_of_pipe_req = DisplayClock.is_pipe_joiner_required('gfx_0',
                                                                                               self.display)
                if is_pipe_joiner_required:
                    logging.info("Pipe Joiner is enabled for applied mode")

                    # Create pipe list accordingly to pass it to DE Verification
                    for i in range(1, no_of_pipe_req):
                        # Append Pipe Obj
                        pipe_obj = display_pipe.DisplayPipe(self.display, COLOR_FORMAT(applyvalue.DisplayModeControlFlag.data.color_format).name)
                        adj_pipe = chr(ord(pipe_obj.pipe[-1]) + i)
                        pipe_obj.pipe = "PIPE_" + adj_pipe
                        pipe_obj.pipe_suffix = adj_pipe
                        pipeList.append(pipe_obj)

                        plane_obj = display_plane.DisplayPlane(self.display)
                        plane_obj.pipe = pipe_obj.pipe
                        plane_obj.pipe_suffix = adj_pipe
                        plane_list.append(plane_obj)

                if self.Platform in ['MTL', 'ELG', 'LNL', 'PTL', 'NVL'] and current_mode.scaling == enum.MDS:
                    logging.info(f"Verifying Voltage Level notified to PCode for {self.Platform}")
                    if DisplayClock.verify_voltage_level_notified_to_pcode('gfx_0', ports) is False:
                        logging.error(f"FAIL: DVFS VoltageLevel verification failed for {ports} on gfx_0")
                        gdhm.report_driver_bug_pc("[Interfaces][Display_Engine][CD Clock] Failed to verify "
                                                  "Voltage level during MDS modeset",
                                                  gdhm.ProblemClassification.FUNCTIONALITY)
                    else:
                        logging.info("PASS: DVFS VoltageLevel verification successful")
                else:
                    if current_mode.scaling != enum.MDS:
                        title = "for scaled modes"
                        gdhm.report_test_bug_os(f"Skipping DVFS VoltageLevel verification {title}",
                                                priority=gdhm.Priority.P4, exposure=gdhm.Exposure.E3)
                        logging.warning(f"Skipping DVFS VoltageLevel verification due to scaled mode {current_mode}."
                                        f" Reason: Potential Virtual modeset. Scaling applied for current mode :"
                                        f" {current_mode.scaling}")
                    logging.warning(f"Skipping DVFS VoltageLevel verification for platform: {self.Platform}")

                # DE Verification
                display = DisplayEngine()
                test_fail = display.verify_display_engine(ports, plane_list, pipeList, transcoderList, None, dipList)
                if test_fail is False:
                    fail_flag = True

        hdmi_2_1_pcon = self.is_hdmi_2_1_pcon_present(self.display_and_adapter_info, self.display)

        if hdmi_2_1_pcon:
            status = self.verify_max_supported_bpc_by_pcon(self.display_and_adapter_info)
            if status:
                logging.info(f'BPC of all enumerated modes is less than or equal to Max supported BPC by PCON')
            else:
                gdhm.report_bug(
                    title="[Interfaces][MODE_ENUMERATION] PCON Max Supported BPC Verification Failure",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P1,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("FAIL : PCON Max Supported BPC Verification Failure")

            status = self.verify_hdmi_edid_processing_by_pcon(self.display_and_adapter_info)
            if status:
                logging.info("HDMI EDID processing by PCON is disabled")
            else:
                gdhm.report_driver_bug_di("HDMI EDID processing by PCON is not disabled")
                self.fail("HDMI EDID processing by PCON is not disabled")

        if fail_flag is True:
            self.fail("FAIL : display_mode_enumeration")

    ##
    # @brief        Verify if BPC of enumerated modes is less than or equal to maximum supported BPC by PCON
    # @param        display_and_adapter_info
    # @return       True if verification is successful. False, otherwise
    @staticmethod
    def verify_max_supported_bpc_by_pcon(display_and_adapter_info):
        status = True
        is_max_pcon_bpc_present = False

        dpcd_read_flag, dpcd_val = driver_escape.read_dpcd(display_and_adapter_info,
                                                           PconDpcdOffsets.ADDITIONAL_HDMI_LINK_CAPABILITY)

        if dpcd_read_flag is False:
            logging.error(f'DPCD: {PconDpcdOffsets.ADDITIONAL_HDMI_LINK_CAPABILITY} read failed')
            return False

        # Bits[1:0] gives Max BPC supported by PCON
        extracted_dpcd = DSCHelper.extract_bits(dpcd_val[0], 2, 0)
        max_pcon_bpc = bpc_mapping_of_pcon[extracted_dpcd]

        # As per spec, Minimum supported BPC for HDMI 2.1 capable PCON should be 10
        if max_pcon_bpc < 10:
            logging.error("Overriding to 10BPC as per PCON spec requirement. Need to correct Test DPCD")
            max_pcon_bpc = 10
        logging.info(f'Maximum BPC Supported by PCON: {max_pcon_bpc}')

        # Stop ETL Tracer
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("Failed to stop ETL Trace")
            return False

        # Renaming ETL file
        etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
        if os.path.exists(etl_file_path):
            file_name = 'GfxTrace_PCON' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
        else:
            logging.error("[Test Issue]: Default etl file does not exist")
            return False

        # Start ETL Tracer
        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to start ETL Tracer")
            return False

        # Generate report with etl_file using etl_parser
        if etl_parser.generate_report(etl_file_path) is False:
            logging.error("Failed to generate EtlParser report")
            return False

        # Get Target_Mode event data
        target_mode_output = etl_parser.get_event_data(etl_parser.Events.TARGET_MODE)

        if target_mode_output is None:
            logging.error("[Driver Issue] - No TargetMode event found in ETL")
            return False

        # Iterating through each mode
        for mode in target_mode_output:
            # Supported BPC for each mode is returned in string format. For ex: "_8_BPC, _10_BPC"
            supported_bpc_string = mode.BpcSupported
            # Extract only bpc values for each mode from above string and store it in a list
            supported_bpc_list = [int(i) for i in supported_bpc_string.split('_') if i.isdigit()]
            logging.debug(f'Supported BPC List for current mode {mode} is {supported_bpc_list}')

            # Iterate supported_bpc_list and check if all BPC for the mode are less than or equal to max_pcon_bpc
            for bpc in supported_bpc_list:
                if bpc > max_pcon_bpc:
                    logging.error(
                        f"BPC: {bpc} of Mode: {mode} is greater than Max BPC Supported by PCON: {max_pcon_bpc}")
                    status = False

            # Check if max_pcon_bpc is listed in atleast one of the modes
            if max_pcon_bpc in supported_bpc_list:
                is_max_pcon_bpc_present = True

        # If no mode is enumerated with max bpc supported by pcon, return False
        if not is_max_pcon_bpc_present:
            logging.error(f"No mode is enumerated with max BPC supported by PCON: {max_pcon_bpc}")
            status = False

        return status

    ##
    # @brief        Method to check if HDMI 2.1 PCON is present
    # @param        display_and_adapter_info
    # @param        display_port
    # @return       True if PCON is present. False otherwise
    @staticmethod
    def is_hdmi_2_1_pcon_present(display_and_adapter_info, display_port):
        hdmi_down_stream_port = 0xB
        dpcd_bit_mask = 0xF

        if 'DP' in display_port:
            dpcd_read_flag, dpcd_val = driver_escape.read_dpcd(display_and_adapter_info,
                                                               PconDpcdOffsets.DOWN_STREAM_PORT_PRESENT)

            if dpcd_read_flag is False:
                logging.error(f'DPCD: {PconDpcdOffsets.DOWN_STREAM_PORT_PRESENT} read failed')
                return False

            # Bit 4 of DPCD: 0x5 is DETAILED_CAP_INFO_AVAILABLE
            detailed_cap_info_available = DSCHelper.extract_bits(dpcd_val[0], 1, 4)

            # Read DPCD: 0x80 only if DETAILED_CAP_INFO_AVAILABLE is 1
            if detailed_cap_info_available:
                # Read DPCD: 0x305A (FRL_LINK_CONFIGURATION_1)
                dpcd_read_flag, dpcd_val = driver_escape.read_dpcd(display_and_adapter_info,
                                                                   PconDpcdOffsets.FRL_LINK_CONFIGURATION_1)
                if dpcd_read_flag is False:
                    logging.error(f'DPCD: {PconDpcdOffsets.FRL_LINK_CONFIGURATION_1} read failed')
                    return False

                # Bit 3 of DPCD: 0x305A is SOURCE_CONTROLLED_MODE_ENABLE, 1 represents enabled and 0 represents disabled
                is_source_control_mode_enable = bool(DSCHelper.extract_bits(dpcd_val[0], 1, 3))

                dpcd_read_flag, dpcd_val = driver_escape.read_dpcd(display_and_adapter_info, PconDpcdOffsets.DFPX_CAP)
                if dpcd_read_flag is False:
                    logging.error(f'DPCD: {PconDpcdOffsets.DFPX_CAP} read failed')
                    return False

                # 0Bh means the downstream-facing port is HDMI
                if ((dpcd_val[0] & dpcd_bit_mask) == hdmi_down_stream_port) & is_source_control_mode_enable:
                    logging.info("HDMI 2.1 PCON is Present")
                    return True
        return False

    ##
    # @brief         Method to check if HDMI EDID processing by PCON is disabled or not
    # @param         display_and_adapter_info
    # @return        status - True if hdmi_edid_processing is disabled, else False
    @staticmethod
    def verify_hdmi_edid_processing_by_pcon(display_and_adapter_info):
        dpcd_read_flag, dpcd_val = driver_escape.read_dpcd(display_and_adapter_info,
                                                           PconDpcdOffsets.PROTOCOL_CONVERTER_CONTROL_1)

        if dpcd_read_flag is False:
            logging.error(f'DPCD: {PconDpcdOffsets.PROTOCOL_CONVERTER_CONTROL_1} read failed')
            return False

        # Verify Bit 1: HDMI_EDID_PROCESSING_DISABLE [0 = HDMI Processing Enabled, 1 = HDMI Processing Disabled]
        if dpcd_val[0] & 0x2 == 0x2:
            return True

        return False

    ##
    # @brief         Method to set HDMI2.1 FRL rate in VBT
    # @param         display_port - Port Name
    # @param         frl_to_set - FRL given in the command line
    # @return        status - True if VBT change is successful, else False
    def set_hdmi_2_1_frl_rate_in_vbt(self, display_port, frl_to_set):
        gfx_vbt = Vbt()
        index = gfx_vbt.get_panel_index_for_port(display_port)
        display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index]

        max_frl_rate_mapping = vbt_context.MAX_FRL_RATE_MAPPING
        current_frl = self.get_hdmi_2_1_frl_rate_in_vbt(display_port)
        logging.info(f"Current FRL Rate in VBT: FRL_{current_frl}")
        logging.info(f"User defined FRL Rate to be set in VBT: {frl_to_set}")

        # Set HDMI2.1 FRL to Valid and set FRL which is passed in command line
        display_entry.IsMaxFrlRateFieldValid = 1
        display_entry.MaximumFrlRate = max_frl_rate_mapping[frl_to_set]

        # Apply VBT Changes
        gfx_vbt.apply_changes()

        # Restart Display driver for changes to take effect
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error("Failed to Restart Display driver")
            return False

        current_frl = self.get_hdmi_2_1_frl_rate_in_vbt(display_port)
        logging.info(f"FRL Rate in VBT after driver restart: FRL_{current_frl}")

        return True

    ##
    # @brief         Method to get current HDMI2.1 FRL rate in VBT
    # @param         display_port - Port Name
    # @return        current_frl - FRL Rate set in VBT
    @staticmethod
    def get_hdmi_2_1_frl_rate_in_vbt(display_port):
        gfx_vbt = Vbt()
        index = gfx_vbt.get_panel_index_for_port(display_port)
        display_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index]

        current_frl = frl_rate_mapping[display_entry.MaximumFrlRate]
        logging.debug(f"Current FRL Rate in VBT: {current_frl}Gbps")

        return current_frl

    ##
    # @brief        Unit-test teardown function to reset the registry settings if done and
    #               unplugging the display plugged in setup phase.
    # @return       None
    def tearDown(self):
        ##
        # Resetting ForceApplyYUV422Mode value in case of YUV422 mode
        status = True
        value, reg_type = registry_access.read(args=self.ss_reg_args, reg_name="ForceApplyYUV422Mode")
        if value == 1:
            if registry_access.write(args=self.ss_reg_args, reg_name="ForceApplyYUV422Mode",
                                     reg_type=registry_access.RegDataType.DWORD, reg_value=0) is False:
                self.fail()
            ##
            # Restarting display driver
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("\tFailed to restart display driver")

        # Reset Default BPC and Default Encoding using escape call in setup.
        if "HDMI" in self.display:
            status = color_escapes.set_bpc_encoding(self.display_and_adapter_info, self.default_bpc, self.default_encoding,
                                                    self.platform_type, False, feature="ModeEnum")
            if not status:
                gdhm.report_test_bug_os("Reset BPC and Encoding using escape call Failure")
                self.fail("Reset BPC and Encoding using escape call Failure")
            else:
                logging.info("Reset BPC and Encoding using escape call successful")

        # Reset BPC to default value in SelectBPCFromRegistry
        if self.is_bpc_set_using_registry:
            is_success = DSCHelper.set_bpc_in_registry('gfx_0', self.default_bpc_in_registry)
            self.assertTrue(is_success, "Resetting Source BPC Failed.")

        # Disable SelectBPC registry
        value, reg_type = registry_access.read(args=self.ss_reg_args, reg_name="SelectBPC")
        if value == 1:
            is_success = DSCHelper.enable_disable_bpc_registry('gfx_0', enable_bpc=0)
            self.assertTrue(is_success, "Disabling BPC in registry failed.")

        # Reset VBT to Max FRL Rate
        if self.hdmi_2_1_status and self.frl_to_set is not None:
            # Reset HDMI2.1 FRL to max 12Gbps
            status = self.set_hdmi_2_1_frl_rate_in_vbt(self.display, "FRL_12")
            self.assertTrue(status, "Reset FRL rate in VBT Failed")
            logging.info("Reset FRL rate in VBT successful")

        for display in [self.display]:
            if self.edp is False:
                display_utility.unplug(display)
        logging.info("**************MODE ENUMERATION TEST END**************")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
