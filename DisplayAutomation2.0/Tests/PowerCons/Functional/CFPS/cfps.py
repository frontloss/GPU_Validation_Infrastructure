#######################################################################################################################
# @file         cfps.py
# @brief        Contains CFPS verification APIs
#
# @author       Vinod D S
#######################################################################################################################

import logging
import os
from enum import IntEnum

from Libs.Core import etl_parser, driver_escape, display_essential
from Libs.Core.logger import gdhm
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Core.wrapper.driver_escape_args import CappedFpsArgs, CappedFpsState, CappedFpsOpcode
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import common, workload
from Tests.VRR import vrr

MAX_PLANES_PER_PIPE = 5


##
# @brief        Enum maintained to have list of features to be used for respective concurrency test.
class Feature(IntEnum):
    NONE = 0
    HDR = 1
    FBC = 2
    RENDER_DECOMPRESSION = 3
    MPO = 4
    FLIPQ = 5
    HW_ROTATION = 6
    PIPE_SCALAR = 7


##
# @brief        Exposed object class for all apps used for IGCL
class AppsForIgcl:
    FLIP_AT = b"FlipAt.exe"
    FLIP_MODEL_D3D12 = b"FlipModelD3D12.exe"
    CLASSIC_3D = b"Classic3DCubeApp.exe"
    MOVING_RECTANGLE = b"MovingRectangleApp.exe"
    ANGRY_BOTS = b"AngryBotsGame.exe"
    GLOBAL = b""


##
# @brief        Exposed API to enable CFPS
# @param[in]    adapter object of Adapter
# @param[in]    panel object of Panel
# @param[in]    is_auto bool, whether enabling AUTO mode or ENABLE mode
# @param[in]    application_name name of the application
# @return       True if operation is successful, False otherwise
def enable(adapter, panel=None, is_auto=False, application_name=AppsForIgcl.GLOBAL):
    assert adapter

    if adapter.name in common.PRE_GEN_13_PLATFORMS:
        return enable_via_escape(adapter, is_auto)
    else:
        if panel is None:
            status = True
            for panel in adapter.panels.values():
                status &= __enable_via_igcl(adapter, panel, application_name)
            return status
        else:
            return __enable_via_igcl(adapter, panel, application_name)


##
# @brief        Exposed API to disable CFPS
# @param[in]    adapter object of Adapter
# @param[in]    panel object of Panel
# @param[in]    application_name name of the application
# @return       True if operation is successful, False otherwise
def disable(adapter, panel=None, application_name=AppsForIgcl.GLOBAL):
    assert adapter

    if adapter.name in common.PRE_GEN_13_PLATFORMS:
        return __disable_via_escape(adapter)
    else:
        if panel is None:
            status = True
            for panel in adapter.panels.values():
                status &= __disable_via_igcl(adapter, panel, application_name)
            return status
        else:
            return __enable_via_igcl(adapter, panel, application_name)


##
# @brief        Internal API to enable CFPS via IGCL
# @param[in]    adapter object of Adapter
# @param[in]    panel object of Panel
# @param[in]    application_name name of the application
# @return       True if operation is successful, None if not required, False otherwise
def __enable_via_igcl(adapter, panel, application_name=AppsForIgcl.GLOBAL):
    assert adapter
    assert panel

    if panel.is_lfp is False:
        logging.info(f"Panel on {panel.port} is not LFP. CFPS enable is not required")
        return True

    logging.info(f"Step: Enabling CFPS via IGCL for {adapter.name} on {panel.port} for {application_name}")

    # Disable VRR if supported in the adapter
    # TODO disable VRR panel wise in IGCL way
    if adapter.is_vrr_supported is True:
        if vrr.disable(adapter) is False:
            logging.error("\tFAILED to disable VRR")
            return False
        logging.info(f"\tSuccessfully disabled VRR for {adapter.name}")
    else:
        logging.info(f"\tVRR is not supported for {adapter.name}")

    ctl_3d_feature_args = control_api_args.ctl_3d_feature_getset_t()
    ctl_3d_feature_args.bSet = True
    ctl_3d_feature_args.ApplicationName = application_name
    flip_mode = control_api_args.CTL_BIT(5)

    if control_api_wrapper.get_set_gaming_flip_modes(ctl_3d_feature_args, flip_mode, panel.target_id) is False:
        logging.error(f"\tFAILED to enable CFPS via IGCL for {adapter.name} on {panel.port} for {application_name}")
        return False
    logging.info(f"Successfully enabled CFPS via IGCL for {adapter.name} on {panel.port} for {application_name}")
    return True


##
# @brief        Internal API to disable CFPS via IGCL
# @param[in]    adapter object of Adapter
# @param[in]    panel object of Panel
# @param[in]    application_name name of the application
# @return       True if operation is successful, None if not required, False otherwise
def __disable_via_igcl(adapter, panel, application_name=AppsForIgcl.GLOBAL):
    assert adapter
    assert panel

    if panel.is_lfp is False:
        logging.info(f"Panel on {panel.port} is not LFP. CFPS disable is not required")
        return True

    logging.info(f"Step: Disabling CFPS for {adapter.name} on {panel.port} for {application_name} via IGCL")
    ctl_3d_feature_args = control_api_args.ctl_3d_feature_getset_t()
    ctl_3d_feature_args.bSet = True
    ctl_3d_feature_args.ApplicationName = application_name
    flip_mode = control_api_args.CTL_BIT(0)

    if control_api_wrapper.get_set_gaming_flip_modes(ctl_3d_feature_args, flip_mode, panel.target_id) is False:
        logging.error(f"\tFAILED to disable CFPS via IGCL for {adapter.name} on {panel.port} for {application_name}")
        return False
    logging.info(f"Successfully disabled CFPS via IGCL for {adapter.name} on {panel.port} for {application_name}")
    return True


##
# @brief        Internal API to enable CFPS via Escape
# @param[in]    adapter object of Adapter
# @param[in]    is_auto bool, whether enabling AUTO mode or ENABLE mode
# @return       True if operation is successful, False otherwise
def enable_via_escape(adapter, is_auto=False):
    assert adapter

    logging.info("Step: Enabling{0} CFPS for {1}".format("(AUTO)" if is_auto else "", adapter.name))
    # Disable VRR if supported in the adapter
    if adapter.is_vrr_supported is True:
        if vrr.disable(adapter) is False:
            logging.error("FAILED to disable VRR")
            return False
        logging.info(f"Successfully disabled VRR for {adapter.name}")
    else:
        logging.info(f"VRR is not supported for {adapter.name}")

    # Make sure CFPS is enabled in DisplayPcFeatureControl before calling escape call, otherwise escape call, won't work
    display_pc_feature_control = registry.DisplayPcFeatureControl(adapter.gfx_index)
    if display_pc_feature_control.DisableCappedFps == 1:
        display_pc_feature_control.DisableCappedFps = 0
        if display_pc_feature_control.update(adapter.gfx_index) is False:
            logging.error("\tFAILED to enable CFPS in registry - DisplayPcFeatureControl")
            return False
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error("\tFAILED to restart display driver")
            return False

    # Get the current CFPS status
    cfps_args = CappedFpsArgs()
    cfps_args.opCode = CappedFpsOpcode.GET_CAPPED_FPS.value
    cfps_flag, cfps_args = driver_escape.get_set_cfps(adapter.gfx_index, cfps_args)
    if not cfps_flag:
        logging.error(f'\tEscape call FAILED to get CFPS status')
        return False
    if cfps_args.cappedFpsSupport is False:
        logging.error("\tCFPS is not supported in the platform")
        return False

    expected_state = CappedFpsState.AUTO.value if is_auto else CappedFpsState.ENABLE.value

    # Enable CFPS
    if cfps_args.cappedFpsState != expected_state:
        cfps_args.opCode = CappedFpsOpcode.SET_CAPPED_FPS.value
        cfps_args.cappedFpsState = expected_state
        cfps_flag, cfps_args = driver_escape.get_set_cfps(adapter.gfx_index, cfps_args)
        if not cfps_flag:
            logging.error(f'\tEscape call FAILED to enable CFPS')
            return False

        # Verify CFPS is enabled
        cfps_args = CappedFpsArgs()
        cfps_args.opCode = CappedFpsOpcode.GET_CAPPED_FPS.value
        cfps_flag, cfps_args = driver_escape.get_set_cfps(adapter.gfx_index, cfps_args)
        if not cfps_flag:
            logging.error(f'\tEscape call FAILED to get CFPS status')
            return False
        if cfps_args.cappedFpsState != expected_state:
            logging.error("\tFAILED to enable CFPS via escape-call")
            return False

    logging.info("\tPASS: CFPS status Expected= {0}, Actual= {0}".format("AUTO" if is_auto else "ENABLED"))
    return True


##
# @brief        Internal API to disable CFPS via Escape
# @param[in]    adapter object of Adapter
# @return       True if operation is successful, False otherwise
def __disable_via_escape(adapter):
    assert adapter

    logging.info("Step: Disabling CFPS for {0}".format(adapter.name))
    # CFPS should be enabled in DisplayPcFeatureControl before calling escape call, otherwise escape call, won't work
    display_pc_feature_control = registry.DisplayPcFeatureControl(adapter.gfx_index)
    if display_pc_feature_control.DisableCappedFps == 1:
        logging.info("\tPASS: CFPS status Expected= DISABLED, Actual= DISABLED")
        return True

    # Get the current CFPS status
    cfps_args = CappedFpsArgs()
    cfps_args.opCode = CappedFpsOpcode.GET_CAPPED_FPS.value
    cfps_flag, cfps_args = driver_escape.get_set_cfps(adapter.gfx_index, cfps_args)
    if not cfps_flag:
        logging.error(f'Escape call FAILED to get CFPS status')
        return False

    if cfps_args.cappedFpsSupport is False:
        logging.error("\tCFPS is not supported in the platform")
        return False

    # Disable CFPS
    if cfps_args.cappedFpsState != CappedFpsState.DISABLE.value:
        cfps_args.opCode = CappedFpsOpcode.SET_CAPPED_FPS.value
        cfps_args.cappedFpsState = CappedFpsState.DISABLE.value
        cfps_flag, cfps_args = driver_escape.get_set_cfps(adapter.gfx_index, cfps_args)
        if not cfps_flag:
            logging.error(f'\tEscape call FAILED to disable CFPS')
            return False

        # Verify CFPS is disabled
        cfps_args = CappedFpsArgs()
        cfps_args.opCode = CappedFpsOpcode.GET_CAPPED_FPS.value
        cfps_flag, cfps_args = driver_escape.get_set_cfps(adapter.gfx_index, cfps_args)
        if not cfps_flag:
            logging.error(f'\tEscape call FAILED to get CFPS status')
            return False
        if cfps_args.cappedFpsState != CappedFpsState.DISABLE.value:
            logging.error("\tFAILED to disable CFPS")
            return False

    logging.info("\tPASS: CFPS status Expected= DISABLED, Actual= DISABLED")
    return True


##
# @brief        Exposed API to verify CFPS
# @param[in]    adapter object of Adapter
# @param[in]    etl_file String, etl file to be used for verification
# @return       True if operation is successful, False otherwise
def verify(adapter, etl_file):
    assert adapter
    assert etl_file

    # Make sure etl file is present
    if os.path.exists(etl_file) is False:
        logging.error(etl_file + " NOT found.")
        return False

    # Generate reports from ETL file using EtlParser
    logging.info("\tGenerating EtlParser Report for {0}".format(etl_file))
    etl_parser_config = etl_parser.EtlParserConfig()
    etl_parser_config.commonData = 1
    etl_parser_config.flipData = 1
    etl_parser_config.vbiData = 1
    if etl_parser.generate_report(etl_file, etl_parser_config) is False:
        logging.error("\t\tFAILED to generate EtlParser report (Test Issue)")
        return False
    logging.info("\t\tPASS: Generated EtlParser report successfully")

    status = True
    for panel in adapter.panels.values():
        if panel.is_lfp is False or 'DP' not in panel.port:
            continue
        logging.info("Step: Verifying CFPS on {0}-{1}".format(adapter.name, panel.port))
        if __verify_capped_fps_per_vbi(panel) is True:
            logging.info("\tCFPS is functional")
        else:
            logging.warning("\tCFPS is NOT functional")
            status = False

    return status


##
# @brief        Helper API to verify incoming flips with vbi
# @param[in]    panel, Panel
# @param[in]    start, float, start timestamp - optional
# @param[in]    end, float, end timestamp - optional
# @return       status, Boolean, True if verification is successful, False otherwise
def __verify_capped_fps_per_vbi(panel, start=None, end=None):
    pipe = 'PIPE_' + panel.pipe
    panel_max_rr = panel.max_rr

    flip_data = etl_parser.get_flip_data(pipe, start_time=start, end_time=end)
    if flip_data is None:
        logging.error("\t\tFAIL: No Flip data found")
        return False
    logging.info("\t\tNumber of incoming flips: {0}".format(len(flip_data)))

    vbi_data = etl_parser.get_vbi_data(pipe, start, end)
    if vbi_data is None:
        logging.error("\t\tFAIL: No VBI data found")
        return False
    logging.info("\t\tNumber of VBIs reported to OS: {0}".format(len(vbi_data)))

    vbi_flip_mapping = {}  # Holds vbi & flip mapping per layer { vbi_time_stamp : { layer_index : [flip_time_stamps]}}
    pos = 0
    first_vbi_timestamp = None
    last_vbi_timestamp = None
    # Segregating the flips per layer per vbi
    for vbi in vbi_data:
        vbi_flip_mapping[vbi.TimeStamp] = {}
        if first_vbi_timestamp is None:
            first_vbi_timestamp = vbi.TimeStamp
        last_vbi_timestamp = vbi.TimeStamp
        for index in range(pos, len(flip_data)):
            # If the flip being processed is after vbi, then break fo the current iteration tagging to vbi
            if flip_data[index].TimeStamp > vbi.TimeStamp:
                break
            # Flip data for each layer index, do the vbi & flip mapping
            for layer_flip in flip_data[index].PlaneInfoList:
                if layer_flip.LayerIndex not in vbi_flip_mapping[vbi.TimeStamp].keys():
                    vbi_flip_mapping[vbi.TimeStamp][layer_flip.LayerIndex] = [flip_data[index].TimeStamp]
                else:
                    vbi_flip_mapping[vbi.TimeStamp][layer_flip.LayerIndex].append(flip_data[index].TimeStamp)
            pos += 1

    # Check that no. of VBI are less than or equal to RR
    vbi_num = round(len(vbi_data) * 1000 / (last_vbi_timestamp - first_vbi_timestamp), 0)
    logging.info("\t\tNumber of VBIs per second= {0}, RR= {1}".format(vbi_num, panel_max_rr))

    # Print the VBI(s) where multiple flips are coming (violating CFPS logic)
    fps_capped = True
    flip_capped_status = [None for _ in range(MAX_PLANES_PER_PIPE)]
    for vbi, flip_info in sorted(vbi_flip_mapping.items()):
        for layer_index, flip in sorted(flip_info.items()):
            if len(flip) > 1:
                if flip_capped_status[layer_index] is not None:
                    logging.info(
                        "\t\tVBI - {0}ms: {1} flips are seen for layer {2} -> {3} "
                        "({4} flips were seen in previous VBI -> {5})".format(
                            vbi, len(flip), layer_index, flip,
                            len(flip_capped_status[layer_index]), flip_capped_status[layer_index]))
                    fps_capped = False
                else:
                    logging.info("\t\tVBI - {0}ms: {1} flips are seen for layer {2} -> {3} ".format(
                        vbi, len(flip), layer_index, flip))
                flip_capped_status[layer_index] = flip
            else:
                flip_capped_status[layer_index] = None
        # Clear the tagging for the layers which are not involved in current vbi
        for plane in range(MAX_PLANES_PER_PIPE):
            if plane not in flip_info.keys():
                flip_capped_status[plane] = None

    if fps_capped:
        logging.info("\t\tFPS is capped (there are NO consecutive 2 flips or more than 2 flips in single VBI)")
    else:
        logging.warning("\t\tFPS is NOT capped (there are consecutive 2 flips or more than 2 flips in single VBI)")

    return fps_capped


##
# @brief        Helper function to handle all the common steps required for all the tests like opening/closing of
#               game
# @param[in]    full_screen Boolean, True= game will be played in full screen mode, False= windowed mode
# @param[in]    power_event [optional] Enum, CS/S3/S4
# @return       etl file and status
def run_workload(full_screen, power_event=None):
    app = workload.Apps.MovingRectangleApp
    workload_args = [app, 30, full_screen, power_event]
    if not full_screen:
        app = workload.Apps.FlipAt
        app_config = workload.FlipAtAppConfig()
        app_config.game_index = 6  # NO_MAN_SKY GAME
        workload_args = [app, 30, full_screen, power_event, None, app_config]

    etl_file, status = workload.run(workload.GAME_PLAYBACK, workload_args)
    # Ensure async flips
    if vrr.async_flips_present(etl_file):
        return etl_file, status

    if app is workload.Apps.FlipAt:
        gdhm.report_bug(
            title="[PowerCons][CFPS] OS is not sending async flips during game playback",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P3,
            exposure=gdhm.Exposure.E3
        )
        logging.error("OS is NOT sending async flips")
        return None, None
    app = workload.Apps.FlipAt
    app_config = workload.FlipAtAppConfig()
    app_config.game_index = 6  # NO_MAN_SKY GAME
    workload_args = [app, 30, full_screen, power_event, None, app_config]
    etl_file, status = workload.run(workload.GAME_PLAYBACK, workload_args)
    if vrr.async_flips_present(etl_file) is False:
        gdhm.report_bug(
            title="[PowerCons][CFPS] OS is not sending async flips during game playback",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P3,
            exposure=gdhm.Exposure.E3
        )
        logging.error("OS is NOT sending async flips")
        return None, None
    return etl_file, status
