########################################################################################################################
# @file         mmio_optimize.py
# @brief        The test script contains Etl parsing logic for mmio optimizations
# @author       Pai, Vinayak1
########################################################################################################################
import logging

from Libs.Core import etl_parser
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

VBLANK_MAX_DURATION = 0xFFFFFFFF

exclusion_register_offset_list = [
    # Common FlipQ register offsets for Gen 12, 13, 14, 15
    0x90008, 0x90188, 0x98008, 0x98188, 0x52008, 0x52188, 0x59008, 0x59188, 0x9000c, 0x9018c, 0x9800c, 0x9818c, 0x5200c,
    0x5218c, 0x5900c, 0x5918c, 0x90010, 0x90190, 0x98010, 0x98190, 0x52010, 0x52190, 0x59010, 0x59190, 0x90014, 0x90194,
    0x98014, 0x98194, 0x52014, 0x52194, 0x59014, 0x59194, 0x90018, 0x90198, 0x98018, 0x98198, 0x52018, 0x52198, 0x59018,
    0x59198, 0x90148, 0x902C8, 0x98148, 0x982C8, 0x52148, 0x522C8, 0x59148, 0x592C8,

    # FlipQ register offsets specific for Gen 12
    0x5f128, 0x5f138, 0x5f528, 0x5f538, 0x5f928, 0x5f938, 0x5fd28, 0x5fd38, 0x5f12C, 0x5f13C, 0x5f52C, 0x5f53C, 0x5f92C,
    0x5f93C, 0x5fd2C, 0x5fd3C, 0x85FB4, 0x85FAC, 0x85FA8, 0x8013C,

    # PIPEDMC_CHICKEN
    0x92084, 0x96084, 0x9a084, 0x9e084,

    # PIPEDMC_EVT_CTL
    0x5F034, 0x5F038, 0x5F03C, 0x5F040, 0x5F044, 0x5F048, 0x5F04C, 0x5F050, 0x5F434, 0x5F438, 0x5F43C, 0x5F440, 0x5F444,
    0x5F448, 0x5F44C, 0x5F450, 0x5F834, 0x5F838, 0x5F83C, 0x5F840, 0x5F844, 0x5F848, 0x5F84C, 0x5F850, 0x5FC34, 0x5FC38,
    0x5FC3C, 0x5FC40, 0x5FC44, 0x5FC48, 0x5FC4C, 0x5FC50,

    # PIPEDMC_SCANLINECMPLOWER
    0x5F120, 0x5F520, 0x5F920, 0x5FD20,

    # PIPEDMC_SCANLINECMPUPPER
    0x5F124, 0x5F524, 0x5F924, 0x5FD24,

    # PIPEDMC_FQ_CTRL_A
    0x5F078, 0x5F478, 0x5F878, 0x5FC78,

    # PIPEDMC_FPQ1_HP
    0x5F128, 0x5F528, 0x5F928, 0x5FD28,

    # PIPEDMC_FPQ1_TP
    0x5F12C, 0x5F52C, 0x5F92C, 0x5FD2C,

    # PIPEDMC_FPQ1_CHP
    0x5F130, 0x5F530, 0x5F930, 0x5FD30,

    # PIPEDMC_FPQ2_HP
    0x5F138, 0x5F538, 0x5F938, 0x5FD38,

    # PIPEDMC_FPQ2_TP
    0x5F13C, 0x5F53C, 0x5F93C, 0x5FD3C,

    # PIPEDMC_FPQ2_CHP
    0x5F140, 0x5F540, 0x5F940, 0x5FD40,

    # PIPEC_DMC_SIMPLEFQ_BASE
    0x52008, 0x59008, 0x90008, 0x98008,

    # PIPEDMC_CHICKEN
    0x5F084, 0x5F484, 0x5F884, 0x5FC84,

    # PIPEDMC_FRAMECOUNT_CMTG
    0x5F148, 0x5F548, 0x5F948, 0x5FD48,

    # PIPEDMC_FQ_STATUS
    0x5F098, 0x5F498, 0x5F898, 0x5FC98,

    # PIPEDMC_FPQ1_HP
    0x5F128, 0x5F138, 0x5F168, 0x5F174, 0x5F180, 0x5F528, 0x5F538, 0x5F568, 0x5F574, 0x5F580, 0x5F928, 0x5F938, 0x5F968,
    0x5F974,
    0x5F980, 0x5FD28, 0x5FD38, 0x5FD68, 0x5FD74, 0x5FD80,

    # PIPEDMC_FPQ1_CHP
    0x5F130, 0x5F140, 0x5F170, 0x5F17C, 0x5F188, 0x5F530, 0x5F540, 0x5F570, 0x5F57C, 0x5F588, 0x5F930, 0x5F940, 0x5F970,
    0x5F97C, 0x5F988, 0x5FD30, 0x5FD40, 0x5FD70, 0x5FD7C, 0x5FD88,

    # PIPEDMC_FPQ_ATOMIC
    0x5F0A0, 0x5F4A0, 0x5F8A0, 0x5FCA0,

    # PIPEDMC_FPQ_TS
    0x5F134, 0x5F534, 0x5F934, 0x5FD34,

    # PIPEDMC_FPQ_CTL
    0x5F160, 0x5F560, 0x5F960, 0x5FD60,

    # DMC_FQ_W2_PTS_CFG_SEL
    0x8F240,

    # PIPEDMC_VBI_MASK_CTL
    0x5F07C, 0x5F47C, 0x5F87C, 0x5FC7C,

    # SCANLINE_DC6V
    0x4559C,

    # GT Offset not display related
    0x145984,

    # FlipQ RAM Offsets for PIPE A
    0x90008, 0x9000C, 0x90010, 0x90014, 0x90018, 0x9001C, 0x90020, 0x90024, 0x90028, 0x9002C, 0x90030, 0x90034, 0x90038,
    0x9003C, 0x90040, 0x90044, 0x90048, 0x9004C, 0x90050, 0x90054, 0x90058, 0x9005C, 0x90060, 0x90064, 0x90068, 0x9006C,
    0x90070, 0x90074, 0x90078, 0x9007C, 0x90080, 0x90084, 0x90088, 0x9008C, 0x90090, 0x90094, 0x90098, 0x9009C, 0x900A0,
    0x900A4,

    # FLipQ RAM Offsets PIPE B
    0x98008, 0x9800C, 0x98010, 0x98014, 0x98018, 0x9801C, 0x98020, 0x98024, 0x98028, 0x9802C, 0x98030, 0x98034, 0x98038,
    0x9803C, 0x98040, 0x98044, 0x98048, 0x9804C, 0x98050, 0x98054, 0x98058, 0x9805C, 0x98060, 0x98064, 0x98068, 0x9806C,
    0x98070, 0x98074, 0x98078, 0x9807C, 0x98080, 0x98084, 0x98088, 0x9808C, 0x98090, 0x98094, 0x98098, 0x9809C, 0x980A0,
    0x980A4,

    # FlipQ RAM Offsets PIPE C
    0x52008, 0x5200C, 0x52010, 0x52014, 0x52018, 0x5201C, 0x52020, 0x52024, 0x52028, 0x5202C, 0x52030, 0x52034, 0x52038,
    0x5203C, 0x52040, 0x52044, 0x52048, 0x5204C, 0x52050, 0x52054, 0x52058, 0x5205C, 0x52060, 0x52064, 0x52068, 0x5206C,
    0x52070, 0x52074, 0x52078, 0x5207C, 0x52080, 0x52084, 0x52088, 0x5208C, 0x52090, 0x52094, 0x52098, 0x5209C, 0x520A0,
    0x520A4,

    # FlipQ RAM Offsets PIPE D
    0x59008, 0x5900C, 0x59010, 0x59014, 0x59018, 0x5901C, 0x59020, 0x59024, 0x59028, 0x5902C, 0x59030, 0x59034, 0x59038,
    0x5903C, 0x59040, 0x59044, 0x59048, 0x5904C, 0x59050, 0x59054, 0x59058, 0x5905C, 0x59060, 0x59064, 0x59068, 0x5906C,
    0x59070, 0x59074, 0x59078, 0x5907C, 0x59080, 0x59084, 0x59088, 0x5908C, 0x59090, 0x59094, 0x59098, 0x5909C, 0x590A0,
    0x590A4
]

# The SCANLINE_DC6V_ADDR, PIPEDMC_FRAMECOUNT_CMTG, PIPE_SCANLINE and PIPE_FRMCNT registers are dependent on CMTG
# Enable/Disable state.So, created a separate list of registers that needs to be excluded for enable and disable
# cases of CMTG.
cmtg_enable_exclusion_offset_list = [
    # SCANLINE_DC6V_ADDR for Gen 13, 14, 15
    0x4559C, 0x455C4,

    # PIPEDMC_FRAMECOUNT_CMTG for Gen 13, 14, 15
    0x5F148, 0x5F548, 0x5F948, 0x5FD48, 0x5F14C, 0x5F54C, 0x5F94C, 0x5FD4C
]

cmtg_disable_exclusion_offset_list = [
    # PIPE_SCANLINE for Gen 13, 14, 15
    0x70000, 0x71000, 0x72000, 0x73000,

    # PIPE_FRMCNT for Gen 13, 14, 15
    0x70040, 0x71040, 0x72040, 0x73040
]


##################
# Helper Function
##################

##
# @brief        API to get mmioData based on thread ID
# @param[in]    thread_id   : ThreadId of the process
# @param[in]    is_write    : True or False to filter out read or write operations
# @param[in]    start_time  : Start time in ms
# @param[in]    end_time    : End time in ms
# @param[in]    cmtg_status : True if CMTG is enabled else False
# @return       output     : A list of mmioData objects if successful, None otherwise
def __get_violate_mmio_data(thread_id=None, is_write=None, start_time=None, end_time=None, cmtg_status=False):
    report = etl_parser.__get_report(etl_parser.__ReportNames.MMIO)

    if "mmioDataQueue" not in report.keys():
        return None

    exclusion_register_list = exclusion_register_offset_list + (
        cmtg_enable_exclusion_offset_list if cmtg_status else cmtg_disable_exclusion_offset_list)

    output = []
    for mmio_entry in report["mmioDataQueue"]:
        if mmio_entry['ThreadId'] == thread_id:
            if mmio_entry["Offset"] in exclusion_register_list:
                continue
            if is_write is not None and mmio_entry["IsWrite"] != is_write:
                continue
            if start_time is not None and mmio_entry['TimeStamp'] < start_time:
                continue
            if end_time is not None and mmio_entry['TimeStamp'] > end_time:
                break
            output.append(etl_parser.MmioData(mmio_entry))

    if len(output) == 0:
        return None
    return output


##
# @brief        Helper Function to get DDI timings
# @return       ddi_start_end_timings : (StartTime, EndTime, ThreadID), tuple, a list of tuple having DDI StartTime,
#                                       EndTime and ThreadID
def __ddi_data():
    ddi_start_end_timings = []
    ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY3)
    if ddi_output is None:
        logging.warning("\tNo DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY3 event found in ETLs (Driver Issue)")
        return False

    for each_ddi in ddi_output:
        ddi_start_end_timings.append((each_ddi.StartTime, each_ddi.EndTime, each_ddi.ThreadID))
    return ddi_start_end_timings


##
# @brief            Helper function to get non zero duration
# @param[in]        panel  : Panel Object
# @return           Timestamp if non zero duration is present else False
def __non_zero_duration(panel):
    # Get the flip data and check if the flip has a duration
    flip_data = etl_parser.get_flip_data(f"PIPE_{panel.pipe}")
    if flip_data is None:
        logging.warning(f"\tNo flip data found for PIPE_{panel.pipe}")
        return False

    logging.info(f"\tIncoming flips on PIPE_{panel.pipe} : {len(flip_data)}")
    for flip in flip_data:
        # Skip the flips with plane disable call, these flips might have unexpected data.
        is_plane_disable_call = False
        for plane_info in flip.PlaneInfoList:
            if plane_info.Flags == "":
                is_plane_disable_call = True
                logging.info("\tSkipping: Flip found with plane disable call (it might have unexpected data)")
                break
        if is_plane_disable_call:
            logging.debug(f"\tSkipped plane disable flip for duration calculation")
            logging.debug(f"\t\t{flip}")
            continue

        if flip.Duration != 0 and flip.Duration != VBLANK_MAX_DURATION:
            logging.info(f"Non-zero duration flip found at {flip.TimeStamp}")
            return flip.TimeStamp
    logging.error(f"No non-zero duration flips found")
    return False


##
# @brief        Helper function to fetch PSR2 disable time
# @param[in]    panel     : Panel Object
# @param[in]    adapter   : Adapter Object
# @return       timestamp : Timestamp at which PSR2 was disabled
def psr_disable_check(panel, adapter):
    if panel.psr_caps.is_psr2_supported:
        psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", f"PSR2_CTL_{panel.transcoder}", adapter.name)
        if adapter.name in common.PRE_GEN_14_PLATFORMS:
            psr2_val = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True)
        else:
            # from GEN14+, Driver will write first 16 bits & last 16 bit's separately to avoid synchronization issues
            psr2_val = etl_parser.get_mmio_data(0x60902, is_write=True)

        for val in psr2_val:
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                psr2_ctl.asUint = val.Data
            else:
                psr2_ctl.asUint = val.Data << 16
            if psr2_ctl.psr2_enable == 0:
                logging.info(f"PSR2 disabled at {val.TimeStamp}")
                return val.TimeStamp
    else:
        logging.info("Skipping PSR2 verification")
        return None


##
# @brief        Helper function to check CMTG enable status
# @param[in]    adapter : Adapter Object
# @return       status  : True if CMTG is enabled else False
def cmtg_enable_status(adapter):
    if adapter.name not in ['LNL']:
        cmtg_ctl = MMIORegister.read("TRANS_CMTG_CTL_REGISTER", 'TRANS_CMTG_CTL', adapter.name)
        logging.debug(f"CMTG Enable Status: {True if cmtg_ctl.cmtg_enable == 1 else False}")
        return True if cmtg_ctl.cmtg_enable == 1 else False


##
# @brief        Exposed API to verify mmioData when DC6v is enabled
# @param[in]    etl_file                : Name of the ETL file to be verified
# @param[in]    panel                   : Panel Object
# @param[in]    adapter                 : Adapter Object
# @param[in]    cmtg_status             : True if CMTG is enabled else False
# @return       status, register_offsets
def verify_mmio_data(etl_file, panel, adapter, cmtg_status):
    status = True
    register_offsets = set()
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False

    first_non_zero_timestamp = __non_zero_duration(panel)
    psr2_disable_timestamp = psr_disable_check(panel, adapter)
    ddi_start_end_timings = __ddi_data()

    for each_time in ddi_start_end_timings:
        flip_data = etl_parser.get_flip_data(pipe=f"PIPE_{panel.pipe}", start_time=each_time[0], end_time=each_time[1])

        if flip_data is None:
            logging.warning("\tFAIL: No flip data present in ETL file")
            continue

        for each_flip in flip_data:
            # MMIO Optimization does not support all param flips, so skipping it
            if each_flip.IsAllParam:
                continue
            # MMIO optimization does not support async flips, so skipping it
            for plane_info in each_flip.PlaneInfoList:
                if "FlipImmediate" in plane_info.Flags:
                    continue
            if each_flip.IsAddressOnly:
                logging.debug("Address only Flips")
                for flip_address in each_flip.FlipAddressList:
                    if flip_address.OutFlags == "SubmittedAsCpuMmio":
                        continue
                    if flip_address.OutFlags == "SubmittedToHwQueue":
                        logging.debug(f"Start-Time:{each_time[0]} - End-Time: {each_time[1]}")
                        # Cond 1: If panel is PSR2 supported then we do not consider the flips from time when first
                        #         non-zero duration flip is found till PSR2 is disabled.
                        if panel.psr_caps.is_psr2_supported:
                            if (first_non_zero_timestamp < each_time[0] < psr2_disable_timestamp and
                                    first_non_zero_timestamp < each_time[1] < psr2_disable_timestamp):
                                continue
                        # Cond 2: For the first non duration flip, the WM gets re-calculated. So, need to skip the flip
                        #         that has the start time similar to the first non duration flip.
                        if each_time[0] < first_non_zero_timestamp < each_time[1]:
                            continue
                        output = __get_violate_mmio_data(thread_id=each_time[2], start_time=each_time[0],
                                                         end_time=each_time[1],
                                                         cmtg_status=cmtg_status)
                        if output is not None:
                            status = False
                            for each_output in output:
                                register_offsets.add(hex(each_output.Offset))
                                logging.debug(''.center(64, "*"))
                                logging.debug(f"MMIO Data:{register_offsets}")
                                logging.debug(''.center(64, "*"))

    if status:
        logging.info("PASS: No MMIO read or write data found when DC6v is enabled")
    else:
        logging.info("FAIL: MMIO read or write found when DC6v is enabled")
    return status, register_offsets
