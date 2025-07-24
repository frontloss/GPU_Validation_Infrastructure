#######################################################################################################################
# @file         mode_enum_xml_parser.py
# @brief        Module To Parse the Mode Enum XML For all Mode Enumeration Tests.
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import os
from ctypes import Structure, Union, c_ubyte, c_uint
from enum import IntEnum
from typing import Optional, List, Any, Tuple, Dict
from xml.etree import ElementTree

from Libs.Core.test_env.test_context import TestContext
from Libs.Core import registry_access, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_struct import DisplayMode, DisplayAndAdapterInfo, SamplingMode, \
    DisplayTimings
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.display_mode_enum.mode_vic_info import VIC_MODE_INFO, DEFAULT_VIC_ID
from Libs.Feature.powercons import registry


##
# @brief        Enums for all the supported color types. These enum values are defined based on the ModeControlFlag
#               values present in the mode enumeration xml files.
class ColorFormat(IntEnum):
    RGB = 0
    YUV420 = 1
    YUV444 = 2
    YUV422 = 3


##
# @brief        BPC Mapping dictionary for ModeControlFlag.
#               (ControlFlags.bpc as Key) and (BPC as Value)
bpc_mapping = dict([
    (0, 6),
    (1, 8),
    (2, 10),
    (3, 12)
])


##
# @brief        Structure Definition for control flags for DisplayModeControlFlags.
class ControlFlags(Structure):
    _pack_ = 1
    _fields_ = [('color_format', c_ubyte, 2),
                ('sdp_splitting', c_ubyte, 1),
                ('bpc', c_ubyte, 2),
                ('reserved_5', c_ubyte, 1),
                ('pixel_rep_mode', c_ubyte, 1),
                ('is_fec_not_capable', c_ubyte, 1),
                ('is_dsc_not_capable', c_ubyte, 1),
                ('reserved_9', c_ubyte, 7)]


##
# @brief        Union Definition for DisplayModeControlFlags.
class DisplayModeControlFlags(Union):
    _fields_ = [("data", ControlFlags),
                ("as_int", c_uint)]


##
# @brief        Structure Definition for DisplayModeBlock.
class DisplayModeBlock:

    ##
    # @brief        Initializes the DisplayModeBlock member variables.
    def __init__(self) -> None:
        self.display_mode: Optional[DisplayMode] = None
        self.display_mode_control_flags: Optional[DisplayModeControlFlags] = None
        self.pixel_clock: int = 0
        self.audio_channel: int = 0
        self.audio_frequency_hz: int = 0
        self.audio_bitrate: int = 0


##
# @brief        Class Which Implements the Function to Parse the Mode Enum XML and to Initialize Golden Modes, Ignore
#               Modes and Modes to Apply. Also, to Get the Edid and DPCD File to Plug the Display.
class ModeEnumXMLParser:
    DISPLAY_HARDWARE_INFO = SystemInfo().get_gfx_display_hardwareinfo()
    SCAN_LINE_DICT = {'Progressive': 1, 'Interlaced': 2}
    SCALE_DICT = {'UN_SP': 0, 'Center': 1, 'Stretch': 2, 'MAR': 4, 'CAR': 8, 'Default': 64}

    ##
    # @brief        Initialize the Mode Enum XML Parser to the Default Values.
    # @param[in]    gfx_index: str
    #                   Graphics Adapter On Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port_name: str
    #                   Por Name On Which the Display is Plugged. E.g 'dp_b', 'hdmi_b'
    # @param[in]    xml_file_path: str
    #                   Contains XML File Path From Where Modes have to be Retrieved.
    def __init__(self, gfx_index: str, port_name: str, xml_file_path: str) -> None:
        self.gfx_index: str = gfx_index
        self._port_name: str = port_name.upper()
        self._xml_file_path = xml_file_path

        self._platform: str = ''
        self._sku_name: str = ''
        self._display_config: DisplayConfiguration = DisplayConfiguration()
        self._display_adapter_info: Optional[DisplayAndAdapterInfo] = None
        self._is_dp_dongle: bool = False

        # Get Edid and DPCD From the XML Which is Required to Plug the Display.
        self._panel_info: Any = ElementTree.parse(self._xml_file_path).getroot()
        self.edid_file = self._panel_info.get("EDID")
        self.dpcd_file = self._panel_info.get("DPCD")

        self.mst_topology_path = self._panel_info.get("TOPOLOGY_PATH")
        if self.mst_topology_path is not None:
            self.mst_topology_path = os.path.join(TestContext.panel_input_data(), self.mst_topology_path)

        self.display_tech = self._panel_info.get("DISPLAY_TECH")

        # Get Color Format
        self.color_format = self._panel_info.get('COLOR_FORMAT')
        self.color_format = self.color_format if self.color_format is not None else "RGB"

        # These Dictionaries Data Will be Parsed From the XML After Plugging the Display.
        self._mode_control_flag_dict: Dict[str, Any] = {}  # Value can be either int or List[int]
        self.golden_mode_dict: Dict[str, DisplayModeBlock] = {}
        self.ignore_mode_dict: Dict[str, DisplayModeBlock] = {}

        # Contains the list of modes that will be applied in the same order
        self.apply_mode_list: List[DisplayModeBlock] = []

    ##
    # @brief        Public Member Function to Parse and Construct the Display Based on the Internal State of the Object.
    # @return       None
    def parse_and_construct_mode_tables(self) -> None:
        is_success: bool = True
        index = int(self.gfx_index[-1])
        self._platform = ModeEnumXMLParser.DISPLAY_HARDWARE_INFO[index].DisplayAdapterName
        self._sku_name = SystemInfo().get_sku_name(self.gfx_index)

        self._display_adapter_info = self._display_config.get_display_and_adapter_info_ex(
            self._port_name, self.gfx_index
        )
        if type(self._display_adapter_info) is list:
            self._display_adapter_info = self._display_adapter_info[0]

        self._is_dp_dongle = self._get_is_dp_dongle()

        is_success &= self._parse_mode_enum_xml()
        assert is_success, 'Failed to Parse the XML and Construct Mode Table for {} Display'.format(self._port_name)

    ##
    # @brief        Private Member Function Which Helps to Decide If DP++ is Enabled in VBT.
    # @return       is_dp_dongle: bool
    #                   Return True if DP++ is Enabled in VBT, False Otherwise.
    def _get_is_dp_dongle(self) -> bool:
        is_dp_dongle: bool = False

        if 'HDMI' in self._port_name:
            port_label = self._port_name.split('_')[-1]
            supported_ports = display_config.get_supported_ports().keys()
            if ("DP_{0}".format(port_label) in supported_ports) or ("DP_{0}_++".format(port_label) in supported_ports):
                is_dp_dongle = True

        return is_dp_dongle

    ##
    # @brief        Private Member Function to Construct List Of Modes to be Applied From Test Script.
    # @param[in]    apply_mode_index_list: List[str]
    #                   Contains List Mode Index to Apply Which is Parsed From the Mode Enum XML.
    # @return       None
    def _construct_mode_list_to_apply(self, apply_mode_index_list: List[str]) -> None:

        # '*' Represents All the Modes In the Golden Modes. Hence, Copy to All the Modes to Apply Mode Dictionary
        if len(apply_mode_index_list) == 1 and apply_mode_index_list[0] == "*":
            self.apply_mode_list = list(self.golden_mode_dict.values())
        else:
            # Copy Only the Modes That Needs to Be Applied From Golden Mode Dictionary Using Apply Mode Index List.
            for apply_mode_index in apply_mode_index_list:
                self.apply_mode_list.append(self.golden_mode_dict[apply_mode_index])

    ##
    # @brief        Private Member Function To Update the Golden Mode Dictionary by Removing What's Present in the
    #               Ignore Mode Dictionary.
    # @return       None
    def _update_golden_mode_dict(self) -> None:
        if self.ignore_mode_dict:
            for ignore_mode_index, value in self.ignore_mode_dict.items():
                del self.golden_mode_dict[ignore_mode_index]

    ##
    # @brief        Private Member Function To Construct the Ignore Mode Dictionary By Using Ignore Mode Index List
    #               Read From the Mode Enum XML File and Also by Removing the Unsupported Modes Based on Pixel Clock
    #               And Pixel Rep Mode.
    # @param[in]    ignore_mode_index_list
    #                   Contains List of Modes That Are Parsed From the Mode Enum XML.
    # @return       None
    def _construct_ignore_mode_dict(self, ignore_mode_index_list: List[str]) -> None:
        if len(ignore_mode_index_list) == 0:
            return

        for golden_mode_index, mode in self.golden_mode_dict.items():
            for ignore_mode_index in ignore_mode_index_list:

                if ignore_mode_index == golden_mode_index:
                    self.ignore_mode_dict[golden_mode_index] = mode

            pixel_rep_mode = mode.display_mode_control_flags.data.pixel_rep_mode
            if pixel_rep_mode or (self._is_dp_dongle and mode.pixel_clock > 300000000) and ("HDMI" == self._port_name):
                self.ignore_mode_dict[golden_mode_index] = mode

    ##
    # @brief        Private Member Function to Get Display mode and Display Mode Control Flags For the Particular Mode.
    # @param[in]    mode_index: str
    #                   Mode Index For Which Display Mode Control Flags Has to be Created.
    # @param[in]    pixel_clock: int
    #                   Pixel Clock Required For the Respective Mode.
    # @param[in]    edid_instance: Any
    # #                   Represents Each Entry of the Mode In the Mode Enum XML File.
    # @return       mode_control_flags: DisplayModeControlFlags
    #                   Return the Display Mode and Display Mode Control Flags constructed using the XML Data
    def _get_display_mode_and_mode_control_flags(self, mode_index: str, pixel_clock: int, edid_instance: Any
                                                 ) -> Tuple[DisplayMode, DisplayModeControlFlags]:
        mode_control_flags = DisplayModeControlFlags()
        display_mode = DisplayMode()
        display_mode.displayAndAdapterInfo = self._display_adapter_info
        display_mode.targetId = self._display_adapter_info.TargetID
        display_mode.HzRes = int(edid_instance.get('HActive'))
        display_mode.VtRes = int(edid_instance.get('VActive'))
        display_mode.refreshRate = int(edid_instance.get('RefreshRate'))
        display_mode.pixelClock_Hz = int(edid_instance.get('PixelCLK'))
        display_mode.BPP = 4  # Assuming RGB888
        display_mode.rotation = 1
        display_mode.scanlineOrdering = ModeEnumXMLParser.SCAN_LINE_DICT[edid_instance.get('Scanline')]
        display_mode.scaling = ModeEnumXMLParser.SCALE_DICT[edid_instance.get('Scaling')]

        if mode_index in self._mode_control_flag_dict.keys():
            control_flag_list = self._mode_control_flag_dict[mode_index]
            for mode_flag in control_flag_list:
                mode_control_flags.as_int = mode_flag
                display_mode.samplingMode = ModeEnumHelper.update_sampling_mode(
                    mode_control_flags.data, display_mode.samplingMode
                )
        else:
            mode_control_flags.as_int = self._mode_control_flag_dict['CommonValue']
            display_mode.samplingMode = ModeEnumHelper.update_sampling_mode(
                mode_control_flags.data, display_mode.samplingMode
            )

        # Checking for DP++ dongle and resetting BPC to 8 if symbol clock exceeds allowed range (300MHz)
        if ('HDMI' in self._port_name) and self._is_dp_dongle and mode_control_flags.data.bpc > 1:
            bpc_multiplier = float(bpc_mapping[mode_control_flags.data.bpc]) / float(8)
            if (pixel_clock * bpc_multiplier) > 300000000:
                logging.debug("ModeIndex: {0} Pixel Clock exceeds 300MHz. Setting 8 BPC as expected".format(mode_index))
                mode_control_flags.data.bpc = 1  # 8 BPC

        return display_mode, mode_control_flags

    ##
    # @brief        Private Member Function to Get the Display Mode Block Which Contains Display Mode, Pixel Clock and
    #               display mode control flags.
    # @param[in]    mode_index: str
    #                   Represents the Mode Index For Which Display Mode Block Has to be Created.
    # @param[in]    edid_instance: Any
    #                   Represents Each Entry of the Mode In the Mode Enum XML File.
    # @return       display_mode_block: DisplayModeBlock
    #                   Returns DisplayModeBlock Object For the Edid Instance.
    def __get_display_mode_block__(self, mode_index: str, edid_instance: Any) -> DisplayModeBlock:
        pixel_clock = int(edid_instance.get('PixelCLK'))

        display_mode, display_mode_control_flags = self._get_display_mode_and_mode_control_flags(
            mode_index, pixel_clock, edid_instance
        )

        display_mode_block = DisplayModeBlock()
        display_mode_block.display_mode = display_mode
        display_mode_block.display_mode_control_flags = display_mode_control_flags
        display_mode_block.pixel_clock = pixel_clock
        if edid_instance.get('Channel') is not None and edid_instance.get('Channel') is not None and edid_instance.get(
                'Bitrate') is not None:
            display_mode_block.audio_channel = int(edid_instance.get('Channel'))
            display_mode_block.audio_frequency_hz = int(edid_instance.get('AudioFrequencyHz'))
            display_mode_block.audio_bitrate = int(edid_instance.get('Bitrate'))

        return display_mode_block

    ##
    # @brief        Private Member Function To Read the Golden Mode Values From the Mode Enum XML and Construct the
    #               Golden Mode Dictionary
    # @return       None
    def _construct_golden_mode_dict(self) -> None:
        golden_mode_table = self._panel_info.find('GoldenModeTable')

        edid_instance_iterator = golden_mode_table.iterfind('EDIDInstance')
        for edid_instance in edid_instance_iterator:
            mode_index: str = edid_instance.get('ModeIndex')
            display_mode_block = self.__get_display_mode_block__(mode_index, edid_instance)
            self.golden_mode_dict[mode_index] = display_mode_block

    ##
    # @brief        Private Member Function to Read the Mode Control Flag Values Present in the Mode Enum XML File.
    # @param[in]    platform_entry: Dict
    #                   Represents Each of the Platform Entry in the Mode Enum XML.
    # @return       None
    def __handle_mode_control_flag__(self, platform_entry: Any) -> None:
        custom_mode_values = []
        self._mode_control_flag_dict = {}

        mode_control_flag_entry = platform_entry.find('ModeControlFlag')
        if mode_control_flag_entry.text != 'None':
            custom_mode_values = mode_control_flag_entry.text.split(";")

        self._mode_control_flag_dict['CommonValue'] = int(mode_control_flag_entry.get('CommonValue'), 16)
        for flag_value in custom_mode_values:
            split_data = flag_value.split('=')
            index = split_data[0].split(',')
            # Append the multiple supported color format to the list for each mode_index.This avoids over-writing
            # of the supported color formats
            for i in index:
                if i not in self._mode_control_flag_dict.keys():
                    self._mode_control_flag_dict[i] = [int(split_data[1], 16)]
                else:
                    self._mode_control_flag_dict[i].append(int(split_data[1], 16))

    ##
    # @brief        Private Member Function to Get the Ignore Mode Index List and Apply Mode Index List By Parsing the
    #               Mode Enum XML File.
    # @return       (, , ): Tuple[bool, List[str], List[str]]
    #                   is_platform_supported: bool
    #                       Tells if the XML File is Valid For the Given Platform.
    #                   ignore_mode_index_list: List[str]
    #                       Contains List of Indices For the Modes to be Ignored.
    #                   apply_mode_index_list: List[str]
    #                       Contains List of Indices For the Modes to be Applied by the Test.
    def _get_ignore_apply_mode_index_list(self) -> Tuple[bool, List[str], List[str]]:
        is_platform_supported: bool = False
        ignore_mode_index_list = apply_mode_index_list = mode_sequence_index_list = []
        matched_platform_entry = None

        platform_iterator = self._panel_info.iterfind('Platform')
        for platform_entry in platform_iterator:
            platform_name: str = platform_entry.get('Name')
            sku_name: str = platform_entry.get('SKU')

            if self._platform == platform_name and sku_name == "":
                matched_platform_entry = platform_entry

            # Checking for the derivative platform. Cannot combine SKU name condition in above platform name condition,
            # if we combine then we can't handle all the cases.
            # Case 1: E.g. On DG2, in xml SKU name will be empty, and the sku_name will have value which is present in
            # platform_ids.xml file, so it will never match, and we will not enter inside the "if" and for this case the
            # details will be updated in above itself.
            # Case 2: E.g. On ACMP, in xml SKU name will be ACMP, and the sku_name will have value which is present in
            # platform_ids.xml file, which will be again ACMP and hence below if condition will match for ACMP which is
            # a derivative platform of DG2 and all the entries will be updated as per ACMP entry instead of DG2 entry.
            if self._platform == platform_name and sku_name == self._sku_name:
                matched_platform_entry = platform_entry
                break

        if matched_platform_entry is not None:
            is_platform_supported = True
            ignore_mode_index_list = matched_platform_entry.find("IgnoreModeIndex").text.split(",")
            apply_mode_index_list = matched_platform_entry.find("ApplyModeIndex").text.split(",")
            if matched_platform_entry.find("ModeSequenceIndex") is not None:
                mode_sequence_index_list = matched_platform_entry.find("ModeSequenceIndex").text.split(",")
            self.__handle_mode_control_flag__(matched_platform_entry)

        # Replace the Apply Mode Index List with Mode Sequence Index list if Sequence is specified in the XML
        if len(mode_sequence_index_list) != 0:
            apply_mode_index_list = mode_sequence_index_list

        if is_platform_supported is False:
            logging.error(f"XML File Specified is Not Valid For the Platform {self._platform} [{self._sku_name}]")

        return is_platform_supported, ignore_mode_index_list, apply_mode_index_list

    ##
    # @brief        Public Member Function to Which Helps to Parse the Mode Enum XML File and Construct Golden Mode
    #               Table, Ignore Mode Table and Apply Mode Table.
    # @return       is_success: bool
    #                   Returns True If XML Parsing is Success and If All Mode Tables are Constructed.
    def _parse_mode_enum_xml(self) -> bool:
        is_success: bool = True

        func_status, ignore_mode_index_list, apply_mode_index_list = self._get_ignore_apply_mode_index_list()
        is_success &= func_status

        if is_success is True:
            self._construct_golden_mode_dict()
            self._construct_ignore_mode_dict(ignore_mode_index_list)
            self._update_golden_mode_dict()
            self._construct_mode_list_to_apply(apply_mode_index_list)

        return is_success


##
# @brief        Helper class which holds all the helper functions required for all ModeEnumeration Tests.
class ModeEnumHelper:

    ##
    # @brief        Class method to force YUV422 mode in driver by setting ForceApplyYUV422Mode reg key
    # @param[in]    gfx_index: str
    #                   Graphics Adapter On Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    to_enable: int
    #                   1 - To enable reg key, 0 to disable the reg key
    # @return       is_success: bool
    #                   True if Registry write is success or if same value exists in registry, False otherwise
    @classmethod
    def enable_yuv422_mode(cls, gfx_index, to_enable: int) -> bool:
        registry_key = "ForceApplyYUV422Mode"

        is_success = registry.write(gfx_index, registry_key, registry_access.RegDataType.DWORD, to_enable)

        if is_success is True:  # Registry write is successful, restart the display driver
            is_success, reboot_required = display_essential.restart_gfx_driver()
            if is_success is False:
                logging.error("Failed to restart display driver after updating {0} registry key".format(registry_key))
        elif is_success is False:  # Registry write is failed.
            logging.error("Failed to update {0} registry value to {1}".format(registry_key, to_enable))
        else:  # Registry write not done, since same value already exists.
            logging.info("Skipping registry write as same value already exists in {} registry".format(registry_key))
            is_success = True

        return is_success

    ##
    # @brief        Update the SamplingMode() object based on the color format bits of mode control flag
    # @param[in]    control_flags: ControlFlags
    #                    First 2 bits of the control flag represent the color format.Ex: colorFormat_RGB = 00,
    #                    colorFormat_YUV420 = 01, colorFormat_YUV444 = 10, colorFormat_YUV422 = 11
    # @param[in]    sampling_mode: SamplingMode
    #                    The first four bits of this object represents RGB, YUV420,YUV444, YUV422 formats respectively
    #                    These bits are set based on the color format bits obtained from control_flags
    # @return       sampling_mode: SamplingMode
    #                    Contains the updated value
    @classmethod
    def update_sampling_mode(cls, control_flags: ControlFlags, sampling_mode: SamplingMode) -> SamplingMode:
        if control_flags.color_format == 0:
            sampling_mode.rgb = 1  # Assigning default value to RGB
        elif control_flags.color_format == 1:
            sampling_mode.yuv420 = 1  # YUV420
        elif control_flags.color_format == 2:
            sampling_mode.yuv444 = 1  # YUV444
        elif control_flags.color_format == 3:
            sampling_mode.yuv422 = 1  # YUV422

        return sampling_mode

    ##
    # @brief        get_vic_data for the current mode
    # @param[in]    display_timing: Display timing details for which the VIC id is required.
    # @return       vic_id: VIC id for the current timing
    @classmethod
    def get_vic_data(cls, display_timing: DisplayTimings) -> int:
        vic_id = 255
        logging.info(f"Display timing: {display_timing.to_string()}")

        for vic_data, vic_display_timing in VIC_MODE_INFO.items():
            # QDC currently gives incorrect vTotal and doesn't have RR. Both these are anyway not required here as
            # we will be able to find the VIC id with hActive, vActive, hTotal and target pixel rate.
            # Hence removing it from this condition
            if (vic_display_timing['hactive'] == display_timing.hActive and
                    vic_display_timing['vactive'] == display_timing.vActive and
                    vic_display_timing['htotal'] == display_timing.hTotal and
                    vic_display_timing['pixel_clock'] == display_timing.targetPixelRate and
                    vic_display_timing['interlaced'] == display_timing.scanlineOrdering):
                vic_list = list(map(int, vic_data.split('_')[1:]))
                vic_id = vic_list[0]
                logging.info(f'Mode is a VIC Mode. Corresponding VIC ID List: {vic_list}')
                break

        if vic_id == 255:
            logging.info(f'Mode is not a vic mode. Default VIC ID: {DEFAULT_VIC_ID}')

        return vic_id
