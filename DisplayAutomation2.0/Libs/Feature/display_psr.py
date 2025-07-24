#####################################################################################################################
# @file     display_psr.py
# @brief    Python wrapper helper module providing psr verification
# @author   Vinod D S
#####################################################################################################################

import configparser
import datetime
import logging
import os
import re
import subprocess
import time
from enum import Enum, IntEnum

from Libs.Core import display_power , driver_escape, registry_access
from Libs.Core import enum as custom_enum
from Libs.Core import winkb_helper
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature import socwatch

from registers.mmioregister import MMIORegister

##
# List of PSR Feature Driver Versions
class DriverPsrVersion(IntEnum):
    NONE = 0
    PSR_1 = 1
    PSR_2 = 2


##
# eDP DPCD Revision
class EdpDpcdRevision(IntEnum):
    REV_1_1_OR_LOWER = 0
    REV_1_2 = 1
    REV_1_3 = 2
    REV_1_4 = 3
    REV_1_4A = 4
    REV_1_4B = 5
    REV_1_5 = 6
    REV_RESERVED = 7


##
# List of PSR Feature Panel Versions
class PanelPsrVersion(IntEnum):
    NONE = 0
    VER_1 = 1
    VER_2 = 2
    VER_3 = 3
    VER_4 = 4
    VER_RESERVED = 5


##
# PSR Event Type
class PsrEventType(Enum):
    DEFAULT = 0
    CURSOR_MOVE = 1
    CURSOR_CHANGE = 2
    KEY_PRESS = 3
    NOTHING = 4


##
# PSR Registry Entries
class PsrRegistryEntry(Enum):
    FEATURE_TEST_CONTROL = 0
    PSR2_DISABLE = 1
    PSR_DISABLE_IN_AC = 2
    PSR_DEBUG_CTRL = 3
    PSR2_DRRS_ENABLE = 4
    VRR_ADAPTIVE_VSYNC_ENABLE = 5
    SEAMLESS_DRRS_ENABLE = 6
    STATIC_DRRS_ENABLE = 7


##
# LRR sequence Entries
class LRRSequence(Enum):
    PSR2_DISABLE = 0
    LRR_ENTRY = 1
    PSR2_ENABLE = 2
    LRR_EXIT = 3


DC_STATE_COUNTERS_DICT = {
    'APL': [0x80038],
    'GLK': [0x80030],
    'ICLHP': [0x101084, 0x101088],
    'Platform_None': [0x80030, 0x8002C]  # Default for rest GEN - SKL, KBL
}

# PSR setup time in Micro secs
PSR_SETUP_TIME = {
    0: 330,
    1: 275,
    2: 220,
    3: 165,
    4: 110,
    5: 55,
    6: 0
}


##
# @brief DisplayPsr
class DisplayPsr:
    # External path variables used
    __SOC_WATCH_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "SocWatch")
    __PSR_UTIL_PATH = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "psrutil.exe")
    __PSR_CONFIG_PATH = os.path.join(test_context.ROOT_FOLDER, "Libs\\Feature\\psr_config.ini")
    __FRAME_UPDATE_PATH = os.path.join(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PowerCons"),
                                       "FrameUpdate.exe")

    # Minimum test duration
    __MIN_TEST_DURATION_IN_SECONDS = 20

    # PSR1 registers
    __PSR1_CTRL_REG = 0x6F800
    __PSR1_STAT_REG = 0x6F840
    __PSR1_PERF_CNT_REG = 0x6F844

    # PSR2 registers
    __PSR2_CTRL_REG = 0x6F900
    __PSR2_STAT_REG = 0x6F940
    __PSR2_PERF_CNT_REG = 0x45560  # Valid only from ICL onwards
    __PSR2_PERF_CNT_CTRL = 0x45550

    # PSR DPCD Offsets
    __DPCD_EDP_REV_ADDR = 0x00700
    __DPCD_PSRCAPS_SUPPORT_VER = 0x00070
    __DPCD_AUX_FRAMESYNC_SUPPORT = 0x0007F
    __DPCD_PR_CAPS_SUPPORT = 0x000B0

    # DC5 DC6 register
    __DC5_DC6_REG = 0x45504
    __TRANS_LINKM1_EDP = 0x6F040

    # LP7 Register
    __PLANE_WM_1_A_7_ADDR_D10 = 0x7025C

    driver_interface_ = driver_interface.DriverInterface()
    display_config = display_config.DisplayConfiguration()
    display_power = display_power.DisplayPower()

    psr_entry_count = 0
    psr_perf_count = 0
    socwatch_check = -1
    lrr_check = False
    rr_list = []
    edp_target_id = None
    power_line_status = None
    l_entry = l_exit = 0
    platform = None

    def __init__(self):
        # Get Platform type using System info library
        gfx_display_hwinfo = machine_info.SystemInfo().get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = gfx_display_hwinfo[i].DisplayAdapterName
            break

        ##
        # Get CS Supported system information
        self.is_cs_supported = self.display_power.is_power_state_supported(display_power.PowerEvent.CS)

    ##
    # @brief Bits extract
    # @param[in] num
    # @param[in] lsb
    # @param[in] msb
    # @return value
    def __extract_bits_value(self, num, lsb, msb):
        if lsb > msb:
            return 0
        if lsb < 0 or msb > 31:
            return num

        value = (num & ((1 << (msb + 1)) - 1)) >> lsb
        return value

    ##
    # @brief Read count
    # @param[in] file_name
    # @return count
    def __read_count(self, file_name):
        count = 0
        full_file_name = os.path.join(test_context.TestContext.bin_store(), file_name)
        os.path.isfile(full_file_name)
        fo = open(full_file_name, "r")
        first_line = fo.readline()
        regex = r"\w+:(\d+)"
        p = re.compile(regex)
        match = p.search(first_line)
        fo.close()
        if match:
            count = match.group(1)
        return int(count)

    ##
    # @brief API for getting the psr feature caps in the eDP panel.
    #
    # Get the psr feature caps in the eDP panel.
    #
    # @param[in] self is object of DisplayPsr class
    # @param[in] enumerated_displays is displays enumerated (optional)
    # @return tuple (ret_value, edp_dpcd_rev, psr_version, is_aux_frame_sync_supported)
    def __get_psr_capability_from_panel(self, enumerated_displays=None, edp_port='DP_A'):
        ret_value = True
        edp_dpcd_rev = EdpDpcdRevision.REV_1_1_OR_LOWER
        psr_version = PanelPsrVersion.NONE
        is_aux_frame_sync_supported = False
        if enumerated_displays is None:
            enumerated_displays = self.display_config.get_enumerated_display_info()
        edp_target_id = self.display_config.get_target_id(edp_port, enumerated_displays)

        if edp_target_id == 0:
            logging.error("eDP Target ID is ZERO (0)")
            return False, edp_dpcd_rev, psr_version, is_aux_frame_sync_supported
        count = 0
        # Retry for 5 times in case of DPCD read failure
        while (count < 5):
            dpcd_flag, reg_value = driver_escape.read_dpcd(edp_target_id, self.__DPCD_EDP_REV_ADDR)
            if dpcd_flag and reg_value[0]:
                edp_dpcd_rev = EdpDpcdRevision(reg_value[0]) if (reg_value[0] <= 6) else EdpDpcdRevision.REV_RESERVED
                ret_value = True
                break
            else:
                ret_value = False
                logging.error("Reading DPCD offset %s failed" % hex(self.__DPCD_EDP_REV_ADDR))
                count += 1

        dpcd_flag, reg_value = driver_escape.read_dpcd(edp_target_id, self.__DPCD_PSRCAPS_SUPPORT_VER)
        if dpcd_flag:
            psr_version = PanelPsrVersion(reg_value[0]) if (reg_value[0] <= 4) else PanelPsrVersion.VER_RESERVED
        else:
            ret_value = False
            logging.error("Reading DPCD offset %s failed" % hex(self.__DPCD_PSRCAPS_SUPPORT_VER))

        if (edp_dpcd_rev > EdpDpcdRevision.REV_1_3) and (psr_version > PanelPsrVersion.VER_1):
            dpcd_flag, reg_value = driver_escape.read_dpcd(edp_target_id, self.__DPCD_AUX_FRAMESYNC_SUPPORT)
            if dpcd_flag:
                is_aux_frame_sync_supported = True if (reg_value[0] & 0x01) == 0x01 else False
            else:
                ret_value = False
                logging.error("Reading DPCD offset %s failed" % hex(self.__DPCD_AUX_FRAMESYNC_SUPPORT))

        return ret_value, edp_dpcd_rev, psr_version, is_aux_frame_sync_supported

    ##
    # @brief            Checks PSR supported in Panel
    # @param[in]        psr_version_under_testing
    # @param[in]        enumerated_displays
    # @param[in]        edp_port
    # @return           Bool
    def is_psr_supported_in_panel(self, psr_version_under_testing, enumerated_displays=None, edp_port='DP_A'):
        ret_val = False
        try:
            logging.info("Launching FullFrame update App ")
            frame_update = subprocess.Popen(self.__FRAME_UPDATE_PATH)
            time.sleep(1)
            ret_val, edp_dpcd_rev, psr_version, frame_sync_sup = self.__get_psr_capability_from_panel(
                enumerated_displays, edp_port)
            frame_update.kill()
            logging.info(" Successfully Closed FullFrame Update App")
        except Exception as e:
            logging.error(e)
            return False
        if not ret_val:
            logging.error("Getting PSR capability from panel failed")
            return False
        logging.info(" EDP_DPCD rev : {0} PSR version : {1}".format(edp_dpcd_rev.name, psr_version.name))
        if psr_version_under_testing == DriverPsrVersion.PSR_1:
            if (edp_dpcd_rev < EdpDpcdRevision.REV_1_3) or (psr_version < PanelPsrVersion.VER_1):
                return False
        elif psr_version_under_testing == DriverPsrVersion.PSR_2:
            if (edp_dpcd_rev < EdpDpcdRevision.REV_1_4) or (psr_version < PanelPsrVersion.VER_2):
                return False
        else:
            return False
        return True

    ##
    # @brief            Checks PR supported in Panel
    # @param[in]        enumerated_displays
    # @param[in]        edp_port
    # @return           Bool
    def is_pr_supported_in_panel(self, enumerated_displays=None, edp_port='DP_A'):
        ret_val, pr_supported = False, False
        count = 0
        if enumerated_displays is None:
            enumerated_displays = self.display_config.get_enumerated_display_info()
        edp_target_id = self.display_config.get_target_id(edp_port, enumerated_displays)

        if edp_target_id == 0:
            logging.error("eDP Target ID is ZERO (0)")
            return None
        try:
            logging.info("Launching FullFrame update App ")
            frame_update = subprocess.Popen(self.__FRAME_UPDATE_PATH)
            time.sleep(1)
            # Retry for 5 times in case of DPCD read failure
            while (count < 5):
                dpcd_flag, reg_value = driver_escape.read_dpcd(edp_target_id, self.__DPCD_PR_CAPS_SUPPORT)
                if dpcd_flag:
                    pr_supported = reg_value[0] & 0x1 == 0x1
                    logging.info(f"PR supported on {edp_port} = {pr_supported}")
                    ret_val = True
                    break
                else:
                    logging.error(f"Reading DPCD offset {hex(self.__DPCD_PR_CAPS_SUPPORT)} failed on {edp_port}")
                    count += 1
            frame_update.kill()
            logging.info(" Successfully Closed FullFrame Update App")
        except Exception as e:
            logging.error(e)
            return False
        if not ret_val:
            logging.error("Getting PR capability from panel failed")
            return False
        return pr_supported

    ##
    # @brief            Checks AUX frame sync required
    # @param[in]        enumerated_displays
    # @return           Bool
    def is_aux_frame_sync_required(self, enumerated_displays=None):
        ret_val, edp_dpcd_rev, psr_version, frame_sync_sup = self.__get_psr_capability_from_panel(enumerated_displays)

        if not ret_val:
            logging.error("Getting PSR capability from panel failed")
            return False

        return (edp_dpcd_rev > EdpDpcdRevision.REV_1_3) and (psr_version > PanelPsrVersion.VER_1) and frame_sync_sup

    ##
    # @brief API for getting the psr feature status in the driver.
    #
    # Get the psr feature status in the driver.
    #
    # @param[in] self is object of DisplayPower class
    # @param[in] psr_version_under_testing is the feature to be queried
    # @return returns True if specified feature is enabled, otherwise False
    def is_psr_feature_enabled_in_driver(self, psr_version_under_testing):
        if psr_version_under_testing == DriverPsrVersion.NONE:
            return False

        offset = self.__PSR1_CTRL_REG if psr_version_under_testing == DriverPsrVersion.PSR_1 else self.__PSR2_CTRL_REG
        psr_result = []
        status = False
        # Max Try 5 times to check PSR enable status
        for i in range(5):
            reg_value = self.driver_interface_.mmio_read(offset, 'gfx_0')
            logging.debug(" PSR {} register offset {} value {} ".format(psr_version_under_testing, offset, reg_value))
            if (self.__extract_bits_value(reg_value, 31, 31)) == 1:
                psr_result.append('Enabled')
                status = True
                break
            time.sleep(1)
            psr_result.append('Disabled')
        logging.debug("PSR status re-tries --> {}".format(psr_result))

        return status

    ##
    # @brief  Check whether DMC is enabled
    # @return Bool
    def is_perf_count_check_possible(self):

        winkb_helper.press('WIN+M')  # Everything is minimized
        time.sleep(2)  # Breather for above event

        if self.driver_interface_.mmio_read(self.__DC5_DC6_REG, 'gfx_0') == 0xFFFFFFFF:  # Hit DC9 state
            return False

        ##
        # If DC state counter is explicitly defined in dictionary, then return that
        dc_state_counters = DC_STATE_COUNTERS_DICT['Platform_None']
        if self.platform in DC_STATE_COUNTERS_DICT.keys():
            dc_state_counters = DC_STATE_COUNTERS_DICT[self.platform]

        counter_val1 = 0
        for counter in dc_state_counters:
            counter_val1 += self.driver_interface_.mmio_read(counter, 'gfx_0')

        time.sleep(self.__MIN_TEST_DURATION_IN_SECONDS)

        counter_val2 = 0
        for counter in dc_state_counters:
            counter_val2 += self.driver_interface_.mmio_read(counter, 'gfx_0')

        winkb_helper.press('SHIFT+WIN+M')  # Everything is undo-minimized
        if counter_val1 != counter_val2:  # Hit DC5/ DC6
            return False

        return True

    ##
    #
    # @brief            Modify the registry key to enable or disable the feature
    # @param[in]        reg_key_type - Type of the registry key of type PsrRegistryEntry
    # @param[in]        enable_reg_key - To enable the feature or disable
    # @return           bool - whether the setting psr reg key operation success of not
    def set_psr_regkey(self, reg_key_type, enable_reg_key):

        key_name = None
        value = 0x0
        feature_str = ""
        reg_args = registry_access.StateSeparationRegArgs("gfx_0")

        if reg_key_type == PsrRegistryEntry.FEATURE_TEST_CONTROL:
            key_name = "FeatureTestControl"
            value_data, _ = registry_access.read(args=reg_args, reg_name=key_name)
            value = (value_data & ~(1 << 11)) if enable_reg_key else (value_data | (1 << 11))
            feature_str = "PSR Enable"
        elif reg_key_type == PsrRegistryEntry.PSR2_DISABLE:
            key_name = "PSR2Disable"
            value = 0x1 if enable_reg_key else 0x0
            feature_str = "PSR2 Disable"
        elif reg_key_type == PsrRegistryEntry.PSR_DISABLE_IN_AC:
            key_name = "PsrDisableInAc"
            value = 0x1 if enable_reg_key else 0x0
            feature_str = "PSR Disable in AC"
        elif reg_key_type == PsrRegistryEntry.PSR_DEBUG_CTRL:
            key_name = "PSRDebugCtrl"
            value = 0x10  # 0x11?
            feature_str = "GTC Enable"
        elif reg_key_type == PsrRegistryEntry.PSR2_DRRS_ENABLE:
            key_name = "PSR2DrrsEnable"
            value = 0x1 if enable_reg_key else 0x0
            feature_str = "LRR Enable"
        elif reg_key_type == PsrRegistryEntry.VRR_ADAPTIVE_VSYNC_ENABLE:
            key_name = "AdaptiveVsyncEnable"
            value = 0x1 if enable_reg_key else 0x0
            feature_str = "VRR Enable"
        elif reg_key_type == PsrRegistryEntry.SEAMLESS_DRRS_ENABLE:
            key_name = "Display1_DPSPanel_Type"
            value = 0x2
            feature_str = "Seamless DRRS panel type"
        elif reg_key_type == PsrRegistryEntry.STATIC_DRRS_ENABLE:
            key_name = "Display1_DPSPanel_Type"
            value = 0x1
            feature_str = "Static DRRS panel type"

        if key_name is None:
            logging.error("INVALID reg_key specified")
            return False

        logging.info("Setting {0} to {1} (RegKey = {2})".format(feature_str, enable_reg_key, key_name))

        if registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                 reg_value=value) is False:
            logging.error("\tModifying \"{0}\" registry key FAILED".format(key_name))
            return False

        logging.info("\tModifying \"{0}\" registry key successful".format(key_name))
        return True

    ##
    # @brief PSR1 logger
    # @param[in] duration_in_seconds
    # @param[in] p_util
    # @param[in] msb
    # @return None
    def __psr1_logger(self, duration_in_seconds, p_util=None):
        prev_psr1_stat = 7
        prev_link_status = 2
        psr1_reg_value = 0
        cur_psr1_stat = 0
        cur_link_status = 0

        self.psr_entry_count = 0

        current_time = datetime.datetime.now()
        target_time = current_time + datetime.timedelta(seconds=duration_in_seconds)

        while (current_time <= target_time and p_util is None) or (p_util is not None and p_util.poll() is None):
            psr1_reg_value = self.driver_interface_.mmio_read(self.__PSR1_STAT_REG, 'gfx_0')

            cur_psr1_stat = self.__extract_bits_value(psr1_reg_value, 29, 31)
            cur_link_status = self.__extract_bits_value(psr1_reg_value, 26, 27)

            if cur_psr1_stat != prev_psr1_stat:
                if cur_psr1_stat == 0:  # Psr1_state = IDLE(Reset state)
                    pass
                elif cur_psr1_stat == 1:  # Psr1_state = SRDONACK
                    # (Wait for TG / Stream to send on frame of data after SRD conditions are met)
                    pass
                elif cur_psr1_stat == 2:  # Psr1_state = SRDENT(SRD entry)
                    self.psr_entry_count += 1
                elif cur_psr1_stat == 3:  # Psr1_state = BUFOFF(Wait for buffer turn off - transcoder EDP only)
                    pass
                elif cur_psr1_stat == 4:  # Psr1_state = BUFON(Wait for buffer turn on - transcoder EDP only)
                    pass
                elif cur_psr1_stat == 5:  # Psr1_state = AUXACK
                    # (Wait for AUX to acknowledge on SRD exit - transcoder EDP only)
                    pass
                elif cur_psr1_stat == 6:  # Psr1_state = SRDOFFACK(Wait for TG / Stream to acknowledge the SRD VDM exit)
                    pass
                else:  # Psr1_state = Reserved(Wrong State)
                    pass
                prev_psr1_stat = cur_psr1_stat

            if cur_link_status != prev_link_status:
                if cur_link_status == 0:  # Link_status = Link is Full Off
                    pass
                elif cur_link_status == 1:  # Link_status = Link is Full On
                    pass
                elif cur_link_status == 2:  # Link_status = Link is In Standby
                    pass
                else:  # Link_status = Reserved(Wrong State)
                    pass
                prev_link_status = cur_link_status

            time.sleep(1 / 17.0)
            current_time = datetime.datetime.now()

    ##
    # @brief PSR2 logger
    # @param[in] duration_in_seconds
    # @param[in] p_util
    # @param[in] msb
    # @return None
    def __psr2_logger(self, duration_in_seconds, p_util=None):
        prev_psr2_stat = 15
        prev_link_status = 2
        psr2_reg_value = 0
        cur_psr2_stat = 0
        cur_link_status = 0
        curr_psr2 = prev_psr2 = seq_check = False
        prev_rr = 0
        lrr_entry = [[LRRSequence.PSR2_DISABLE, LRRSequence.LRR_ENTRY, LRRSequence.PSR2_ENABLE],
                     [LRRSequence.PSR2_DISABLE, LRRSequence.LRR_ENTRY, LRRSequence.LRR_EXIT, LRRSequence.PSR2_ENABLE]]
        lrr_exit = [[LRRSequence.PSR2_DISABLE, LRRSequence.LRR_EXIT, LRRSequence.PSR2_ENABLE],
                    [LRRSequence.PSR2_DISABLE, LRRSequence.LRR_EXIT, LRRSequence.LRR_ENTRY, LRRSequence.PSR2_ENABLE]]
        psr2_disable_enable_seq = [LRRSequence.PSR2_DISABLE, LRRSequence.PSR2_ENABLE]
        lst = []
        mode = self.display_config.get_current_mode(self.edp_target_id)
        curr_rr = mode.refreshRate
        ratio = 1.0
        self.psr_entry_count = 0

        if self.lrr_check and self.power_line_status == display_power.PowerSource.DC:
            trans_linkm1_value1 = self.driver_interface_.mmio_read(self.__TRANS_LINKM1_EDP, 'gfx_0') & 0x00FFFFFF
            ratio = trans_linkm1_value1 / curr_rr  # Calculate the ratio with M1/RR1

        current_time = datetime.datetime.now()
        target_time = current_time + datetime.timedelta(seconds=duration_in_seconds)

        while (current_time <= target_time and p_util is None) or (p_util is not None and p_util.poll() is None):
            if self.lrr_check and self.power_line_status == display_power.PowerSource.DC:
                psr2_reg = self.driver_interface_.mmio_read(self.__PSR2_CTRL_REG, 'gfx_0')
                curr_psr2 = True if ((self.__extract_bits_value(psr2_reg, 28, 31)) & 0x8) else False

                trans_linkm1_value2 = self.driver_interface_.mmio_read(self.__TRANS_LINKM1_EDP, 'gfx_0') & 0x00FFFFFF
                curr_rr = trans_linkm1_value2 / ratio

                if curr_psr2 != prev_psr2:
                    if not curr_psr2:
                        seq_check = True
                        if seq_check:
                            lst.append(LRRSequence.PSR2_DISABLE)
                    elif curr_psr2:
                        if seq_check:
                            lst.append(LRRSequence.PSR2_ENABLE)
                    prev_psr2 = curr_psr2

                if curr_rr != prev_rr:
                    if curr_rr == max(self.rr_list):
                        if seq_check:
                            lst.append(LRRSequence.LRR_ENTRY)
                    else:
                        if seq_check:
                            lst.append(LRRSequence.LRR_EXIT)
                    prev_rr = curr_rr

                if (len(lst) == 3) or (len(lst) == 4):
                    if lst in lrr_entry:
                        self.l_entry += 1
                        lst = []
                    elif lst in lrr_exit:
                        self.l_exit += 1
                        lst = []
                elif len(lst) == 2:
                    if lst == psr2_disable_enable_seq:
                        lst = []

            psr2_reg_value = self.driver_interface_.mmio_read(self.__PSR2_STAT_REG, 'gfx_0')
            cur_psr2_stat = self.__extract_bits_value(psr2_reg_value, 28, 31)
            cur_link_status = self.__extract_bits_value(psr2_reg_value, 26, 27)

            if cur_psr2_stat != prev_psr2_stat:
                if cur_psr2_stat == 0:  # PSR2_state = IDLE (Reset state)
                    pass
                elif cur_psr2_stat == 1:  # PSR2_state = CAPTURE (Send capture frame)
                    pass
                elif cur_psr2_stat == 2:  # PSR2_state = CPTURE_FS (Fast sleep after capture frame is sent)
                    pass
                elif cur_psr2_stat == 3:  # PSR2_state = SLEEP (Selective Update)
                    pass
                elif cur_psr2_stat == 4:  # PSR2_state = BUFON_FW (Turn Buffer on and Send Fast wake)
                    pass
                elif cur_psr2_stat == 5:  # PSR2_state = ML_UP (Turn Main link up and send SR)
                    pass
                elif cur_psr2_stat == 6:  # PSR2_state = SU_STANDBY (Selective update or Standby state)
                    pass
                elif cur_psr2_stat == 7:  # PSR2_state = FAST_SLEEP (Send Fast sleep)
                    pass
                elif cur_psr2_stat == 8:  # PSR2_state = DEEP_SLEEP (Enter Deep sleep)
                    self.psr_entry_count += 1
                elif cur_psr2_stat == 9:  # PSR2_state = BUF_ON (Turn ON IO Buffer)
                    pass
                elif cur_psr2_stat == 10:  # PSR2_state = TG_ON (Turn ON Timing Generator)
                    pass
                else:  # PSR2_state = Reserved (Wrong State)
                    pass
                prev_psr2_stat = cur_psr2_stat

            if cur_link_status != prev_link_status:
                if cur_link_status == 0:  # Link_status = Link is Full Off
                    pass
                elif cur_link_status == 1:  # Link_status = Link is Full On
                    pass
                elif cur_link_status == 2:  # Link_status = Link is In Standby
                    pass
                else:  # Link_status = Reserved(Wrong State)
                    pass
                prev_link_status = cur_link_status

            time.sleep(1 / 70.0)
            current_time = datetime.datetime.now()

    ##
    # @brief __check_psr_with_util_app
    # @param[in] psr_version_under_testing
    # @param[in] event_type
    # @param[in] edp_position
    # @param[in] duration
    # @return None
    def __check_psr_with_util_app(self, psr_version_under_testing, event_type, edp_position, duration):

        cmd_line = "%s c:clock d:%s x:300 y:200" % (self.__PSR_UTIL_PATH, edp_position)
        if event_type == PsrEventType.CURSOR_MOVE:
            cmd_line = "%s c:cursormove d:%s" % (self.__PSR_UTIL_PATH, edp_position)
        elif event_type == PsrEventType.CURSOR_CHANGE:
            cmd_line = "%s c:cursorchange d:%s x:300 y:200 n:50" % (self.__PSR_UTIL_PATH, edp_position)
        elif event_type == PsrEventType.KEY_PRESS:
            cmd_line = "%s c:keypress d:%s t:%s" % (self.__PSR_UTIL_PATH, edp_position, duration)

        p_util = None
        if event_type != PsrEventType.NOTHING:
            p_util = subprocess.Popen(cmd_line)

        time.sleep(3)  # Breather for the app which is just launched
        second_arg = p_util if (event_type == PsrEventType.CURSOR_CHANGE or event_type == PsrEventType.KEY_PRESS) \
            else None

        if psr_version_under_testing == DriverPsrVersion.PSR_1:
            self.__psr1_logger(duration, second_arg)
        elif psr_version_under_testing == DriverPsrVersion.PSR_2:
            self.__psr2_logger(duration, second_arg)

        if event_type != PsrEventType.NOTHING:
            p_util.terminate()

    ##
    # @brief API for checking that whether PSR is actually working or not by getting PSR entry count.
    #
    # Check that whether PSR is actually working or not by getting PSR entry count.
    #
    # @param[in] self is object of DisplayPower class
    # @param[in] psr_version_under_testing is the PSR version to be specified
    # @param[in] event_type is the event type should be used for the testing
    # @param[in] edp_position is position of the edp in display config (0 for SINGLE/CLONE, or index for EXTENDED)
    # @param[in] duration is the time for how long the test must run (in seconds)
    # @return actual and required psr entry count
    def check_psr_entry_count(self, psr_version_under_testing, event_type, edp_position, duration):

        if duration < self.__MIN_TEST_DURATION_IN_SECONDS:
            duration = self.__MIN_TEST_DURATION_IN_SECONDS

        if not os.path.exists(self.__PSR_UTIL_PATH):
            logging.error("%s does not exist" % self.__PSR_UTIL_PATH)
            return 0, 0

        if not self.is_psr_supported_in_panel(psr_version_under_testing):
            logging.error("%s not supported in the panel" % DriverPsrVersion(psr_version_under_testing).name)
            return 0, 0

        if not self.is_psr_feature_enabled_in_driver(psr_version_under_testing):
            if not self.lrr_check:
                logging.error("PSR is not enabled in driver")
                return 0, 0

        self.__check_psr_with_util_app(psr_version_under_testing, event_type, edp_position, duration)

        actual_psr_entry_count = self.psr_entry_count
        required_psr_entry_count = duration - 5

        if event_type == PsrEventType.CURSOR_MOVE:
            read_count = self.__read_count(os.path.join(test_context.TestContext.root_folder(), "cursormove.tmp"))
            if read_count == 0:
                read_count = int(duration * 0.8)
            required_psr_entry_count = int(read_count * 0.8)
        elif event_type == PsrEventType.CURSOR_CHANGE:
            read_count = self.__read_count(os.path.join(test_context.TestContext.root_folder(), "cursorchange.tmp"))
            if read_count == 0:
                read_count = int(duration * 0.8)
            required_psr_entry_count = int(read_count * 0.8)
        elif event_type == PsrEventType.KEY_PRESS:
            read_count = self.__read_count(os.path.join(test_context.TestContext.root_folder(), "keypress.tmp"))
            if read_count == 0:
                read_count = int(duration * 0.8)
            required_psr_entry_count = int(read_count * 0.8)
        elif event_type == PsrEventType.NOTHING:
            # When event type is 'nothing', requiredEntryCount cannot be decided here.
            # The caller has to take care of success or failure criteria
            required_psr_entry_count = 0

        return actual_psr_entry_count, required_psr_entry_count

    ##
    # @brief API for checking that whether PSR is actually working or not by getting PSR perf count.
    #
    # Check that whether PSR is actually working or not by getting PSR perf count.
    #
    # @param[in] self is object of DisplayPsr class
    # @param[in] psr_version_under_testing is the PSR version to be specified
    # @param[in] duration is the time for how long the test must run
    # @return psr perf count
    def check_psr_perf_count(self, psr_version_under_testing, duration):

        if duration < self.__MIN_TEST_DURATION_IN_SECONDS:
            duration = self.__MIN_TEST_DURATION_IN_SECONDS

        self.psr_perf_count = 0

        psr_perf_reg_offset = self.__PSR1_PERF_CNT_REG if psr_version_under_testing == DriverPsrVersion.PSR_1 \
            else self.__PSR2_PERF_CNT_REG

        if psr_version_under_testing == DriverPsrVersion.PSR_2 and self.platform in ['ICL', 'ICLHP', 'ICLLP', 'LKF1',
                                                                                     'CFL', 'TGL', 'JSL', 'RYF', 'DG1',
                                                                                     'RKL', 'LKFR']:
            reg_val = self.driver_interface_.mmio_read(self.__PSR2_PERF_CNT_CTRL, 'gfx_0')
            if (reg_val & 0x20) != 0x20:
                reg_val = reg_val | 0x20
                self.driver_interface_.mmio_write(self.__PSR2_PERF_CNT_CTRL, reg_val, 'gfx_0')

        if psr_version_under_testing == DriverPsrVersion.PSR_1 or \
                (psr_version_under_testing == DriverPsrVersion.PSR_2 and self.platform in ['ICL', 'ICLHP', 'ICLLP',
                                                                                           'LKF1', 'CFL', 'TGL', 'JSL',
                                                                                           'RYF', 'DG1', 'RKL',
                                                                                           'LKFR']):
            time.sleep(2)  # Breather time if any event done in caller function
            psr_perf_count_begin = self.driver_interface_.mmio_read(psr_perf_reg_offset, 'gfx_0')
            time.sleep(duration)
            psr_perf_count_end = self.driver_interface_.mmio_read(psr_perf_reg_offset, 'gfx_0')

            if psr_perf_count_end >= psr_perf_count_begin:
                self.psr_perf_count = psr_perf_count_end - psr_perf_count_begin
            else:
                self.psr_perf_count = (0x00FFFFFF - psr_perf_count_begin) + psr_perf_count_end

        return self.psr_perf_count

    ##
    # @brief        PSR verification mechanism using socwatch
    # @param[in]    duration
    # @return       Bool
    def get_io_bandwidth_using_socwatch(self, duration=60):
        if self.socwatch_check == -1:
            if os.path.exists(self.__PSR_CONFIG_PATH) is True:
                psr_config = configparser.ConfigParser()
                psr_config.read_file(open(self.__PSR_CONFIG_PATH))
                if psr_config.get('Config', 'SocWatch') == 'False':
                    logging.info("SocWatch check is disabled in psr_config.ini")
                    self.socwatch_check = False
                else:
                    self.socwatch_check = True
            else:
                self.socwatch_check = True

        if self.socwatch_check is False:
            logging.info("SocWatch check is disabled in psr_config.ini")
            return True, 0.0

        ret_value = True
        io_requests_bw = 0.0

        ##
        # Run SocWatch for "duration" seconds (-t duration), capture starts after 5 seconds (-s 5)
        # and polling happens for every 1000ms (--polling -n 1000)
        soc_command = "socwatch --polling -n 1000 -t %s -s 5 -f sys" % duration
        result = socwatch.run_socwatch(self.__SOC_WATCH_PATH, soc_command)
        if result:
            soc_logfile_path = os.path.join(os.getcwd(), "SOCWatchOutput.csv")
            result, soc_output = socwatch.parse_socwatch_output(soc_logfile_path)
            if result:
                io_requests_bw = soc_output[socwatch.SocWatchFields.IO_REQUESTS]
                p_state_str = ""
                for key, value in soc_output.items():
                    if "PACKAGE" in socwatch.SocWatchFields(key).name.upper():
                        p_state_str += "%s = %s, " % (socwatch.SocWatchFields(key).name, value)
                logging.debug("Package Residency: %s", p_state_str)
                logging.debug("IO Request Memory Bandwidth in PSR: %s", io_requests_bw)
            else:
                ret_value = False
                logging.error("Aborting the test as socwatch log parse is failed")
        else:
            ret_value = False
            logging.error("Aborting the test as running the socwatch failed")
        return ret_value, io_requests_bw

    ##
    # Get edp position in the current display config
    def __get_topology_and_path_index_in_current_config(self, target_id):
        topology = None
        path_index = -1
        get_cfg = self.display_config.get_current_display_configuration()
        if get_cfg.status == custom_enum.DISPLAY_CONFIG_SUCCESS:
            topology = get_cfg.topology
            for display_index in range(get_cfg.numberOfDisplays):
                if get_cfg.displayPathInfo[display_index].targetId == target_id and \
                        get_cfg.displayPathInfo[display_index].isActive:
                    path_index = get_cfg.displayPathInfo[display_index].pathIndex
        return topology, path_index

    ##
    # @brief        This is the common verification mechanism for PSR
    # @param[in]    psr_version_under_testing
    # @param[in]    psr_test_duration
    # @param[in]    perf_count_check_possible
    # @param[in]    psr_disable_io_bw
    # @param[in]    psr_event_type
    # @param[in]    psr_req_entry_count
    # @param[in]    gfx_index
    # @return       Bool
    def verify_psr(self, psr_version_under_testing, psr_test_duration, perf_count_check_possible=False,
                   psr_disable_io_bw=0, psr_event_type=PsrEventType.DEFAULT, psr_req_entry_count=0, gfx_index='gfx_0'):
        ret_val = True
        is_edp_active = False
        is_sd_edp = False
        edp_position = 0
        lrr_expected_sequence = 15
        self.power_line_status = self.display_power.get_current_powerline_status()

        enumerated_displays = self.display_config.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[display_index]
            if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex and \
                    'DP_A' in CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name:
                self.edp_target_id = int(display.TargetID)
                break

        if self.edp_target_id is not None:
            topology, edp_path_index = self.__get_topology_and_path_index_in_current_config(self.edp_target_id)
            if topology is None:
                logging.error("Getting current display configuration failed")
                return False
            if edp_path_index == -1:
                logging.info("eDP is not the active display in the current configuration")
            else:
                is_edp_active = True
                edp_position = 0 if topology != custom_enum.EXTENDED else edp_path_index
                is_sd_edp = (topology == custom_enum.SINGLE)
        else:
            logging.info("eDP is not present")

        ##
        # Querying power feature status in driver
        if ((self.platform == 'SKL' and
             ((
                      self.power_line_status == display_power.PowerSource.AC and not self.is_cs_supported) or not is_sd_edp))
                or (self.platform != 'SKL' and not is_edp_active)):

            if self.is_psr_feature_enabled_in_driver(psr_version_under_testing):
                logging.error("Feature is enabled in driver.(Not expected)")
                ret_val = False
            else:
                logging.info("Feature is disabled in driver in AC mode - NonCS system as expected")
            return ret_val

        actual_psr_entry_count, required_psr_entry_count = \
            self.check_psr_entry_count(psr_version_under_testing, psr_event_type, edp_position, psr_test_duration)

        logging.debug("PSR Entry Count = %s" % actual_psr_entry_count)
        if psr_event_type is PsrEventType.NOTHING:
            required_psr_entry_count = psr_req_entry_count

        if actual_psr_entry_count == 0:
            logging.error(
                "PSR Entry Count (expected = %s, actual = %s)" % (required_psr_entry_count, actual_psr_entry_count))
            return False
        logging.info(
            "PSR Entry Count (expected = %s, actual = %s)" % (required_psr_entry_count, actual_psr_entry_count))

        if self.lrr_check and self.power_line_status == display_power.PowerSource.DC:
            if self.l_exit < lrr_expected_sequence and self.l_entry < lrr_expected_sequence:
                logging.error("LRR sequence failed (expected 15, actual - LRR entry %s, LRR exit %s)" %
                              (self.l_entry, self.l_exit))
                return False
            logging.info("LRR sequence passed (expected 15, actual - LRR entry %s, LRR exit %s)" %
                         (self.l_entry, self.l_exit))

        skip_perf = False
        if not perf_count_check_possible:
            skip_perf = True
            logging.info("DMC is enabled, so ignoring the perf count check")
        if self.platform in ['IVB', 'HSW', 'VLV', 'BDW', 'APL', 'CHV', 'SKL', 'BXT', 'KBL', 'CNL', 'GLK', 'ICL'] and \
                psr_version_under_testing == DriverPsrVersion.PSR_2:
            skip_perf = True
            logging.info("For platforms lower than ICL, no perf count register available for PSR2")
        if not is_sd_edp:
            skip_perf = True
            logging.info("Current config is not SD eDP, so ignoring the perf count check")

        if not skip_perf:
            winkb_helper.press('WIN+M')  # Everything is minimized
            psr_perf_count = self.check_psr_perf_count(psr_version_under_testing, psr_test_duration)
            winkb_helper.press('SHIFT+WIN+M')  # Everything is undo-minimized
            logging.debug("PSR Perf Count = %s" % psr_perf_count)
            required_psr_perf_count = psr_test_duration * 1000 * 0.8  # Giving 20% buffer
            logging.info("PSR Perf Count (expected = %s, actual = %s)" % (required_psr_perf_count, psr_perf_count))

        ##
        # Check whether PSR check passed and display config is sd edp, then only go for socwatch verification
        if not ret_val:
            logging.info("PSR check failed by now, so skipping socwatch bandwidth check")
        else:
            if is_sd_edp:
                ##
                # SocWatch Bandwidth capture not supported for all platforms
                if psr_disable_io_bw == 0.0:
                    logging.info("SocWatch bandwidth capture may not be supported on this platform, so skipping..")
                else:
                    winkb_helper.press('WIN+M')  # Everything is minimized
                    ret_val, io_request_bw = self.get_io_bandwidth_using_socwatch()
                    winkb_helper.press('SHIFT+WIN+M')  # Everything is undo-minimized

                    ##
                    # Based on the platform, fine tune this value
                    if ret_val:
                        if psr_disable_io_bw > (io_request_bw * 5.0):
                            logging.info("PSR is saving the expected bandwidth (SocWatch bandwidth check passed)")
                        else:
                            ret_val = False
                            logging.error("PSR is NOT saving the expected bandwidth (SocWatch bandwidth check failed)")
                    else:
                        logging.error("Getting IO bandwidth failed")
            else:
                logging.info("Skipping socwatch bandwidth check as current config is not SD eDP")
        return ret_val

    ##
    # @brief    Function to check LRR support in connected eDP
    # @param    gfx_index
    # @return   True if Panel supports LRR else False
    def verify_lrr_supported(self, gfx_index: str = 'gfx_0'):
        ##
        # get eDP target
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[display_index]
            if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex and \
                    'DP_A' in CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name:
                self.edp_target_id = int(display.TargetID)
                break

        supported_mode_list = self.display_config.get_all_supported_modes([self.edp_target_id])
        for key, values in supported_mode_list.items():
            for mode in values:
                mode_str = mode.to_string(enumerated_displays)
                if 'MDS' in mode_str:
                    self.rr_list.append(mode.refreshRate)
        if len(self.rr_list) > 1:
            logging.info("Connected eDP panel supports LRR")
            return True
        else:
            logging.error("Connected eDP panel does not supports LRR")
            return False

    ##
    # @brief API to check whether the panel has PSR Setup Time Restriction
    # @param    gfx_index
    # @param    port
    # @param    transcoder
    # @param    platform_name
    # @return True if panel has PSR Setup Time Restriction. False if Panel doesn't have PSR Setup Time Restriction
    # None if DPCD read is failed
    def check_psr_setup_time(self, gfx_index, port, transcoder, platform_name):
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[display_index]
            if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex and \
                    port in CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name:
                panel_target_id = int(display.TargetID)
                break
        dpcd_read_status, dpcd_read_value = driver_escape.read_dpcd(panel_target_id, 0x71)
        logging.debug(f"PSR Capabilities DPCD read value : {dpcd_read_value}")
        if not dpcd_read_status:
            return None
        setup_time_key = self.__extract_bits_value(dpcd_read_value[0], 1, 3)
        logging.debug(f"Setup Time value : {setup_time_key}")
        if platform_name in machine_info.PRE_GEN_16_PLATFORMS:
            v_total = MMIORegister.read(
                'TRANS_VTOTAL_REGISTER', 'TRANS_VTOTAL_' + transcoder, platform_name, gfx_index='gfx_0')
        else:
            v_total = MMIORegister.read(
                'TRANS_VRR_VMAX_REGISTER', 'TRANS_VRR_VMAX_' + transcoder, platform_name, gfx_index='gfx_0')
        h_total = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + transcoder,
                                    platform_name, gfx_index='gfx_0')
        mode = self.display_config.get_current_mode(panel_target_id)
        # Calculate line time in micro secs
        line_time_in_us = round(((h_total.horizontal_total + 1) / float(mode.pixelClock_Hz / (1000 * 1000))), 3)
        logging.debug(f"line time in us = {line_time_in_us} us")
        vblank_time_in_us = (v_total.vertical_total - v_total.vertical_active) * line_time_in_us
        setup_time = PSR_SETUP_TIME[setup_time_key]
        if setup_time <= (vblank_time_in_us - line_time_in_us):
            logging.info(f"{port} doesn't have Setup Time Restriction")
            return False
        logging.info(f"{port} has setup time restriction")
        return True


    ##
    # @brief    API to check whether the panel has PSR VBlank and Line Time Restriction
    # @param    port Port
    # @param    transcoder Transcoder
    # @param    gfx_index Gfx Index
    # @return True if panel has Restriction. False if Panel doesn't have PSR Line Time Restriction
    def check_psr_line_time(self, port, transcoder, gfx_index):
        # line time restriction check is not applicable from LNL+
        if self.platform not in machine_info.PRE_GEN_15_PLATFORMS:
            return True
        min_block_count = 8
        max_block_count = 12
        max_line_time = 5250  # in Nano secs
        psr2_ctl_edp = MMIORegister.read(
            'PSR2_CTL_REGISTER', 'PSR2_CTL_' + transcoder, self.platform, gfx_index=gfx_index)
        vblank = MMIORegister.read(
            'TRANS_VBLANK_REGISTER', 'TRANS_VBLANK_' + transcoder, self.platform, gfx_index=gfx_index)
        h_total = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + transcoder,
                                    self.platform, gfx_index=gfx_index)
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[display_index]
            if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex and \
                    port in CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name:
                panel_target_id = int(display.TargetID)
                break
    
        mode = self.display_config.get_current_mode(panel_target_id)
        # Calculate line time in micro secs
        line_time_in_ns = round(((h_total.horizontal_total + 1) / float(mode.pixelClock_Hz / (1000 * 1000))) * 1000, 3)
        if self.platform in machine_info.GEN_11_PLATFORMS:
            min_line_time_in_ns = 6250  # in Nano secs
            block_count_lines = min_block_count
        else:
            # PSR2 requires total line time of at least 3.5us
            # Bspec - https://gfxspecs.intel.com/Predator/Home/Index/49274
            min_line_time_in_ns = 3500  # in Nano secs
            # If Line time is greater than 5.25 us, vblank should be greater than or equal to 8 lines.
            # If line time with less than 5.25 us, vblank should be greater than 12 lines.
            block_count_lines = (min_block_count if line_time_in_ns >= max_line_time else max_block_count)

        vblank_status = (vblank.vertical_blank_end - vblank.vertical_blank_start) < block_count_lines
        if vblank_status and (psr2_ctl_edp.psr2_enable == 0):
            logging.error(
                f"Required min Vblank val >=8 . Actual= {vblank.vertical_blank_end - vblank.vertical_blank_start}")
            return False
        logging.info(f"Panel : {port} doesn't have VBlank Time Restriction")

        # PSR2 will not be enabled if (TRANS_VBLANK Vertical Blank END - TRANS_VBLANK Vertical Blank START) <
        # PSR2_CTL Block Count Number value in lines
        # minimum block count of 8 lines means PSR2 requires vblank to be at least 8 scan lines
        line_time_status = (line_time_in_ns < min_line_time_in_ns)
        if line_time_status and (psr2_ctl_edp.psr2_enable == 0):
            logging.error(f"line_time Expected >= {min_line_time_in_ns} ns, Actual = {line_time_in_ns} ns")
            return False
        logging.info(f"Panel : {port} doesn't have Line Time Restriction")
        return True

