######################################################################################
# @file         lnl_clock_helper.py
# @brief        Python helper script for doing LNL generic PLL and PHY functions
# @author       Goutham N
######################################################################################

import logging
import time
from enum import Enum
from typing import List, Tuple, Dict

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen15 import Gen15NonAutoGenRegs
from DisplayRegs.Gen15 import LnlSnpsPhyRegisters
from registers.mmioregister import MMIORegister


##
# @brief Enumeration of message bus command types and respective values to program in register field.
class MESSAGE_BUS_COMMANDS(Enum):
    NOP = 0b0000
    WRITE_UNCMT = 0b0001
    WRITE_CMT = 0b0010
    READ = 0b0011
    READ_COMPLETION = 0b0100
    WRITE_ACK = 0b0101


##
# @brief Set of registers that are helpful to access the C20 PHY SRAM/CREG registers via Message bus to APB transaction.
class C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS(Enum):
    PHY_WR_ADDRESS_L = 0xC02
    PHY_WR_ADDRESS_H = 0xC03
    PHY_WR_DATA_L = 0xC04
    PHY_WR_DATA_H = 0xC05
    PHY_RD_ADDRESS_L = 0xC06
    PHY_RD_ADDRESS_H = 0xC07
    PHY_RD_DATA_L = 0xC08
    PHY_RD_DATA_H = 0xC09


##
# @brief Class that holds objects of all C10 VDR registers. Used for reading and storing values.
class SnpsC10Regs:
    phy_c10_vdr_pll0: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL0 = None
    phy_c10_vdr_pll1: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL1 = None
    phy_c10_vdr_pll2: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL2 = None
    phy_c10_vdr_pll3: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL3 = None
    phy_c10_vdr_pll4: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL4 = None
    phy_c10_vdr_pll5: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL5 = None
    phy_c10_vdr_pll6: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL6 = None
    phy_c10_vdr_pll7: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL7 = None
    phy_c10_vdr_pll8: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL8 = None
    phy_c10_vdr_pll9: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL9 = None
    phy_c10_vdr_pll10: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL10 = None
    phy_c10_vdr_pll11: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL11 = None
    phy_c10_vdr_pll12: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL12 = None
    phy_c10_vdr_pll13: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL13 = None
    phy_c10_vdr_pll14: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL14 = None
    phy_c10_vdr_pll15: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL15 = None
    phy_c10_vdr_pll16: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL16 = None
    phy_c10_vdr_pll17: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL17 = None
    phy_c10_vdr_pll18: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL18 = None
    phy_c10_vdr_pll19: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL19 = None
    phy_c10_vdr_cmn0: LnlSnpsPhyRegisters.REG_PHY_C10_VDR_CMN0 = None


##
# @brief Class that holds objects of all C20 SRAM MPLL registers. Used for reading and storing values.
class SnpsC20Regs:
    sram_generic_mpllb_cntx_cfg_10: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_10 = None
    sram_generic_mpllb_cntx_cfg_9: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_9 = None
    sram_generic_mpllb_cntx_cfg_8: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_8 = None
    sram_generic_mpllb_cntx_cfg_7: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_7 = None
    sram_generic_mpllb_cntx_cfg_6: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_6 = None
    sram_generic_mpllb_cntx_cfg_5: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_5 = None
    sram_generic_mpllb_cntx_cfg_4: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_4 = None
    sram_generic_mpllb_cntx_cfg_3: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_3 = None
    sram_generic_mpllb_cntx_cfg_2: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_2 = None
    sram_generic_mpllb_cntx_cfg_1: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_1 = None
    sram_generic_mpllb_cntx_cfg_0: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_0 = None

    sram_generic_mplla_cntx_cfg_9: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_9 = None
    sram_generic_mplla_cntx_cfg_8: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_8 = None
    sram_generic_mplla_cntx_cfg_7: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_7 = None
    sram_generic_mplla_cntx_cfg_6: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_6 = None
    sram_generic_mplla_cntx_cfg_5: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_5 = None
    sram_generic_mplla_cntx_cfg_4: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_4 = None
    sram_generic_mplla_cntx_cfg_3: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_3 = None
    sram_generic_mplla_cntx_cfg_2: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_2 = None
    sram_generic_mplla_cntx_cfg_1: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_1 = None
    sram_generic_mplla_cntx_cfg_0: LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_0 = None


##
# @brief Helper class for LNL clock related methods.
class LnlClockHelper:
    # Map of ddi to bspec name convention
    ddi_to_bspec_name_map = dict([
        ('A', 'A'),
        ('B', 'B'),
        ('F', 'USBC1'),
        ('G', 'USBC2'),
        ('H', 'USBC3'),
        ('I', 'USBC4')
    ])

    ##
    # @brief        private method to do the series of operations needed to write into PORT_M2P_MSGBUS_CTL register.
    # @param[in]    display_port    port name for whose PHY we are writing to. Like DP_A, HDMI_B, DP_F, etc.
    # @param[in]    cmd_type        the type of command. Accepted values from MESSAGE_BUS_COMMANDS enumeration.
    # @param[in]    address         C10 or C20 PHY target VDR register address.
    # @param[in]    data            buffer data that needs to be sent.
    # @param[in]    gfx_index       Adapter to use.
    # @param[in]    msgbus_lane     Msgbus lane (integer) to use among the available [0,1] lanes.
    # @return       True/False if Success/fail respectively.
    def __write_m2p_msgbus_ctl(self, display_port, cmd_type, address, data, gfx_index, msgbus_lane=0):
        msgbus_ctl = 0
        bspec_port_name = self.ddi_to_bspec_name_map[display_port.split('_')[1]]
        # PLL programming must use lane 0 message bus. So by default we use LN0 MSGBUS, unless explicitly specified.
        offset = eval('Gen15NonAutoGenRegs.OFFSET_PORT_M2P_MSGBUS_CTL.PORT_M2P_MSGBUS_CTL_LN' + str(msgbus_lane) +
                      '_' + bspec_port_name)

        # Before writing, poll for Transaction Pending==0 in PORT_M2P_MSGBUS_CTL
        # SW shall poll on this bit to ensure no transaction is pending before launching a new transaction.
        for iteration in range(5):
            value = DisplayArgs.read_register(offset, gfx_index)
            msgbus_ctl = Gen15NonAutoGenRegs.REG_PORT_M2P_MSGBUS_CTL(offset, value)
            if msgbus_ctl.TransactionPending == 0:
                break
            time.sleep(0.5)
        if msgbus_ctl.TransactionPending == 1:
            logging.error(f'Before write, PORT_M2P_MSGBUS_CTL_LN{msgbus_lane}_{bspec_port_name}.TransactionPending '
                          f'did not clear even after 5 poll iterations.')
            return False

        # Write to PORT_M2P_MSGBUS_CTL
        value = 0
        msgbus_ctl = Gen15NonAutoGenRegs.REG_PORT_M2P_MSGBUS_CTL(offset, value)
        msgbus_ctl.TransactionPending = 1
        msgbus_ctl.CommandType = cmd_type.value
        msgbus_ctl.Address = address
        msgbus_ctl.Data = data
        DisplayArgs.write_register(offset, msgbus_ctl.value, gfx_index)

        # Poll for Transaction Pending==0 in PORT_M2P_MSGBUS_CTL
        for iteration in range(5):
            value = DisplayArgs.read_register(offset, gfx_index)
            msgbus_ctl = Gen15NonAutoGenRegs.REG_PORT_M2P_MSGBUS_CTL(offset, value)
            if msgbus_ctl.TransactionPending == 0:
                break
            time.sleep(0.5)

        if msgbus_ctl.TransactionPending == 0:
            return True
        else:
            logging.error(f'After write, PORT_M2P_MSGBUS_CTL_LN{msgbus_lane}_{bspec_port_name}.TransactionPending '
                          f'did not clear even after 5 poll iterations.')
            return False

    ##
    # @brief        private method to do the series of operations needed to read from PORT_P2M_MSGBUS_STATUS register.
    # @param[in]    display_port            port name for whose PHY we are writing to. Like DP_A, HDMI_B, DP_F, etc.
    # @param[in]    cmd_response_expected   the type of command response expected after reading the register.
    #               Can take values from MESSAGE_BUS_COMMANDS enumeration.
    # @param[in]    gfx_index               Adapter to use.
    # @param[in]    msgbus_lane     Msgbus lane (integer) to use among the available [0,1] lanes.
    # @return       ret_status, data_read: True/False if Success/fail respectively, the data read from
    #               PORT_P2M_MSGBUS_STATUS register
    def __read_p2m_msgbus_status(self, display_port, cmd_response_expected, gfx_index, msgbus_lane=0):
        ret_status = False
        data_read = None
        bspec_port_name = self.ddi_to_bspec_name_map[display_port.split('_')[1]]
        # PLL programming must use lane 0 message bus. So by default we use LN0 MSGBUS, unless explicitly specified.
        offset = eval('Gen15NonAutoGenRegs.OFFSET_PORT_P2M_MSGBUS_STATUS.PORT_P2M_MSGBUS_STATUS_LN' + str(msgbus_lane) +
                      '_' + bspec_port_name)

        # Read PORT_P2M_MSGBUS_STATUS. Poll for ResponseReady == 1.
        # Poll for CommandType whose value should be 'Read completion' for read cmd sent previously in M2P,
        # or 'Write Ack' for write committed cmd sent previously in M2P (no need to poll this for write uncommitted).
        for iteration in range(5):
            value = DisplayArgs.read_register(offset, gfx_index)
            msgbus_status = Gen15NonAutoGenRegs.REG_PORT_P2M_MSGBUS_STATUS(offset, value)

            # if HW sets Error set bit, it means there is some error while doing read transaction.
            if msgbus_status.ErrorSet == 1:
                logging.error(f'Error while reading Snps PHY registers through '
                              f'PORT_P2M_MSGBUS_STATUS_LN{msgbus_lane}_{bspec_port_name}')
                break

            if msgbus_status.ResponseReady == 1:
                if cmd_response_expected == MESSAGE_BUS_COMMANDS.NOP:  # Use this for write uncommitted.
                    ret_status = True
                    break
                if cmd_response_expected == MESSAGE_BUS_COMMANDS.READ_COMPLETION and \
                        msgbus_status.CommandType == cmd_response_expected.value:
                    data_read = msgbus_status.Data
                    ret_status = True
                    break
                if cmd_response_expected == MESSAGE_BUS_COMMANDS.WRITE_ACK and \
                        msgbus_status.CommandType == cmd_response_expected.value:
                    ret_status = True
                    break
            time.sleep(0.5)

        # Do a Write clear. SW should not set PORT_M2P_MSGBUS_CTL[Transaction pending] bit without
        # clearing Response ready bit and Error bit set in this register.
        value = 0
        msgbus_status = Gen15NonAutoGenRegs.REG_PORT_P2M_MSGBUS_STATUS(offset, value)
        msgbus_status.ResponseReady = 1
        msgbus_status.ErrorSet = 1
        DisplayArgs.write_register(offset, msgbus_status.value, gfx_index)

        # Return the data read.
        return ret_status, data_read

    ##
    # @brief        private method to help do write clear into P2M_MSGBUS_STATUS register
    # @param[in]    display_port            port name for whose PHY we are writing to. Like DP_A, HDMI_B, DP_F, etc.
    # @param[in]    gfx_index               Adapter to use.
    # @param[in]    msgbus_lane     Msgbus lane (integer) to use among the available [0,1] lanes.
    # @return       None
    def __write_clear_p2m_msgbus_status_register(self, display_port, gfx_index, msgbus_lane=0):

        bspec_port_name = self.ddi_to_bspec_name_map[display_port.split('_')[1]]
        # PLL programming must use lane 0 message bus. So by default we use LN0 MSGBUS, unless explicitly specified.
        offset = eval('Gen15NonAutoGenRegs.OFFSET_PORT_P2M_MSGBUS_STATUS.PORT_P2M_MSGBUS_STATUS_LN' + str(msgbus_lane) +
                      '_' + bspec_port_name)

        # Do a Write clear. SW should not set PORT_M2P_MSGBUS_CTL[Transaction pending] bit without
        # clearing Response ready bit and Error bit set in this register.
        value = DisplayArgs.read_register(offset, gfx_index)
        DisplayArgs.write_register(offset, value, gfx_index)

    ##
    # @brief        Exposed API to read the C10 PHY VDR registers.
    # @details      Ref: Message bus : https://gfxspecs.intel.com/Predator/Home/Index/64599
    #               C10 PHY register programming and example: https://gfxspecs.intel.com/Predator/Home/Index/67636
    # @param[in]    display_port    port name for whose PHY we are writing to. Like DP_A, HDMI_B, DP_F, etc.
    # @param[in]    address         C10 PHY target VDR register address.
    # @param[in]    gfx_index       Adapter to use.
    # @param[in]    msgbus_lane     Msgbus lane (integer) to use among the available [0,1] lanes.
    # @return       returns the data read from the C10 PHY register.
    def read_c10_phy_vdr_register(self, gfx_index, display_port, address, msgbus_lane=0):

        # Write the address and command type to Message bus CTL register as per format
        if not self.__write_m2p_msgbus_ctl(display_port, MESSAGE_BUS_COMMANDS.READ, address, 0x0, gfx_index,
                                           msgbus_lane=msgbus_lane):
            logging.error(f'Failed to read {address} for {display_port} on {gfx_index}')
            return None

        # Read the Message bus Status for READ_COMPLETION
        ret, data_read = self.__read_p2m_msgbus_status(display_port, MESSAGE_BUS_COMMANDS.READ_COMPLETION, gfx_index,
                                                       msgbus_lane=msgbus_lane)
        if data_read is None:
            logging.error(f'Failed to read {address} for {display_port} on {gfx_index}')

        return data_read

    ##
    # @brief        Exposed API to read the C20 PHY SRAM registers.
    # @details      Ref: Message bus : https://gfxspecs.intel.com/Predator/Home/Index/64599
    #               C20 PHY register programming and example: https://gfxspecs.intel.com/Predator/Home/Index/67610
    # @param[in]    display_port    port name for whose PHY we are writing to. Like DP_A, HDMI_B, DP_F, etc.
    # @param[in]    address         C20 PHY target VDR register address.
    # @param[in]    gfx_index       Adapter to use.
    # @param[in]    msgbus_lane     Msgbus lane (integer) to use among the available [0,1] lanes.
    # @return       returns the data read from the C20 PHY register.
    def read_c20_phy_sram_register(self, gfx_index, display_port, address, msgbus_lane=0):
        address_high = (address >> 8) & 0xFF
        address_low = address & 0xFF

        # 0. Do Write clear of P2M_MSGBUS_STATUS register as without this, SRAM register reads are sometimes failing
        # by not receiving WRITE_ACK.
        self.__write_clear_p2m_msgbus_status_register(display_port, gfx_index, msgbus_lane=msgbus_lane)

        # 1. Send Uncommitted write command to Message bus CTL register. Address is VDR PHY_RD_ADDRESS_H and data is
        # address_high part of APB register to read.
        if not self.__write_m2p_msgbus_ctl(display_port, MESSAGE_BUS_COMMANDS.WRITE_UNCMT,
                                           C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_ADDRESS_H.value,
                                           address_high, gfx_index, msgbus_lane=msgbus_lane):
            logging.error(f'Failed to write to {C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_ADDRESS_H} for '
                          f'{display_port} on {gfx_index}')
            return None

        # 2. Send Committed write command to Message bus CTL register. Address is VDR PHY_RD_ADDRESS_L and data is
        # address_low part of APB register to read.
        if not self.__write_m2p_msgbus_ctl(display_port, MESSAGE_BUS_COMMANDS.WRITE_CMT,
                                           C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_ADDRESS_L.value,
                                           address_low, gfx_index, msgbus_lane=msgbus_lane):
            logging.error(f'Failed to write to {C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_ADDRESS_L} for '
                          f'{display_port} on {gfx_index}')
            return None

        # 3. Read the Message bus Status register for WRITE_ACK.
        ret, data_read = self.__read_p2m_msgbus_status(display_port, MESSAGE_BUS_COMMANDS.WRITE_ACK, gfx_index,
                                                       msgbus_lane=msgbus_lane)
        if ret is False:
            logging.error(f'After committed write for APB offset {address}, Write Ack not received in '
                          f'PORT_P2M_MSGBUS_STATUS polling. For {display_port} on {gfx_index}.')
            return None

        # 4. Send Read command to Message bus CTL register. Address is VDR PHY_RD_DATA_H.
        if not self.__write_m2p_msgbus_ctl(display_port, MESSAGE_BUS_COMMANDS.READ,
                                           C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_DATA_H.value,
                                           0x0, gfx_index, msgbus_lane=msgbus_lane):
            logging.error(f'Failed to write to {C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_DATA_H} for '
                          f'{display_port} on {gfx_index}')
            return None

        # 5. Read the Message bus Status register for READ_COMPLETION. Data received will be high part of APB register.
        ret, data_high = self.__read_p2m_msgbus_status(display_port, MESSAGE_BUS_COMMANDS.READ_COMPLETION, gfx_index,
                                                       msgbus_lane=msgbus_lane)
        if data_high is None:
            logging.error(f'After committed write for APB offset {address} and data read request sent, read completion '
                          f'status not received or data_high not received in PORT_P2M_MSGBUS_STATUS. '
                          f'For {display_port} on {gfx_index}.')
            return None

        # 6. Send Read command to Message bus CTL register. Address is VDR PHY_RD_DATA_L.
        if not self.__write_m2p_msgbus_ctl(display_port, MESSAGE_BUS_COMMANDS.READ,
                                           C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_DATA_L.value,
                                           0x0, gfx_index, msgbus_lane=msgbus_lane):
            logging.error(f'Failed to write to {C20_MSGBUS_TO_APB_TRANSACTION_REGISTERS.PHY_RD_DATA_L} for '
                          f'{display_port} on {gfx_index}')
            return None

        # 7. Read the Message bus Status register for READ_COMPLETION. Data received will be low part of APB register.
        ret, data_low = self.__read_p2m_msgbus_status(display_port, MESSAGE_BUS_COMMANDS.READ_COMPLETION, gfx_index,
                                                      msgbus_lane=msgbus_lane)
        if data_low is None:
            logging.error(f'After committed write for APB offset {address} and data read request sent, read completion '
                          f'status not received or data_low not received in PORT_P2M_MSGBUS_STATUS. '
                          f'For {display_port} on {gfx_index}.')
            return None

        # return the 16-bit data (combine data_high and data_low parts)
        return (data_high << 8) | data_low

    ##
    # @brief        Helper function to read all C10 VDR registers and return the data-filled class reference.
    # @param[in]    display_port    port name for whose PHY we are writing to. Like DP_A, HDMI_B, etc.
    # @param[in]    gfx_index       Adapter to use.
    # @return       returns the data-filled reference of class SnpsC10Regs
    def read_all_c10_vdr_registers_helper(self, display_port, gfx_index='gfx_0'):

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL0.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll0 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL0(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL1.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll1 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL1(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL2.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll2 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL2(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL3.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll3 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL3(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL4.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll4 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL4(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL5.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll5 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL5(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL6.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll6 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL6(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL7.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll7 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL7(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL8.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll8 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL8(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL9.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll9 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL9(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL10.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll10 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL10(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL11.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll11 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL11(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL12.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll12 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL12(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL13.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll13 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL13(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL14.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll14 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL14(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL15.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll15 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL15(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL16.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll16 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL16(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL17.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll17 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL17(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL18.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll18 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL18(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_PLL19.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_pll19 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_PLL19(offset, value)

        offset = LnlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_CMN0.offset
        value = self.read_c10_phy_vdr_register(gfx_index, display_port, offset)
        SnpsC10Regs.phy_c10_vdr_cmn0 = LnlSnpsPhyRegisters.REG_PHY_C10_VDR_CMN0(offset, value)

        return SnpsC10Regs

    ##
    # @brief        Helper function to read all C20 SRAM registers for respective context and MPLL required
    #               and return the data-filled class reference.
    # @param[in]    display_port      port name for whose PHY we are writing to. Like DP_A, HDMI_B, etc.
    # @param[in]    current_context   C20 has two contexts/sets of registers A and B. This param specifies the context
    # @param[in]    mpll              string specifying which MPLL to use, i.e. MPLLA / MPPLB
    # @param[in]    gfx_index         Adapter to use
    # @return       returns the data-filled reference of class SnpsC20Regs
    def read_all_c20_sram_mpll_registers_helper(self, gfx_index, display_port, current_context, mpll):

        if mpll == 'MPLLB':
            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_10.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_10 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_10(offset,
                                                                                                                value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_9.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_9 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_9(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_8.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_8 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_8(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_7.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_7 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_7(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_6.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_6 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_6(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_5.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_5 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_5(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_4.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_4 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_4(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_3.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_3 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_3(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_2.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_2 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_2(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_1.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_1 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_1(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLB_CNTX_CFG_0.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mpllb_cntx_cfg_0 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLB_CNTX_CFG_0(offset,
                                                                                                              value)

        elif mpll == 'MPLLA':
            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_9.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_9 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_9(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_8.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_8 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_8(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_7.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_7 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_7(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_6.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_6 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_6(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_5.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_5 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_5(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_4.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_4 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_4(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_3.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_3 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_3(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_2.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_2 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_2(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_1.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_1 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_1(offset,
                                                                                                              value)

            offset = eval('LnlSnpsPhyRegisters.OFFSET_SRAM_GENERIC_MPLLA_CNTX_CFG_0.CONTEXT_' + current_context)
            value = self.read_c20_phy_sram_register(gfx_index, display_port, offset)
            SnpsC20Regs.sram_generic_mplla_cntx_cfg_0 = LnlSnpsPhyRegisters.REG_SRAM_GENERIC_MPLLA_CNTX_CFG_0(offset,
                                                                                                              value)
        else:
            logging.error(f'Invalid MPLL = {mpll} passed')
            return None

        return SnpsC20Regs

    ##
    # @brief        Get maximum DDI symbol clock frequency for active displays
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @param[in]    ports: List[str]
    #                   List of port names for active display
    # @return       (target_id, symbol_clock_frequency): (int, float)
    #                   returns tuple of target ID, and it's symbol clock frequency
    @classmethod
    def get_max_ddi_symbol_clock_frequency(cls, gfx_index: str, ports: List[str]) -> Tuple[str, float]:
        # Store link rates per panel connected to port for comparison
        symbol_frequencies: Dict[str, float] = dict()

        for port_name in ports:
            port_ddi = cls.ddi_to_bspec_name_map[port_name[-1].upper()]
            offset = eval(
                'Gen15NonAutoGenRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_' + port_ddi.replace('USBC', 'USB'))
            value = DisplayArgs.read_register(offset, gfx_index)
            ddi_clk_valfreq = Gen15NonAutoGenRegs.REG_DDI_CLK_VALFREQ(offset, value)
            logging.info(f'DDI Clk ValFreq = 0x{ddi_clk_valfreq.value:X}')
            logging.info(f"ddi_clk_valfreq_value = {ddi_clk_valfreq.DdiValidationFrequency}")

            valfreq = ddi_clk_valfreq.DdiValidationFrequency / 1000  # KHz to MHz
            logging.info(f"DDI CLK ValFreq for {port_name} = {valfreq} MHz")
            symbol_frequencies[port_name] = valfreq

        logging.info(f"Symbol frequencies - {symbol_frequencies}")
        max_ddi_freq = max(symbol_frequencies.values())
        return list(symbol_frequencies.keys())[list(symbol_frequencies.values()).index(max_ddi_freq)], max_ddi_freq
