######################################################################################
# @file     dpcd_helper.py
# @brief    Helper to read DPCD registers
# @author   Ap, Kamal
######################################################################################

import logging

from Libs.Core import display_utility, driver_escape
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.display_config import display_config_struct as cfg_struct


##
# @brief        Function to get SSC value from DPCD.
# @param[in]    target_id
# @return       BOOL ssc value
def DPCD_getSSC(target_id):
    DPCD_SSC = 0x00003
    ssc = 0b0
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_SSC)
    if dpcd_flag:
        logging.debug("DPCD_SSC = Offset :" + str(hex(DPCD_SSC)).rstrip("L")
                      + "--> Value : 0x" + str(reg_value[0]))
        mask = 0b1
        ssc = mask & reg_value[0]
        if ssc:
            logging.debug("Get SSC from DPCD :SSC is ENABLED")
        else:
            logging.debug("Get SSC from DPCD :SSC is DISABLED")
    else:
        logging.error("ERROR : Get SSC from DPCD : DPCD read fail- dpcd flag ="
                      + str(dpcd_flag) + " dpcd_reg_value= " + str(reg_value[0]))
    return ssc


##
# @brief        Function to get Number of lanes from DPCD.
# @param[in]    target_id
# @return       INT number of lanes
def DPCD_getNumOfLanes(target_id):
    LANE_COUNT_SET = 0x00101
    MAX_LANE_COUNT = 0x00002
    lanes = 0
    lanes1 = 0
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, MAX_LANE_COUNT)
    dpcd_flag1, reg_value1 = driver_escape.read_dpcd(target_id, LANE_COUNT_SET)
    if dpcd_flag:
        logging.debug("MAX_LANE_COUNT = Offset :"
                      + str(hex(MAX_LANE_COUNT)).rstrip("L")
                      + "--> Value : " + str(hex(reg_value[0])).rstrip("L"))
        lanes = getNumOfLanes(reg_value[0])
        if dpcd_flag1:
            logging.debug("LANE_COUNT_SET = Offset :"
                          + str(hex(LANE_COUNT_SET)).rstrip("L")
                          + "--> Value : " + str(hex(reg_value[0])).rstrip("L"))
            lanes1 = getNumOfLanes(reg_value1[0])
        else:
            logging.error("ERROR : Get Lane count Set from DPCD : DPCD read fail- dpcd flag ="
                          + str(dpcd_flag1) + " dpcd_reg_value= " + str(reg_value1[0]))
        if ((lanes == 0) or (lanes1 == 0)):
            logging.error("ERROR : Get number of lanes from DPCD : INVALID ")
        logging.info("INFO : MAX Lane Count DPCD(0x00002h) = " + str(
            lanes) + ", Driver Optimized Lane Count DPCD(0x00101h) = " + str(lanes1))
    else:
        logging.error("ERROR : Get number of lanes from DPCD : DPCD read fail- dpcd flag ="
                      + str(dpcd_flag) + " dpcd_reg_value= " + str(reg_value[0]))
    return lanes1  # 0 for undefined values


##
# @brief        Function to get Number of lanes mapping.
# @param[in]    value - DPCD read value
# @return       INT number of lanes
def getNumOfLanes(value):
    mask = 0b1111
    no_of_lanes = mask & value
    if no_of_lanes == 0x1:
        lanes = 1
    elif no_of_lanes == 0x2:
        lanes = 2
    elif no_of_lanes == 0x4:
        lanes = 4
    else:
        lanes = value
    return lanes


##
# @brief        Function to get DPCD Revision.
# @param[in]    target_id
# @return       Returns DPCD revision
def DPCD_getRevision(target_id):
    DPCD_VER = 0x00000
    dpcd_rev = "Unsupported DPCD Revision"
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_VER)
    if dpcd_flag:
        logging.debug("DPCD_VER = Offset :"
                      + str(hex(DPCD_VER).rstrip("L").rstrip("0x")) + "--> Value :"
                      + str(hex(reg_value[0])).rstrip("L"))
        if (reg_value[0] == 0x10):
            dpcd_rev = "DPCD r1.0"
        elif (reg_value[0] == 0x11):
            dpcd_rev = "DPCD r1.1"
        elif (reg_value[0] == 0x12):
            dpcd_rev = "DPCD r1.2"
        elif (reg_value[0] == 0x13):
            dpcd_rev = "DPCD r1.3"
        elif (reg_value[0] == 0x14):
            dpcd_rev = "DPCD r1.4"
        else:
            dpcd_rev = "Unsupported DPCD Revision"

        logging.debug("INFO : dpcd_rev Address : %s Revision : %s" % (hex(DPCD_VER), dpcd_rev))
    else:
        logging.error("ERROR : Get DPCD_VER from DPCD failed : dpcd flag =" + str(dpcd_flag)
                      + " dpcd_reg_value= " + str(reg_value[0]))
    return dpcd_rev


##
# @brief        Function to get EDP DPCD Revision.
# @param[in]    target_id
# @return       Returns EDP DPCD revision
def DPCD_geteDPRevision(target_id):
    EDP_DPCD_VER = 0x00700
    dpcd_rev = "Unsupported DPCD Revision"
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, EDP_DPCD_VER)
    if dpcd_flag:
        logging.debug("EDP_DPCD_VER = Offset :"
                      + str(hex(EDP_DPCD_VER)) + "--> Value :" + str(hex(reg_value[0])).rstrip("L"))
        if (reg_value[0] == 0x0):
            dpcd_rev = "eDP DPCD r1.1"
        elif (reg_value[0] == 0x1):
            dpcd_rev = "eDP DPCD r1.2"
        elif (reg_value[0] == 0x2):
            dpcd_rev = "eDP DPCD r1.3"
        elif (reg_value[0] == 0x3):
            dpcd_rev = "eDP DPCD r1.4"
        elif (reg_value[0] == 0x4):
            dpcd_rev = "eDP DPCD r1.4a"
        elif (reg_value[0] == 0x5):
            dpcd_rev = "eDP DPCD r1.4b"
        elif (reg_value[0] == 0x6):
            dpcd_rev = "eDP DPCD r1.5"
        else:
            dpcd_rev = "Unsupported DPCD Revision"

        logging.debug("INFO : eDP_dpcd_rev Address : %s Revision : %s" % (hex(EDP_DPCD_VER), dpcd_rev))
    else:
        logging.error("ERROR : Get EDP_DPCD_VER from DPCD failed : dpcd flag =" + str(dpcd_flag)
                      + " dpcd_reg_value= " + str(reg_value[0]))
    return reg_value[0]


##
# @brief        Function to get Link Rate/intermediate linkrate value from DPCD.
# @param[in]    target_id - offset in hex
# @return       float link rate
def DPCD_getLinkRate(target_id):
    MAX_LINKRATE = 0x00001
    DPCD_LINKRATE = 0x00100
    EXTENSION_CAPS = 0x0000E
    MAX_LINKRATE_EXTENDED = 0x02201
    MAIN_LINK_CHANNEL_ENCODING_CAP = 0x2206
    DP_2_0_SUPPORTED_LINKRATE = 0x2215
    max_lr = 0

    max_lr_offset = MAX_LINKRATE
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, MAX_LINKRATE)
    if dpcd_flag:
        max_lr = getLinkRate(reg_value[0])

    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, EXTENSION_CAPS)
    if dpcd_flag:
        if reg_value[0] & 0x80 == 0x80:  # bit 7 is 1 , then extended receiver caps supported
            max_lr_offset = MAX_LINKRATE_EXTENDED

    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, max_lr_offset)
    if dpcd_flag:
        max_lr = getLinkRate(reg_value[0])

        # Check 2206h bit 0 and 1 for DP 2.0 support.DP 2.0 supports UHBR linkrates. Check max UHBR linkrate at 2215h
        dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, MAIN_LINK_CHANNEL_ENCODING_CAP)
        if dpcd_flag:
            if reg_value[0] & 0x03 == 0x03:
                max_lr_offset = DP_2_0_SUPPORTED_LINKRATE
                dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, max_lr_offset)
                if dpcd_flag:
                    max_lr = getLinkRate(reg_value[0])

    dpcd_inter_addr = dict([(0x00010, 0x00011),
                            (0x00012, 0x00013),
                            (0x00014, 0x00015),
                            (0x00016, 0x00017),
                            (0x00018, 0x00019),
                            (0x0001A, 0x0001B),
                            (0x0001C, 0x0001D),
                            (0x0001E, 0x0001F)])
    DPCD_INTERMEDIATE_LR_LSB = 0x00010
    DPCD_INTERMEDIATE_LR_USB = 0x00011
    lr = 0.0
    ilr = 0.0

    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_LINKRATE)
    if dpcd_flag:
        lr = getLinkRate(reg_value[0])
        logging.info("INFO : For Target_id: " + str(target_id) + " MAX Link-Rate DPCD(" + str(hex(max_lr_offset)) +
                     "h) = " + str(max_lr) + " GHz/lane, Driver Optimized Link-Rate DPCD(" + str(hex(DPCD_LINKRATE)) +
                     "h) = " + str(lr) + " GHz/lane")
    else:
        logging.error("ERROR : Get link rate from DPCD failed : dpcd flag =" + str(dpcd_flag)
                      + " dpcd_reg_value= " + str(reg_value[0]))
    port = GetConnectorPort(target_id)

    if display_utility.get_vbt_panel_type(port, 'gfx_0') == display_utility.VbtPanelType.LFP_DP:
        dpcd_rev = DPCD_geteDPRevision(target_id)
    else:
        dpcd_rev = DPCD_getRevision(target_id)

    if (dpcd_rev == "DPCD r1.3") or ((display_utility.get_vbt_panel_type(port, 'gfx_0') ==
                                      display_utility.VbtPanelType.LFP_DP) and dpcd_rev >= 0x3):
        # intermediate link rate is supported only for DPCD rev 1.3 and edp DPCD rev >= 1.4
        DPCD_LINKRATE = 0x00115
        dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_LINKRATE)
        if dpcd_flag:
            logging.debug("DPCD_LINKRATE = Offset :"
                          + str(hex(DPCD_LINKRATE)) + "--> Value :"
                          + str(hex(reg_value[0])).rstrip("L"))
            index = reg_value[0]
            DPCD_INTERMEDIATE_LR_LSB = list(dpcd_inter_addr)[index:index + 1][0]
            DPCD_INTERMEDIATE_LR_USB = list(dpcd_inter_addr.values())[index:index + 1][0]
        # if intermediate link rate supported
        dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_INTERMEDIATE_LR_LSB)
        if dpcd_flag:
            logging.debug("DPCD_INTERMEDIATE_LINKRATE LSB = Offset :"
                          + str(hex(DPCD_INTERMEDIATE_LR_LSB).rstrip("L"))
                          + "--> Value : " + str(hex(reg_value[0])).rstrip("L"))

            ilr_lsb = str(hex(reg_value[0]).rstrip("L").lstrip("0x"))
            dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_INTERMEDIATE_LR_USB)
            if dpcd_flag:

                logging.debug("DPCD_INTERMEDIATE_LINKRATE USB = Offset :"
                              + str(hex(DPCD_INTERMEDIATE_LR_USB).rstrip("L"))
                              + "--> Value : " + str(hex(reg_value[0])).rstrip("L"))

                ilr_usb = str(hex(reg_value[0]).rstrip("L").lstrip("0x"))
                ilr_s = ilr_usb + ilr_lsb
                # logging.info("ilr_s = " + ilr_s)
                if (ilr_s != ''):
                    ilr = (int(ilr_s, 16) * 200 / 1000000.00)
                    logging.info("INFO : Intermediate link rate supported in DPCD = " + str(ilr) + " GHz/lane")
                    lr = ilr
            else:
                logging.error("ERROR : Get intermediate link rate USB from DPCD failed : dpcd flag ="
                              + str(dpcd_flag) + " dpcd_reg_value= " + str(reg_value[0]))
            # TODO: read all supported link rates from table
        else:
            logging.error("ERROR : Get intermediate link rate LSB from DPCD failed : dpcd flag ="
                          + str(dpcd_flag) + " dpcd_reg_value= " + str(reg_value[0]))

    return lr


##
# @brief        Function to map DPCD read value to linkrate.
# @param[in]    value - DPCD read data.
# @return       programmed linkrate
def getLinkRate(value):
    if value == 0x6:
        lr = 1.62
    elif value == 0xA:
        lr = 2.7
    elif value == 0x14:
        lr = 5.4
    elif value == 0x1E:
        lr = 8.1
    elif value == 0x1:
        lr = 10
    elif value in [0x4, 0x5]:
        lr = 13.5
    elif value in [0x2, 0x3, 0x7]:
        lr = 20
    else:
        lr = value

    return lr


##
# @brief        Function to check if Alternate_Scrambler_Reset is enabled from DPCD.
# @param[in]    target_id
# @return       bool - true if ASRE is enabled else false
def DPCD_checkASSR(target_id):
    DPCD_ASSR_CHECK = 0x0010A

    # Check whether ASSR is enabled in the panel or not (DPCD read)
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_ASSR_CHECK)
    if dpcd_flag:
        logging.debug("DPCD_ASSR_CHECK = Offset :" + str(hex(DPCD_ASSR_CHECK)).rstrip("L")
                      + "--> Value : " + str(hex(reg_value[0])).rstrip("L"))
        if (reg_value[0] & 0x1) == 0x1:
            logging.debug("ASSR is enabled in the panel.")
            return 1
        else:
            logging.debug("ASSR is disabled in the panel.")
            return 0
    else:
        logging.error("ERROR : Reading DPCD failed.")
        return 0


##
# @brief        Function to get DDI transport mode from DPCD.
# @param[in]    target_id
# @return       based on DPCD value, return SST, MST or None
def DPCD_getTransportModeSelect(target_id):
    DPCD_MSTM_CAP = 0x00021
    DPCD_MSTM_CTRL = 0x00111
    DPCD_LINK_CHANNEL_ENCODING_SET = 0x00108

    # For DP2.0 if the display is operating in 128/132 bit encoding, then trans ddi select bits in TRANS_DDI_CTL_REG
    # will programmed in new mode called DP2.0 32b symbol mode.
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_LINK_CHANNEL_ENCODING_SET)
    if not dpcd_flag:
        dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_LINK_CHANNEL_ENCODING_SET)

    if dpcd_flag:
        logging.info("DPCD_LINK_CHANNEL_ENCODING_SET[{}] = {}".format(hex(DPCD_LINK_CHANNEL_ENCODING_SET),
                                                                      hex(reg_value[0])))
        if reg_value[0] == 0x02:
            return "DP_128_132_BIT_SYMBOL_MODE"
    else:
        logging.info("[Test Issue] - DPCD Read Failed for offset: {}".format(hex(DPCD_LINK_CHANNEL_ENCODING_SET)))
        return None

    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_MSTM_CTRL)

    # WA - sporadically get transport mode select dpcd read fails when called multiple times in a loop
    # To WA this issue , we will re-read dpcd in case first read attempt failed.
    # Other dpcd read calls in this helper file do not face this issue as they are not called multiple times in a loop
    if not dpcd_flag:
        dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_MSTM_CTRL)

    if dpcd_flag:
        logging.debug("DPCD_MSTM_CTRL = Offset :" + str(hex(DPCD_MSTM_CTRL)).rstrip("L")
                      + "--> Value : " + str(hex(reg_value[0])).rstrip("L"))

        # Transcoder will be programmed to MST mode in following cases
        #   1) When MST supported display is connected.
        #   2) When DP 2.0 display operates in 128b/132b encoding - MST SBM and SST SBM
        #   3) When DP 2.0 display operates in 8b/10b encoding (Fall back scenario) - MST SBM and SST SBM
        if ((reg_value[0] & 0x1) == 0x1) or ((reg_value[0] & 0x7) == 0x6):
            dpcd_flag1, reg_value1 = driver_escape.read_dpcd(target_id, DPCD_MSTM_CAP)
            if dpcd_flag1:
                logging.debug("INFO : DPCD_MSTM_CAP = Offset :" + str(hex(DPCD_MSTM_CAP)).rstrip("L")
                              + "--> Value : " + str(hex(reg_value1[0])).rstrip("L"))

                # Return mode select as MST when the display supports multi-stream Transport or supports sideband
                # messaging but not mult-stream transport. 2nd case will come into picture when DP 2.0 display which
                # supports sideband messaging but not multi-stream transport is connected but display got trained with
                # DP 1.4 link rate.
                if ((reg_value1[0] & 0x1) == 0x1) or (reg_value1[0] & 0x3 == 0x2):
                    return "MST"
            else:
                logging.error("ERROR : Reading DPCD failed.")
                return None
        else:
            return "SST"
    else:
        logging.error("ERROR : Reading DPCD failed.")
        return None


##
# @brief        Function to check ENHANCED_FRAME is enabled from DPCD.
# @param[in]    target_id
# @return       bool - true if ENHANCED_FRAME is enabled else false
def DPCD_checkEnhancedFraming(target_id):
    DPCD_MAX_LANE_COUNT = 0x00002

    # Check whether ENHANCED_FRAME is enabled in the panel or not (DPCD read)
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, DPCD_MAX_LANE_COUNT)
    if dpcd_flag:
        logging.debug("INFO : DPCD_MAX_LANE_COUNT = Offset :" + str(hex(DPCD_MAX_LANE_COUNT)).rstrip("L")
                      + "--> Value : " + str(hex(reg_value[0])).rstrip("L"))
        if (reg_value[0] & 0x80) == 0x80:
            logging.debug("ENHANCED_FRAME_CAP is enabled in the panel.")
            return 1
        else:
            logging.debug("ENHANCED_FRAME_CAP is disabled in the panel.")
            return 0
    else:
        logging.error("ERROR : Reading DPCD failed.")
        return 0


##
# @brief        Get connector port for passed target ID
# @param[in]    display_adapter_info
# @return       connector port
def GetConnectorPort(display_adapter_info):
    targetId = display_adapter_info
    if type(display_adapter_info) is cfg_struct.DisplayAndAdapterInfo:
        targetId = display_adapter_info.TargetID

    display_config = disp_cfg.DisplayConfiguration()
    enumerated_displays = display_config.get_enumerated_display_info()
    for display_index in range(enumerated_displays.Count):
        target_id = enumerated_displays.ConnectedDisplays[display_index].TargetID
        if ((target_id == targetId)
                and enumerated_displays.ConnectedDisplays[display_index].IsActive):
            return (cfg_enum.CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name
    logging.debug("ERROR : " + str(target_id) + " is NOT ACTIVE")
    return None


##
# @brief        Function to get Panel supported Link Ratefrom DPCD.
# @param[in]    target_id  or display and adapter info
# @return       float link rate
def DPCD_getPanelMaxLinkRate(target_id):
    MAX_LINKRATE = 0x00001
    DP_2_0_SUPPORTED_LINKRATE = 0x02215
    EXTENSION_CAPS = 0x0000E
    MAX_LINKRATE_EXTENDED = 0x02201
    MAIN_LINK_CHANNEL_CODING_CAP = 0x02206
    max_lr = 0

    max_lr_offset = MAX_LINKRATE
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, EXTENSION_CAPS)
    if dpcd_flag:
        if reg_value[0] & 0x80 == 0x80:  # bit 7 is 1 , then extended receiver caps supported
            max_lr_offset = MAX_LINKRATE_EXTENDED
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, max_lr_offset)
    if dpcd_flag:
        max_lr = getLinkRate(reg_value[0])

    # Check 2206h bit 0 and 1 for DP 2.0 support.DP 2.0 supports UHBR linkrates. Check max UHBR linkrate at 2215h
    dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, MAIN_LINK_CHANNEL_CODING_CAP)
    if dpcd_flag:
        if reg_value[0] & 0x03 == 0x03:
            logging.info("Panel supports DP2.0 Link layer")
            max_lr_offset = DP_2_0_SUPPORTED_LINKRATE
            dpcd_flag, reg_value = driver_escape.read_dpcd(target_id, max_lr_offset)
            if dpcd_flag:
                max_lr = getLinkRate(reg_value[0])

    return max_lr

