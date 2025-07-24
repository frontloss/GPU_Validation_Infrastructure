######################################################################################
# @file     display_config_ult_2.0.py
# @brief    Each function in this base will verify the functionality of display_config.py
# @author   Raghupathy
# @details  Commandline : python Tests\ULT\display_config_ult_2.0.py -gfx_index_1 <Display1><Display2>< ... >
#           Example : python Tests\ULT\display_config_ult_2.0.py -gfx_0 -edp_a -dp_b -gfx_1 -dp_b -hdmi_c
######################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser, enum
from Libs.Core import display_utility
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.test_env import test_environment


class DisplayConfigULT(unittest.TestCase):
    internal_displays_list = {}
    display_dict = {}
    topology = None
    enum_info = None
    cmd_line_param = None
    display_config_ = None
    display_and_adapter_info_list = []

    @classmethod
    def setUpClass(cls):
        cls.display_config_ = display_config.DisplayConfiguration()
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        cls.de_result = True

        def add_or_append(dictionary, key, value):
            if key not in dictionary:
                dictionary[key] = []
            dictionary[key].append(value)

        for index in range(len(cls.cmd_line_param)):
            for key, value in cls.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        add_or_append(cls.display_dict, value['gfx_index'], value['connector_port'])
                        if value['is_lfp'] is True:
                            add_or_append(cls.internal_displays_list, value['gfx_index'], value['connector_port'])

        for key, value in cls.display_dict.items():
            if key in cls.internal_displays_list:
                value = set(cls.internal_displays_list[key]).symmetric_difference(cls.display_dict[key])
            for port in value:
                assert display_utility.plug(port, gfx_index=str(key).lower()), "Failed to plug the display"

        cls.display_and_adapter_info_list = []
        for key, value in cls.display_dict.items():
            for port in value:
                display_and_adapter_info = cls.display_config_.get_display_and_adapter_info_ex(port, key)
                if type(display_and_adapter_info) is list:
                    display_and_adapter_info = display_and_adapter_info[0]

                cls.display_and_adapter_info_list.append(display_and_adapter_info)

    ##
    # Getting Display Config Interface Version
    def test_0_1(self):
        logging.info("******************** TEST_1: START **********************************")
        logging.info("*********get_display_config_interface_version() *********************")
        version = self.display_config_.get_display_config_interface_version()
        self.assertIsNotNone(version, "FAIL : Get Display Config Interface Version")
        logging.info("PASS : Display Config DLL version : {}".format(version))
        logging.info("******************** TEST_1: END ************************************\n")

    ##
    # Getting Enumerated Display Info, All Display Configuration, Current Display Configuration Ex
    def test_0_2(self):
        logging.info("******************** TEST_2: START **********************************")
        logging.info("************ get_enumerated_display_info() **************************")
        self.enum_info = self.display_config_.get_enumerated_display_info()
        self.assertNotEqual(self.enum_info.Count, 0, "FAIL : Failed to Get Enumerated Display Info")
        logging.info("PASS : Get Enumerated Display Info")
        logging.info("INFO : Number of Enumerated Display's : {}".format(self.enum_info.Count))
        for display_index in range(self.enum_info.Count):
            logging.info("INFO : Display-{} Info:".format(display_index + 1))
            logging.info("          Port Info           : {0}_{1}, [{2}]".format(
                (cfg_enum.CONNECTOR_PORT_TYPE(self.enum_info.ConnectedDisplays[display_index].ConnectorNPortType)).name,
                self.enum_info.ConnectedDisplays[display_index].PortType,
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex))
            logging.info(
                "          Display isActive    : {}".format(self.enum_info.ConnectedDisplays[display_index].IsActive))
            logging.info("          Source ID           : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.SourceID))
            logging.info("          Target ID           : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.TargetID))
            logging.info("          BusDeviceID         : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.busDeviceID))
            logging.info("          VendorID            : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.vendorID))
            logging.info("          DeviceID            : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.deviceID))
            logging.info("          DeviceInstanceID    : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.deviceInstanceID))
            logging.info("          GfxIndex            : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex))
            logging.info("          Adapter isActive    : {}".format(
                self.enum_info.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.isActive))

        logging.info("************get_all_display_configuration() *************************")
        all_config = self.display_config_.get_all_display_configuration()
        self.assertNotEqual(all_config.numberOfDisplays, 0, "FAIL : Failed to Get All Display Configuration")
        logging.info("PASS : Get ALL Display Configuration : {}".format(all_config.to_string(self.enum_info)))
        logging.info("*******get_current_display_configuration_ex() ***********************")
        topology, connector_port, display_and_adapter_info_list = self.display_config_.get_current_display_configuration_ex(
            self.enum_info)
        self.assertNotEqual(topology, 'TOPOLOGY_NONE', "FAIL : Failed to Get Current Display Configuration")
        port_list = []
        for count in range(len(connector_port)):
            port_list.append(
                connector_port[count] + ':' + str(display_and_adapter_info_list[count].adapterInfo.gfxIndex))
        logging.info("PASS : Current Display Configuration Topology : {0}, Connector_Port's : {1}".format(topology,
                                                                                                          port_list))
        logging.info("******************** TEST_2: END ************************************\n")

    ##
    # Getting All Supported Modes
    def test_0_3(self):
        logging.info("******************** TEST_3: START **********************************")
        logging.info("************** get_all_supported_modes() ****************************")
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        if enumerated_displays.Count > 1:
            status = self.set_configuration_and_apply(enumerated_displays)
            self.assertTrue(status, "FAIL : Failed to Apply Set Display Configuration Ex for Extended Topology")
        for display_adapter_info in self.display_and_adapter_info_list:
            available_modes = self.display_config_.get_all_supported_modes([display_adapter_info], sorting_flag=True)
            self.assertNotEqual(len(available_modes), 0, "FAIL : Failed to Get All Supported Modes")
            logging.info(
                "PASS : All Supported Modes for : [{0}][{1}]".format(display_adapter_info.adapterInfo.gfxIndex,
                                                                     display_adapter_info.TargetID))
            for key, values in available_modes.items():
                for mode in values:
                    logging.info("  Supported Modes : {}".format(mode.to_string(enumerated_displays)))
        logging.info("******************** TEST_3: END ************************************\n")

    ##
    # Set Extended configuration before applying modes.
    def set_configuration_and_apply(self, enumerated_displays):
        topology, connector_port, display_and_adapter_info_list = self.display_config_.get_current_display_configuration_ex(
            enumerated_displays)
        if topology != 'EXTENDED':
            status = self.display_config_.set_display_configuration_ex(enum.EXTENDED,
                                                                       self.display_and_adapter_info_list)
            return status
        else:
            return True

    ##
    # Verifying Set Display mode (Min,Max,Medium)
    def test_0_4(self):
        logging.info("******************** TEST_4: START **********************************")
        logging.info("****************** set_display_mode *********************************")
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        if enumerated_displays.Count > 1:
            status = self.set_configuration_and_apply(enumerated_displays)
            self.assertTrue(status, "FAIL : Failed to Apply Set Display Configuration Ex for Extended Topology")
        for display_and_adapter_info in self.display_and_adapter_info_list:
            available_modes = self.display_config_.get_all_supported_modes([display_and_adapter_info],
                                                                           sorting_flag=True)
            modes = []
            for key, values in available_modes.items():
                noOfModes = len(values)
                for index in range(len(values)):
                    if values[noOfModes - 1].HzRes == values[index].HzRes and \
                            values[noOfModes - 1].VtRes == values[index].VtRes and \
                            values[noOfModes - 1].refreshRate == values[index].refreshRate:
                        modes.append(values[index])
                for mode in modes:
                    logging.info("Applying Mode : {}".format(mode.to_string(enumerated_displays)))
                    status = self.display_config_.set_display_mode([mode])
                    if status:
                        logging.info("Successfully Applied Mode : {} x {} @ {} {}".
                                     format(mode.HzRes, mode.VtRes, mode.refreshRate,
                                            (cfg_enum.ScanlineOrdering(mode.scanlineOrdering)).name))
                        get_current_mode = self.display_config_.get_current_mode(display_and_adapter_info)
                        if (mode == get_current_mode) is True:
                            logging.info("PASS : Successfully Verified applied display mode {} for Target ID {}".format(
                                mode.to_string(enumerated_displays), display_and_adapter_info.TargetID))
                    else:
                        self.fail("FAIL : Unable to apply display mode {} for Target ID {}".format(
                            mode.to_string(enumerated_displays), display_and_adapter_info.TargetID))

        logging.info("******************** TEST_4: END ************************************\n")

    ##
    # Getting Current Mode and Display Timings
    def test_0_5(self):
        logging.info("******************** TEST_5: START **********************************")
        logging.info("********** get_current_mode() &  get_display_timings() **************")
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        for display_and_adapter_info in self.display_and_adapter_info_list:
            logging.info("************ get_current_mode() Verification ************************")
            try:
                current_mode = self.display_config_.get_current_mode(display_and_adapter_info)
                logging.info(
                    "Pass: Get Current Mode for : [{0},{1}]".format(display_and_adapter_info.adapterInfo.gfxIndex,
                                                                    display_and_adapter_info.TargetID))
                logging.info("  Target ID           : {}".format(current_mode.targetId))
                logging.info("  HzRes               : {}".format(current_mode.HzRes))
                logging.info("  VtRes               : {}".format(current_mode.VtRes))
                logging.info("  Rotation            : {}".format((cfg_enum.Rotation(current_mode.rotation)).name))
                logging.info("  RefreshRate         : {}".format(current_mode.refreshRate))
                logging.info("  BPP                 : {}".format((cfg_enum.PixelFormat(current_mode.BPP)).name))
                logging.info(
                    "  ScanlineOrdering    : {}".format(
                        (cfg_enum.ScanlineOrdering(current_mode.scanlineOrdering)).name))
                logging.info("  Scaling             : {}".format((cfg_enum.Scaling(current_mode.scaling)).name))
                logging.info("  PixelClock          : {} Hz".format(current_mode.pixelClock_Hz))
                logging.info(
                    "  Status              : {}".format(cfg_enum.DisplayConfigErrorCode(current_mode.status).name))

                if current_mode.targetId == display_and_adapter_info.TargetID:
                    logging.info("Current Mode : {}".format(current_mode.to_string(enumerated_displays)))
                else:
                    self.fail(
                        "Fail: Unable to get Current Mode for Target ID {}".format(display_and_adapter_info.TargetID))

            except Exception as ex:
                logging.error("Exception Msg: {}".format(ex))

            logging.info("***************** END : get_current_mode() Verification**************")
            logging.info("************ get_display_timings() Verification *********************")
            try:
                display_timings = self.display_config_.get_display_timings(display_and_adapter_info)
                if display_timings.status is enum.DISPLAY_CONFIG_SUCCESS:
                    logging.info("Pass: Get Display Timings for : [{0},{1}]".format(
                        display_and_adapter_info.adapterInfo.gfxIndex, display_and_adapter_info.TargetID))
                    logging.info("  Target ID           : {}".format(display_timings.targetId))
                    logging.info("  hActive             : {}".format(display_timings.hActive))
                    logging.info("  vActive             : {}".format(display_timings.vActive))
                    logging.info("  hSyncDenominator    : {}".format(display_timings.hSyncDenominator))
                    logging.info("  targetPixelRate     : {}".format(display_timings.targetPixelRate))
                    logging.info("  hTotal              : {}".format(display_timings.hTotal))
                    logging.info("  vTotal              : {}".format(display_timings.vTotal))
                    logging.info("  vSyncNumerator      : {}".format(display_timings.vSyncNumerator))
                    logging.info("  vSyncDenominator    : {}".format(display_timings.vSyncDenominator))
                    logging.info("  isPrefferedMode     : {}".format(display_timings.isPrefferedMode))
                    logging.info(
                        "  status              : {}".format(
                            cfg_enum.DisplayConfigErrorCode(display_timings.status).name))
                else:
                    self.fail("Fail: Get Display Timings for Target ID {}".format(display_and_adapter_info.TargetID))
            except Exception as ex:
                logging.error("Exception Msg: {}".format(ex))
            logging.info("************** END : get_display_timings() Verification *************")
        logging.info("******************** TEST_5: END ************************************\n")

    ##
    # Getting Target IDs of respective ports
    # This test only for to verify the API is working or not. Not for MultiAdapter Support
    def test_0_6(self):
        logging.info("******************** TEST_6: START **********************************")
        logging.info("******************* get_target_id() *********************************")
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        for key, value in self.display_dict.items():
            for port in value:
                logging.info("INFO : Get Target ID for : [{}]".format(port))
                target_id_value = self.display_config_.get_target_id(port, enumerated_displays)
                self.assertNotEqual(target_id_value, 0, "FAIL: Failed to Get Target ID for {}".format(port))
                logging.info("PASS : {0} Target ID is: [{1}]".format(port, target_id_value))
        logging.info("******************** TEST_6: END ************************************\n")

    ##
    # Query Display Configuration
    def test_0_7(self):
        logging.info("******************** TEST_7: START **********************************")
        logging.info("************ query_display_config() Verification ********************")
        for display_adapter_info in self.display_and_adapter_info_list:
            query_disp_config = self.display_config_.query_display_config(display_adapter_info)
            self.assertNotEqual(query_disp_config.targetId, 0,
                                "FAIL: Failed to Get Query Display Configuration for : [{0},{1}]".format(
                                    display_adapter_info.adapterInfo.gfxIndex, display_adapter_info.TargetID))
            logging.info(
                "PASS : Query Display Configuration for : [{0},{1}]".format(display_adapter_info.adapterInfo.gfxIndex,
                                                                            display_adapter_info.TargetID))
            logging.info("  TargetId    : {}".format(query_disp_config.targetId))
            logging.info("  QdcFlag     : {}".format(query_disp_config.qdcFlag))
            logging.info("  Topology    : {}".format(query_disp_config.topologyId))
            logging.info("**Path Info**")
            logging.info("      AdapterId LowPart                       : {}".format(
                query_disp_config.pathInfo.sourceInfo.adapterId.LowPart))
            logging.info("      AdapterId HighPart                      : {}".format(
                query_disp_config.pathInfo.sourceInfo.adapterId.HighPart))
            logging.info(
                "      PathInfo Id                             : {}".format(query_disp_config.pathInfo.sourceInfo.id))
            logging.info("      ModeInfoIdx                             : {}".format(
                query_disp_config.pathInfo.sourceInfo.dummyUnion.modeInfoIdx))
            logging.info("      CloneGroupId                            : {}".format(
                query_disp_config.pathInfo.sourceInfo.dummyUnion.dummyStruct.cloneGroupId))
            logging.info("      SourceModeInfoIdx                       : {}".format(
                query_disp_config.pathInfo.sourceInfo.dummyUnion.dummyStruct.sourceModeInfoIdx))
            logging.info("      StatusFlags                             : {}".format(
                query_disp_config.pathInfo.sourceInfo.statusFlags))
            logging.info("**TargetMode Info**")
            logging.info("      PixelRate                               : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.pixelRate))
            logging.info("      HSyncFreq Numerator                     : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.hSyncFreq.Numerator))
            logging.info("      HSyncFreq Denominator                   : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.hSyncFreq.Denominator))
            logging.info("      VSyncFreq Numerator                     : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.vSyncFreq.Numerator))
            logging.info("      VSyncFreq Denominator                   : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.vSyncFreq.Denominator))
            logging.info("      ActiveSize cx                           : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.activeSize.cx))
            logging.info("      ActiveSize cy                           : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.activeSize.cy))
            logging.info("      TotalSize cx                            : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.totalSize.cx))
            logging.info("      TotalSize cy                            : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.totalSize.cy))
            logging.info("      videoStandard                           : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.videoStandard.videoStandard))
            logging.info("      AdditionalSignalInfo videoStandard      : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.videoStandard.AdditionalSignalInfo.videoStandard))
            logging.info("      AdditionalSignalInfo vSyncFreqDivider   : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.videoStandard.AdditionalSignalInfo.vSyncFreqDivider))
            logging.info("      AdditionalSignalInfo reserved           : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.videoStandard.AdditionalSignalInfo.reserved))
            logging.info("      ScanLineOrdering                        : {}".format(
                query_disp_config.targetModeInfo.targetVideoSignalInfo.scanlineOrdering))
            logging.info("**SourceMode Info**")
            logging.info(
                "      Width                                   : {}".format(query_disp_config.sourceModeInfo.width))
            logging.info(
                "      Height                                  : {}".format(query_disp_config.sourceModeInfo.height))
            logging.info("      PixelFormat                             : {}".format(
                query_disp_config.sourceModeInfo.pixelFormat))
            logging.info("      Position X                              : {}".format(
                query_disp_config.sourceModeInfo.position.x))
            logging.info("      Position Y                              : {}".format(
                query_disp_config.sourceModeInfo.position.y))
            logging.info("**DesktopImage Info**")
            logging.info("      PathSourceSize X                        : {}".format(
                query_disp_config.desktopImageInfo.PathSourceSize.x))
            logging.info("      PathSourceSize Y                        : {}".format(
                query_disp_config.desktopImageInfo.PathSourceSize.y))
            logging.info("      DesktopImageRegion left                 : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageRegion.left))
            logging.info("      DesktopImageRegion top                  : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageRegion.top))
            logging.info("      DesktopImageRegion right                : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageRegion.right))
            logging.info("      DesktopImageRegion bottom               : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageRegion.bottom))
            logging.info("      DesktopImageClip left                   : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageClip.left))
            logging.info("      DesktopImageClip top                    : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageClip.top))
            logging.info("      DesktopImageClip right                  : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageClip.right))
            logging.info("      DesktopImageClip bottom                 : {}".format(
                query_disp_config.desktopImageInfo.DesktopImageClip.bottom))
            logging.info("INFO : Query Display Configuration Status     : {}".format(query_disp_config.status))
        logging.info("******************** TEST_7: END ************************************\n")

    ##
    # Getting Active Display Configuration
    def test_0_8(self):
        logging.info("******************** TEST_8: START **********************************")
        logging.info("*********** get_active_display_configuration() **********************")
        active_disp_config = self.display_config_.get_active_display_configuration()
        self.assertEqual(active_disp_config.status, 0, "FAIL: Failed to Get Active Display Configuration")
        logging.info("PASS : Get Active Display Configuration")
        logging.info("Size              : {}".format(active_disp_config.size))
        logging.info("Topology          : {}".format(cfg_enum.DisplayConfigTopology(active_disp_config.topology).name))
        logging.info("NumberOfDisplays  : {}".format(active_disp_config.numberOfDisplays))
        for each_display in range(0, len(self.display_and_adapter_info_list)):
            logging.info("INFO : Active Display - {}".format(each_display + 1))
            logging.info(
                "  TargetId                  : {}".format(active_disp_config.displayInfo[each_display].targetId))
            logging.info(
                "  SourceId                  : {}".format(active_disp_config.displayInfo[each_display].sourceId))
            logging.info(
                "  PathIndex                 : {}".format(active_disp_config.displayInfo[each_display].pathIndex))
            logging.info(
                "  CloneGroupCount           : {}".format(active_disp_config.displayInfo[each_display].cloneGroupCount))
            logging.info("  ExtendedGroupCount        : {}".format(
                active_disp_config.displayInfo[each_display].extendedGroupCount))
            for clone_num in range(0, active_disp_config.displayInfo[each_display].cloneGroupCount):
                logging.info("  CloneGroupTargetIds     : {}".format(
                    active_disp_config.displayInfo[each_display].cloneGroupTargetIds[clone_num]))
            for extended_num in range(0, active_disp_config.displayInfo[each_display].extendedGroupCount):
                logging.info("  ExtendedGroupTargetIds  : {}".format(
                    active_disp_config.displayInfo[each_display].extendedGroupTargetIds[extended_num]))
        logging.info("INFO : Get Active Display Configuration Status: {}".format(
            (cfg_enum.DisplayConfigErrorCode(active_disp_config.status)).name))
        logging.info("******************** TEST_8: END ************************************\n")

    ##
    # Getting All Gfx Adapter Details
    def test_0_9(self):
        logging.info("******************** TEST_9: START **********************************")
        logging.info("************ get_all_gfx_adapter_details() **************************")
        gfx_adapter_details = self.display_config_.get_all_gfx_adapter_details()
        self.assertEqual(gfx_adapter_details.status, 0, "FAIL: Failed to Get All Gfx Adapter Details")
        logging.info("PASS : Get All Gfx Adapter Details")
        logging.info("Get All Gfx Adapter Details NumDisplayAdapter: {}".format(gfx_adapter_details.numDisplayAdapter))
        for each_adapter in range(gfx_adapter_details.numDisplayAdapter):
            logging.info("INFO : Gfx Adapter Info - {}".format(each_adapter + 1))
            logging.info(
                "          busDeviceID         : {}".format(gfx_adapter_details.adapterInfo[each_adapter].busDeviceID))
            logging.info(
                "          vendorID            : {}".format(gfx_adapter_details.adapterInfo[each_adapter].vendorID))
            logging.info(
                "          deviceID            : {}".format(gfx_adapter_details.adapterInfo[each_adapter].deviceID))
            logging.info("          deviceInstanceID    : {}".format(
                gfx_adapter_details.adapterInfo[each_adapter].deviceInstanceID))
            logging.info(
                "          gfxIndex            : {}".format(gfx_adapter_details.adapterInfo[each_adapter].gfxIndex))
            logging.info(
                "          isActive            : {}".format(gfx_adapter_details.adapterInfo[each_adapter].isActive))
        logging.info("INFO : Get All Gfx Adapter Details Status: {}".format(gfx_adapter_details.status))
        logging.info("******************** TEST_9: END ************************************\n")

    ##
    # Getting Native Mode
    def test_1_0(self):
        logging.info("******************** TEST_10: START *********************************")
        logging.info("******************* get_native_mode() *******************************")
        for display_adapter_info in self.display_and_adapter_info_list:
            logging.info("Get Native Mode for : [{0},{1}]".format(display_adapter_info.adapterInfo.gfxIndex,
                                                                  display_adapter_info.TargetID))
            native_mode = self.display_config_.get_native_mode(display_adapter_info)
            self.assertIsNotNone(native_mode, "FAIL: Get Native mode : {} FAILED".format(display_adapter_info.TargetID))
            logging.info("PASS : Get Native mode [{0}] is : {1}".format(display_adapter_info.TargetID, native_mode))
        logging.info("******************** TEST_10: END ***********************************\n")

    ##
    # Getting Internal Display List
    def test_1_1(self):
        logging.info("******************** TEST_11: START *********************************")
        logging.info("************** get_internal_display_list() **************************")
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        display_list = self.display_config_.get_internal_display_list(enumerated_displays)
        self.assertNotEqual(len(display_list), 0, "FAIL: Get Internal Display List FAILED")
        logging.info("PASS : Get Internal Display List : {0}".format(display_list))
        logging.info("******************** TEST_11: END ***********************************\n")

    ##
    # Getting Display and Adapter Info of respective Target IDs
    def test_1_2(self):
        logging.info("******************** TEST_12: START *********************************")
        logging.info("************* get_display_and_adapter_info() ************************")
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        for count in range(enumerated_displays.Count):
            logging.info("Get Display and Adapter Info for TargetID : {}".format(
                enumerated_displays.ConnectedDisplays[count].TargetID))
            display_and_adapter_info = self.display_config_.get_display_and_adapter_info(
                enumerated_displays.ConnectedDisplays[count].TargetID)
            if display_and_adapter_info is not None:
                logging.info("PASS: Display and Adapter Info : [{}]".format(
                    enumerated_displays.ConnectedDisplays[count].TargetID))
                logging.info("      Source ID           : {}".format(display_and_adapter_info.SourceID))
                logging.info("      Target ID           : {}".format(display_and_adapter_info.TargetID))
                logging.info("      BusDeviceID         : {}".format(display_and_adapter_info.adapterInfo.busDeviceID))
                logging.info("      VendorID            : {}".format(display_and_adapter_info.adapterInfo.vendorID))
                logging.info("      DeviceID            : {}".format(display_and_adapter_info.adapterInfo.deviceID))
                logging.info(
                    "      DeviceInstanceID    : {}".format(display_and_adapter_info.adapterInfo.deviceInstanceID))
                logging.info("      GfxIndex            : {}".format(display_and_adapter_info.adapterInfo.gfxIndex))
                logging.info("      isActive            : {}".format(display_and_adapter_info.adapterInfo.isActive))
            else:
                self.fail("FAIL : Get Display and Adapter Info : {}".format(
                    enumerated_displays.ConnectedDisplays[count].TargetID))
        logging.info("******************** TEST_12: END ***********************************\n")

    ##
    # Getting Display is Attached or not of respective ports
    def test_1_3(self):
        logging.info("******************** TEST_13: START *********************************")
        logging.info("***************** is_display_attached() *****************************")
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        for key, value in self.display_dict.items():
            for port in value:
                logging.info("Check is Display attached in this Port : [{0}] and GfxIndex : [{1}]".format(port, key))
                status = display_config.is_display_attached(enumerated_displays, port, str(key).lower())
                if status:
                    logging.info("PASS : [{0},{1}] Display is Attached".format(key, port))
                else:
                    self.fail("FAIL : [{0},{1}] Display is NOT Attached".format(key, port))
        logging.info("******************** TEST_13: END ***********************************\n")

    ##
    # Getting Display is Active or Not of respective ports
    def test_1_4(self):
        logging.info("******************** TEST_14: START *********************************")
        logging.info("****************** is_display_active() ******************************")
        for key, value in self.display_dict.items():
            for port in value:
                logging.info("Check is Display Active in this Port : [{0}] and GfxIndex : [{1}]".format(port, key))
                status = display_config.is_display_active(port, str(key).lower())
                self.assertIsNotNone(status,
                                     "FAIL : Failed to Get Display Active/Inactive for [{0},{1}]".format(key, port))
                if status:
                    logging.info("PASS : [{0},{1}] Display is Active".format(key, port))
                else:
                    logging.info("PASS : [{0},{1}] Display is InActive".format(key, port))
        logging.info("******************** TEST_14: END ***********************************\n")

    ##
    # Getting Supported Ports and Free Ports of respective Adapter
    def test_1_5(self):
        logging.info("******************** TEST_15: START *********************************")
        logging.info("******** get_supported_ports() & get_free_ports() *******************")
        gfx_adapter_details = self.display_config_.get_all_gfx_adapter_details()
        for each_adapter in range(gfx_adapter_details.numDisplayAdapter):
            temp_supported_port_list = []
            logging.info(
                "INFO : Get Supported Ports for : {}".format(gfx_adapter_details.adapterInfo[each_adapter].gfxIndex))
            supported_ports = display_config.get_supported_ports(
                str(gfx_adapter_details.adapterInfo[each_adapter].gfxIndex))
            for key, value in supported_ports.items():
                temp_supported_port_list.append(key + '_' + value)
            self.assertIsNotNone(supported_ports, "FAIL : Failed to Get Supported Ports for {}".format(
                gfx_adapter_details.adapterInfo[each_adapter].gfxIndex))
            logging.info("PASS : [{0}] Supported Ports are  : {1}".format(
                gfx_adapter_details.adapterInfo[each_adapter].gfxIndex, temp_supported_port_list))

            logging.info(
                "INFO : Get Free Ports for : {}".format(gfx_adapter_details.adapterInfo[each_adapter].gfxIndex))
            free_ports = display_config.get_free_ports(str(gfx_adapter_details.adapterInfo[each_adapter].gfxIndex))
            self.assertIsNotNone(free_ports, "FAIL : Failed to Get Free Ports for {}".format(
                gfx_adapter_details.adapterInfo[each_adapter].gfxIndex))
            logging.info(
                "PASS : [{0}] Free Ports are       :{1}".format(gfx_adapter_details.adapterInfo[each_adapter].gfxIndex,
                                                                free_ports))

        logging.info("******************** TEST_15: END ***********************************\n")

    ##
    # qdc OS API return
    def test_1_6(self):
        logging.info("******************** TEST_16: START *********************************")
        logging.info("***************** query_display_config_os() *************************")
        ret_status, path_info_arr, mode_info_arr, topology_id = self.display_config_.query_display_configuration_os(
            cfg_enum.QdcFlag.QDC_ONLY_ACTIVE_PATHS | cfg_enum.QdcFlag.QDC_VIRTUAL_MODE_AWARE)
        logging.info(f"Return status = {ret_status} Topology ID = {topology_id}")

        logging.info(f"Path Info Length = {len(path_info_arr)}")
        for path_info in list(path_info_arr):
            logging.info(f"Path Info: {path_info.__str__()}")

        logging.info(f"Mode Info Length = {len(mode_info_arr)}")
        for mode_info in list(mode_info_arr):
            logging.info(f"Mode Info: {mode_info.__str__()}")
        if ret_status is not True:
            self.fail("Failed to get QDC data!")

        logging.info("******************** TEST_16: END ***********************************\n")

    ##
    # Cleanup, Clearing CCD Database
    def test_1_7(self):
        logging.info("******************** TEST_17: START *********************************")
        logging.info("************* cleanup() & clear_ccd_database() **********************")
        logging.info("Clear the Memory Allocation in DisplayConfig DLL")
        self.display_config_.cleanup()
        logging.info("INFO : Cleanup done in DisplayConfig DLL ")
        logging.info("Clearing saved configuration and Connectivity database")
        status = self.display_config_.clear_ccd_database()
        logging.info("INFO : Clear ccd database : {}".format(status))
        logging.info("******************** TEST_16: END ***********************************\n")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
