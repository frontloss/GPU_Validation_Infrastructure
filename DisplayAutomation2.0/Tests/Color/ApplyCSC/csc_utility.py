#######################################################################################################################
# @file         csc_utility.py
# @addtogroup   Test_Color
# @section      csc_utility
# @remarks      @ref csc_utility.py \n
#               The script contains helper functions used by the ApplyCSC tests.
# @author       Smitha B
#######################################################################################################################
import math
import ctypes
import itertools
import logging

from Libs.Core.sw_sim import driver_interface
from registers.mmioregister import MMIORegister
from Tests.Color import color_common_utility
from Libs.Feature.presi.presi_crc import start_plane_processing
from Libs.Core import system_utility
from Tests.Planes.Common import planes_helper


##
# Utility to convert from double to 15.16 format
def convert_csc_to_16bit(csc_matrix):
    for row in range(0,3):
        for col in range(0,3):
            csc_matrix[row][col] = csc_matrix[row][col] * 65536
    logging.debug("CSC Matrix after conversion")
    logging.debug(csc_matrix)
    return csc_matrix


##
# Utility to round up the matrix values
def round_up(csc_matrix):
    for row in range(0,3):
        for col in range(0,3):
            csc_matrix[row][col] = round(csc_matrix[row][col])
    return csc_matrix


##
# Utility to prepare the coefficients to be passed as an input to the escape call
def create_15_16_format_csc_matrix(csc_coefficients):
    csc_matrix = [[],[],[]]
    coefficients = [ctypes.c_int32(i) for i in range(0, 9)]
    csc_matrix = convert_csc_to_16bit(csc_coefficients)
    csc_matrix = round_up(csc_matrix)
    coefficients = list(itertools.chain.from_iterable(csc_matrix))
    logging.debug("CSC Matrix as coefficients")
    logging.debug(coefficients)
    return coefficients


##
# Utility to convert CSC Coefficients from register format as float coefficients(defined as per BSpec)
def convert_csc_regformat_to_coeff(csc_coeff):
    position_of_point_from_right = 0

    sign_bit = color_common_utility.get_bit_value(csc_coeff, 15, 15)
    exponent = color_common_utility.get_bit_value(csc_coeff, 12, 14)
    mantissa = int(color_common_utility.get_bit_value(csc_coeff, 3, 11))

    if exponent == 6:
        position_of_point_from_right = 7
    elif exponent == 7:
        position_of_point_from_right = 8
    elif exponent == 0:
        position_of_point_from_right = 9
    elif exponent == 1:
        position_of_point_from_right = 10
    elif exponent == 2:
        position_of_point_from_right = 11
    elif exponent == 3:
        position_of_point_from_right = 12

    scale_factor = math.pow(2.0, float(position_of_point_from_right))
    out_val = float(mantissa) / scale_factor
    if sign_bit:
        out_val = out_val * -1

    return out_val


##
# Utility to fetch the CSC coefficients from register
def get_csc_coeff_matrix_from_reg(unit_name, current_pipe):
    platform = color_common_utility.get_platform_info()
    programmed_val = [[0,0,0],[0,0,0],[0,0,0]]
    csc_coeff = [[0,0,0],[0,0,0],[0,0,0]]

    module_name = unit_name + "_REGISTER"
    reg_name = unit_name +"_" + current_pipe
    instance = MMIORegister.get_instance(module_name, reg_name,platform)
    base_offset = instance.offset
    for i in range(0,3):
        offset = ( base_offset + i*8 ) # 2 DWORDS for each row RGB
        reg_val = driver_interface.DriverInterface().mmio_read(offset, 'gfx_0')
        csc_reg = MMIORegister.get_instance(module_name,reg_name,platform,reg_val)
        programmed_val[i][0] = csc_reg.coeff1
        programmed_val[i][1] = csc_reg.coeff2
        reg_val = driver_interface.DriverInterface().mmio_read(offset + 4, 'gfx_0')
        csc_reg =MMIORegister.get_instance(module_name,reg_name,platform,reg_val)
        programmed_val[i][2] = csc_reg.coeff1

    for i in range(0, 3):
        for j in range(0, 3):
            csc_coeff[i][j] = convert_csc_regformat_to_coeff(programmed_val[i][j])

    return csc_coeff


##
# Utility to identify whether the csc matrix is Identity or otherwise
def identify_csc_matrix_type(csc_matrix):
    reference_identity_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    if csc_matrix == reference_identity_matrix:
        return "IDENTITY"
    return "NON_IDENTITY"


##
# Utility to compare programmed and reference CSC.
# In case of an Identity CSC, difference between programmed and reference should be 0
# In Non-Identity case, an error of difference of 0.005 is accepted
def compare_csc_coeff(prog_csc_val, ref_csc_value, reg_name):
    threshold = 0 if identify_csc_matrix_type(ref_csc_value) == "IDENTITY" else 0.005
    logging.debug("Programmed CSC Value is %s" %prog_csc_val)
    logging.debug("Reference CSC Value is %s" %ref_csc_value)
    result = True
    for i in range(0,3):
        for j in range(0,3):
            if prog_csc_val[i][j] * ref_csc_value[i][j] >= 0.0:  # Same sign
                logging.debug("Difference in value is %s" %(math.fabs(prog_csc_val[i][j] - ref_csc_value[i][j])))
                if math.fabs(prog_csc_val[i][j] - ref_csc_value[i][j]) > threshold:
                    logging.error("FAIL: %s - Coeff values didn't match pos : (%d,%d) Expected Val = %f Programmed Val = %f",
                                  reg_name, i, j, ref_csc_value[i][j], prog_csc_val[i][j])
                    result = False
            else:
                result = False
    return result


##
# Verify DeGamma, CSC and Gamma Blocks
def verify_degamma_csc_gamma_blocks(ref_csc_value, display, csc_type, hdr_mode=False, color_conv_blk="cc1"):
    sys_util = system_utility.SystemUtility()
    exec_env = sys_util.get_execution_environment_type()
    if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_adapter_index='gfx_0'):
        start_plane_processing()
    ##
    # Verify if de-gamma is enabled
    current_pipe = color_common_utility.get_current_pipe(display)
    platform = color_common_utility.get_platform_info()
    gamma_reg_name = "GAMMA_MODE" + "_" + current_pipe
    gamma_mode_reg = MMIORegister.read("GAMMA_MODE_REGISTER", gamma_reg_name, platform)
    csc_reg_name = "CSC_COEFF" if color_conv_blk == "cc1" else "CSC_CC2_COEFF"
    ##
    # In case of Linear CSC, need to check DeGamma and Gamma Enable bits
    if csc_type == 0:
        if color_conv_blk == "cc1":
            if hdr_mode:
                if gamma_mode_reg.pre_csc_gamma_enable:
                    logging.error("FAIL: Pipe Pre CSC Gamma : Expected = DISABLE Actual = ENABLE")
                    color_common_utility.gdhm_report_app_color("[COLOR][ApplyCSC]Register verification failed due to pipe pre csc gamma enabled in HDR mode")
                    return False
                else:
                    logging.info("PASS: In HDR Mode, Pipe Pre CSC Gamma : Expected = DISABLE Actual = DISABLE")
            else:
                if gamma_mode_reg.pre_csc_gamma_enable:
                    logging.info("PASS: Pipe Pre CSC Gamma : Expected = ENABLE Actual = ENABLE")
                else:
                    color_common_utility.gdhm_report_app_color(
                        "[COLOR][ApplyCSC]Register verification failed due to pipe pre csc gamma enabled in Non-HDR mode")
                    logging.error("FAIL: Pipe Pre CSC Gamma : Expected = ENABLE Actual = DISABLE")
                    return False
        else:
            if hdr_mode:
                if gamma_mode_reg.pre_csc_cc2_gamma_enable:
                    color_common_utility.gdhm_report_app_color(
                        "[COLOR][ApplyCSC]Register verification failed due to pipe pre csc cc2 gamma enabled in HDR mode")
                    logging.error("FAIL: Pipe Pre CSC CC2 Gamma : Expected = DISABLE Actual = ENABLE")
                    return False
                else:
                    logging.info("PASS: In HDR Mode, Pipe Pre CSC CC2 Gamma : Expected = DISABLE Actual = DISABLE")
            else:
                if gamma_mode_reg.pre_csc_cc2_gamma_enable:
                    logging.info("PASS: Pipe Pre CSC CC2 Gamma : Expected = ENABLE Actual = ENABLE")
                else:
                    color_common_utility.gdhm_report_app_color(
                        "[COLOR][ApplyCSC]Register verification failed due to pipe pre csc cc2 gamma enabled in Non-HDR mode")
                    logging.error("FAIL: Pipe Pre CSC CC2 Gamma : Expected = ENABLE Actual = DISABLE")
                    return False

        ##
        # Verify Pipe CSC
        prog_csc_val = get_csc_coeff_matrix_from_reg(csc_reg_name, current_pipe)
        if compare_csc_coeff(prog_csc_val, ref_csc_value, csc_reg_name):
            logging.info("SUCCESS : CSC Coefficients Match")
        else:
            logging.error("FAIL : CSC Coefficients NOT matching")
            return False

        ##
        # Verify Pipe Gamma
        if color_conv_blk == "cc1":
            if gamma_mode_reg.post_csc_gamma_enable == 1:
                logging.info("PASS: Pipe Post CSC Gamma : Expected = ENABLE, Actual = ENABLE")
            else:
                color_common_utility.gdhm_report_app_color(
                    "[COLOR][ApplyCSC]Register verification failed due to pipe post csc gamma disabled")
                logging.error("FAIL: Pipe Post CSC Gamma : Expected = ENABLE, Actual = DISABLE")
                return False
        else:
            if gamma_mode_reg.post_csc_cc2_gamma_enable == 1:
                logging.info("PASS: Pipe Post CSC CC2 Gamma  : Expected = ENABLE, Actual = ENABLE")
            else:
                color_common_utility.gdhm_report_app_color(
                    "[COLOR][ApplyCSC]Register verification failed due to pipe post csc cc2 gamma disabled")
                logging.error("FAIL: Pipe Post CSC CC2 Gamma : Expected = ENABLE, Actual = DISABLE")
                return False
    else:
        prog_csc_val = get_csc_coeff_matrix_from_reg("OUTPUT_CSC_COEFF", current_pipe)
        if compare_csc_coeff(prog_csc_val, ref_csc_value, "OUTPUT_CSC_COEFF"):
            logging.info("SUCCESS : CSC Coefficients Match")
        else:
            title = "[COLOR][ApplyCSC] Failed due to comparsion of Output csc coeff mismatch"
            color_common_utility.gdhm_report_app_color(title=title)
            logging.error("FAIL : CSC Coefficients NOT matching")
            return False
    return True

