####################################################################################################
# @file     display_phy_buffer.py
# @brief    Python wrapper exposes interfaces for Display PHY Buffer Verification
# @details  display_phy_buffer.py provides interfaces to Verify Display Phy Buffer Values (Pre-Emp and Vswing)
#           for EDP, DP.
#           User-Input : DisplayDDI() instance - display_port to be verifed
#           DisplayDDI information mentioned below: \n
# @note     Supported display interfaces are EDP, DP\n
# @author   Kumar V Arun, Veluru Veena, Goutham N
##################################################################################################
import logging
import re

from Libs.Core import display_utility, driver_escape
from Libs.Core.system_utility import SystemUtility
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import driver_interface
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_engine.de_base import display_phy_buffer_utils
from Libs.Feature.display_port import dpcd_helper
from registers.mmioregister import MMIORegister
from Libs.Core.logger import gdhm

from DisplayRegs.Gen13.Ddi import Gen13DdiRegs
from DisplayRegs.Gen14 import MtlSnpsPhyRegisters
from DisplayRegs.Gen14 import ElgSnpsPhyRegisters
from DisplayRegs.Gen15 import LnlSnpsPhyRegisters
from DisplayRegs import DisplayArgs
from Libs.Feature.clock.mtl.mtl_clock_helper import MtlClockHelper
from Libs.Feature.clock.lnl.lnl_clock_helper import LnlClockHelper
from Libs.Feature.clock.elg.elg_clock_helper import ElgClockHelper


##
# @brief Class to verify Phy Buffer Verification
class DisplayPhyBuffer(display_base.DisplayBase):

    ##
    # @brief Initializes required DP Variables
    # @param[in] display_port port under verification
    # @param[in] gfx_index graphics adapter gfx_0/gfx_1
    def __init__(self, display_port=None, gfx_index='gfx_0'):
        self.display_port = display_port
        display_base.DisplayBase.__init__(self, display_port, gfx_index=gfx_index)


##
# @brief Verify Phy Buffer Values programming for the passed port list
# @param[in] phyList List of Phy Objects of type DisplayPhyBuffer()
# @param[in] vbt_override True/False based on driver/vbt tables being verified
# @param[in] gfx_vbt VBT Handle
# @param[in] gfx_index gfx adapter under verification gfx_0/gfx_1
# @return bool Return true if MMIO programming is correct, else return false
def VerifyPhyBufferProgramming(phyList, vbt_override=False, gfx_vbt=0, gfx_index='gfx_0'):
    status = True

    for phyObj in phyList:
        if phyObj.platform in display_phy_buffer_utils.supported_platform_list:
            logging.info(
                "******* Phy Buffer Verification for " + phyObj.display_port +
                " (Target ID : {0}) - {1} Connected to {2},{3} on Adapter {4} *******".format(
                    phyObj.targetId, phyObj.display_port, phyObj.pipe, phyObj.ddi, gfx_index))
            if phyObj.pipe is None:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]: {} is not connected to any Pipe".format(
                        phyObj.display_port),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    "ERROR:" + phyObj.display_port + " is NOT Connected to any Pipe. Check if it is Connected")
                return False
            if phyObj.display_port.startswith("DP"):
                status = verify_phy_buffer_per_phy(phyObj, vbt_override, gfx_vbt, gfx_index)
                if status is False:
                    return status
            else:
                logging.info("INFO: Phy Buffer Verification NOT Supported for " + phyObj.display_port)
        else:
            logging.info("Unsupported platform {0} and port {1} for phy verification".format(phyObj.platform,
                                                                                             phyObj.display_port))
    return status


##
# @brief Verify Phy Buffer Values programming for specific Port/Phy
# @param[in] phyObj Phy Object of type DisplayPhyBuffer()
# @param[in] vbt_override True/False based on driver/vbt tables being verified
# @param[in] gfx_vbt VBT Handle
# @param[in] gfx_index gfx adapter under verification gfx_0/gfx_1
# @return Bool return true if MMIO programming is correct, else return false
def verify_phy_buffer_per_phy(phyObj, vbt_override, gfx_vbt, gfx_index='gfx_0'):
    ddi = phyObj.ddi.split("_")

    for platform_id, ports in display_phy_buffer_utils.combo_phy_platform_supported_ports_dict.items():
        if phyObj.platform == platform_id and ddi[1] in ports:
            status = verify_combo_phy_buffer(phyObj, ddi[1], vbt_override, gfx_vbt, gfx_index)
            return status

    for platform_id, ports in display_phy_buffer_utils.typec_phy_platform_supported_ports_dict.items():
        if phyObj.platform == platform_id and ddi[1] in ports:
            port_num = 0
            for index in range(len(ports)):
                if ddi[1] == ports[index]:
                    port_num = index + 1
            status = verify_typec_phy_buffer(phyObj, port_num, vbt_override, gfx_vbt, gfx_index)
            return status


##
# @brief Verify MMIO programming for specific Combo Phy port
# @param[in] phyObj Phy Object of type DisplayPhyBuffer()
# @param[in] port_id for the specific port : example 1/2/3/4
# @param[in] vbt_override True/False based on driver/vbt tables being verified
# @param[in] gfx_vbt VBT Handle
# @param[in] gfx_index gfx adapter under verification gfx_0/gfx_1
# @return bool Return true if MMIO programming is correct, else return false
def verify_combo_phy_buffer(phyObj, port_id, vbt_override, gfx_vbt, gfx_index='gfx_0'):
    status = True
    system_info_status, misc_system_info = driver_escape.get_misc_system_info(gfx_index)
    low_link_rates_list = [1.62, 2.16, 2.43, 2.7]
    high_link_rates_list = [3.24, 4.32, 5.4]
    execution_environment_type = SystemUtility().get_execution_environment_type()

    # skip pre-si env as the environment don't simulate Snps PHY registers
    if execution_environment_type is None or execution_environment_type != "POST_SI_ENV":
        logging.info("Skipping PHY buffer verification on pre-si as the environment don't "
                     "simulate Snps PHY registers")
        return True

    if system_info_status is False:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][Phy_Buffer]:Driver Escape failed to fetch System Info for Adapter:{} "
                  "Status:{} ".format(system_info_status, gfx_index),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("Driver Escape failed to fetch System Info for Adapter:{}; Status:{} ".format(system_info_status,
                                                                                                    gfx_index))
    device_id = misc_system_info.platformInfo.deviceID
    obj_machine_info = machine_info.SystemInfo()
    logging.debug("Platform Device ID: {}".format(hex(device_id)[2:]))
    platform_details = obj_machine_info.get_platform_details(hex(device_id)[2:])
    platform_sku = platform_details.SkuName
    logging.debug("Platform Sku: {}".format(str(platform_sku)))

    # Check if pre-emp vswing values programmed in dpcd is supported
    supported_preemp_vswing_list = display_phy_buffer_utils.combo_phy_platform_supported_vswing_preemp_dict[
        "{0}".format(phyObj.platform)]

    number_of_lanes = dpcd_helper.DPCD_getNumOfLanes(phyObj.display_and_adapter_info)

    link_rate = dpcd_helper.DPCD_getLinkRate(phyObj.display_and_adapter_info)
    logging.debug("Link rate as programmed by driver: {}".format(link_rate))

    for lane_index in range(number_of_lanes):
        dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(phyObj.display_and_adapter_info,
                                                             display_phy_buffer_utils.DPCD_OFFSET_TRAINING_LANE_SET[
                                                                 lane_index])
        vswing_level = dpcd_value[0] & display_phy_buffer_utils.VSWING_LEVEL_SET
        preemp_level = (dpcd_value[0] & display_phy_buffer_utils.PREEMP_LEVEL_SET) >> 3

        logging.info("INFO: Lane:{0} Step1: Checking if Vswing and Pre-emp levels in DPCD offset {1} are supported "
                     "as per b-spec".format(lane_index,
                                            hex(display_phy_buffer_utils.DPCD_OFFSET_TRAINING_LANE_SET[lane_index])))

        if [vswing_level, preemp_level] in supported_preemp_vswing_list:
            logging.info("PASS: Lane:{0} Vswing:{1} Pre-emp:{2}  -- Verification successful"
                         .format(lane_index, vswing_level, preemp_level))
        else:
            status = False
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][Phy_Buffer]: Failed! Lane:{0} Vswing:{1} Pre-emp:{2} -- Unsupported"
                      " Vswing, Pre-emp level combination for platform".format(lane_index, vswing_level, preemp_level),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL: Lane:{0} Vswing:{1} Pre-emp:{2}  -- Unsupported Vswing, Pre-emp level "
                          "combination for the platform".format(lane_index, vswing_level, preemp_level))

        # Check if the phy mmio programming matches bspec for the pre-emp vswing set in DPCD
        if phyObj.platform not in display_phy_buffer_utils.supported_platform_list:
            return status

        # Platforms like MTL use external Snps PHY. The Vswing pre-emp values are programmed in external PHY registers
        if phyObj.platform == 'MTL':

            logging.info("INFO: Lane:{0} Step2: Comparing PhyBuffer (Pre-emp, Vswing) register programming "
                         "with b-spec/VBT PhyBuffer table".format(lane_index))

            # Verify the PHY registers against the expected PHY values
            # Each msgbus lane contains TX1 and TX2. So msgbus_lane0 has DP_lane_0 and DP_lane_1, and
            # msgbus_lane1 has DP_lane_2 and DP_lane_3
            msgbus_lane = 0 if lane_index in [0, 1] else 1
            if lane_index in [0, 2]:
                offset_phy_vdr_pre_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX1
                offset_phy_vdr_main_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX1
                offset_phy_vdr_post_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX1
            else:
                offset_phy_vdr_pre_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX2
                offset_phy_vdr_main_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX2
                offset_phy_vdr_post_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX2

            # PIPE Spec Defined Registers are common for C10 and C20 and are read with VDR_reg_read way.
            mtl_clock_helper = MtlClockHelper()
            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_pre_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_pre_ovrd_c10 = MtlSnpsPhyRegisters.REG_PHY_VDR_PRE_OVRD(offset_phy_vdr_pre_ovrd, value)

            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_main_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_main_ovrd_c10 = MtlSnpsPhyRegisters.REG_PHY_VDR_MAIN_OVRD(offset_phy_vdr_main_ovrd,
                                                                              value)

            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_post_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_post_ovrd_c10 = MtlSnpsPhyRegisters.REG_PHY_VDR_POST_OVRD(offset_phy_vdr_post_ovrd,
                                                                              value)

            if vbt_override is False:
                expected_phy_reg_values_C10_DP_1_4 = \
                    display_phy_buffer_utils.gen14_MTL_C10_phy_DP1_4_vswing_preemp_table[
                        f'{vswing_level},{preemp_level}']
            else:
                logging.info("TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT")
                continue  # TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT

            # C10 PHY DP 1.4 verification
            if phy_vdr_pre_ovrd_c10.TxEqPre == expected_phy_reg_values_C10_DP_1_4[0] and \
                    phy_vdr_main_ovrd_c10.TxEqMain == expected_phy_reg_values_C10_DP_1_4[1] and \
                    phy_vdr_post_ovrd_c10.TxEqPost == expected_phy_reg_values_C10_DP_1_4[2]:
                logging.info(f'PASS: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C10 PHY: '
                             f'Expected: [{expected_phy_reg_values_C10_DP_1_4[0]}, {expected_phy_reg_values_C10_DP_1_4[1]}, '
                             f'{expected_phy_reg_values_C10_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c10.TxEqPre}, '
                             f'{phy_vdr_main_ovrd_c10.TxEqMain}, {phy_vdr_post_ovrd_c10.TxEqPost}]')
                logging.info(
                    f'PASS: Lane:{lane_index} -- Verification Successful')
            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                          "Pre Cursor, Main Cursor, Post Cursor mismatch",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f'FAIL: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C10 PHY:'
                              f' Expected: [{expected_phy_reg_values_C10_DP_1_4[0]}, {expected_phy_reg_values_C10_DP_1_4[1]}, '
                              f'{expected_phy_reg_values_C10_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c10.TxEqPre}, '
                              f'{phy_vdr_main_ovrd_c10.TxEqMain}, {phy_vdr_post_ovrd_c10.TxEqPost}]')

            expected_lane_commit_bit = display_phy_buffer_utils.gen14_MTL_expected_lane_commit_bit_native[
                number_of_lanes]

            # Reading this offset to check if Lane commit bit is set as per b-spec
            # https://gfxspecs.intel.com/Predator/Home/Index/65449
            # Refer SW Programming of TX EQ settings - Point 5-8
            offset_phy_vdr_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_OVRD.offset

            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_ovrd = MtlSnpsPhyRegisters.REG_PHY_VDR_OVRD(offset_phy_vdr_ovrd, value)

            # As per b-spec, bit 0 and bit 2 of offset 0xD71 should be set
            # to 1 after updating 0xD80/0xD81/0xD82 VDR registers
            # https://gfxspecs.intel.com/Predator/Home/Index/65449
            # Refer SW Programming of TX EQ settings - Point 5-8
            if [phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2] == expected_lane_commit_bit:
                logging.info(f'PASS: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is set')
            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                          "Bit0 and Bit2 of offset 0xD71 is not set",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    f'FAIL: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is not set'
                    f' Expected: {expected_lane_commit_bit},   Actual: [{phy_vdr_ovrd.bit0}, 'f'{phy_vdr_ovrd.bit2}]')

        # Platforms like LNL use external Snps PHY. The Vswing pre-emp values are programmed in external PHY registers
        elif phyObj.platform == 'LNL':

            logging.info("INFO: Lane:{0} Step2: Comparing PhyBuffer (Pre-emp, Vswing) register programming "
                         "with b-spec/VBT PhyBuffer table".format(lane_index))

            # Verify the PHY registers against the expected PHY values
            # Each msgbus lane contains TX1 and TX2. So msgbus_lane0 has DP_lane_0 and DP_lane_1, and
            # msgbus_lane1 has DP_lane_2 and DP_lane_3
            msgbus_lane = 0 if lane_index in [0, 1] else 1
            if lane_index in [0, 2]:
                offset_phy_vdr_pre_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX1
                offset_phy_vdr_main_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX1
                offset_phy_vdr_post_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX1
            else:
                offset_phy_vdr_pre_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX2
                offset_phy_vdr_main_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX2
                offset_phy_vdr_post_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX2

            # PIPE Spec Defined Registers are common for C10 and C20 and are read with VDR_reg_read way.
            lnl_clock_helper = LnlClockHelper()
            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_pre_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_pre_ovrd_c10 = LnlSnpsPhyRegisters.REG_PHY_VDR_PRE_OVRD(offset_phy_vdr_pre_ovrd, value)

            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_main_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_main_ovrd_c10 = LnlSnpsPhyRegisters.REG_PHY_VDR_MAIN_OVRD(offset_phy_vdr_main_ovrd,
                                                                              value)

            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_post_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_post_ovrd_c10 = LnlSnpsPhyRegisters.REG_PHY_VDR_POST_OVRD(offset_phy_vdr_post_ovrd,
                                                                              value)

            if vbt_override is False:
                expected_phy_reg_values_C10_DP_1_4 = \
                    display_phy_buffer_utils.gen15_LNL_C10_phy_DP1_4_vswing_preemp_table[
                        f'{vswing_level},{preemp_level}']
            else:
                logging.info("TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT")
                continue  # TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT

            # C10 PHY DP 1.4 verification
            if phy_vdr_pre_ovrd_c10.TxEqPre == expected_phy_reg_values_C10_DP_1_4[0] and \
                    phy_vdr_main_ovrd_c10.TxEqMain == expected_phy_reg_values_C10_DP_1_4[1] and \
                    phy_vdr_post_ovrd_c10.TxEqPost == expected_phy_reg_values_C10_DP_1_4[2]:
                logging.info(f'PASS: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C10 PHY: '
                             f'Expected: [{expected_phy_reg_values_C10_DP_1_4[0]}, {expected_phy_reg_values_C10_DP_1_4[1]}, '
                             f'{expected_phy_reg_values_C10_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c10.TxEqPre}, '
                             f'{phy_vdr_main_ovrd_c10.TxEqMain}, {phy_vdr_post_ovrd_c10.TxEqPost}]')
                logging.info(
                    f'PASS: Lane:{lane_index} -- Verification Successful')
            else:
                status = False
                gdhm.report_test_bug_di("[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due "
                                        "to Pre Cursor, Main Cursor, Post Cursor mismatch")
                logging.error(f'FAIL: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C10 PHY:'
                              f' Expected: [{expected_phy_reg_values_C10_DP_1_4[0]}, {expected_phy_reg_values_C10_DP_1_4[1]}, '
                              f'{expected_phy_reg_values_C10_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c10.TxEqPre}, '
                              f'{phy_vdr_main_ovrd_c10.TxEqMain}, {phy_vdr_post_ovrd_c10.TxEqPost}]')

            expected_lane_commit_bit = display_phy_buffer_utils.gen15_LNL_expected_lane_commit_bit_native[
                number_of_lanes]

            # Reading this offset to check if Lane commit bit is set as per b-spec
            # https://gfxspecs.intel.com/Predator/Home/Index/65449
            # Refer SW Programming of TX EQ settings - Point 5-8
            offset_phy_vdr_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_OVRD.offset

            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_ovrd = LnlSnpsPhyRegisters.REG_PHY_VDR_OVRD(offset_phy_vdr_ovrd, value)

            # When writing to TX1 or TX2 of PHY Lane 0 or PHY Lane 1, bit 0 or bit 2, respectively, of register 0xD71
            # (lane_commit_bit) is set to 1. According to the PHY Lane and Transmitter Usage table provided in
            # https://gfxspecs.intel.com/Predator/Home/Index/68960, if the lane count is 1, only bit 0 is set for TX1
            # of PHY Lane 0. For a lane count of 2, both bits 0 and 2 are set for TX1 and TX2 of PHY Lane 0. For a
            # lane count of 4, bits 0 and 2 are set for TX1 and TX2 of both Lane 0 and Lane 1, where Lane 0 TX2 is
            # equivalent to Lane 1 TX2 and Lane 0 TX1 is equivalent to Lane 1 TX1.
            if [phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2] == expected_lane_commit_bit:
                logging.info(f'PASS: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is as per expectation! '
                             f'Expected: {expected_lane_commit_bit} Actual {[phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2]}')
            else:
                status = False
                gdhm.report_test_bug_di(
                    "[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                    "Bit0 and Bit2 of offset 0xD71 is not set")
                logging.error(
                    f'FAIL: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is not set'
                    f' Expected: {expected_lane_commit_bit},   Actual: [{phy_vdr_ovrd.bit0}, 'f'{phy_vdr_ovrd.bit2}]')

        else:
            logging.info("INFO: Lane:{0} Step2: Comparing PhyBuffer (Pre-emp, Vswing) register programming "
                         "with b-spec/VBT PhyBuffer table".format(lane_index))

            if link_rate in [6.48, 8.1]:
                hbr3 = True
            else:
                hbr3 = False

            if (display_utility.get_vbt_panel_type(phyObj.display_port, 'gfx_0') ==
                display_utility.VbtPanelType.LFP_DP) and (hbr3 is True):
                if is_edp_low_swing_setting(phyObj.display_port, gfx_index) is True:
                    if vbt_override is False:
                        if phyObj.platform in ['ICLLP', 'TGL', 'DG2']:
                            # for edp hbr3 with low swing vbt setting , pick edp hbr3 swing table as per b-spec
                            expected_phy_reg_values = display_phy_buffer_utils.combo_phy_vswing_preemp_table_edp_HBR3[
                                "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'DG1':
                            # for edp hbr3 with low swing vbt setting , pick edp hbr3 swing table as per b-spec
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_edp_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLP':
                            # for edp hbr3 with low swing vbt setting , pick edp hbr3 swing table as per b-spec
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_edp_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'RKL':
                            # for edp hbr3 with low swing vbt setting , pick edp hbr3 swing table as per b-spec
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_edp_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLS':
                            # for edp hbr3 with low swing vbt setting , pick edp hbr3 swing table as per b-spec
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_edp_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]

                    else:
                        if phyObj.platform == 'ICLLP':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.combo_phy_vswing_preemp_table_edp_HBR3,
                                display_phy_buffer_utils.ICL_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform in ['TGL', 'DG2']:
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.combo_phy_vswing_preemp_table_edp_HBR3,
                                display_phy_buffer_utils.TGL_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'DG1':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_edp_HBR3,
                                display_phy_buffer_utils.DG1_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLP':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_edp_HBR3,
                                display_phy_buffer_utils.ADLP_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'RKL':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_edp_HBR3,
                                display_phy_buffer_utils.RKL_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLS':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_edp_HBR3,
                                display_phy_buffer_utils.ADLS_COMBO_PHY_LOW_VSWING_UPTO_HBR3_INDEX, vswing_level,
                                preemp_level, gfx_vbt)

                else:
                    if vbt_override is False:
                        # for edp hbr3 with default swing vbt setting, pick external dp upto hbr2 swing table as per b-spec
                        if phyObj.platform == 'ICLLP':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen11_combo_phy_vswing_preemp_table_dp_uptoHBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform in ['TGL', 'DG2']:
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2_TGLUY[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'DG1':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLP':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'RKL':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLS':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                    "{0},{1}".format(vswing_level, preemp_level)]

                    else:
                        if phyObj.platform == 'ICLLP':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.combo_phy_vswing_preemp_table_edp_HBR3,
                                display_phy_buffer_utils.ICL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform in ['TGL', 'DG2']:
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2_TGLUY,
                                display_phy_buffer_utils.TGL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'DG1':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                display_phy_buffer_utils.DG1_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLP':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                display_phy_buffer_utils.ADLP_COMBO_PHY_VSWING_UPTO_HBR2_HBR3_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'RKL':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                display_phy_buffer_utils.RKL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLS':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                display_phy_buffer_utils.ADLS_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)

            elif (display_utility.get_vbt_panel_type(phyObj.display_port, 'gfx_0') ==
                  display_utility.VbtPanelType.LFP_DP) and (hbr3 is False):
                if is_edp_low_swing_setting(phyObj.display_port, gfx_index) is True:
                    if vbt_override is False:
                        # for edp upto hbr2 with low swing vbt setting, pick edp upto hbr2 swing table as per b-spec
                        if phyObj.platform in ['ICLLP', 'TGL', 'DG2']:
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.combo_phy_vswing_preemp_table_edp_uptoHBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'DG1':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_edp_upto_HBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLP':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_edp_upto_HBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'RKL':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_edp_upto_HBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLS':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_edp_upto_HBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                    else:
                        if phyObj.platform == 'ICLLP':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.combo_phy_vswing_preemp_table_edp_uptoHBR2,
                                display_phy_buffer_utils.ICL_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform in ['TGL', 'DG2']:
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.combo_phy_vswing_preemp_table_edp_uptoHBR2,
                                display_phy_buffer_utils.TGL_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'DG1':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_edp_upto_HBR2,
                                display_phy_buffer_utils.DG1_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLP':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_edp_upto_HBR2,
                                display_phy_buffer_utils.ADLP_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'RKL':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_edp_upto_HBR2,
                                display_phy_buffer_utils.RKL_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLS':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_edp_upto_HBR2,
                                display_phy_buffer_utils.ADLS_COMBO_PHY_LOW_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                else:
                    if vbt_override is False:
                        # for edp upto hbr2 with default swing vbt setting, pick external dp upto hbr2 swing table as per bspec
                        if phyObj.platform == 'ICLLP':
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.gen11_combo_phy_vswing_preemp_table_dp_uptoHBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]

                        elif phyObj.platform in ['TGL', 'DG2']:
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2_TGLUY[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'DG1':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLP':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'RKL':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                        elif phyObj.platform == 'ADLS':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                        "{0},{1}".format(vswing_level, preemp_level)]
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = \
                                    display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                        "{0},{1}".format(vswing_level, preemp_level)]

                    else:
                        if phyObj.platform == 'ICLLP':
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.gen11_combo_phy_vswing_preemp_table_dp_uptoHBR2,
                                display_phy_buffer_utils.ICL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)

                        elif phyObj.platform in ['TGL', 'DG2']:
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2_TGLUY,
                                    display_phy_buffer_utils.TGL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_uptoHBR,
                                    display_phy_buffer_utils.TGL_COMBO_PHY_VSWING_UPTO_HBR_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                        elif phyObj.platform == 'DG1':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                    display_phy_buffer_utils.DG1_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_uptoHBR,
                                    display_phy_buffer_utils.DG1_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLP':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                    display_phy_buffer_utils.ADLP_COMBO_PHY_VSWING_UPTO_HBR2_HBR3_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_uptoHBR,
                                    display_phy_buffer_utils.ADLP_COMBO_PHY_VSWING_UPTO_HBR_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                        elif phyObj.platform == 'RKL':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                    display_phy_buffer_utils.RKL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_uptoHBR,
                                    display_phy_buffer_utils.RKL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                        elif phyObj.platform == 'ADLS':
                            if link_rate in high_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                                    display_phy_buffer_utils.ADLS_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)
                            if link_rate in low_link_rates_list:
                                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                    display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_uptoHBR,
                                    display_phy_buffer_utils.ADLS_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                    preemp_level, gfx_vbt)

            elif 'DP' in phyObj.display_port and vbt_override is False:
                if phyObj.platform == 'ICLLP':
                    # for all external dp, pick external dp hbr2 swing table, icl combo phy does not support hbr3
                    expected_phy_reg_values = display_phy_buffer_utils.gen11_combo_phy_vswing_preemp_table_dp_uptoHBR2[
                        "{0},{1}".format(vswing_level, preemp_level)]

                elif phyObj.platform in ['TGL', 'DG2']:
                    if link_rate in high_link_rates_list:
                        if re.match(r'[uyUY]+', str(platform_sku)):
                            # for external dp hbr2, pick TGLUY external dp hbr2 swing table(tgl combo phy does not support hbr3)
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2_TGLUY[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                        else:
                            # for external dp hbr2, pick generic external dp hbr2 swing table(tgl combo phy does not support hbr3)
                            expected_phy_reg_values = \
                                display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2[
                                    "{0},{1}".format(vswing_level, preemp_level)]
                    elif link_rate in low_link_rates_list:
                        # for external dp upto hbr, pick external dp upto hbr swing table
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                "{0},{1}".format(vswing_level, preemp_level)]
                elif phyObj.platform == 'DG1':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                "{0},{1}".format(vswing_level, preemp_level)]
                    elif link_rate in low_link_rates_list:
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                "{0},{1}".format(vswing_level, preemp_level)]
                elif phyObj.platform == 'ADLP':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        # for external dp hbr2, pick TGLUY external dp hbr2 swing table(tgl combo phy does not support hbr3)
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                "{0},{1}".format(vswing_level, preemp_level)]
                    elif link_rate in low_link_rates_list:
                        # for external dp hbr2, pick TGLUY external dp hbr2 swing table(tgl combo phy does not support hbr3)
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                "{0},{1}".format(vswing_level, preemp_level)]
                elif phyObj.platform == 'RKL':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        # for external dp hbr2, pick RKL external dp hbr2 swing table(tgl combo phy does not support hbr3)
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                "{0},{1}".format(vswing_level, preemp_level)]
                    elif link_rate in low_link_rates_list:
                        # for external dp hbr2, pick RKL external dp hbr2 swing table(tgl combo phy does not support hbr3)
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                "{0},{1}".format(vswing_level, preemp_level)]
                elif phyObj.platform == 'ADLS':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        # for external dp hbr2, pick ADLS external dp hbr2 swing table(ADLS combo phy does not support hbr3)
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_HBR2_HBR3[
                                "{0},{1}".format(vswing_level, preemp_level)]
                    elif link_rate in low_link_rates_list:
                        # for external dp hbr2, pick ADLS external dp hbr2 swing table(ADLS combo phy does not support hbr3)
                        expected_phy_reg_values = \
                            display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_uptoHBR[
                                "{0},{1}".format(vswing_level, preemp_level)]

            elif 'DP' in phyObj.display_port and vbt_override is True:
                if phyObj.platform == 'ICLLP':
                    expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                        display_phy_buffer_utils.gen11_combo_phy_vswing_preemp_table_dp_uptoHBR2,
                        display_phy_buffer_utils.ICL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                        preemp_level, gfx_vbt)
                elif phyObj.platform in ['TGL', 'DG2']:
                    if link_rate in high_link_rates_list:
                        if re.match(r'[uyUY]+', str(platform_sku)):
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2_TGLUY,
                                display_phy_buffer_utils.TGL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                        else:
                            expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                                display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_HBR2,
                                display_phy_buffer_utils.TGL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                                preemp_level, gfx_vbt)
                    elif link_rate in low_link_rates_list:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.TGL_DG2_combo_phy_vswing_preemp_table_dp_uptoHBR,
                            display_phy_buffer_utils.TGL_COMBO_PHY_VSWING_UPTO_HBR_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                elif phyObj.platform == 'DG1':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                            display_phy_buffer_utils.DG1_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                    elif link_rate in low_link_rates_list:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_DG1_combo_phy_vswing_preemp_table_dp_uptoHBR,
                            display_phy_buffer_utils.DG1_COMBO_PHY_VSWING_UPTO_HBR_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                elif phyObj.platform == 'ADLP':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                            display_phy_buffer_utils.ADLP_COMBO_PHY_VSWING_UPTO_HBR2_HBR3_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                    elif link_rate in low_link_rates_list:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_ADLP_combo_phy_vswing_preemp_table_dp_uptoHBR,
                            display_phy_buffer_utils.ADLP_COMBO_PHY_VSWING_UPTO_HBR_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                elif phyObj.platform == 'RKL':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                            display_phy_buffer_utils.RKL_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                    elif link_rate in low_link_rates_list:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_RKL_combo_phy_vswing_preemp_table_dp_uptoHBR,
                            display_phy_buffer_utils.RKL_COMBO_PHY_VSWING_UPTO_HBR_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                elif phyObj.platform == 'ADLS':
                    if link_rate in [3.24, 4.32, 5.4, 6.48, 8.1]:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_HBR2_HBR3,
                            display_phy_buffer_utils.ADLS_COMBO_PHY_VSWING_UPTO_HBR2_INDEX, vswing_level,
                            preemp_level, gfx_vbt)
                    elif link_rate in low_link_rates_list:
                        expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                            display_phy_buffer_utils.gen13_ADLS_combo_phy_vswing_preemp_table_dp_uptoHBR,
                            display_phy_buffer_utils.ADLS_COMBO_PHY_VSWING_UPTO_HBR_INDEX, vswing_level,
                            preemp_level, gfx_vbt)

            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Phy_Buffer verification invalid on {} port as "
                          "expected port is eDP or DP".format(phyObj.display_port),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL: Port not detected as eDP or DP, phy buffer verification should not happen")
                expected_phy_reg_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # dummy initialization to avoid exception
                status = False

            offset_name = "PORT_TX_DW2_LN{0}_{1}".format(lane_index, port_id)
            port_tx_dw2_lnx = MMIORegister.read("PORT_TX_DW2_REGISTER", offset_name, phyObj.platform,
                                                gfx_index=gfx_index)
            offset_name = "PORT_TX_DW4_LN{0}_{1}".format(lane_index, port_id)
            port_tx_dw4_lnx = MMIORegister.read("PORT_TX_DW4_REGISTER", offset_name, phyObj.platform,
                                                gfx_index=gfx_index)
            offset_name = "PORT_TX_DW5_LN{0}_{1}".format(lane_index, port_id)
            port_tx_dw5_lnx = MMIORegister.read("PORT_TX_DW5_REGISTER", offset_name, phyObj.platform,
                                                gfx_index=gfx_index)
            offset_name = "PORT_TX_DW7_LN{0}_{1}".format(lane_index, port_id)
            port_tx_dw7_lnx = MMIORegister.read("PORT_TX_DW7_REGISTER", offset_name, phyObj.platform,
                                                gfx_index=gfx_index)

            swing_delect_dw2_binary = int("{0:b}{1:03b}".format(port_tx_dw2_lnx.swing_sel_upper,
                                                                port_tx_dw2_lnx.swing_sel_lower), 2)
            logging.debug(
                "DEBUG: Lane:{0} Vswing:{1} Pre-emp:{2} Combo Phy buffer register values :"
                "{3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}".
                    format(lane_index,
                           vswing_level,
                           preemp_level,
                           bin(swing_delect_dw2_binary),
                           hex(port_tx_dw7_lnx.NScalar),
                           hex(port_tx_dw4_lnx.cursor_coeff),
                           hex(port_tx_dw4_lnx.post_cursor_2),
                           hex(port_tx_dw4_lnx.post_cursor_1),
                           hex(port_tx_dw2_lnx.rcomp_scalar),
                           bin(port_tx_dw5_lnx.RtermSelect),
                           bin(port_tx_dw5_lnx.Disable3Tap),
                           bin(port_tx_dw5_lnx.Disable2Tap),
                           bin(port_tx_dw5_lnx.CursorProgram),
                           bin(port_tx_dw5_lnx.CoeffPolarity)
                           ))
            if (
                    (swing_delect_dw2_binary == expected_phy_reg_values[0]) and
                    (port_tx_dw7_lnx.NScalar == expected_phy_reg_values[1]) and
                    (port_tx_dw4_lnx.cursor_coeff == expected_phy_reg_values[2]) and
                    (port_tx_dw4_lnx.post_cursor_2 == expected_phy_reg_values[3]) and
                    (port_tx_dw4_lnx.post_cursor_1 == expected_phy_reg_values[4]) and
                    (port_tx_dw2_lnx.rcomp_scalar == expected_phy_reg_values[5]) and
                    (port_tx_dw5_lnx.RtermSelect == expected_phy_reg_values[6]) and
                    (port_tx_dw5_lnx.Disable3Tap == expected_phy_reg_values[7]) and
                    (port_tx_dw5_lnx.Disable2Tap == expected_phy_reg_values[8]) and
                    (port_tx_dw5_lnx.CursorProgram == expected_phy_reg_values[9]) and
                    (port_tx_dw5_lnx.CoeffPolarity == expected_phy_reg_values[10])
            ):
                logging.info(" PASS: Lane:{0} Vswing:{1} Pre-emp:{2} -- Verification Successful"
                             .format(lane_index, vswing_level, preemp_level))

            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for ComboPhy Buffer due to "
                          "Vswing Pre-emp mismatch",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    "FAIL: Lane:{0} Vswing:{1} Pre-emp:{2} Type:ComboPhy  "
                    "Expected:{3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}  "
                    "Observed:{14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}, {24}".
                        format(lane_index,
                               vswing_level,
                               preemp_level,
                               bin(expected_phy_reg_values[0]),
                               hex(expected_phy_reg_values[1]),
                               hex(expected_phy_reg_values[2]),
                               hex(expected_phy_reg_values[3]),
                               hex(expected_phy_reg_values[4]),
                               hex(expected_phy_reg_values[5]),
                               bin(expected_phy_reg_values[6]),
                               bin(expected_phy_reg_values[7]),
                               bin(expected_phy_reg_values[8]),
                               bin(expected_phy_reg_values[9]),
                               bin(expected_phy_reg_values[10]),
                               bin(swing_delect_dw2_binary),
                               hex(port_tx_dw7_lnx.NScalar),
                               hex(port_tx_dw4_lnx.cursor_coeff),
                               hex(port_tx_dw4_lnx.post_cursor_2),
                               hex(port_tx_dw4_lnx.post_cursor_1),
                               hex(port_tx_dw2_lnx.rcomp_scalar),
                               bin(port_tx_dw5_lnx.RtermSelect),
                               bin(port_tx_dw5_lnx.Disable3Tap),
                               bin(port_tx_dw5_lnx.Disable2Tap),
                               bin(port_tx_dw5_lnx.CursorProgram),
                               bin(port_tx_dw5_lnx.CoeffPolarity),
                               ))

    return status


##
# @brief Verify MMIO programming for specific Type-c phy port
# @param[in] phyObj Phy Object of type DisplayPhyBuffer()
# @param[in] port_num for the specific port : example 1/2/3/4
# @param[in] vbt_override True/False based on driver/vbt tables being verified
# @param[in] gfx_vbt VBT Handle
# @param[in] gfx_index gfx adapter under verification gfx_0/gfx_1
# @return bool Return true if MMIO programming is correct, else return false
def verify_typec_phy_buffer(phyObj, port_num, vbt_override, gfx_vbt, gfx_index='gfx_0'):
    status = True
    port_type = None
    low_link_rates_list = [1.62, 2.16, 2.43, 2.7]
    high_link_rates_list = [3.24, 4.32, 5.4, 6.48, 8.1]
    UHBR_link_rates_list = [10, 20, 13.5]
    tx_ffe_preset = 0
    status, misc_system_info = driver_escape.get_misc_system_info(gfx_index)
    device_id = misc_system_info.platformInfo.deviceID
    execution_environment_type = SystemUtility().get_execution_environment_type()
    disp_cfg = display_config.DisplayConfiguration()
    enum_displays = disp_cfg.get_enumerated_display_info()

    # skip pre-si env as the environment don't simulate Snps PHY registers
    if execution_environment_type is None or execution_environment_type != "POST_SI_ENV":
        logging.info("Skipping PHY buffer verification on pre-si as the environment don't "
                     "simulate Snps PHY registers")
        return True

    for i in range(enum_displays.Count):
        connector_port = str(cfg_enum.CONNECTOR_PORT_TYPE(enum_displays.ConnectedDisplays[i].ConnectorNPortType))
        if connector_port == phyObj.display_port:
            port_type = enum_displays.ConnectedDisplays[i].PortType
            break

    # Check if pre-emp vswing values programmed in dpcd is supported
    supported_preemp_vswing_list = display_phy_buffer_utils.typec_phy_platform_supported_vswing_preemp_dict[
        "{0}".format(phyObj.platform)]
    supported_tx_ffe_preset_list = display_phy_buffer_utils.DP_2P0_SUPPORTED_TX_FFE_PRESET_LIST
    number_of_lanes = dpcd_helper.DPCD_getNumOfLanes(phyObj.display_and_adapter_info)
    logging.info(f"SUPPORTED TX FFE PRESET LIST:{supported_tx_ffe_preset_list}")
    link_rate = dpcd_helper.DPCD_getLinkRate(phyObj.display_and_adapter_info)

    is_lttpr = False
    is_128b_132b_ch_encoding = False
    dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(phyObj.display_and_adapter_info,
                                                         display_phy_buffer_utils.DPCD_OFFSET_LTTPR)
    if dpcd_value[1] != 0 and dpcd_value[2] != 0:
        is_lttpr = True
    dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(phyObj.display_and_adapter_info,
                                                         display_phy_buffer_utils.MAIN_LINK_CHANEL_CODING_CAP)
    if dpcd_read_flag == True:
        if dpcd_value[0] == 0x3:
            is_128b_132b_ch_encoding = True
            logging.info(f"Display connected on port{phyObj.display_port} supports 128b/132b encoding")
    else:
        logging.error("[Test Issue]- Failed to read DPCD Data")
        return False
    for lane_index in range(number_of_lanes):
        if is_lttpr:
            dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(phyObj.display_and_adapter_info,
                                                                 display_phy_buffer_utils.DPCD_OFFSET_TRAINING_LANE_SET_LTTPR[
                                                                     lane_index])
        else:
            # Non-LTTPR Case
            dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(phyObj.display_and_adapter_info,
                                                                 display_phy_buffer_utils.DPCD_OFFSET_TRAINING_LANE_SET[
                                                                     lane_index])

        vswing_level = dpcd_value[0] & display_phy_buffer_utils.VSWING_LEVEL_SET
        preemp_level = (dpcd_value[0] & display_phy_buffer_utils.PREEMP_LEVEL_SET) >> 3
        if is_128b_132b_ch_encoding is False:
            logging.info("INFO: Lane:{0} Step1: Checking if Vswing and Pre-emp levels in DPCD offset {1} are supported "
                         "as per b-spec".format(lane_index,
                                                hex(display_phy_buffer_utils.DPCD_OFFSET_TRAINING_LANE_SET[
                                                        lane_index])))
            if [vswing_level, preemp_level] in supported_preemp_vswing_list:
                logging.info("PASS: Lane:{0} Vswing:{1} Pre-emp:{2}  -- Verification successful"
                             .format(lane_index, vswing_level, preemp_level))
            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Failed! Lane:{0} Vswing:{1} Pre-emp:{2} -- Unsupported "
                          "Vswing, Pre-emp level combination for platform".format(lane_index, vswing_level,
                                                                                  preemp_level),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL: Lane:{0} Vswing:{1} Pre-emp:{2}  -- Unsupported Vswing, Pre-emp level "
                              "combination for the platform".format(lane_index, vswing_level, preemp_level))
        else:
            tx_ffe_preset = dpcd_value[0] & display_phy_buffer_utils.FFE_PRESET_SET_MASK

            logging.info("INFO: Lane:{0} Step1: Checking if FFE preset value in DPCD offset {1} are supported "
                         "as per b-spec".format(lane_index,
                                                hex(display_phy_buffer_utils.DPCD_OFFSET_TRAINING_LANE_SET[
                                                        lane_index])))
            if tx_ffe_preset in supported_tx_ffe_preset_list:
                logging.info("PASS: Lane:{0} preset:{1}  -- Verification successful"
                             .format(lane_index, tx_ffe_preset))
            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Failed! Lane:{0} Preset:{1}  -- Unsupported "
                          " ffe preset for platform".format(lane_index, tx_ffe_preset),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL: Lane:{0} preset:{1}   -- Unsupported ffe preset "
                              "combination for the platform".format(lane_index, tx_ffe_preset))

        # Check if the phy mmio programming matches bspec for the pre-emp vswing set
        logging.info("INFO: Lane:{0} Step2: Comparing PhyBuffer (Pre-emp, Vswing) register programming "
                     "with b-spec/VBT PhyBuffer table".format(lane_index))
        if phyObj.platform in ["ICLLP"]:
            if link_rate in [1.62, 2.7] and vbt_override is False:
                # rbr and hbr have a set of values , hbr2 and hbr3 have different set
                expected_phy_reg_values = display_phy_buffer_utils.gen11_typec_phy_vswing_preemp_table_RBR_HBR[
                    "{0},{1}".format(vswing_level, preemp_level)]
            elif link_rate in [1.62, 2.7] and vbt_override is True:
                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                    display_phy_buffer_utils.gen11_typec_phy_vswing_preemp_table_RBR_HBR,
                    display_phy_buffer_utils.ICL_MGPHY_VSWING_INDEX, vswing_level, preemp_level,
                    gfx_vbt)
            elif vbt_override is False:
                expected_phy_reg_values = display_phy_buffer_utils.gen11_typec_phy_vswing_preemp_table_HBR2_HBR3[
                    "{0},{1}".format(vswing_level, preemp_level)]
            else:
                expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                    display_phy_buffer_utils.gen11_typec_phy_vswing_preemp_table_HBR2_HBR3,
                    display_phy_buffer_utils.ICL_MGPHY_VSWING_INDEX, vswing_level, preemp_level,
                    gfx_vbt)

            if lane_index in [0, 1]:
                tx_index = lane_index + 1
                lane_index_temp = 0
            else:
                tx_index = lane_index - 1
                lane_index_temp = 1

            offset_name = "MG_TX_DRVCTRL_TX{0}LN{1}_TXPORT{2}".format(tx_index, lane_index_temp, port_num)
            mg_tx_drvctrl = MMIORegister.read("MG_TX_DRVCTRL_REGISTER", offset_name, phyObj.platform,
                                              gfx_index=gfx_index)
            offset_name = "MG_TX_SWINGCTRL_TX{0}LN{1}_TXPORT{2}".format(tx_index, lane_index_temp, port_num)
            mg_tx_swingctrl = MMIORegister.read("MG_TX_SWINGCTRL_REGISTER", offset_name, phyObj.platform,
                                                gfx_index=gfx_index)

            logging.debug("DEBUG: Lane:{0} Vswing:{1} Pre-emp:{2} Type-c Phy buffer register values :"
                          " {3}, {4}, {5}, {6}".
                          format(lane_index,
                                 vswing_level,
                                 preemp_level,
                                 hex(mg_tx_drvctrl.cri_txdeemph_override_11_6),
                                 hex(mg_tx_drvctrl.cri_txdeemph_override_en),
                                 hex(mg_tx_drvctrl.cri_txdeemph_override_5_0),
                                 hex(mg_tx_swingctrl.cri_txdeemph_override17_12)
                                 ))

            if (
                    (mg_tx_drvctrl.cri_txdeemph_override_11_6 == expected_phy_reg_values[0]) and
                    (mg_tx_drvctrl.cri_txdeemph_override_en == expected_phy_reg_values[1]) and
                    (mg_tx_drvctrl.cri_txdeemph_override_5_0 == expected_phy_reg_values[2]) and
                    (mg_tx_swingctrl.cri_txdeemph_override17_12 == expected_phy_reg_values[3])
            ):
                logging.info("PASS: Lane:{0} Vswing:{1} Pre-emp:{2} -- Verification Successful"
                             .format(lane_index, vswing_level, preemp_level))
            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for MGPhy Buffer due to "
                          "Vswing Pre-emp mismatch",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL: Lane:{0} Vswing:{1} Pre-emp:{2} Type: MGPhy "
                              "Expected: {3}, {4}, {5}, {6}  "
                              "Observed: {7}, {8}, {9}, {10}".
                              format(lane_index,
                                     vswing_level,
                                     preemp_level,
                                     hex(expected_phy_reg_values[0]),
                                     hex(expected_phy_reg_values[1]),
                                     hex(expected_phy_reg_values[2]),
                                     hex(expected_phy_reg_values[3]),
                                     hex(mg_tx_drvctrl.cri_txdeemph_override_11_6),
                                     hex(mg_tx_drvctrl.cri_txdeemph_override_en),
                                     hex(mg_tx_drvctrl.cri_txdeemph_override_5_0),
                                     hex(mg_tx_swingctrl.cri_txdeemph_override17_12)
                                     ))

        elif phyObj.platform == 'TGL':
            if vbt_override is False:
                if link_rate in low_link_rates_list:
                    expected_phy_reg_values = display_phy_buffer_utils.gen12_typec_phy_vswing_preemp_table_RBR_HBR[
                        "{0},{1}".format(vswing_level, preemp_level)]
                elif link_rate in high_link_rates_list:
                    expected_phy_reg_values = display_phy_buffer_utils.gen12_typec_phy_vswing_preemp_table_HBR2_HBR3[
                        "{0},{1}".format(vswing_level, preemp_level)]

            else:
                if link_rate in low_link_rates_list:
                    expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                        display_phy_buffer_utils.gen12_typec_phy_vswing_preemp_table_RBR_HBR,
                        display_phy_buffer_utils.TGL_DKL_PHY_VSWING_UPTO_HBR_INDEX, vswing_level, preemp_level,
                        gfx_vbt)
                elif link_rate in high_link_rates_list:
                    expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                        display_phy_buffer_utils.gen12_typec_phy_vswing_preemp_table_HBR2_HBR3,
                        display_phy_buffer_utils.TGL_DKL_PHY_VSWING_UPTO_HBR3_INDEX, vswing_level, preemp_level,
                        gfx_vbt)

            if lane_index in [0, 1]:
                index_value = 0x0
            else:
                index_value = 0x1

            offset_name = "DKL_TX_DPCNTL{}_PORT{}".format(lane_index, port_num)
            dkl_tx_dpcntl = read_dkl_register_helper("DKL_TX_DPCNTL_REGISTER", offset_name, port_num, index_value,
                                                     phyObj.platform, gfx_index)

            logging.debug("DEBUG: Lane:{0} Vswing:{1} Pre-emp:{2} DekelPhy register values: "
                          "{3}, {4}, {5}".
                          format(lane_index,
                                 vswing_level,
                                 preemp_level,
                                 hex(dkl_tx_dpcntl.vswing_control_tx),
                                 hex(dkl_tx_dpcntl.preshoot_control_l0),
                                 hex(dkl_tx_dpcntl.de_emphasis_control_l0_tx)
                                 ))

            if (
                    (dkl_tx_dpcntl.vswing_control_tx == expected_phy_reg_values[0]) and
                    (dkl_tx_dpcntl.preshoot_control_l0 == expected_phy_reg_values[1]) and
                    (dkl_tx_dpcntl.de_emphasis_control_l0_tx == expected_phy_reg_values[2])
            ):
                logging.info("PASS: Lane:{0} Vswing:{1} Pre-emp:{2} -- Verification Successful"
                             .format(lane_index, vswing_level, preemp_level))
            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for DekelPhy due to "
                          "Vswing Pre-emp mismatch",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL: Lane:{0} Vswing:{1} Pre-emp:{2} Type: DekelPhy  "
                              "Expected: {3}, {4}, {5}   Observed: {6}, {7}, {8}".
                              format(lane_index,
                                     vswing_level,
                                     preemp_level,
                                     hex(expected_phy_reg_values[0]),
                                     hex(expected_phy_reg_values[1]),
                                     hex(expected_phy_reg_values[2]),
                                     hex(dkl_tx_dpcntl.vswing_control_tx),
                                     hex(dkl_tx_dpcntl.preshoot_control_l0),
                                     hex(dkl_tx_dpcntl.de_emphasis_control_l0_tx)))
        elif phyObj.platform == 'ADLP':
            if vbt_override is False:
                ## checking DeviceId for RPL P platform
                if device_id >= 0XA7A0 and is_128b_132b_ch_encoding:
                    if link_rate in UHBR_link_rates_list:
                        logging.info("Verifying UHBR link rate- linkrate:{0}".format(link_rate))
                        expected_phy_reg_values = display_phy_buffer_utils.gen13_rplp_dp2_0_tx_ffe_preset_table[
                            tx_ffe_preset]
                    else:
                        logging.error(
                            "[Driver Issue] - Link Training happened with non UHBR link rates for DP 2.1 panels. ")
                        gdhm.report_driver_bug_di(
                            "[Interfaces][Display_Engine] Link Training happened with non UHBR link rates for DP 2.1 "
                            "panels.")
                        return False
                if link_rate in low_link_rates_list:
                    expected_phy_reg_values = display_phy_buffer_utils.gen13_ADLP_typec_phy_vswing_preemp_table_RBR_HBR[
                        "{0},{1}".format(vswing_level, preemp_level)]
                elif link_rate in high_link_rates_list:
                    expected_phy_reg_values = \
                        display_phy_buffer_utils.gen13_ADLP_typec_phy_vswing_preemp_table_HBR2_HBR3[
                            "{0},{1}".format(vswing_level, preemp_level)]

            else:
                if link_rate in low_link_rates_list:
                    expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                        display_phy_buffer_utils.gen13_ADLP_typec_phy_vswing_preemp_table_RBR_HBR,
                        display_phy_buffer_utils.ADLP_DKL_PHY_VSWING_INDEX_UPTO_HBR_INDEX, vswing_level, preemp_level,
                        gfx_vbt)
                elif link_rate in high_link_rates_list:
                    expected_phy_reg_values = get_expected_phy_reg_values_vbt(
                        display_phy_buffer_utils.gen13_ADLP_typec_phy_vswing_preemp_table_RBR_HBR,
                        display_phy_buffer_utils.ADLP_DKL_PHY_VSWING_INDEX_HBR2_INDEX, vswing_level, preemp_level,
                        gfx_vbt)

            if lane_index == 0:
                index_value = 0x0
                offset1 = Gen13DdiRegs.OFFSET_DKLP_PCS_GLUE_TX_DPCNTL0.DKLP_PCS_GLUE_TX_DPCNTL0
            elif lane_index == 1:
                index_value = 0x0
                offset1 = Gen13DdiRegs.OFFSET_DKLP_PCS_GLUE_TX_DPCNTL1.DKLP_PCS_GLUE_TX_DPCNTL1
            else:
                index_value = 0x1
                offset1 = Gen13DdiRegs.OFFSET_DKLP_PCS_GLUE_TX_DPCNTL0.DKLP_PCS_GLUE_TX_DPCNTL0
            offset2 = Gen13DdiRegs.OFFSET_DKLP_PCS_GLUE_TX_DPCNTL2.DKLP_PCS_GLUE_TX_DPCNTL2

            read_offset1, read_offset2 = read_dkl_autogen_register_helper(offset1, offset2, port_num, index_value,
                                                                          gfx_index=gfx_index)
            read_value1 = DisplayArgs.read_register(read_offset1, gfx_index)
            read_value2 = DisplayArgs.read_register(read_offset2, gfx_index)
            dkl_pcs_glue_tx_dpcntl = Gen13DdiRegs.REG_DKLP_PCS_GLUE_TX_DPCNTL0(read_offset1, read_value1)
            dkl_pcs_glue_tx_dpcntl2 = Gen13DdiRegs.REG_DKLP_PCS_GLUE_TX_DPCNTL2(read_offset2, read_value2)

            logging.debug("DEBUG: Lane:{0} Vswing:{1} Pre-emp:{2} DekelPhy register values: "
                          "{3}, {4}, {5}".
                          format(lane_index,
                                 vswing_level,
                                 preemp_level,
                                 hex(dkl_pcs_glue_tx_dpcntl.Cfg_Vswing_Control_Tx1),
                                 hex(dkl_pcs_glue_tx_dpcntl.Cfg_Preshoot_Control_L0_Tx1),
                                 hex(dkl_pcs_glue_tx_dpcntl.Cfg_De_Emphasis_Control_L0_Tx1)
                                 ))
            if is_128b_132b_ch_encoding:
                if (
                        (dkl_pcs_glue_tx_dpcntl.Cfg_Vswing_Control_Tx1 == expected_phy_reg_values[0]) and
                        (dkl_pcs_glue_tx_dpcntl.Cfg_Preshoot_Control_L0_Tx1 == expected_phy_reg_values[1]) and
                        (dkl_pcs_glue_tx_dpcntl.Cfg_De_Emphasis_Control_L0_Tx1 == expected_phy_reg_values[2]) and
                        (dkl_pcs_glue_tx_dpcntl.Cfg_Shunt_Cm_Tx1 == expected_phy_reg_values[3]) and
                        (dkl_pcs_glue_tx_dpcntl.Cfg_Shunt_Cp_Tx1 == expected_phy_reg_values[4]) and
                        (dkl_pcs_glue_tx_dpcntl.Cfg_Cursor_Control_Tx1 == expected_phy_reg_values[5]) and
                        (dkl_pcs_glue_tx_dpcntl2.Cfg_Dp20Bitmode == 0)
                ):
                    logging.info("Pass: Lane:{0} FFE_Preset{1} Type: DekelPhy  "
                                 "Expected: [{2}, {3}, {4}, {5}, {6}, {7}]  Actual: [{8}, {9}, {10}, {11}, {12}, {13}, {14}]".
                                 format(lane_index,
                                        tx_ffe_preset,
                                        hex(expected_phy_reg_values[0]),
                                        hex(expected_phy_reg_values[1]),
                                        hex(expected_phy_reg_values[2]),
                                        hex(expected_phy_reg_values[3]),
                                        hex(expected_phy_reg_values[4]),
                                        hex(expected_phy_reg_values[5]),
                                        hex(dkl_pcs_glue_tx_dpcntl.Cfg_Vswing_Control_Tx1),
                                        hex(dkl_pcs_glue_tx_dpcntl.Cfg_Preshoot_Control_L0_Tx1),
                                        hex(dkl_pcs_glue_tx_dpcntl.Cfg_De_Emphasis_Control_L0_Tx1),
                                        hex(dkl_pcs_glue_tx_dpcntl.Cfg_Shunt_Cm_Tx1),
                                        hex(dkl_pcs_glue_tx_dpcntl.Cfg_Shunt_Cp_Tx1),
                                        hex(dkl_pcs_glue_tx_dpcntl.Cfg_Cursor_Control_Tx1),
                                        hex(dkl_pcs_glue_tx_dpcntl2.Cfg_Dp20Bitmode)))
                    logging.info("PASS: Lane:{0} FFE_Preset:{1} -- Verification Successful"
                                 .format(lane_index, tx_ffe_preset))
                else:
                    status = False
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for DekelPhy due to "
                              "FFE preset  mismatch",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error("FAIL: Lane:{0} FFE_Preset{1} Type: DekelPhy  "
                                  "Expected: {2}, {3}, {4}, {5}, {6}, {7}  Observed: {8}, {9}, {10}, {11}, {12}, {13}, {14}".
                                  format(lane_index,
                                         tx_ffe_preset,
                                         hex(expected_phy_reg_values[0]),
                                         hex(expected_phy_reg_values[1]),
                                         hex(expected_phy_reg_values[2]),
                                         hex(expected_phy_reg_values[3]),
                                         hex(expected_phy_reg_values[4]),
                                         hex(expected_phy_reg_values[5]),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_Vswing_Control_Tx1),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_Preshoot_Control_L0_Tx1),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_De_Emphasis_Control_L0_Tx1),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_Shunt_Cm_Tx1),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_Shunt_Cp_Tx1),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_Cursor_Control_Tx1),
                                         dkl_pcs_glue_tx_dpcntl2.Cfg_Dp20Bitmode))
            else:
                if (
                        (dkl_pcs_glue_tx_dpcntl.Cfg_Vswing_Control_Tx1 == expected_phy_reg_values[0]) and
                        (dkl_pcs_glue_tx_dpcntl.Cfg_Preshoot_Control_L0_Tx1 == expected_phy_reg_values[1]) and
                        (dkl_pcs_glue_tx_dpcntl.Cfg_De_Emphasis_Control_L0_Tx1 == expected_phy_reg_values[2]) and
                        (dkl_pcs_glue_tx_dpcntl2.Cfg_Dp20Bitmode == 0)
                ):
                    logging.info("PASS: Lane:{0} Vswing:{1} Pre-emp:{2} -- Verification Successful"
                                 .format(lane_index, vswing_level, preemp_level))
                else:
                    status = False
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for DekelPhy due to "
                              "Vswing Pre-emp mismatch",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error("FAIL: Lane:{0} Vswing:{1} Pre-emp:{2} Type: DekelPhy  "
                                  "Expected: {3}, {4}, {5} 0 Observed: {6}, {7}, {8}, {9}".
                                  format(lane_index,
                                         vswing_level,
                                         preemp_level,
                                         hex(expected_phy_reg_values[0]),
                                         hex(expected_phy_reg_values[1]),
                                         hex(expected_phy_reg_values[2]),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_Vswing_Control_Tx1),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_Preshoot_Control_L0_Tx1),
                                         hex(dkl_pcs_glue_tx_dpcntl.Cfg_De_Emphasis_Control_L0_Tx1),
                                         dkl_pcs_glue_tx_dpcntl2.Cfg_Dp20Bitmode))

        elif phyObj.platform == 'MTL':

            # The reason for skipping PHY buffer verification for TBT port type is that, according to the bspec,
            # for type-C DP tunneled over Thunderbolt, the Thunderbolt controller owns the PHY and the display
            # should not utilize the message bus or reversal.
            # https://gfxspecs.intel.com/Predator/Home/Index/64539
            if 'TBT' in port_type:
                logging.info("Skipping PHY buffer verification,  according to the bspec, "
                             "for type-C DP tunneled over Thunderbolt, "
                             "the Thunderbolt controller owns the PHY and the "
                             "display should not utilize the message bus or reversal.")
                return status

            # Verify the PHY registers against the expected PHY values
            # Each msgbus lane contains TX1 and TX2. So msgbus_lane0 has DP_lane_0 and DP_lane_1, and
            # msgbus_lane1 has DP_lane_2 and DP_lane_3
            msgbus_lane = 0 if lane_index in [0, 1] else 1
            if lane_index in [0, 2] and "TC" not in port_type:
                offset_phy_vdr_pre_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX1
                offset_phy_vdr_main_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX1
                offset_phy_vdr_post_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX1
            else:
                offset_phy_vdr_pre_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX2
                offset_phy_vdr_main_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX2
                offset_phy_vdr_post_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX2

            # PIPE Spec Defined Registers are common for C10 and C20 and are read with VDR_reg_read way.
            mtl_clock_helper = MtlClockHelper()

            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_pre_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_pre_ovrd_c20 = MtlSnpsPhyRegisters.REG_PHY_VDR_PRE_OVRD(offset_phy_vdr_pre_ovrd, value)

            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_main_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_main_ovrd_c20 = MtlSnpsPhyRegisters.REG_PHY_VDR_MAIN_OVRD(offset_phy_vdr_main_ovrd, value)

            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_post_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_post_ovrd_c20 = MtlSnpsPhyRegisters.REG_PHY_VDR_POST_OVRD(offset_phy_vdr_post_ovrd, value)

            if vbt_override is False:
                if link_rate in UHBR_link_rates_list:
                    expected_phy_reg_values_C20_DP_2_1 = \
                        display_phy_buffer_utils.gen14_MTL_C20_phy_DP2_0_ffe_preset_table[
                            tx_ffe_preset]
                else:
                    expected_phy_reg_values_C20_DP_1_4 = \
                        display_phy_buffer_utils.gen14_MTL_C20_phy_DP1_4_vswing_preemp_table[
                            f'{vswing_level},{preemp_level}']
            else:
                logging.info("TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT")
                continue  # TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT

            if link_rate in UHBR_link_rates_list:
                # C20 PHY DP 2.1 verification
                if phy_vdr_pre_ovrd_c20.TxEqPre == expected_phy_reg_values_C20_DP_2_1[0] and \
                        phy_vdr_main_ovrd_c20.TxEqMain == expected_phy_reg_values_C20_DP_2_1[1] and \
                        phy_vdr_post_ovrd_c20.TxEqPost == expected_phy_reg_values_C20_DP_2_1[2]:
                    logging.info(
                        f'PASS: For Lane:{lane_index}, FFE_Preset:{tx_ffe_preset}, Tx EQ settings for DP 2.1: '
                        f'Expected: [{expected_phy_reg_values_C20_DP_2_1[0]}, {expected_phy_reg_values_C20_DP_2_1[1]}, '
                        f'{expected_phy_reg_values_C20_DP_2_1[2]}]   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                        f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
                    logging.info(
                        f'PASS: Lane:{lane_index} -- Verification Successful')
                else:
                    status = False
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                              "Pre Cursor, Main Cursor, Post Cursor mismatch",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(
                        f'FAIL: For Lane:{lane_index}, FFE_Preset:{tx_ffe_preset}, Tx EQ settings for DP 2.1:'
                        f' Expected: [{expected_phy_reg_values_C20_DP_2_1[0]}, {expected_phy_reg_values_C20_DP_2_1[1]}, '
                        f'{expected_phy_reg_values_C20_DP_2_1[2]}]  Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                        f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
            else:
                # C20 PHY DP 1.4 verification
                if phy_vdr_pre_ovrd_c20.TxEqPre == expected_phy_reg_values_C20_DP_1_4[0] and \
                        phy_vdr_main_ovrd_c20.TxEqMain == expected_phy_reg_values_C20_DP_1_4[1] and \
                        phy_vdr_post_ovrd_c20.TxEqPost == expected_phy_reg_values_C20_DP_1_4[2]:
                    logging.info(f'PASS: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C20 PHY: '
                                 f'Expected: [{expected_phy_reg_values_C20_DP_1_4[0]}, {expected_phy_reg_values_C20_DP_1_4[1]}, '
                                 f'{expected_phy_reg_values_C20_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                                 f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
                    logging.info(
                        f'PASS: Lane:{lane_index} -- Verification Successful')
                else:
                    status = False
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                              "Pre Cursor, Main Cursor, Post Cursor mismatch",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(f'FAIL: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C20 PHY:'
                                  f' Expected: [{expected_phy_reg_values_C20_DP_1_4[0]}, {expected_phy_reg_values_C20_DP_1_4[1]}, '
                                  f'{expected_phy_reg_values_C20_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                                  f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')

            if "TC" in port_type:
                expected_lane_commit_bit = display_phy_buffer_utils.gen14_MTL_expected_lane_commit_bit_type_c[
                    number_of_lanes]
            else:
                expected_lane_commit_bit = display_phy_buffer_utils.gen14_MTL_expected_lane_commit_bit_native[
                    number_of_lanes]

            # Reading this offset to check if Lane commit bit is set as per b-spec
            # https://gfxspecs.intel.com/Predator/Home/Index/65449
            # Refer SW Programming of TX EQ settings - Point 5-8
            offset_phy_vdr_ovrd = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_OVRD.offset

            value = mtl_clock_helper.read_c10_phy_vdr_register(phyObj.display_port, offset_phy_vdr_ovrd,
                                                               gfx_index, msgbus_lane=msgbus_lane)
            phy_vdr_ovrd = MtlSnpsPhyRegisters.REG_PHY_VDR_OVRD(offset_phy_vdr_ovrd, value)

            # As per b-spec, bit 0 and bit 2 of offset 0xD71 should be set
            # to 1 after updating 0xD80/0xD81/0xD82 VDR registers
            # https://gfxspecs.intel.com/Predator/Home/Index/65449
            # Refer SW Programming of TX EQ settings - Point 5-8
            if [phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2] == expected_lane_commit_bit:
                logging.info(f'PASS: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is set')
            else:
                status = False
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                          "Bit0 and Bit2 of offset 0xD71 is not set",
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f'FAIL: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is not set'
                              f' Expected: {expected_lane_commit_bit},   Actual: [{phy_vdr_ovrd.bit0}, 'f'{phy_vdr_ovrd.bit2}]')

        elif phyObj.platform == 'LNL':

            # The reason for skipping PHY buffer verification for TBT port type is that, according to the bspec,
            # for type-C DP tunneled over Thunderbolt, the Thunderbolt controller owns the PHY and the display
            # should not utilize the message bus or reversal.
            # https://gfxspecs.intel.com/Predator/Home/Index/64539
            if 'TBT' in port_type:
                logging.info("Skipping PHY buffer verification,  according to the bspec, "
                             "for type-C DP tunneled over Thunderbolt, "
                             "the Thunderbolt controller owns the PHY and the "
                             "display should not utilize the message bus or reversal.")
                return status

            # Verify the PHY registers against the expected PHY values
            # Each msgbus lane contains TX1 and TX2. So msgbus_lane0 has DP_lane_0 and DP_lane_1, and
            # msgbus_lane1 has DP_lane_2 and DP_lane_3
            msgbus_lane = 0 if lane_index in [0, 1] else 1
            if lane_index in [0, 2] and "TC" not in port_type:
                offset_phy_vdr_pre_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX1
                offset_phy_vdr_main_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX1
                offset_phy_vdr_post_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX1
            else:
                offset_phy_vdr_pre_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX2
                offset_phy_vdr_main_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX2
                offset_phy_vdr_post_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX2

            # PIPE Spec Defined Registers are common for C10 and C20 and are read with VDR_reg_read way.
            lnl_clock_helper = LnlClockHelper()

            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_pre_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_pre_ovrd_c20 = LnlSnpsPhyRegisters.REG_PHY_VDR_PRE_OVRD(offset_phy_vdr_pre_ovrd, value)

            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_main_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_main_ovrd_c20 = LnlSnpsPhyRegisters.REG_PHY_VDR_MAIN_OVRD(offset_phy_vdr_main_ovrd, value)

            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_post_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_post_ovrd_c20 = LnlSnpsPhyRegisters.REG_PHY_VDR_POST_OVRD(offset_phy_vdr_post_ovrd, value)

            if vbt_override is False:
                if link_rate in UHBR_link_rates_list:
                    expected_phy_reg_values_C20_DP_2_1 = \
                        display_phy_buffer_utils.gen15_LNL_C20_phy_DP2_0_ffe_preset_table[
                            tx_ffe_preset]
                else:
                    expected_phy_reg_values_C20_DP_1_4 = \
                        display_phy_buffer_utils.gen15_LNL_C20_phy_DP1_4_vswing_preemp_table[
                            f'{vswing_level},{preemp_level}']
            else:
                logging.info("TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT")
                continue  # TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT

            if link_rate in UHBR_link_rates_list:
                # C20 PHY DP 2.1 verification
                if phy_vdr_pre_ovrd_c20.TxEqPre == expected_phy_reg_values_C20_DP_2_1[0] and \
                        phy_vdr_main_ovrd_c20.TxEqMain == expected_phy_reg_values_C20_DP_2_1[1] and \
                        phy_vdr_post_ovrd_c20.TxEqPost == expected_phy_reg_values_C20_DP_2_1[2]:
                    logging.info(
                        f'PASS: For Lane:{lane_index}, FFE_Preset:{tx_ffe_preset}, Tx EQ settings for DP 2.1: '
                        f'Expected: [{expected_phy_reg_values_C20_DP_2_1[0]}, {expected_phy_reg_values_C20_DP_2_1[1]}, '
                        f'{expected_phy_reg_values_C20_DP_2_1[2]}]   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                        f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
                    logging.info(
                        f'PASS: Lane:{lane_index} -- Verification Successful')
                else:
                    status = False
                    gdhm.report_test_bug_di("[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy "
                                            "due to "
                                            "Pre Cursor, Main Cursor, Post Cursor mismatch")
                    logging.error(
                        f'FAIL: For Lane:{lane_index}, FFE_Preset:{tx_ffe_preset}, Tx EQ settings for DP 2.1:'
                        f' Expected: [{expected_phy_reg_values_C20_DP_2_1[0]}, {expected_phy_reg_values_C20_DP_2_1[1]}, '
                        f'{expected_phy_reg_values_C20_DP_2_1[2]}]  Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                        f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
            else:
                # C20 PHY DP 1.4 verification
                if phy_vdr_pre_ovrd_c20.TxEqPre == expected_phy_reg_values_C20_DP_1_4[0] and \
                        phy_vdr_main_ovrd_c20.TxEqMain == expected_phy_reg_values_C20_DP_1_4[1] and \
                        phy_vdr_post_ovrd_c20.TxEqPost == expected_phy_reg_values_C20_DP_1_4[2]:
                    logging.info(f'PASS: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C20 PHY: '
                                 f'Expected: [{expected_phy_reg_values_C20_DP_1_4[0]}, {expected_phy_reg_values_C20_DP_1_4[1]}, '
                                 f'{expected_phy_reg_values_C20_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                                 f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
                    logging.info(
                        f'PASS: Lane:{lane_index} -- Verification Successful')
                else:
                    status = False
                    gdhm.report_test_bug_di(
                        "[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                        "Pre Cursor, Main Cursor, Post Cursor mismatch")
                    logging.error(f'FAIL: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C20 PHY:'
                                  f' Expected: [{expected_phy_reg_values_C20_DP_1_4[0]}, {expected_phy_reg_values_C20_DP_1_4[1]}, '
                                  f'{expected_phy_reg_values_C20_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                                  f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')

            if "TC" in port_type:
                expected_lane_commit_bit = display_phy_buffer_utils.gen15_LNL_expected_lane_commit_bit_type_c[
                    number_of_lanes]
            else:
                expected_lane_commit_bit = display_phy_buffer_utils.gen15_LNL_expected_lane_commit_bit_native[
                    number_of_lanes]

            # Reading this offset to check if Lane commit bit is set as per b-spec
            # https://gfxspecs.intel.com/Predator/Home/Index/65449
            # Refer SW Programming of TX EQ settings - Point 5-8
            offset_phy_vdr_ovrd = LnlSnpsPhyRegisters.OFFSET_PHY_VDR_OVRD.offset

            value = lnl_clock_helper.read_c10_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_ovrd = LnlSnpsPhyRegisters.REG_PHY_VDR_OVRD(offset_phy_vdr_ovrd, value)

            # When writing to TX1 or TX2 of PHY Lane 0 or PHY Lane 1, bit 0 or bit 2, respectively, of register 0xD71
            # (lane_commit_bit) is set to 1. According to the PHY Lane and Transmitter Usage table provided in
            # https://gfxspecs.intel.com/Predator/Home/Index/68960, if the lane count is 1, only bit 2 is set for TX2
            # of PHY Lane 0. For a lane count of 2, both bits 0 and 2 are set for TX1 and TX2 of PHY Lane 0. For a
            # lane count of 4, bits 0 and 2 are set for TX1 and TX2 of both Lane 0 and Lane 1, where Lane 0 TX2 is
            # equivalent to Lane 1 TX2 and Lane 0 TX1 is equivalent to Lane 1 TX1.
            if [phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2] == expected_lane_commit_bit:
                logging.info(f'PASS: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is as per expectation! '
                             f'Expected: {expected_lane_commit_bit} Actual {[phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2]}')
            else:
                status = False
                gdhm.report_test_bug_di("[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due "
                                        "to Bit0 and Bit2 of offset 0xD71 is not set")
                logging.error(f'FAIL: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is not set'
                              f' Expected: {expected_lane_commit_bit},   Actual: [{phy_vdr_ovrd.bit0}, 'f'{phy_vdr_ovrd.bit2}]')

        elif phyObj.platform == 'ELG':

            # Verify the PHY registers against the expected PHY values
            # Each msgbus lane contains TX1 and TX2. So msgbus_lane0 has DP_lane_0 and DP_lane_1, and
            # msgbus_lane1 has DP_lane_2 and DP_lane_3
            msgbus_lane = 0 if lane_index in [0, 1] else 1
            if lane_index in [0, 2]:
                offset_phy_vdr_pre_ovrd = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX1
                offset_phy_vdr_main_ovrd = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX1
                offset_phy_vdr_post_ovrd = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX1
            else:
                offset_phy_vdr_pre_ovrd = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_PRE_OVRD.TX2
                offset_phy_vdr_main_ovrd = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_MAIN_OVRD.TX2
                offset_phy_vdr_post_ovrd = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_POST_OVRD.TX2

            # PIPE Spec Defined Registers are read with VDR_reg_read way
            elg_clock_helper = ElgClockHelper()

            value = elg_clock_helper.read_c20_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_pre_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_pre_ovrd_c20 = ElgSnpsPhyRegisters.REG_PHY_VDR_PRE_OVRD(offset_phy_vdr_pre_ovrd, value)

            value = elg_clock_helper.read_c20_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_main_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_main_ovrd_c20 = ElgSnpsPhyRegisters.REG_PHY_VDR_MAIN_OVRD(offset_phy_vdr_main_ovrd, value)

            value = elg_clock_helper.read_c20_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_post_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_post_ovrd_c20 = ElgSnpsPhyRegisters.REG_PHY_VDR_POST_OVRD(offset_phy_vdr_post_ovrd, value)

            if vbt_override is False:
                if link_rate in UHBR_link_rates_list:
                    expected_phy_reg_values_C20_DP_2_1 = \
                        display_phy_buffer_utils.gen14_ELG_C20_phy_DP2_1_ffe_preset_table[
                            tx_ffe_preset]
                else:
                    expected_phy_reg_values_C20_DP_1_4 = \
                        display_phy_buffer_utils.gen14_ELG_C20_phy_DP1_4_vswing_preemp_table[
                            f'{vswing_level},{preemp_level}']
            else:
                logging.info("TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT")
                continue  # TODO: Need to add code here for getting the Vswing & Pre-emph indexes from VBT

            if link_rate in UHBR_link_rates_list:
                # C20 PHY DP 2.1 verification
                if phy_vdr_pre_ovrd_c20.TxEqPre == expected_phy_reg_values_C20_DP_2_1[0] and \
                        phy_vdr_main_ovrd_c20.TxEqMain == expected_phy_reg_values_C20_DP_2_1[1] and \
                        phy_vdr_post_ovrd_c20.TxEqPost == expected_phy_reg_values_C20_DP_2_1[2]:
                    logging.info(
                        f'PASS: For Lane:{lane_index}, FFE_Preset:{tx_ffe_preset}, Tx EQ settings for DP 2.1: '
                        f'Expected: [{expected_phy_reg_values_C20_DP_2_1[0]}, {expected_phy_reg_values_C20_DP_2_1[1]}, '
                        f'{expected_phy_reg_values_C20_DP_2_1[2]}]   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                        f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
                    logging.info(
                        f'PASS: Lane:{lane_index} -- Verification Successful')
                else:
                    status = False
                    gdhm.report_test_bug_di("[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy "
                                            "due to "
                                            "Pre Cursor, Main Cursor, Post Cursor mismatch")
                    logging.error(
                        f'FAIL: For Lane:{lane_index}, FFE_Preset:{tx_ffe_preset}, Tx EQ settings for DP 2.1:'
                        f' Expected: [{expected_phy_reg_values_C20_DP_2_1[0]}, {expected_phy_reg_values_C20_DP_2_1[1]}, '
                        f'{expected_phy_reg_values_C20_DP_2_1[2]}]  Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                        f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
            else:
                # C20 PHY DP 1.4 verification
                if phy_vdr_pre_ovrd_c20.TxEqPre == expected_phy_reg_values_C20_DP_1_4[0] and \
                        phy_vdr_main_ovrd_c20.TxEqMain == expected_phy_reg_values_C20_DP_1_4[1] and \
                        phy_vdr_post_ovrd_c20.TxEqPost == expected_phy_reg_values_C20_DP_1_4[2]:
                    logging.info(f'PASS: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C20 PHY: '
                                 f'Expected: [{expected_phy_reg_values_C20_DP_1_4[0]}, {expected_phy_reg_values_C20_DP_1_4[1]}, '
                                 f'{expected_phy_reg_values_C20_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                                 f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')
                    logging.info(
                        f'PASS: Lane:{lane_index} -- Verification Successful')
                else:
                    status = False
                    gdhm.report_test_bug_di(
                        "[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due to "
                        "Pre Cursor, Main Cursor, Post Cursor mismatch")
                    logging.error(f'FAIL: For Lane:{lane_index}, Tx EQ settings for DP 1.4 C20 PHY:'
                                  f' Expected: [{expected_phy_reg_values_C20_DP_1_4[0]}, {expected_phy_reg_values_C20_DP_1_4[1]}, '
                                  f'{expected_phy_reg_values_C20_DP_1_4[2]}],   Actual: [{phy_vdr_pre_ovrd_c20.TxEqPre}, '
                                  f'{phy_vdr_main_ovrd_c20.TxEqMain}, {phy_vdr_post_ovrd_c20.TxEqPost}]')

            expected_lane_commit_bit = display_phy_buffer_utils.gen14_ELG_expected_lane_commit_bit_native[
                number_of_lanes]

            # Reading this offset to check if Lane commit bit is set as per b-spec
            # https://gfxspecs.intel.com/Predator/Home/Index/65449
            # Refer SW Programming of TX EQ settings - Point 5-8
            offset_phy_vdr_ovrd = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_OVRD.offset

            value = elg_clock_helper.read_c20_phy_vdr_register(gfx_index, phyObj.display_port, offset_phy_vdr_ovrd,
                                                               msgbus_lane=msgbus_lane)
            phy_vdr_ovrd = ElgSnpsPhyRegisters.REG_PHY_VDR_OVRD(offset_phy_vdr_ovrd, value)

            # When writing to TX1 or TX2 of PHY Lane 0 or PHY Lane 1, bit 0 or bit 2, respectively, of register 0xD71
            # (lane_commit_bit) is set to 1. According to the PHY Lane and Transmitter Usage table provided in
            # https://gfxspecs.intel.com/Predator/Home/Index/68960, if the lane count is 1, only bit 2 is set for TX2
            # of PHY Lane 0. For a lane count of 2, both bits 0 and 2 are set for TX1 and TX2 of PHY Lane 0. For a
            # lane count of 4, bits 0 and 2 are set for TX1 and TX2 of both Lane 0 and Lane 1, where Lane 0 TX2 is
            # equivalent to Lane 1 TX2 and Lane 0 TX1 is equivalent to Lane 1 TX1.
            if [phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2] == expected_lane_commit_bit:
                logging.info(f'PASS: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is as per expectation! '
                             f'Expected: {expected_lane_commit_bit} Actual {[phy_vdr_ovrd.bit0, phy_vdr_ovrd.bit2]}')
            else:
                status = False
                gdhm.report_test_bug_di("[Interfaces][Display_Engine][Phy_Buffer]:Verification failed for SnpsPhy due "
                                        "to Bit0 and Bit2 of offset 0xD71 is not set")
                logging.error(f'FAIL: For Lane:{lane_index}, Bit0 and Bit2 of offset 0xD71 is not set'
                              f' Expected: {expected_lane_commit_bit},   Actual: [{phy_vdr_ovrd.bit0}, 'f'{phy_vdr_ovrd.bit2}]')

        return status


##
# @brief Helper to read dekel phy registers
# @param[in] register_name Register name as string
# @param[in] offset_name Offset name as string
# @param[in] port_num Type-c Port number , example 1/2/3/4
# @param[in] index_value Index value to write into HIP Index registers
# @param[in] platform short string name , as defined in platform name XML, example ICLLP/TGL
# @param[in] gfx_index gfx adapter under verification gfx_0/gfx_1
# @return bool Return true if MMIO programming is correct, else return false
def read_dkl_register_helper(register_name, offset_name, port_num, index_value, platform, gfx_index='gfx_0'):
    reg1_value = MMIORegister.read("HIP_INDEX_REG0_REGISTER", "HIP_INDEX_REG0", platform, gfx_index=gfx_index)
    reg2_value = MMIORegister.read("HIP_INDEX_REG1_REGISTER", "HIP_INDEX_REG1", platform, gfx_index=gfx_index)

    HIP_INDEX_REG0 = 0x1010A0
    HIP_INDEX_REG1 = 0x1010A4

    if port_num == 1:
        reg1_value.HIP_168_Index = index_value
    elif port_num == 2:
        reg1_value.HIP_169_Index = index_value
    elif port_num == 3:
        reg1_value.HIP_16A_Index = index_value
    elif port_num == 4:
        reg1_value.HIP_16B_Index = index_value
    elif port_num == 5:
        reg2_value.HIP_16C_Index = index_value
    elif port_num == 6:
        reg2_value.HIP_16D_Index = index_value

    driver_interface.DriverInterface().mmio_write(HIP_INDEX_REG0, reg1_value.asUint, gfx_index=gfx_index)
    driver_interface.DriverInterface().mmio_write(HIP_INDEX_REG1, reg2_value.asUint, gfx_index=gfx_index)

    return MMIORegister.read(register_name, offset_name, platform, gfx_index=gfx_index)


##
# @brief Helper to read dekel phy autgen registers
# @param[in] offset1 Verification Register1 Offset
# @param[in] offset2 Verification Register2 Offset
# @param[in] port_num port 1/2/3..
# @param[in] index_value Index value to write into HIP Index registers
# @param[in] gfx_index e.g. gfx_0/gfx_1
# @return readoffset1, readoffset2 return read offsets
def read_dkl_autogen_register_helper(offset1, offset2, port_num, index_value, gfx_index='gfx_0'):
    if port_num == 1:
        write_offset = Gen13DdiRegs.OFFSET_HIP_INDEX_REG0.HIP_INDEX_REG0
        read_offset1 = offset1 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_168_Base']
        read_offset2 = offset2 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_168_Base']
    elif port_num == 2:
        write_offset = Gen13DdiRegs.OFFSET_HIP_INDEX_REG0.HIP_INDEX_REG0
        read_offset1 = offset1 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_169_Base']
        read_offset2 = offset2 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_169_Base']
    elif port_num == 3:
        write_offset = Gen13DdiRegs.OFFSET_HIP_INDEX_REG0.HIP_INDEX_REG0
        read_offset1 = offset1 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16A_Base']
        read_offset2 = offset2 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16A_Base']
    elif port_num == 4:
        write_offset = Gen13DdiRegs.OFFSET_HIP_INDEX_REG0.HIP_INDEX_REG0
        read_offset1 = offset1 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16B_Base']
        read_offset2 = offset2 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16B_Base']
    elif port_num == 5:
        write_offset = Gen13DdiRegs.OFFSET_HIP_INDEX_REG1.HIP_INDEX_REG1
        read_offset1 = offset1 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16C_Base']
        read_offset2 = offset2 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16C_Base']
    elif port_num == 6:
        write_offset = Gen13DdiRegs.OFFSET_HIP_INDEX_REG1.HIP_INDEX_REG1
        read_offset1 = offset1 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16D_Base']
        read_offset2 = offset2 + display_phy_buffer_utils.PHY_BASE_DICT['HIP_16D_Base']
    else:
        logging.error("Invalid Port Number Passed {}".format(port_num))
        return

    DisplayArgs.write_register(write_offset, index_value, gfx_index)
    return read_offset1, read_offset2


##
# @brief Helper to check if edp has vbt set for low power swing or default swing
# @param[in] display input .e.g. dp_a
# @param[in] gfx_index input .e.g. gfx_0, gfx_1
# @return bool Return true if low swing is selected in vbt else return false
def is_edp_low_swing_setting(display, gfx_index='gfx_0'):
    vbt = Vbt(gfx_index)

    if display_utility.get_vbt_panel_type(display, gfx_index) == display_utility.VbtPanelType.LFP_DP:
        panel_index = vbt.get_lfp_panel_type(display)
        logging.debug(f"\tPanel Index for {display}= {panel_index}")

        ##
        # Make sure panel_index is present
        if panel_index not in range(16):
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][Phy_Buffer]:Panel index {0} is not in the range of 0 to 15".format(
                    panel_index),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR: Panel index {0} is not in the range of 0 to 15".format(panel_index))

        shift = 0
        if panel_index % 2 != 0:
            shift = 3
        if (vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] >> shift) & 0xF == 0:
            logging.debug("DEBUG: VBT VSwingPreEmphasis Table Selection= LOW VOLTAGE TABLE")
            return True
        else:
            logging.debug("DEBUG: VBT VSwingPreEmphasis Table Selection= DEFAULT VOLTAGE TABLE")
            return False
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][Phy_Buffer]:Function is supported only for edp, but unexpectedly called"
                  " for {0}".format(display),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(
            "ERROR: Function is supported only for edp, but unexpectedly called for {0}, will return False".format(
                display))
        return False


##
# @brief Helper to get expected
# @param[in] table pre-emp v-swing table to use
# @param[in] table_index index for the table
# @param[in] vswing_level v-swing level
# @param[in] preemp_level pre-emp level
# @param[in] gfx_vbt handle
# @return list of phy register values from vbt block 57
def get_expected_phy_reg_values_vbt(table, table_index, vswing_level, preemp_level, gfx_vbt):
    swing_level_index = sorted(list(table.keys())).index("{0},{1}".format(vswing_level, preemp_level))
    param_set_length = len(table["{0},{1}".format(vswing_level, preemp_level)])
    return gfx_vbt.block_57.VSwingPreempTables[table_index].VswingPreempTableFields[
           (swing_level_index * 11): (swing_level_index * 11) + param_set_length]
