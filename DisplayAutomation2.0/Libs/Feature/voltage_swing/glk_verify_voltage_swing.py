###############################################################################################################
# \file         glk_verify_voltage_swing.py
# \addtogroup   PyLibs_Voltage_swing
# \brief        Python class to validate GLK Voltage swing programming
#               GLKVerifyVoltageSwing class exposes an interface verify_voltage_swing which is internal and used by voltage_swing.py
# \author       Girish Y D
###############################################################################################################
import logging

from Libs.Feature.clock.glk import glk_clock_pll
from Libs.Feature.voltage_swing import voltage_swing_helper

from registers.mmioregister import MMIORegister


##
# \brief - Class to verify GLK Voltage swing programming
class GLKVerifyVoltageSwing:
    platform = "glk"
    scale_enable = 0
    scale_value = "DoNotCare"
    deemphasis_decimal = 0
    deemphasis_decimal_ln3 = 0
    swing_decimal = 0

    ##
    # list of hdm voltage swing values for active level shifter
    # [scale_enable,  scale_value, deemphasis_decimal, deemphasis_decimal_ln3, swing_decimal] as per Bpsec
    hdmi_active_level_shifter_voltage_swing_values = [
        [0, 'DoNotCare', 128, 128, 52],
        [0, 'DoNotCare', 85, 85, 78],
        [0, 'DoNotCare', 64, 64, 104],
        [0, 'DoNotCare', 43, 43, 154],
        [0, 'DoNotCare', 128, 128, 77],
        [0, 'DoNotCare', 85, 85, 116],
        [0, 'DoNotCare', 64, 64, 154],
        [0, 'DoNotCare', 128, 128, 102],
        [0, 'DoNotCare', 85, 85, 154],
        [1, 0x9A, 128, 128, 154]
    ]

    ##
    # list of hdm voltage swing values for passive level shifter
    # [scale_enable,  scale_value, deemphasis_decimal, deemphasis_decimal_ln3, swing_decimal] as per Bpsec
    hdmi_passive_level_shifter_voltage_swing_values = [
        [1, 0x9A, 128, 128, 133],
        [1, 0x9A, 96, 128, 160]
    ]

    ##
    # @brief     - Verifies voltage swing programming for the display_port on GLK based on active/passive level shifter
    #              and this interface will read the current set level shifter configuration from VBT and
    #              use it to verify voltage swing
    #              and this interface verify_voltage_swing which is internal and used by voltage_swing.py
    # @param[in] - vs_test_parameters_obj is of type VoltageSwingTestParameters
    # @return    - True If success; False If Fail
    def verify_voltage_swing(self, vs_test_parameters_obj):
        result = True
        display_port = vs_test_parameters_obj.display_port
        is_active_level_shifter = vs_test_parameters_obj.is_active_level_shifter
        display = str(display_port).split('_')[0]
        port = str(display_port).split('_')[1]

        if display != 'HDMI':
            logging.error("verify_voltage_swing is not implemented for %s" % display)
            return False

        ##
        # Fill/Assign the voltage values to be checked based on active/passive level shifter
        if is_active_level_shifter is True:
            result, level_shifter_configuration_level = voltage_swing_helper.get_vbt_hdmi_level_shifter_configuration(
                self.platform,
                display_port)
            if result is False or level_shifter_configuration_level is None:
                return False

            index = level_shifter_configuration_level
            self.scale_enable = self.hdmi_active_level_shifter_voltage_swing_values[index][0]
            self.scale_value = self.hdmi_active_level_shifter_voltage_swing_values[index][1]
            self.deemphasis_decimal = self.hdmi_active_level_shifter_voltage_swing_values[index][2]
            self.deemphasis_decimal_ln3 = self.hdmi_active_level_shifter_voltage_swing_values[index][3]
            self.swing_decimal = self.hdmi_active_level_shifter_voltage_swing_values[index][4]
        else:
            clock = glk_clock_pll.GlkClockPll()
            self.symbol_freq = clock.calculate_symbol_freq(display_port)
            index = 0
            if self.symbol_freq > 165:
                index = 1

            self.scale_enable = self.hdmi_passive_level_shifter_voltage_swing_values[index][0]
            self.scale_value = self.hdmi_passive_level_shifter_voltage_swing_values[index][1]
            self.deemphasis_decimal = self.hdmi_passive_level_shifter_voltage_swing_values[index][2]
            self.deemphasis_decimal_ln3 = self.hdmi_passive_level_shifter_voltage_swing_values[index][3]
            self.swing_decimal = self.hdmi_passive_level_shifter_voltage_swing_values[index][4]

        # Verify voltage swing values as per bspec
        ##
        # PORT_TX_DW2
        port_tx_dw2_ln0_reg_offset_name = 'PORT_TX_DW2_LN0_%s' % port
        port_tx_dw2_ln0_reg = MMIORegister.read("PORT_TX_DW2_REGISTER", port_tx_dw2_ln0_reg_offset_name,
                                                self.platform)
        port_tx_dw2_ln1_reg_offset_name = 'PORT_TX_DW2_LN1_%s' % port
        port_tx_dw2_ln1_reg = MMIORegister.read("PORT_TX_DW2_REGISTER", port_tx_dw2_ln1_reg_offset_name,
                                                self.platform)
        port_tx_dw2_ln2_reg_offset_name = 'PORT_TX_DW2_LN2_%s' % port
        port_tx_dw2_ln2_reg = MMIORegister.read("PORT_TX_DW2_REGISTER", port_tx_dw2_ln2_reg_offset_name,
                                                self.platform)
        port_tx_dw2_ln3_reg_offset_name = 'PORT_TX_DW2_LN3_%s' % port
        port_tx_dw2_ln3_reg = MMIORegister.read("PORT_TX_DW2_REGISTER", port_tx_dw2_ln3_reg_offset_name,
                                                self.platform)

        ##
        # PORT_TX_DW3
        port_tx_dw3_ln0_reg_offset_name = 'PORT_TX_DW3_LN0_%s' % port
        port_tx_dw3_ln0_reg = MMIORegister.read("PORT_TX_DW3_REGISTER", port_tx_dw3_ln0_reg_offset_name,
                                                self.platform)
        port_tx_dw3_ln1_reg_offset_name = 'PORT_TX_DW3_LN1_%s' % port
        port_tx_dw3_ln1_reg = MMIORegister.read("PORT_TX_DW3_REGISTER", port_tx_dw3_ln1_reg_offset_name,
                                                self.platform)
        port_tx_dw3_ln2_reg_offset_name = 'PORT_TX_DW3_LN2_%s' % port
        port_tx_dw3_ln2_reg = MMIORegister.read("PORT_TX_DW3_REGISTER", port_tx_dw3_ln2_reg_offset_name,
                                                self.platform)
        port_tx_dw3_ln3_reg_offset_name = 'PORT_TX_DW3_LN3_%s' % port
        port_tx_dw3_ln3_reg = MMIORegister.read("PORT_TX_DW3_REGISTER", port_tx_dw3_ln3_reg_offset_name,
                                                self.platform)

        ##
        # PORT_TX_DW4
        port_tx_dw4_ln0_reg_offset_name = 'PORT_TX_DW4_LN0_%s' % port
        port_tx_dw4_ln0_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln0_reg_offset_name,
                                                self.platform)
        port_tx_dw4_ln1_reg_offset_name = 'PORT_TX_DW4_LN1_%s' % port
        port_tx_dw4_ln1_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln1_reg_offset_name,
                                                self.platform)
        port_tx_dw4_ln2_reg_offset_name = 'PORT_TX_DW4_LN2_%s' % port
        port_tx_dw4_ln2_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln2_reg_offset_name,
                                                self.platform)
        port_tx_dw4_ln3_reg_offset_name = 'PORT_TX_DW4_LN3_%s' % port
        port_tx_dw4_ln3_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln3_reg_offset_name,
                                                self.platform)

        ##
        # Verify Scale Enable
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw3_ln0_reg_offset_name, port_tx_dw3_ln0_reg,
                                                                  "oscaledcompmethod",
                                                                  self.scale_enable)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw3_ln1_reg_offset_name, port_tx_dw3_ln1_reg,
                                                                  "oscaledcompmethod",
                                                                  self.scale_enable)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw3_ln2_reg_offset_name, port_tx_dw3_ln2_reg,
                                                                  "oscaledcompmethod",
                                                                  self.scale_enable)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw3_ln3_reg_offset_name, port_tx_dw3_ln3_reg,
                                                                  "oscaledcompmethod",
                                                                  self.scale_enable)

        ##
        # Verify Scale Value
        if self.scale_value != "DoNotCare":
            result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln0_reg_offset_name,
                                                                      port_tx_dw2_ln0_reg, "ouniqtranscale",
                                                                      self.scale_value)
            result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln1_reg_offset_name,
                                                                      port_tx_dw2_ln1_reg, "ouniqtranscale",
                                                                      self.scale_value)
            result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln2_reg_offset_name,
                                                                      port_tx_dw2_ln2_reg, "ouniqtranscale",
                                                                      self.scale_value)
            result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln3_reg_offset_name,
                                                                      port_tx_dw2_ln3_reg, "ouniqtranscale",
                                                                      self.scale_value)

        ##
        # Verify deemphasis decimal
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln0_reg_offset_name, port_tx_dw4_ln0_reg,
                                                                  "ow2tapdeemph9p5",
                                                                  self.deemphasis_decimal)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln1_reg_offset_name, port_tx_dw4_ln1_reg,
                                                                  "ow2tapdeemph9p5",
                                                                  self.deemphasis_decimal)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln2_reg_offset_name, port_tx_dw4_ln2_reg,
                                                                  "ow2tapdeemph9p5",
                                                                  self.deemphasis_decimal)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln3_reg_offset_name, port_tx_dw4_ln3_reg,
                                                                  "ow2tapdeemph9p5",
                                                                  self.deemphasis_decimal_ln3)

        # Verify Swing decimal
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln0_reg_offset_name, port_tx_dw2_ln0_reg,
                                                                  "omargin000",
                                                                  self.swing_decimal)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln1_reg_offset_name, port_tx_dw2_ln1_reg,
                                                                  "omargin000",
                                                                  self.swing_decimal)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln2_reg_offset_name, port_tx_dw2_ln2_reg,
                                                                  "omargin000",
                                                                  self.swing_decimal)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln3_reg_offset_name, port_tx_dw2_ln3_reg,
                                                                  "omargin000",
                                                                  self.swing_decimal)

        return result
