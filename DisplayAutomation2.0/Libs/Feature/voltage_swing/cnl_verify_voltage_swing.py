###############################################################################################################
# \file         cnl_verify_voltage_swing.py
# \addtogroup   PyLibs_Voltage_swing
# \brief        Python class to validate CNL Voltage swing programming
#               CNLVerifyVoltageSwing class exposes an interface verify_voltage_swing which is internal and used by voltage_swing.py
# \author       Girish Y D
###############################################################################################################
import logging

from Libs.Feature.voltage_swing import voltage_swing_helper

from registers.mmioregister import MMIORegister


##
# \brief - Class to verify CNL Voltage swing programming
class CNLVerifyVoltageSwing:
    platform = "cnl"
    non_transition_mv_difp_p = 0
    transition_mV_diff_p_p = 0
    pre_emphasis_dB = 0
    swing_sel_dw2_binary = 0
    n_scalar_dw7_hex = 0
    cursor_coeff_dw4_hex = 0
    post_cursor2_dw4_hex = 0
    post_cursor_1_dw4_hex = 0
    rcomp_scalar_dw2_hex = 0
    rterm_select_dw5_binary = 0
    three_tap_disable_dw5 = 0
    two_tap_disable_dw5 = 0
    cursor_program_dw5 = 0
    coeff_polarity_dw5 = 0

    voltage_reg_map = dict([
        (0b00, 0.85),
        (0b01, 0.95),
        (0b10, 1.05)
    ])

    ##
    # HDMI Voltage Swing Values for VCCIO 0.85V
    # level: [non_transition_mv_difp_p,	transition_mV_diff_p_p,	pre_emphasis_dB, swing_sel_dw2_binary, n_scalar_dw7_hex, cursor_coeff_dw4_hex, post_cursor2_dw4_hex, post_cursor_1_dw4_hex, rcomp_scalar_dw2_hex, rterm_select_dw5_binary, three_tap_disable_dw5, two_tap_disable_dw5, cursor_program_dw5, coeff_polarity_dw5]
    hdmi_voltage_swing_values_0_85V = {
        0: [450, 450, 0, 0b1010, 0x60, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        1: [450, 650, 3.2, 0b1011, 0x73, 0x36, 0x00, 0x09, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        2: [450, 850, 5.5, 0b0110, 0x7F, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        3: [650, 650, 0, 0b1011, 0x73, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        4: [650, 850, 2.3, 0b0110, 0x7F, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        5: [850, 850, 0, 0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        6: [600, 850, 3, 0b0110, 0x7F, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
    }

    ##
    # HDMI Voltage Swing Values for VCCIO 0.95V
    # level: [non_transition_mv_difp_p,	transition_mV_diff_p_p,	pre_emphasis_dB, swing_sel_dw2_binary, n_scalar_dw7_hex, cursor_coeff_dw4_hex, post_cursor2_dw4_hex, post_cursor_1_dw4_hex, rcomp_scalar_dw2_hex, rterm_select_dw5_binary, three_tap_disable_dw5, two_tap_disable_dw5, cursor_program_dw5, coeff_polarity_dw5]
    hdmi_voltage_swing_values_0_95V = {
        0: [450, 450, 0, 0b1010, 0x5E, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        6: [600, 850, 3, 0b1011, 0x79, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        7: [400, 400, 0, 0b1010, 0x5C, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        8: [400, 600, 3.5, 0b1011, 0x69, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        9: [400, 800, 6, 0b0101, 0x76, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        10: [600, 600, 0, 0b1011, 0x69, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        11: [600, 1000, 4.4, 0b0110, 0x7D, 0x32, 0x00, 0x0D, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        12: [800, 800, 0, 0b0101, 0x76, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        13: [800, 1000, 1.9, 0b0110, 0x7D, 0x39, 0x00, 0x06, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        14: [850, 1050, 1.8, 0b0110, 0x7F, 0x39, 0x00, 0x06, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        15: [1050, 1050, 0, 0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
    }

    ##
    # HDMI Voltage Swing Values for VCCIO 1.05V
    # level: [non_transition_mv_difp_p,	transition_mV_diff_p_p,	pre_emphasis_dB, swing_sel_dw2_binary, n_scalar_dw7_hex, cursor_coeff_dw4_hex, post_cursor2_dw4_hex, post_cursor_1_dw4_hex, rcomp_scalar_dw2_hex, rterm_select_dw5_binary, three_tap_disable_dw5, two_tap_disable_dw5, cursor_program_dw5, coeff_polarity_dw5]
    hdmi_voltage_swing_values_1_05V = {
        0: [450, 450, 0, 0b1010, 0x5B, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        6: [600, 850, 3, 0b0101, 0x73, 0x35, 0x00, 0x0A, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        7: [400, 400, 0, 0b1010, 0x58, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        8: [400, 600, 3.5, 0b1011, 0x64, 0x37, 0x00, 0x08, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        9: [400, 800, 6, 0b0101, 0x70, 0x31, 0x00, 0x0E, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        10: [600, 600, 0, 0b1011, 0x64, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        11: [600, 1000, 4.4, 0b0110, 0x7C, 0x32, 0x00, 0x0D, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        12: [800, 800, 0, 0b0101, 0x70, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        13: [800, 1000, 1.9, 0b0110, 0x7C, 0x39, 0x00, 0x06, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        14: [850, 1050, 1.8, 0b0110, 0x7F, 0x39, 0x00, 0x06, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0],
        15: [1050, 1050, 0, 0b0110, 0x7F, 0x3F, 0x00, 0x00, 0x98, 0b110, 0b1, 0b0, 0b0, 0b0]
    }

    ##
    # @brief     - Verifies voltage swing programming for the display_port on CNL
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
        port_or_AE = port
        if port in ['E', 'A']:
            port_or_AE = 'AE'

        if display != 'HDMI':
            logging.error("verify_voltage_swing is not implemented for %s" % display)
            return False

        result, level_shifter_configuration_level = voltage_swing_helper.get_vbt_hdmi_level_shifter_configuration(
            self.platform,
            display_port)
        if result is False or level_shifter_configuration_level is None:
            return False

        ##
        # PORT_COMP_DW3 vccio_voltage check
        port_comp_dw3_reg_offset_name = 'PORT_COMP_DW3'
        port_comp_dw3_reg = MMIORegister.read("PORT_COMP_DW3_REGISTER", port_comp_dw3_reg_offset_name,
                                              self.platform)
        voltage_value = port_comp_dw3_reg.voltage_info
        hdmi_voltage_values_dict = None
        if voltage_value == 0b00:
            hdmi_voltage_values_dict = self.hdmi_voltage_swing_values_0_85V
        elif voltage_value == 0b01:
            hdmi_voltage_values_dict = self.hdmi_voltage_swing_values_0_95V
        elif voltage_value == 0b10:
            hdmi_voltage_values_dict = self.hdmi_voltage_swing_values_1_05V
        else:
            logging.error(
                "PORT_COMP_DW3 vccio info = %s is wrong; Expected : [0b00, 0b01, 0b10]" % voltage_value)
            return False

        if level_shifter_configuration_level not in hdmi_voltage_values_dict.keys():
            min_level_shifter_configuration_level = 0
            if voltage_value == 0b01 or voltage_value == 0b10:
                min_level_shifter_configuration_level = 7
            logging.info(" Level =%s is not supported for VCCIO = %s, "
                         "verifying minimum supported Vswing and Pre-emphasis by Vccio"
                         % (level_shifter_configuration_level, self.voltage_reg_map.get(voltage_value)))
            level_shifter_configuration_level = min_level_shifter_configuration_level

        hdmi_voltage_values = hdmi_voltage_values_dict[level_shifter_configuration_level]
        logging.info("Verifying Voltage swing Level =%s (Voltage Swing: %s x %s Pre-emphashis :%s) "
                     "for VCCIO Voltage= %s"
                     % (level_shifter_configuration_level, hdmi_voltage_values[0], hdmi_voltage_values[1],
                        hdmi_voltage_values[2], self.voltage_reg_map.get(voltage_value)))

        ##
        # Assign the voltage values to be checked.
        self.non_transition_mv_difp_p = hdmi_voltage_values[0]
        self.transition_mV_diff_p_p = hdmi_voltage_values[1]
        self.pre_emphasis_dB = hdmi_voltage_values[2]
        self.swing_sel_dw2_binary = hdmi_voltage_values[3]
        self.n_scalar_dw7_hex = hdmi_voltage_values[4]
        self.cursor_coeff_dw4_hex = hdmi_voltage_values[5]
        self.post_cursor2_dw4_hex = hdmi_voltage_values[6]
        self.post_cursor_1_dw4_hex = hdmi_voltage_values[7]
        self.rcomp_scalar_dw2_hex = hdmi_voltage_values[8]
        self.rterm_select_dw5_binary = hdmi_voltage_values[9]
        self.three_tap_disable_dw5 = hdmi_voltage_values[10]
        self.two_tap_disable_dw5 = hdmi_voltage_values[11]
        self.cursor_program_dw5 = hdmi_voltage_values[12]
        self.coeff_polarity_dw5 = hdmi_voltage_values[13]

        logging.debug("non_transition_mv_difp_p = %s, transition_mV_diff_p_p = %s, pre_emphasis_dB = %s, "
                      "swing_sel_dw2_binary = %s, n_scalar_dw7_hex = %s, cursor_coeff_dw4_hex = %s, "
                      "post_cursor2_dw4_hex = %s, post_cursor_1_dw4_hex = %s, rcomp_scalar_dw2_hex = %s,"
                      "rterm_select_dw5_binary = %s, three_tap_disable_dw5 = %s, two_tap_disable_dw5 = %s,"
                      " cursor_program_dw5 = %s, coeff_polarity_dw5 = %s"
                      % (self.non_transition_mv_difp_p, self.transition_mV_diff_p_p, self.pre_emphasis_dB,
                         self.swing_sel_dw2_binary, self.n_scalar_dw7_hex, self.cursor_coeff_dw4_hex,
                         self.post_cursor2_dw4_hex, self.post_cursor_1_dw4_hex, self.rcomp_scalar_dw2_hex,
                         self.rterm_select_dw5_binary, self.three_tap_disable_dw5, self.two_tap_disable_dw5,
                         self.cursor_program_dw5, self.coeff_polarity_dw5))

        ##
        # Verify registers related to voltage swing values as per BSPEC.
        ##
        # DDI_BUF_CTL
        ddi_buf_ctl_reg_offset_name = 'DDI_BUF_CTL_%s' % port
        ddi_buf_ctl_reg = MMIORegister.read("DDI_BUF_CTL_REGISTER", ddi_buf_ctl_reg_offset_name, self.platform)
        expected_ddi_buffer_enable = 0b1
        result &= voltage_swing_helper.verify_register_bit_fields(ddi_buf_ctl_reg_offset_name, ddi_buf_ctl_reg,
                                                                  "ddi_buffer_enable",
                                                                  expected_ddi_buffer_enable)

        ##
        # PORT_PCS_DW1 common keeper enable check
        # If port type is eDP or DP, set PORT_PCS_DW1 cmnkeeper_enable to 1b, else clear to 0b
        port_pcs_dw1_ln0_reg_offset_name = 'PORT_PCS_DW1_LN0_%s' % port_or_AE
        port_pcs_dw1_reg = MMIORegister.read("PORT_PCS_DW1_REGISTER", port_pcs_dw1_ln0_reg_offset_name, self.platform)
        expected_cmnkeeper_enable = 0b0
        result &= voltage_swing_helper.verify_register_bit_fields(port_pcs_dw1_ln0_reg_offset_name, port_pcs_dw1_reg,
                                                                  "cmnkeeper_enable",
                                                                  expected_cmnkeeper_enable)

        ##
        # PORT_TX_DW4_LN0, LN1, LN2, LN3, loadgen_select check
        port_tx_dw4_ln0_reg_offset_name = 'PORT_TX_DW4_LN0_%s' % port_or_AE
        port_tx_dw4_ln0_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln0_reg_offset_name, self.platform)
        expected_loadgen_select = 0b0
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln0_reg_offset_name, port_tx_dw4_ln0_reg,
                                                                  "loadgen_select",
                                                                  expected_loadgen_select)

        port_tx_dw4_ln1_reg_offset_name = 'PORT_TX_DW4_LN1_%s' % port_or_AE
        port_tx_dw4_ln1_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln1_reg_offset_name, self.platform)
        expected_loadgen_select = 0b1
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln1_reg_offset_name, port_tx_dw4_ln1_reg,
                                                                  "loadgen_select",
                                                                  expected_loadgen_select)

        port_tx_dw4_ln2_reg_offset_name = 'PORT_TX_DW4_LN2_%s' % port_or_AE
        port_tx_dw4_ln2_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln2_reg_offset_name, self.platform)
        expected_loadgen_select = 0b1
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln2_reg_offset_name, port_tx_dw4_ln2_reg,
                                                                  "loadgen_select",
                                                                  expected_loadgen_select)

        port_tx_dw4_ln3_reg_offset_name = 'PORT_TX_DW4_LN3_%s' % port_or_AE
        port_tx_dw4_ln3_reg = MMIORegister.read("PORT_TX_DW4_REGISTER", port_tx_dw4_ln3_reg_offset_name, self.platform)
        expected_loadgen_select = 0b1
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln3_reg_offset_name, port_tx_dw4_ln3_reg,
                                                                  "loadgen_select",
                                                                  expected_loadgen_select)

        ##
        # PORT_CL_DW5 sus_clock_config check
        port_cl_dw5_reg_offset_name = 'PORT_CL_DW5'
        port_cl_dw5_reg = MMIORegister.read("PORT_CL_DW5_REGISTER", port_cl_dw5_reg_offset_name, self.platform)
        expected_sus_clock_config = 0b11
        result &= voltage_swing_helper.verify_register_bit_fields(port_cl_dw5_reg_offset_name, port_cl_dw5_reg,
                                                                  "sus_clock_config",
                                                                  expected_sus_clock_config)

        # PORT_TX_DW2 - Verify rcomp_scalar, swing_sel_lower, swing_sel_upper
        port_tx_dw2_ln0_reg_offset_name = 'PORT_TX_DW2_LN0_%s' % port_or_AE
        port_tx_dw2_ln0_reg = MMIORegister.read("PORT_TX_DW2_REGISTER", port_tx_dw2_ln0_reg_offset_name, self.platform)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln0_reg_offset_name, port_tx_dw2_ln0_reg,
                                                                  "rcomp_scalar",
                                                                  self.rcomp_scalar_dw2_hex)

        expected_port_tx_dw2_ln0_swing_select = self.swing_sel_dw2_binary
        expected_port_tx_dw2_ln0_swing_select_lower = expected_port_tx_dw2_ln0_swing_select & 0b0111
        expected_port_tx_dw2_ln0_swing_select_upper = expected_port_tx_dw2_ln0_swing_select >> 3
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln0_reg_offset_name, port_tx_dw2_ln0_reg,
                                                                  "swing_sel_lower",
                                                                  expected_port_tx_dw2_ln0_swing_select_lower)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw2_ln0_reg_offset_name, port_tx_dw2_ln0_reg,
                                                                  "swing_sel_upper",
                                                                  expected_port_tx_dw2_ln0_swing_select_upper)

        ##
        # PORT_TX_DW7 - Verify n_scalar
        port_tx_dw7_ln0_reg_offset_name = 'PORT_TX_DW7_LN0_%s' % port_or_AE
        port_tx_dw7_ln0_reg = MMIORegister.read("PORT_TX_DW7_REGISTER", port_tx_dw7_ln0_reg_offset_name, self.platform)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw7_ln0_reg_offset_name, port_tx_dw7_ln0_reg,
                                                                  "n_scalar",
                                                                  self.n_scalar_dw7_hex)

        ##
        # PORT_TX_DW4_LN0, LN1, LN2, LN3  - Verify post_cursor1, post_cursor2, cursor_coeff
        # PORT_TX_DW4  - post_cursor1
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln0_reg_offset_name, port_tx_dw4_ln0_reg,
                                                                  "post_cursor1",
                                                                  self.post_cursor_1_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln1_reg_offset_name, port_tx_dw4_ln1_reg,
                                                                  "post_cursor1",
                                                                  self.post_cursor_1_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln2_reg_offset_name, port_tx_dw4_ln2_reg,
                                                                  "post_cursor1",
                                                                  self.post_cursor_1_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln3_reg_offset_name, port_tx_dw4_ln3_reg,
                                                                  "post_cursor1",
                                                                  self.post_cursor_1_dw4_hex)

        ##
        # PORT_TX_DW4  - post_cursor2
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln0_reg_offset_name, port_tx_dw4_ln0_reg,
                                                                  "post_cursor2",
                                                                  self.post_cursor2_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln1_reg_offset_name, port_tx_dw4_ln1_reg,
                                                                  "post_cursor2",
                                                                  self.post_cursor2_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln2_reg_offset_name, port_tx_dw4_ln2_reg,
                                                                  "post_cursor2",
                                                                  self.post_cursor2_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln3_reg_offset_name, port_tx_dw4_ln3_reg,
                                                                  "post_cursor2",
                                                                  self.post_cursor2_dw4_hex)

        ##
        # PORT_TX_DW4  - cursor_coeff
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln0_reg_offset_name, port_tx_dw4_ln0_reg,
                                                                  "cursor_coeff",
                                                                  self.cursor_coeff_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln1_reg_offset_name, port_tx_dw4_ln1_reg,
                                                                  "cursor_coeff",
                                                                  self.cursor_coeff_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln2_reg_offset_name, port_tx_dw4_ln2_reg,
                                                                  "cursor_coeff",
                                                                  self.cursor_coeff_dw4_hex)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw4_ln3_reg_offset_name, port_tx_dw4_ln3_reg,
                                                                  "cursor_coeff",
                                                                  self.cursor_coeff_dw4_hex)

        ##
        # PORT_TX_DW5 - Verify  rterm_select, disable_3tap, disable_2tap, cursor_program, coeff_polarity
        port_tx_dw5_ln0_reg_offset_name = 'PORT_TX_DW5_LN0_%s' % port_or_AE
        port_tx_dw5_ln0_reg = MMIORegister.read("PORT_TX_DW5_REGISTER", port_tx_dw5_ln0_reg_offset_name, self.platform)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw5_ln0_reg_offset_name, port_tx_dw5_ln0_reg,
                                                                  "rterm_select",
                                                                  self.rterm_select_dw5_binary)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw5_ln0_reg_offset_name, port_tx_dw5_ln0_reg,
                                                                  "disable_3tap",
                                                                  self.three_tap_disable_dw5)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw5_ln0_reg_offset_name, port_tx_dw5_ln0_reg,
                                                                  "disable_2tap",
                                                                  self.two_tap_disable_dw5)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw5_ln0_reg_offset_name, port_tx_dw5_ln0_reg,
                                                                  "cursor_program",
                                                                  self.cursor_program_dw5)
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw5_ln0_reg_offset_name, port_tx_dw5_ln0_reg,
                                                                  "coeff_polarity",
                                                                  self.coeff_polarity_dw5)

        ##
        # PORT_TX_DW5 - Verify  scaling_mode_sel, tx_training_enable
        expected_port_tx_dw5_ln0_scaling_mode_sel = 0b010
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw5_ln0_reg_offset_name, port_tx_dw5_ln0_reg,
                                                                  "scaling_mode_sel",
                                                                  expected_port_tx_dw5_ln0_scaling_mode_sel)

        expected_port_tx_dw5_ln0_tx_training_enable = 0b1
        result &= voltage_swing_helper.verify_register_bit_fields(port_tx_dw5_ln0_reg_offset_name, port_tx_dw5_ln0_reg,
                                                                  "tx_training_enable",
                                                                  expected_port_tx_dw5_ln0_tx_training_enable)
        return result
