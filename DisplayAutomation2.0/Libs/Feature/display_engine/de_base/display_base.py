#####################################################################################################################################
# @file     display_base.py
# @brief    Python wrapper exposes common display interfaces for Verification logic
# @details  display_base.py provides interface's to get the pipe and DDI mapping for display port
#           passed as input
#           User-Input : DisplayBase() object - display_port name of type CONNECTOR_PORT_TYPE(Enum)
#           defined in system_utility
# @todo     all common functions to be moved here
# @author   Aafiya, Kaleem
######################################################################################

import logging
import os
from enum import IntEnum

import Libs.Feature.display_port.dpcd_helper as dpcd
from Libs.Core import display_utility
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.vbt.vbt import Vbt
from registers.mmioregister import MMIORegister


##
# @brief    DDI Selected
class DDI_SELECT(IntEnum):
    DDI_A = 0
    DDI_B = 1
    DDI_C = 2
    DDI_D = 3
    DDI_E = 4
    DDI_F = 5


##
# @brief    DDI Selected for gen11.5
class GEN11p5_DDI_SELECT(IntEnum):
    NONE = 0
    DDI_A = 1
    DDI_B = 2
    DDI_C = 3
    DDI_D = 4
    DDI_E = 5
    DDI_F = 6
    DDI_G = 7
    DDI_H = 8
    DDI_I = 9


##
# @brief    DDI Selected for DG2
class DG2_DDI_SELECT(IntEnum):
    NONE = 0
    DDI_A = 1
    DDI_B = 2
    DDI_C = 3
    DDI_F = 4
    DDI_D = 8
    DDI_E = 9


##
# @brief    DDI Selected for DG1
class DG1_DDI_SELECT(IntEnum):
    NONE = 0
    DDI_A = 1
    DDI_B = 2
    DDI_C = 4  # Port C drive through DDI-C
    DDI_D = 5  # Port D drive through DDI-D


##
# @brief    DDI Selected for ADLS
class ADLS_DDI_SELECT(IntEnum):
    NONE = 0
    DDI_A = 1
    DDI_B = 4  # Port B drive through DDI-TC1
    DDI_C = 5  # Port C drive through DDI-TC2
    DDI_D = 6  # Port D drive through DDI-TC3
    DDI_E = 7  # Port E drive through DDI-TC4


##
# @brief    DDI Selected for ADLP
class ADLP_DDI_SELECT(IntEnum):
    NONE = 0
    DDI_A = 1
    DDI_B = 2
    DDI_C = 3
    DDI_F = 4  # Port F drive through DDI-TC1
    DDI_G = 5  # Port G drive through DDI-TC2
    DDI_H = 6  # Port H drive through DDI-TC3
    DDI_I = 7  # Port I drive through DDI-TC4
    DDI_D = 8
    DDI_E = 9


##
# @brief    DDI Selected for MTL, LNL
class MTL_DDI_SELECT(IntEnum):
    NONE = 0
    DDI_A = 1
    DDI_B = 2
    DDI_C = 3
    DDI_F = 4  # Port F drive through DDI-TC1
    DDI_G = 5  # Port G drive through DDI-TC2
    DDI_H = 6  # Port H drive through DDI-TC3
    DDI_I = 7  # Port I drive through DDI-TC4
    DDI_D = 8
    DDI_E = 9


##
# @brief    ELG_DDI_SELECT
class ELG_DDI_SELECT(IntEnum):
    NONE = 0
    DDI_A = 1
    DDI_F = 4  # Port F drive through DDI-TC1
    DDI_G = 5  # Port G drive through DDI-TC2
    DDI_H = 6  # Port H drive through DDI-TC3
    DDI_I = 7  # Port I drive through DDI-TC4


##
# @brief    DDI mode
class DDI_MODE(object):
    HDMI = 0
    DVI = 1
    DP_SST = 2
    DP_MST = 3
    DP_128_132_BIT_SYMBOL_MODE = 4


##
# @brief    WD Mode
class WD_MODE(object):
    WB_0 = 0
    WB_1 = 1


##
# @brief    Pipe Mapping for EDP/DSI
class PIPE_MAPPING(IntEnum):
    PIPE_A = 0
    PIPE_B = 5
    PIPE_C = 6
    PIPE_D = 7


##
# @brief    BPC Value
class BPC_VALUE(object):
    bpc_8 = 0
    bpc_10 = 1
    bpc_6 = 2
    bpc_12 = 3


##
# @brief    Dictionary of TRANSCODER connected as key and integers as values
transcoder_dict = {"transcoder_none": -1,
                   "transcoder_edp": 0,
                   "transcoder_a": 1,
                   "transcoder_b": 2,
                   "transcoder_c": 3,
                   "transcoder_d": 4,
                   "transcoder_dsi0": 5,
                   "transcoder_dsi1": 6,
                   "transcoder_wb0": 7,
                   "transcoder_wb1": 8}

##
# @brief    Dictionary of PIPE connected as key and integers as values
pipe_dict = {"pipe_none": -1,
             "pipe_a": 0,
             "pipe_b": 1,
             "pipe_c": 2,
             "pipe_d": 3}

yuv422_supported_platform_list = ["DG2", "ADLP", "MTL", "ELG", "LNL", "PTL", "NVL", "CLS"]


##
# @brief    Display Base Class
# @details  Has base functions to be used in Display Engine Verification
class DisplayBase:
    display_and_adapter_info = None
    ddi = None  # DDI-A/B/C/D/E/F
    pipe = None  # PIPE_A/B/C/D
    platform = None
    pipe_suffix = None  # A/B/C/D

    ##
    # @brief        To do mandatory initializations for any Display connected
    # @param[in]    display_port - Display port
    # @param[in]    platform -Platform in testing
    # @param[in]    gfx_index - Graphics adapter
    def __init__(self, display_port, platform=None, gfx_index='gfx_0'):
        display_config = disp_cfg.DisplayConfiguration()
        self.get_platform_for_adapter(gfx_index)
        if platform is not None:
            self.platform = platform

        self.display_and_adapter_info = display_config.get_display_and_adapter_info_ex(display_port, gfx_index)
        if type(self.display_and_adapter_info) is list:
            self.display_and_adapter_info = self.display_and_adapter_info[0]

        self.targetId = self.display_and_adapter_info.TargetID

        # COLLAGE_0 is a virtual port that gets enabled when collage is applied b/w 2, 3 or 4 displays.
        # It contains 2 or more pipes and transcoders depending on collage type (E.g Dual, Tri, Quad).
        # At present this case is not handled in GetPipeDDIAttachedToPort().
        # it will return None, None.
        # Hence this is skipped for COLLAGE_0 case and will be handled separately at required places.
        if display_port not in ["COLLAGE_0"]:
            self.pipe, self.ddi = self.GetPipeDDIAttachedToPort(display_port, gfx_index=gfx_index)
            if self.pipe:
                self.pipe_suffix = GetPipeSuffix(self.pipe)

    ##
    # @brief        Get the pipe mapping for internal display edp/dsi.
    # @param[in]    edp_dsi_input_select - value from TRANS_DDI_FUNC_CTL_REGISTER
    # @return       pipe_mapping - Mapped PIPE to edp/dsi port
    def GetPipeMapping(self, edp_dsi_input_select):
        return PIPE_MAPPING(edp_dsi_input_select).name

    ##
    # @brief        Verify if the transcoder for display port is enabled.
    # @param[in]    connector_port - Display to verify
    # @param[in]    trans_ddi_mode_select - from TRANS_DDI_FUNC_CTL_REGISTER
    # @param[in]    gfx_index - gfx adapter
    # @return       bool -Return true if enabled else return false
    def CheckTransDDIModeSelect(self, connector_port, trans_ddi_mode_select, gfx_index='gfx_0'):
        if ((display_utility.get_vbt_panel_type(connector_port, gfx_index) == display_utility.VbtPanelType.LFP_DP) and
                (trans_ddi_mode_select == DDI_MODE.DP_SST)):
            return True
        elif (connector_port == "MIPI_A" or connector_port == "MIPI_C"):
            return True
        elif (connector_port.startswith("HDMI_") and
              (trans_ddi_mode_select == DDI_MODE.HDMI or trans_ddi_mode_select == DDI_MODE.DVI)):
            return True
        elif (connector_port.startswith("DP_") and
              (trans_ddi_mode_select in [DDI_MODE.DP_SST, DDI_MODE.DP_MST, DDI_MODE.DP_128_132_BIT_SYMBOL_MODE])):
            return True
        elif (connector_port.startswith("WD_") and
              (trans_ddi_mode_select == WD_MODE.WB_0 or trans_ddi_mode_select == WD_MODE.WB_1)):
            return True

        return False

    ##
    # @brief        Get the DDI mapping for display port connected.
    # @param[in]    ddi_selected from TRANS_DDI_FUNC_CTL_REGISTER
    # @param[in]    gfx_index - graphics adapter
    # @return       None / Return the mapped DDI
    def GetTransDDISelectMapping(self, ddi_selected, gfx_index='gfx_0'):
        self.get_platform_for_adapter(gfx_index)
        if (self.platform in ['ICLHP', 'LKF1', 'TGL', 'RYF']):
            return GEN11p5_DDI_SELECT(ddi_selected).name
        elif (self.platform in ['DG1', 'RKL']):
            return DG1_DDI_SELECT(ddi_selected).name
        elif (self.platform in ['JSL', 'ICLLP', 'GLK', 'KBL', 'SKL', 'CFL', 'CNL']):
            return DDI_SELECT(ddi_selected).name
        elif (self.platform in ['ADLS']):
            return ADLS_DDI_SELECT(ddi_selected).name
        elif (self.platform in ['DG2']):
            return DG2_DDI_SELECT(ddi_selected).name
        elif (self.platform in ['ADLP']):
            return ADLP_DDI_SELECT(ddi_selected).name
        elif (self.platform in ['MTL', 'LNL', 'PTL', 'NVL', 'CLS']):
            return MTL_DDI_SELECT(ddi_selected).name
        elif (self.platform in ['ELG']):
            return ELG_DDI_SELECT(ddi_selected).name
        else:
            return None

    ##
    # @brief        Get pipe and DDI attached to the display port.
    # @param[in]    port_name - display to verify
    # @param[in]    transcoder_mapping_details - to get transcoder details(False/True)
    # @param[in]    gfx_index - graphics adapter
    # @return       Pipe connected, DDI Mapping and Transcoder connected(Based on transcoder_mapping_details = True)
    def GetPipeDDIAttachedToPort(self, port_name, transcoder_mapping_details=False, gfx_index='gfx_0'):
        pipe_suffix = None
        self.get_platform_for_adapter(gfx_index)
        if ((port_name == "DP_A") and (self.platform in ['JSL', 'ICLLP', 'GLK', 'KBL', 'SKL', 'CFL', 'CNL'])):
            pipe_suffix = "EDP"
        elif (port_name == "MIPI_A"):
            pipe_suffix = "DSI0"
        elif (port_name == "MIPI_C"):
            pipe_suffix = "DSI1"
        elif (port_name == "WD_0"):
            pipe_suffix = "0"
        elif (port_name == "WD_1"):
            pipe_suffix = "1"
        else:
            pipe_map = dict([('A', 1), ('B', 2), ('C', 3), ('D', 4)])

        if ((port_name.startswith(("HDMI_", "DP_"))) and (pipe_suffix is None)):
            for key, value in pipe_map.items():
                reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL_%s" % (key), self.platform,
                                        gfx_index=gfx_index)
                if (reg.trans_ddi_function_enable):
                    if (self.CheckTransDDIModeSelect(port_name, reg.trans_ddi_mode_select, gfx_index)):
                        mapped_ddi = self.GetTransDDISelectMapping(reg.ddi_select, gfx_index)
                        logging.debug("TRANS_DDI_FUNC_CTL_%s" % (key) + " --> Offset : "
                                      + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
                        ddi = str(mapped_ddi).split("_")
                        port = port_name.split("_")
                        if (ddi[1] == port[1]):
                            logging.debug(
                                "INFO : " + port_name + " Enabled and Connected to PIPE_%s, %s" % (key, mapped_ddi))
                            if transcoder_mapping_details:
                                return "pipe_%s" % (key.lower()), str(mapped_ddi), "transcoder_%s" % (key.lower())
                            return "PIPE_%s" % (key), str(mapped_ddi)

        elif (port_name.startswith("WD_")):
            reg = MMIORegister.read("TRANS_WD_FUNC_CTL_REGISTER", "TRANS_WD_FUNC_CTL_%s" % (pipe_suffix),
                                    self.platform)
            value = reg.wd_input_select
            if (reg.wd_function_enable):
                connected_pipe = self.GetPipeMapping(value)
                if transcoder_mapping_details:
                    return str(connected_pipe).lower(), "DDI_WD", "transcoder_wb" + str(pipe_suffix)
                return str(connected_pipe), "DDI_WD"

        else:
            reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL_%s" % (pipe_suffix),
                                    self.platform)
            value = reg.edp_dsi_input_select
            if (reg.trans_ddi_function_enable):
                if (self.CheckTransDDIModeSelect(port_name, reg.trans_ddi_mode_select, gfx_index)):
                    if (port_name == "MIPI_A"):
                        mapped_ddi = "DDI_A"
                    elif (port_name == "MIPI_C"):
                        mapped_ddi = "DDI_B"
                    else:
                        mapped_ddi = self.GetTransDDISelectMapping(reg.ddi_select, gfx_index)
                    logging.debug("TRANS_DDI_FUNC_CTL_%s" % (pipe_suffix) + " --> Offset : "
                                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
                    connected_pipe = self.GetPipeMapping(value)
                    logging.debug(port_name + " Connected to %s, %s" % (connected_pipe, mapped_ddi))
                    if transcoder_mapping_details:
                        if pipe_suffix == "EDP":
                            current_transcoder = "transcoder_edp"
                        elif pipe_suffix == "DSI0":
                            current_transcoder = "transcoder_dsi0"
                        elif pipe_suffix == "DSI1":
                            current_transcoder = "transcoder_dsi1"
                        else:
                            current_transcoder = str(mapped_ddi).replace("DDI_", "transcoder_")
                        return str(connected_pipe).lower(), str(mapped_ddi), current_transcoder.lower()
                    return str(connected_pipe), str(mapped_ddi)
        return None, None

    ##
    # @brief        Get pipe and Transcoder to the display port
    # @param[in]    display Display to verify
    # @param[in]    gfx_index graphics adapter
    # @return       int - Integer Values of Connected Transcoder and Pipe from respective Dictionaries
    def get_transcoder_and_pipe(self, display, gfx_index='gfx_0'):
        current_transcoder_pipe = self.GetPipeDDIAttachedToPort(port_name=display, transcoder_mapping_details=True,
                                                                gfx_index=gfx_index)
        current_transcoder, current_pipe = transcoder_dict[current_transcoder_pipe[2]], pipe_dict[
            current_transcoder_pipe[0]]
        logging.debug("current_transcoder : {}, current_pipe : {}".format(current_transcoder, current_pipe))
        return current_transcoder, current_pipe

    ##
    # @brief        Get platform for given adapter
    # @param[in]    gfx_index
    # @return       None, Platform name update in global variable
    def get_platform_for_adapter(self, gfx_index='gfx_0'):
        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        if (gfx_display_hwinfo != None):
            self.platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][De_Base]: Display hardware info is empty for requested adapter "
                      "{}".format(gfx_index),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : For requested adapter display hardware info list is empty!")


##
# @brief Function to get the port to pipe mapping
# @param[in] by_index
# @param[in] gfx_index graphics adapter
# @return dictionary of port and pipe index [0:2, 1:3]
def get_port_to_pipe(by_index=False, gfx_index='gfx_0'):
    port2Pipe = dict()
    platform = None
    machine_info = SystemInfo()
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    if (gfx_display_hwinfo != None):
        platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName

    ports = disp_cfg.get_supported_ports(gfx_index).keys()
    for port in ports:
        if disp_cfg.is_display_active(port, gfx_index):
            base = DisplayBase(port, platform, gfx_index)
            if base.pipe:
                port_index = ord(port[-1:]) - ord('A')
                pipe_index = ord(base.pipe[-1:]) - ord('A')
                if by_index:
                    port2Pipe[port_index] = pipe_index
                else:
                    port2Pipe[port] = base.pipe

    return port2Pipe


##
# @brief Get the DDI transport mode from DPCD 
# @param[in] connector_port Display to verify
# @param[in] gfx_index Graphics adapter
# @return Transport mode value programmed in the DPCD
def CheckDPCDTransportModeSelect(connector_port, gfx_index='gfx_0'):
    display_config = disp_cfg.DisplayConfiguration()
    display_and_adapter_info = display_config.get_display_and_adapter_info_ex(connector_port, gfx_index)
    if type(display_and_adapter_info) is list:
        display_and_adapter_info = display_and_adapter_info[0]

    transport_mode = dpcd.DPCD_getTransportModeSelect(display_and_adapter_info)
    if transport_mode == "MST":
        return DDI_MODE.DP_MST
    elif transport_mode == "SST":
        return DDI_MODE.DP_SST
    elif transport_mode == "DP_128_132_BIT_SYMBOL_MODE":
        return DDI_MODE.DP_128_132_BIT_SYMBOL_MODE

    return None


##
# @brief Get the Pipe Suffix 
# @param[in] pipe connected
# @return suffix attached to pipe
def GetPipeSuffix(pipe):
    suffix = pipe.split("PIPE_")
    suffix = suffix[1]
    return suffix


##
# @brief Get the SSC is supported
# @param[in] display_port display to verify
# @param[in] gfx_index Graphics adapter
# @return True if SSC is enabled in VBT & DPCD
def GetSSC(display_port, gfx_index='gfx_0'):
    vbt = Vbt(gfx_index)
    display_config = disp_cfg.DisplayConfiguration()
    display_and_adapter_info = display_config.get_display_and_adapter_info_ex(display_port, gfx_index)
    if type(display_and_adapter_info) is list:
        display_and_adapter_info = display_and_adapter_info[0]

    ssc_enable_dpcd = dpcd.DPCD_getSSC(display_and_adapter_info)
    # LFP case
    if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                       display_utility.VbtPanelType.LFP_MIPI]:
        logging.debug("INFO : VBT Panel Type:" + str(vbt.block_40.PanelType))
        logging.debug("INFO : VBT SSC Enabled Bits:" + str(vbt.block_40.LvdsSscEnableBits))
        ssc_enable_vbt = (vbt.block_40.LvdsSscEnableBits & (
                (1 << (vbt.block_40.PanelType + 1)) - 1)) >> vbt.block_40.PanelType
    else:
        # DP case
        # 0x8 : bit[3] for SSC enable check
        ssc_enable_vbt = vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Enable
        logging.debug(
            "VBT DP SSC Enable Bit is bit 3 in block1.IntegratedDisplaysSupported; its value = {0}".format(
                vbt.block_1.IntegratedDisplaysSupported.value))
    ssc_dpcd = "ENABLED" if ssc_enable_dpcd else "DISABLED"
    ssc_vbt = "ENABLED" if ssc_enable_vbt else "DISABLED"
    logging.info("INFO : SSC - VBT ({0}) DPCD ({1})".format(ssc_vbt, ssc_dpcd))
    return ssc_enable_dpcd and ssc_enable_vbt


##
# @brief Get the BPP value 
# @param[in] value bits per component value
# @return Bytes per pixel, Bits per Color
def GetBPPValue(value):
    bpc = 0
    if (value == BPC_VALUE.bpc_8):
        bpc = 8
    elif (value == BPC_VALUE.bpc_10):
        bpc = 10
    elif (value == BPC_VALUE.bpc_6):
        bpc = 6
    elif (value == BPC_VALUE.bpc_12):
        bpc = 12
    return float(bpc * 3) / 8, bpc  # RGB - 8bit


##
# @brief Get the BPC, BPP value programmed for each transcoder
# @param[in] displayObj DisplayBase() object
# @param[in] gfx_index graphics adapter
# @return BPC value programmed in the MMIO and corresponding BPP
def GetTranscoderBPCValue(displayObj, gfx_index='gfx_0'):
    reg_bpc = GetTranscoderBPC(displayObj, gfx_index)
    return GetBPPValue(reg_bpc)


##
# @brief Get the BPC value programmed for each transcoder
# @param[in] displayObj DisplayBase() object
# @param[in] gfx_index graphics adapter
# @return BPC value programmed in the MMIO
def GetTranscoderBPC(displayObj, gfx_index='gfx_0'):
    if ((displayObj.display_port == "DP_A") and (
            displayObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL'])):
        suffix = "EDP"
    elif (displayObj.display_port == "MIPI_A"):
        suffix = "DSI0"
    elif (displayObj.display_port == "MIPI_C"):
        suffix = "DSI1"
    else:
        suffix = displayObj.pipe_suffix

    reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL_%s" % (suffix), displayObj.platform,
                            gfx_index=gfx_index)
    logging.debug("TRANS_DDI_FUNC_CTL_" + suffix + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))
    return reg.bits_per_color


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

    DisplayBase("DP_A")
