######################################################################################
# \file         lace_base.py
# \section      lace_base
# \remarks      This script contains helper functions which help in performing register level verification used by
#               LACE test scripts
# \ref          lace_verification.py \n
# \author       Soorya R, Smitha B
######################################################################################
import ctypes
import importlib
import logging
import math

from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core import registry_access
from Libs.Core import enum
from registers.mmioregister import MMIORegister
from Tests.Color.color_common_utility import gdhm_report_app_color


TILE_SIZE = 256.0
HIST_BIN_SIZE = 32
NUM_OF_IE_ENTRIES = 33
MAX_TILE_SIZE = 20 # Generic for both portrait(9X16)/landscape(16X9) until Gen12 . In Gen12 5k LACE is supported hence max tiles is 20X13
START_OF_HISTOGRAM_DATA = "Bin data: "
START_OF_IE_DATA = "IE data: "


class HistogramBins(ctypes.Structure):
    _fields_ = [('Bins', (ctypes.c_uint * HIST_BIN_SIZE))]

    def __init__(self):
        for i in range(0, HIST_BIN_SIZE):
            self.Bins[i] = 0


class IEEntries(ctypes.Structure):
    _fields_ = [('Entries', (ctypes.c_uint * NUM_OF_IE_ENTRIES))]

    def __init__(self):
        for i in range(0, NUM_OF_IE_ENTRIES):
            self.Entries[i] = 0


class LaceData(ctypes.Structure):
    _fields_ = [('HistogramDataHW', (HistogramBins * MAX_TILE_SIZE) * MAX_TILE_SIZE),
                ('HistogramDataSW', (HistogramBins * MAX_TILE_SIZE) * MAX_TILE_SIZE),
                ('IEDataHW', (IEEntries * MAX_TILE_SIZE) * MAX_TILE_SIZE),
                ('IEDataSW', (IEEntries * MAX_TILE_SIZE) * MAX_TILE_SIZE)]

    def __init__(self):
        for i in range(0, MAX_TILE_SIZE):
            for j in range(0, MAX_TILE_SIZE):
                self.HistogramDataHW[i][j] = HistogramBins()
                self.HistogramDataSW[i][j] = HistogramBins()
                self.IEDataHW[i][j] = IEEntries()
                self.IEDataSW[i][j] = IEEntries()


reg_read = MMIORegister()
machine_info = SystemInfo()
##
# Get the platform info
platform = None
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break
LaceParams = LaceData()
dplc_reg = importlib.import_module("registers.%s.DPLC_CTL_REGISTER" % (platform))

##
# For reference :
# DISPLAY_LACE_AGGRESSIVENESS_LOW = LaceAggressivenessLevel = 0
# LaceAlsThresholdT0 = 2000;
# LaceAlsThresholdT1 = 5000;
# LaceAlsThresholdT2 = 10000;
# LaceT1MaxSlope = 150;
# LaceT2MaxSlope = 250

##
# DISPLAY_LACE_AGGRESSIVENESS_MODERATE = LaceAggressivenessLevel = 1
# LaceAlsThresholdT0 = 500;
# LaceAlsThresholdT1 = 1500;
# LaceAlsThresholdT2 = 5000;
# LaceT1MaxSlope = 250;
# LaceT2MaxSlope = 700;

##
# DISPLAY_LACE_AGGRESSIVENESS_HIGH = LaceAggressivenessLevel = 2
# LaceAlsThresholdT0 = 250;
# LaceAlsThresholdT1 = 750;
# LaceAlsThresholdT2 = 2500;
# LaceT1MaxSlope = 250;
# LaceT2MaxSlope = 700;

AGGR_LEVEL_T0_LOW = 2000
AGGR_LEVEL_T0_MODERATE = 500
AGGR_LEVEL_T0_HIGH = 250

AGGR_LEVEL_LOW = 0
AGGR_LEVEL_MODERATE = 1
AGGR_LEVEL_HIGH = 2

def ROUND_UP_DIV(x, y):
    if (x % y == 0):
        result = int(x / y)
    else:
        result = int(math.ceil((x) / (y)))
    return result


def get_actual_lace_status(current_pipe):
    dplc_ctl_reg = 'DPLC_CTL' + '_' + current_pipe
    dplc_ctl_reg_value = reg_read.read('DPLC_CTL_REGISTER', dplc_ctl_reg, platform)
    if dplc_ctl_reg_value.__getattribute__("function_enable") == getattr(dplc_reg, 'function_enable_ENABLE'):
        return "ENABLED"
    return "DISABLED"

def get_t0_value():
    t0_for_each_aggr_level = []
    default_t0_for_each_aggr_level = [AGGR_LEVEL_T0_LOW, AGGR_LEVEL_T0_MODERATE, AGGR_LEVEL_T0_HIGH]
    t0_registry_customization_list = ["LaceMinLuxForLowAggressiveness", "LaceMinLuxForModerateAggressiveness",
                                      "LaceMinLuxForHighAggressiveness"]
    for index in range(len(t0_registry_customization_list)):
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        t0_value, reg_type = registry_access.read(args=reg_args, reg_name=t0_registry_customization_list[index])
        if t0_value:
            t0_for_each_aggr_level.insert(index,t0_value)
        else:
            t0_for_each_aggr_level.insert(index,default_t0_for_each_aggr_level[index])

    return t0_for_each_aggr_level

def get_expected_lace_status(lux, aggressiveness_level):
    t0_for_each_aggr_level = get_t0_value()
    if aggressiveness_level == 0:
        if lux > t0_for_each_aggr_level[AGGR_LEVEL_LOW]:
            return "ENABLED"
    if aggressiveness_level == 1:
        if lux > t0_for_each_aggr_level[AGGR_LEVEL_MODERATE]:
            return "ENABLED"
    if aggressiveness_level == 2:
        if lux > t0_for_each_aggr_level[AGGR_LEVEL_HIGH]:
            return "ENABLED"
    return "DISABLED"


#  Due to high power impact with Fast Lace+video playback,from Gen13+ fast lace was disabled and replaced
#  with legacy lace with DSB and DMC functionality, hence below checks moved to separate function
def verify_fast_lace_register_programming(pipe_id, target_id, lux):
    if (dplc_ctl.fast_access_mode_enable):
        logging.info('PASS: %s - LACE Fast Access mode status: Expected = ENABLE, Actual = ENABLE' % dplc_ctl_reg)
    else:
        gdhm_report_app_color(title="[COLOR][LACE]Failed due to lace fast access mode disabled")
        logging.error(
            'FAIL: %s - LACE  LACE Fast Access mode status: Expected = ENABLE, Actual = DISABLE' % dplc_ctl_reg)
        status = False

    # resolution.VtRes
    part_a_start = 0
    tiles_per_col = int(math.ceil(resolution.VtRes / 256.0))
    part_a_tile_rows = int(math.ceil(
        50 * tiles_per_col / 100.0))  # As per BSpec - int(math.floor(resolution.VtRes/2/TILE_SIZE)+1) 60 -40 split changed to 50 - 50 split in BSpec
    logging.info("******* part_a_tile_rows is %d *********" % part_a_tile_rows)
    part_b_tile_rows = tiles_per_col - part_a_tile_rows
    logging.info("******* part_b_tile_rows is %d *********" % part_b_tile_rows)
    part_a_end = part_a_tile_rows - 1
    part_b_start = part_a_end + 1
    part_b_end = tiles_per_col - 1  # As per BSpec int(math.ceil(resolution.VtRes/TILE_SIZE)-1)
    # As per BSpec part_b_tile_rows = (part_b_end - part_b_start) + 1

    ##
    # Verify DPLC Part Control

    dplc_part_ctl_reg = "DPLC_PART_CTL_" + str_pipe
    dplc_part_ctl = reg_read.read("DPLC_PART_CTL_REGISTER", dplc_part_ctl_reg, platform)

    if (dplc_part_ctl.part_a_start_tile_row == part_a_start):
        logging.info('PASS: %s - LACE Part A Start :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_a_start, dplc_part_ctl.part_a_start_tile_row))
    else:
        gdhm_report_app_color(
            title="[COLOR][LACE]Verification of DPLC Part Control failed due to mismatch of expected Lace part")
        logging.error('FAIL: %s - LACE Part A Start :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_a_start, dplc_part_ctl.part_a_start_tile_row))
        status = False

    if (dplc_part_ctl.part_a_end_tile_row == part_a_end):
        logging.info('PASS: %s - LACE Part A End :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_a_end, dplc_part_ctl.part_a_end_tile_row))
    else:
        gdhm_report_app_color(
            title="[COLOR][LACE]Verification of DPLC Part Control failed due to mismatch of expected Lace part")
        logging.error('FAIL: %s - LACE Part A End :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_a_end, dplc_part_ctl.part_a_end_tile_row))
        status = False

    if (dplc_part_ctl.part_b_start_tile_row == part_b_start):
        logging.info('PASS: %s - LACE Part B Start :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_b_start, dplc_part_ctl.part_b_start_tile_row))
    else:
        gdhm_report_app_color(
            title="[COLOR][LACE]Verification of DPLC Part Control failed due to mismatch of expected Lace part")
        logging.error('FAIL: %s - LACE Part B Start :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_b_start, dplc_part_ctl.part_b_start_tile_row))
        status = False

    if (dplc_part_ctl.part_b_end_tile_row == part_b_end):
        logging.info('PASS: %s - LACE Part B End :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_b_end, dplc_part_ctl.part_b_end_tile_row))
    else:
        gdhm_report_app_color(
            title="[COLOR][LACE]Verification of DPLC Part Control failed due to mismatch of expected Lace part")
        logging.error('FAIL: %s - LACE Part B End :Expected = %d, Actual = %d ' % (
            dplc_part_ctl_reg, part_b_end, dplc_part_ctl.part_b_end_tile_row))
        status = False

    ##
    # Verify DPLC Pointer Config

    part_a_x_index = 0
    part_a_y_index = 0
    part_a_dw_index = 0
    part_b_x_index = 0
    part_b_y_index = part_b_start
    part_b_dw_index = 0

    dplc_ptr_config_partA_reg = "DPLC_PTRCFG_PARTA_" + str_pipe
    dplc_ptr_config_partA = reg_read.read("DPLC_PTRCFG_REGISTER", dplc_ptr_config_partA_reg, platform)

    if (
            dplc_ptr_config_partA.x_index == part_a_x_index and dplc_ptr_config_partA.y_index == part_a_y_index and dplc_ptr_config_partA.dw_index == part_a_dw_index):
        logging.info(
            'PASS: %s - LACE Ptr Config Part A - X Index : Expected = %d, Actual = %d  , Y Index : Expected = %d, Actual = %d , DW Bin Index : Expected = %d, Actual = %d'
            % (dplc_ptr_config_partA_reg, part_a_x_index, dplc_ptr_config_partA.x_index, part_a_y_index,
               dplc_ptr_config_partA.y_index, part_a_dw_index, dplc_ptr_config_partA.dw_index))
    else:
        gdhm_report_app_color(
            title="[COLOR][LACE]Verification of DPLC Ptr Config failed due to mismatch of expected LACE Ptr Config for part")
        logging.error(
            'FAIL: %s - LACE Ptr Config Part A- X Index : Expected = %d, Actual = %d  , Y Index : Expected = %d, Actual = %d , DW Bin Index : Expected = %d, Actual = %d'
            % (dplc_ptr_config_partA_reg, part_a_x_index, dplc_ptr_config_partA.x_index, part_a_y_index,
               dplc_ptr_config_partA.y_index, part_a_dw_index, dplc_ptr_config_partA.dw_index))
        status = False

    dplc_ptr_config_partB_reg = "DPLC_PTRCFG_PARTB_" + str_pipe
    dplc_ptr_config_partB = reg_read.read("DPLC_PTRCFG_REGISTER", dplc_ptr_config_partB_reg, platform)

    if (
            dplc_ptr_config_partB.x_index == part_b_x_index and dplc_ptr_config_partB.y_index == part_b_y_index and dplc_ptr_config_partB.dw_index == part_b_dw_index):
        logging.info(
            'PASS: %s - LACE Ptr Config Part B - X Index : Expected = %d, Actual = %d  , Y Index : Expected = %d, Actual = %d , DW Bin Index : Expected = %d, Actual = %d'
            % (dplc_ptr_config_partB_reg, part_b_x_index, dplc_ptr_config_partB.x_index, part_b_y_index,
               dplc_ptr_config_partB.y_index, part_b_dw_index, dplc_ptr_config_partB.dw_index))
    else:
        gdhm_report_app_color(
            title="[COLOR][LACE]Verification of DPLC Ptr Config failed due to mismatch of expected LACE Ptr Config part")
        logging.error(
            'FAIL: %s - LACE Ptr Config Part B - X Index : Expected = %d, Actual = %d  , Y Index : Expected = %d, Actual = %d , DW Bin Index : Expected = %d, Actual = %d'
            % (dplc_ptr_config_partB_reg, part_b_x_index, dplc_ptr_config_partB.x_index, part_b_y_index,
               dplc_ptr_config_partB.y_index, part_b_dw_index, dplc_ptr_config_partB.dw_index))
        status = False

    ##
    # Verify  DPLC Read Length

    tile_columns = int(math.ceil(resolution.HzRes / TILE_SIZE))
    part_a_read_length = int(math.ceil(part_a_tile_rows * tile_columns * HIST_BIN_SIZE) / 16)
    part_b_read_length = int(math.ceil(part_b_tile_rows * tile_columns * HIST_BIN_SIZE) / 16)

    dplc_rdlength_partA_reg = "DPLC_RDLENGTH_PARTA_" + str_pipe
    dplc_rdlength_partA = reg_read.read("DPLC_RDLENGTH_REGISTER", dplc_rdlength_partA_reg, platform)

    if (dplc_rdlength_partA.read_length == part_a_read_length):
        logging.info('PASS: %s - LACE Read Length Part A : Expected = %d, Actual = %d ' % (
            dplc_rdlength_partA_reg, part_a_read_length, dplc_rdlength_partA.read_length))
    else:
        gdhm_report_app_color(title="[COLOR][LACE]Failed due to mismatch of expected LACE Read Length part")
        logging.error('FAIL: %s - LACE Read Length Part A : Expected = %d, Actual = %d ' % (
            dplc_rdlength_partA_reg, part_a_read_length, dplc_rdlength_partA.read_length))
        status = False

    dplc_rdlength_partB_reg = "DPLC_RDLENGTH_PARTB_" + str_pipe
    dplc_rdlength_partB = reg_read.read("DPLC_RDLENGTH_REGISTER", dplc_rdlength_partB_reg, platform)

    if (dplc_rdlength_partB.read_length == part_b_read_length):
        logging.info('PASS: %s - LACE Read Length Part B : Expected = %d, Actual = %d ' % (
            dplc_rdlength_partB_reg, part_b_read_length, dplc_rdlength_partB.read_length))
    else:
        gdhm_report_app_color(title="[COLOR][LACE]Failed due to mismatch of expected LACE Read Length part")
        logging.error('FAIL: %s - LACE Read Length Part B : Expected = %d, Actual = %d ' % (
            dplc_rdlength_partB_reg, part_b_read_length, dplc_rdlength_partB.read_length))
        status = False


def verify_lace_register_programming(pipe_id, target_id, lux):
    status = True
    str_pipe = chr(int(pipe_id) + 65)

    config = DisplayConfiguration()
    resolution = config.get_current_mode(target_id)

    # TODO : Verify pipe DMC load

    ##
    # Verify DPLC Control

    dplc_ctl_reg = "DPLC_CTL_" + str_pipe
    dplc_ctl = reg_read.read("DPLC_CTL_REGISTER", dplc_ctl_reg, platform)

    ##
    # Verification for LACE disable
    if (lux < 500):
        if (dplc_ctl.function_enable == 0):
            logging.info(
                'PASS: %s - LACE Function enable status for Lux %d : Expected = DISABLE, Actual = DISABLE' % (
                    dplc_ctl_reg, lux))
        else:
            gdhm_report_app_color(title="[COLOR][LACE]Failed due to lace enabled for lux<500")
            logging.error(
                'FALSE: %s - LACE Function enable status for Lux %d : Expected = DISABLE, Actual = ENABLE' % (
                    dplc_ctl_reg, lux))
            status = False

        return status

    # LACE status
    if (dplc_ctl.function_enable):
        logging.info('PASS: %s - LACE Function enable status: Expected = ENABLE, Actual = ENABLE' % dplc_ctl_reg)
    else:
        gdhm_report_app_color(title="[COLOR][LACE]Failed due to lace disabled")
        logging.error('FAIL: %s - LACE Function enable status: Expected = ENABLE, Actual = DISABLE' % dplc_ctl_reg)
        status = False

    # LACE IE Enable - will be enabled only when IE of part A & B is complete so cant be checked during initialization
    if (dplc_ctl.ie_enable):
        logging.info('PASS: %s - LACE IE Enable status: Expected = ENABLE, Actual = ENABLE' % dplc_ctl_reg)
    else:
        gdhm_report_app_color(title="[COLOR][LACE]Failed due to lace IE disabled")
        logging.error('FAIL: %s - LACE IE Enable status: Expected = ENABLE, Actual = DISABLE' % dplc_ctl_reg)
        status = False

    # LACE Orientation - Landscape/Portrait
    if resolution.HzRes > resolution.VtRes:
        if dplc_ctl.orientation == 0:  # Landscape
            logging.info('PASS: %s - LACE Orientation : Expected = LANDSCAPE, Actual = LANDSCAPE' % dplc_ctl_reg)
        else:
            gdhm_report_app_color(title="[COLOR][LACE]Failed due to mismatch of lace orientation type")
            logging.error('FAIL: %s - LACE Orientation : Expected = LANDSCAPE, Actual = PORTRAIT' % dplc_ctl_reg)
            status = False
    else:
        if dplc_ctl.orientation == 1:  # Portrait
            logging.info('PASS: %s - LACE Orientation : Expected = PORTRAIT, Actual = PORTRAIT' % dplc_ctl_reg)
        else:
            gdhm_report_app_color(title="[COLOR][LACE]Failed due to mismatch of lace orientation type")
            logging.error('FAIL: %s - LACE Orientation : Expected = PORTRAIT , Actual = LANDSCAPE' % dplc_ctl_reg)
            status = False

    # LACE Enhancement mode - Direct/Multiplicative
    if (dplc_ctl.enhancement_mode == 1):
        logging.info(
            'PASS: %s - LACE Enhancement mode status: Expected = MULTIPLICATIVE, Actual = MULTIPLICATIVE' % dplc_ctl_reg)
    else:
        gdhm_report_app_color(title="[COLOR][LACE]Failed due to lace Enhancement mode was Direct")
        logging.error(
            'FAIL: %s - LACE Enhancement mode status: Expected = MULTIPLICATIVE, Actual = DIRECT/RESERVED' % dplc_ctl_reg)
        status = False

    # LACE Tile Size
    if (dplc_ctl.tile_size == 0):
        logging.info('PASS: %s - LACE Tile Size : Expected = 256X256, Actual = 256X256' % dplc_ctl_reg)
    else:
        gdhm_report_app_color(title="[COLOR][LACE]Failed due to lace tile size was 128x128")
        logging.error('FAIL: %s - LACE Tile Size : Expected = 256X256, Actual = 128X128' % dplc_ctl_reg)
        status = False

    return status
