######################################################################################
# @file         mipi.py
# @brief        Python module providing APIs to get MIPI encoder information
# @author       Sri Sumanth Geesala
######################################################################################
from enum import IntEnum

from Libs.Core.machine_info.machine_info import SystemInfo

from registers.bxt.MIPI_DSI_FUNC_PRG_REG_REGISTER import *
from registers.bxt.MIPI_PORT_CTRL_REGISTER import *
from registers.icl.DSS_CTL1_REGISTER import *
from registers.icl.TRANS_DDI_FUNC_CTL2_REGISTER import *
from registers.icl.TRANS_DSI_FUNC_CONF_REGISTER import *
from registers.lkf1.PIPE_DSS_CTL1_REGISTER import *
from registers.mmioregister import MMIORegister


##
# @brief Enum for MIPI modes of operation
class MipiMode(IntEnum):
    VIDEO = 0
    COMMAND = 1


##
# @brief Enum for MIPI single link / dual link modes
class MipiDualLinkMode(IntEnum):
    NOT_SUPPORTED = 0
    FRONT_BACK = 1
    INTERLEAVE = 2


##
# @brief Mipi class that has APIs to get MIPI encoder information
class Mipi(object):

    ##
    # @brief Mipi class constructor.
    def __init__(self):
        self.machine_info = SystemInfo()
        self.platform = None
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

    ##
    # @brief        Get mipi mode of operation for the port passed, whether it is video mode or command mode.
    # @param[in]    mipi_port mipi port name
    # @return       enum of type MipiMode.
    def get_mipi_mode_of_operation(self, mipi_port):
        if self.platform in ["bxt", "apl", "glk"]:
            if mipi_port == 'MIPI_A':
                port = 'MIPIA'
            elif mipi_port == 'MIPI_C':
                port = 'MIPIC'
            else:
                return None

            mipi_dsi_func_prg_reg = MMIORegister.read("MIPI_DSI_FUNC_PRG_REG_REGISTER", port + "_DSI_FUNC_PRG_REG",
                                                      "bxt")
            if mipi_dsi_func_prg_reg.supported_format_in_video_mode != supported_format_in_video_mode_VIDEO_MODE_NOT_SUPPORTED:
                return MipiMode.VIDEO
            elif mipi_dsi_func_prg_reg.supported_data_width_in_command_mode != supported_data_width_in_command_mode_COMMAND_MODE_NOT_SUPPORTED:
                return MipiMode.COMMAND
            else:
                return None
        else:  # ICLLP and above
            if mipi_port == 'MIPI_A':
                port = 'DSI0'
            elif mipi_port == 'MIPI_C':
                port = 'DSI1'
            else:
                return None

            trans_dsi_func_conf_reg = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF_" + port,
                                                        "icl")
            if trans_dsi_func_conf_reg.mode_of_operation == mode_of_operation_VIDEO_MODE_SYNC_EVENT or \
                    trans_dsi_func_conf_reg.mode_of_operation == mode_of_operation_VIDEO_MODE_SYNC_PULSE:
                return MipiMode.VIDEO
            elif trans_dsi_func_conf_reg.mode_of_operation == mode_of_operation_COMMAND_MODE_NO_GATE or \
                    trans_dsi_func_conf_reg.mode_of_operation == mode_of_operation_COMMAND_MODE_TE_GATE:
                return MipiMode.COMMAND
            else:
                return None

    ##
    # @brief        Get dual link mode, whether it is front back or interleaved or dual link not supported.
    # @return       enum of type MipiDualLinkMode.
    def get_mipi_dual_link_mode(self):
        if self.platform in ["bxt", "apl", "glk"]:
            mipia_port_ctrl_reg = MMIORegister.read("MIPI_PORT_CTRL_REGISTER", "MIPIA_PORT_CTRL", "bxt")
            mipic_port_ctrl_reg = MMIORegister.read("MIPI_PORT_CTRL_REGISTER", "MIPIC_PORT_CTRL", "bxt")

            # in dual link case, both ports will be enabled
            if mipia_port_ctrl_reg.en == en_ENABLE and mipic_port_ctrl_reg.en == en_ENABLE:
                if mipia_port_ctrl_reg.mipi_dual_link_mode == mipi_dual_link_mode_FRONT_BACK:
                    return MipiDualLinkMode.FRONT_BACK
                else:
                    return MipiDualLinkMode.INTERLEAVE
            else:
                return MipiDualLinkMode.NOT_SUPPORTED
        else:
            if self.platform in ["icllp", "jsl"]:
                dss_ctl1_reg = MMIORegister.read("DSS_CTL1_REGISTER", "DSS_CTL1", "icl")
            else:  # LKF and above
                # If dual link, it means only 1 MIPI panel connected, so it will be on pipeA
                dss_ctl1_reg = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", "PIPE_DSS_CTL1_PA", "lkf1")

            trans_ddi_func_ctl2_dsi0_reg = MMIORegister.read("TRANS_DDI_FUNC_CTL2_REGISTER", "TRANS_DDI_FUNC_CTL2_DSI0",
                                                             "icl")

            if trans_ddi_func_ctl2_dsi0_reg.port_sync_mode_enable == port_sync_mode_enable_ENABLE and \
                    dss_ctl1_reg.splitter_enable == splitter_enable_ENABLE:
                if dss_ctl1_reg.dual_link_mode == dual_link_mode_FRONT_BACK_MODE:
                    return MipiDualLinkMode.FRONT_BACK
                else:
                    return MipiDualLinkMode.INTERLEAVE
            else:
                return MipiDualLinkMode.NOT_SUPPORTED

    ##
    # @brief    Get whether dual link is enabled or not.
    # @return   returns True if MIPI is configured to dual link mode or False otherwise.
    def is_mipi_dual_link(self):
        if self.get_mipi_dual_link_mode() == MipiDualLinkMode.NOT_SUPPORTED:
            return False
        else:
            return True
