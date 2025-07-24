########################################################################################################################
# @file         edid_modes_xml_parser.py
# @brief        Provides HdmiEdidModesXmlParser class with methods for parsing EDID Modes xml info
# @details      <ul>
#               <li> ref  get_edid_mode_enumeration_list     \n copybrief get_edid_mode_enumeration_list \n
#               <li> ref  get_unsupported_mode_list        	 \n copybrief get_unsupported_mode_list \n
#               <li> ref  get_apply_edid_mode_list        	 \n copybrief get_apply_edid_mode_list \n
#               <li> ref  get_apply_deep_color_mode_list     \n copybrief get_apply_deep_color_mode_list \n
#               <li> ref  get_apply_mode_list        		 \n copybrief get_apply_mode_list \n
#               </li>
#               </ul>
# @author       Girish Y D
########################################################################################################################

import os
import xml.etree.ElementTree as ET

from Tests.Hdmi.utility.edid_mode_info import *


##
# @brief        HdmiEdidModeXmlParser
class HdmiEdidModesXmlParser(object):
    ##
    # @brief        Parses both Mode node/elements in the XML
    # @param[in]    mode_element - Element mode Value
    # @return       edid_mode
    def parse_mode_element(self, mode_element):
        edid_mode = TestModeInfo(int(mode_element.get('HzRes')), int(mode_element.get('VtRes')),
                                 int(mode_element.get('refreshRate')),
                                 int(SCANLINE_DICT[mode_element.get('scanlineOrdering')]))

        if mode_element.get('modeIndex') is not None:
            edid_mode.modeIndex = int(mode_element.get('modeIndex'))
        if mode_element.get('edidModeCategory') is not None:
            edid_mode.edidModeCategory = str(mode_element.get('edidModeCategory'))
        if mode_element.get('vic') is not None:
            edid_mode.vic = int(mode_element.get('vic'))
        if mode_element.get('BPP') is not None:
            edid_mode.BPP = int(BPP_DICT[mode_element.get('BPP')])
        if mode_element.get('scaling') is not None:
            edid_mode.scaling = int(SCALING_DICT[mode_element.get('scaling')])
        if mode_element.get('rotation') is None:
            edid_mode.rotation = int(ROTATION_DICT[mode_element.get('rotation')])
        if mode_element.get('isNativeMode') is not None:
            edid_mode.isNativeMode = int(mode_element.get('isNativeMode'))
        if mode_element.get('isYUV420Mode') is not None:
            edid_mode.isYUV420Mode = int(mode_element.get('isYUV420Mode'))
            if edid_mode.isYUV420Mode == 1:
                edid_mode.sourcePixelFormat = "YUV420"
                edid_mode.expectedPixelFormat = "YUV420"

        if mode_element.get('modeName') is not None:
            edid_mode.modeName = str(mode_element.get('modeName'))
        else:
            if mode_element.get('scanlineOrdering') == "PROGRESSIVE":
                scanlineOrdering = "P"
            elif mode_element.get('scanlineOrdering') == "INTERLACED":
                scanlineOrdering = "I"
            else:
                scanlineOrdering = "U"

            pixelFormat = "RGB"
            if int(mode_element.get('isYUV420Mode')) == 1:
                pixelFormat = "YUV420"

            edid_mode.modeName = (
                    "%s_8BPC_%s_%s_%s%s" % (pixelFormat, mode_element.get('HzRes'), mode_element.get('VtRes'),
                                            mode_element.get('refreshRate'), scanlineOrdering))

        ExpectedParameters = mode_element.find('ExpectedParameters')
        if ExpectedParameters is not None:
            edid_mode.expectedPixelClockMHz = float(ExpectedParameters.get('pixelClockMHz'))
            edid_mode.Hactive = int(ExpectedParameters.get('Hactive'))
            edid_mode.Vactive = int(ExpectedParameters.get('Vactive'))
            edid_mode.Hblank = int(ExpectedParameters.get('Hblank'))
            edid_mode.Vblank = float(ExpectedParameters.get('Vblank'))
            edid_mode.Htotal = int(ExpectedParameters.get('Htotal'))
            edid_mode.Vtotal = int(ExpectedParameters.get('Vtotal'))
            if ExpectedParameters.get('PictureAspectRatio') is not None:
                edid_mode.PictureAspectRatio = str(ExpectedParameters.get('PictureAspectRatio'))
        return edid_mode

    ##
    # @brief        Parses the xml and returns edid mode indexes of unsupported modes based on platform
    # @param[in]    edid_modes_xml_path - EDID modes XML file path
    # @param[in]    platform - Platform Info
    # @return       unsupported_edid_mode_indexes - Unsupported EDID mode Indexes
    def get_unsupported_edid_mode_indexes(self, edid_modes_xml_path, platform):
        tree = ET.parse(edid_modes_xml_path)
        display_root = tree.getroot()
        unsupported_edid_mode_indexes = []
        for UnSupportedModes_node in display_root.findall('UnSupportedModes'):
            for UnSupportedModeIndex_node in UnSupportedModes_node.findall('EdidModeIndexes'):
                platforms = UnSupportedModeIndex_node.get('Platform').split(",")
                if platform in platforms:
                    if UnSupportedModeIndex_node.text is not None:
                        unsupported_edid_mode_indexes = UnSupportedModeIndex_node.text.split(",")
        return unsupported_edid_mode_indexes

    ##
    # @brief        Parses the xml and returns all the Edid modes to be enumerated by driver based on platform
    # @param[in]    edid_modes_xml_path - EDID modes XML file path
    # @param[in]    platform - Platform Info
    # @return       mode_enumeration_list - List of Modes
    def get_edid_mode_enumeration_list(self, edid_modes_xml_path, platform):
        tree = ET.parse(edid_modes_xml_path)
        display_root = tree.getroot()
        mode_enumeration_list = []
        unsupported_edid_mode_indexes = self.get_unsupported_edid_mode_indexes(edid_modes_xml_path, platform)
        for edid_modes_node in display_root.findall('EdidModes'):
            for edid_mode_element in edid_modes_node.findall('EdidMode'):
                if unsupported_edid_mode_indexes is None or edid_mode_element.get(
                        'modeIndex') not in unsupported_edid_mode_indexes:
                    edid_mode = self.parse_mode_element(edid_mode_element)
                    mode_enumeration_list.append(edid_mode)
        return mode_enumeration_list

    ##
    # @brief        Parses the xml and returns all the unsupported modes by platform which are listed in XML
    # @param[in]    edid_modes_xml_path - EDID modes XML file path
    # @param[in]    platform - Platform Info
    # @return       unsupported_mode_list - list of Unsupported modes
    def get_unsupported_mode_list(self, edid_modes_xml_path, platform):
        tree = ET.parse(edid_modes_xml_path)
        display_root = tree.getroot()
        unsupported_mode_list = []
        unsupported_edid_mode_indexes = self.get_unsupported_edid_mode_indexes(edid_modes_xml_path, platform)
        if unsupported_edid_mode_indexes is not None:
            for edid_modes_node in display_root.findall('EdidModes'):
                for edid_mode_element in edid_modes_node.findall('EdidMode'):
                    if edid_mode_element.get('modeIndex') in unsupported_edid_mode_indexes:
                        edid_mode = self.parse_mode_element(edid_mode_element)
                        unsupported_mode_list.append(edid_mode)

        for UnSupportedModes_node in display_root.findall('UnSupportedModes'):
            for unsupported_modes in UnSupportedModes_node.findall('NonEdidModes'):
                if unsupported_modes.get('Platform') is not None:
                    platforms = unsupported_modes.get('Platform').split(",")
                    if platform in platforms:
                        for mode_element in unsupported_modes.findall('Mode'):
                            mode = self.parse_mode_element(mode_element)
                            unsupported_mode_list.append(mode)
        return unsupported_mode_list

    ##
    # @brief        Parses the xml and returns list of apply edid modes which are listed in xml
    # @param[in]    edid_modes_xml_path - EDID modes XML file path
    # @param[in]    platform - Platform Info
    # @return       apply_mode_list - List of modes to be applied
    def get_apply_edid_mode_list(self, edid_modes_xml_path, platform):
        tree = ET.parse(edid_modes_xml_path)
        display_root = tree.getroot()
        ##
        # Get apply Mode index
        apply_edid_mode_indexes = []
        for apply_modes_node in display_root.findall('ApplyModes'):
            for apply_edid_mode_indexes_node in apply_modes_node.findall('EdidModeIndexes'):
                platforms = apply_edid_mode_indexes_node.get('Platform').split(",")
                if platform in platforms:
                    if apply_edid_mode_indexes_node.text is not None:
                        apply_edid_mode_indexes = apply_edid_mode_indexes_node.text.split(",")
        ##
        # Build Apply Mode List
        apply_mode_list = []
        if apply_edid_mode_indexes is not None:
            mode_enumeration_list = self.get_edid_mode_enumeration_list(edid_modes_xml_path, platform)
            for mode in mode_enumeration_list:
                if apply_edid_mode_indexes[0] == "*" or str(mode.modeIndex) in apply_edid_mode_indexes:
                    mode.platform = platform
                    apply_mode_list.append(mode)
        return apply_mode_list

    ##
    # @brief        Parses the xml and Returns the list of deep color  mode listed in XML
    # @param[in]    edid_modes_xml_path - EDID modes XML file path
    # @param[in]    platform - Platform Info
    # @return       apply_deep_color_mode_list - List of deep color modes to be applied
    def get_apply_deep_color_mode_list(self, edid_modes_xml_path, platform):
        tree = ET.parse(edid_modes_xml_path)
        display_root = tree.getroot()
        apply_deep_color_mode_list = []
        for apply_modes_node in display_root.findall('ApplyModes'):
            for deep_color_modes in apply_modes_node.findall('DeepColorModes'):
                platforms = deep_color_modes.get('Platform').split(",")
                if platform.upper() in platforms:
                    for mode_element in deep_color_modes.findall('Mode'):
                        mode = None
                        if mode_element.get('EdidModeIndex') is not None:
                            edid_mode_enumeration_list = self.get_edid_mode_enumeration_list(edid_modes_xml_path,
                                                                                             platform)
                            for edid_mode in edid_mode_enumeration_list:
                                if edid_mode.modeIndex == int(mode_element.get('EdidModeIndex')):
                                    mode = edid_mode
                        else:
                            mode = self.parse_mode_element(mode_element)
                        if mode is not None:
                            mode.platform = platform
                            mode.modeName = str(mode_element.get('modeName'))
                            if mode_element.find('sourcePixelFormat') is not None:
                                mode.sourcePixelFormat = mode_element.find('sourcePixelFormat').text
                            if mode_element.find('sourceBPC') is not None:
                                mode.sourceBPC = int(mode_element.find('sourceBPC').text)
                            if mode_element.find('expectedPixelFormat') is not None:
                                mode.expectedPixelFormat = mode_element.find(
                                    'expectedPixelFormat').text
                            if mode_element.find('expectedBPC') is not None:
                                mode.expectedBPC = int(mode_element.find('expectedBPC').text)
                            apply_deep_color_mode_list.append(mode)

        return apply_deep_color_mode_list

    ##
    # @brief        Parses the xml and returns the list of apply mode listed in XML
    # @param[in]    edid_modes_xml_path - EDID modes XML file path
    # @param[in]    platform - Platform Info
    # @return       apply_mode_list - Mode list to be applied
    def get_apply_mode_list(self, edid_modes_xml_path, platform):
        apply_mode_list = []
        apply_edid_mode_list = self.get_apply_edid_mode_list(edid_modes_xml_path, platform)
        apply_deepcolor_mode_list = self.get_apply_deep_color_mode_list(edid_modes_xml_path, platform)

        apply_mode_list.extend(apply_edid_mode_list)
        apply_mode_list.extend(apply_deepcolor_mode_list)

        return apply_mode_list

    ##
    # @brief        Parses the xml and Returns Edid Info which is in XML
    # @param[in]    edid_modes_xml_path - EDID modes XML file path
    # @return       edid_info - the edid info obtained from XML file
    def get_edid_info_from_xml(self, edid_modes_xml_path):
        tree = ET.parse(edid_modes_xml_path)
        display_root = tree.getroot()
        edid_info = HdmiEDIDInfo()
        if display_root.get('Type') is not None:
            edid_info.display_type = display_root.get('Type')

        for EDIDInfo_node in display_root.findall('EDIDInfo'):
            if EDIDInfo_node.find('MaxTMDSClockSupported') is not None:
                edid_info.MaxTMDSClockSupported = float(EDIDInfo_node.find('MaxTMDSClockSupported').text)
            if EDIDInfo_node.find('SCDCPresent') is not None:
                edid_info.SCDCPresent = float(EDIDInfo_node.find('SCDCPresent').text)
            if EDIDInfo_node.find('RRCapable') is not None:
                edid_info.RRCapable = float(EDIDInfo_node.find('RRCapable').text)
            if EDIDInfo_node.find('LTE340MhzScramble') is not None:
                edid_info.LTE340MhzScramble = float(EDIDInfo_node.find('LTE340MhzScramble').text)
        return edid_info


if __name__ == "__main__":
    edid_path = r"C:\temp-work\DisplayAutomation2.0_x64\Tests\Hdmi\mode\edid_modes_xml"
    edid_file = "HDMI_EDID_YUV420_3840_2160_60HzMode.xml"
    edid_modes_xml_path = os.path.join(edid_path, edid_file)
    hdmi_edid_modes_xml_parser = HdmiEdidModesXmlParser()

    ##
    # Get modes from xml which need to be set and set the all modes
    edid_info = hdmi_edid_modes_xml_parser.get_edid_info_from_xml(edid_modes_xml_path)
    test_mode_info_list = hdmi_edid_modes_xml_parser.get_apply_mode_list(edid_modes_xml_path, "ICL")
    for test_mode_info in test_mode_info_list:
        print(test_mode_info.modeName)
        print(test_mode_info)
