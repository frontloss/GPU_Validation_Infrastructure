###############################################################################################################
# \file         gen9_verify_voltage_swing.py
# \addtogroup   PyLibs_Voltage_swing
# \brief        Python class to validate GEN9 (SKL, KBL, CFL) Voltage swing programming
#               GEN9VerifyVoltageSwing class exposes an interface verify_voltage_swing which is internal and used by voltage_swing.py
# \author       Girish Y D
###############################################################################################################
import logging

from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.voltage_swing import voltage_swing_helper

from registers.mmioregister import MMIORegister


##
# \brief - Class to verify GEN9 (SKL, KBL, CFL) Voltage swing programming
class GEN9VerifyVoltageSwing:
    # As voltage swing registers and values are same for all GEN9 platforms, platform is set to 'SKL'
    platform = "SKL"  # by default assigning to SKL as registers for KBL/CFL is same as SKL
    ddi_buf_trans_dword0 = 0
    ddi_buf_trans_dword1 = 0
    expected_tx_blnclegsctl = 0

    ##
    # list of hdmi voltage swing values  for other than ULX SKU as per Bspec
    # [ddi_buf_trans_dword0, ddi_buf_trans_dword1]
    hdmi_voltage_swing_values = [
        [0x00000018, 0x000000AC],
        [0x00005012, 0x0000009D],
        [0x00007011, 0x00000088],
        [0x00000018, 0x000000A1],
        [0x00000018, 0x00000098],
        [0x00004013, 0x00000088],
        [0x80006012, 0x000000CD],
        [0x00000018, 0x000000DF],
        [0x80003015, 0x000000CD],
        [0x80003015, 0x000000C0],
        [0x80000018, 0x000000C0]
    ]

    ##
    # list of hdmi voltage swing values  for ULX SKU as per Bspec
    # [ddi_buf_trans_dword0, ddi_buf_trans_dword1]
    hdmi_voltage_swing_values_for_ulx = [
        [0x00000018, 0x000000A1],
        [0x00005012, 0x000000DF],
        [0x80007011, 0x000000CB],
        [0x00000018, 0x000000A4],
        [0x00000018, 0x0000009D],
        [0x00004013, 0x00000080],
        [0x80006013, 0x000000C0],
        [0x00000018, 0x0000008A],
        [0x80003015, 0x000000C0],
        [0x80003015, 0x000000C0],
        [0x80000018, 0x000000C0]
    ]

    ##
    # @brief     - Verifies voltage swing programming for the display_port on GEN9 (SKL, KBL, CFL) based on SKU
    #              and this interface will read the current set level shifter configuration from VBT and
    #              use it to verify voltage swing
    #              and this interface verify_voltage_swing which is internal and used by voltage_swing.py
    # @param[in] - vs_test_parameters_obj is of type VoltageSwingTestParameters
    # @return    - True If success; False If Fail
    def verify_voltage_swing(self, vs_test_parameters_obj):
        result = True
        display_port = vs_test_parameters_obj.display_port
        display = str(display_port).split('_')[0]
        port = str(display_port).split('_')[1]

        if display != 'HDMI':
            logging.error("verify_voltage_swing is not implemented for %s" % display)
            return False

        # Get Level shifter configuration level set in VBT
        result, level_shifter_configuration_level = voltage_swing_helper.get_vbt_hdmi_level_shifter_configuration(
            self.platform,
            display_port)
        if result is False or level_shifter_configuration_level is None:
            return False

        # Get iboost details from VBT
        result, iboost_enabled, iboost_magnitude = voltage_swing_helper.get_iboost_details(self.platform, display_port)
        if result is False:
            return False

        logging.info(
            "########Verify Voltage Swing for Display Port : %s; Level : %s ; iboost_eanbled : %s; iboost_magnitude: %s ########" % (
            display_port, level_shifter_configuration_level, iboost_enabled, iboost_magnitude))

        # Get SKU details
        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            sku = gfx_display_hwinfo[i].SkuName
            break

        if sku is None:
            logging.error("Failed to get SKU Details using the API get_machine_info")

        # Fill the Voltage swing values to be verified based on SKU And iboost
        index = level_shifter_configuration_level
        if (sku.upper().find('ULX') != -1):
            self.ddi_buf_trans_dword0 = self.hdmi_voltage_swing_values_for_ulx[index][0]
            self.ddi_buf_trans_dword1 = self.hdmi_voltage_swing_values_for_ulx[index][1]
            self.expected_tx_blnclegsctl = 0x3
        else:
            self.ddi_buf_trans_dword0 = self.hdmi_voltage_swing_values[index][0]
            self.ddi_buf_trans_dword1 = self.hdmi_voltage_swing_values[index][1]
            self.expected_tx_blnclegsctl = 0x1

        if iboost_enabled == 1:
            self.ddi_buf_trans_dword0 |= 0x80000000
            self.expected_tx_blnclegsctl = iboost_magnitude

        # Verify voltage swing values as per bspec
        ##
        # DDI_BUF_CTL
        ddi_buf_ctl_reg_offset_name = 'DDI_BUF_CTL_%s' % port
        ddi_buf_ctl_reg = MMIORegister.read("DDI_BUF_CTL_REGISTER", ddi_buf_ctl_reg_offset_name,
                                            self.platform)
        expected_ddi_buffer_enable = 0b1
        result &= voltage_swing_helper.verify_register_bit_fields(ddi_buf_ctl_reg_offset_name, ddi_buf_ctl_reg,
                                                                  "ddi_buffer_enable",
                                                                  expected_ddi_buffer_enable)

        ##
        # DISPIO_CR_TX_BMU_CR0
        dispio_cr_tx_bmu_cr0_reg_offset_name = 'DISPIO_CR_TX_BMU_CR0'
        dispio_cr_tx_bmu_cr0_reg = MMIORegister.read("DISPIO_CR_TX_BMU_CR0_REGISTER",
                                                     dispio_cr_tx_bmu_cr0_reg_offset_name,
                                                     self.platform)
        expected_tx_blnclegdisbl = 0x00
        result &= voltage_swing_helper.verify_register_bit_fields(dispio_cr_tx_bmu_cr0_reg_offset_name,
                                                                  dispio_cr_tx_bmu_cr0_reg,
                                                                  "tx_blnclegdisbl", expected_tx_blnclegdisbl)

        tx_blnclegsctl = 'tx_blnclegsctl_1'
        if port == 'B':
            tx_blnclegsctl = 'tx_blnclegsctl_1'
        elif port == 'C':
            tx_blnclegsctl = 'tx_blnclegsctl_2'
        elif port == 'D':
            tx_blnclegsctl = 'tx_blnclegsctl_3'
        result &= voltage_swing_helper.verify_register_bit_fields(dispio_cr_tx_bmu_cr0_reg_offset_name,
                                                                  dispio_cr_tx_bmu_cr0_reg,
                                                                  tx_blnclegsctl,
                                                                  self.expected_tx_blnclegsctl)

        ##
        # DDI_BUF_TRANS ENTRY9 DWORD0
        ddi_buf_trans_entry9_dword0_offset_name = 'DDI_BUF_TRANS_%s_ENTRY9_DWORD0' % port

        ddi_buf_trans_entry9_dword0 = MMIORegister.read("DDI_BUF_TRANS_REGISTER",
                                                        ddi_buf_trans_entry9_dword0_offset_name,
                                                        self.platform)
        result &= voltage_swing_helper.verify_register_bit_fields(ddi_buf_trans_entry9_dword0_offset_name,
                                                                  ddi_buf_trans_entry9_dword0,
                                                                  "dword",
                                                                  self.ddi_buf_trans_dword0)

        ##
        # DDI_BUF_TRANS ENTRY9 DWORD1
        ddi_buf_trans_entry9_dword1_offset_name = 'DDI_BUF_TRANS_%s_ENTRY9_DWORD1' % port

        ddi_buf_trans_entry9_dword1 = MMIORegister.read("DDI_BUF_TRANS_REGISTER",
                                                        ddi_buf_trans_entry9_dword1_offset_name,
                                                        self.platform)
        result &= voltage_swing_helper.verify_register_bit_fields(ddi_buf_trans_entry9_dword1_offset_name,
                                                                  ddi_buf_trans_entry9_dword1,
                                                                  "dword",
                                                                  self.ddi_buf_trans_dword1)
        return result
