#####################################################################################################################################
# @file         display_transcoder.py
# @brief        Python wrapper exposes interfaces for Display Port/Transcoder
# @details      display_transcoder.py provides interface's to Verify Display Port/Transcoder
#               Configuration for all connected displays : check if transcoder is enabled,
#               transcoder to DDI port mapping, verify Link M/N and Data M/N values,
#               verify transcoder timing for eDP, DSI, HDMI, DP display
#               User-Input : DisplayTranscoder() object - targetID, platform name(skl,icl,..)
#               Display Transcoder information mentioned below: \n
# @note         Supported display interfaces are MIPI, EDP, DP, HDMI\n
# @author       Aafiya Kaleem
####################################################################################################################################

import importlib
import logging
import os
import math
from typing import Dict

from Libs.Core import display_utility
from Libs.Core import driver_escape
from Libs.Core import enum
from Libs.Core import system_utility as sys_utility
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.machine_info.machine_info import SystemInfo, PRE_GEN_16_PLATFORMS
from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock import display_clock
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.display_port import dpcd_helper as dpcd
from Libs.Feature.display_port.dp_helper import DPHelper
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Feature.vdsc.dsc_enum_constants import DPCDOffsets
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.EDP.MSO import mso
from Tests.PowerCons.Modules import dpcd as dpcd_mso
from registers.mmioregister import MMIORegister

clock_helper = clk_helper.ClockHelper()

logger_template = "{res:^5}: {feature:<60}: Expected: {exp:<20}  Actual: {act}"


##
# @brief    DisplayTranscoder Base Class. Has functions for Transcoder verification
class DisplayTranscoder(display_base.DisplayBase):

    ##
    # @brief        Initializes Display Transcoder Object
    # @param[in]    display_port display to create the object for
    # @param[in]    hactive Width of Transcoder active area
    # @param[in]    vactive Height of Transcoder active area
    # @param[in]    htotal total height of transcoder
    # @param[in]    vtotal total width of transcoder
    # @param[in]    rrate refresh rate
    # @param[in]    pixelClock_Hz Pixel clock in Hz
    # @param[in]    bpc bits per component
    # @param[in]    LTE340MhzScramble scrambling enable option
    # @param[in]    pipe_color_space RGB/YUV
    # @param[in]    gfx_index
    def __init__(self, display_port=None, hactive=None, vactive=None,
                 htotal=None, vtotal=None, rrate=None, pixelClock_Hz=None,
                 bpc=None, LTE340MhzScramble=None, pipe_color_space="RGB", gfx_index='gfx_0'):
        self.display_port = display_port
        self.hactive = hactive
        self.vactive = vactive
        self.htotal = htotal
        self.vtotal = vtotal
        self.rrate = rrate
        self.pixelClock_Hz = pixelClock_Hz
        self.bpc = bpc
        self.LTE340MhzScramble = LTE340MhzScramble
        self.pipe_color_space = pipe_color_space
        display_base.DisplayBase.__init__(self, display_port, gfx_index=gfx_index)


##
# @brief        Get the Link M/N values programmed for each transcoder
# @param[in]    portObj DisplayTranscoder() object
# @param[in]    connector_port display port name
# @param[in]    gfx_index graphics adapter
# @return       Link M/N value programmed in the MMIO
def GetLinkMNValues(portObj, connector_port, gfx_index='gfx_0'):
    suffix = portObj.pipe_suffix
    if ((connector_port == "DP_A") and (portObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL'])):
        reg = MMIORegister.read("LINKM_REGISTER", "TRANS_LINKM1_EDP", portObj.platform, gfx_index=gfx_index)
        reg_info = "TRANS_LINKM1_EDP"
        logging.debug("TRANS_LINKM1_EDP --> Offset : "
                      + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
        reg1 = MMIORegister.read("LINKN_REGISTER", "TRANS_LINKN1_EDP", portObj.platform, gfx_index=gfx_index)
        logging.debug("TRANS_LINKN1_EDP --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))
        return reg.link_m_value, reg1.link_n_value, reg_info
    else:
        reg = MMIORegister.read("LINKM_REGISTER", "TRANS_LINKM1_%s" % (suffix), portObj.platform, gfx_index=gfx_index)
        reg_info = "TRANS_LINKM1_" + suffix
        logging.debug("TRANS_LINKM1_" + suffix + "  --> Offset : "
                      + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
        reg1 = MMIORegister.read("LINKN_REGISTER", "TRANS_LINKN1_%s" % (suffix), portObj.platform, gfx_index=gfx_index)
        logging.debug("TRANS_LINKN1_" + suffix + "  --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))

        # For HDMI both LinkM And Extended LinkM values will be used for programming. Similarly,LinkN and Extended LinkN
        if connector_port.startswith("HDMI"):
            return reg.asUint, reg1.asUint, reg_info

        return reg.link_m_value, reg1.link_n_value, reg_info


##
# @brief        Get the Data M/N values programmed for each transcoder
# @param[in]    portObj DisplayTrans Object
# @param[in]    connector_port display to verify
# @param[in]    gfx_index graphics adapter
# @return       Data M/N value programmed in the MMIO
def GetDataMNValues(portObj, connector_port, gfx_index='gfx_0'):
    suffix = portObj.pipe_suffix
    if ((connector_port == "DP_A") and (portObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL'])):
        reg = MMIORegister.read("DATAM_REGISTER", "TRANS_DATAM1_EDP", portObj.platform, gfx_index=gfx_index)
        reg_info = "TRANS_DATAM1_EDP"
        logging.debug("TRANS_DATAM1_EDP --> Offset : "
                      + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
        reg1 = MMIORegister.read("DATAN_REGISTER", "TRANS_DATAN1_EDP", portObj.platform, gfx_index=gfx_index)
        logging.debug("TRANS_DATAN1_EDP --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))
        return reg.data_m_value, reg1.data_n_value, reg_info
    else:
        reg = MMIORegister.read("DATAM_REGISTER", "TRANS_DATAM1_%s" % (suffix), portObj.platform, gfx_index=gfx_index)
        reg_info = "TRANS_DATAM1_" + suffix
        logging.debug("TRANS_DATAM1_" + suffix + " --> Offset : "
                      + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
        reg1 = MMIORegister.read("DATAN_REGISTER", "TRANS_DATAN1_%s" % (suffix), portObj.platform, gfx_index=gfx_index)
        logging.debug("TRANS_DATAN1_" + suffix + " --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))
        return reg.data_m_value, reg1.data_n_value, reg_info


##
# @brief        Verify Link M/N and Data M/N values for active transcoder
# @param[in]    portObj DisplayTrans object structure
# @param[in]    gfx_index graphics adapter
# @return       bool - true if pass, else false
def VerifyTranscoderMNValues(portObj, gfx_index='gfx_0'):
    connector_port = portObj.display_port
    is_edp_drrs = False
    rr_list = set()  # only unique values are added to set , so set is used
    config = display_config.DisplayConfiguration()
    display_and_adapter_info = config.get_display_and_adapter_info_ex(connector_port, gfx_index)
    if type(display_and_adapter_info) is list:
        display_and_adapter_info = display_and_adapter_info[0]

    if (portObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL']):
        transcoder_ddi = portObj.display_port[-1]
    else:
        transcoder_ddi = portObj.pipe_suffix

    is_lfp_dp = display_utility.get_vbt_panel_type(connector_port, 'gfx_0') == display_utility.VbtPanelType.LFP_DP
    if is_lfp_dp:
        all_supported_modes = config.get_all_supported_modes([display_and_adapter_info])
        for _, modes in all_supported_modes.items():
            for mode in modes:
                if mode.refreshRate != 0:
                    rr_list.add(mode.refreshRate)  # mode structure has pixelclk, but it has value of 0Hz, cannot use it
        # fail safe code: even if get all supported modes fails, add default RR passed in portObj
        # This can prevent empty set and possible divide by 0 errors later
        rr_list.add(round(portObj.rrate))
        rr_list = list(rr_list)
        rr_list.sort()  # increasing order of RRs, set converted to list for sorting
        # if eDP contains multiple RRs, it means seamless DRRS is supported.
        if len(rr_list) > 1:
            is_edp_drrs = True
            logging.info("eDP DRRS is supported, RRs for display {0} are {1}".
                         format(connector_port, rr_list))

    if connector_port.startswith("DP"):
        pixelClock = int(portObj.pixelClock_Hz)
        pixel_clock_hz = pixelClock * 100

        BPP, BPC = display_base.GetTranscoderBPCValue(portObj, gfx_index)
        if BPP == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][TRANSCODER]:ERROR : BPP value is ZERO, NOT Programmed in MMIO",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : BPP value is ZERO, NOT Programmed in MMIO")
            return False

        if ((portObj.display_port == "DP_A") and (
                portObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL'])):
            suffix = "EDP"
        elif portObj.display_port == "MIPI_A":
            suffix = "DSI0"
        elif portObj.display_port == "MIPI_C":
            suffix = "DSI1"
        else:
            suffix = portObj.pipe_suffix

        DdiFuncCtl = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL_%s" % (suffix),
                                       portObj.platform, gfx_index=gfx_index)

        trans_ddi_func_ctl = importlib.import_module(
            "registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (portObj.platform.lower()))

        is_mst = DdiFuncCtl.trans_ddi_mode_select == getattr(trans_ddi_func_ctl, 'trans_ddi_mode_select_DP_MST')

        link_rate_gbps: float = dpcd.DPCD_getPanelMaxLinkRate(display_and_adapter_info)
        is_128b_132b_encoding = True if link_rate_gbps >= 10 else False

        # On DG2 when pixel clock is > 1250 MHz, driver will fall back to HBR3 link rate in case of DP 2.1 SST SBM or
        # DP 2.1 SST Display. This is because of HW bug on DG2. Hence, making is_128b_132b_encoding as False for this
        # case.
        is_acmp = True if SystemInfo().get_sku_name(gfx_index).upper() == "ACMP" else False
        if portObj.platform == "DG2" and is_acmp is False:
            mstm_cap = DSCHelper.read_dpcd(gfx_index, portObj.display_port, DPCDOffsets.MSTM_CAP)[0]
            is_single_stream = is_128b_132b_encoding and ((mstm_cap == 0x2) or (mstm_cap == 0x0))
            logging.info(f"Is Single Stream Display: {is_single_stream}")

            if is_single_stream and (pixel_clock_hz / (1000 * 1000)) >= 1250:
                is_128b_132b_encoding = False

        color_format = ColorFormat.RGB
        if portObj.pipe_color_space == "YUV420":
            color_format = ColorFormat.YUV420
        elif portObj.pipe_color_space == "YUV422":
            color_format = ColorFormat.YUV422

        is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, portObj.display_port)
        is_dsc_hw_improvements_not_implemented = DSCHelper.is_dsc_hw_improvements_not_implemented_platform(
            gfx_index, portObj.platform
        )
        bits_per_pixel, bytes_per_pixel = DPHelper.get_bits_and_bytes_per_pixel(
            gfx_index, portObj.pipe_suffix, BPC, color_format, is_compression_enabled
        )

        # New MNTU calculation is used for DP2.0/DP 2.1 displays or if display is not LFP DP (EDP) and if compression
        # is enabled and if the platform has DSC HW improvements implemented.
        if (
                (is_128b_132b_encoding is True) or
                ((is_lfp_dp is False) and is_compression_enabled and (is_dsc_hw_improvements_not_implemented is False))
        ):
            is_link_bw_sufficient, *mn_values = DPHelper.get_link_data_m_n_values_considering_eoc(
                display_and_adapter_info, portObj.pipe_suffix, portObj.hactive, pixel_clock_hz, bits_per_pixel
            )
        elif is_mst is True:
            is_link_bw_sufficient, *mn_values = DPHelper.get_mst_link_data_m_n_values(
                display_and_adapter_info, pixel_clock_hz, bits_per_pixel
            )
        else:
            is_link_bw_sufficient, *mn_values = DPHelper.get_sst_link_data_mn_values(
                display_and_adapter_info, portObj.pipe_suffix, pixel_clock_hz, color_format, BPC, bytes_per_pixel,
                bits_per_pixel
            )

        link_dm, link_dn, data_dm, data_dn = mn_values

        # Checking if its EDP DRRS panel here as for DRRS panel we might not get the right data and pixel clock needs to
        # be adjusted which is taken care at later stage.
        if is_edp_drrs is False and is_link_bw_sufficient is False:
            logging.error("[Driver Issue] - Insufficient Link Bandwidth")
            gdhm.report_driver_bug_di(
                title=f'[Interfaces][Display_Engine][DRRS] Insufficient link bandwidth!. '
            )
            return False

        if portObj.platform == "DG2" and is_acmp is False:
            is_dp2p0 = DdiFuncCtl.trans_ddi_mode_select == getattr(trans_ddi_func_ctl,
                                                                   'trans_ddi_mode_select_128b_132b_mode')
            if is_dp2p0 and (link_dm / link_dn) > 4:
                logging.error("[Driver Issue] - LINK M / LINK N should not be greater than 4 in case of DP 2.0 on DG2")
                gdhm.report_driver_bug_di(
                    title=f'[Interfaces][Display_Engine][DRRS] LINK M / LINK N should not be greater than 4 in case of DP 2.0 on DG2!. '
                )
                return False
        elif portObj.platform == "ELG" and (link_dm / link_dn) > 10:
            logging.error("[Driver Issue] - LINK M / LINK N should not be greater than 10 on BMG")
            gdhm.report_driver_bug_di(
                title=f'[Interfaces][Display_Engine] LINK M / LINK N should not be greater than 10 on BMG.')
            return False

        # If provided panel is MSO supported then divide link_dm by number of segments
        if (display_utility.get_vbt_panel_type(connector_port, gfx_index) == display_utility.VbtPanelType.LFP_DP) and \
                (mso.is_mso_supported_in_panel(portObj.targetId)):
            mso_caps = dpcd_mso.EdpMsoCaps(portObj.targetId)
            link_dm = int(link_dm / mso_caps.no_of_links)

        # LINK and DATA M/N Values
        link_m, link_n, reg_link = GetLinkMNValues(portObj, connector_port, gfx_index)
        data_m, data_n, reg_data = GetDataMNValues(portObj, connector_port, gfx_index)

        if (link_m == link_dm) and (data_m == data_dm) and (link_n == link_dn) and (data_n == data_dn):

            logging.info(logger_template.format(res="PASS", feature="{} - (LINKM,LINKN) ".format(reg_link),
                                                exp="{},{}".format(link_dm, link_dn),
                                                act="{},{}".format(link_m, link_n)))
            logging.info(logger_template.format(res="PASS", feature="{} - (DATAM,DATAN) ".format(reg_data),
                                                exp="{},{}".format(data_dm, data_dn),
                                                act="{},{}".format(data_m, data_n)))
            logging.debug("PASS : Link M/N and Data M/N values are correct")
            return True

        # With eDP DRRS panel, RR will be dynamically varying, and link_m, data_m values along with it
        # This is not known by OS. So, OS will still return nominal RR with QDC call
        # If value mismatches with this RR, re-try verification with min and max RR and check if result in allowed range
        elif is_edp_drrs and ((link_m != link_dm) or (data_m != data_dm)):
            logging.info(logger_template.format(res="", feature="(LINKM,DATAM)",
                                                exp="{},{}".format(link_dm, data_dm),
                                                act="{},{}".format(link_m, data_m)))
            logging.warning("WARNING: LINKM or DATAM values are not matching w.r.t nominal RR. "
                            "It might have switched to lower RR due to eDP DRRS. So re-trying with other RRs.")
            link_dm_values = []
            data_dm_values = []
            for rr in rr_list:
                # no way to get pixel clocks for other RRs directly, so coming up with approximation
                # TODO: revisit this code if get_all_supported_modes() returns pixel clocks for other RRs
                pixelclock_temp = (rr * pixel_clock_hz) / rr_list[-1]
                # for lower pixel clocks , adding 10 % relaxation, another WA to handle DRRS
                if pixelclock_temp < pixel_clock_hz:
                    pixelclock_temp = (pixelclock_temp * 9) / 10

                is_link_bw_sufficient, link_dm, link_dn, data_dm, data_dn = DPHelper.get_sst_link_data_mn_values(
                    display_and_adapter_info, portObj.pipe_suffix, pixelclock_temp, color_format, BPC, bytes_per_pixel,
                    bits_per_pixel)

                if is_link_bw_sufficient is False:
                    logging.error("[Driver Issue][Display_Engine][DRRS] - Insufficient Link Bandwidth")
                    gdhm.report_driver_bug_di(
                        title=f'[Interfaces][Display_Engine][DRRS] Insufficient link bandwidth!. '
                    )
                    return False

                link_dm_values.append(link_dm)
                data_dm_values.append(data_dm)
            if ((link_m >= min(link_dm_values)) and (link_m <= max(link_dm_values)) and (data_m >= min(data_dm_values))
                    and (data_m <= max(data_dm_values)) and (link_n == link_dn) and (data_n == data_dn)):
                logging.info(logger_template.format(res="PASS", feature="{} - (LINKM,LINKN) ".format(reg_link),
                                                    exp="value in range of {} to {},{}".
                                                    format(min(link_dm_values), max(link_dm_values), link_dn),
                                                    act="{},{}".format(link_m, link_n)))
                logging.info(logger_template.format(res="PASS", feature="{} - (DATAM,DATAN) ".format(reg_data),
                                                    exp="value in range of {} to {},{}".
                                                    format(min(data_dm_values), max(data_dm_values), data_dn),
                                                    act="{},{}".format(data_m, data_n)))
                logging.debug("PASS : Link M/N and Data M/N values are correct")
                return True
            else:
                logging.error(logger_template.format(res="FAIL", feature="{} - (LINKM,LINKN)".format(reg_link),
                                                     exp="value not in range of {} to {},{}".
                                                     format(min(link_dm_values), max(link_dm_values), link_dn),
                                                     act="{},{}".format(link_m, link_n)))
                logging.error(logger_template.format(res="FAIL", feature="{} - (DATAM,DATAN) ".format(reg_data),
                                                     exp="value not in range of {} to {},{}".
                                                     format(min(data_dm_values), max(data_dm_values), data_dn),
                                                     act="{},{}".format(data_m, data_n)))
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][TRANSCODER]:Link M/N and Data M/N values are NOT Programmed "
                          "Correctly for EDP_DRRS",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL : Link M/N and Data M/N values are NOT Programmed Correctly")
                return False

        else:
            logging.error(logger_template.format(res="FAIL", feature="{} - (LINKM,LINKN)".format(reg_link),
                                                 exp="{},{}".format(link_dm, link_dn),
                                                 act="{},{}".format(link_m, link_n)))
            logging.error(logger_template.format(res="FAIL", feature="{} - (DATAM,DATAN) ".format(reg_data),
                                                 exp="{},{}".format(data_dm, data_dn),
                                                 act="{},{}".format(data_m, data_n)))
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][TRANSCODER]:Link M/N and Data M/N values are NOT Programmed "
                      "Correctly",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL : Link M/N and Data M/N values are NOT Programmed Correctly")
            return False

    if connector_port.startswith("HDMI"):
        return verify_link_mn_values_for_hdmi_2_1(portObj, gfx_index)

    return True


##
# @brief        Verify transcoder timing data with the register programmed values
# @param[in]    portObj DisplayTranscoder object
# @param[in]    gfx_index graphics adapter
# @return       bool - true if pass, else false
def VerifyTranscoderTiming(portObj, gfx_index='gfx_0'):
    if (portObj.display_port == "DP_A") and (portObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL']):
        suffix = "EDP"
    elif portObj.display_port == "MIPI_A":
        suffix = "DSI0"
    elif portObj.display_port == "MIPI_C":
        suffix = "DSI1"
    elif (portObj.display_port == "WD_0"):
        suffix = "WD0"
    elif (portObj.display_port == "WD_1"):
        suffix = "WD1"
    else:
        suffix = portObj.pipe_suffix

    reg = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_%s" % (suffix), portObj.platform,
                            gfx_index=gfx_index)
    logging.debug("TRANS_HTOTAL_" + suffix + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
    if portObj.platform in PRE_GEN_16_PLATFORMS:
        reg1 = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_%s" % (suffix), portObj.platform,
                                 gfx_index=gfx_index)
        logging.debug("TRANS_VTOTAL_" + suffix + " --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))
        vtotal = reg1.vertical_total
        trans_vtotal = "TRANS_VTOTAL_"
    else:
        reg1 = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_%s" % (suffix), portObj.platform,
                                 gfx_index=gfx_index)
        logging.debug("TRANS_VTOTAL_" + suffix + " --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))
        reg2 = MMIORegister.read("TRANS_VRR_VMAX_REGISTER", "TRANS_VRR_VMAX_%s" % (suffix), portObj.platform,
                                 gfx_index=gfx_index)
        logging.debug("TRANS_VRR_VMAX_" + suffix + " --> Offset : "
                      + format(reg2.offset, '08X') + " Value :" + format(reg2.asUint, '08X'))
        vtotal = reg2.vrr_vmax
        trans_vtotal = "TRANS_VRR_VMAX_"

    # If provided panel is MSO supported then divide H_TOTAL and H_ACTIVE values by number of segments
    if (display_utility.get_vbt_panel_type(portObj.display_port, gfx_index) == display_utility.VbtPanelType.LFP_DP) and \
            (mso.is_mso_supported_in_panel(portObj.targetId)):
        mso_caps = dpcd_mso.EdpMsoCaps(portObj.targetId)
        portObj.htotal = int(portObj.htotal / mso_caps.no_of_links)
        portObj.hactive = int(portObj.hactive / mso_caps.no_of_links)

    if ((reg.horizontal_total == (portObj.htotal - 1)) and (reg.horizontal_active == (portObj.hactive - 1))
            and (vtotal == (portObj.vtotal - 1)) and (reg1.vertical_active == (portObj.vactive - 1))):
        logging.info(logger_template.format(res="PASS",
                                            feature="TRANS_HTOTAL_{} & {}{} - (HTOTAL x VTOTAL)".format(
                                                suffix, trans_vtotal, suffix),
                                            exp="{} x {}".format(portObj.htotal, portObj.vtotal),
                                            act="{} x {}".format(reg.horizontal_total + 1, vtotal + 1)))

        logging.info(logger_template.format(res="PASS",
                                            feature="TRANS_HTOTAL_{} & TRANS_VTOTAL_{} - (HACTIVE x VACTIVE)".format(
                                                suffix, suffix),
                                            exp="{} x {}".format(portObj.hactive, portObj.vactive),
                                            act="{} x {}".format(reg.horizontal_active + 1, reg1.vertical_active + 1)))
        if not portObj.display_port.startswith("MIPI_") and not portObj.display_port.startswith("WD_"):
            reg = MMIORegister.read("TRANS_HBLANK_REGISTER", "TRANS_HBLANK_%s" % (suffix), portObj.platform,
                                    gfx_index=gfx_index)
            logging.debug("TRANS_HBLANK_" + suffix + " --> Offset : "
                          + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
            if ((reg.horizontal_blank_end == portObj.htotal - 1) and (
                    reg.horizontal_blank_start == portObj.hactive - 1)):

                logging.info(logger_template.format(res="PASS",
                                                    feature="TRANS_HBLANK_{} - (HBLANK-START x HBLANK-END)".format(
                                                        suffix),
                                                    exp="{} x {}".format(portObj.hactive, portObj.htotal),
                                                    act="{} x {}".format(reg.horizontal_blank_start + 1,
                                                                         reg.horizontal_blank_end + 1)))

                if portObj.platform not in ['TGL', 'RKL', 'ADLS', 'DG1', 'ADLP', 'DG2', 'MTL', 'ELG', 'LNL', 'PTL', 'NVL', 'CLS']:
                    reg = MMIORegister.read("TRANS_VBLANK_REGISTER", "TRANS_VBLANK_%s" % (suffix), portObj.platform,
                                            gfx_index=gfx_index)
                    logging.debug("TRANS_VBLANK_" + suffix + " --> Offset : "
                                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
                    if ((reg.vertical_blank_end == portObj.vtotal - 1) and (
                            reg.vertical_blank_start == portObj.vactive - 1)):
                        logging.info(logger_template.format(res="PASS",
                                                            feature="TRANS_VBLANK_{} - (VBLANK-START x VBLANK-END)".format(
                                                                suffix),
                                                            exp="{} x {}".format(portObj.vactive, portObj.vtotal),
                                                            act="{} x {}".format(reg.vertical_blank_start + 1,
                                                                                 reg.vertical_blank_end + 1)))
                        return True
                    else:
                        gdhm.report_bug(
                            title="[Interfaces][Display_Engine][TRANSCODER]:TRANS_VBLANK_{0} - (VBLANK-START x VBLANK-END) "
                                  "value Mis-Matched! Expected: {1} x {2}, Actual: {3} x {4}".format(
                                suffix, portObj.vactive, portObj.vtotal, reg.vertical_blank_start + 1,
                                                                         reg.vertical_blank_end + 1),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        logging.error(logger_template.format(res="FAIL",
                                                             feature="TRANS_VBLANK_{} - (VBLANK-START x VBLANK-END)".format(
                                                                 suffix),
                                                             exp="{} x {}".format(portObj.vactive, portObj.vtotal),
                                                             act="{} x {}".format(reg.vertical_blank_start + 1,
                                                                                  reg.vertical_blank_end + 1)))
                        return False
                else:
                    logging.info("INFO : Temporary WA:[] Skipping Transcoder VBlank Verification for Gen12+ "
                                 "Platforms".format(portObj.platform))
                    return True

            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][TRANSCODER]:TRANS_HBLANK_{0} - (HBLANK-START x HBLANK-END) "
                          "value Mis-Matched! Expected: {1} x {2}, Actual: {3} x {4}".format(
                        suffix, portObj.hactive, portObj.htotal, reg.horizontal_blank_start + 1,
                                                                 reg.horizontal_blank_end + 1),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(logger_template.format(res="FAIL",
                                                     feature="TRANS_HBLANK_{} - (HBLANK-START x HBLANK-END)".format(
                                                         suffix),
                                                     exp="{} x {}".format(portObj.hactive, portObj.htotal),
                                                     act="{} x {}".format(reg.horizontal_blank_start + 1,
                                                                          reg.horizontal_blank_end + 1)))
            return False
        return True
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][TRANSCODER]:TRANS_HTOTAL_{0} & {1}{0} - (HTOTAL x VTOTAL) "
                  "value Mis-Matched! Expected: {2} x {3}, Actual: {4} x {5}".format(
                suffix, trans_vtotal, portObj.htotal, portObj.vtotal, reg.horizontal_total + 1, vtotal + 1),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL",
                                             feature="TRANS_HTOTAL_{} & {}{} - (HTOTAL x VTOTAL)".format(
                                                 suffix, trans_vtotal, suffix),
                                             exp="{} x {}".format(portObj.htotal, portObj.vtotal),
                                             act="{} x {}".format(reg.horizontal_total + 1, vtotal + 1)))

        gdhm.report_bug(
            title="[Interfaces][Display_Engine][TRANSCODER]:TRANS_HTOTAL_{0} & TRANS_VTOTAL_{0} - (HACTIVE x VACTIVE) "
                  "value Mis-Matched! Expected: {1} x {2}, Actual: {3} x {4}".format(
                suffix, portObj.hactive, portObj.vactive, reg.horizontal_active + 1, reg1.vertical_active + 1),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL",
                                             feature="TRANS_HTOTAL_{} & TRANS_VTOTAL_{} - (HACTIVE x VACTIVE)".format(
                                                 suffix, suffix),
                                             exp="{} x {}".format(portObj.hactive, portObj.vactive),
                                             act="{} x {}".format(reg.horizontal_active + 1, reg1.vertical_active + 1)))
        return False


##
# @brief        Get transcoder to DDI port mapping
# @param[in]    portObj DisplayTranscoder object
# @param[in]    ddi_select DDI to select
# @return       bool true if display is mapped to correct DDI port
def VerifyConnectedDDI(portObj, ddi_select):
    if portObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL']:
        mapped_ddi = display_base.DDI_SELECT(ddi_select).name
    elif portObj.platform in ['DG1', 'RKL']:
        mapped_ddi = display_base.DG1_DDI_SELECT(ddi_select).name
    elif portObj.platform in ['ADLS']:
        mapped_ddi = display_base.ADLS_DDI_SELECT(ddi_select).name
    elif portObj.platform in ['DG2']:
        mapped_ddi = display_base.DG2_DDI_SELECT(ddi_select).name
    elif portObj.platform in ['ADLP']:
        mapped_ddi = display_base.ADLP_DDI_SELECT(ddi_select).name
    elif portObj.platform in ['MTL', 'LNL', 'PTL', 'NVL', 'CLS']:
        mapped_ddi = display_base.MTL_DDI_SELECT(ddi_select).name
    elif portObj.platform in ['ELG']:
        mapped_ddi = display_base.ELG_DDI_SELECT(ddi_select).name
    else:
        mapped_ddi = display_base.GEN11p5_DDI_SELECT(ddi_select).name

    if portObj.ddi == mapped_ddi:
        return True

    gdhm.report_bug(
        title="[Interfaces][Display_Engine][TRANSCODER]:ERROR : Incorrect DDI Mapping while verifying connected DDI",
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )
    logging.error("ERROR : Incorrect DDI Mapping.")
    return False


##
# @brief        Verify the connected port, check transcoder enable along with DDI mapping.
# @param[in]    portObj DisplayTranscoder object
# @param[in]    gfx_index graphics adapter
# @return       bool true if pass, else false
def VerifyConnectedTranscoder(portObj, gfx_index='gfx_0'):
    if (portObj.display_port == "DP_A") and (portObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL']):
        suffix = "EDP"
    elif portObj.display_port == "MIPI_A":
        suffix = "DSI0"
    elif portObj.display_port == "MIPI_C":
        suffix = "DSI1"
    elif (portObj.display_port == "WD_0"):
        suffix = "WD0"
    elif (portObj.display_port == "WD_1"):
        suffix = "WD1"
    else:
        suffix = portObj.pipe_suffix

    reg = MMIORegister.read("TRANS_CONF_REGISTER", "TRANS_CONF_%s" % (suffix), portObj.platform, gfx_index=gfx_index)
    logging.debug("TRANS_CONF_%s" % (suffix) + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
    reg.transcoder_state = 1  # temp assignment for FULSIM

    if (reg.transcoder_enable and reg.transcoder_state and (suffix == "WD0" or suffix == "WD1")):
        reg1 = MMIORegister.read("TRANS_WD_FUNC_CTL_REGISTER", "TRANS_WD_FUNC_CTL_%s" % (suffix[-1]), portObj.platform,
                                 gfx_index=gfx_index)
        logging.debug("TRANS_WD_FUNC_CTL_%s" % (suffix) + " --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))
        return True

    elif (reg.transcoder_enable and reg.transcoder_state):
        reg1 = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL_%s" % (suffix), portObj.platform,
                                 gfx_index=gfx_index)
        logging.debug("TRANS_DDI_FUNC_CTL_%s" % (suffix) + " --> Offset : "
                      + format(reg1.offset, '08X') + " Value :" + format(reg1.asUint, '08X'))
        if (reg1.trans_ddi_function_enable):
            ddi_mode = reg1.trans_ddi_mode_select
            ddi_select = reg1.ddi_select
            if (portObj.display_port.startswith("MIPI_")):
                ddi = True  # DDI mapping is fixed for MIPI ports
            else:
                ddi = VerifyConnectedDDI(portObj, ddi_select)
            if ddi is True:
                logging.debug("INFO : " + portObj.display_port + " Enabled and Connected to " + portObj.ddi)
                return True
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][TRANSCODER]:DDI Transcoder Enable Bit for {} is Disabled! Expected: 1, "
                  "Actual: 0".format(portObj.display_port),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )

        logging.error(logger_template.format(res="FAIL", feature="DDI Transcoder Enable Bit for {} is Disabled".format(
            portObj.display_port), exp="1", act="0"))
        return False


##
# @brief        Verify HDMI Scrambling and TMDS char rate for HDMI port.
# @param[in]    portObj DisplayTranscoder object
# @param[in]    gfx_index graphics adapter
# @return       bool true if pass, else false
def VerifyTMDSCharRateAndScrambling(portObj, gfx_index='gfx_0'):
    frl_status = False
    reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL_%s" % (portObj.pipe_suffix),
                            portObj.platform, gfx_index=gfx_index)
    logging.debug("TRANS_DDI_FUNC_CTL_%s" % (portObj.pipe_suffix) + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))

    # get pixel clock calculated for RGB/YUV pipe color space
    clkObj = display_clock.DisplayClock()
    clock = clkObj.calculate_symbol_freq(portObj.display_port, gfx_index)
    reg_info = "TRANS_DDI_FUNC_CTL_%s" % (portObj.pipe_suffix)
    # Check if the platform is MTL+ and check if FRL is enabled
    if (portObj.platform not in machine_info.PRE_GEN_14_PLATFORMS) and (
            clock_helper.is_hdmi_2_1(portObj.display_port, gfx_index)):
        frl_status = True
    ver_tmds = VerifyTMDSCharRate(clock, reg.high_tmds_char_rate, reg_info, frl_status)

    ver_scrambling = VerifyScrambling(clock, portObj.LTE340MhzScramble, reg.hdmi_scrambling_enabled, reg_info,
                                      frl_status)

    return (ver_tmds and ver_scrambling)


##
# @brief        Verify HDMI TMDS char rate for HDMI port.
# @param[in]    clock - calculated pixel clock for RGB/YUV
# @param[in]    high_tmds_char_rate - clock calculated pixel clock for RGB/YUV
# @param[in]    reg_info - reg bit value for high_tmds_char_rate
# @param[in]    frl_status - if HDMI2.1 or not
# @return       bool - true if pass, else false
def VerifyTMDSCharRate(clock, high_tmds_char_rate, reg_info, frl_status):
    if (clock > 340):
        # TMDS_CHAR_RATE  will be 0 when FRL is enabled even when pixelclock is >340
        if (high_tmds_char_rate == 0) and (frl_status is True):
            logging.info(logger_template.format(res="PASS", feature="{} - High Tmds Char Rate".format(reg_info),
                                                exp="0(DISABLED)", act=high_tmds_char_rate))
            return True

        if (high_tmds_char_rate):
            logging.info(logger_template.format(res="PASS", feature="{} - High Tmds Char Rate".format(reg_info),
                                                exp="1(ENABLED)", act=high_tmds_char_rate))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][TRANSCODER]:{0} - High Tmds Char Rate is disabled! Expected: 1, "
                      "Actual: {1}".format(reg_info, high_tmds_char_rate),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL", feature="{} - High Tmds Char Rate".format(reg_info),
                                                 exp="1(ENABLED)", act=high_tmds_char_rate))
    else:
        if high_tmds_char_rate == 0:
            logging.info(logger_template.format(res="PASS", feature="{} - High Tmds Char Rate".format(reg_info),
                                                exp="0(DISABLED)", act=high_tmds_char_rate))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][TRANSCODER]:{0} - High Tmds Char Rate is enabled! Expected: 0, "
                      "Actual: {1}".format(reg_info, high_tmds_char_rate),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL", feature="{} - High Tmds Char Rate".format(reg_info),
                                                 exp="0(DISABLED)", act=high_tmds_char_rate))
    return False


##
# @brief        Verify HDMI Scrambling for HDMI port.
# @param[in]    clock - calculated pixel clock for RGB/YUV
# @param[in]    LTE340MhzScramble - user input if scrambling need to be enabled
# @param[in]    scrambling - user input if scrambling need to be enable
# @param[in]    reg_info - scrambling reg bit value for hdmi_scrambling_enabled
# @param[in]    frl_status - Checks the FRL status from the EDID
# @return       bool - true if pass, else false
def VerifyScrambling(clock: object, LTE340MhzScramble: object, scrambling: object, reg_info: object,
                     frl_status: object) -> object:

    string = 'DISABLED'
    is_scrambling_required = 0

    if (clock > 340) or LTE340MhzScramble:

        # Scrambling will be 0 when FRL is enabled even when pixelclock is >340
        if (scrambling == 0) and (frl_status is True):
            logging.info(logger_template.format(res="PASS", feature="{} - Scrambling".format(reg_info),
                                                exp="{}({})".format(is_scrambling_required, string), act=scrambling))
            return True
        elif (scrambling == 1) and (frl_status is True):
            logging.error(logger_template.format(res="FAIL", feature="{} - Scrambling".format(reg_info),
                                                exp="{}({})".format(is_scrambling_required, string), act=scrambling))
            gdhm.report_test_bug_di("Scrambling is enabled when FRL is enabled", gdhm.ProblemClassification.FUNCTIONALITY)
            return False

        string = 'ENABLED'
        is_scrambling_required = 1

        if scrambling:
            logging.info(logger_template.format(res="PASS", feature="{} - Scrambling".format(reg_info),
                                                exp="{}({})".format(is_scrambling_required, string), act=scrambling))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][TRANSCODER]:{0} - Scrambling is disabled when clock>340MHz! "
                      "Expected: {1}({2}) Actual: {3}".format(reg_info, is_scrambling_required, string, scrambling),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL", feature="{} - Scrambling".format(reg_info),
                                                 exp="{}({})".format(is_scrambling_required, string), act=scrambling))
    else:
        if scrambling == 0:
            logging.info(logger_template.format(res="PASS", feature="{} - Scrambling".format(reg_info),
                                                exp="{}({})".format(is_scrambling_required, string), act=scrambling))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][TRANSCODER]:{0} - Scrambling is enabled when clock<=340MHz! "
                      "Expected: {1}({2}) Actual: {3}".format(reg_info, is_scrambling_required, string, scrambling),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL", feature="{} - Scrambling".format(reg_info),
                                                 exp="{}({})".format(is_scrambling_required, string), act=scrambling))
    return False


##
# @brief        Verify the BPC value passed by the user for each transcoder
# @param[in]    portObj - display port object
# @param[in]    gfx_index - graphics adapter
# @return       bool - true if pass, else false
def VerifyBPC(portObj, gfx_index='gfx_0'):
    if portObj.bpc is None:
        logging.debug("BPC is NOT Passed as User Input. Skipping the VerifyBPC Check")
        return True

    bpp, bpc = display_base.GetTranscoderBPCValue(portObj, gfx_index)

    if bpc == portObj.bpc:
        logging.info(
            logger_template.format(res="PASS", feature="TRANS_DDI_FUNC_CTL - BPC Value", exp=portObj.bpc, act=bpc))
        return True
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][TRANSCODER]:TRANS_DDI_FUNC_CTL - BPC value Mis-Matched! Expected: {0}, "
                  "Actual: {1}".format(portObj.bpc, bpc),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(
            logger_template.format(res="FAIL", feature="TRANS_DDI_FUNC_CTL - BPC Value", exp=portObj.bpc, act=bpc))
    return False


##
# @brief        Get the display transcoder timings for passed targetID
# @param[in]    portObj DisplayTranscoder() object(passed as reference object)
# @param[in]    gfx_index - graphics adapter
# @return       None
def GetDisplayTimings(portObj, gfx_index='gfx_0'):
    config = display_config.DisplayConfiguration()
    enumerated_displays = config.get_enumerated_display_info()
    display_and_adapter_info = []
    for count in range(enumerated_displays.Count):
        display_name = ((cfg_enum.CONNECTOR_PORT_TYPE(
            enumerated_displays.ConnectedDisplays[count].ConnectorNPortType)).name)
        gfx_adapter = enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
        if ((display_name == portObj.display_port) and (gfx_adapter == gfx_index)):
            display_and_adapter_info.append(enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo)

    display_timings = config.get_display_timings(display_and_adapter_info[0])

    if (portObj.hactive is None or portObj.vactive is None or portObj.htotal is None or
            portObj.vtotal is None or portObj.rrate is None or portObj.pixelClock_Hz is None):
        portObj.hactive = display_timings.hActive
        portObj.vactive = display_timings.vActive
        portObj.htotal = display_timings.hTotal
        portObj.vtotal = display_timings.vTotal
        portObj.rrate = float(display_timings.vSyncNumerator) / float(display_timings.vSyncDenominator)
        portObj.pixelClock_Hz = (float(display_timings.vSyncNumerator) / 100)  # convert to MHz

    if (portObj.LTE340MhzScramble is None):
        portObj.LTE340MhzScramble = 0

    # Added this additional check for ddrw branch since get_timing_info will return raw target timing
    #  where as mainline Escape will handle this requirement.
    sys_util = sys_utility.SystemUtility()
    if sys_util.is_ddrw(gfx_index):
        current_mode = config.get_current_mode(display_and_adapter_info[0])
        if current_mode.scanlineOrdering == enum.INTERLACED:
            portObj.vtotal = portObj.vtotal - 1


##
# @brief        Verify display transcoder programming for all connected displays.
# @param[in]    portList DisplayTranscoder() objects list
# @param[in]    gfx_index graphics adapter
# @return       bool - Return true if transcoder verification passes, else return false
def VerifyTranscoderProgramming(portList, gfx_index='gfx_0'):
    status = fail_count = False

    for portObj in portList:
        if portObj.pipe is None:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][TRANSCODER]:ERROR : {} port is NOT Connected to any Pipe".format(
                    portObj.display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : " + portObj.display_port + " NOT Connected to any Pipe. Check if it is Connected")
            return False

        GetDisplayTimings(portObj, gfx_index)

        logging.info("******* Transcoder Verification for adapter {} -> port {} (Tagrget ID : {}) : {} x {} @ {} "
                     "PixelClock : {} Hz *******".format(gfx_index, str(portObj.display_port), portObj.targetId,
                                                         str(portObj.hactive), str(portObj.vactive), str(portObj.rrate),
                                                         str(portObj.pixelClock_Hz)))

        status = VerifyTranscoderTiming(portObj, gfx_index)
        if status is False:
            fail_count = True

        status = VerifyConnectedTranscoder(portObj, gfx_index)
        if status is False:
            fail_count = True

        if not (portObj.display_port.startswith("WD_")):
            status = VerifyTranscoderMNValues(portObj, gfx_index)
            if (status is False):
                fail_count = True

        status = VerifyBPC(portObj, gfx_index)
        if status is False:
            fail_count = True

        if ((portObj.display_port).startswith("HDMI_") and
                (portObj.platform != 'KBL') and (portObj.platform != 'SKL') and (portObj.platform != 'CFL')):
            status = VerifyTMDSCharRateAndScrambling(portObj, gfx_index)
            status = status and verify_tb_borrowed_for_hdmi_2_1(portObj, gfx_index)
            if status is False:
                fail_count = True

    if fail_count:
        return False
    else:
        return status


##
# @brief        Get PixelClock value from Link M/N and Data M/N values for given connector port
#               Use Only for DP-SST and eDP
# @param[in]    connector_port display port name
# @param[in]    gfx_index graphics adapter
# @return       Pixel Clock value in Hz (0 if Failed)
def GetPixelClockFromDataAndLinkMN(connector_port, gfx_index='gfx_0'):
    # Not Supported for VDSC, COG, DP-MST, DP-TILE
    pixel_clock_hz = 0

    if 'DP' not in connector_port:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][TRANSCODER]:GetPixelClockFromDataAndLinkMN() is supported only for "
                  "DP ports",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("Get Pixel Clock from Data/Link MN is supported only for DP ports.")
        return pixel_clock_hz

    portObj = DisplayTranscoder(connector_port, gfx_index=gfx_index)
    data_m, data_n, reg_data = GetDataMNValues(portObj, connector_port, gfx_index)

    link_rate = dpcd.DPCD_getLinkRate(portObj.display_and_adapter_info)
    if link_rate == 0.0:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][TRANSCODER]:ERROR : Link Rate is ZERO, NOT Programmed in DPCD",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("ERROR : Link Rate is ZERO, NOT Programmed in DPCD")
        return False

    link_rate = (link_rate * 1000000)  # convert LinkRate to MHz
    lane_count = dpcd.DPCD_getNumOfLanes(portObj.display_and_adapter_info)

    BPP, BPC = display_base.GetTranscoderBPCValue(portObj, gfx_index)

    stream_clock = (data_m * link_rate * lane_count) / (BPP * data_n)

    ssc_enable = display_base.GetSSC(connector_port, gfx_index)
    if ssc_enable:
        stream_clock = stream_clock - (stream_clock * (0.25 / 100))

    pixel_clock_hz = int(round(stream_clock)) * 100

    return pixel_clock_hz


##
# @brief        Calculate Average Tri byte Nominal rate for HDMI2.1 when DSC is not enabled
# @param[in]    portObj DisplayTranscoder object
# @return       non_dsc_avg_tri_byte_nominal_rate_in_hz in int
def calculate_avg_tri_byte_for_non_dsc_hdmi_2_1(portObj):
    # Calculate Pixel Clock Frequency Nominal in Hz
    pixel_clock_hz = int(portObj.pixelClock_Hz) * 100
    logging.debug(f"pixel_clock_frequency_nominal_in_hz {pixel_clock_hz}")

    # Calculate HBlank
    h_blank = portObj.htotal - portObj.hactive
    logging.debug(f"h_blank {h_blank}")

    # Get TBActive
    tb_active = calculate_tb_active_for_hdmi_2_1(portObj.hactive, portObj.pipe_color_space, portObj.bpc)

    # Get TBBlank
    tb_blank = calculate_tb_blank_for_hdmi_2_1(h_blank, portObj.pipe_color_space, portObj.bpc)

    # Calculate Average Tri Byte Nominal Rate in Hz
    avg_tri_byte_rate_hz = int((pixel_clock_hz * (tb_active + tb_blank)) / (portObj.hactive + h_blank))
    logging.debug(f"Average TriByte Nominal Rate in Hz in Non DSC case: {avg_tri_byte_rate_hz}")

    return avg_tri_byte_rate_hz


##
# @brief        Calculate Tb Blank for HDMI2.1
# @param[in]    h_active HActive of the mode
# @param[in]    color_space Color Format supported
# @param[in]    bpc BPC supported
# @return       tb_active in int
def calculate_tb_active_for_hdmi_2_1(h_active, color_space, bpc):
    k420 = 2 if color_space == "YUV420" else 1
    logging.debug(f"k420 {k420}")

    kcd_num_x8 = 8 if color_space == "YUV422" else bpc
    logging.debug(f"kcd_num_x8 {kcd_num_x8}")

    # Calculate BPP
    bpp = int((24 * kcd_num_x8) / (k420 * 8))
    logging.debug(f"bpp {bpp}")

    # Calculate Video Bytes per Line
    video_bytes_per_line = int((bpp * h_active) / 8)
    logging.debug(f"video_bytes_per_line {video_bytes_per_line}")

    # Calculate TBActive
    if video_bytes_per_line % 3 == 0:
        tb_active = int(video_bytes_per_line / 3)
    else:
        tb_active = int((video_bytes_per_line / 3) + 1)
    logging.debug(f"tb_active {tb_active}")

    return tb_active


##
# @brief        Calculate Tb Blank for HDMI2.1
# @param[in]    h_blank HBlank of the mode
# @param[in]    color_space Color Format supported
# @param[in]    bpc BPC supported
# @return       tb_blank in int
def calculate_tb_blank_for_hdmi_2_1(h_blank, color_space, bpc):
    k420 = 2 if color_space == "YUV420" else 1
    logging.debug(f"k420 {k420}")

    kcd_num_x8 = 8 if color_space == "YUV422" else bpc
    logging.debug(f"kcd_num_x8 {kcd_num_x8}")

    # Calculate TBBlank
    if (h_blank * kcd_num_x8) % (8 * k420) == 0:
        tb_blank = int((h_blank * kcd_num_x8) / (8 * k420))
    else:
        tb_blank = int(((h_blank * kcd_num_x8) / (8 * k420)) + 1)
    logging.debug(f"tb_blank {tb_blank}")

    return tb_blank


##
# @brief        Calculate Average Tri byte Nominal rate for HDMI2.1 when DSC is enabled
# @param[in]    portObj DisplayTranscoder object
# @param[in]    gfx_index Graphics Adapter
# @return        dsc_avg_tri_byte_nominal_rate_in_hz in int
def calculate_avg_tri_byte_for_dsc_hdmi_2_1(portObj, gfx_index):
    # Calculate Pixel Clock Frequency Nominal in Hz
    pixel_clock_hz = int(portObj.pixelClock_Hz) * 100
    logging.debug(f"pixel_clock_frequency_nominal_in_hz {pixel_clock_hz}")

    # Calculate HBlank
    h_blank = portObj.htotal - portObj.hactive
    logging.debug(f"h_blank {h_blank}")

    # HCTotal is required to calculate Average Tri byte Nominal rate for HDMI2.1 when DSC is enabled.
    # Since these calculations(hc_active, hc_blank) are being verified in DSC test cases, using the value from MMIO here

    # Read HCTotal value from MMIO.
    suffix = portObj.pipe_suffix
    reg = MMIORegister.read("TRANS_HDMI_HCTOTAL_REGISTER", "TRANS_HDMI_HCTOTAL_%s" % (suffix), portObj.platform,
                            gfx_index=gfx_index)
    logging.debug("TRANS_HDMI_HCTOTAL_" + suffix + "  --> Offset : " + format(reg.offset, '08X') +
                  " Value :" + format(reg.asUint, '08X'))

    # HCTotal = HActive + HBlank
    hc_total = reg.hc_total + 1
    logging.debug(f"reg.hc_total {hc_total}")

    avg_tri_byte_rate_hz = int((pixel_clock_hz * hc_total) / (portObj.hactive + h_blank))
    logging.debug(f"Average TriByte Nominal Rate in Hz in DSC case: {avg_tri_byte_rate_hz}")

    return avg_tri_byte_rate_hz


##
# @brief        Calculate Link MN values for HDMI2.1
# @param[in]    max_frl_rate - Max FRL rate supported by the Display
# @param[in]    avg_tri_byte_nominal_rate_in_hz - Calculated Average Tri byte Nominal rate
# @return       calculated_link_m - Link M Value
#               calculated_link_n - Link N Value
def calculate_link_mn_values_for_hdmi_2_1(max_frl_rate, avg_tri_byte_nominal_rate_in_hz):

    # Convert FRL Rate to Mbps
    max_frl_rate_mbps = max_frl_rate * 1000
    logging.debug(f"max_frl_rate_mbps {max_frl_rate_mbps}")

    # Calculate HDMI FRL Link Symbol clock
    hdmi_frl_link_symbol_clock = int(max_frl_rate_mbps * 1000000 / 18)
    logging.debug(f"hdmi_frl_link_symbol_clock {hdmi_frl_link_symbol_clock}")

    # Get GCD
    gcd = math.gcd(avg_tri_byte_nominal_rate_in_hz, hdmi_frl_link_symbol_clock)
    logging.debug(f"GCD Value: {gcd}")

    # Calculate Link M and Link N values
    calculated_link_m = int(avg_tri_byte_nominal_rate_in_hz / gcd)
    calculated_link_n = int(hdmi_frl_link_symbol_clock / gcd)

    return calculated_link_m, calculated_link_n


##
# @brief        Verify Link MN values for HDMI2.1
# @param[in]    portObj DisplayTranscoder object
# @param[in]    gfx_index Graphics Adapter
# @return       True if Link MN verification is successful else False
def verify_link_mn_values_for_hdmi_2_1(portObj, gfx_index):
    from Tests.ModeEnumAndSet.display_mode_enumeration_base import ModeEnumAndSetBase
    connector_port = portObj.display_port
    is_hdmi_2_1 = clock_helper.is_hdmi_2_1(connector_port, gfx_index)

    # Link M,N Values will be programmed only for HDMI2.1 FRL
    if not is_hdmi_2_1:
        logging.info(f"SKIP: Link M/N Verification for Legacy HDMI")
        return True

    # Parse HF-VSDB block
    hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
    hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, connector_port)

    # Get the actual Link M/N values programmed by the driver
    programmed_link_m, programmed_link_n, reg_link = GetLinkMNValues(portObj, connector_port, gfx_index)

    # Calculation for Link M/N values starts here

    # Check if compression is enabled. The formula to calculate Link M/N values varies in DSC and Non DSC case
    is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, connector_port)

    # Non DSC Case
    if not is_compression_enabled:
        # Get Max FRL Rate from HF-VSDB Block
        max_frl_rate = hf_vsdb_parser.max_frl_rate[0]
        logging.debug(f"max_frl_rate: {max_frl_rate} ")

        # Calculate Average Tri Byte Nominal rate in Non DSC case
        avg_tri_byte_nominal_rate_in_hz = calculate_avg_tri_byte_for_non_dsc_hdmi_2_1(portObj)

    # DSC Case
    else:
        # Get DSC Max FRL Rate from HF-VSDB block
        max_frl_rate = hf_vsdb_parser.dsc_max_frl_rate[0]
        logging.debug(f"Max DSC FRL Rate: {max_frl_rate} ")

        # Calculate Average Tri Byte Nominal rate in DSC case
        avg_tri_byte_nominal_rate_in_hz = calculate_avg_tri_byte_for_dsc_hdmi_2_1(portObj, gfx_index)

    frl_rate_in_vbt = ModeEnumAndSetBase.get_hdmi_2_1_frl_rate_in_vbt(connector_port)
    max_frl_rate = min(frl_rate_in_vbt, max_frl_rate)

    # Calculate Link MN values
    calculated_link_m, calculated_link_n = calculate_link_mn_values_for_hdmi_2_1(max_frl_rate,
                                                                                 avg_tri_byte_nominal_rate_in_hz)

    # Calculation for Link M/N values ends here

    if calculated_link_m == programmed_link_m and calculated_link_n == programmed_link_n:
        logging.info(logger_template.format(res="PASS", feature="{} - (LINKM,LINKN) ".format(reg_link),
                                            exp="{},{}".format(calculated_link_m, calculated_link_n),
                                            act="{},{}".format(programmed_link_m, programmed_link_n)))
        logging.info("PASS : Link M/N values Programming Successful for HDMI2.1")
    else:
        logging.error(logger_template.format(res="FAIL", feature="{} - (LINKM,LINKN)".format(reg_link),
                                             exp="{},{}".format(calculated_link_m, calculated_link_n),
                                             act="{},{}".format(programmed_link_m, programmed_link_n)))
        gdhm.report_driver_bug_di("Link M/N values are NOT programmed Correctly for HDMI2.1")
        logging.error("FAIL : Link M/N values are NOT programmed Correctly for HDMI2.1")
        return False
    return True


##
# @brief        Calculate TbBorrowed for HDMI2.1
# @param[in]    portObj DisplayTranscoder object
# @param[in]    gfx_index Graphics Adapter
# @return       tri_bytes_borrowed - Calculated Tri Bytes borrowed Value
def calculate_tb_borrowed_for_hdmi_2_1(portObj, gfx_index):
    from Tests.ModeEnumAndSet.display_mode_enumeration_base import ModeEnumAndSetBase
    million = 10 ** 6

    # Parse HF-VSDB block
    hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
    hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, portObj.display_port)

    # Get Max FRL rate and Lane count from HF-VSDB block
    max_frl_rate, frl_lane_count = hf_vsdb_parser.max_frl_rate

    frl_rate_in_vbt = ModeEnumAndSetBase.get_hdmi_2_1_frl_rate_in_vbt(portObj.display_port)
    max_frl_rate = min(frl_rate_in_vbt, max_frl_rate)

    max_frl_rate_in_mbps = max_frl_rate * 1000
    logging.debug(f"max_frl_rate {max_frl_rate}, frl_lane_count {frl_lane_count}")
    logging.debug(f"max_frl_rate_in_mbps {max_frl_rate_in_mbps}")

    # Calculate Pixel Clock Frequency Nominal in Hz
    pixel_clock_hz = int(portObj.pixelClock_Hz) * 100
    logging.debug(f"pixel_clock_frequency_nominal_in_hz {pixel_clock_hz}")

    # Calculate HBlank
    h_blank = portObj.htotal - portObj.hactive
    logging.debug(f"h_blank {h_blank}")

    # Initialize FVA Factor to 1
    fva_factor = 1

    # Initialize Pixel Clock Tolerance to 5
    pixel_clock_tolerance = 5

    # Calculate Overhead Margin
    overhead_max_in_mega_units = 21360 if (frl_lane_count == 3) else 21840
    logging.debug(f"overhead_max_in_mega_units {overhead_max_in_mega_units}")

    # Calculate Maximum Pixel Clock
    max_pixel_clock_hz = int(pixel_clock_hz * (1000 + pixel_clock_tolerance) * fva_factor / 1000)
    logging.debug(f"max_pixel_clock_hz {max_pixel_clock_hz}")

    # Calculate Video Line Period
    video_line_period_ps = int(portObj.htotal * million)
    video_line_period_ps = int(video_line_period_ps * million / max_pixel_clock_hz)
    logging.debug(f"video_line_period_ps {video_line_period_ps}")

    # Calculate worst-case slow FRL Bit Rate
    min_frl_rate_bps = max_frl_rate_in_mbps * (million - 300)
    logging.debug(f"min_frl_rate_bps {min_frl_rate_bps}")

    # Calculate worst-case slow FRL Character Rate
    slow_frl_char_rate_hz = int(min_frl_rate_bps / 18)
    logging.debug(f"slow_frl_char_rate_hz {slow_frl_char_rate_hz}")

    # Calculate Active Ref period
    active_ref_period_ps = int((video_line_period_ps * portObj.hactive) / portObj.htotal)
    logging.debug(f"active_ref_period_ps {active_ref_period_ps}")

    # Calculate Blank Ref period
    blank_ref_period_ps = int((video_line_period_ps * h_blank) / portObj.htotal)
    logging.debug(f"blank_ref_period_ps {blank_ref_period_ps}")

    den = int((frl_lane_count * slow_frl_char_rate_hz * (million - overhead_max_in_mega_units)) / million)
    logging.debug(f"den {den}")

    # Get TBActive
    tb_active = calculate_tb_active_for_hdmi_2_1(portObj.hactive, portObj.pipe_color_space, portObj.bpc)

    # Get TBBlank
    tb_blank = calculate_tb_blank_for_hdmi_2_1(h_blank, portObj.pipe_color_space, portObj.bpc)

    # Calculate TBActive Minimum period
    tb_active_min_period_ps = int((3 * tb_active * million * million) / (2 * den))
    logging.debug(f"tb_active_min_period_ps {tb_active_min_period_ps}")

    # Calculate TBBlank Minimum period
    tb_blank_min_period_ps = int((tb_blank * million * million) / den)
    logging.debug(f"tb_blank_min_period_ps {tb_blank_min_period_ps}")

    if (active_ref_period_ps >= tb_active_min_period_ps) and (blank_ref_period_ps >= tb_blank_min_period_ps):
        tri_byte_borrowed_ps = 0
    elif (active_ref_period_ps < tb_active_min_period_ps) and (blank_ref_period_ps >= tb_blank_min_period_ps):
        tri_byte_borrowed_ps = tb_active_min_period_ps - active_ref_period_ps
    else:
        assert False, "HDMI FRL TBlank MIN exceeds TBlank REF"
    logging.debug(f"tri_byte_borrowed_ps {tri_byte_borrowed_ps}")

    # Get Average Tri Byte Nominal rate in Hz
    avg_tri_byte_hz = calculate_avg_tri_byte_for_non_dsc_hdmi_2_1(portObj)
    logging.debug(f"avg_tri_byte_hz {avg_tri_byte_hz}")

    # Calculate Tri Bytes Borrowed
    tri_bytes_borrowed = tri_byte_borrowed_ps * avg_tri_byte_hz

    # For simplicity, assigning required values to x and y
    x = tri_bytes_borrowed
    y = million * million

    tri_bytes_borrowed = (x / y) if x % y == 0 else (x / y) + 1
    logging.debug(f"tri_bytes_borrowed {int(tri_bytes_borrowed)}")

    return int(tri_bytes_borrowed)


##
# @brief        Verify TbBorrowed for HDMI2.1
# @param[in]    portObj DisplayTranscoder object
# @param[in]    gfx_index Graphics Adapter
# @return       True if TbBorrowed is successful else False
def verify_tb_borrowed_for_hdmi_2_1(portObj, gfx_index):
    connector_port = portObj.display_port
    is_hdmi_2_1 = clock_helper.is_hdmi_2_1(connector_port, gfx_index)

    if not is_hdmi_2_1:
        logging.info(f"SKIP: TbBorrowed Verification for Legacy HDMI")
        return True

    # Check if compression is enabled.
    is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, connector_port)

    # Verify TbBorrowed in Non DSC Case. DSC case is already being verified in pps_calculator_hdmi.py
    if not is_compression_enabled:
        calculated_tri_bytes_borrowed = calculate_tb_borrowed_for_hdmi_2_1(portObj, gfx_index)

        # Verify if Tri Bytes Borrowed is less than Max allowed Tri Bytes
        if calculated_tri_bytes_borrowed > 400:
            logging.error(f"HDMI FRL Tri Bytes Borrowed exceeds Max allowed Tri Bytes that can be borrowed ")
            return False

        # MMIO Verification
        suffix = portObj.pipe_suffix
        reg = MMIORegister.read("TRANS_HDMI_DFMWRCTL_REGISTER", "TRANS_HDMI_DFMWRCTL_%s" % (suffix), portObj.platform,
                                gfx_index=gfx_index)
        logging.debug("TRANS_HDMI_DFMWRCTL_" + suffix + "  --> Offset : " + format(reg.offset, '08X') +
                      " Value :" + format(reg.asUint, '08X'))

        # Get Programmed Tri Bytes Borrowed value
        programmed_tri_bytes_borrowed = reg.tb_actual_offset * 2

        if calculated_tri_bytes_borrowed == programmed_tri_bytes_borrowed:
            logging.info(f"PASS : TbBorrowed Verification for HDMI2.1    Expected: {calculated_tri_bytes_borrowed}   "
                         f"Actual: {programmed_tri_bytes_borrowed}")
        else:
            logging.error(f"FAIL : TbBorrowed Verification for HDMI2.1    Expected: {calculated_tri_bytes_borrowed}    "
                          f"Actual: {programmed_tri_bytes_borrowed}")

    return True


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

    portList = []
    portList.append(DisplayTranscoder("DP_A"))
    # portList.append(DisplayTranscoder("HDMI_C",1920,1080,2200,1125,60,1800000,8,0))

    result = VerifyTranscoderProgramming(portList, 'gfx_0')
    if result is False:
        # GDHM handled in VerifyTranscoderProgramming(portList, 'gfx_0')
        logging.error("FAIL : verifyPortProgramming")
    else:
        logging.info("PASS : verifyPortProgramming")
