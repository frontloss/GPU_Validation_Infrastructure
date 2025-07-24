##
# @file    clock_helper.py
# @brief   Python helper class for doing generic functions for clock verification
# @author  rradhakr, Doriwala Nainesh P

import logging
import math
from dataclasses import dataclass
from enum import IntEnum
from math import floor
from typing import Tuple, Union

import Libs.Feature.display_port.dpcd_helper as dpcd
from DisplayRegs import DisplayArgs
from DisplayRegs.Gen14.Transcoder import Gen14TranscoderRegs  # Do not remove
from DisplayRegs.Gen14.Pll import Gen14PllRegs
from DisplayRegs.Gen14.Ddi import Gen14DdiRegs  # Do not remove
from DisplayRegs.Gen15.Transcoder import Gen15TranscoderRegs  # Do not remove
from DisplayRegs.Gen15.Pll import Gen15PllRegs
from Libs.Core import display_utility, driver_escape
from Libs.Core.wrapper.driver_escape_args import CuiDeepColorInfo
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.display_config.display_config_struct import TARGET_ID
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Feature.vdsc.dsc_enum_constants import DPCDOffsets, DSCEngine
from registers.mmioregister import MMIORegister

PSR_CAPS_DPCD_OFFSET = 0x70

GEN16_PLUS_MAX_HACTIVE_SUPPORTED = 6144
PRE_GEN16_MAX_HACTIVE_SUPPORTED = 5120
MAX_V_ACTIVE_SUPPORTED = 4320

PRE_GEN14_PIPE_JOINED_MAX_H_ACTIVE = 7680
PRE_GEN14_PIPE_JOINED_MAX_V_ACTIVE = 4320

# Except MTL
GEN14_PIPE_JOINED_MAX_H_ACTIVE = 8192
GEN14_PIPE_JOINED_MAX_V_ACTIVE = 4800

# Custom Scaling Downscaling factor in 1K
MAX_DOWNSCALING_FACTOR = 1125

GEN14PLUS_MAX_CD_CLOCK_MHZ = 652.8  # in MHz
GEN14PLUS_EFFECTIVE_CD_CLOCK_MHZ = GEN14PLUS_MAX_CD_CLOCK_MHZ * 2  # in MHz

PTL_MAX_CD_CLOCK_MHZ = 691.2  # in MHz
PTL_EFFECTIVE_CD_CLOCK_MHZ = PTL_MAX_CD_CLOCK_MHZ * 2  # in MHz
PTL_NON_DSC_EFFECTIVE_CD_CLOCK_MHZ = 1350

NVL_MAX_CD_CLOCK_MHZ = 787.2  # in MHz
NVL_EFFECTIVE_CD_CLOCK_MHZ = 1537.5  # in MHz

WCL_MAX_CD_CLOCK_MHZ = 480.0  # in MHz

# Default Reference clock frequency - Gen14+
DEFAULT_REFERENCE_CLOCK_FREQUENCY = 38.4

##
# @brief        This DataClass is used to generate CD Clock verification expectations
@dataclass
class CdClockMap:
    # Programmed CD clock frequency in MHz.
    cdclk_freq: float
    # This field selects the CDCLK PLL divider ratio, controlling the output frequency.
    pll_ratio: int
    # This field selects how the CDCLK PLL output is divided before driving the display CD2X clock.
    cd2x_divider: int
    # This field selects the source for the memory clock MDCLK.
    pll_output: float
    # This field sets the cd2xclk waveform produced by the squashing logic.
    squash_wave: int
    # This field describes the Voltage Frequency group where current mapping belongs
    vf_level: int


##
# @brief        Voltage frequency level enum
class VoltageFrequencyLevel(IntEnum):
    VF0 = 0
    VF1 = 1
    VF2 = 2
    VF3 = 3


##
# @brief        Translation Throttle Min enum
# @details      Ref: DBUF_CTL bits 18:16
# @details      Ref: MBUS_CTL bits 15:13
class MBusType(IntEnum):
    SEPARATE_MDCLK2_CDCLK1 = 1  # 1b
    SEPARATE_MDCLK3_CDCLK1 = 2  # 2b
    SEPARATE_MDCLK4_CDCLK1 = 3  # 3b, Also applicable for JOINED_MDCLK2_CDCLK1
    JOINED_MDCLK3_CDCLK1 = 5  # 5b
    JOINED_MDCLK4_CDCLK1 = 7  # 7b


##
# @brief    Helper class for clock related methods.
class ClockHelper:
    ##
    # To Do: Need to add Gen 17 platform check in the Future.
    PRE_GEN_14_PLATFORMS = ['TGL', 'RKL', 'DG1', 'ADLS', 'DG2', 'ADLP']
    GEN_14_PLATFORMS = ['DG3', 'MTL', 'ELG']
    GEN_15_PLATFORMS = ['LNL']
    GEN_16_PLATFORMS = ['PTL']
    GEN_17_PLATFORMS = ['NVL', 'CLS']

    # Mapping of bit per color
    trans_ddi_func_ctl_bit_per_color = dict([
        (8, 0),
        (10, 1),
        (6, 2),
        (12, 3)
    ])

    # Mapping of color format
    pipe_misc_color_format = dict([
        ('RGB', 0),
        ('YUV420', 1)
    ])

    # Color Format to BPP map
    colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25),
                                  ('RGB_12', 1.5), ('YUV420_8', 0.5),
                                  ('YUV420_10', 0.625), ('YUV420_12', 0.75)])
    ##
    # @brief    This dictionary defines possible values for reference clock programming in DSSM register bits 31:29
    reference_clock = {
        "LNL": {
            0: 24,  # 000b = 24 MHz
            1: 19.2,  # 001b = 19.2 MHz
            2: DEFAULT_REFERENCE_CLOCK_FREQUENCY,  # 010b = 38.4 MHz
            3: 25  # 011b = 25 MHz
        },
        "PTL": {
            0: 24,  # 000b = 24 MHz
            1: 19.2,  # 001b = 19.2 MHz
            2: DEFAULT_REFERENCE_CLOCK_FREQUENCY,  # 010b = 38.4 MHz
            3: 25  # 011b = 25 MHz
        },
        "NVL": {
            0: 24,  # 000b = 24 MHz
            1: 19.2,  # 001b = 19.2 MHz
            2: DEFAULT_REFERENCE_CLOCK_FREQUENCY,  # 010b = 38.4 MHz
            3: 25  # 011b = 25 MHz
        },
        "ELG": {
            2: DEFAULT_REFERENCE_CLOCK_FREQUENCY,  # 010b = 38.4 MHz
        },
        "MTL": {
            2: DEFAULT_REFERENCE_CLOCK_FREQUENCY,  # 010b = 38.4 MHz
        }
    }

    ##
    # @brief Get the value by range for the features
    # @param[in] reg_value - Register value
    # @param[in] start - Starting bit of range
    # @param[in] end - End bit of range
    # @param[in] dict_map - Dictionary mapping of feature
    # @param[in] feature - Feature mapping
    # @return  feature value
    def get_value_by_range(self, reg_value, start, end, dict_map, feature):
        feature_val = (reg_value & ((1 << (end + 1)) - 1)) >> start
        if dict_map != '':
            if feature_val in dict_map.values():
                new_val = list(dict_map)[list(dict_map.values()).index(feature_val)]
                return new_val
            else:
                logging.debug("Warning:Value {0} is not present in the map for feature {1}"
                              .format(hex(feature_val), feature))
        else:
            logging.debug("{0}-> Range ({1},{2}) - {3} = {4}"
                          .format(feature, start, end, hex(reg_value), feature_val))
            return feature_val

    ##
    # @brief Get the mapped value for the features
    # @param[in] feature_val - feature value,
    # @param[in] dict_map - dictionary to map
    # @param[in] feature - Feature name
    # @return  feature value
    def map_reg_value_to_dict(self, feature_val, dict_map, feature):
        if dict_map != '':
            if feature_val in dict_map.values():
                mapped_key = list(dict_map)[list(dict_map.values()).index(feature_val)]
                logging.debug("Value {0} is present in the map for feature {1} and the mapped key is: {2}"
                              .format(feature_val, feature, mapped_key))
                return mapped_key
            else:
                logging.debug("Warning:Value {0} is not present in the map for feature {1}"
                              .format(hex(feature_val), feature))
        else:
            logging.debug("{0}-> Offset Value :{1}"
                          .format(feature, feature_val))
            return feature_val

    ##
    # @brief Function to read register value for given adapter
    # @param[in] register - Register definition
    # @param[in] offset - Offset of register
    # @param[in] gfx_index - Graphics index on which register read
    # @return register value
    def clock_register_read(self, register, offset, gfx_index='gfx_0'):
        platform = ClockHelper.get_platform_name(gfx_index)

        reg_value = MMIORegister.read(register, offset, platform, gfx_index=gfx_index)
        logging.debug("{0}--> Offset : {1} Value :{2}"
                      .format(offset, hex(reg_value.offset), hex(reg_value.asUint)))
        return reg_value.asUint

    ##
    # @brief Get TargetId for the give Display on given graphics adapter
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which register read
    # @return target_id
    def get_target_id(self, display_port, gfx_index='gfx_0'):
        display_config_ = display_config.DisplayConfiguration()
        display_and_adapter_info = display_config_.get_display_and_adapter_info_ex(display_port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        target_id = display_and_adapter_info.TargetID
        logging.debug("INFO : Target Id for Display {0} is {1}".format(display_port, str(target_id)))
        return target_id

    ##
    # @brief Get AdapterInfo for the Given Display and graphics adapter
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which register read
    # @return display_and_adapter_info
    def get_adapter_info(self, display_port, gfx_index='gfx_0'):
        display_config_ = display_config.DisplayConfiguration()
        display_and_adapter_info = display_config_.get_display_and_adapter_info_ex(display_port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        return display_and_adapter_info

    ##
    # @brief        Get Pixel Rate for the Display
    # @param[in]    display_port - Display port
    # @param[in]    gfx_index - Graphics index on which register read
    # @param[in]    require_target_id - Returns TargetID for current panel if set to True
    # @return       pixel_rate and target_id based on require_target_id parameter value
    def get_pixel_rate(self, display_port, gfx_index='gfx_0', require_target_id=False) -> Union[int, Tuple[int, int]]:
        pixel_rate = 0  # Assigning default value in case of failures
        display_config_ = display_config.DisplayConfiguration()

        platform = ClockHelper.get_platform_name(gfx_index)
        adapter_info = self.get_adapter_info(display_port, gfx_index)
        current_mode = display_config_.get_current_mode(adapter_info)

        if platform not in self.PRE_GEN_14_PLATFORMS + ['MTL']:  # Gen14+ platforms except MTL
            if current_mode.pixelClock_Hz != 0:
                pixel_rate = (float(current_mode.pixelClock_Hz) / 1000000)
            else:
                gdhm.report_bug(
                    title=f"[Interfaces][Display_Engine][CD Clock] Failed to get pixel clock from OS API",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f"Failed to get pixel clock from OS API for {display_port} on {gfx_index}")
        else:
            display_timings = display_config_.get_display_timings(adapter_info)

            if display_timings.vSyncNumerator == 0:
                # WA to handle cases where vSync values are not properly filled from DLL
                pixel_rate = (float(current_mode.pixelClock_Hz) / 1000000)
            else:
                pixel_rate = (float(display_timings.vSyncNumerator) / 1000000)

        if require_target_id is True:
            return pixel_rate, current_mode.targetId
        return pixel_rate

    ##
    # @brief        Get the max Pixel Rate among the Displays
    # @param[in]    display_list - List of Display
    # @param[in]    gfx_index - Graphics index on which register read
    # @param[in]    require_target_id - Returns TargetID of first display with max pixel clock value
    # @param[in]    pipe_joiner_ports - Pass pipe joiner ports info if detected in current setup
    # @return       pixel_rate and target_id based on require_target_id parameter value
    def get_max_pixel_rate(self, display_list, gfx_index='gfx_0', require_target_id=False, pipe_joiner_ports=None) -> \
            Union[int, Tuple[int, int]]:
        if pipe_joiner_ports is None:
            pipe_joiner_ports = {}
        pixel_rates = {}
        logging.info(f"display_list={display_list}")

        for display_port in display_list:
            logging.info(f"display_port={display_port}")
            pixel_rate, target_id = self.get_pixel_rate(display_port, gfx_index, True)
            if display_port in pipe_joiner_ports.keys():
                if pipe_joiner_ports[display_port]['gfx_index'] == gfx_index:
                    # Divide the pixel rate by no of pipes to get the correct pixel rate for each of the pipe.
                    pixel_rates[target_id] = pixel_rate / pipe_joiner_ports[display_port]['no_of_pipe_required']
            else:
                pixel_rates[target_id] = pixel_rate

        max_pixel_rate = max(pixel_rates.values())
        target_id = list(pixel_rates.keys())[list(pixel_rates.values()).index(max_pixel_rate)]
        logging.info("INFO : Max Pixel Clock is {0}, Target {1}:{2}".format(max_pixel_rate, gfx_index, target_id))

        if require_target_id is True:
            max_pixel_rate_target_id = (max_pixel_rate, target_id)
            return max_pixel_rate_target_id
        return max_pixel_rate

    ##
    # @brief function to get SSC value from DPCD.
    # @param[in] display_port - Display Port
    # @param[in] gfx_index - Graphics index
    # @return BOOL ssc value
    def get_ssc_from_dpcd(self, display_port, gfx_index='gfx_0'):
        vbt = Vbt(gfx_index)
        display_config_ = display_config.DisplayConfiguration()
        adapter_info = display_config_.get_display_and_adapter_info_ex(display_port, gfx_index)
        if type(adapter_info) is list:
            adapter_info = adapter_info[0]

        ssc_enable_dpcd = dpcd.DPCD_getSSC(adapter_info)

        if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                           display_utility.VbtPanelType.LFP_MIPI]:
            logging.debug("INFO : VBT Panel Type:" + str(vbt.block_40.PanelType))
            logging.debug("INFO : VBT SSC Enabled Bits:" + str(vbt.block_40.LvdsSscEnableBits))
            ssc_enable_vbt = (vbt.block_40.LvdsSscEnableBits & (
                    (1 << (vbt.block_40.PanelType + 1)) - 1)) >> vbt.block_40.PanelType
        else:
            # bit[3] for DP SSC and bit[5] for DP active dongle SSC enable
            # For now only DP SSC is enabled, dongle SSC is not considered
            ssc_enable_vbt = vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Enable
            logging.debug("INFO : VBT SSC Enabled Bits:" + str(vbt.block_1.IntegratedDisplaysSupported.value))

        ssc_dpcd = "ENABLED" if ssc_enable_dpcd else "DISABLED"
        ssc_vbt = "ENABLED" if ssc_enable_vbt else "DISABLED"
        logging.info("INFO : SSC - VBT ({0}) DPCD ({1})".format(ssc_vbt, ssc_dpcd))

        return ssc_enable_dpcd and ssc_enable_vbt

    ##
    # @brief        Method to validate CD Clock check status based on test expected and actual inputs
    # @param[in]    current_value - Actual value
    # @param[in]    expected_value - Expected value
    # @param[in]    feature - Feature name
    # @return       Return True if verification is successful, False otherwise
    @classmethod
    def verify_cd_clock_programming(cls, current_value, expected_value, feature):
        return cls.__verify_clock_programming(current_value, expected_value, feature, "CD Clock")

    ##
    # @brief        Method to validate Port Clock check status based on test expected and actual inputs
    # @param[in]    current_value - Actual value
    # @param[in]    expected_value - Expected value
    # @param[in]    feature - Feature name
    # @return       Return True if verification is successful, False otherwise
    @classmethod
    def verify_port_clock_programming(cls, current_value, expected_value, feature):
        return cls.__verify_clock_programming(current_value, expected_value, feature, "Port Clock")

    ##
    # @brief        Generic method to validate check status based on test expected and actual inputs
    # @param[in]    current_value - Actual value
    # @param[in]    expected_value - Expected value
    # @param[in]    feature - Feature name
    # @return       Return True if verification is successful, False otherwise
    @classmethod
    def __verify_clock_programming(cls, current_value, expected_value, feature, feature_name):
        if current_value == expected_value:
            logging.info(
                "PASS : {0} - Expected : {1} Actual : {2}".format(feature, str(expected_value), str(current_value)))
            return True
        else:
            gdhm.report_bug(
                title=f"[Interfaces][Display_Engine][{feature_name}] Verification failed for: {feature}."
                      f"Expected: {expected_value} and Actual: {current_value}",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "FAIL : {0} - Expected : {1} Actual : {2}".format(feature, str(expected_value), str(current_value)))
            return False

    ##
    # @brief        Method to validate CD Clock check status based on test expected and actual inputs passed as lists
    # @param[in]    feature - Feature name
    # @param[in]    parameter - List of features
    # @param[in]    expected - Expected value
    # @param[in]    actual - Actual value
    # @return       Return True if verification is successful, False otherwise
    @classmethod
    def verify_cd_clock_programming_ex(cls, feature, parameter, expected, actual):
        return cls.__verify_clock_programming_ex(feature, parameter, expected, actual, "CD Clock")

    ##
    # @brief        Method to validate Port Clock check status based on test expected and actual inputs passed as lists
    # @param[in]    feature - Feature name
    # @param[in]    parameter - List of features
    # @param[in]    expected - Expected value
    # @param[in]    actual - Actual value
    # @return       Return True if verification is successful, False otherwise
    @classmethod
    def verify_port_clock_programming_ex(cls, feature, parameter, expected, actual):
        return cls.__verify_clock_programming_ex(feature, parameter, expected, actual, "Port Clock")

    ##
    # @brief        Generic method to validate check status based on test expected and actual inputs passed as lists
    # @param[in]    feature - Feature name
    # @param[in]    parameter - List of features
    # @param[in]    expected - Expected value
    # @param[in]    actual - Actual value
    # @return       Return True if verification is successful, False otherwise
    @classmethod
    def __verify_clock_programming_ex(cls, feature, parameter, expected, actual, feature_name):
        temp_fail = []
        logger_template_pass = "PASS : {feature:<60}: Expected: {exp:<20}  Actual: {act}"
        logger_template_fail = "FAIL : {feature:<60}: Expected: {exp:<20}  Actual: {act}  --> {failure}"

        if len(expected) != len(actual):
            gdhm.report_bug(
                title=f"[Interfaces][Display_Engine][{feature_name}] Invalid parameters given to compare: {feature}",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(f"Expected and Actual Length is NOT Matching for {feature}. "
                          f"Parameters - Expected {expected} Actual {actual}")
            return False

        for index in range(len(expected)):
            if expected[index] != actual[index]:
                temp_fail.append(parameter[index])

        formatted_exp = '[{0}]'.format(','.join(map(str, expected)))
        formatted_act = '[{0}]'.format(','.join(map(str, actual)))

        if len(temp_fail) != 0:
            if len(expected) != 1:
                formatted_fail_str = '[{0}]'.format(','.join(map(str, temp_fail)))
                gdhm.report_bug(
                    title=f"[Interfaces][Display_Engine][{feature_name}] Verification failed for: {formatted_fail_str}",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    logger_template_fail.format(feature=f"{feature} - {parameter}", exp=formatted_exp,
                                                act=formatted_act, failure=formatted_fail_str))
            else:
                gdhm.report_bug(
                    title=f"[Interfaces][Display_Engine][{feature_name}] Verification failed for: {parameter}",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    logger_template_fail.format(feature=f"{feature} - {parameter}", exp=formatted_exp,
                                                act=formatted_act, failure=parameter))
            return False
        else:
            logging.info(logger_template_pass.format(feature=f"{feature} - {parameter}", exp=formatted_exp,
                                                     act=formatted_act))
        return True

    ##
    # @brief function to check dynamic cd clk enable or not for particular graphics driver
    # @param[in] gfx_index - Graphics index
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def is_dynamic_cdclock_enabled(self, gfx_index='gfx_0'):
        logging.debug('Getting VBT Block 1 : To Check for Dynamic CD Clock Enabled')
        return (Vbt(gfx_index).block_1.BmpBits2 & 64) == 64

    ##
    # @brief function to write dekel phy index value and read dekel phy register
    # @param[in] register - dekel phy register name
    # @param[in] offset - offset of register
    # @param[in] display_tc_port - takes valid values of ['TC1', 'TC2', 'TC3', 'TC4', 'TC5', 'TC6']
    # @param[in] gfx_index - Graphics index
    # @param[in] mmio_index - the index that needs to be written into HIP_INDEX_REGISTER before doing DKL reg read
    # @return dekel phy register value
    def read_dkl_register(self, register, offset, display_tc_port, gfx_index='gfx_0', mmio_index=2):
        reg_value = 0
        index_register = 0

        port_index_mmio_write_map = dict([
            ('TC1', mmio_index),
            ('TC2', mmio_index << 8),
            ('TC3', mmio_index << 16),
            ('TC4', mmio_index << 24),
            ('TC5', mmio_index),
            ('TC6', mmio_index << 8)
        ])

        port_index_mmio_write_clear_map = dict([
            ('TC1', 0xffffff00),
            ('TC2', 0xffff00ff),
            ('TC3', 0xff00ffff),
            ('TC4', 0x00ffffff),
            ('TC5', 0xffffff00),
            ('TC6', 0xffff00ff)
        ])

        platform = ClockHelper.get_platform_name(gfx_index)

        if str(display_tc_port).upper() in ['TC1', 'TC2', 'TC3', 'TC4']:
            index_register = 0x1010A0
            reg_value = self.clock_register_read('HIP_INDEX_REG0_REGISTER',
                                                 'HIP_INDEX_REG0', gfx_index)
        elif str(display_tc_port).upper() in ['TC5', 'TC6']:
            index_register = 0x1010A4
            reg_value = self.clock_register_read('HIP_INDEX_REG1_REGISTER',
                                                 'HIP_INDEX_REG1', gfx_index)
        else:
            logging.info("Fail:Port is not valid for Dekel phy programming. Port passed is {0}".format(
                str(display_tc_port).upper()))

        reg_value_mimo_clear = reg_value & port_index_mmio_write_clear_map[str(display_tc_port).upper()]
        reg_value_mmio_write = reg_value_mimo_clear | port_index_mmio_write_map[str(display_tc_port).upper()]
        driver_interface.DriverInterface().mmio_write(index_register, reg_value_mmio_write, gfx_index)

        return MMIORegister.read(register, offset, platform, gfx_index=gfx_index)

    ##
    # @brief function to check if minimum of psr2 is supported
    # @param[in] display_port - port name . e.g. DP_A , DP_B
    # @param[in] gfx_index - graphics index
    # @return Boolean : True or False
    def __is_min_psr2_supported(self, display_port, gfx_index='gfx_0'):
        display_config_ = display_config.DisplayConfiguration()
        if display_utility.get_vbt_panel_type(display_port, gfx_index) != display_utility.VbtPanelType.LFP_DP:
            return False
        disp_adap_info = display_config_.get_display_and_adapter_info_ex(display_port, gfx_index)
        if type(disp_adap_info) is list:
            disp_adap_info = disp_adap_info[0]

        flag, value = driver_escape.read_dpcd(disp_adap_info, PSR_CAPS_DPCD_OFFSET)
        if flag:
            if value[0] >= 0x02:  # 0x02 indicates PSR2 , higher values indicate higher versions of PSR
                return True
            else:
                return False
        return False

    ##
    # @brief function to check if DC3C0 is supported or not
    # @param[in] display_port - port name . e.g. DP_A , DP_B
    # @param[in] gfx_index - Graphics index
    # @return Boolean - True or False
    def is_dc3c0_supported(self, display_port, gfx_index='gfx_0'):
        display_config_ = display_config.DisplayConfiguration()
        platform = ClockHelper.get_platform_name(gfx_index)

        current_config = display_config_.get_current_display_configuration()
        # HW may put system in DC3C0 state if PSR2 is active on Gen12 and above platforms
        if current_config.numberOfDisplays == 1 and \
                platform not in ['HSW', 'SKL', 'GLK', 'CFL', 'KBL', 'ICLLP', 'ICLHP', 'ICL', 'LKF1', 'JSL'] and \
                self.__is_min_psr2_supported(display_port, gfx_index):
            logging.info("DC3C0 supported, platform = {0}".format(platform))
            return True
        else:
            logging.info("DC3C0 not supported, platform = {0}".format(platform))
            return False

    ##
    # @brief function to get max dsc slice of 1 pixel clock
    # @param[in] gfx_index - Graphics index
    # @param[in] display_list - List of Displays
    # @return max_dsc_slice_1_pixel_clock
    def get_max_dsc_slice_1_pixel_clock(self, gfx_index, display_list, require_target_id=False):
        from Libs.Feature.vdsc.dsc_helper import DSCHelper

        display_config_ = display_config.DisplayConfiguration()
        max_dsc_slice_1_pixel_clock = slice_caps1 = slice_caps2 = 0
        max_dsc_slice_1_target_id = None
        for display_port in display_list:
            target_id = self.get_target_id(display_port, gfx_index)
            is_vdsc_supported = DSCHelper.is_vdsc_supported_in_panel(gfx_index, display_port)
            is_vdsc_supported = is_vdsc_supported and DSCHelper.is_vdsc_enabled_in_driver(gfx_index, display_port)
            if is_vdsc_supported is True:
                if 'EDP' in display_port or 'DP' in display_port:
                    slice_caps1 = \
                    DSCHelper.read_dpcd(gfx_index, display_port, DPCDOffsets.DSC_SLICE_CAPABILITIES_1)[0]
                    slice_caps2 = \
                    DSCHelper.read_dpcd(gfx_index, display_port, DPCDOffsets.DSC_SLICE_CAPABILITIES_2)[0]
                elif 'HDMI' in display_port:
                    hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
                    hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, display_port)
                    slice_caps1, _ = hf_vsdb_parser.dsc_max_slices
                    slice_caps2 = 0

            if slice_caps1 == 1 and slice_caps2 == 0:
                current_mode = display_config_.get_display_timings(target_id)
                pixel_rate = (float(current_mode.vSyncNumerator) / 1000000)
                if pixel_rate > max_dsc_slice_1_pixel_clock:
                    max_dsc_slice_1_pixel_clock = pixel_rate
                    max_dsc_slice_1_target_id = target_id

        if require_target_id is True:
            max_pixel_rate_target_id = (max_dsc_slice_1_pixel_clock, max_dsc_slice_1_target_id)
            return max_pixel_rate_target_id
        return max_dsc_slice_1_pixel_clock

    ##
    # @brief function to check panel's and driver's dsc status for current mode
    # @param[in] gfx_index - Graphics index
    # @param[in] display_list - List of Displays
    # @return max_dsc_slice_1_pixel_clock
    def get_dsc_status_for_current_mode(self, gfx_index, port_name):
        from Libs.Feature.vdsc.dsc_helper import DSCHelper
        display_config_ = display_config.DisplayConfiguration()

        display_and_adapter_info = display_config_.get_display_and_adapter_info_ex(port_name, gfx_index)

        current_mode = display_config_.get_current_mode(display_and_adapter_info)
        logging.info(f'HActive: {current_mode.HzRes}, VActive: {current_mode.VtRes} for display at: {port_name}')
        logging.info(f'Pixel Rate: {current_mode.pixelClock_Hz}hz for display at: {port_name}')

        is_vdsc_supported = DSCHelper.is_vdsc_supported_in_panel(gfx_index, port_name)
        is_vdsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port_name)

        return  is_vdsc_supported, is_vdsc_enabled

    ##
    # @brief function to get HTotal and Slice Count
    # @param[in] gfx_index - Graphics index
    # @param[in] pixel_rate_target_id - pixel rate and target_id
    # @param[in] display_port - port_name e.g DP_A, DP_F
    # @param[in] no_of_pipe_required - to get pipe count for pipe joiner case
    # @return h_total and slice_count
    def get_h_total_slice_count(self, gfx_index, pixel_rate_target_id, display_port, no_of_pipe_required):
        from Libs.Feature.vdsc.dsc_helper import DSCHelper

        target_id = pixel_rate_target_id[1]
        slice_count = 0
        display_configuration = display_config.DisplayConfiguration()
        display_and_adapter_info = display_configuration.get_display_and_adapter_info(target_id)
        display_timing = DSCHelper.get_display_timing_from_qdc(display_and_adapter_info)
        logging.info('Pixel Rate: {}hz for Target Id: {}'.format(display_timing.targetPixelRate, target_id))

        h_total = (display_timing.hTotal / no_of_pipe_required)

        # Get PIPE
        disp_base = display_base.DisplayBase(display_port)
        pipe, ddi = disp_base.GetPipeDDIAttachedToPort(display_port)
        pipe = pipe.split('_')[-1].upper()
        logging.info(f"=====>pipe: {pipe}")

        # GET Platform
        platform = ClockHelper.get_platform_name(gfx_index)
        logging.info(f"=====>platform: {platform}")
        r_offset = 'PPS3_' + str(DSCEngine.LEFT.value) + '_' + pipe
        dsc_pps3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3", r_offset, platform, gfx_index=gfx_index)

        if dsc_pps3.slice_width != 0:
            slice_count = math.ceil(display_timing.hActive / dsc_pps3.slice_width)

        return h_total, slice_count

    ##
    # @brief function to get elevated pixel clock
    # @param[in] gfx_index - Graphics index
    # @param[in] pixel_rate_target_id - pixel rate and target_id
    # @param[in] display_list - display_port - port_name e.g DP_A, DP_F
    # @param[in] no_of_pipe_required - to get pipe count for pipe joiner case
    # @return h_total and slice_count
    def get_elevated_pixel_clock(self, gfx_index, pixel_rate_target_id, display_list, pipe_joiner_ports):
        from Libs.Feature.vdsc.dsc_helper import DSCHelper

        elevated_pixel_clock = pixel_rate_target_id[0]
        no_of_pipe_required = 1
        is_elevation_needed = False
        port = display_list[0]

        for display_port in display_list:
            target_id = self.get_target_id(display_port, gfx_index)
            if target_id == pixel_rate_target_id[1]:
                is_vdsc_supported = DSCHelper.is_vdsc_supported_in_panel(gfx_index, display_port)
                if is_vdsc_supported is True:
                    is_elevation_needed = True
                    if pipe_joiner_ports:
                        no_of_pipe_required = pipe_joiner_ports[display_port]['no_of_pipe_required']
                    port = display_port

        if is_elevation_needed:
            h_total, dsc_slice_per_line = self.get_h_total_slice_count(gfx_index, pixel_rate_target_id, port, no_of_pipe_required)
            elevated_pixel_clock_in_khz = elevated_pixel_clock * 1000

            logging.info(f"Pixel Clock to be elevated : {elevated_pixel_clock_in_khz}")
            logging.info(f"Elevation Needed - Htotal : {h_total}, slice : {dsc_slice_per_line}")

            elevated_pixel_clock_in_khz = self.calculate_elevated_pixel_clock(dsc_slice_per_line, h_total, elevated_pixel_clock_in_khz)
            elevated_pixel_clock = elevated_pixel_clock_in_khz / 1000

        logging.info(f"Elevated Pixel Clock : {elevated_pixel_clock}")
        return elevated_pixel_clock

    ##
    # @brief function to check if any non-dsc mode present in topology
    # @param[in] gfx_index - Graphics index
    # @param[in] display_list - display_port - port_name e.g. DP_A, DP_F
    # @return Boolean - True or False
    def is_non_dsc_mode_present(self, gfx_index, display_list):
        from Libs.Feature.vdsc.dsc_helper import DSCHelper
        for display_port in display_list:
            is_vdsc_supported = DSCHelper.is_vdsc_supported_in_panel(gfx_index, display_port)
            is_vdsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, display_port)
            if is_vdsc_supported and not is_vdsc_enabled:
                return True
        return False

    ##
    # @brief function to calculate elevated pixel clock
    # @param[in] dsc_slice_per_line - slice_count of current mode
    # @param[in] h_total - Htotal of current mode
    # @param[in] pixel_clock_in_khz - pixel clock to be elevated
    # @return elevated_pixel_clock
    def calculate_elevated_pixel_clock(self, dsc_slice_per_line, h_total, pixel_clock_in_khz):
        WORST_DSC_FLATNESS_DETERMINATION_CDCLK_CYCLES = 14
        DD_1K = 1000
        # Calculate DSC Slice Bubbles
        dsc_slice_bubbles = WORST_DSC_FLATNESS_DETERMINATION_CDCLK_CYCLES * dsc_slice_per_line
        # Calculate Elevated Horizontal Total
        elevated_h_total_1000 = (h_total + dsc_slice_bubbles) * DD_1K
        # Calculate DSC Slice Scale Factor
        dsc_slice_scale_factor_1000 = (elevated_h_total_1000 + h_total // 2) // h_total
        # Calculate Elevated Pixel Clock
        elevated_pixel_clock_in_khz_1000 = dsc_slice_scale_factor_1000 * pixel_clock_in_khz
        # Calculate final Pixel Clock in KHz
        pixel_clock_in_khz = (elevated_pixel_clock_in_khz_1000 + DD_1K // 2) // DD_1K
        return pixel_clock_in_khz


    ##
    # @brief for a given display_port, returns the port_type configured in the system.
    # @param[in] display_port   port name like DP_F, HDMI_B, etc.
    # @return port_type value like TC/TBT/Native
    def get_port_type_for_port(self, display_port):
        phy_type = None
        display_config_ = display_config.DisplayConfiguration()
        enumerated_displays = display_config_.get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            if str(cfg_enum.CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)) == display_port:
                phy_type = enumerated_displays.ConnectedDisplays[index].PortType
        return phy_type

    ##
    # @brief for a given display_port, tells if panel connected is DP 2.0 or not
    # @param[in] display_port   port name like DP_F, HDMI_B, etc.
    # @param[in] gfx_index      adapter index like 'gfx_0'
    # @return BOOL : returns True if DP 2.0, False otherwise
    def is_dp_2_0(self, display_port, gfx_index):
        if 'DP' in display_port:
            adapter_info = self.get_adapter_info(display_port, gfx_index)
            link_bw = dpcd.DPCD_getLinkRate(adapter_info)
            return True if link_bw in [10.0, 13.5, 20.0] else False
        return False

    ##
    # @brief for a given HDMI display, tells if panel connected is HDMI 2.1 or not
    # @param[in] display_port   port name like  HDMI_B, etc.
    # @param[in] gfx_index      adapter index like 'gfx_0'
    # @return BOOL : returns True if FRL is true and HDMI 2.1 is connected , False otherwise
    def is_hdmi_2_1(self, display_port, gfx_index):
        platform_gen = ""
        platform = ClockHelper.get_platform_name(gfx_index)
        if platform in self.PRE_GEN_14_PLATFORMS:
            return False
        elif platform in self.GEN_14_PLATFORMS:
            platform_gen = 'Gen14'
        elif platform in (self.GEN_15_PLATFORMS + self.GEN_16_PLATFORMS + self.GEN_17_PLATFORMS):
            platform_gen = 'Gen15'
        # The above code can be modified to Change the Transcoder Gen Value and pick corresponding Gen Transcoder
        db = display_base.DisplayBase(display_port, platform, gfx_index)
        pipe_ddi = db.GetPipeDDIAttachedToPort(display_port, False, gfx_index)
        pipe = (pipe_ddi[0])[-1]
        offset = eval(
            platform_gen + 'TranscoderRegs.OFFSET_TRANS_HDMI_FIXED_RATE_CFG.TRANS_HDMI_FIXED_RATE_CFG_' + pipe)
        value = DisplayArgs.read_register(offset, gfx_index)
        transcoder_reg = eval(platform_gen + 'TranscoderRegs')
        trans_hdmi_fixed_rate_cfg = transcoder_reg.REG_TRANS_HDMI_FIXED_RATE_CFG(offset, value)

        hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
        hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, display_port)
        hdmi_2_1_status = hf_vsdb_parser.is_frl_enable and trans_hdmi_fixed_rate_cfg.FrlFunctionEnable
        return hdmi_2_1_status

    ##
    # @brief        Private API to know if Pipe Joiner is required to drive the display.
    # @param[in]    gfx_index: str
    #                    Adapter ID e.g. gfx_0/gfx_1
    # @param[in]     port_name: str
    #                    Display Port e.g. DP_B/DP_C
    # @param[in]    effective_cd_clock_hz: int
    #                    CD Clock in hz
    # @return       (is_pipe_ganged_modeset, no_of_pipe_required): Tuple[bool, int]
    #               is_pipe_ganged_modeset: bool
    #                   Returns True if pipe joiner is required, False otherwise
    #               no_of_pipes_required: int
    #                   Returns the number of pipe required to drive the mode.
    @classmethod
    def is_pipe_joiner_required(cls, gfx_index: str, port_name: str, effective_cd_clock_hz: int) -> Tuple[bool, int]:
        is_pipe_joiner_required = False
        no_of_pipe_required = 1
        display_config_ = display_config.DisplayConfiguration()

        display_and_adapter_info = display_config_.get_display_and_adapter_info_ex(port_name, gfx_index)

        current_mode = display_config_.get_current_mode(display_and_adapter_info)
        logging.info(f'HActive: {current_mode.HzRes}, VActive: {current_mode.VtRes} for display at: {port_name}')
        logging.info(f'Pixel Rate: {current_mode.pixelClock_Hz}hz for display at: {port_name}')

        # In Case of Tiled Displays Two Pipes will be used. Hence, the Target Pixel Rate and h_active should be
        # Divided by 2 inorder to Determine per Port BW is Sufficient to Drive one half of the Tile Without using
        # Pipe Joiner.
        if TARGET_ID(Value=display_and_adapter_info.TargetID).TiledDisplay == 1:
            current_mode.pixelClock_Hz //= 2
            if current_mode.HzRes != 0:
                current_mode.HzRes //= 2
            else:
                assert False, "Failed to get horizontal resolution for tiled display"

        platform = ClockHelper.get_platform_name(gfx_index)
        logging.debug("Platform: {}".format(platform))

        if platform in machine_info.PRE_GEN_16_PLATFORMS:
            max_h_active = PRE_GEN16_MAX_HACTIVE_SUPPORTED
        else:
            max_h_active = GEN16_PLUS_MAX_HACTIVE_SUPPORTED

        if platform not in ['ELG']:
            max_pipe_joined_h_active = PRE_GEN14_PIPE_JOINED_MAX_H_ACTIVE
            max_pipe_joined_v_active = PRE_GEN14_PIPE_JOINED_MAX_V_ACTIVE
        else:
            max_pipe_joined_h_active = GEN14_PIPE_JOINED_MAX_H_ACTIVE
            max_pipe_joined_v_active = GEN14_PIPE_JOINED_MAX_V_ACTIVE

        h_active, v_active, pixel_clock_hz = current_mode.HzRes, current_mode.VtRes, current_mode.pixelClock_Hz

        if "HDMI" in port_name:
            hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
            hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, port_name)
            fva_factor = 1

            # TODO: Need to compute FVA factor for Compressed Video Format.
            if hf_vsdb_parser.is_fast_v_active_supported is True:
                fva_factor = 1

            pixel_clock_hz = fva_factor * pixel_clock_hz
        # TODO: Check for the fva_factor from the hf_vsdb_parser

        if (max_h_active < h_active) or (MAX_V_ACTIVE_SUPPORTED < v_active) or (
                effective_cd_clock_hz < pixel_clock_hz):
            if (max_pipe_joined_h_active >= h_active) and (max_pipe_joined_v_active >= v_active):
                if effective_cd_clock_hz >= (pixel_clock_hz / 2):
                    is_pipe_joiner_required = True
                    no_of_pipe_required = 2
                elif effective_cd_clock_hz >= (pixel_clock_hz / 4):
                    is_pipe_joiner_required = True
                    no_of_pipe_required = 4
            else:
                # Ideally this case should not be hit from test script.
                assert False, f"[Invalid Case] - Mode Not supported by the platform."

        logging.debug("Is Pipe Ganged Modeset Required for {}: {}".format(port_name, is_pipe_joiner_required))
        return is_pipe_joiner_required, no_of_pipe_required

    ##
    # @brief        Get DownScale Amount considering max down scaling
    # @param[in]    pixel_clock - calculated pixel clock (in MHz)
    # @param[in]    is_custom_scaling_applied - Pass True if custom scaling is applied, False otherwise
    # @return       pixel_clock - Calculated pixel clock
    @classmethod
    def get_calculated_pixel_clock(cls, pixel_clock: float, is_custom_scaling_applied: bool = False):
        # Todo: Implement Custom Scaling Verification. VSDI-28480
        # display_config_ = display_config.DisplayConfiguration()
        # display_timings = display_config_.get_display_timings(target_id)
        # logging.debug(f"Current Display Timings for {target_id}: {display_timings}")

        if is_custom_scaling_applied is True:
            # Implementation Reference: https://gfxspecs.intel.com/Predator/Home/Index/49199
            # This is an Obsolete sequence.
            pixel_clock = pixel_clock * 1000
            pixel_clock *= MAX_DOWNSCALING_FACTOR
            pixel_clock = floor(pixel_clock / 1000)

        return pixel_clock

    ##
    # @brief function to find the Symbol Frequency for HDMI
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_hdmi_symbol_freq(self, display_port, gfx_index='gfx_0'):
        disp_base = display_base.DisplayBase(display_port)
        pipe, ddi = disp_base.GetPipeDDIAttachedToPort(display_port)
        pipe = pipe.split('_')[-1].upper()
        reg_value = self.clock_register_read('TRANS_DDI_FUNC_CTL_REGISTER', 'TRANS_DDI_FUNC_CTL_' + pipe, gfx_index)
        bit_per_color_value = self.get_value_by_range(reg_value, 20, 22, self.trans_ddi_func_ctl_bit_per_color,
                                                      'Bits Per Color')
        reg_value = self.clock_register_read('PIPE_MISC_REGISTER', 'PIPE_MISC_' + pipe, gfx_index)
        color_format_value = str(self.get_value_by_range(reg_value, 27, 27, self.pipe_misc_color_format,
                                                         'Color Format')) + '_' + str(bit_per_color_value)
        color_multiplier = list(self.colorFormatDictionary.values())[
            list(self.colorFormatDictionary).index(color_format_value)]

        pixel_rate = self.get_pixel_rate(display_port, gfx_index)
        logging.info("Pixel rate: {0} , Bits per color value: {1}".format(pixel_rate, bit_per_color_value))
        symbol_freq = (pixel_rate * color_multiplier)
        return symbol_freq

    ##
    # @brief        Check if intermediate CD clock is supported (Specific to RPL-P SKUs)
    # @details      This helper is only meant for RPL-U SKUs to check CPU type - ES/QS part.
    #               RCR ID: https://jira.devtools.intel.com/browse/VPMG-11814
    #               Ref: https://hsdes.intel.com/appstore/article/#/14017568024
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @return       support: bool
    #                   returns True if 480MHz CD clock frequency is supported, False otherwise
    @staticmethod
    def is_480_mhz_supported(gfx_index: str) -> bool:
        support = False
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        if adapter_info.deviceID in ['A7A1', 'A721', 'A7A9']:
            cpu_brand_str = machine_info.SystemInfo().get_cpu_brand_string()
            logging.debug(f"CPU Brand string={cpu_brand_str}")
            if 'Genuine Intel' not in cpu_brand_str:
                support = True
        return support

    ##
    # @brief        Gets current sampling mode
    # @param[in]    display_port - Display port for which sampling mode to be fetched.
    # @param[in]    gfx_index - Graphics index
    # @return       deep_color_info_obj.overrideEncodingFormat,
    #               deep_color_info_obj.overrideBpcValue  - Calculated pixel clock and bpc
    @classmethod
    def get_bpc_encoding(cls, display_port: str, gfx_index: str) -> Tuple[int, int, bool]:
        display_config_ = display_config.DisplayConfiguration()
        display_and_adapter_info = display_config_.get_display_and_adapter_info_ex(display_port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]
        deep_color_info_obj = CuiDeepColorInfo()
        deep_color_info_obj.display_id = display_and_adapter_info.TargetID

        ##
        # Get escape call
        status, deep_color_info_obj = driver_escape.get_set_output_format(display_and_adapter_info, deep_color_info_obj)
        if deep_color_info_obj.overrideEncodingFormat is None:
            status = False
            gdhm.report_test_bug_os(title=f'[Display_Engine][color] Failed to fetch encoding format!')
            return 0, 0, status
        elif deep_color_info_obj.overrideBpcValue is None:
            status = False
            gdhm.report_test_bug_os(title=f'[Display_Engine][color] Failed to get BPC value!')
            return 0, 0, status

        return deep_color_info_obj.overrideEncodingFormat, deep_color_info_obj.overrideBpcValue, status

    ##
    # @brief        Helper method to fetch reference clock from register
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       reference_clock - Reference clock value
    def get_reference_clock_from_register(self, gfx_index: str) -> float:
        reference_clock = 0
        offset, reg_value = None, 0
        platform = ClockHelper.get_platform_name(gfx_index)
        if platform in self.GEN_14_PLATFORMS:
            offset = Gen14PllRegs.OFFSET_DSSM.DSSM
            value = DisplayArgs.read_register(offset, gfx_index)
            reg_value = Gen14PllRegs.REG_DSSM(offset, value)
        elif platform in self.GEN_15_PLATFORMS + self.GEN_16_PLATFORMS + self.GEN_17_PLATFORMS:
            offset = Gen15PllRegs.OFFSET_DSSM.DSSM
            value = DisplayArgs.read_register(offset, gfx_index)
            reg_value = Gen15PllRegs.REG_DSSM(offset, value)
        if offset is None:
            gdhm.report_test_bug_pc(title=f'[Interfaces][Display_Engine][CD Clock] Failed to fetch DSSM offset')
            logging.error(f"Failed to get reference clock from DSSM register for {platform}")
            return reg_value

        reference_freq = reg_value.ReferenceFrequency

        # B-Spec defines DSSM register to be programmed with value 2 (=38.4 MHz) for reference freq bit
        if reference_freq in self.reference_clock[platform].keys():
            reference_clock = self.reference_clock[platform][reference_freq]

        return reference_clock

    ##
    # @brief        This method returns platform name
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       platform_name - name of the platform EX: TGL, ADLP
    @staticmethod
    def get_platform_name(gfx_index: str) -> str:
        machine_info_ = machine_info.SystemInfo()
        gfx_display_hwinfo = machine_info_.get_gfx_display_hardwareinfo()
        # call get_gfx_display_hardwareinfo to get the platform type from system_info
        platform_name = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName
        logging.debug(f"Platform name for {gfx_index} : {platform_name}")
        return platform_name
