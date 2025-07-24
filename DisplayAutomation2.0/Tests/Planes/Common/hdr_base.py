########################################################################################################################
# @file         hdr_base.py
# @brief        The script implements unittest default functions for setUp and tearDown, and common helper functions
#               given below:
#               * Parse XML and populate attributes.
#               * Enable HDR mode, Higher BPC.
#               * Enable/Disable required settings to linear mode.
#               * Convert PNG input to raw dump given buffer parameters.
#               * Get number of planes given source id.
#               * Perform flip based on input parameters and hardware accuracy.
# @author       R Soorya, Balasubramanyam Smitha
########################################################################################################################

import logging
import os
import sys
import unittest
import xml.etree.ElementTree as ET

from Libs.Core import cmd_parser, registry_access, display_essential
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import flip
from Libs.Core import system_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Tests.Color.color_common_utility import gdhm_report_app_color
from Tests.Planes.Common import hdr_verification
from Tests.Planes.Common import planes_verification, planes_helper
from Libs.Feature.presi.presi_crc import start_plane_processing

BT2020_LINEAR = 2
XML_PATH = os.path.join(test_context.ROOT_FOLDER, "Tests\\Planes\\HDR\\INPUT_XML")


##
# @brief Base class for HDR tests
class HDRBase(unittest.TestCase):
    native_mode, HzRes, VtRes, rr = None, None, None, None
    source_id = []
    pixel_format = []
    color_space = []
    path = []
    blending_mode = []
    output_range = []
    panel_caps = []
    hdr_metadata = []
    current_mode = []
    hdr = hdr_verification.HDRVerification()
    underrun = UnderRunStatus()
    display_config = DisplayConfiguration()
    connected_list = []
    reference_metadata = []
    step_counter = 0
    exec_env = None
    sinkHDR = None
    DP_chaining = None
    mpo = flip.MPO()
    driver_interface_ = driver_interface.DriverInterface()
    ##
    # SB_PIXELFORMAT values for planar formats
    planar_formats = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

    ##
    # @brief            Unittest setUp function
    # @return           None
    def setUp(self):
        logging.info('********************* TEST  STARTS HERE **************************')
        self.exec_env = system_utility.SystemUtility().get_execution_environment_type()

        ##
        # Custom tags for input XML
        custom_tags = ["-INPUTFILE"]
        ##
        # Parse the commandlines
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags)
        ##
        # Obtain display port list and xml name from the command line.
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])
            elif key in "INPUTFILE" and value != 'NONE':
                self.xml = value[0]
        ##
        # Verify and plug the display.
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        ##
        # Apply Display configuration
        if len(self.connected_list) > 1:
            topology = enum.EXTENDED
            if self.display_config.set_display_configuration_ex(topology, self.connected_list) is True:
                logging.info(" Step %s : Applied display configuration successfully as %s %s" % (
                    (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))
                self.current_config = self.display_config.get_current_display_configuration()
                self.targetId = self.current_config.displayPathInfo[1].targetId
                self.source_id.insert(0, self.current_config.displayPathInfo[1].sourceId)
            else:
                self.fail("Step %s : Failed to apply display configuration %s %s" % (
                    (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))
        else:
            topology = enum.SINGLE
            if self.display_config.set_display_configuration_ex(topology, self.connected_list) is True:
                logging.info(" Step %s : Applied display configuration successfully as %s %s" % (
                    (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))
                self.current_config = self.display_config.get_current_display_configuration()
                self.targetId = self.current_config.displayPathInfo[0].targetId
                self.source_id.insert(0, self.current_config.displayPathInfo[0].sourceId)
            else:
                self.fail("Step %s : Failed to apply display configuration %s %s" % (
                    (self.step_counter + 1), DisplayConfigTopology(topology).name, self.connected_list))
        self.no_displays = 1
        ##
        # Start underrun monitor.
        self.underrun.clear_underrun_registry()

    ##
    # @brief        To set the native resolution of each display
    # @return       None
    def set_native_mode(self):
        status = False
        for index in range(0, self.no_displays):

            target_id = self.display_config.get_target_id(self.connected_list[index], self.enumerated_displays)

            native_mode = self.display_config.get_native_mode(target_id)
            if native_mode is None:
                logging.error(f"Failed to get native mode for {target_id}")
                return False
            edid_hzres = native_mode.hActive
            edid_vtres = native_mode.vActive
            edid_refreshrate = native_mode.refreshRate

            supported_modes = self.display_config.get_all_supported_modes([target_id])
            for key, values in supported_modes.items():
                for mode in values:
                    if mode.HzRes == edid_hzres and mode.VtRes == edid_vtres and mode.refreshRate == edid_refreshrate and mode.scaling == enum.MDS:
                        status = self.display_config.set_display_mode([mode])
                        logging.info("Applied Display mode: %s" % mode.to_string(self.enumerated_displays))

            if status:
                logging.info("Successfully applied native mode")
            else:
                logging.error("Failed to apply native mode")

            mode = self.display_config.get_current_mode(target_id)
            self.current_mode.append(mode)

    ##
    # @brief        To parse the input xml and populate the attributes required for the test
    # @param[in]    xml_file Input XML file name
    # @return       None
    def parse_xml(self, xml_file):
        xml_file = os.path.join(XML_PATH, xml_file)
        tree = ET.parse(xml_file)
        input = tree.getroot()

        plane = input.findall("./Plane")

        for element in plane:
            ##
            # Get the plane info from the XML file
            self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, element.find("./SourcePixelFormat").text))
            self.color_space.append(getattr(flip.MPO_COLOR_SPACE_TYPE, element.find("./ColorSpace").text))
            self.path.append(os.path.join(test_context.SHARED_BINARY_FOLDER, element.find("./ImageFilePath").text))

        pipe = input.findall("./Pipe")

        for element in pipe:
            ##
            # Get the pipe info from the XML file
            self.blending_mode.append(getattr(hdr_verification.BLENDINGMODE, element.find("./BlendingMode").text))
            if len(self.connected_list) > 1 and self.connected_list[1][:2] == 'DP' and self.connected_list[1] != 'DP_A':
                self.output_range.append(hdr_verification.OUTPUTRANGE.FULL)
            else:
                self.output_range.append(getattr(hdr_verification.OUTPUTRANGE, element.find("./OutputRange").text))
            self.panel_caps.append(getattr(hdr_verification.PANELCAPS, element.find("./PanelCaps").text))
            self.DP_chaining = element.find('SinkHDR')
            if self.DP_chaining is not None:
                self.sinkHDR = element.find("./SinkHDR").text

        hdr_metadata = input.findall("./HDRMetadata")
        for element in hdr_metadata:
            ##
            # Get the HDR Metadata info from the XML file
            eotf = int(element.find("./EOTF").text)
            primariesX = list(map(int, element.find("./DisplayPrimariesX").text.split(",")))
            primariesY = list(map(int, element.find("./DisplayPrimariesY").text.split(",")))
            whitepointX = int(element.find("./WhitePointX").text)
            whitepointY = int(element.find("./WhitePointY").text)
            maxlum = int(element.find("./MaxLuminance").text)
            minlum = int(element.find("./MinLuminance").text)
            maxCLL = int(element.find("./MaxCLL").text)
            maxFALL = int(element.find("./MaxFALL").text)

            self.hdr_metadata = flip.HDR_INFO(eotf, primariesX, primariesY, whitepointX, whitepointY, maxlum, minlum,
                                              maxCLL,
                                              maxFALL)
            ##
            # Translation of the HDR10 Luminnance data in Reference Metadata
            # by converting to milli nits before comparing with the programmed
            self.reference_metadata = [eotf, primariesX[0], primariesY[0], primariesX[1], primariesY[1], primariesX[2],
                                       primariesY[2], whitepointX, whitepointY,
                                       (maxlum / 1000), (minlum * 10), (maxCLL / 1000), (maxFALL / 1000)]

    ##
    # @brief        To set ForceHDR registry to enable HDR mode
    # @return       None
    def set_force_hdrenable_regkey(self):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if self.exec_env != 'POST_SI_ENV':
            reg_value, reg_type = registry_access.read(args=reg_args, reg_name="ForceHDRMode")
            if not reg_value:
                logging.error(
                    "Exec Env is %s  and the registry key for Linear mode is not set in the plugin" % self.exec_env)
                self.fail()
        else:
            if not registry_access.write(args=reg_args, reg_name="ForceHDRMode",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=1):
                logging.error("Registry key add to enable ForceHDRMode failed")
                self.fail()

    ##
    # @brief        To set override BPC registry to enable higher BPC
    # @return       None
    def set_bpc_registry(self):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if len(self.connected_list) > 1:
            bits_per_color = 10
        else:
            if (self.connected_list[0][:2] == 'DP'):
                bits_per_color = 10
            else:
                bits_per_color = 12

        if self.exec_env != 'POST_SI_ENV':
            reg_value1, reg_type1 = registry_access.read(args=reg_args, reg_name="SelectBPC")
            reg_value2, reg_type2 = registry_access.read(args=reg_args, reg_name="SelectBPCFromRegistry")
            if reg_value1 == 0 or reg_value2 == 0:
                logging.error(
                    "Exec Env is %s  and the registry key for BPC is not set in the plugin" % self.exec_env)
                self.fail()
        else:
            key_name = "SelectBPC"
            value = 1
            if registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                     reg_value=value) is False:
                self.fail("Registry key add to enable SelectBPC  failed")
            key_name = "SelectBPCFromRegistry"
            value = int(bits_per_color)
            if registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                     reg_value=value) is False:
                self.fail("Registry key add to set SelectBPCFromRegistry  failed")

    ##
    # @brief        To enable settings required exclusive to linear mode
    # @return       None
    def setup_for_linear_mode(self):
        self.set_force_hdrenable_regkey()
        # TODO : Uncomment after the PreSi restart issue is resolved
        # self.set_bpc_registry()
        if self.exec_env == 'POST_SI_ENV':
            logging.info("Exec env is Post Si hence the driver restart needs to be done")
            status, reboot_required = display_essential.restart_gfx_driver()

    ##
    # @brief        To disable settings required exclusive to linear mode
    # @return       None
    def reset_registries_linear_mode(self):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if self.exec_env == 'POST_SI_ENV':
            if not registry_access.write(args=reg_args, reg_name="ForceHDRMode",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=0):
                logging.error("Registry key add to disable ForceHDRMode failed")
                self.fail()
            if not registry_access.write(args=reg_args, reg_name="SelectBPC",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=0):
                logging.error("Registry key add to disable SelectBPC  failed")
                self.fail()
            status, reboot_required = display_essential.restart_gfx_driver()

    ##
    # @brief        To invoke the utility to convert PNG input file to raw dump given the buffer parameters
    # @param[in]    input_file PNG input file name
    # @param[in]    width Output HRes of buffer
    # @param[in]    height Output VRes of buffer
    # @param[in]    pixel_format Source Pixel format
    # @param[in]    layer_index Layer index of the plane
    # @param[in]    display_index Display index
    # @return       output_file
    def convert_png_to_bin(self, input_file, width, height, pixel_format, layer_index, display_index):
        str1 = '_' + str(layer_index) + str(display_index) + '.bin'
        output_file = input_file.replace('.png', str1)
        if os.path.exists(output_file):
            os.remove(output_file)
        executable = 'ImageFormater.exe'
        commandline = executable + ' -i ' + input_file + ' -w ' + str(width) + ' -h ' + str(height) + ' -f ' + str(
            pixel_format) + ' -o ' + output_file
        logging.debug("ImageFormatter commandline : %s", commandline)
        currentdir = os.getcwd()
        os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
        logging.debug("Current path : %s", os.getcwd())
        os.system(commandline)
        os.chdir(currentdir)
        return output_file

    ##
    # @brief        Get the no of planes created for given source id
    # @param[in]	source_id source_id Source id of the plane
    # @param[in]	planes planes Pointer to structure PLANE containing the plane info
    # @return       Plane count per source id
    def get_plane_count_for_source_id(self, source_id, planes):
        plane_count = 0
        for index in range(0, planes.uiPlaneCount):
            if source_id == planes.stPlaneInfo[index].iPathIndex:
                plane_count = plane_count + 1
        return plane_count

    ##
    # @brief        To initiate plane processing
    # @return       None
    def perform_plane_processing(self):
        logging.info("Performing plane processing")
        swf_offset = 0x4f080
        value = 0x1
        self.driver_interface_.mmio_write(swf_offset, value, 'gfx_0')

    ##
    # @brief        To flip with the given input parameters
    # @param[in]	planes Pointer to structure PLANE containing the plane info
    # @return       Boolean,status of the flip
    def perform_hdr_flip(self, planes):
        display_index = 0

        ##
        # Applying Unity Gamma LUT since from 19H1 onwards, OS applies a non-linear LUT on boot
        logging.info("Trying to apply UnityGamma LUT")
        executable = 'UnityGamma.exe'
        currentdir = os.getcwd()
        os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
        os.system(executable)
        os.chdir(currentdir)
        logging.info("Successfully applied UnityGamma LUT")

        if len(self.connected_list) > 1:
            display_index = len(self.connected_list) - 1
        ##
        # Check for the hardware support for plane parameters
        logging.info(" Step %s :Calling CheckMPO to verify if HW supports flipping of requested plane(s)" % (
                self.step_counter + 1))
        checkmpo_result = self.mpo.check_mpo3(planes)

        if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
            logging.info("Step %s: Flipping the planes and verifying the planes" % (self.step_counter + 1))
            ##
            # Flip the content
            ssa_result = self.mpo.set_source_address_mpo3(planes)

            if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                sys_util = system_utility.SystemUtility()
                exec_env = sys_util.get_execution_environment_type()
                if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_adapter_index='gfx_0'):
                    start_plane_processing()
                logging.info("Successfully flipped planes")

                # Iterate through all active planes
                for index in range(0, planes.uiPlaneCount):
                    logging.info("Step %s : MMIO Programming Verification " % (self.step_counter + 1))
                    for index in range(0, planes.uiPlaneCount):
                        display_base_obj = DisplayBase(self.connected_list[display_index])
                        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(
                            self.connected_list[display_index])
                        pipe_id = current_pipe
                        plane_count = self.get_plane_count_for_source_id(planes.stPlaneInfo[index].iPathIndex, planes)
                        plane_id = planes_verification.get_plane_id_from_layerindex(plane_count, planes.stPlaneInfo[index].uiLayerIndex, gfx_index='gfx_0')
                        pixel_format = planes.stPlaneInfo[index].ePixelFormat
                        tile_format = planes.stPlaneInfo[index].eSurfaceMemType
                        width = planes.stPlaneInfo[index].stMPOSrcRect.lRight - planes.stPlaneInfo[
                            index].stMPOSrcRect.lLeft
                        if (planes.stPlaneInfo[index].stMPOSrcRect.lRight != planes.stPlaneInfo[
                            index].stMPODstRect.lRight
                                or planes.stPlaneInfo[index].stMPOSrcRect.lBottom != planes.stPlaneInfo[
                                    index].stMPODstRect.lBottom
                                or planes.stPlaneInfo[index].stMPOSrcRect.lLeft != planes.stPlaneInfo[
                                    index].stMPODstRect.lLeft
                                or planes.stPlaneInfo[index].stMPOSrcRect.lTop != planes.stPlaneInfo[
                                    index].stMPODstRect.lTop):
                            scalar_enable = 1
                        else:
                            scalar_enable = 0

                        logging.info(" Plane verification for Pipe : {} Plane :{}".format(pipe_id, plane_id))

                        if not planes_verification.verify_planes(pipe_id, plane_id, pixel_format, tile_format, width,
                                                                 scalar_enable,
                                                                 planes.stPlaneInfo[index].stMPOClipRect.lLeft,
                                                                 planes.stPlaneInfo[index].stMPOClipRect.lRight,
                                                                 planes.stPlaneInfo[index].stMPOClipRect.lTop,
                                                                 planes.stPlaneInfo[index].stMPOClipRect.lBottom,
                                                                 planes.stPlaneInfo[index].bEnabled):
                            logging.error("Plane verification failed !!")
                            return False

                        else:
                            logging.info("Plane verification passed ")
                        logging.info(
                            "HDR Plane programming fo verification for Pipe : {} Plane :{}".format(pipe_id, plane_id))
                        if not self.hdr.verify_hdr_plane_programming(pipe_id, plane_id,
                                                                     planes.stPlaneInfo[index].ePixelFormat,
                                                                     planes.stPlaneInfo[index].eColorSpace,
                                                                     self.blending_mode[0]):
                            logging.error("HDR Plane Programming verification failed !!")
                            return False
                        else:
                            logging.info("HDR Plane Programming verification passed")

                # Iterate through active pipes
                for display in range(0, self.no_displays):
                    display_base_obj = DisplayBase(self.connected_list[display_index])
                    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(
                        self.connected_list[display_index])
                    pipe_id = current_pipe

                    logging.info("Verifying HDR Pipe programming for Pipe : {} ".format(pipe_id))
                    if not self.hdr.verify_hdr_pipe_programming(pipe_id, self.blending_mode[0], self.panel_caps[0],
                                                                self.output_range[0]):
                        logging.error("HDR Pipe Programming verification failed !!")
                        return False
                    else:
                        logging.info("HDR Pipe Programming verification passed")

                    if self.sinkHDR == "DP1.4_SDP_Chaining":
                        if self.hdr.verifyDP1_4HDRMetadataProgramming(pipe_id, self.reference_metadata):
                            logging.info("Verification of DP1.4 Static Metadata Programming is completed")
                        else:
                            logging.error("Verification of DP1.4 Static Metadata Programming failed")
                            return False

                logging.info(" Step %s : Verifying for underrun" % (self.step_counter + 1))
                if self.underrun.verify_underrun():
                    logging.error("Underrun Occured")
            elif ssa_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                gdhm_report_app_color(title="[COLOR][HDR]Resource creation failed")
                logging.error("Resource creation failed")
                return False
            else:
                gdhm_report_app_color(title="[COLOR][HDR]Set source address failed")
                logging.error("Set source address failed")
                return False
        elif checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            gdhm_report_app_color(title="[COLOR][HDR]Resource creation failed")
            logging.error("Resource creation failed")
            return False
        else:
            gdhm_report_app_color(title="[COLOR][HDR]Driver did not meet the requirements")
            logging.error("Driver didn't meet the plane requirements !!")
            return False
        return True

    ##
    # @brief            To perform flip based on hardware accuracy
    # @param[in]        planes planes Pointer to structure PLANE containing the plane info
    # @return           void
    def perform_flip_hwaccuracy(self, planes):
        result = self.mpo.check_mpo3(planes)
        if result != 0:
            logging.info("CheckMPO returned success")
            logging.info(" Performing flip of planes")
            status = self.mpo.set_source_address_mpo3(planes)
        else:
            logging.info("Driver didn't meet the plane requirements !!")
        return result

    ##
    # @brief            Unittest tearDown function
    # @return           None
    def tearDown(self):
        ##
        # Disable DFT
        self.mpo.enable_disable_mpo_dft(False, 1)

        ##
        # Reset registries set for linear mode
        if self.blending_mode[0] == BT2020_LINEAR:
            self.reset_registries_linear_mode()
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.connected_list:
            if display != 'DP_A':
                logging.info("Trying to unplug %s", display)
                display_utility.unplug(display)
        logging.info('********************* TEST  ENDS HERE **************************')


if __name__ == '__main__':
    unittest.main()
