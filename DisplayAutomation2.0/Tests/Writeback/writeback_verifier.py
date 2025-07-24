########################################################################################################################
# @file         writeback_verifier.py
# @brief        The script contains following helper functions to verify writeback devices.
#               * Checks whether the writeback devices are plugged or not
#               * Verify WD transcoder, WD function and WD input select are enabled or not
#               * Get current powerwell status, to dump Wd registers value and to log WD register
#               * Verify frame number programming, display value improvement,caching
#               * Verify wb enable sequence and wb disable sequence
# @author       Patel, Ankurkumar G
########################################################################################################################
import importlib
import logging
import time
from collections import defaultdict

from Libs.Core import display_utility
from Libs.Core.core_base import singleton
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from registers.mmioregister import MMIORegister

PLATFORM_NAME = SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
DSB_WORKAROUND = ['ICLLP', 'LKF1', 'LKFR', 'JSL', 'EHL', 'TGL']


@singleton
##
# @brief     Contains helper functions for writeback tests
class WritebackVerifier(object):
    platform = None
    disp_config = DisplayConfiguration()
    reg_read = MMIORegister()
    machine_info = SystemInfo()

    # list of platforms for which display-vdenc enhancement is enabled
    display_vdenc_improvement_platform_list = ['tgllp', 'tgl', 'adls', 'adlp']

    # list of platforms for powerwell 5 supported
    powerwell_5_supported_platform_list = ['tgllp', 'tgl', 'lkf1', 'dg1', 'adls']

    # list of platforms for new powerwell register definition
    pwr_well_dfn_change_post_gen12_platform_list = ['dg2', 'adlp', 'mtl', 'dg3', 'jps', 'elg', 'lnl']

    # list to store frame numbers derived from WD_TRANS_FUNC_CTL register programming
    frame_number_list = []

    # Number of times dump frame number - frame_number_list.Count
    frame_number_count = 5

    # Dictionary definition for valid values of Trans_wd_func_ctl & Trans_Conf registers - used in dump_wd_registers
    dict_bool = defaultdict(lambda: "Invalid Value", {'0b1': "Enable", '0b0': "Disable"})
    dict_wd_color_mode = defaultdict(lambda: "Invalid Value",
                                     {'0b11': "RGB10", '0b101': "YUY2", '0b1': "Y410", '0b011': "RGBX",
                                      '0b01': "XYUV_444", '0b001': "YUV_422", '0b0': "YUV_444"})
    dict_control_pointers = defaultdict(lambda: "Invalid Value",
                                        {'0b0': "control_pointers_00", '0b01': "control_pointers_01",
                                         '0b11': "control_pointers_11"})
    dict_vdenc_session_select = defaultdict(lambda: "Invalid Value",
                                            {'0b0': "vdenc_session_select_00", '0b01': "vdenc_session_select_01",
                                             '0b1': "vdenc_session_select_10", '0b11': "vdenc_session_select_11"})
    dict_wd_input_select = defaultdict(lambda: "Invalid Value",
                                       {'0b0': "Pipe A", '0b101': "Pipe B", '0b110': "Pipe C", '0b111': "Pipe D"})
    dict_interlaced_mode = defaultdict(lambda: "Invalid Value", {'0b0': "Progressive Fetch with Progressive Display",
                                                                 '0b01': "Progressive Fetch with Interlaced Display",
                                                                 '0b11': "Interlaced Fetch with Interlaced Display"})
    dict_dp_audio_symbol_watermark = defaultdict(lambda: "Invalid Value",
                                                 {'0x24L': "dp_audio_symbol_watermark_36_ENTRIES"})

    ##
    # @brief        Verify writeback device is enumerated or not
    # @return       dictionary that contains all the writeback devices
    def get_wb_devices(self):
        logging.debug("writeback_verifier: get_wb_devices() Entry:")
        # Need to wait to get writeback device enumerated in enumerated display list

        wb_device_dict = dict()
        enumerated_display = self.disp_config.get_enumerated_display_info()
        logging.debug("Enumarated Display %s" % enumerated_display.to_string())
        for display_index in range(enumerated_display.Count):
            logging.debug("connectorport type = %s\n" % str(
                CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_index].ConnectorNPortType)))
            if "WD_" in str(
                    CONNECTOR_PORT_TYPE(
                        enumerated_display.ConnectedDisplays[display_index].ConnectorNPortType)):
                wb_device_dict.update({str(CONNECTOR_PORT_TYPE(
                    enumerated_display.ConnectedDisplays[display_index].ConnectorNPortType)): ' Active' if
                enumerated_display.ConnectedDisplays[display_index].IsActive is True else ' Inactive'})
        logging.debug("writeback_verifier: get_wb_devices() Exit:")
        return wb_device_dict

    ##
    # @brief         Verify writeback device is enumerated or not
    # @param[in]     wb_device_count; number of devices
    # @return        boolean value true if wb_device count and number_of_writeback_devices are same
    def is_wb_device_plugged(self, wb_device_count):
        logging.debug("writeback_verifier: is_wb_device_plugged() Entry:")

        number_of_writeback_devices = 0
        for key, value in self.get_wb_devices().items():
            logging.info("key is : %s" % key)
            number_of_writeback_devices += 1
        if not str(number_of_writeback_devices) == str(wb_device_count):
            logging.info("wb_device_count is = %s" % wb_device_count)
            logging.info("number_of_writeback_devices = %s" % number_of_writeback_devices)
            return False
        logging.debug("writeback_verifier: is_wb_device_plugged() Exit:")
        return True

    ##
    # @brief        Verify WD Function is enabled or not
    # @param[in]    transcoder_number; either 0 or 1
    # @return       Boolean value true if wd function is enabled else false
    def verify_wd_function_enable(self, transcoder_number):
        logging.debug("writeback_verifier: verify_wd_function_enable() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % self.platform)

        wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(transcoder_number)
        wd_trans_ctl_reg_value = self.reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg, self.platform, 0x0)

        if (wd_trans_ctl_reg_value.__getattribute__("wd_function_enable") == getattr(wd_trans_ctl_file,
                                                                                     "wd_function_enable_ENABLE")):
            logging.info("wd function is enabled for WD_%s" % transcoder_number)
            logging.debug("writeback_verifier: verify_wd_function_enable() Exit:")
            return True
        else:
            logging.info("wd function is not enabled for WD_%s" % transcoder_number)
            return False

    ##
    # @brief         Verify WD transcoder is enabled or not
    # @param[in]     transcoder_number; either 0 or 1
    # @return        Boolean value true if wd transcoder is enabled else false
    def is_wd_transcoder_enabled(self, transcoder_number):
        logging.debug("writeback_verifier: is_wd_transcoder_enabled() Entry:")
        trans_conf_file = importlib.import_module("registers.skl.TRANS_CONF_REGISTER")

        trans_conf_reg = "TRANS_CONF_WD" + str(transcoder_number)
        trans_conf_reg_value = self.reg_read.read('TRANS_CONF_REGISTER', trans_conf_reg, 'skl', 0x0)

        if (trans_conf_reg_value.__getattribute__("transcoder_state") == getattr(trans_conf_file,
                                                                                 "transcoder_state_ENABLED")):
            logging.info("wd transcoder is enabled for WD_%s" % transcoder_number)
            logging.debug("writeback_verifier: is_wd_transcoder_enabled() Exit:")
            return True
        else:
            logging.info("wd transcoder is not enabled for WD_%s" % transcoder_number)
            return False

    ##
    # @brief         Verify WD input select
    # @param[in]     transcoder_number; either 0 or 1
    # @return        Boolean value true or false
    def verify_wd_input_select(self, transcoder_number):
        logging.debug("writeback_verifier: verify_wd_input_select() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % self.platform)

        wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(transcoder_number)
        wd_trans_ctl_reg_value = self.reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg, self.platform, 0x0)

        logging.debug("wd input select is programmed with : %s" % self.dict_wd_input_select[
            bin(wd_trans_ctl_reg_value.__getattribute__("wd_input_select"))])
        if self.dict_wd_input_select[
            bin(wd_trans_ctl_reg_value.__getattribute__("wd_input_select"))] != "Invalid Value" and \
                self.dict_wd_input_select[bin(wd_trans_ctl_reg_value.__getattribute__("wd_input_select"))] != "Pipe A":
            logging.debug("writeback_verifier: verify_wd_input_select() Exit:")
            return True
        return False

    ##
    # @brief         Check for dual lfp displays
    # @param[in]     displays;
    # @return        displays; total number of displays
    def verify_dual_lfp(self, displays):
        logging.debug("writeback_verifier: verify_dual_lfp() Entry:")
        enumerated_display = self.disp_config.get_enumerated_display_info()
        active_displays = []

        for display_index in range(enumerated_display.Count):
            if enumerated_display.ConnectedDisplays[display_index].IsActive is True:
                active_displays.append(str(
                    CONNECTOR_PORT_TYPE(
                        enumerated_display.ConnectedDisplays[display_index].ConnectorNPortType)))

        edp_panels = [panel for panel in active_displays if display_utility.get_vbt_panel_type(panel, 'gfx_0') ==
                      display_utility.VbtPanelType.LFP_DP]
        mipi_panels = [panel for panel in active_displays if display_utility.get_vbt_panel_type(panel, 'gfx_0') ==
                       display_utility.VbtPanelType.LFP_MIPI]

        if (len(edp_panels) > 1) or (len(mipi_panels) > 1):
            displays += 1
        logging.debug("writeback_verifier: verify_dual_lfp() Exit:")
        return displays

    ##
    # @brief        Verify powerwell till gen12
    # @return       boolean value true or false
    def verify_wd_powerwells_till_gen12(self):
        logging.debug("writeback_verifier: verify_wd_powerwells_till_gen12() Entry:")
        actual_pg_status_dict = self.get_current_powerwell_status_till_gen12()
        number_of_active_displays = self.number_of_external_displays_present_and_active()
        expected_pg_status_for_1_pipe_active_dict = {'PG1': 'ON', 'PG3': 'OFF', 'PG4': 'OFF', 'PG5': 'OFF'}
        expected_pg_status_for_2_pipe_active_dict = {'PG1': 'ON', 'PG3': 'ON', 'PG4': 'OFF', 'PG5': 'OFF'}
        expected_pg_status_for_3_pipe_active_dict = {'PG1': 'ON', 'PG3': 'ON', 'PG4': 'ON', 'PG5': 'OFF'}
        expected_pg_status_for_4_pipe_active_dict = {'PG1': 'ON', 'PG3': 'ON', 'PG4': 'ON', 'PG5': 'ON'}

        # Get number of active displays
        number_of_active_displays = self.verify_dual_lfp(number_of_active_displays)

        if number_of_active_displays == 0:
            if actual_pg_status_dict == expected_pg_status_for_1_pipe_active_dict:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_1_pipe_active_dict)
                logging.debug("writeback_verifier: verify_wd_powerwells_till_gen12() Exit:")
                return True
            else:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_1_pipe_active_dict)
                return False

        if number_of_active_displays == 1:
            if actual_pg_status_dict == expected_pg_status_for_2_pipe_active_dict:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_2_pipe_active_dict)
                logging.debug("writeback_verifier: verify_wd_powerwells_till_gen12() Exit:")
                return True
            else:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_2_pipe_active_dict)
                return False

        if number_of_active_displays == 2:
            if actual_pg_status_dict == expected_pg_status_for_3_pipe_active_dict:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_3_pipe_active_dict)
                logging.debug("writeback_verifier: verify_wd_powerwells_till_gen12() Exit:")
                return True
            else:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_3_pipe_active_dict)
                return False

        if number_of_active_displays == 3:
            if actual_pg_status_dict == expected_pg_status_for_4_pipe_active_dict:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_4_pipe_active_dict)
                logging.debug("writeback_verifier: verify_wd_powerwells_till_gen12() Exit:")
                return True
            else:
                self.log_pg_status(actual_pg_status_dict, expected_pg_status_for_4_pipe_active_dict)
                return False

    ##
    # @brief        Verify powerwells post gen12
    # @return       boolean value true or false
    def verify_wd_powerwells_post_gen12(self):
        logging.debug("writeback_verifier: verify_wd_powerwells_post_gen12() Entry:")
        actual_pg_status_dict = self.get_current_powerwell_status_post_gen12()
        number_of_active_displays = self.number_of_external_displays_present_and_active()
        expected_pg_status_for_1_pipe_active_dict = {'PGA': 'ON'}
        expected_pg_status_for_2_pipe_active_dict = {'PGA': 'ON', 'PGB': 'ON'}
        expected_pg_status_for_3_pipe_active_dict = {'PGA': 'ON', 'PGB': 'ON', 'PGC': 'ON'}
        expected_pg_status_for_4_pipe_active_dict = {'PGA': 'ON', 'PGB': 'ON', 'PGC': 'ON', 'PGD': 'ON'}

        # Get number of active displays
        number_of_active_displays = self.verify_dual_lfp(number_of_active_displays)
        logging.debug("writeback_verifier: number_of_active_displays {} ".format(number_of_active_displays))

        if number_of_active_displays == 0:
            if len(actual_pg_status_dict.keys()) == len(expected_pg_status_for_1_pipe_active_dict.keys()):
                logging.debug("writeback_verifier: verify_wd_powerwells_post_gen12() Exit:")
                return True
            else:
                return False

        if number_of_active_displays == 1:
            if len(actual_pg_status_dict.keys()) == len(expected_pg_status_for_2_pipe_active_dict.keys()):
                logging.debug("writeback_verifier: verify_wd_powerwells_post_gen12() Exit:")
                return True
            else:
                return False

        if number_of_active_displays == 2:
            if len(actual_pg_status_dict.keys()) == len(expected_pg_status_for_3_pipe_active_dict.keys()):
                logging.debug("writeback_verifier: verify_wd_powerwells_post_gen12() Exit:")
                return True
            else:
                return False

        if number_of_active_displays == 3:
            if len(actual_pg_status_dict.keys()) == len(expected_pg_status_for_4_pipe_active_dict.keys()):
                logging.debug("writeback_verifier: verify_wd_powerwells_post_gen12() Exit:")
                return True
            else:
                return False

    ##
    # @brief        Verify powerwells post gen12
    # @param[in]    self;
    # @param[in]    actual_pg_status_dict - dictionary which contains actual status of powerwell
    # @param[in]    expected_pg_status_dict - dictionary which contains expected status of powerwell
    # @return       None
    def log_pg_status(self, actual_pg_status_dict, expected_pg_status_dict):
        logging.debug("writeback_verifier: log_pg_status() Entry:")
        for key, value in actual_pg_status_dict.items():
            logging.info("Actual %s status %s ; Expected %s status %s" % (
                str(key), str(value), str(key), expected_pg_status_dict[str(key)]))
        logging.debug("writeback_verifier: log_pg_status() Exit:")

    ##
    # @brief        Check for number of external display/writeback devices present
    # @param[in]    self
    # @return       number_of_external_displays_present_and_active - number of external displays present and active
    def number_of_external_displays_present_and_active(self):
        logging.debug("writeback_verifier: number_of_external_displays_present_and_active() Entry:")
        number_of_external_displays_present_and_active = 0
        internal_displays = ['DP_A', 'MIPI_A', 'MIPI_C']
        enumerated_display = self.disp_config.get_enumerated_display_info()
        for display_index in range(enumerated_display.Count):
            logging.debug("connectorport type = %s\n" % str(
                CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_index].ConnectorNPortType)))
            if str(CONNECTOR_PORT_TYPE(
                    enumerated_display.ConnectedDisplays[display_index].ConnectorNPortType)) not in internal_displays:
                if enumerated_display.ConnectedDisplays[display_index].IsActive is True:
                    number_of_external_displays_present_and_active += 1
        logging.debug("writeback_verifier: number_of_external_displays_present_and_active() Exit:")
        return number_of_external_displays_present_and_active

    ##
    # @brief         Get current powerwell status : applicable till gen12
    # @param[in]     self
    # @return        powerwell_actual_status_dict - dictionary that contains actual status of the powerwell
    def get_current_powerwell_status_till_gen12(self):
        logging.debug("writeback_verifier: get_current_powerwell_status_till_gen12() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        pwr_well_ctl_file = importlib.import_module("registers.%s.PWR_WELL_CTL_REGISTER" % self.platform)

        pwr_well_ctl_reg = "PWR_WELL_CTL2"
        pwr_well_ctl_reg_value = self.reg_read.read('PWR_WELL_CTL_REGISTER', pwr_well_ctl_reg, self.platform, 0x0)

        powerwell_actual_status_dict = dict()
        # Powerwell 1
        if (pwr_well_ctl_reg_value.__getattribute__("power_well_1_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_1_state_ENABLED")):
            logging.debug("power well 1 is enabled")
            powerwell_actual_status_dict.update({'PG1': 'ON'})
        else:
            logging.debug("power well 1 is disabled")
            powerwell_actual_status_dict.update({'PG1': 'OFF'})

        # Powerwell 3
        if (pwr_well_ctl_reg_value.__getattribute__("power_well_3_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_3_state_ENABLED")):
            logging.debug("power well 3 is enabled")
            powerwell_actual_status_dict.update({'PG3': 'ON'})
        else:
            logging.debug("power well 3 is disabled")
            powerwell_actual_status_dict.update({'PG3': 'OFF'})

        # Powerwell 4
        if (pwr_well_ctl_reg_value.__getattribute__("power_well_4_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_4_state_ENABLED")):
            logging.debug("power well 4 is enabled")
            powerwell_actual_status_dict.update({'PG4': 'ON'})
        else:
            logging.debug("power well 4 is disabled")
            powerwell_actual_status_dict.update({'PG4': 'OFF'})

        # Powerwell 5
        if self.platform not in self.powerwell_5_supported_platform_list:
            logging.debug("power well 5 not supported on %s platform, keeping status as OFF " % self.platform)
            powerwell_actual_status_dict.update({'PG5': 'OFF'})
            return powerwell_actual_status_dict

        if (pwr_well_ctl_reg_value.__getattribute__("power_well_5_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_5_state_ENABLED")):
            logging.debug("power well 5 is enabled")
            powerwell_actual_status_dict.update({'PG5': 'ON'})
        else:
            logging.debug("power well 5 is disabled")
            powerwell_actual_status_dict.update({'PG5': 'OFF'})

        logging.debug("writeback_verifier: get_current_powerwell_status_till_gen12() Exit:")
        return powerwell_actual_status_dict

    ##
    # @brief         Get current powerwell status : applicable post gen12
    # @param[in]     self;
    # @return        powerwell_actual_status_dict - dictionary that contains actual status of the powerwell
    def get_current_powerwell_status_post_gen12(self):
        logging.debug("writeback_verifier: get_current_powerwell_status_post_gen12() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        pwr_well_ctl_file = importlib.import_module("registers.%s.PWR_WELL_CTL_REGISTER" % self.platform)

        pwr_well_ctl_reg = "PWR_WELL_CTL2"
        pwr_well_ctl_reg_value = self.reg_read.read('PWR_WELL_CTL_REGISTER', pwr_well_ctl_reg, self.platform, 0x0)

        powerwell_actual_status_dict = dict()
        # Powerwell A
        if (pwr_well_ctl_reg_value.__getattribute__("power_well_a_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_a_state_ENABLED")):
            logging.debug("power well A is enabled")
            powerwell_actual_status_dict.update({'PGA': 'ON'})
        else:
            logging.debug("power well A is disabled")

        # Powerwell B
        if (pwr_well_ctl_reg_value.__getattribute__("power_well_b_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_b_state_ENABLED")):
            logging.debug("power well B is enabled")
            powerwell_actual_status_dict.update({'PGB': 'ON'})
        else:
            logging.debug("power well B is disabled")

        # Powerwell C
        if (pwr_well_ctl_reg_value.__getattribute__("power_well_c_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_c_state_ENABLED")):
            logging.debug("power well C is enabled")
            powerwell_actual_status_dict.update({'PGC': 'ON'})
        else:
            logging.debug("power well C is disabled")

        # Powerwell D
        if (pwr_well_ctl_reg_value.__getattribute__("power_well_d_state") == getattr(pwr_well_ctl_file,
                                                                                     "power_well_d_state_ENABLED")):
            logging.debug("power well D is enabled")
            powerwell_actual_status_dict.update({'PGD': 'ON'})
        else:
            logging.debug("power well D is disabled")

        logging.debug("writeback_verifier: get_current_powerwell_status_post_gen12() Exit:")
        return powerwell_actual_status_dict

    ##
    # @brief         Dump wd registers; it tells the value of each bitfield programmed by driver
    # @param[in]     transcoder_number; either 0 or 1
    # @return        boolean value true
    def dump_wd_registers(self, transcoder_number):
        logging.debug("writeback_verifier: dump_wd_registers() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % (self.platform))
        trans_conf_file = importlib.import_module("registers.skl.TRANS_CONF_REGISTER")

        wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(transcoder_number)
        wd_trans_ctl_reg_value = self.reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg, self.platform, 0x0)
        trans_conf_reg = "TRANS_CONF_WD" + str(transcoder_number)
        trans_conf_reg_value = self.reg_read.read('TRANS_CONF_REGISTER', trans_conf_reg, 'skl', 0x0)

        # Trans_wd_func_ctl
        logging.debug("*****************************************************************************")
        logging.debug("Dump of Register TRANS_WD_FUNC_CTL_%s " % transcoder_number)
        logging.debug("*****************************************************************************")
        logging.debug("wd_function_enable : \t\t\t%s " % self.dict_bool[
            bin(wd_trans_ctl_reg_value.__getattribute__("wd_function_enable"))] + "[ Value : %s, BIT31 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("wd_function_enable")))
        logging.debug("triggered_capture_mode_enable : \t\t%s " % self.dict_bool[bin(
            wd_trans_ctl_reg_value.__getattribute__("triggered_capture_mode_enable"))] + "[ Value : %s, BIT30 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("triggered_capture_mode_enable")))
        logging.debug("start_trigger_frame : \t\t\t%s " % self.dict_bool[
            bin(wd_trans_ctl_reg_value.__getattribute__("start_trigger_frame"))] + "[ Value : %s, BIT29 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("start_trigger_frame")))
        logging.debug("stop_trigger_frame : \t\t\t%s " % self.dict_bool[
            bin(wd_trans_ctl_reg_value.__getattribute__("stop_trigger_frame"))] + "[ Value : %s, BIT28 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("stop_trigger_frame")))
        logging.debug("enable_write_caching : \t\t\t%s " % self.dict_bool[
            bin(wd_trans_ctl_reg_value.__getattribute__("enable_write_caching"))] + "[ Value : %s, BIT27 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("enable_write_caching")))
        logging.debug("chroma_filtering_enable : \t\t\t%s " % self.dict_bool[
            bin(wd_trans_ctl_reg_value.__getattribute__("chroma_filtering_enable"))] + "[ Value : %s, BIT26 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("chroma_filtering_enable")))
        logging.debug("reserved_23 : \t\t\t\tReserved " + "[ Value : %s, BIT23-BIT25 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("reserved_23")))
        logging.debug("wd_color_mode : \t\t\t\t%s " % self.dict_wd_color_mode[
            bin(wd_trans_ctl_reg_value.__getattribute__("wd_color_mode"))] + "[ Value : %s, BIT20-BIT22 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("wd_color_mode")))
        logging.debug("control_pointers : \t\t\t\t%s " % self.dict_control_pointers[
            bin(wd_trans_ctl_reg_value.__getattribute__("control_pointers"))] + "[ Value : %s, BIT18-BIT19 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("control_pointers")))
        logging.debug("vdenc_session_select : \t\t\t%s " % self.dict_vdenc_session_select[
            bin(wd_trans_ctl_reg_value.__getattribute__("vdenc_session_select"))] + "[ Value : %s, BIT16-BIT17 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("vdenc_session_select")))
        logging.debug("reserved_15 : \t\t\t\tReserved " + "[ Value : %s, BIT15 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("reserved_15")))
        logging.debug("wd_input_select : \t\t\t\t%s " % self.dict_wd_input_select[
            bin(wd_trans_ctl_reg_value.__getattribute__("wd_input_select"))] + "[ Value : %s, BIT12-BIT14 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("wd_input_select")))
        if bin(wd_trans_ctl_reg_value.__getattribute__("maximum_defference_to_enable_write_caching")) == '0b0':
            logging.debug(
                "maximum_defference_to_enable_write_caching : All writes are cached " + "[ Value : 0b0, BIT4-BIT11 ]")
        else:
            logging.debug("maximum_defference_to_enable_write_caching : %s scanlines" % (16 * (int(
                wd_trans_ctl_reg_value.__getattribute__(
                    "maximum_defference_to_enable_write_caching")))) + "[ Value : %s (in units of 16 scanlines), BIT4-BIT11 ]" % (
                                  16 * (int(wd_trans_ctl_reg_value.__getattribute__(
                              "maximum_defference_to_enable_write_caching")))))
        logging.debug("frame_number : \t\t\t\t%s " % (
            wd_trans_ctl_reg_value.__getattribute__("frame_number")) + "[ Value : %s, BIT0-BIT3 ]" % bin(
            wd_trans_ctl_reg_value.__getattribute__("frame_number")))
        logging.debug("*****************************************************************************")

        # Trans_Conf
        logging.debug("*****************************************************************************")
        logging.debug("Dump of Register TRANS_CONF_WD%s " % transcoder_number)
        logging.debug("*****************************************************************************")
        logging.debug("transcoder_enable : \t\t%s " % self.dict_bool[
            bin(trans_conf_reg_value.__getattribute__("transcoder_enable"))] + "[ Value : %s, BIT31 ]" % bin(
            trans_conf_reg_value.__getattribute__("transcoder_enable")))
        logging.debug("transcoder_state : \t\t%s " % self.dict_bool[
            bin(trans_conf_reg_value.__getattribute__("transcoder_state"))] + "[ Value : %s, BIT30 ]" % bin(
            trans_conf_reg_value.__getattribute__("transcoder_state")))
        logging.debug("reserved_23 : \t\tReserved " + "[ Value : %s, BIT23-BIT29 ]" % bin(
            trans_conf_reg_value.__getattribute__("reserved_23")))
        logging.debug("interlaced_mode : \t\t%s " % self.dict_interlaced_mode[
            bin(trans_conf_reg_value.__getattribute__("interlaced_mode"))] + "[ Value : %s, BIT21-BIT22 ]" % bin(
            trans_conf_reg_value.__getattribute__("interlaced_mode")))
        logging.debug("reserved_7 : \t\tReserved " + "[ Value : %s, BIT7-BIT23 ]" % bin(
            trans_conf_reg_value.__getattribute__("reserved_7")))
        logging.debug("dp_audio_symbol_watermark : \t%s " % self.dict_dp_audio_symbol_watermark[hex(
            trans_conf_reg_value.__getattribute__("dp_audio_symbol_watermark"))] + "[ Value : %s, BIT0-BIT6 ]" % hex(
            trans_conf_reg_value.__getattribute__("dp_audio_symbol_watermark")))
        logging.debug("*****************************************************************************")

        logging.debug("writeback_verifier: dump_wd_registers() Exit:")
        return True

    ##
    # @brief        Log wd register
    # @param[in]    wb_device_list; list of writeback devices
    # @return       void
    def log_wd_register_proggramming(self, wb_device_list):
        logging.debug("writeback_verifier: log_wd_register_proggramming() Entry:")
        logging.debug("Number of writeback devices are %s" % len(wb_device_list))
        if len(wb_device_list) == 1:
            self.dump_wd_registers(0)
        if len(wb_device_list) == 2:
            self.dump_wd_registers(0)
            self.dump_wd_registers(1)
        logging.debug("writeback_verifier: log_wd_register_proggramming() Exit:")

    ##
    # @brief        Verify wb enable sequence
    # @param[in]    wb_device_list; list of writeback devices
    # @return       boolean value true or false
    def verify_wb_enable_sequence(self, wb_device_list):
        logging.debug("writeback_verifier: verify_wb_enable_sequence() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        # Verify writeback devices are plugged
        logging.info("Step - Verify Writeback devices are enumerated")
        if not self.is_wb_device_plugged(len(wb_device_list)):
            logging.info("\tFAIL: Writeback devices are not enumerated")
            gdhm.report_bug(title="[Writeback] Writeback devices are not enumerated",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2)
            return False
        logging.info("\tPASS: Writeback devices are enumerated successfully")

        # Verify transcoder is enabled
        logging.info("Step - Verify writeback transcoder is enabled")
        for wb_device_index in range(0, len(wb_device_list)):
            if not self.is_wd_transcoder_enabled(wb_device_index):
                logging.info("\tFAIL: Writeback transcoder WD_%s is not enabled" % wb_device_index)
                gdhm.report_bug(
                    title="[Writeback] Writeback transcoder WD_{0} is not enabled".format(wb_device_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: Writeback transcoder WD_%s is enabled" % wb_device_index)
        logging.info("\tPASS: Writeback transcoder enabled")

        # Verify wd_function_enable
        logging.info("Step - Verify wd_function_enable")
        for wb_device_index in range(0, len(wb_device_list)):
            if not self.verify_wd_function_enable(wb_device_index):
                logging.info(
                    "\tFAIL: wd_function_enable is not enabled for Writeback transcoder WD_%s" % wb_device_index)
                gdhm.report_bug(
                    title="[Writeback] WD_Function_Enable is not enabled for Writeback transcoder WD_{0}".format(
                        wb_device_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: wd_function_enable is enabled for Writeback transcoder WD_%s" % wb_device_index)
        logging.info("\tPASS: wd_function_enable is enabled")

        # Verify wd input select
        logging.info("Step - Verify wd_input_select")
        for wb_device_index in range(0, len(wb_device_list)):
            if not self.verify_wd_input_select(wb_device_index):
                logging.info(
                    "\tFAIL: wd_input_select is not properly programmed for Writeback transcoder WD_%s" % wb_device_index)
                gdhm.report_bug(
                    title="[Writeback] wd_input_select is not properly programmed for Writeback transcoder WD_{0}".format(
                        wb_device_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info(
                "\tPASS: wd_input_select is properly programmed for Writeback transcoder WD_%s" % wb_device_index)
        logging.info("\tPASS: wd input select is properly programmed")

        # Verify powerwells for writeback devices
        logging.info("Step - Verify powerwells ")
        if self.platform not in self.pwr_well_dfn_change_post_gen12_platform_list:
            if not self.verify_wd_powerwells_till_gen12():
                logging.info("Required powerwells for writeback device are not enabled")
                gdhm.report_bug(
                    title="[Writeback] Powerwells are not enabled for Writeback device",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: Required powerwells for writeback device are enabled sucessfully")
        else:
            if not self.verify_wd_powerwells_post_gen12():
                logging.info("Required powerwells for writeback device are not enabled")
                gdhm.report_bug(
                    title="[Writeback] Powerwells are not enabled for Writeback device",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: Required powerwells for writeback device are enabled sucessfully")
        logging.debug("writeback_verifier: verify_wb_enable_sequence() Exit:")
        return True

    ##
    # @brief        Verify wb disable sequence
    # @param[in]    wb_device_list; list of writeback devices
    # @return       boolean value true or false
    def verify_wb_disable_sequence(self, wb_device_list):
        logging.debug("writeback_verifier: verify_wb_disable_sequence() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        # Verify writeback devices are not plugged
        logging.info("Step - Verify Writeback devices")
        if self.is_wb_device_plugged(len(wb_device_list)):
            logging.info("\tFAIL: Writeback devices are enumerated.")
            gdhm.report_bug(title="[Writeback] Writeback devices are enumerated post disabling",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2)
            return False
        logging.info("\tPASS: Writeback devices are not enumerated")

        # Verify transcoder is disabled
        logging.info("Step - Verify writeback transcoder is disabled")
        for wb_device_index in range(0, len(wb_device_list)):
            if self.is_wd_transcoder_enabled(wb_device_index):
                logging.info("\tFAIL: Writeback transcoder WD_%s is not disabled" % wb_device_index)
                gdhm.report_bug(
                    title="[Writeback] Writeback transcoder WD_{0} is not disbaled".format(wb_device_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: Writeback transcoder WD_%s is disabled" % wb_device_index)
        logging.info("\tPASS: Writeback transcoder disabled")

        # Verify wd_function_enable
        logging.info("Step - Verify wd_function_enable ")
        for wb_device_index in range(0, len(wb_device_list)):
            if self.verify_wd_function_enable(wb_device_index):
                logging.info(
                    "\tFAIL: wd_function_enable is not disabled for Writeback transcoder WD_%s" % wb_device_index)
                gdhm.report_bug(
                    title="[Writeback] WD_Function_Enable is not disabled for Writeback transcoder WD_{0}".format(
                        wb_device_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: wd_function_enable is disabled for Writeback transcoder WD_%s" % wb_device_index)
        logging.info("\tPASS: wd_function_enable is disabled")

        # Verify powerwells for writeback devices
        logging.info("Step - Verify powerwells ")
        if self.platform not in self.pwr_well_dfn_change_post_gen12_platform_list:
            if not self.verify_wd_powerwells_till_gen12():
                logging.info("Powerwells are not disabled successfully")
                gdhm.report_bug(
                    title="[Writeback] Powerwells are not disabled for Writeback device",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: Powerwells are disabled successfully")
        else:
            if not self.verify_wd_powerwells_post_gen12():
                logging.info("Powerwells are not disabled successfully")
                gdhm.report_bug(
                    title="[Writeback] Powerwells are not disabled for Writeback device",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info("\tPASS: Powerwells are disabled successfully")
        logging.debug("writeback_verifier: verify_wb_disable_sequence() Exit:")
        return True

    ##
    # @brief         Verify caching
    # @param[in]     wb_device_list; list of writeback devices
    # @return        boolean value true or false
    def verify_caching(self, wb_device_list):
        logging.debug("writeback_verifier: verify_caching() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % (self.platform))
        trans_conf_file = importlib.import_module("registers.skl.TRANS_CONF_REGISTER")

        for wb_device_index in range(0, len(wb_device_list)):
            wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(wb_device_index)
            wd_trans_ctl_reg_value = self.reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg, self.platform,
                                                        0x0)

            if (wd_trans_ctl_reg_value.__getattribute__("enable_write_caching") != getattr(wd_trans_ctl_file,
                                                                                           "enable_write_caching_ENABLE")):
                logging.info("\tFAIL: Write caching is not enabled for writeback device WB_%s" % wb_device_index)
                gdhm.report_bug(
                    title="[Writeback] Write caching is not enabled for Writeback device WB_{0}".format(
                        wb_device_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            else:
                logging.info("\tPASS: Write Caching is enabled for writeback device WB_%s" % wb_device_index)
                # Todo : Need to change the logic of write caching based on the inputs from SV team for programming distance between head and tail pointer
                if (wd_trans_ctl_reg_value.__getattribute__("maximum_defference_to_enable_write_caching") != getattr(
                        wd_trans_ctl_file, "maximum_defference_to_enable_write_caching_0")):
                    logging.info("\tFAIL: All Writes are not cached for writeback device WB_%s" % wb_device_index)
                    gdhm.report_bug(
                        title="[Writeback] Writes are not cached for Writeback device WB_{0}".format(wb_device_index),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2)
                    return False
            logging.info("\tPASS: All Writes are cached for writeback device WB_%s" % wb_device_index)

        logging.debug("writeback_verifier: verify_caching() Exit:")
        return True

    ##
    # @brief         Verify display vdenc improvement
    # @param[in]     wb_device_list; list of writeback devices
    # @return        boolean value true or false
    def verify_display_vdenc_improvement(self, wb_device_list):
        logging.debug("writeback_verifier: verify_display_vdenc_improvement() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % self.platform)
        trans_conf_file = importlib.import_module("registers.skl.TRANS_CONF_REGISTER")

        for wb_device_index in range(0, len(wb_device_list)):
            wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(wb_device_index)
            wd_trans_ctl_reg_value = self.reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg, self.platform,
                                                        0x0)

            if self.platform in self.display_vdenc_improvement_platform_list:
                if (wd_trans_ctl_reg_value.__getattribute__("control_pointers") != getattr(wd_trans_ctl_file,
                                                                                           "control_pointers_00")) and (
                        wd_trans_ctl_reg_value.__getattribute__("control_pointers") == getattr(wd_trans_ctl_file,
                                                                                               "control_pointers_11")):
                    logging.info(
                        "\tFAIL: Display vdenc interface improvement is not enabled for writeback device WB_%s, eventhough it is supported on this platform" % wb_device_index)
                    gdhm.report_bug(
                        title="[Writeback] Display VDEnc Interface Improvement is not enabled for Writeback device WB_{0} on {0} Supported platform".format(
                            wb_device_index, self.platform),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2)
                    return False
                elif (wd_trans_ctl_reg_value.__getattribute__("control_pointers") == getattr(wd_trans_ctl_file,
                                                                                             "control_pointers_00")) and (
                        wd_trans_ctl_reg_value.__getattribute__("control_pointers") != getattr(wd_trans_ctl_file,
                                                                                               "control_pointers_11")):
                    logging.info(
                        "\tPASS: Display vdenc interface improvement is enabled for writeback device WB_%s and it is supported on this platform" % wb_device_index)
                else:
                    logging.info(
                        "\FAIL: Invalid value programmed for control_pointers field for writeback device WB_%s" % wb_device_index)
                    gdhm.report_bug(
                        title="[Writeback] Invalid value programmed for control_pointers field for Writeback device WB_{0}".format(
                            wb_device_index),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2)
                    return False
            else:
                if (wd_trans_ctl_reg_value.__getattribute__("control_pointers") == getattr(wd_trans_ctl_file,
                                                                                           "control_pointers_00")) and (
                        wd_trans_ctl_reg_value.__getattribute__("control_pointers") != getattr(wd_trans_ctl_file,
                                                                                               "control_pointers_11")):
                    logging.info(
                        "\tFAIL: Display vdenc interface improvement is enabled for writeback device WB_%s, eventhough it is not supported on this platform" % wb_device_index)
                    gdhm.report_bug(
                        title="[Writeback] Display VDEnc Interface Improvement is enabled for Writeback device WB_{0} on Unsupported platform".format(
                            wb_device_index),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2)
                    return False
                elif (wd_trans_ctl_reg_value.__getattribute__("control_pointers") != getattr(wd_trans_ctl_file,
                                                                                             "control_pointers_00")) and (
                        wd_trans_ctl_reg_value.__getattribute__("control_pointers") == getattr(wd_trans_ctl_file,
                                                                                               "control_pointers_11")):
                    logging.info(
                        "\tPASS: Display vdenc interface improvement is not enabled for writeback device WB_%s and it is not supported on this platform" % wb_device_index)
                else:
                    logging.info(
                        "\tFAIL: Invalid value programmed for control_pointers field for writeback device WB_%s" % wb_device_index)
                    gdhm.report_bug(
                        title="[Writeback] Invalid value programmed for control_pointers field for Writeback device WB_{0}".format(
                            wb_device_index),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2)
                    return False
        logging.debug("writeback_verifier: verify_display_vdenc_improvement() Exit:")
        return True

    ##
    # @brief        Verify frame number programming
    # @param[in]    wb_device_list; list of writeback devices
    # @return       boolean value true or false
    def verify_frame_number_programming(self, wb_device_list):
        logging.debug("writeback_verifier: verify_frame_number_programming() Entry:")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        wd_trans_ctl_file = importlib.import_module("registers.%s.TRANS_WD_FUNC_CTL_REGISTER" % (self.platform))
        trans_conf_file = importlib.import_module("registers.skl.TRANS_CONF_REGISTER")

        for wb_device_index in range(0, len(wb_device_list)):
            wd_trans_ctl_reg = "TRANS_WD_FUNC_CTL_" + str(wb_device_index)
            for count in range(0, self.frame_number_count):
                wd_trans_ctl_reg_value = self.reg_read.read('TRANS_WD_FUNC_CTL_REGISTER', wd_trans_ctl_reg,
                                                            self.platform, 0x0)
                self.frame_number_list.append(str(hex(wd_trans_ctl_reg_value.__getattribute__("frame_number"))))
                logging.info("Frame number = %s\n" % self.frame_number_list[count])
                time.sleep(1)  # wait for 1 sec before reading resgister next time

            # check for duplicate entry (framenumber) in frame_number_list
            if self.is_duplicate_entry_in_list(self.frame_number_list):
                logging.info(
                    "\tFAIL: Invalid value programmed for frame number field (BIT0 - BIT3) for writeback device WB_%s" % wb_device_index)
                gdhm.report_bug(
                    title="[Writeback] Invalid value programmed for frame_number field for Writeback device WB_{0}".format(
                        wb_device_index),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2)
                return False
            logging.info(
                "\tPASS: Frame number field (BIT0 - BIT3)is properly programmed for writeback device WB_%s" % wb_device_index)
        logging.info("\tPASS: Frame number field (BIT0 - BIT3)is properly programmed for all writeback devices")
        logging.debug("writeback_verifier: verify_frame_number_programming() Exit:")
        return True

    ##
    # @brief        Verify is there any duplicate entry in the list
    # @param[in]    input_list;
    # @return       boolean value true or false
    def is_duplicate_entry_in_list(self, input_list):
        logging.debug("writeback_verifier: is_duplicate_entry_in_list() Entry:")
        for frame_num in range(0, len(input_list)):
            index = frame_num + 1
            for index in range(index, len(input_list)):
                if input_list[frame_num] == input_list[index]:
                    logging.info("\tFAIL: Found duplicate values in provided frame number list")
                    logging.debug("writeback_verifier: is_duplicate_entry_in_list() Exit:")
                    return True
        return False
