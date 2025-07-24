########################################################################################################################
# @file     dispdiag_verification.py
# @brief    Contains Display Diagnostics Verification.
# @details  This interface will help verify Display Diagnostic DDIs data for collecting generic display state
#           information from the miniport drivers for diagnostic scenarios like black screen.
#           1) verify_dispdiagnonintrusivedata() - Verify Display Diagnostics NonIntrusive data.
#               * Non-Intrusive data consists of display state information for below cases
#               * Display Connectivity, Display ModeSet, Display LinkState, Basic Display Topology, Display LidState
# @author   Prateek Joshi
########################################################################################################################
import logging

from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import valsim_wrapper
from Libs.Core.Verifier import dispdiag_verification_args as dispdiag
from Libs.Core.Verifier.dispdiag_verification_args import DxgkDiagDisplayConnectivity as DiagConnectivity
from Libs.Core.Verifier.dispdiag_verification_args import DxgkDiagDisplayModeSet as DiagModeSet
from Libs.Core.Verifier.dispdiag_verification_args import DxgkDiagDisplayLinkState as DiagLinkState
from Libs.Core.Verifier.dispdiag_verification_args import DxgkDiagBasicDisplayTopology as DiagTopology
from Libs.Core.Verifier.dispdiag_verification_args import DxgkDiagDisplayLidState as DiagLidState
from Libs.Core.Verifier.dispdiag_verification_args import DxgkDiagGetDisplayStateSubstatusFlags as DiagSubstatusFlags
from Libs.Core.Verifier.dispdiag_verification_args import DxgkDiagDisplayScanoutState as DiagScanoutState


##
# @brief        Exposed API to verify display diagnostics non-intrusive data.
# @param[in]    gfx_adapter_index - Graphics Adapter Index
# @return       None
def verify_dispdiagnonintrusivedata(gfx_adapter_index):
    display_info = []
    # Get OS Build Info
    os_info = machine_info.SystemInfo()
    os_build_number = os_info.get_os_info()

    # Check for 20H1 OS - 19041, if other OS ignore verification
    if os_build_number.BuildNumber < '19041':
        logging.info("Display Diagnostics verification is not applicable for OS {}".format(os_build_number.BuildNumber))
        return

    logging.debug(" Display Diagnostics Non-Intrusive Verification ".center(64, "*"))

    enumerated_display = display_config.DisplayConfiguration().get_enumerated_display_info()
    gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
    adapter_info = gfx_adapter_dict[gfx_adapter_index]
    nonintrusive_data = dispdiag.DisplayStateNonIntrusive()

    # Fill NumOfTargets
    nonintrusive_data.NumOfTargets = 0

    # Fill VidPnTargetId
    for target_index in range(0, enumerated_display.Count):
        if enumerated_display.ConnectedDisplays[target_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex == \
                gfx_adapter_index:
            nonintrusive_data.NonIntrusiveData[nonintrusive_data.NumOfTargets].VidPnTargetId = \
                enumerated_display.ConnectedDisplays[target_index].TargetID
            nonintrusive_data.NumOfTargets = nonintrusive_data.NumOfTargets + 1

    # Wrapper call to get display non-intrusive data
    dll_status = valsim_wrapper.get_display_nonintrusivedata(adapter_info, nonintrusive_data)
    if dll_status is False:
        logging.error("Unable to fetch Display Diagnostic Non-intrusive data")
        gdhm.report_bug(
            title="[Display_Diagnostics][DLL] Unable to fetch Display Diagnostics Non-intrusive data",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E3
        )
        return

    # Display Info details stored in order with index to access {Display[0], PortType[1], TargetID[2], GfxIndex[3]}
    for data in range(0, enumerated_display.Count):
        if enumerated_display.ConnectedDisplays[data].DisplayAndAdapterInfo.adapterInfo.gfxIndex == \
                gfx_adapter_index:
            display_info.append([
                str(cfg_enum.CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[data].ConnectorNPortType)),
                enumerated_display.ConnectedDisplays[data].PortType,
                enumerated_display.ConnectedDisplays[data].TargetID,
                enumerated_display.ConnectedDisplays[data].DisplayAndAdapterInfo.adapterInfo.gfxIndex])

    logging.debug("Display Info {}".format(display_info))

    for target_index in range(0, len(display_info)):
        if gfx_adapter_index == display_info[target_index][3]:
            _display = display_info[target_index][0]
            _port_type = display_info[target_index][1]
            _targetid = display_info[target_index][2]
            _gfxindex = display_info[target_index][3]

            logging.info("Display - {} PortType - {} TargetID - {} GfxIndex - {}".format(_display, _port_type,
                                                                                         _targetid, _gfxindex))

            # DisplayConnectivity
            __verify_display_connectivity(nonintrusive_data, target_index, _display)
            # DisplayLidState
            __verify_lid_state(nonintrusive_data, target_index, _port_type, _display)
            # BasicDisplayTopology
            __verify_basic_display_topology(nonintrusive_data, target_index, _port_type, _display)
            # DisplayLinkState
            __verify_link_state(nonintrusive_data, target_index, _display)
            # DisplayModeSet
            __verify_modeset(nonintrusive_data, target_index, _display)
            # ReturnSubStatus of Display
            __verify_substatus(nonintrusive_data, target_index, _display)


##
# @brief        Helper private function to report to GDHM
# @param[in]    display_state - NonIntrusive display state {For Ex: DXGK_DIAG_DISPLAY_CONNECTED}
# @param[in]    display - Display associated with display state {For Ex: DP_A}
# @return       None
def __report_to_gdhm(display_state, display):
    gdhm.report_bug(
        title="[Display_Diagnostics] Unexpected display state {} for display {} ".format(display_state, display),
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E3
    )


##
# @brief        Helper private function to verify display connectivity
# @param[in]    nonintrusive_data - NonIntrusive data structure
# @param[in]    target_index - loop index for display
# @param[in]    display - Display associated with display state
# @return       None
def __verify_display_connectivity(nonintrusive_data, target_index, display):
    get_status = nonintrusive_data.NonIntrusiveData[target_index].DisplayConnectivity
    if get_status == DiagConnectivity.DXGK_DIAG_DISPLAY_CONNECTED.value:
        logging.debug("DisplayConnectivity - {}".format(DiagConnectivity(get_status).name))
    else:
        logging.error("DisplayConnectivity - {}".format(DiagConnectivity(get_status).name))
        __report_to_gdhm(DiagConnectivity(get_status).name, display)


##
# @brief        Helper private function to verify display lid state
# @param[in]    nonintrusive_data - NonIntrusive data structure
# @param[in]    target_index - loop index for display
# @param[in]    port_type - connector port type
# @param[in]    display - Display associated with display state
# @return       None
def __verify_lid_state(nonintrusive_data, target_index, port_type, display):
    get_status = nonintrusive_data.NonIntrusiveData[target_index].DisplayLidState
    if port_type == "EMBEDDED":
        __verify_lid_state_internal(get_status, display)
    elif port_type != "EMBEDDED":
        __verify_lid_state_external(get_status, display)
    else:
        logging.error("DisplayLidState - {}".format(DiagLidState(get_status).name))
        __report_to_gdhm(DiagLidState(get_status).name, display)


##
# @brief        Verifies Internal lid state
# @param[in]    get_status - lid status
# @param[in]    display - Display associated with display state
# @return       None
def __verify_lid_state_internal(get_status, display):
    if get_status == DiagLidState.DXGK_DIAG_DISPLAY_LID_STATE_OPEN.value:
        logging.debug("DisplayLidState - {}".format(DiagLidState(get_status).name))
    else:
        logging.error("DisplayLidState - {}".format(DiagLidState(get_status).name))
        __report_to_gdhm(DiagLidState(get_status).name, display)


##
# @brief        Verifies external lid state
# @param[in]    get_status - lid status
# @param[in]    display - Display associated with display state
# @return       None
def __verify_lid_state_external(get_status, display):
    if get_status == DiagLidState.DXGK_DIAG_DISPLAY_LID_STATE_NOTAPPLICABLE.value:
        logging.debug("DisplayLidState - {}".format(DiagLidState(get_status).name))
    else:
        logging.error("DisplayLidState - {}".format(DiagLidState(get_status).name))
        __report_to_gdhm(DiagLidState(get_status).name, display)


##
# @brief        Helper private function to verify basic display topology
# @param[in]    nonintrusive_data - NonIntrusive data structure
# @param[in]    target_index - loop index for display
# @param[in]    port_type - connector port type
# @param[in]    display - Display associated with display state
# @return       None
def __verify_basic_display_topology(nonintrusive_data, target_index, port_type, display):
    get_status = nonintrusive_data.NonIntrusiveData[target_index].DisplayTopology

    if port_type == "EMBEDDED":
        __verify_basic_display_topology_direct(get_status, display)
    elif port_type == "NATIVE" or port_type == "TC" or port_type == "TC_TBT":
        __verify_basic_display_topology_direct(get_status, display)
    elif display == "COLLAGE_0":
        __verify_basic_display_topology_direct(get_status, display)
    elif port_type == "PLUS":
        __verify_basic_display_topology_plus(get_status, display)
    elif "WD_" in display and get_status == DiagTopology.DXGK_DIAG_DISPLAY_CONNECTED_UNKNOWN.value:
        logging.debug("DisplayTopology - {}".format(DiagTopology(get_status).name))
    else:
        logging.error("DisplayTopology - {}".format(DiagTopology(get_status).name))
        # ToDo: Enable GDHM for Topology in Phase 2
        # __report_to_gdhm(Topology(get_status).name, display)


##
# @brief        Verifies Display topology
# @param[in]    get_status - display topology status
# @param[in]    display - Display associated with display state
# @return       None
def __verify_basic_display_topology_direct(get_status, display):
    if get_status == DiagTopology.DXGK_DIAG_DISPLAY_CONNECTED_DIRECTLY.value:
        logging.debug("DisplayTopology - {}".format(DiagTopology(get_status).name))
    else:
        logging.error("DisplayTopology - {}".format(DiagTopology(get_status).name))
        # ToDo: Enable GDHM for Topology in Phase 2
        # __report_to_gdhm(Topology(get_status).name, display)


##
# @brief        Verifies Display topology
# @param[in]    get_status - display topology status
# @param[in]    display - Display associated with display state
# @return       None
def __verify_basic_display_topology_plus(get_status, display):
    if "HDMI_" in display and get_status == DiagTopology.DXGK_DIAG_DISPLAY_CONNECTED_INDIRECTLY_CONVERTOR.value:
        logging.debug("DisplayTopology - {}".format(DiagTopology(get_status).name))
    elif "DP_" in display and get_status == DiagTopology.DXGK_DIAG_DISPLAY_CONNECTED_DIRECTLY.value:
        logging.debug("DisplayTopology - {}".format(DiagTopology(get_status).name))
    else:
        logging.error("DisplayTopology - {}".format(DiagTopology(get_status).name))
        # ToDo: Enable GDHM for Topology in Phase 2
        # __report_to_gdhm(Topology(get_status).name, display)


##
# @brief        Helper private function to verify various link states
# @param[in]    nonintrusive_data - NonIntrusive data structure
# @param[in]    target_index - loop index for display
# @param[in]    display - Display associated with display state
# @return       None
def __verify_link_state(nonintrusive_data, target_index, display):
    get_status = nonintrusive_data.NonIntrusiveData[target_index].DisplayLinkState
    if get_status == DiagLinkState.DXGK_DIAG_DISPLAY_LINK_STATE_STABLE.value:
        logging.debug("DisplayLinkState - {}".format(DiagLinkState(get_status).name))
    elif "WD_" in display and (get_status == DiagLinkState.DXGK_DIAG_DISPLAY_LINK_STATE_NOTAPPLICABLE.value):
        logging.debug("DisplayLinkState - {}".format(DiagLinkState(get_status).name))
    elif display == "VIRTUALDISPLAY" and (get_status == DiagLinkState.DXGK_DIAG_DISPLAY_LINK_STATE_NOTAPPLICABLE.value):
        logging.debug("DisplayLinkState - {}".format(DiagLinkState(get_status).name))
    else:
        logging.error("DisplayLinkState - {}".format(DiagLinkState(get_status).name))
        # ToDo: Enable GDHM for Link State in Phase 2
        # __report_to_gdhm(LinkState(get_status).name, display)


##
# @brief        Helper private function to verify modeset states
# @param[in]    nonintrusive_data - NonIntrusive data structure
# @param[in]    target_index - loop index for display
# @param[in]    display - Display associated with display state
# @return       None
def __verify_modeset(nonintrusive_data, target_index, display):
    get_status = nonintrusive_data.NonIntrusiveData[target_index].DisplayModeSet
    if get_status == DiagModeSet.DXGK_DIAG_DISPLAY_MODE_SET_YES.value:
        logging.debug("DisplayModeSet - {}".format(DiagModeSet(get_status).name))
    else:
        logging.error("DisplayModeSet - {}".format(DiagModeSet(get_status).name))
        # ToDo: Enable GDHM for ModeSet in Phase 2
        # __report_to_gdhm(ModeSet(get_status).name, display)


##
# @brief        Helper private function to verify various display sub-status states
# @param[in]    nonintrusive_data - NonIntrusive data structure
# @param[in]    target_index - loop index for display
# @param[in]    display - Display associated with display state
# @return       None
def __verify_substatus(nonintrusive_data, target_index, display):
    get_status = nonintrusive_data.NonIntrusiveData[target_index].ReturnSubStatus
    if get_status == DiagSubstatusFlags.DXGK_DIAG_GETDISPLAYSTATE_SUCCESS.value:
        logging.debug("ReturnSubStatus - {}".format(DiagSubstatusFlags(get_status).name))
    else:
        logging.error("ReturnSubStatus - {}".format(DiagSubstatusFlags(get_status).name))
        __report_to_gdhm(DiagSubstatusFlags(get_status).name, display)


##
# @brief        Exposed API to verify display diagnostics intrusive data.
# @param[in]    gfx_adapter_index - Graphics Adapter Index
# @return       bool - True/False
def verify_dispdiag_intrusive_data(gfx_adapter_index):
    scanoutstate = {}
    # Get OS Build Info
    os_info = machine_info.SystemInfo()
    os_build_number = os_info.get_os_info()

    # Check for 20H1 OS - 19041, if other OS ignore verification
    if os_build_number.BuildNumber < '19041':
        logging.error("Display Diagnostics verification is not applicable for OS {}".format(os_build_number.BuildNumber))
        return False

    logging.info(" Display Diagnostics Intrusive Verification ".center(64, "*"))

    enumerated_display = display_config.DisplayConfiguration().get_enumerated_display_info()
    gfx_adapter_dict = test_context.TestContext.get_gfx_adapter_details()
    adapter_info = gfx_adapter_dict[gfx_adapter_index]
    intrusive_data = dispdiag.DisplayStateIntrusive()

    # Fill NumOfTargets
    intrusive_data.NumOfTargets = 0

    # Fill VidPnTargetId
    for target_index in range(0, enumerated_display.Count):
        if enumerated_display.ConnectedDisplays[target_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex == \
                gfx_adapter_index:
            intrusive_data.IntrusiveData[intrusive_data.NumOfTargets].VidPnTargetId = \
                enumerated_display.ConnectedDisplays[target_index].TargetID
            intrusive_data.NumOfTargets = intrusive_data.NumOfTargets + 1

    # Wrapper call to get display intrusive data
    if valsim_wrapper.get_display_intrusivedata(adapter_info, intrusive_data) is False:
        logging.error("Unable to fetch Display Diagnostic intrusive data")
        gdhm.report_test_bug_os(
            title="[Display_Diagnostics][DLL] Unable to fetch Display Diagnostics intrusive data")
        return False

    for target_index in range(enumerated_display.Count):
        if enumerated_display.ConnectedDisplays[target_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex == \
                gfx_adapter_index:
            _display = str(cfg_enum.CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[target_index].ConnectorNPortType))
            _port_type = enumerated_display.ConnectedDisplays[target_index].PortType
            _targetid = enumerated_display.ConnectedDisplays[target_index].TargetID
            _gfxindex = enumerated_display.ConnectedDisplays[target_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex

            logging.info(f"Display - {_display} PortType - {_port_type} TargetID - {_targetid} GfxIndex - {_gfxindex}")

            # DisplayScanoutState
            scanoutstate[_display] = __verify_scanout_state(intrusive_data, target_index)
    return scanoutstate


##
# @brief        Helper private function to verify scanout state
# @param[in]    intrusive_data - Intrusive data structure
# @param[in]    target_index - loop index for display
# @return       bool - True/False if black screen detected
def __verify_scanout_state(intrusive_data, target_index):
    get_status = intrusive_data.IntrusiveData[target_index].DisplayScanoutState
    status = get_status == DiagScanoutState.DXGK_DIAG_DISPLAY_SCANOUT_ACTIVE_BLACK.value
    logging.info("Black screen is detected" if status else "Black screen is not detected")
    return status
