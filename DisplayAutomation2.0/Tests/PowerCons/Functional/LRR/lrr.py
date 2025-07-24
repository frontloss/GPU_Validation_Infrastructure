#######################################################################################################################
# @file         lrr.py
# @brief        Contains LRR enable/disable and verification APIs
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import sys
from collections import OrderedDict
from enum import Enum

from DisplayRegs.DisplayOffsets import PsrOffsetValues, CmtgOffsetValues
from Libs.Core import etl_parser, registry_access
from Libs.Core.logger import html, gdhm
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules.dut_context import Panel, Adapter, RrSwitchingMethod
from Tests.PowerCons.Functional.DMRRS import hrr
from Tests.VRR import vrr
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.interruptData = 1
ETL_PARSER_CONFIG.functionData = 1

VIDEO_FILE_MAPPING = {
    '24': '24.000.mp4',
    '25': '25.000.mp4',
    '30': '30.000.mp4',
    '23_976': '23.976.mp4',
    '29_970': '29.970.mp4',
    '59_940': '59.940.mp4',
    '30_BLANK_VIDEO': '30.000_FPS_WITH_BLANK.mp4'
}

VIDEO_FPS_MAPPING = {
    '24.000.mp4': 24.000,
    '25.000.mp4': 25.000,
    '30.000.mp4': 30.000,
    '23.976.mp4': 23.976,
    '29.970.mp4': 29.970,
    '59.940.mp4': 59.940,
    '30.000_FPS_WITH_BLANK.mp4': 30.000
}


##
# @brief        Method to be used for LRR tests
class Method:
    IDLE = "IDLE"
    VIDEO = "VIDEO"


##
# @brief        Enum for different LRR versions
class LrrVersion(Enum):
    LRR1_0 = 1
    LRR2_0 = 2
    LRR2_5 = 2.5
    NO_LRR = 10


##
# @brief        Exposed API to enable LRR
# @param[in]    adapter object Adapter
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
@html.step("Enabling LRR using reg-key")
def enable(adapter: Adapter) -> bool:
    assert adapter

    # LRR is DRRS + PSR2. Make sure PSR2 is enabled for given adapter.
    psr2_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
    if psr2_status is False:
        logging.error(f"\tFAILED to enable PSR2 on {adapter.name}")
        return False
    logging.info(f"\tPASS: Enabled PSR2 on {adapter.name}")

    # Enable DMRRS (DRRS will be enabled as part of DMRRS)
    dmrrs_status = dmrrs.enable(adapter)
    if dmrrs_status is False:
        logging.error(f"\tFAILED to enable DMRRS on {adapter.name}")
        return False
    logging.info(f"\tPASS: Enabled DMRRS on {adapter.name}")

    logging.info(f"\tUpdating {registry.RegKeys.PSR.PSR2_DRRS_ENABLE}= 0x1 for {adapter.gfx_index}")
    # Make sure PSR2 is enabled
    lrr_status = registry.write(adapter.gfx_index, registry.RegKeys.PSR.PSR2_DRRS_ENABLE,
                                registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
    if lrr_status is False:
        logging.error(f"\tFAILED to update {registry.RegKeys.PSR.PSR2_DRRS_ENABLE} reg-key")
        return False
    logging.info(f"\tPASS: Updated {registry.RegKeys.PSR.PSR2_DRRS_ENABLE} reg-key")

    return psr2_status or dmrrs_status or lrr_status


##
# @brief        Exposed API to disable LRR in driver
# @param[in]    adapter Adapter
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
@html.step("Disabling LRR using reg-key")
def disable(adapter: Adapter) -> bool:
    assert adapter

    status = registry.write(adapter.gfx_index, registry.RegKeys.PSR.PSR2_DRRS_ENABLE, registry_access.RegDataType.DWORD,
                            registry.RegValues.DISABLE)
    if status is False:
        logging.error(f"\tFAILED to disable LRR from {registry.RegKeys.PSR.PSR2_DRRS_ENABLE} reg-key")
        return False
    logging.info(f"\tPASS: Disabled LRR for {adapter.name}")

    return status


##
# @brief        Exposed API to verify LRR
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    etl_file String path to etl file
# @param[in]    polling_data Tuple
# @param[in]    method string, Method
# @param[in]    rr_method enum, RrSwitchingMethod
# @param[in]    pause_video Boolean
# @param[in]    verify_hrr Boolean, to indicate if hrr has to be verified
# @param[in]    check_psr1 Boolean, to indicate if psr_1 has to be verified
# @param[in]    video dictionary, VIDEO_FILE_MAPPING
# @return       status, True lrr functionality is verified, False otherwise
def verify(adapter: Adapter, panel: Panel, etl_file: str, polling_data: dict, method: Method, rr_method: RrSwitchingMethod,
           pause_video: bool = False, verify_hrr: bool = False, check_psr1: bool = False,
           video: VIDEO_FILE_MAPPING = VIDEO_FILE_MAPPING['24']) -> bool:
    assert adapter
    assert panel
    assert etl_file
    media_fps = VIDEO_FPS_MAPPING[video]
    status = True

    html.step_start(f"LRR Verification for {panel.port} on {adapter.gfx_index}")
    logging.info(f"\tGeneric Info: LRR switching method= {rr_method}, Method= {method}, FPS= {media_fps}")
    # RR change verification
    # Verify that there is no RR change of any kind (LinkM, VrrVmax, VTotal)
    if (rr_method == RrSwitchingMethod.UNSUPPORTED) or (method == Method.IDLE and rr_method in
                                                        [RrSwitchingMethod.VTOTAL_HW, RrSwitchingMethod.VTOTAL_SW]):
        html.step_start("Checking for any RR change (Expectation: RR should not change)")
        rr_change_status = drrs.is_rr_changing(adapter, panel, etl_file)
        if rr_change_status is None:
            logging.error("\tETL report generation FAILED")
            status = False
        elif rr_change_status is False:
            logging.info("\tNo RefreshRate change detected (Expected)")
        else:
            gdhm.report_driver_bug_os(f"[OsFeatures][DMRRS] Refresh rate is changing for {rr_method} method")
            logging.error("\tRefreshRate change is detected (Unexpected)")
            status = False
        html.step_end()
    else:
        if method == Method.IDLE:
            status &= drrs.verify(adapter, panel, etl_file)
        elif method == Method.VIDEO:
            status &= dmrrs.verify(adapter, panel, etl_file, media_fps)
            if verify_hrr:
                status &= hrr.verify(adapter, panel, etl_file, media_fps)
        if rr_method == RrSwitchingMethod.VTOTAL_SW:
            if check_rr_programming_in_active_region(adapter, panel, etl_file, rr_method) is False:
                status = False

    # PSR verification
    html.step_start(f"\tVerifying PSR2 on {panel.port} for LRR {rr_method} method")

    # Check for PSR Restriction and PSR Setup time, the api will return the supported version,
    # if supported version is not PSR2, LRR will not be supported
    psr_version = psr.verify_psr_restrictions(adapter, panel, psr.UserRequestedFeature.PSR_2)
    logging.info(f"PSR Supported Version Expected= PSR_2 Actual= PSR_{psr_version}")

    # Double Check to confirm PSR2 is not enabled in driver
    if psr_version is not psr.UserRequestedFeature.PSR_2:
        if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
            logging.info(f"Skipping verification as PSR2 Restriction failed and PSR2 is disabled in "
                         f" driver for {panel.port}")
            return True
        logging.error(f"PSR2 Restriction failed but PSR2 is enabled in driver for {panel.port}")
        return False

    if rr_method == RrSwitchingMethod.CLOCK or rr_method == RrSwitchingMethod.VTOTAL_SW:
        status &= psr.verify_psr2(adapter, panel, polling_data, method, pause_video, True)
        # verify if PSR1 is not enabled with LRR2.5/LRR1.0
        if check_psr1:
            status &= verify_psr1_enabled(adapter, panel, etl_file)

    elif rr_method == RrSwitchingMethod.VTOTAL_HW:
        if method == Method.IDLE:
            status &= psr.verify_psr2(adapter, panel, polling_data, method, pause_video, True)
        elif method == Method.VIDEO:
            # From Gen14+, PSR2 and VRR HW should work together
            if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                status &= psr.verify_psr2(adapter, panel, polling_data, method, pause_video, True)
            else:
                su_verify_status = verify_no_su_during_video(adapter, panel, etl_file, pause_video)
                logging.debug(f"DMRRS_SU_Status_in_LRR2_0: {su_verify_status}")
                status &= su_verify_status
    html.step_end()
    return status


##
# @brief        Exposed API to verify PSR1 is enabled using etl
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_file path to the etl file of the workload
# @return       status, True lrr functionality is verified, False otherwise
def verify_psr1_enabled(adapter: Adapter, panel: Panel, etl_file):
    html.step_start(f"Verifying PSR1 status is enabled for {panel.port} on {adapter.gfx_index} ")
    # Generate the etl report
    logging.info(f"\tGenerating EtlParser Report for {etl_file}")
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        html.step_end()
        return False
    logging.info("\tSuccessfully generated ETL Parser report")

    # get the mmio offsets
    psr_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)
    psr_ctl_offset = psr_regs.SrdCtlReg
    # get the mmio entries from etl
    mmio_output = etl_parser.get_mmio_data(psr_ctl_offset)
    # if no entry of the offset is found in the etl return True
    if mmio_output is None:
        logging.info("No MMIO of PSR1 register found (PSR1 is not enabled)")
        html.step_end()
        return True
    # if entries are found check ensure PSR1 is disabled
    for mmio_data in mmio_output:
        psr_info = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(SrdCtlReg=mmio_data.Data))
        if psr_info.SrdEnable:
            logging.error(f"PSR1 is enabled at {mmio_data.TimeStamp}")
            html.step_end()
            return False

    logging.info("PSR1 is not enabled")
    html.step_end()
    return True


##
# @brief        Exposed API to verify PSR2 during video playback in LRR 2.0 using ETL
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_path path to the etl file of the workload
# @param[in]    is_video_pause
# @return       status, True if video playback with lrr2.0 scenario is verified, False otherwise
@html.step("Verifying No Selective Update happens during Video Playback")
def verify_no_su_during_video(adapter: Adapter, panel: Panel, etl_path, is_video_pause=None):
    # In Video playback case: No SU should happen because in LRR 2.0 switches to DMRRS in case of Video playback
    # Steps:
    # 1. Get the Video playback time using the flip data(Check for non-zero duration flips)
    # 2. Get the Start time and end time
    # 3. From the ETL Get the PSR2_STATUS_REGISTER MMIO
    # 4. Loop through each entry and get selective update count
    # 5. If count == 0, then PSR was inactive during the video playback return True
    # 6. Else return False

    # Parse ETL
    logging.info(f"\tGenerating EtlParser Report for {etl_path}")
    if etl_parser.generate_report(etl_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False
    logging.info("\tSuccessfully generated ETL Parser report")

    # Get the Flip Data
    flip_data = etl_parser.get_flip_data('PIPE_' + panel.pipe)
    if flip_data is None:
        logging.error(f"Flip Data NOT found for PIPE_{panel.pipe}")
        gdhm.report_driver_bug_os(f"[OsFeatures][LRR]Flip Data not found")
        return False

    # Get the start and end time of flips with duration.
    duration_regions = {}  # Dictionary to contain the start and end time of regions with non-zero duration flips
    previous_flip = None
    same_flip = None
    for flip in flip_data:
        # Skip the flips with plane disable call, these flips might have unexpected data.
        is_plane_disable_call = False
        for plane_info in flip.PlaneInfoList:
            if plane_info.Flags == "":
                is_plane_disable_call = True
                break

        if is_plane_disable_call:
            logging.debug(f"\tSkipped plane disable flip for duration calculation")
            logging.debug(f"\t{flip}")
            continue

        if flip.Duration is not None:
            # Whenever a changed duration is found add it to the list
            # List format = {duration1: [(start1, end1), (start2, end2),...], duration2 = [(start1, end1),...]}
            if flip.Duration not in duration_regions.keys():
                duration_regions[flip.Duration] = []

            # If previous flip is None
            if previous_flip is None:
                previous_flip = flip
                logging.info(f"Flip Duration(first entry): {flip.Duration}, [Start - {flip.TimeStamp}]")
                duration_regions[flip.Duration].append((0, flip.TimeStamp))
                continue
            if previous_flip.Duration == flip.Duration:
                same_flip = flip
                continue

            if same_flip is None:
                logging.info(
                    f"Flip Duration: {previous_flip.Duration}, [{previous_flip.TimeStamp} - {previous_flip.TimeStamp}]")
                duration_regions[previous_flip.Duration].append((previous_flip.TimeStamp, previous_flip.TimeStamp))
            else:
                logging.info(
                    f"Flip Duration: {previous_flip.Duration}, [{previous_flip.TimeStamp} - {same_flip.TimeStamp}]")
                duration_regions[previous_flip.Duration].append((previous_flip.TimeStamp, same_flip.TimeStamp))
            previous_flip = flip

    # Add last flip to the duration region
    logging.info(f"Flip Duration(last entry): {previous_flip.Duration}, [{previous_flip.TimeStamp} - END]")
    duration_regions[previous_flip.Duration].append((previous_flip.TimeStamp, sys.maxsize))
    logging.info(f"Duration Regions : {duration_regions}")

    # Check if any Control interrupt observed then Duration regions change,
    # scenario can hit in case of pause and play VPB
    non_zero_duration_regions = {}  # non_zero duration dictionary
    if is_video_pause:
        for duration, timestamps in duration_regions.items():
            if duration > 0:
                if duration not in non_zero_duration_regions.keys():
                    non_zero_duration_regions[duration] = []
                for se_timestamp in timestamps:
                    start_t, end_t = se_timestamp
                    logging.info("\tStep: Verifying VBI notification calls during video playback")
                    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                                   etl_parser.InterruptType.CRTC_VSYNC,
                                                                   start_t, end_t)
                    if interrupt_data is None:
                        logging.info(f"\t\tNo VBI notification found during video {duration} : {start_t} - {end_t}")
                        non_zero_duration_regions[duration].append((start_t, end_t))
                    else:
                        disable_no_phase_found = False
                        disable_interrupt_time = 0
                        enable_found = False
                        enable_interrupt_time = start_t
                        for interrupt in interrupt_data:
                            # looking for first disable no phase interrupt
                            if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.DISABLE_NO_PHASE] and \
                                    disable_no_phase_found is False:
                                disable_no_phase_found = True
                                non_zero_duration_regions[duration].append((enable_interrupt_time, interrupt.TimeStamp))
                            # check for enable interrupt post receive disable no phase interrupt.
                            if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.ENABLE] and \
                                    disable_no_phase_found is True:
                                disable_no_phase_found = False
                                enable_found = True
                                enable_interrupt_time = interrupt.TimeStamp
                        if enable_found is True and disable_no_phase_found is False:
                            non_zero_duration_regions[duration].append((enable_interrupt_time, end_t))

    # In case of VPB scenario not expecting any interrupt so directly considering non zero duration region.
    else:
        for duration, timestamps in duration_regions.items():
            if duration > 0:
                if duration not in non_zero_duration_regions.keys():
                    non_zero_duration_regions[duration] = []
                for se_timestamp in timestamps:
                    start_t, end_t = se_timestamp
                    non_zero_duration_regions[duration].append((start_t, end_t))


    # get the mmio offsets
    psr_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)
    psr2_status_offset = psr_regs.Psr2StatusReg
    psr2_status = MMIORegister.get_instance("PSR2_STATUS_REGISTER", "PSR2_STATUS_" + panel.transcoder, adapter.name)

    # get the mmio offsets for PSR2 CTL register
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        psr2_ctl_offset = psr_regs.Psr2CtrlReg
    else:
        psr2_ctl_offset = 0x60902
        if panel.transcoder == 'B':
            psr2_ctl_offset = 0x61902
    psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)

    # removing time tuple where no flip.
    for duration, timestamps in non_zero_duration_regions.items():
        index = 0
        list_length = len(timestamps)
        while index < list_length:
            start_t, end_t = timestamps[index]
            # Get the Flip Data to confirm non zero duration flip present during that time
            flip_data = etl_parser.get_flip_data('PIPE_' + panel.pipe, start_time= start_t, end_time=end_t)
            if flip_data is None:
                timestamps.remove(timestamps[index])
                # reducing index value to 1 as after removing value shift left by one value
                list_length = list_length - 1
                continue
            index = index + 1
    for duration, timestamps in non_zero_duration_regions.items():
        for se_timestamp in timestamps:
            start_t, end_t = se_timestamp
            start_t += 1000  # Delay is observed between first non-zero duration call and RR switch

            # Check for the MMIO entries of PSR2_STATUS_REGISTER in ETL
            psr2_status_mmio_output = etl_parser.get_mmio_data(psr2_status_offset, start_time=start_t,
                                                               end_time=end_t)
            if psr2_status_mmio_output is None:
                logging.warning(f"No MMIO output found for PSR2_STATUS_{panel.transcoder}")
                continue
            logging.debug(
                f"PSR2_STATUS_{panel.transcoder} Data from [{start_t} - {end_t}]= {psr2_status_mmio_output}")

            psr2_su_count = 0
            for mmio_data in psr2_status_mmio_output:
                psr2_status.asUint = mmio_data.Data
                if psr2_status.asUint is None:
                    continue
                if psr2_status.psr2_state == 0x6:
                    logging.error(
                        f"Selective update found to be ON with the MMIO entry: {mmio_data} at {mmio_data.TimeStamp}"
                        f" psr2_state_value= {psr2_status.psr2_state}")
                    psr2_su_count += 1

            if psr2_su_count > 0:
                logging.error(
                    f"PSR2 SU happened during Video Playback for {panel.port} on {adapter.gfx_index}"
                    f" PSR2 SU Count= {psr2_su_count}")

            # If psr2_ctl_enable_count == 0, that means PSR2 was not active during video playback.
            psr2_ctl_enable_count = 0

            # Check for the MMIO entries of PSR2_CTL_REGISTER in ETL
            psr2_mmio_ctl_output = etl_parser.get_mmio_data(psr, is_write=True, start_time=start_t, end_time=end_t)
            if psr2_mmio_ctl_output is None:
                logging.warning(f"No MMIO output found for PSR2_CTL_{panel.transcoder}")
                continue
            logging.debug(f"PSR2_CTL_{panel.transcoder} Data from [{start_t} - {end_t}]= {psr2_mmio_ctl_output}")

            for mmio_data in psr2_mmio_ctl_output:
                if adapter.name in common.PRE_GEN_14_PLATFORMS:
                    data = mmio_data.Data
                else:
                    data = mmio_data.Data << 16
                psr2_ctl.asUint = data
                if psr2_ctl.asUint is None:
                    continue
                if psr2_ctl.psr2_enable == 0x1:
                    logging.error(f"PSR2 CTL {psr2_ctl_offset}= {mmio_data} at {mmio_data.TimeStamp}"
                                  f" 31st bit Expected= Disabled, Actual= Enabled")
                    psr2_ctl_enable_count += 1

            if psr2_ctl_enable_count > 0:
                logging.error(
                    f"PSR2 CTL is enabled during Video Playback for {panel.port} on {adapter.gfx_index}"
                    f" PSR2 CTL Enable Count= {psr2_ctl_enable_count}")

            if psr2_su_count > 0 or psr2_ctl_enable_count > 0:
                return False

    # Special conditions
    # 1. No non-zero duration in duration regions.items()  -- Meaning No Flips with duration found -- No Video Playback
    if len(list(filter(lambda x: x > 0, duration_regions.keys()))) == 0:
        logging.warning(f"Non-Zero Duration Flips not found on {panel.port} - {adapter.gfx_index}")

    return True


##
# @brief        Exposed API to override LRR caps using registry method
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    version enum, LrrVersion
# @return       status Boolean, True if operation is successful, False otherwise
def override_lrr_caps(adapter: Adapter, panel: Panel, version: LrrVersion):
    html.step_start(f"Overriding LRR DPCD caps using reg-key for {panel.port} on {adapter.name}")
    reg_key = registry.RegKeys.LRR.LRR_VERSION_CAPS_OVERRIDE + '_' + panel.pnp_id
    if version == LrrVersion.LRR1_0:
        value = registry.RegValues.LRR.LRR_VERSION_1_0
    elif version == LrrVersion.LRR2_0:
        value = registry.RegValues.LRR.LRR_VERSION_2_0
    elif version == LrrVersion.LRR2_5:
        value = registry.RegValues.LRR.LRR_VERSION_2_5
    else:
        value = registry.RegValues.LRR.LRR_VERSION_INVALID

    logging.info(f"\tCreating {reg_key} with value {value}")
    status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, value)
    if status is False:
        gdhm.report_test_bug_os(f"[OsFeatures][LRR] Failed to create LRR INF {registry.RegKeys.LRR.LRR_VERSION_CAPS_OVERRIDE}",gdhm.ProblemClassification.FUNCTIONALITY,gdhm.Priority.P3,
            gdhm.Exposure.E3)
        return False
    if status is None:
        logging.warning(f"\t\t{reg_key} registry was present at the start of test")
    else:
        logging.info(f"\t\tPASS: Successfully updated {reg_key} with value {value}")

    html.step_end()
    return True


##
# @brief        Exposed API to reset LRR caps override using registry
# @param[in]    adapter Adapter
# @return       None
@html.step("Reset LRR DPCD caps by deleting reg-key")
def reset_lrr_caps_override(adapter: Adapter):
    for port, panel in adapter.panels.items():
        reg_key = registry.RegKeys.LRR.LRR_VERSION_CAPS_OVERRIDE + '_' + panel.pnp_id
        registry.delete(adapter.gfx_index, key=reg_key)


##
# @brief        Exposed API to check if VTotal is changing in case of game play
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    etl_file string, path to etl file
# @return       bool False if VTotal is changing, True otherwise
@html.step("Checking V_TOTAL register is changing")
def is_vtotal_changing(adapter: Adapter, panel: Panel, etl_file):
    logging.info(f"\tGenerating EtlParser Report for {etl_file}")
    if etl_parser.generate_report(etl_file, vrr.ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False
    logging.info("\tSuccessfully generated ETL Parser report")

    vrr_active_period = vrr.get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error(f"No VRR active period found for {panel.port} - {adapter.gfx_index}")
        return False

    # Get the offset
    timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)
    offset = timing_offsets.VTotal
    for vrr_active_start, vrr_active_end in vrr_active_period:
        mmio_data = etl_parser.get_mmio_data(offset, True, vrr_active_start, vrr_active_end)
        if mmio_data is None:
            logging.warning(
                f"No VTotal MMIO entries found during VRR active period ({vrr_active_start}, {vrr_active_end})")
            continue

        initial_value = mmio_data[0].Data  # First value in the active period
        for mmio in mmio_data:
            if mmio.Data != initial_value:
                logging.error(f"VTotal changed during the VRR active period [{vrr_active_start} - {vrr_active_end}]"
                              f"for panel on {panel.port} - {adapter.gfx_index}")
                return False

        logging.info(
            f"No VTotal change during [{vrr_active_start} - {vrr_active_end}] on {panel.port} - {adapter.gfx_index}")

    return True


##
# @brief        External API to check if RR programming is happening in active region
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    etl_file string, path to etl file
# @param[in]    rr_method enum, RrSwitchingMethod
# @return       True if verification successful, False if verification failed, None for not applicable cases
def check_rr_programming_in_active_region(adapter: Adapter, panel: Panel, etl_file, rr_method: RrSwitchingMethod):
    if rr_method in [RrSwitchingMethod.UNSUPPORTED, RrSwitchingMethod.VTOTAL_HW]:
        logging.info("Skipping Active Region check for LRR2.0/No_LRR/LRR2.5 HW switching method")
        return None

    logging.info("Checking RR programming in active region")
    mmio_common_config = etl_parser.EtlParserConfig()
    mmio_common_config.commonData = 1
    mmio_common_config.mmioData = 1
    if etl_parser.generate_report(etl_file, mmio_common_config) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False

    status = True
    is_clock_based = (rr_method == RrSwitchingMethod.CLOCK)
    cmtg_enabled_region, cmtg_disabled_region = __get_cmtg_enable_disable_region(adapter, panel)
    if cmtg_enabled_region is not None:
        for start_time, end_time in cmtg_enabled_region:
            logging.info(f"\tCMTG enabled region: {'etl_start' if start_time is None else start_time} - "
                         f"{'etl_stop' if end_time is None else end_time} m-secs")
            status &= __check_rr_in_active_region(adapter, panel, is_clock_based, start_time, end_time, True)
    if cmtg_disabled_region is not None:
        for start_time, end_time in cmtg_disabled_region:
            logging.info(f"\tCMTG disabled region: {'etl_start' if start_time is None else start_time} - "
                         f"{'etl_stop' if end_time is None else end_time} m-secs")
            status &= __check_rr_in_active_region(adapter, panel, is_clock_based, start_time, end_time, False)

    if status is True:
        logging.info("\tSuccessfully verified RR programming with-in active region")
    else:
        logging.error("\tFAILED to verify RR programming with-in active region")
    return status


##
# @brief        Internal function to get CMTG enable & disabled region
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       tuple of (enabled_region - list, disabled_region - list), various return values,
#               (None, [(None, None)]) --> When No CMTG region, everything is Non-CMTG
#               ([(None, None)], None) --> Only CMTG region, No Non-CMTG region
#               (enabled_region, disabled_region) --> When CMTG & Non-CMTG region exist
def __get_cmtg_enable_disable_region(adapter: Adapter, panel: Panel):
    if adapter.name in common.PRE_GEN_13_PLATFORMS + ["DG2"]:
        return None, [(None, None)]

    cmtg_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
    cmtg_data = etl_parser.get_mmio_data(cmtg_offsets.CmtgControlReg, is_write=True)
    if cmtg_data is None:
        cmtg_data = etl_parser.get_mmio_data(cmtg_offsets.CmtgControlReg)
        if cmtg_data is None:
            return None, [(None, None)]
        cmtg_ctl = adapter.regs.get_cmtg_info(panel.transcoder_type, CmtgOffsetValues(CmtgControlReg=cmtg_data[0].Data))
        if cmtg_ctl.CmtgEnable == 0:
            return None, [(None, None)]
        return [(None, None)], None

    enabled_region = []
    disabled_region = []
    prev_time = None
    cmtg_disabled = True
    for mmio_data in cmtg_data:
        cmtg_val = adapter.regs.get_cmtg_info(panel.transcoder_type, CmtgOffsetValues(CmtgControlReg=mmio_data.Data))
        cmtg_disabled = (cmtg_val.CmtgEnable == 0)
        if cmtg_disabled:
            enabled_region.append((prev_time, mmio_data.TimeStamp))
            prev_time = mmio_data.TimeStamp
        else:
            disabled_region.append((prev_time, mmio_data.TimeStamp))
            prev_time = mmio_data.TimeStamp
    if cmtg_disabled:
        disabled_region.append((prev_time, None))
    else:
        enabled_region.append((prev_time, None))
    return enabled_region, disabled_region


##
# @brief        Internal function to check if RR programming is happening in active region in a given timeline
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    is_clock_based boolean, Yes for LRR1.0 & No for LRR2.5
# @param[in]    start_time object, startTime
# @param[in]    end_time object, endTime
# @param[in]    is_cmtg boolean, whether this is CMTG case or not
# @return       True for successful, False for failed
def __check_rr_in_active_region(adapter: Adapter, panel: Panel, is_clock_based, start_time, end_time, is_cmtg):
    if is_cmtg is True:
        if adapter.name in common.PRE_GEN_13_PLATFORMS + ["DG2"]:
            logging.error("\t\tCMTG is not supported on pre-ADLP platforms")
            return False
        timing_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
        rr_offset = timing_offsets.CmtgLinkMReg if is_clock_based else timing_offsets.CmtgVTotalReg
        scanline_offset = MMIORegister.get_instance("SCANLINE_DC6V_REGISTER", "SCANLINE_DC6V", adapter.name).offset
    else:
        timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)
        rr_offset = timing_offsets.LinkM if is_clock_based else timing_offsets.VTotal
        scanline_offset = MMIORegister.get_instance("PIPE_SCANLINE_REGISTER", "PIPE_SCANLINE_" + panel.pipe,
                                                    adapter.name).offset

    rr_mmio_output = etl_parser.get_mmio_data(rr_offset, is_write=True, start_time=start_time, end_time=end_time)
    if rr_mmio_output is None:  # No RR change seen in the given range, so nothing to verify
        return True
    scanline_mmio_output = etl_parser.get_mmio_data(scanline_offset, start_time=start_time, end_time=end_time)
    data_dict = {mmio.TimeStamp: mmio.Offset for mmio in rr_mmio_output}
    scanline_data_dict = {}
    if scanline_mmio_output is not None:
        data_dict.update({mmio.TimeStamp: mmio.Offset for mmio in scanline_mmio_output})
        # Convert list of object to dictionary {time_stamp : data}
        scanline_data_dict.update({mmio.TimeStamp: mmio.Data for mmio in scanline_mmio_output})
    # RR mmio is programmed from set timing as well where scanline counter is not read
    settiming_output = etl_parser.get_event_data(etl_parser.Events.SET_TIMING, start_time=start_time, end_time=end_time)
    if settiming_output is not None:
        data_dict.update({set_timing.TimeStamp: set_timing for set_timing in settiming_output})
    # Order the dictionary with time_stamp
    data_dict = OrderedDict(sorted(data_dict.items()))
    vactive = panel.native_mode.VtRes
    last_scanline_read = None
    skip_next_rr_program_check = False
    status = True
    for time_stamp, data in data_dict.items():
        if type(data) is etl_parser.SetTimingData:
            skip_next_rr_program_check = True  # Its set timing event
            logging.info(f"\t\t{data}")
            continue

        if data == scanline_offset:
            last_scanline_read = time_stamp

        if data == rr_offset:
            if skip_next_rr_program_check is True:
                skip_next_rr_program_check = False
                logging.info(f"\t\tDue to SetTiming, skipping rr programming check with CMTG= {is_cmtg} "
                             f"via offset {hex(data)} at {time_stamp} m-secs")
                continue

            if last_scanline_read is None or ((time_stamp - last_scanline_read) > 1):  # 1ms
                logging.error(f"\t\tNo scanline counter read "
                              f"before programming offset {hex(data)} at {time_stamp} m-secs")
                status = False
            else:
                # Bspec reference - https://gfxspecs.intel.com/Predator/Home/Index/65453
                if scanline_data_dict[last_scanline_read] > vactive:
                    logging.error(f"\t\tScanline counter read is not within V_ACTIVE range ({'0 - ' + vactive}) "
                                  f"before programming offset {hex(data)} at {time_stamp} m-secs")
                    status = False
                else:
                    logging.info(f"\t\tRR programmed with CMTG= {is_cmtg} via offset {hex(data)} with scanline "
                                 f"{scanline_data_dict[last_scanline_read]} at {time_stamp} m-secs")
            last_scanline_read = None
    return status
