########################################################################################################################
# @file     display_config.py
# @brief    Python Wrapper exposes interfaces for Display Config
# @author   Amit Sau, Raghupathy
########################################################################################################################


import copy
import ctypes
import logging
import os
from operator import attrgetter
from typing import Union, List, Tuple, Optional

from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper.control_api_args import ctl_genlock_target_mode_list_t
from Libs.Core import enum
from Libs.Core import system_utility as utility
from Libs.Core.Verifier.dispdiag_verification import verify_dispdiagnonintrusivedata
from Libs.Core.core_base import singleton
from Libs.Core.display_config import display_config_enums as cfg_enum, adapter_info_struct
from Libs.Core.display_config import display_config_struct as cfg_struct
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import state_machine_manager
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import control_api_args, os_interfaces as os_interfaces_dll


##
# @brief        Contains enums which are used for displayconfig feature
# @details      Display configuration API's supports below functionality.
#               GetDisplayConfigInterfaceVersion
#                   Get API interface version.
#               GetAllDisplayConfiguration
#                   Get display configuration which includes both active and inactive displays.
#               GetCurrentDisplayConfiguration
#                   Get display configuration which includes only active displays.
#               SetDisplayConfiguration
#                   Set display configuration (SINGLE, CLONE, EXTENDED).
#               GetAllSupportedModes
#                   Get all supported modes for specified DisplayAndAdapterInfo which are active.
#               GetCurrentMode
#                   Get current display mode for specified DisplayAndAdapterInfo which is active.
#               SetDisplayMode
#                   Set display mode for specified DisplayAndAdapterInfo.
@singleton
class DisplayConfiguration(object):
    list_ctypes = []
    structureenum_dict = {'topology': 'DisplayConfigTopology', 'ConnectorNPortType': 'CONNECTOR_PORT_TYPE',
                          'BPP': 'PixelFormat', 'rotation': 'Rotation', 'scaling': 'Scaling',
                          'scanlineOrdering': 'ScanlineOrdering'}

    ##
    # @brief        Display Configuration constructor.
    def __init__(self):
        ##
        # Load DisplayConfig C library
        os_interfaces_dll.load_library()

    ##
    # @brief        Get API interface version.
    # @return       version - interface version of type INT
    def get_display_config_interface_version(self):
        version = os_interfaces_dll.get_display_config_interface_version()
        return version

    ##
    # @brief        Get display configuration which includes both active and inactive displays
    # @return       get_config - display config object of type DisplayConfig
    def get_all_display_configuration(self):
        get_config = os_interfaces_dll.get_all_display_configuration()
        return get_config

    ##
    # @brief        Get display configuration which includes only active displays
    # @return       current_display_config - object of type DisplayConfig
    def get_current_display_configuration(self):
        all_display_config = self.get_all_display_configuration()
        current_display_config = cfg_struct.DisplayConfig()
        current_display_config.size = all_display_config.size
        current_display_config.topology = all_display_config.topology
        current_display_config.status = all_display_config.status
        for path in all_display_config.displayPathInfo:
            if path.isActive:
                current_display_config.displayPathInfo[current_display_config.numberOfDisplays] = path
                current_display_config.numberOfDisplays += 1
        return current_display_config

    ##
    # @brief        Get Current display configuration
    # @param[in]    enumerated_displays - Object of type EnumeratedDisplaysEx
    # @return       (, config_str, display_and_adapter_info_list) - Current display configuration in
    #               (String Of DisplayConfigTopology, [CONNECTOR_PORT_TYPE], [DisplayAndAdapterInfo]).
    def get_current_display_configuration_ex(self, enumerated_displays=None):
        if enumerated_displays is None:
            enumerated_displays = self.get_enumerated_display_info()
            if enumerated_displays is None:
                logging.error("enumerated_displays is None")
                # Gdhm handled in get_enumerated_display_info()
                return None, None, None

        # Getting current configuration
        get_cfg = self.get_current_display_configuration()
        config_str = []
        display_and_adapter_info_list = []
        if get_cfg.status == enum.DISPLAY_CONFIG_SUCCESS:
            for display_index in range(get_cfg.numberOfDisplays):
                for eachDisplay in range(enumerated_displays.Count):
                    display_info = enumerated_displays.ConnectedDisplays[eachDisplay]
                    if get_cfg.displayPathInfo[display_index].targetId == display_info.TargetID and \
                            get_cfg.displayPathInfo[display_index].displayAndAdapterInfo.adapterInfo.busDeviceID == \
                            display_info.DisplayAndAdapterInfo.adapterInfo.busDeviceID and \
                            get_cfg.displayPathInfo[display_index].displayAndAdapterInfo.adapterInfo.deviceInstanceID \
                            == display_info.DisplayAndAdapterInfo.adapterInfo.deviceInstanceID:
                        config_str.append((cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType)).name)
                        display_and_adapter_info_list.append(display_info.DisplayAndAdapterInfo)
        return (cfg_enum.DisplayConfigTopology(get_cfg.topology)).name, config_str, display_and_adapter_info_list

    ##
    # @brief        Set display configuration (SINGLE, CLONE, EXTENDED)
    # @param[in]    config - display config object of type DisplayConfig
    # @param[in]    add_force_mode_enum_flag - Optional flag to set to True if need to flag as part of SDC else False
    # @return       None
    def set_display_configuration(self, config, add_force_mode_enum_flag: bool = False):
        config_status = os_interfaces_dll.set_display_configuration(config, add_force_mode_enum_flag)
        # Report GDHM bug if Set Display Config failed
        if config_status != enum.DISPLAY_CONFIG_SUCCESS:
            logging.warning("SetDisplayConfiguration API failed with error code {0}".
                            format(cfg_enum.DisplayConfigErrorCode(config_status).name))
            gdhm.report_bug(
                f"[DisplayConfigLib] Failed to set display configuration with error "
                f"code {cfg_enum.DisplayConfigErrorCode(config_status).name}", gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES)
            return

        gfx_index_list = []
        logging.info("Display Diagnostics Verification post Set Display Configuration")
        for numdisplay in range(0, config.numberOfDisplays):
            gfx_index = config.displayPathInfo[numdisplay].displayAndAdapterInfo.adapterInfo.gfxIndex
            if gfx_index not in gfx_index_list:
                gfx_index_list.append(gfx_index)

        for gfx_index in gfx_index_list:
            verify_dispdiagnonintrusivedata(gfx_index)

    ##
    # @brief        Set display configuration (SINGLE, CLONE, EXTENDED)
    # @param[in]    topology - display topology of type DisplayConfigTopology
    # @param[in]    display_and_adapter_info_list - connector_port_list of type CONNECTOR_PORT_TYPE/
    #               display_and_adapter_info_list of type DisplayAndAdapterInfo
    # @param[in]    enumerated_displays - Object of type EnumeratedDisplaysEx
    # @return       status - False if enumerated Display is Not found else True.
    def set_display_configuration_ex(self, topology, display_and_adapter_info_list, enumerated_displays=None):
        # WA : getting new enumerated display info
        enumerated_displays = self.get_enumerated_display_info()
        if enumerated_displays is None:
            logging.error("enumerated_displays is None")
            # Gdhm handled in get_enumerated_display_info()
            return False
        logging.info(f"Enumerated displays: {enumerated_displays.to_string()}")

        ##
        # Prepare display configuration object
        set_config = cfg_struct.DisplayConfig()
        set_config.topology = topology
        path = 0
        # Checking whether it's a TargetID List or DisplayAndAdapterInfo List
        if type(display_and_adapter_info_list[0]) is cfg_struct.DisplayAndAdapterInfo:
            for each_display_and_adapter_info in display_and_adapter_info_list:
                set_config.displayPathInfo[path].targetId = each_display_and_adapter_info.TargetID
                set_config.displayPathInfo[path].displayAndAdapterInfo = each_display_and_adapter_info
                path += 1
        else:
            for each_port in range(len(display_and_adapter_info_list)):
                for each_display in range(enumerated_displays.Count):
                    display_info = enumerated_displays.ConnectedDisplays[each_display]
                    if display_and_adapter_info_list[each_port] == cfg_enum.CONNECTOR_PORT_TYPE(
                            display_info.ConnectorNPortType).name:
                        set_config.displayPathInfo[path].targetId = display_info.TargetID
                        set_config.displayPathInfo[path].displayAndAdapterInfo = display_info.DisplayAndAdapterInfo
                        break
                path += 1
        set_config.numberOfDisplays = len(display_and_adapter_info_list)

        ##
        # Apply display configuration
        self.set_display_configuration(set_config)

        ##
        # Getting current configuration
        get_config = self.get_current_display_configuration()

        if get_config.equals(set_config):
            logging.info("Successfully applied display configuration: {0}"
                         .format(set_config.to_string(enumerated_displays)))
            state_machine_manager.StateMachine().update_adapter_display_context()
            status = True
        else:
            gdhm.report_bug(
                title="[DisplayConfigLib] Failed to apply config as Current Config : {0}, Expected Config:"
                      " {1} are different".format(get_config.to_string(enumerated_displays), set_config.to_string(
                    enumerated_displays)),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Failed to apply display configuration. Current Config : {0} Expected Config : {1}"
                          .format(get_config.to_string(enumerated_displays), set_config.to_string(enumerated_displays)))
            status = False
        return status

    ##
    # @brief        Get all supported modes for specified target ids which are active
    # @param[in]    display_and_adapter_info_list - List of active target ids / displayAndAdapterInfo Structure
    # @param[in]    pruned_mode_list - Optional flag to specify pruning mode list.
    #                       False:Query all supported mode list.
    #                       True: Pruning all supported mode list less than 10x7
    # @param[in]    rotation_flag - Optional flag to specify whether Rotation Modes to be added or not.
    # @param[in]    sorting_flag - Optional flag to specify whether to sort modes based on X,Y and RR.
    # @return       supported_mode_dict - Supported mode list dictionary where
    #                       key = targetId, value = list of supported modes
    def get_all_supported_modes(self, display_and_adapter_info_list, pruned_mode_list=True, rotation_flag=False,
                                sorting_flag=False):
        display_and_adapter_info = []
        adapter_list = []
        if type(display_and_adapter_info_list[0]) is not cfg_struct.DisplayAndAdapterInfo:
            for target_id in display_and_adapter_info_list:
                display_and_adapter_info.append(self.get_display_and_adapter_info(target_id))
                display_and_adapter_info_list = display_and_adapter_info

        supported_mode_dict = {}
        enumerated_displays = self.get_enumerated_display_info()
        for display in range(enumerated_displays.Count):
            adapter_list.append(
                enumerated_displays.ConnectedDisplays[display].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
        adapter_set = set(adapter_list)

        for each_display_and_adapter_info in display_and_adapter_info_list:
            for display_index in range(enumerated_displays.Count):
                each_display = enumerated_displays.ConnectedDisplays[display_index]
                if each_display_and_adapter_info.TargetID == each_display.DisplayAndAdapterInfo.TargetID and \
                        each_display_and_adapter_info.adapterInfo.gfxIndex == each_display.DisplayAndAdapterInfo.adapterInfo.gfxIndex and \
                        each_display.IsActive is True:
                    enumerated_modes = os_interfaces_dll.get_all_supported_modes(each_display_and_adapter_info,
                                                                                 rotation_flag)
                    mode_list = []
                    if enumerated_modes.status == enum.DISPLAY_CONFIG_SUCCESS:
                        for i in range(enumerated_modes.noOfSupportedModes):
                            mode = copy.deepcopy(enumerated_modes.pDisplayModes[i])
                            if pruned_mode_list:
                                if (mode.HzRes < 1024) and (mode.VtRes < 768):
                                    continue
                            mode_list.append(mode)
                            gfx_index = each_display.DisplayAndAdapterInfo.adapterInfo.gfxIndex

                    if len(adapter_set) == 1:
                        if sorting_flag is True:
                            sorted_mode_list = sorted(mode_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                            supported_mode_dict[each_display_and_adapter_info.TargetID] = list(sorted_mode_list)
                        else:
                            supported_mode_dict[each_display_and_adapter_info.TargetID] = list(mode_list)
                    elif len(adapter_set) > 1:
                        if sorting_flag is True:
                            sorted_mode_list = sorted(mode_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                            supported_mode_dict[(gfx_index, each_display_and_adapter_info.TargetID)] = list(
                                sorted_mode_list)
                        else:
                            supported_mode_dict[(gfx_index, each_display_and_adapter_info.TargetID)] = list(
                                mode_list)

        self.cleanup()
        return supported_mode_dict

    ##
    # @brief        Get current display mode
    # @param[in]    display_and_adapter_info - targetId for which current mode need to query
    # @return       mode - display mode of type DisplayMode
    def get_current_mode(self, display_and_adapter_info):
        if type(display_and_adapter_info) is not cfg_struct.DisplayAndAdapterInfo:
            display_and_adapter_info = self.get_display_and_adapter_info(display_and_adapter_info)

        mode = os_interfaces_dll.get_current_mode(display_and_adapter_info)
        enum_displays = self.get_enumerated_display_info()
        logging.info(f"Current Mode for 0x{display_and_adapter_info.TargetID:X}: {mode.to_string(enum_displays)}")

        return mode

    ##
    # @brief        Get DisplayTimings for specified Type of DisplayAndAdapterInfo (Mainline driver).
    # @details      This will make use of QDC, during CLONE mode.
    # @param[in]    display_and_adapter_info - Type of DisplayAndAdapterInfo
    # @return       display_timings - Object of type DisplayTimings.
    def get_display_timings(self, display_and_adapter_info):
        if type(display_and_adapter_info) is not cfg_struct.DisplayAndAdapterInfo:
            display_and_adapter_info = self.get_display_and_adapter_info(display_and_adapter_info)

        current_mode = self.get_current_mode(display_and_adapter_info)

        qdc_data = self.query_display_config(display_and_adapter_info)
        hz_res = qdc_data.targetModeInfo.targetVideoSignalInfo.activeSize.cx
        vt_res = qdc_data.targetModeInfo.targetVideoSignalInfo.activeSize.cy
        # If Virtual mode is applied, update current mode with desktop image size its corresponding RR.
        if (current_mode.HzRes != hz_res) or (current_mode.VtRes != vt_res):
            current_mode.HzRes = qdc_data.desktopImageInfo.PathSourceSize.x
            current_mode.VtRes = qdc_data.desktopImageInfo.PathSourceSize.y

        display_timings = os_interfaces_dll.get_display_timings(current_mode)

        # Display_timings's hActive or vActive can result 0 when clone scaling and scaling applied on
        # given display_and_adapter_info is different. So retrying with MDS.
        if display_timings.hActive == 0 or display_timings.vActive == 0:
            logging.warning(f"Get DisplayTiming returns 0 for 0x{display_and_adapter_info.TargetID:X} with "
                            f"{cfg_enum.Scaling(current_mode.scaling).name} Scaling. Retrying with MDS Scaling")
            current_mode.scaling = enum.MDS
            display_timings = os_interfaces_dll.get_display_timings(current_mode)

        logging.info(f"Display Timings for 0x{display_and_adapter_info.TargetID:X}: {display_timings.to_string()}")
        return display_timings

    ##
    # @brief        Set display mode for specified displayAndAdapterInfo
    # @param[in]    mode_list - specify display mode of type DisplayMode
    # @param[in]    virtual_mode_set_aware - flag (Set this flag as True to enable PLANE scalar else PIPE scalar)
    # @param[in]    enumerated_displays -  Object of type EnumeratedDisplaysEx
    # @param[in]    force_modeset - set to True if no optimization is required while setting display mode else False
    # @return       return_status - True, if mode(s) applied successfully; False, otherwise
    def set_display_mode(self, mode_list, virtual_mode_set_aware=True, enumerated_displays=None, force_modeset=False):
        mode_set_status = []
        if enumerated_displays is None:
            enumerated_displays = self.get_enumerated_display_info()
            if enumerated_displays is None:
                logging.error("Enumerated displays is None")
                # Gdhm handled in get_enumerated_display_info()
                return False

        for mode in mode_list:
            if mode.displayAndAdapterInfo.TargetID == 0 and mode.displayAndAdapterInfo.adapterInfo.deviceID == '' and \
                    mode.displayAndAdapterInfo.adapterInfo.deviceInstanceID == '':
                mode.displayAndAdapterInfo = self.get_display_and_adapter_info(mode.targetId)
            logging.info("Applying display mode : {0}x{1}".format(mode.HzRes, mode.VtRes))
            mode_status = os_interfaces_dll.set_display_mode(mode, virtual_mode_set_aware, force_modeset)

            # Verify if the display mode was applied successfully or not
            if mode_status != enum.DISPLAY_CONFIG_SUCCESS:
                if mode_status == enum.DISPLAY_CONFIG_ERROR_SUCCESS_RR_MISMATCH:
                    mode_set_status.append(True)
                    logging.warning('Successfully applied display modes with RR Mismatch. WA ( Fix - TBD from Driver)')
                    continue
                mode_set_status.append(False)
                gdhm.report_bug(
                    title="[DisplayConfigLib]Failed to apply display mode with error {}".format(
                        cfg_enum.DisplayConfigErrorCode(mode_status).name),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P1,
                    exposure=gdhm.Exposure.E2
                )
                logging.error('Failed to apply display mode with error %s' %
                              cfg_enum.DisplayConfigErrorCode(mode_status).name)
            else:
                mode_set_status.append(True)
                logging.info('Successfully applied display modes')

        return_status = False if False in mode_set_status else True
        return return_status

    ##
    # @brief        This class method helps to get QDC data from OS.
    # @param[in]    display_and_adapter_info - Object of Type DisplayAndAdapterInfo
    # @param[in]    qdc_flag - flag value for QDC. Default value will be used if user doesn't required any specific flag
    # @return       get_config - Object of type QueryDisplay.
    def query_display_config(self, display_and_adapter_info, qdc_flag=None):
        if type(display_and_adapter_info) is not cfg_struct.DisplayAndAdapterInfo:
            display_and_adapter_info = self.get_display_and_adapter_info(display_and_adapter_info)
        get_config = cfg_struct.QueryDisplay()
        if qdc_flag is None:
            qdc_flag = (cfg_enum.QdcFlag.QDC_DATABASE_CURRENT | cfg_enum.QdcFlag.QDC_VIRTUAL_MODE_AWARE)
        get_config = os_interfaces_dll.query_display_config(display_and_adapter_info, qdc_flag)
        return get_config

    ##
    # @brief        This method helps to interface with actual QDC call from OS API (MSFT).
    # @param[in]    qdc_flag - flag value for QDC from QdcFlag enum
    # @return       get_config - Object of type QueryDisplay.
    def query_display_configuration_os(self, qdc_flag) -> (bool, Union[None, List[cfg_struct.DisplayConfigPathInfo]],
                                                           Union[None, List[cfg_struct.DisplayConfigModeInfo]], int):
        ret_status, path_info_arr, mode_info_arr, topology_id = os_interfaces_dll.query_display_configuration_os(
            qdc_flag)
        if ret_status is False:
            gdhm.report_test_bug_os("[DisplayConfigLib] Failed to Query for Display Configuration")
        return ret_status, path_info_arr, mode_info_arr, topology_id

    ##
    # @brief        Get target ID for specified connector_port type
    # @details      This API does not support MultiAdapter - TBD: Removal After Test's are adapted to
    #               DisplayAndAdapterInfo Structure
    # @param[in]    connector_port - Object of type CONNECTOR_PORT_TYPE
    # @param[in]    enumerated_displays - Object of type EnumeratedDisplaysEx
    # @param[in]    gfx_index graphics adapter
    # @return       target_id - The Target ID mapped to current port
    def get_target_id(self, connector_port, enumerated_displays=None, gfx_index='gfx_0'):
        target_id = 0
        if enumerated_displays is None:
            enumerated_displays = self.get_enumerated_display_info()
        for each_display in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[each_display]
            if connector_port.upper() == cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name and \
                    gfx_index == display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
                target_id = display_info.DisplayAndAdapterInfo.TargetID
                break
        return target_id

    ##
    # @brief        Exposed API to get DisplayAndAdapterInfo of any given port and gfx_index
    # @param[in]    port -  String representation of CONNECTOR_PORT_TYPE
    # @param[in]    gfx_index - Graphics adapter index
    # @return       display_and_adapter_info_list - List of type DisplayAndAdapterInfo if successful, None otherwise
    def get_display_and_adapter_info_ex(self, port, gfx_index='gfx_0'):
        display_and_adapter_info_list = []

        # Validate arguments
        gfx_index = str(gfx_index.lower())
        if gfx_index is None or not gfx_index.lower().startswith('gfx_'):
            raise Exception("Invalid arguments: gfx_index= {0}".format(gfx_index))

        enumerated_displays = self.get_enumerated_display_info()
        logging.debug("Enumerated Display Info: {}".format(enumerated_displays.to_string()))

        if enumerated_displays is None:
            logging.error("Failed to get enumerated displays")
            # Gdhm handled in get_enumerated_display_info()
            return None

        for index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[index]
            adapter_info = display_info.DisplayAndAdapterInfo.adapterInfo
            if (port == str(cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name)) and \
                    (gfx_index == adapter_info.gfxIndex):
                display_info.DisplayAndAdapterInfo.ConnectorNPortType = display_info.ConnectorNPortType
                display_and_adapter_info_list.append(display_info.DisplayAndAdapterInfo)

        if len(display_and_adapter_info_list) == 1:  # SST Case
            return display_and_adapter_info_list[0]
        elif len(display_and_adapter_info_list) > 1:  # MST Case
            return display_and_adapter_info_list

        gdhm.report_bug(
            title="[DisplayConfigLib]Adapter info not found for port {0} on {1}".format(port, gfx_index),
            problem_classification=gdhm.ProblemClassification.OTHER,
            component=gdhm.Component.Test.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("Adapter info not found for port {0} on {1}".format(port, gfx_index))
        return None

    ##
    # @brief        OS Interfaces cleanup method
    # @details      In Get all supported modes we are allocating memory in C DLL (DisplayConfig.dll) for each target ID
    #               which includes mode information. User need not to deallocate memory since DisplayConfig python
    #               script takes care of memory de-allocation in C DLL.
    # @return       None
    def cleanup(self):
        os_interfaces_dll.cleanup()

    ##
    # @brief        This method helps to clear CCD database
    # @return       result - True on success else False
    @staticmethod
    def clear_ccd_database():
        ccd_database_path = "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers"
        result = True
        database_list = ['Configuration', 'Connectivity']

        for database in database_list:
            output = os.system("reg delete {0}\\{1} /f".format(ccd_database_path, database))
            if output != 0:
                logging.error("Unable to delete {0} CCD Key from {1}".format(database, ccd_database_path))
                result = False
        return result

    ##
    # @brief        This class method helps to get GetActiveDisplayConfiguration through dll.
    # @return       active_config -  Object of type ActiveDisplayConfig.
    def get_active_display_configuration(self):
        active_config = os_interfaces_dll.get_active_display_configuration()

        if active_config.status != enum.DISPLAY_CONFIG_SUCCESS:
            logging.error("Get Active Display Configuration Failed because of {0}".format(
                cfg_enum.DisplayConfigErrorCode(active_config.status).name))
            gdhm.report_bug(
                f"[DisplayConfigLib] Failed to get active display configuration with error code "
                f"{cfg_enum.DisplayConfigErrorCode(active_config.status).name}",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
        return active_config

    ##
    # @brief        This class method helps to get all Gfx Display Adapter details through dll.
    # @return       adapter_details - Object of type GfxAdapterDetails.
    def get_all_gfx_adapter_details(self):
        adapter_details = os_interfaces_dll.get_all_gfx_adapter_details()

        if adapter_details.status != enum.DISPLAY_CONFIG_SUCCESS:
            logging.error("Get Gfx Adapter Details Failed because of {0}".format(
                cfg_enum.DisplayConfigErrorCode(adapter_details.status).name))
            gdhm.report_bug(
                f"[DisplayConfigLib] Failed to get Gfx adapter details with error code "
                f"{cfg_enum.DisplayConfigErrorCode(adapter_details.status).name}",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
        else:
            # Update LUID for each adapter
            for adapter_index in range(adapter_details.numDisplayAdapter):
                adapter_details.adapterInfo[adapter_index].adapterLUID = self.get_adapter_luid(
                    adapter_details.adapterInfo[adapter_index])
        return adapter_details

    ##
    # @brief        Updates Adapter LUID for given adapter
    # @details      Note: Tests must not call this API.
    # @param[in]    adapter_info - adapter_info_struct.GfxAdapterInfo, adapter info object
    # @return       luid - Object adapter_info_struct.LUID, updated LUID data for given adapter
    def get_adapter_luid(self, adapter_info: adapter_info_struct.GfxAdapterInfo) -> adapter_info_struct.LUID:
        luid = adapter_info_struct.LUID(0, 0)  # Declare default LUID
        status, disp_adapter_caps_details = driver_interface.DriverInterface().get_all_adapter_caps()
        if status is True:
            for caps_index in range(disp_adapter_caps_details.numAdapterCaps):
                caps_info = disp_adapter_caps_details.adapterCaps[caps_index]
                # if match found from valsim adapter caps list
                if adapter_info.busDeviceID.lower().find(caps_info.busDeviceID.lower()) != -1:
                    logging.info(f"Updating current {adapter_info.gfxIndex} with LUID.")
                    luid = caps_info.adapterLUID
                    break
        else:
            logging.debug(f"Failed to get all adapter caps for {adapter_info.to_string()}")
        return luid

    ##
    # @brief        Retrieves information of connected displays, connector type, target ID, count, active status etc..,
    # @return       enum_info - Enum info object of EnumeratedDisplaysEx.
    def get_enumerated_display_info(self):
        enum_info, enum_error = os_interfaces_dll.get_enumerated_display_info()
        supported_ports_dict = {}
        for gfx_index in test_context.TestContext.get_gfx_adapter_details().keys():
            supported_ports_dict[gfx_index] = get_supported_ports(gfx_index)

        for display_count in range(0, enum_info.Count):
            displays = supported_ports_dict[
                enum_info.ConnectedDisplays[display_count].DisplayAndAdapterInfo.adapterInfo.gfxIndex]
            port_name = str(cfg_enum.CONNECTOR_PORT_TYPE(enum_info.ConnectedDisplays[display_count].ConnectorNPortType))
            for port, type in displays.items():
                if port == port_name:
                    enum_info.ConnectedDisplays[display_count].PortType = type
        if enum_info is None:
            gdhm.report_bug(
                f"[DisplayConfigLib] Failed to get enumerated display information with error code {enum_error}",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
        return enum_info

    ##
    # @brief        Retrieves information of Native Resolution and Refresh Rate in the form of
    #               XxY *at the rate symbol* RR.
    # @param[in]    display_and_adapter_info - Object of type DisplayAndAdapterInfo
    # @return       native_mode_string - The native mode String in the form XxY *at the rate Symbol*  RR.
    def get_native_mode(self, display_and_adapter_info):
        native_mode = None
        if type(display_and_adapter_info) is cfg_struct.DisplayAndAdapterInfo:
            logging.debug('DisplayAndAdapterInfo structure')
        else:
            display_and_adapter_info = self.get_display_and_adapter_info(display_and_adapter_info)

        try:
            native_mode = os_interfaces_dll.get_native_mode(display_and_adapter_info)
        except WindowsError as value:
            gdhm.report_bug(
                title="[DisplayConfigLib][WindowsError] Error in get_native_mode: {0} ".format(value.args[1]),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Error in get_native_mode: {0} ".format(value.args[1]))

        return native_mode

    ##
    # @brief        The status after Screen Capture
    # @param[in]    instance - Source Frame instance number
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    capture_args - Object of type ScreenCaptureArgs class
    # @return       status - Returns the status of Captured Screen
    def capture_screen(self, instance, gfx_index, capture_args):
        # type: (int, str, cfg_struct.ScreenCaptureArgs) -> bool
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        status = os_interfaces_dll.capture_screen(instance, adapter_info, capture_args)
        return status

    ##
    # @brief        This API returns list of internal displays (LFP)  ( both Active and Non-Active Internal Display
    #                   like eDP_A , MIPI_A , MIPI_C , eDP_B )
    # @param[in]    enumerated_displays - Object of type EnumeratedDisplaysEx
    # @return       display_list - [LFP TargetID,LFP Port Name,gfx_index]
    #               Example : [['8388688','DP_A','gfx_0'],['8388677','DP_B','gfx_0']] - Provided Dual eDP is Enabled
    #               and connected. If No internal Display Connected returns Empty List.
    #               Note : For Yangra - We use Target-ID Flag to Decide whether it is internal Display or Not
    #               For Legacy - We have currently Hard coded following Display as always internal (DP_A,MIPI_A,MIPI_C)
    def get_internal_display_list(self, enumerated_displays):
        display_list = []
        flag = False
        target_mask = cfg_struct.TARGET_ID()
        system_utility = utility.SystemUtility()
        if system_utility.is_ddrw():
            for display_index in range(enumerated_displays.Count):
                display_info = enumerated_displays.ConnectedDisplays[display_index]
                target_mask.Value = display_info.TargetID
                if target_mask.InternalDisplay:
                    display_list.append([display_info.TargetID,
                                         cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name,
                                         str(display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex)])
        else:
            internal_displays = [enum.DP_A, enum.MIPI_A, enum.MIPI_C]
            for internal_display in internal_displays:
                for display_index in range(enumerated_displays.Count):
                    display_info = enumerated_displays.ConnectedDisplays[display_index]
                    if (cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType)).name == \
                            cfg_enum.CONNECTOR_PORT_TYPE(internal_display).name:
                        display_list.append([display_info.TargetID, cfg_enum.CONNECTOR_PORT_TYPE(internal_display).name,
                                             str(display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex)])
        return display_list

    ##
    # @brief        Get Type of DisplayAndAdapterInfo for given target_ID
    # @param[in]    target_id - Target ID of panel
    # @return       display_info.DisplayAndAdapterInfo - Object of type DisplayAndAdapterInfo
    def get_display_and_adapter_info(self, target_id):
        enumerated_displays = self.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[display_index]
            if target_id == display_info.DisplayAndAdapterInfo.TargetID:
                return display_info.DisplayAndAdapterInfo

    ##
    # @brief        This API returns values of a Structure in 120 char blocks of formatted line.
    # @param[in]    struct_obj - ctypes Structure
    # @return       string_query - Formatted String
    def convert_struct_printable(self, struct_obj):
        self.list_ctypes = []
        if issubclass(type(struct_obj), ctypes.Structure) is False:
            logging.error("Wrong Input. Input parameter it's not a Structure")
            return None
        list_query = []
        list_ctypestr = ""
        for length in range(0, len(self.list_ctypes)):
            list_ctypestr += str(self.list_ctypes[length])

        value = len(list_ctypestr) / 120.0
        value1 = len(list_ctypestr) / 120
        if value - value1 > 0:
            whole = (value1 + 1) * 120
            space_append = int(whole - len(list_ctypestr))
            for temp_index in range(0, space_append):
                list_ctypestr += ' '
        temp_space = ''
        count = 0
        for item in list_ctypestr:
            temp_space += item
            count += 1
            if count == 120:
                list_query.append("{0:>112}{1:>2}".format(": ADV_DEBUG] ", temp_space))
                temp_space = ''
                count = 0
        string_query = ""
        for m in range(len(list_query)):
            string_query += "\n"
            string_query += list_query[m]
        return string_query

    ############################################################################################

    ##
    # @brief        Get display configuration which includes both active and inactive displays
    # @return       get_config - display config object of type DisplayConfig
    def get_config(self):
        get_config = os_interfaces_dll.os_wrapper_get_config()
        return get_config

    ##
    # @brief        Get display configuration which includes only active displays
    # @return       current_display_config - object of type DisplayConfig
    def get_current_config(self):
        all_display_config = self.get_config()
        current_display_config = cfg_struct.DisplayConfig()
        current_display_config.size = all_display_config.size
        current_display_config.topology = all_display_config.topology
        current_display_config.status = all_display_config.status
        for path in all_display_config.displayPathInfo:
            if path.isActive:
                current_display_config.displayPathInfo[current_display_config.numberOfDisplays] = path
                current_display_config.numberOfDisplays += 1
        return current_display_config

    ##
    # @brief        Get Current display configuration
    # @return       (Topology, config_str, display_and_adapter_info_list) - Current display configuration in
    #               (String Of DisplayConfigTopology, [CONNECTOR_PORT_TYPE], [DisplayAndAdapterInfo]).
    def get_current_config_ex(self):
        # Getting current configuration
        get_cfg = self.get_config()
        config_str = []
        display_and_adapter_info_list = []
        if get_cfg.Status == enum.DISPLAY_CONFIG_SUCCESS:
            for display_index in range(get_cfg.NumberOfDisplays):
                if get_cfg.DisplayPath[display_index].IsActive == True:
                    config_str.append(
                        (cfg_enum.CONNECTOR_PORT_TYPE(get_cfg.DisplayPath[display_index].ConnectorNPortType)).name)
                    display_and_adapter_info_list.append(get_cfg.displayPathInfo.DisplayAndAdapterInfo)
        return (cfg_enum.DisplayConfigTopology(get_cfg.Topology)).name, config_str, display_and_adapter_info_list

    ##
    # @brief        Get all supported modes for specified Panel which should be active
    # @param[in]    display_and_adapter_info - Of type DisplayAndAdapterInfo Structure
    # @param[in]    pruned_mode_list - Optional flag to specify pruning mode list.
    #                       False:Query all supported mode list.
    #                       True: Pruning all supported mode list less than 10x7
    # @param[in]    rotation_flag - flag to specify whether Rotation Modes to be added or not.
    # @return       mode_list - List[DisplayMode]
    def get_modes(self, display_and_adapter_info, pruned_mode_list, rotation_flag):
        mode_list = []
        if type(display_and_adapter_info) is not cfg_struct.DisplayAndAdapterInfo:
            logging.error(f"Please pass {display_and_adapter_info} of type DisplayAndAdapterInfo")
            return None

        enumerated_modes = os_interfaces_dll.os_wrapper_get_modes(display_and_adapter_info, rotation_flag)
        if enumerated_modes.status != enum.DISPLAY_CONFIG_SUCCESS:
            mode_set_status = False
            logging.error('Failed to get all supported modes with error %s' %
                          cfg_enum.DisplayConfigErrorCode(enumerated_modes.status).name)
        else:
            for i in range(enumerated_modes.noOfSupportedModes):
                mode = copy.deepcopy(enumerated_modes.pDisplayModes[i])
                if pruned_mode_list:
                    if (mode.HzRes < 1024) and (mode.VtRes < 768):
                        continue
                mode_list.append(mode)

            sorted_mode_list = sorted(mode_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
            mode_list = list(sorted_mode_list)

        self.cleanup()
        return mode_list

    ##
    # @brief        Get current display mode
    # @param[in]    display_and_adapter_info - PanelInfo for which current mode to be queried
    # @return       mode - display mode of type DisplayMode
    def get_mode(self, display_and_adapter_info):
        if type(display_and_adapter_info) is not cfg_struct.DisplayAndAdapterInfo:
            logging.error(f"Please pass display_and_adapter_info of type DisplayAndAdapterInfo")
            return None

        mode = os_interfaces_dll.os_wrapper_get_mode(display_and_adapter_info)
        return mode

    ##
    # @brief        Set display mode for specified displayAndAdapterInfo
    # @param[in]    display_mode - specify display mode of type DisplayMode
    # @param[in]    virtual_mode_set_aware - flag (Set this flag as True to enable PLANE scalar else PIPE scalar)
    # @param[in]    force_modeset - set to True if no optimization is required while setting display mode else False
    # @return       return_status - True, if mode is applied successfully; False, otherwise
    def set_mode(self, display_mode, virtual_mode_set_aware=True, force_modeset=False):
        mode_set_status = True

        if display_mode.displayAndAdapterInfo.TargetID == 0:
            logging.error(f"display_mode.displayAndAdapterInfo.TargetID is 0")
            return None

        logging.info("Applying display mode : {0}".format(self.convert_struct_printable(display_mode)))
        mode_status = os_interfaces_dll.os_wrapper_set_mode(display_mode, virtual_mode_set_aware, force_modeset)

        # Verify if the display mode was applied successfully or not
        if mode_status == enum.DISPLAY_CONFIG_SUCCESS:
            logging.info('Successfully applied display mode')
        elif mode_status == enum.DISPLAY_CONFIG_ERROR_SUCCESS_RR_MISMATCH:
            logging.warning('Successfully applied display modes with RR Mismatch. WA ( Fix - TBD from Driver)')
        else:
            mode_set_status = False
            logging.error('Failed to apply display mode with error %s' %
                          cfg_enum.DisplayConfigErrorCode(mode_status).name)
            gdhm.report_bug(
                title="[DisplayConfigLib]Failed to apply display mode with error {}".format(
                    cfg_enum.DisplayConfigErrorCode(mode_status).name),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )

        return mode_set_status

    ##
    # @brief        Apply higher pixel clock modes from IGCL mode table for one display
    # @details      This API is restricted to be used only for applying modes exceeding 64-bits of pixel clock data.
    #               By default, this method considers requested mode with PROGRESSIVE scanline ordering and LEGACY_RR
    #               Note: BPP and Sampling mode details are not considered to apply given display mode
    #               For applying display modes with (pixel clock <= 32-bits), continue to use set_display_mode()
    #               Note: This API is not supported for applying 64-bit modes as of now.
    #               Additional DLL side changes are required to handle higher pixel clock timings.
    #               GetDisplayHWTimingYangra() to be replaced with a new interface.
    # @param[in]    display_and_adapter_info - DisplayAndAdapterInfo structure
    # @param[in]    igcl_timing - mode object returned from IGCL
    # @param[in]    scaling - [Optional: MDS] Scaling for requested mode
    # @param[in]    rotation - [Optional: ROTATE_0] Rotation for requested mode
    # @param[in]    virtual_mode_set_aware - [Optional: True] Pass True to enable PLANE scalar, False for PIPE scalar
    # @param[in]    force_modeset - [Optional: False] Pass True for no optimization during modeset, else pass False
    # @return       mode_set_status - Returns True if modeset is successful, False otherwise
    @staticmethod
    def set_higher_pixel_clock_mode(display_and_adapter_info: cfg_struct.DisplayAndAdapterInfo,
                                    igcl_timing: control_api_args.ctl_display_timing_t, scaling: int = enum.MDS,
                                    rotation: int = enum.ROTATE_0, virtual_mode_set_aware: bool = True,
                                    force_modeset: bool = False) -> bool:
        display_mode = cfg_struct.DisplayMode()
        display_mode.targetId = display_and_adapter_info.TargetID
        display_mode.displayAndAdapterInfo = display_and_adapter_info
        display_mode.HzRes = igcl_timing.HActive
        display_mode.VtRes = igcl_timing.VActive
        display_mode.rotation = rotation
        display_mode.refreshRate = int(igcl_timing.RefreshRate)
        display_mode.scanlineOrdering = enum.PROGRESSIVE
        display_mode.scaling = scaling
        display_mode.pixelClock_Hz = igcl_timing.PixelClock
        display_mode.rrMode = enum.LEGACY_RR

        display_timing = cfg_struct.DisplayTimings()
        display_timing.targetId = display_and_adapter_info.TargetID
        display_timing.hActive = igcl_timing.HActive
        display_timing.vActive = igcl_timing.VActive
        display_timing.hSyncNumerator = igcl_timing.PixelClock
        display_timing.hSyncDenominator = igcl_timing.HTotal
        display_timing.targetPixelRate = igcl_timing.PixelClock
        display_timing.hTotal = igcl_timing.HTotal
        display_timing.vTotal = igcl_timing.VTotal
        display_timing.vSyncNumerator = igcl_timing.PixelClock
        display_timing.vSyncDenominator = igcl_timing.HTotal * igcl_timing.VTotal
        display_timing.scanlineOrdering = enum.PROGRESSIVE
        display_timing.refreshRate = int(igcl_timing.RefreshRate)

        mode_set_status = os_interfaces_dll.set_igcl_mode(display_mode, display_timing, virtual_mode_set_aware,
                                                          force_modeset)
        # Verify if the display mode was applied successfully or not
        if mode_set_status != enum.DISPLAY_CONFIG_SUCCESS:
            if mode_set_status == enum.DISPLAY_CONFIG_ERROR_SUCCESS_RR_MISMATCH:
                logging.warning('Successfully applied display modes with RR Mismatch. WA ( Fix - TBD from Driver)')
                return True
            gdhm.report_bug(
                title="[DisplayConfigLib]Failed to apply IGCL-returned display mode with error {}".format(
                    cfg_enum.DisplayConfigErrorCode(mode_set_status).name),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            logging.error('Failed to apply display mode with error %s' %
                          cfg_enum.DisplayConfigErrorCode(mode_set_status).name)
            mode_set_status = False
        else:
            mode_set_status = True
            logging.info('Successfully applied display mode')

        return mode_set_status

    ##
    # @brief        Exposed IGCL API to get all the supported modes of a particular display.
    # @param[in]    display_and_adapter_info: DisplayAndAdapterInfo
    #                   Display and adapter details of the display for which supported modes is required.
    # @return       is_success, supported_modes: Tuple[bool, Optional[ctypes.POINTER(ctl_display_timing_t)]]:
    #                   is_success: bool
    #                       Returns True if modes are successfully fetched using the IGCL API else False
    #                   supported modes:  Optional[ctypes.POINTER(ctl_display_timing_t)]
    #                       if is_success is True contains the pointer to supported modes array else None
    @classmethod
    def get_all_supported_modes_igcl(cls, display_and_adapter_info: DisplayAndAdapterInfo) -> \
            Tuple[bool, Optional[ctypes.POINTER(ctl_genlock_target_mode_list_t)]]:
        is_success = False
        supported_modes: Optional[ctypes.POINTER(ctl_genlock_target_mode_list_t)] = None
        gfx_adapter_info = display_and_adapter_info.adapterInfo

        args = control_api_args.ctl_genlock_args_t()
        args.Size = ctypes.sizeof(args)
        args.Version = 0
        args.GenlockTopology.IsPrimaryGenlockSystem = True
        args.Operation = control_api_args.ctl_genlock_operation_v.GET_TIMING_DETAILS

        logging.info(f"Fetching Mode list for displays on Adapter: {gfx_adapter_info.gfxIndex}")
        status = control_api_wrapper.display_genlock_get_all_displays_timings(args, gfx_adapter_info)
        if status is False:
            logging.error("Call to ControlAPIGetAllDisplayTimingsGenlock failed.")
            return is_success, supported_modes

        result, handle = control_api_wrapper.get_target_display_handle(display_and_adapter_info)
        if result is False:
            logging.error("Call to GetTargetDisplayHandle failed.")
            gdhm.report_driver_bug_os("[DisplayConfigLib] Failed to fetch target display handle")
            return is_success, supported_modes

        for i in range(args.GenlockTopology.NumGenlockDisplays):
            supported_modes = args.GenlockTopology.pGenlockModeList[i]
            if handle == supported_modes.hDisplayOutput:
                is_success = True
                for mode_index in range(supported_modes.NumModes):
                    mode = supported_modes.pTargetModes[mode_index]
                    logging.debug(f"Mode ({mode_index}): {mode}")
                return is_success, supported_modes

        if is_success is False:
            logging.error("Could not find matching target display handle.")
            gdhm.report_driver_bug_os("[DisplayConfigLib] Could not find matching target display handle")
        return is_success, supported_modes

    ##
    # @brief        Get BDF information for connected display adapter(s)
    # @return       status, bdf_array, adapter_count - Returns error code, array of BdfInfo objects,
    #               number of display adapters (both active and inactive)
    @staticmethod
    def get_bdf_info():
        status, bdf_data, adapter_count = os_interfaces_dll.get_bdf_details()
        if status != 0:
            logging.error("Failed to get BDF information")
            gdhm.report_bug(
                title="[DisplayConfigLib] Failed to fetch BDF information",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            return False, None, None
        return True, bdf_data, adapter_count.value


####################################################################################################

##
# @brief        Specify particular display is attached or not
# @param[in]    enumerated_displays - list of type EnumeratedDisplayEx
# @param[in]    connector_port - Object of type CONNECTOR_PORT_TYPE
# @param[in]    gfx_index - Graphics adapter index (default is 'gfx_0' for single adapter test case)
# @return       bool - True if Display is attached, False otherwise
def is_display_attached(enumerated_displays, connector_port, gfx_index='gfx_0'):
    for display_index in range(enumerated_displays.Count):
        display_info = enumerated_displays.ConnectedDisplays[display_index]
        if display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index.lower() and \
                (cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType)).name == connector_port.upper():
            return True
    return False


##
# @brief        Specify particular display is active or not
# @param[in]    connector_port - Object of type CONNECTOR_PORT_TYPE
# @param[in]    gfx_index - Graphics adapter index ( default is 'gfx_0' for single adapter test case)
# @return       display_info.IsActive - True if display is active, False otherwise and None for Invalid port
def is_display_active(connector_port, gfx_index='gfx_0'):
    enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
    for display_index in range(enumerated_displays.Count):
        display_info = enumerated_displays.ConnectedDisplays[display_index]
        if display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index.lower() and \
                cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name == connector_port.upper():
            return display_info.IsActive
    else:
        logging.error("\tInvalid port: {0}".format(connector_port))
    return None


##
# @brief        API to get supported ports by platform depending on VBT flashed
# @details      Get supported ports by platform depending on VBT flashed.
# @param[in]    gfx_index - Graphics Adapter Index
# @return       list - List of supported ports
def get_supported_ports(gfx_index='gfx_0'):
    _driver_interface = driver_interface.DriverInterface()
    return _driver_interface.get_supported_ports(gfx_index)


##
# @brief        API to get free ports by platform depending on VBT flashed
# @details      Get free ports by platform depending on VBT flashed which were not yet plugged.
#               Example: DP_B, HDMI_C...
# @param[in]    gfx_index - Graphics adapter index
# @return       free_ports - Free port list based on available and active ports
def get_free_ports(gfx_index='gfx_0'):
    gfx_index = gfx_index.lower()
    supported_ports = get_supported_ports(gfx_index).keys()
    config = DisplayConfiguration()
    enumerated_displays = config.get_enumerated_display_info()

    connected_ports = []
    for index in range(enumerated_displays.Count):
        if gfx_index == enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex:
            port_name = cfg_enum.CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
            connected_ports.append(port_name[-1:])

    # Prune free ports from available port list and check suffix with active ports
    free_ports = [port for port in supported_ports if port[-1:] not in connected_ports]
    return free_ports


##
# @brief        Enables or Disables HDR
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Structure or Target ID of the display
# @param[in]    enable - Boolean value to either enable or disable
# @return       hdr_status - Enable or Disable status code
def configure_hdr(display_and_adapter_info, enable):
    hdr_status = os_interfaces_dll.configure_hdr(display_and_adapter_info, enable)
    return hdr_status
