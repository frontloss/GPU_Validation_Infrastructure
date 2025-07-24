import ctypes
import logging
import os
import sys
import time
import unittest
import win32api
import win32con
from ctypes.wintypes import HANDLE
from xml.etree import ElementTree as ET

from Libs.Core import display_utility, cmd_parser, enum, system_utility, reboot_helper, registry_access, \
    display_essential, window_helper
from Libs.Core.display_config import display_config
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, DisplayConfigTopology
from Libs.Core.display_power import DisplayPower
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.logger import gdhm
from Libs.Core.flip import MPO
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Tests.Color.HDR.Gen11_Flip.MPO3H.HDRVerification import HDRVerification, BlendingMode, PanelCaps, OutputRange
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3args import PLANES, HDRInfo
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3enums import MPO_COLOR_SPACE_CS_FLAG_MAPPING
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3enums import PLANES_ERROR_CODE, SB_PIXELFORMAT, MPO_COLOR_SPACE_TYPE
from Tests.Color.color_common_utility import gdhm_report_app_color
from Tests.MPO.Flip.GEN11.MPO3H import register_verification as reg

machine_info = SystemInfo()
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break

BT2020_LINEAR = 2

VBIEnableExe = os.path.join(test_context.BIN_FOLDER, "VBIEnable.exe")


class HDRBase(unittest.TestCase):
    MPO3 = ctypes.cdll.LoadLibrary(os.path.join(test_context.TestContext.bin_store(), 'GfxValSim.dll'))

    gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
    native_mode, HzRes, VtRes, rr = None, None, None, None
    srcList = []
    destList = []
    currentMode = []
    sourceID = []
    pixel_format = []
    color_space = []
    cs_flags = []
    path = []
    blendingMode = []
    outputRange = []
    panelCaps = []
    hdrmetadata = []
    reference_metadata = []
    NoLayers = []
    targetId = None
    utility = system_utility.SystemUtility()
    is_high_resolution = False
    is_writeback_enabled = False
    wb_device_count = 0
    wb_device_list = list()
    display_config = DisplayConfiguration()
    display_power = DisplayPower()
    hdr = HDRVerification()
    underrun = UnderRunStatus()
    supported_ports_dict = {}
    is_ddrw = system_utility.SystemUtility().is_ddrw()
    custom_tags = ["-INPUTFILEPATH", "-WRITEBACK"]
    my_tags = ["INPUTFILEPATH"]
    connected_list = []
    connected_list_with_wb = []
    sinkHDR = None
    stepCounter = 0
    exec_env = utility.get_execution_environment_type()
    port = None
    test_after_reboot_status = False
    lfp_simulation_enable = False
    DP_chaining = None
    lfp_support_in_vbt = False
    vbi_enable_status = False

    ##
    # This function verifies if at least 2 ports are enabled in VBT as required by the LINEAR tests
    # Also fetches either LFP or an appropriate external port enabled in the VBT so that we can simulate the plug of the port within the test.
    def fetch_port_for_inline_simulation(self):
        lfp_support_in_vbt = False
        port_for_inline_simulation = None
        self.supported_ports_dict = display_config.get_supported_ports()
        if len(self.supported_ports_dict) < 2 and self.blendingMode[0] == BT2020_LINEAR:
            logging.error(
                "Only %s ports is enabled in the VBT! Linear Test requires at least 2 ports to be enabled" % len(
                    self.supported_ports_dict))
            self.fail()
        else:
            for port, types in self.supported_ports_dict.items():
                ##
                # Check if LFP is enabled in VBT
                if display_utility.get_vbt_panel_type(port, 'gfx_0') in [display_utility.VbtPanelType.LFP_DP,
                                                                         display_utility.VbtPanelType.LFP_MIPI]:
                    lfp_support_in_vbt = True
                    port_for_inline_simulation = port
                    break
                ##
                # Cases where LFP is not POR, choose any port enabled other than the port mentioned in the command line.
                # Ex : In platforms like DG1, LFP is not POR.
                else:
                    if port != self.connected_list[0]:
                        port_for_inline_simulation = port
                        break
            logging.debug("Port Details are %s" % self.port)
            return port_for_inline_simulation, lfp_support_in_vbt

    ##
    # For platforms where LFP is not POR, test does an inline plug of the external panel enabled in the VBT.
    # This function calls the plug() with the details of the appropriate port.
    def inline_plug_of_external_display(self):
        if self.port[:2] == 'DP':
            if display_utility.plug(self.port, "DP_3011.EDID", "DP_3011_DPCD.txt") is False:
                logging.error("Failed to plug %s" % self.port)
                self.fail()
            else:
                logging.info("Successfully plugged %s" % self.port)
        elif self.port[:4] == 'HDMI':
            if display_utility.plug(self.port, 'HDMI_Dell_3011.EDID') is False:
                logging.error("Failed to Plug %s" % self.port)
                self.fail()
            else:
                logging.info("Successfully plugged %s" % self.port)
        else:
            logging.error("Failed to apply configuration due to invalid port details")
            self.fail()

    def setUp(self):
        is_lfp_plugged = False
        logging.info('********************* TEST  STARTS HERE **************************')
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

            elif key in self.my_tags and value != 'NONE':
                self.xml = value[0]

        self.parseXML(self.xml)
        ##
        # As a WA for HSD-1507422663, applying ED display config with LFP and external display in case of LINEAR tests.
        # 'port' has port config details of the LFP based on the platform details.
        # If physical LFP is not connected to the machine in GTA, test script will plug the LFP and apply SD configuration on LFP,
        # followed by ED configuration; For platforms where LFP is not POR(Ex : DG1), an external panel will be plugged
        self.port, self.lfp_support_in_vbt = self.fetch_port_for_inline_simulation()

        if self.blendingMode[0] == BT2020_LINEAR and display_utility.get_vbt_panel_type(self.connected_list[0], 'gfx_0')\
                not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
            ##
            # Fetch enumerated display info before plugging LFP to check if LFP is already present
            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            ##
            # Verify if LFP is already plugged
            for index in range(0, self.enumerated_displays.Count):
                logging.debug("TargetID is %d" % self.enumerated_displays.ConnectedDisplays[index].TargetID)
                logging.debug("Is Target Active : %d" % self.enumerated_displays.ConnectedDisplays[index].IsActive)
                logging.debug("Connector Port Type is %s" % (
                    CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)).name)
                gfx_index = self.enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                if display_utility.get_vbt_panel_type(CONNECTOR_PORT_TYPE(
                        self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name, gfx_index) in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                    is_lfp_plugged = True
                    logging.info("LFP panel is already attached!")
                    break
            ##
            # Cases where LFP is not POR; plug the external port
            if self.lfp_support_in_vbt == False:
                self.inline_plug_of_external_display()
            ##
            # Verify if LFP/external display is already plugged and apply configuration
            if is_lfp_plugged or self.lfp_support_in_vbt == False:
                topology = enum.SINGLE
                if self.display_config.set_display_configuration_ex(topology, [self.port]) == True:
                    logging.info("Applied display configuration successfully as %s %s" % (
                        DisplayConfigTopology(topology).name, self.port))
                else:
                    self.fail("Failed to apply display configuration %s %s" % (
                        DisplayConfigTopology(topology).name, self.port))

                self.current_config = self.display_config.get_current_display_configuration()
                self.NoOfDisplays = self.current_config.numberOfDisplays

                # ##
                # Plug the external display which is provided as part of the command line parameter.
                self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self,
                                                                                               self.cmd_line_param)

                ##
                # Apply EXTENDED Display configuration
                topology = enum.EXTENDED
                if self.display_config.set_display_configuration_ex(topology,
                                                                    [self.port, self.connected_list[0]]) is True:
                    logging.info("Applied display configuration successfully as %s %s" % (
                        DisplayConfigTopology(topology).name, self.connected_list))
                else:
                    self.fail("Failed to apply display configuration %s %s" % (
                        DisplayConfigTopology(topology).name, self.connected_list))
                self.current_config = self.display_config.get_current_display_configuration()
                self.targetId = self.current_config.displayPathInfo[1].targetId
                self.sourceID.insert(0, self.current_config.displayPathInfo[1].sourceId)
            ##
            # Plug an LFP through Val-sim if physical LFP is not connected in the GTA farm
            else:
                adapter_info = test_context.TestContext.get_gfx_adapter_details()['gfx_0']
                driver_interface.DriverInterface().initialize_lfp_ports(adapter_info, [self.port])
                plug_result = display_utility.plug(port=self.port, is_lfp=True, gfx_index='gfx_0')
                if plug_result:
                    self.lfp_simulation_enable = True
                    logging.info("Simulation Enable is %s" % self.lfp_simulation_enable)
                    return
                else:
                    logging.error("Failed to plug LFP")
                    self.fail("Failed to plug LFP")
        ##
        # For Non-Linear test, apply SD config on LFP.
        else:
            if self.is_writeback_enabled == False:
                self.enumerated_displays = self.display_config.get_enumerated_display_info()
                topology = enum.SINGLE
                if self.display_config.set_display_configuration_ex(topology, [self.connected_list[0]]) == True:
                    logging.info("Applied display configuration successfully as %s %s" % (
                        DisplayConfigTopology(topology).name, self.connected_list[0]))
                else:
                    self.fail("Failed to apply display configuration %s %s" % (
                        DisplayConfigTopology(topology).name, self.connected_list[0]))
            self.current_config = self.display_config.get_current_display_configuration()
            self.NoOfDisplays = self.current_config.numberOfDisplays
            self.targetId = self.current_config.displayPathInfo[0].targetId
            self.sourceID.insert(0, self.current_config.displayPathInfo[0].sourceId)

        ##
        # Apply native mode on the target display of choice.
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        supported_modes = self.display_config.get_all_supported_modes([self.targetId])
        self.native_mode = self.display_config.get_native_mode(self.targetId)
        if self.native_mode is None:
            logging.error(f"Failed to get native mode for {self.targetId}")
            return False
        self.HzRes = self.native_mode.hActive
        self.VtRes = self.native_mode.vActive
        self.rr = self.native_mode.refreshRate

        logging.info("Native mode is %s %s %s" % (self.HzRes, self.VtRes, self.rr))

        result = False
        for key, values in supported_modes.items():
            for mode in values:
                if mode.HzRes == self.HzRes and mode.VtRes == self.VtRes and mode.scaling == enum.MDS:
                    result = self.display_config.set_display_mode([mode])
                    break
        if result:
            current_mode = self.display_config.get_current_mode(self.targetId)
            logging.info("Mode is %sX%s@%s with scaling : %s" % (
                current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
        else:
            logging.error("Failed to apply the required mode")
            self.fail("Failed to apply the required mode")

        self.current_mode = self.display_config.get_current_mode(self.targetId)
        return

    def getStepCounter(self):
        self.stepCounter = self.stepCounter + 1
        return "STEP-%d:" % self.stepCounter

    def enable_disable_mpo(self, enable_disable_status):
        self.test_name = sys.argv[0]

        if enable_disable_status and self.exec_env == 'POST_SI_ENV':
            MPO().enable_disble_os_flipq(True)
            status, reboot_required = display_essential.restart_gfx_driver()

            time.sleep(2)

        if enable_disable_status:
            win32api.ShellExecute(None, "open", VBIEnableExe, None, None, win32con.SW_NORMAL)
            logging.info("VBIEnable Exe executed successfully")
            self.vbi_enable_status = True

        if self.is_ddrw:
            self.gfxvalsim_handle = driver_interface.DriverInterface().get_driver_handle()
            if self.gfxvalsim_handle is None:
                logging.error("Failed to get valsim handle")
            self.MPO3.DDRW_EnableDisableMPOSimulation.argtypes = [ctypes.POINTER(GfxAdapterInfo), HANDLE, ctypes.c_bool]
            self.MPO3.DDRW_EnableDisableMPOSimulation.restype = ctypes.c_bool
            self.MPO3.DDRW_EnableDisableMPOSimulation(self.gfx_adapter_dict['gfx_0'], self.gfxvalsim_handle,
                                                      enable_disable_status)



            self.MPO3.DDRW_CheckForMultiPlaneOverlaySupport3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                         ctypes.POINTER(PLANES)]
            self.MPO3.DDRW_CheckForMultiPlaneOverlaySupport3.restype = ctypes.c_bool
            self.MPO3.DDRW_SetSourceAddressForMultiPlaneOverlay3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                             ctypes.POINTER(PLANES)]
            self.MPO3.DDRW_SetSourceAddressForMultiPlaneOverlay3.restype = ctypes.c_bool

        else:
            self.MPO3.mainline_CheckForMultiPlaneOverlaySupport3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                             ctypes.POINTER(PLANES)]
            self.MPO3.mainline_CheckForMultiPlaneOverlaySupport3.restype = ctypes.c_int
            self.MPO3.mainline_SetSourceAddressForMultiPlaneOverlay3.argtypes = [ctypes.POINTER(GfxAdapterInfo),
                                                                                 ctypes.POINTER(PLANES)]
            self.MPO3.mainline_SetSourceAddressForMultiPlaneOverlay3.restype = ctypes.c_int
            self.MPO3.mainline_EnableDisableMPODFT.argtypes = [ctypes.POINTER(GfxAdapterInfo), HANDLE, ctypes.c_bool,
                                                                  ctypes.c_int]
            self.MPO3.mainline_EnableDisableMPODFT.restype = ctypes.c_bool
            self.MPO3.mainline_EnableDisableMPODFT(self.gfx_adapter_dict['gfx_0'], self.gfxvalsim_handle,
                                                      enable_disable_status, 1)

        if self.vbi_enable_status and not enable_disable_status:
            status = window_helper.kill_process_by_name('VBIEnable.exe')
            if status:
                logging.info("VBIEnable application is closed")
            else:
                self.fail("VBIEnable application is not closed")
            self.vbi_enable_status = False

        if enable_disable_status is False and self.exec_env == 'POST_SI_ENV':
            MPO().enable_disble_os_flipq(False)
            status, reboot_required = display_essential.restart_gfx_driver()

    def parseXML(self, xmlFile):

        tree = ET.parse(xmlFile)
        input = tree.getroot()

        plane = input.findall("./Plane")

        for element in plane:
            ##
            # Get the plane info from the XML file
            self.pixel_format.append(getattr(SB_PIXELFORMAT, element.find("./SourcePixelFormat").text))
            self.color_space.append(getattr(MPO_COLOR_SPACE_TYPE, element.find("./ColorSpace").text))
            self.cs_flags.append(getattr(MPO_COLOR_SPACE_CS_FLAG_MAPPING, element.find("./ColorSpace").text))

            self.path.append(os.path.join(test_context.SHARED_BINARY_FOLDER, element.find("./ImageFilePath").text))

        pipe = input.findall("./Pipe")

        for element in pipe:
            self.blendingMode.append(getattr(BlendingMode, element.find("./BlendingMode").text))
            if self.connected_list[0][:2] == 'DP':
                self.outputRange.append(OutputRange.FULL)
            else:
                self.outputRange.append(getattr(OutputRange, element.find("./OutputRange").text))
            self.panelCaps.append(getattr(PanelCaps, element.find("./PanelCaps").text))
            self.DP_chaining = element.find('SinkHDR')
            if self.DP_chaining is not None:
                self.sinkHDR = element.find("./SinkHDR").text

        hdrmetadata = input.findall("./HDRMetadata")
        for element in hdrmetadata:
            eotf = int(element.find("./EOTF").text)
            primariesX = list(map(int, element.find("./DisplayPrimariesX").text.split(",")))
            primariesY = list(map(int, element.find("./DisplayPrimariesY").text.split(",")))
            whitepointX = int(element.find("./WhitePointX").text)
            whitepointY = int(element.find("./WhitePointY").text)
            maxlum = int(element.find("./MaxLuminance").text)
            minlum = int(element.find("./MinLuminance").text)
            maxCLL = int(element.find("./MaxCLL").text)
            maxFALL = int(element.find("./MaxFALL").text)

            self.hdrmetadata = HDRInfo(eotf, primariesX, primariesY, whitepointX, whitepointY, maxlum, minlum, maxCLL,
                                       maxFALL)
            ##
            # Translation of the HDR10 Luminnance data in Reference Metadata
            # by converting to milli nits before comparing with the programmed
            self.reference_metadata = [eotf, primariesX[0], primariesY[0], primariesX[1], primariesY[1], primariesX[2],
                                       primariesY[2], whitepointX, whitepointY, (maxlum / 1000), (minlum * 10),
                                       (maxCLL / 1000), (maxFALL / 1000)]
            return

    def set_ForceHDREnable_regkey(self):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if self.exec_env == 'POST_SI_ENV':
            logging.info("Exec env is Post Si hence the driver restart needs to be done")
            if not registry_access.write(args=reg_args, reg_name="ForceHDRMode",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=1):
                logging.error("Registry key add to disable ForceHDRMode failed")
                self.fail()
        else:
            reg_value, reg_type = registry_access.read(args=reg_args, reg_name="ForceHDRMode")
            if not reg_value:
                logging.error(
                    "Exec Env is %s  and the registry key for Linear mode is not set in the plugin" % self.exec_env)
                self.fail()

    def set_mode(self):
        result = False
        if (self.panelCaps[0] == getattr(PanelCaps, "HDR_BT2020_YUV420") or self.panelCaps[0] == getattr(PanelCaps,
                                                                                                         "HDR_BT2020_RGB")):
            rr = 30
        else:
            rr = 60
        supported_modes = self.display_config.get_all_supported_modes([self.targetId])
        for key, values in supported_modes.items():
            for mode in values:
                if mode.HzRes == self.HzRes and mode.VtRes == self.VtRes and mode.scaling == enum.MDS:
                    result = self.display_config.set_display_mode([mode])
                    break

        if result:
            current_mode = self.display_config.get_current_mode(self.targetId)
            logging.info("Current mode: %sX%s @%s %s" % (
                current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate, current_mode.scaling))
        else:
            logging.error("Failed to apply the Native Resolution")
            self.fail("Failed to apply the Native Resolution")

    def setup_for_linear_mode(self):
        self.set_ForceHDREnable_regkey()
        self.set_mode()

    def convert_image(self, input_file, width, height, pixel_format, layer_index):
        str1 = '_' + str(layer_index) + '.bin'
        output_file = input_file.replace('.png', str1)
        if os.path.exists(output_file):
            os.remove(output_file)
        executable = 'ImageFormater.exe'
        commandline = executable + ' -i ' + input_file + ' -w ' + str(width) + ' -h ' + str(height) + ' -f ' + str(
            pixel_format) + ' -o ' + output_file
        print("****************", commandline)
        currentdir = os.getcwd()
        os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
        print("Current", os.getcwd())
        os.system(commandline)
        os.chdir(currentdir)
        return output_file.encode()

    def performFlip(self, planes):
        result = 0
        scalarEnable = []
        current_pipe = 0
        logging.debug("Details of Plane configuration")
        for index in range(0, planes.uiPlaneCount):
            if self.is_writeback_enabled is True:
                # TODO: Current_pipe has been hardcoded to 1. Need to find ways to get pipe id of writeback device
                current_pipe = 1
            else:
                display_base_obj = DisplayBase(self.connected_list[0])
                current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[0])
            pipeID = current_pipe
            logging.info("Pipe : %d Plane : %d Src: (%d,%d,%d %d) , Dst : (%d,%d,%d,%d)  Clip : (%d,%d,%d,%d) ",
                         pipeID + 1, int(self.NoLayers[pipeID] - planes.stPlaneInfo[index].iLayerIndex),
                         planes.stPlaneInfo[index].MPOSrcRect.left,
                         planes.stPlaneInfo[index].MPOSrcRect.top, planes.stPlaneInfo[index].MPOSrcRect.right,
                         planes.stPlaneInfo[index].MPOSrcRect.bottom,
                         planes.stPlaneInfo[index].MPODstRect.left, planes.stPlaneInfo[index].MPODstRect.top,
                         planes.stPlaneInfo[index].MPODstRect.right, planes.stPlaneInfo[index].MPODstRect.bottom,
                         planes.stPlaneInfo[index].MPOClipRect.left, planes.stPlaneInfo[index].MPOClipRect.top,
                         planes.stPlaneInfo[index].MPOClipRect.right, planes.stPlaneInfo[index].MPOClipRect.bottom)

        logging.info(self.getStepCounter() + "Calling CheckMPO to verify if HW supports flipping of requested plane(s)")
        if self.is_ddrw:
            result = self.MPO3.DDRW_CheckForMultiPlaneOverlaySupport3(self.gfx_adapter_dict['gfx_0'],
                                                                      planes)  # TODO: Multi-adapter WA: Hardcoding to gfx_0 to retrieve primary adapter
        else:
            result = self.MPO3.mainline_CheckForMultiPlaneOverlaySupport3(self.gfx_adapter_dict['gfx_0'],
                                                                          planes)  # TODO: Multi-adapter WA: Hardcoding to gfx_0 to retrieve primary adapter
        if result == PLANES_ERROR_CODE.PLANES_SUCCESS:
            logging.info("CheckMPO returned success")

            logging.info(self.getStepCounter() + "Performing flipping of planes")
            if self.is_ddrw:
                status = self.MPO3.DDRW_SetSourceAddressForMultiPlaneOverlay3(self.gfx_adapter_dict['gfx_0'],
                                                                              planes)  # TODO: Multi-adapter WA: Hardcoding to gfx_0 to retrieve primary adapter
            else:
                status = self.MPO3.mainline_SetSourceAddressForMultiPlaneOverlay3(self.gfx_adapter_dict['gfx_0'],
                                                                                  planes)  # TODO: Multi-adapter WA: Hardcoding to gfx_0 to retrieve primary adapter

            if status == PLANES_ERROR_CODE.PLANES_SUCCESS:
                logging.info("Successfully flipped planes")
                for index in range(0, planes.uiPlaneCount):
                    if (planes.stPlaneInfo[index].MPOSrcRect.right != planes.stPlaneInfo[index].MPODstRect.right or
                            planes.stPlaneInfo[index].MPOSrcRect.bottom != planes.stPlaneInfo[index].MPODstRect.bottom):
                        scalarEnable.append(1)

                logging.info(self.getStepCounter() + "Verifying for underrun")
                if self.underrun.verify_underrun():
                    logging.error("Underrun Occured")

                logging.info(self.getStepCounter() + "Verifying programming")
                for index in range(0, planes.uiPlaneCount):
                    if self.is_writeback_enabled == False:
                        display_base_obj = DisplayBase(self.connected_list[0])
                        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(
                            self.connected_list[0])
                    pipeID = current_pipe
                    planeID = int(self.NoLayers[pipeID] - planes.stPlaneInfo[index].iLayerIndex)
                    logging.info("Verifying plane programming for planeId: %d PipeId: %d" % (planeID, pipeID))
                    if not reg.verifyPlaneProgramming(pipeID, planeID, planes.stPlaneInfo[index].eSBPixelFormat,
                                                      planes.stPlaneInfo[index].eSurfaceMemType,
                                                      planes.stPlaneInfo[index].MPOClipRect.left,
                                                      planes.stPlaneInfo[index].MPOClipRect.top,
                                                      planes.stPlaneInfo[index].MPOClipRect.right,
                                                      planes.stPlaneInfo[index].MPOClipRect.bottom,
                                                      (planes.stPlaneInfo[index].MPOSrcRect.right - planes.stPlaneInfo[
                                                          index].MPOSrcRect.left), scalarEnable):
                        return False

                    logging.info(
                        self.getStepCounter() + "Verifying HDR Plane programming: Pipe id = %d Plane Index = %d",
                        pipeID, planeID)
                    if not self.hdr.verifyHDRPlaneProgramming(pipeID, planeID, planes.stPlaneInfo[index].eSBPixelFormat,
                                                              planes.stPlaneInfo[index].eColorSpace,
                                                              self.blendingMode[0]):
                        return False
                    else:
                        logging.info("verifyHDRPlaneProgramming completed")

                    logging.info(self.getStepCounter() + "Verifying HDR Pipe programming")
                    if not self.hdr.verifyHDRPipeProgramming(pipeID, self.blendingMode[0], self.panelCaps[0],
                                                             self.outputRange[0]):
                        return False
                    else:
                        logging.info("verifyHDRPipeProgramming completed")
                    ##
                    # Performing metadata verification
                    if self.blendingMode[0] == BT2020_LINEAR:
                        if self.hdr.verify_metadata(self.connected_list[0], pipeID, self.targetId, self.blendingMode[0], self.reference_metadata):
                            logging.info("Metadata Verification : SUCCESS")
                        else:
                            logging.error("Metadata Verification : FAILED")
                            return False

                    if self.sinkHDR == "DP1.4_SDP_Chaining":
                        if self.hdr.verifyDP1_4HDRMetadataProgramming(pipeID, self.reference_metadata):
                            logging.info("Verification of DP1.4 Static Metadata Programming is completed successfully")
                        else:
                            logging.error("Verification of DP1.4 Static Metadata Programming failed")
                            return False

                time.sleep(5)
            elif status == PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                gdhm_report_app_color(title="[COLOR][HDR]Resource creation failed")
                logging.error("Resource creation failed")
                return False
            else:
                gdhm_report_app_color(title="[COLOR][HDR]Set source address failed")
                logging.error("Set source address failed")
                return False

        elif result == PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
            gdhm_report_app_color(title="[COLOR][HDR]Resource creation failed")
            logging.error("Resource creation failed")
            return False
        else:
            gdhm_report_app_color(title="[COLOR][HDR]Driver did not meet the requirements")
            logging.error("Driver did not meet the requirements")
            return False

        return True

    def apply_config_on_wb_device(self, config_type):
        logging.debug("Apply_config_on_wb_device() Entry:")

        display_info_list = []
        enumerated_display = self.display_config.get_enumerated_display_info()
        for display_count in range(0, enumerated_display.Count):
            self.connected_list_with_wb.append(
                str(CONNECTOR_PORT_TYPE(
                    enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)))
            logging.debug("Connected display is %s" % str(
                CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType)))
            for i in range(0, len(self.connected_list_with_wb)):
                if self.connected_list_with_wb[i] == "WD_0":
                    self.assertEquals(
                        self.display_config.set_display_configuration_ex(config_type, [self.connected_list_with_wb[i]],
                                                                         self.display_config.get_enumerated_display_info()),
                        True, "Failed to apply display configuration")
                    logging.info("\tPASS: Successfully applied Display configuration")
        return True

    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        ##
        # Disable DFT
        self.enable_disable_mpo(False)
        exec_env = self.utility.get_execution_environment_type()
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if exec_env == 'POST_SI_ENV':
            if self.blendingMode[0] == BT2020_LINEAR:
                if not registry_access.write(args=reg_args, reg_name="ForceHDRMode",
                                             reg_type=registry_access.RegDataType.DWORD, reg_value=0):
                    logging.error("Registry key add to disable ForceHDRMode failed")
                    self.fail()
                status, reboot_required = display_essential.restart_gfx_driver()

        ##
        # Unplug the displays and restore the configuration to the initial configuration
        logging.info("In tearDown, getting enumerated display count %s" % self.enumerated_displays.Count)
        for display in self.connected_list:
            if self.lfp_simulation_enable is True:
                if display == 'DP_A' or display == 'MIPI_A':
                    if display_utility.unplug(port=self.port, is_lfp=True, gfx_index='gfx_0'):
                        logging.info("Unplug of LFP is successful")
                else:
                    display_utility.unplug(display)
            else:
                if display == 'DP_A' or display == 'MIPI_A':
                    logging.debug("Unplug of physical eDP not required")
                else:
                    display_utility.unplug(display)

        logging.info('********************* TEST  ENDS HERE **************************')
