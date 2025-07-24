#######################################################################################################################
# @file         csc_utility.py
# @brief        The script contains helper functions used by the color test.
#               1)convert_csc_regformat_to_coeff()
#               2)compare_csc_coeff()
#               3)generate_color_transforms_reference_csc_matrix()
#               4)identify_csc_matrix_type()
#               5)matrix_multiply_3x3()
#               6)get_csc_coeffmatrix_from_reg()
#               7)transform_yuv_to_rgb_matrix()
#               8)get_csc_offsets_from_reg()
#               9)transform_rgb_to_yuv_matrix()
#               10)multiply_csc_with_scale_factor()
#               11)get_offsets_for_range_conversion()
# @author       Vimalesh D
#######################################################################################################################
import ctypes
import itertools
import logging
import math
import time
import DisplayRegs
from DisplayRegs.DisplayOffsets import PipeCscCoeffOffsetValues, PlaneCscCoeffOffsetValues, \
    PipeCscPrePostOffsetValues, PlaneCscPrePostOffsetValues, AviInfoOffsetsValues, TransDDiOffsetsValues
from Tests.Color.Common import color_constants, common_utility, color_enums
from Tests.Color.Common.color_enums import ColorSpace, ConversionType
from Libs.Feature.presi.presi_crc import start_plane_processing
from Libs.Core import system_utility
from Tests.Planes.Common import planes_helper


##
# @brief        Function to convert CSC Coefficients from register format as float coefficients
# @param[in]    csc_coeff - register format
# @return       out_val - float coefficients - float point format
def convert_csc_regformat_to_coeff(csc_coeff):
    position_of_point_from_right = 0

    ##
    # need to confirm for git_bit_value definition
    sign_bit = common_utility.get_bit_value(csc_coeff, 15, 15)
    exponent = common_utility.get_bit_value(csc_coeff, 12, 14)
    mantissa = int(common_utility.get_bit_value(csc_coeff, 3, 11))

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
# @brief        Function to compare programmed and reference CSC.
#               In case of an Identity CSC, difference between programmed and reference should be 0
#               In Non-Identity case, an error of difference of 0.005 is accepted
# @param[in]    prog_csc_coeff - Programmed csc value - matrix format i,j
# @param[in]    ref_csc_coeff - Reference csc value - matrix format i,j
# @return       status - True or False
def compare_csc_coeff(prog_csc_coeff, ref_csc_coeff):
    status = True
    threshold = 0 if identify_csc_matrix_type(
        ref_csc_coeff) == "IDENTITY" else color_constants.CSC_GAMMA_DEVIATION_THRESHOLD
    for i in range(0, 3):
        for j in range(0, 3):
            if prog_csc_coeff[i][j] * ref_csc_coeff[i][j] >= 0.0:  # Same sign
                if math.fabs(prog_csc_coeff[i][j] - ref_csc_coeff[i][j]) > threshold:
                    logging.error("Coeff values didn't match at ({0},{1}) Expected Val = {2} " \
                                  "Programmed Val = {3}".format(i, j, ref_csc_coeff[i][j],
                                                                prog_csc_coeff[i][j]))
                    status = False
            else:
                logging.error("Coeff sign didn't match at ({0},{1}) Expected Val = {2} " \
                              "Programmed Val = {3}".format(i, j, ref_csc_coeff[i][j],
                                                            prog_csc_coeff[i][j]))
                status = False
    if not status:
        logging.debug("Programmed CSC : {0}".format(prog_csc_coeff))
        logging.debug("Reference CSC  : {0}".format(ref_csc_coeff))

    return status


##
# @brief        Function to compare programmed and reference CSC.
#               In case of an Identity CSC, difference between programmed and reference should be 0
#               In Non-Identity case, an error of difference of 0.005 is accepted
# @param[in]    prog_csc_coeff - Programmed csc value - matrix format i,j
# @param[in]    ref_csc_coeff - Reference csc value - matrix format i,j
# @return       status - True or False
# @todo : Removal of the WA after deb0ug of CSC issue
def wa_compare_csc_coeff(prog_csc_coeff, ref_csc_coeff):
    status = True
    threshold = color_constants.WA_CSC_GAMMA_DEVIATION_THRESHOLD
    for i in range(0, 3):
        for j in range(0, 3):
            if prog_csc_coeff[i][j] * ref_csc_coeff[i][j] >= 0.0:  # Same sign
                if math.fabs(prog_csc_coeff[i][j] - ref_csc_coeff[i][j]) > threshold:
                    logging.error("Coeff values didn't match at ({0},{1}) Expected Val = {2} " \
                                  "Programmed Val = {3}".format(i, j, ref_csc_coeff[i][j],
                                                                prog_csc_coeff[i][j]))
                    status = False
            else:
                logging.error("Coeff sign didn't match at ({0},{1}) Expected Val = {2} " \
                              "Programmed Val = {3}".format(i, j, ref_csc_coeff[i][j],
                                                            prog_csc_coeff[i][j]))
                status = False
    if not status:
        logging.debug("Programmed CSC : {0}".format(prog_csc_coeff))
        logging.debug("Reference CSC  : {0}".format(ref_csc_coeff))

    return status


##
# @brief        Function to generate reference XYZ - RGB matrix, based on SDR or HDR Mode
# @param[in]    os_csc_data
# @param[in]    hdr_mode - bool True or False
# @return       reference_matrix
def generate_color_transforms_reference_csc_matrix(os_csc_data, hdr_mode: bool):
    if hdr_mode:
        rgb_xyz_matrix = color_constants.BT2020_RGB_to_XYZ_conversion
        xyz_rgb_matrix = color_constants.XYZ_to_BT2020_RGB_conversion
    else:
        rgb_xyz_matrix = color_constants.BT709_RGB_to_XYZ_conversion
        xyz_rgb_matrix = color_constants.XYZ_to_BT709_RGB_conversion

    inter_matrix = matrix_multiply_3x3(os_csc_data, rgb_xyz_matrix)
    reference_matrix = matrix_multiply_3x3(xyz_rgb_matrix, inter_matrix)
    return reference_matrix


##
# @brief        Function to check Identity or Non-Identity Matrix
# @param[in]    csc_matrix - 3*3 matrix
# @return       matrix_type - Identity,Non-Identity
def identify_csc_matrix_type(csc_matrix):
    reference_identity_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    matrix_type = "NON_IDENTITY"
    if csc_matrix == reference_identity_matrix:
        matrix_type = "IDENTITY"
    return matrix_type


##
# @brief        Function to do matrix multiplication
# @param[in]    matrix1 - matrix format i,j
# @param[in]    matrix2 -  matrix format i,j
# @return       resultant_matrix
def matrix_multiply_3x3(matrix1, matrix2):
    resultant_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # iterate through rows of X
    for i in range(len(matrix1)):
        # iterate through columns of Y
        for j in range(len(matrix2[0])):
            # iterate through rows of Y
            for k in range(len(matrix2)):
                resultant_matrix[i][j] += round(matrix1[i][k], 5) * round(matrix2[k][j], 5)

    return resultant_matrix


##
# @brief         Function to get csc coeff matrix from register
# @param[in]     gfx_index - gfx adapter index
# @param[in]     pipe - current pipe
# @param[in]     reg_name - name of the register as in dataoffsets for ex: PipeCscCoeff, PipeCscCc2Coeff,
#                PipeOutputCscCoeff
# @param[in]     reg_interface - register interface
# @param[in]     mmio_interface - mmio_interface
# @return        csc_coeff_values - matrix format i,j
def get_pipe_csc_coeffmatrix_from_reg(gfx_index: str, pipe: str, reg_name: str, reg_interface, mmio_interface):
    sys_util = system_utility.SystemUtility()
    exec_env = sys_util.get_execution_environment_type()
    if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_index):
        start_plane_processing()
    coeff_index = 0
    coeff_offset_value = []
    temp_list = ["", "", "", "", "", ""]
    programmed_val = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    csc_coeff_values = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    pipe_csc_coeff_attr_list = [attr for attr in dir(PipeCscCoeffOffsetValues()) if
                                not callable(getattr(PipeCscCoeffOffsetValues(), attr)) and not attr.startswith("__")]

    csc_coeff_obj = reg_interface.get_pipe_csc_coeff_offsets(pipe)
    offset_list = getattr(csc_coeff_obj, reg_name)

    # Adding delay of 1 Secs before MMIO Read
    time.sleep(1)

    for offset in offset_list:
        coeff_offset_value.append(mmio_interface.read(gfx_index, offset))

    for index in range(0, len(pipe_csc_coeff_attr_list)):
        if pipe_csc_coeff_attr_list[index] == reg_name:
            setattr(csc_coeff_obj, reg_name, coeff_offset_value)
        else:
            setattr(csc_coeff_obj, pipe_csc_coeff_attr_list[index], temp_list)

    data_list = reg_interface.get_pipe_csc_coeff_info(pipe, csc_coeff_obj)
    for i in range(0, 3):
        programmed_val[i][0] = data_list.PipeCscCoeffValues[coeff_index].Ry
        programmed_val[i][1] = data_list.PipeCscCoeffValues[coeff_index].Gy
        programmed_val[i][2] = data_list.PipeCscCoeffValues[coeff_index + 1].Ry
        coeff_index = coeff_index + 2
        for j in range(0, 3):
            csc_coeff_values[i][j] = convert_csc_regformat_to_coeff(programmed_val[i][j])

    return csc_coeff_values


##
# @brief         Function to get csc coeff matrix from register
# @param[in]     gfx_index - gfx adapter index
# @param[in]     pipe - current pipe
# @param[in]     plane - Current plane
# @param[in]     reg_name - name of the register as in dataoffsets for ex: PipeCscCoeff, PipeCscCc2Coeff,
#                PipeOutputCscCoeff
# @param[in]     reg_interface - register interface
# @param[in]     mmio_interface - mmio_interface
# @return        csc_coeff_values - matrix format i,j
def get_plane_csc_coeffmatrix_from_reg(gfx_index: str, pipe: str, plane: str, reg_name: str, reg_interface,
                                       mmio_interface):
    coeff_offset_value = []
    temp_list = [0, 0, 0, 0, 0, 0]
    programmed_val = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    csc_coeff_values = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    plane_csc_coeff_attr_list = [attr for attr in dir(PlaneCscCoeffOffsetValues()) if
                                 not callable(getattr(PlaneCscCoeffOffsetValues(), attr)) and not attr.startswith("__")]
    csc_coeff_obj = reg_interface.get_plane_csc_coeff_offsets(pipe, plane)
    offset_list = getattr(csc_coeff_obj, reg_name)

    for offset in offset_list:
        coeff_offset_value.append(mmio_interface.read(gfx_index, offset))

    for index in range(0, len(plane_csc_coeff_attr_list)):
        if plane_csc_coeff_attr_list[index] == reg_name:
            setattr(csc_coeff_obj, reg_name, coeff_offset_value)
            break
        else:
            setattr(csc_coeff_obj, reg_name, temp_list)

    data_list = reg_interface.get_plane_csc_coeff_info(pipe, plane, csc_coeff_obj)
    coeff_index = 0 if reg_name == "PlaneCscCoeff" else 6
    for i in range(0, 3):
        programmed_val[i][0] = data_list.PlaneCscCoeffValues[coeff_index].Ry
        programmed_val[i][1] = data_list.PlaneCscCoeffValues[coeff_index].Gy
        programmed_val[i][2] = data_list.PlaneCscCoeffValues[coeff_index + 1].Ry
        coeff_index = coeff_index + 2
        for j in range(0, 3):
            csc_coeff_values[i][j] = convert_csc_regformat_to_coeff(programmed_val[i][j])

    return csc_coeff_values


##
# @brief         Function to verify pre/port offsets
# @param[in]     gfx_index - gfx adapter index
# @param[in]     reg_interface - gfx adapter index
# @param[in]     reg_name - register_name
# @param[in]     pipe - 'A','B','C','D'
# @param[in]     bpc - 8/10/12
# @param[in]     input - RGB/YCBCR Color space Enum
# @param[in]     output - RGB/YCBCR Color Space Enum
# @param[in]     conv_type - Conversion Type Enum
# @param[in]     mmio_interface - mmio_interface
# @return        status - True on Success, False otherwise
def verify_pipe_pre_post_offsets(reg_interface, gfx_index: str, reg_name: str, pipe: str, bpc, input: ColorSpace,
                                 output: ColorSpace,
                                 conv_type: ConversionType, mmio_interface):
    temp_list = ["", "", ""]
    status = False
    pipe_csc_pre_post_attr_list = [attr for attr in dir(PipeCscPrePostOffsetValues()) if
                                   not callable(getattr(PipeCscPrePostOffsetValues(), attr)) and not attr.startswith(
                                       "__")]
    ref_pre_offset, ref_post_offset = get_ref_pre_post_offsets(input, output, conv_type, bpc)

    # @todo Need to add reg_name.strip("Coeff") + "PreOff" in list once the outputcscpreoff updated
    pre_and_post_off_reg_list = [reg_name.strip("Coeff") + "PostOff"]
    reference_list = [ref_post_offset]

    for i in range(0, len(pre_and_post_off_reg_list)):
        csc_offset_value = []

        csc_offset_obj = reg_interface.get_pipe_csc_pre_post_offsets(pipe)
        offset_list = getattr(csc_offset_obj, pre_and_post_off_reg_list[i])

        for offset in offset_list:
            csc_offset_value.append(mmio_interface.read(gfx_index, offset))

        for index in range(0, len(pipe_csc_pre_post_attr_list)):
            if pipe_csc_pre_post_attr_list[index] == pre_and_post_off_reg_list[i]:
                setattr(csc_offset_obj, pre_and_post_off_reg_list[i], csc_offset_value)
            else:
                setattr(csc_offset_obj, pipe_csc_pre_post_attr_list[index], temp_list)

        programmed_list = reg_interface.get_pipe_csc_pre_post_offset_info(pipe, csc_offset_obj)

        if reference_list[i] == programmed_list.PipeCscPrePostOffsetValues:
            status = True
            logging.info("Programmed : {0}".format(programmed_list.PipeCscPrePostOffsetValues))
            logging.info("Reference  : {0}".format(reference_list[i]))
        else:
            logging.error("Pipe PrePostOffset Verification  for Offset:{0} failed".format(pre_and_post_off_reg_list[i]))
            logging.error("Programmed : {0}".format(programmed_list.PipeCscPrePostOffsetValues))
            logging.error("Reference  : {0}".format(reference_list[i]))
            return status

    return status


##
# @brief         Function to verify pre/port offsets
# @param[in]     gfx_index - gfx adapter index
# @param[in]     reg_interface - gfx adapter index
# @param[in]     reg_name - register_name
# @param[in]     pipe - 'A','B','C','D'
# @param[in]     plane - 1,2,3,4
# @param[in]     bpc - 8/10/12
# @param[in]     input - RGB/YCBCR
# @param[in]     output - RGB/YCBCR
# @param[in]     conv_type - FULL_TO_STUDIO, STUDIO_TO_FULL, STUDIO_TO_STUDIO, FULL_TO_FULL
# @param[in]     mmio_interface - mmio_interface
# @return        status - True on Success, False otherwise
def verify_plane_pre_post_offsets(gfx_index: str, reg_interface, reg_name: str, pipe: str, plane: str, bpc, input,
                                  output,
                                  conv_type, mmio_interface):
    temp_list = ["", "", ""]
    status = False

    plane_csc_pre_post_attr_list = [attr for attr in dir(PlaneCscPrePostOffsetValues()) if
                                    not callable(getattr(PlaneCscPrePostOffsetValues(), attr)) and not attr.startswith(
                                        "__")]
    logging.info("Input : {0} Output : {1} Conversion Type : {2} BPC : {3}".format(input, output, conv_type, bpc))
    ref_pre_offset, ref_post_offset = get_ref_pre_post_offsets(input, output, conv_type, bpc)
    pre_and_post_off_reg_list = [reg_name.strip("Coeff") + "PreOff", reg_name.strip("Coeff") + "PostOff"]
    reference_list = [ref_pre_offset, ref_post_offset]
    for i in range(0, len(pre_and_post_off_reg_list)):
        csc_offset_value = []

        csc_offset_obj = reg_interface.get_plane_csc_pre_post_offsets(plane, pipe)
        offset_list = getattr(csc_offset_obj, pre_and_post_off_reg_list[i])

        for offset in offset_list:
            csc_offset_value.append(mmio_interface.read(gfx_index, offset))

        for index in range(0, len(plane_csc_pre_post_attr_list)):
            if plane_csc_pre_post_attr_list[index] == pre_and_post_off_reg_list[i]:
                setattr(csc_offset_obj, pre_and_post_off_reg_list[i], csc_offset_value)
            else:
                setattr(csc_offset_obj, plane_csc_pre_post_attr_list[index], temp_list)
        programmed_list = reg_interface.get_plane_csc_pre_post_offset_info(pipe, plane, csc_offset_obj)

        if reference_list[i] == programmed_list.PlaneCscPrePostOffsetValues:
            status = True
        else:
            logging.error(
                "Plane PrePostOffset Verification  for Offset:{0} failed".format(pre_and_post_off_reg_list[i]))
            logging.debug("Programmed : {0}".format(programmed_list.PlaneCscPrePostOffsetValues))
            logging.debug("Reference  : {0}".format(reference_list[i]))
            return status

    return status


##
# @brief         Function to transform yuv to rgb matrix
# @param[in]     csc_coeff
# @return        res_coeff
def transform_yuv_to_rgb_matrix(csc_coeff):
    res_coeff = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # Programmed matrix [C3 C1 C2] recreate original matrix [C1 C2 C3]

    res_coeff[0][0] = csc_coeff[0][1]
    res_coeff[1][0] = csc_coeff[1][1]
    res_coeff[2][0] = csc_coeff[2][1]

    res_coeff[0][1] = csc_coeff[0][2]
    res_coeff[1][1] = csc_coeff[1][2]
    res_coeff[2][1] = csc_coeff[2][2]

    res_coeff[0][2] = csc_coeff[0][0]
    res_coeff[1][2] = csc_coeff[1][0]
    res_coeff[2][2] = csc_coeff[2][0]

    return res_coeff


##
# @brief         Function to transform rgb to yuv matrix
# @param[in]     csc_coeff
# @return        res_coeff
# @todo Only skeletons should be added now
def transform_rgb_to_yuv_matrix(csc_coeff):
    res_coeff = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # Programmed matrix [R3 R1 R2] recreate original matrix [R1 R2 R3]
    res_coeff[0][0] = csc_coeff[1][0]
    res_coeff[0][1] = csc_coeff[1][1]
    res_coeff[0][2] = csc_coeff[1][2]

    res_coeff[1][0] = csc_coeff[2][0]
    res_coeff[1][1] = csc_coeff[2][1]
    res_coeff[1][2] = csc_coeff[2][2]

    res_coeff[2][0] = csc_coeff[0][0]
    res_coeff[2][1] = csc_coeff[0][1]
    res_coeff[2][2] = csc_coeff[0][2]

    return res_coeff


##
# @brief         Function to scale the coefficients with scale factor
# @param[in]     bpc
# @param[in]     input
# @param[in]     output
# @param[in]     csc_coeff
# @return        converted_csc
def scale_csc_for_range_conversion(bpc: int, input: ColorSpace, output: ColorSpace, csc_coeff,
                                   conv_type: ConversionType = ConversionType.FULL_TO_STUDIO):
    converted_csc = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    max_pixel_val = (1 << bpc) - 1
    if bpc == 8:
        normalizing_factor = float(1.0 / max_pixel_val)
    else:
        normalizing_factor = (1 << (bpc - 8) & 0xffff) / float(max_pixel_val)
    logging.debug("Normalizing Factor : {0}".format(normalizing_factor))

    # Scale factors calculated for FR to LR conversion
    rgb_y_scalefactor = float(219.0 * normalizing_factor)
    cbcr_scalefactor = float(224.0 * normalizing_factor)

    logging.debug("ScaleFactors : {0} {1}".format(rgb_y_scalefactor, cbcr_scalefactor))

    # Scale factors are inverted for LR to FR conversion
    if conv_type == ConversionType.STUDIO_TO_FULL:
        rgb_y_scalefactor = float(1.0 / rgb_y_scalefactor)
        cbcr_scalefactor = float(1.0 / cbcr_scalefactor)
    elif conv_type == ConversionType.FULL_TO_FULL:
        rgb_y_scalefactor = cbcr_scalefactor = 1

    # All coefficients are scaled using same factor in case of RGB to RGB conversion
    if input == output:  # RGB and RGB
        for i in range(0, 3):
            for j in range(0, 3):
                converted_csc[i][j] = csc_coeff[i][j] * rgb_y_scalefactor

    # Y and Cb/Cr are converted using different scale factors
    elif input != output:  # RGB and YCbCr or YCbCr and RGB
        for i in range(0, 3):
            for j in range(0, 3):
                if i == 0:
                    converted_csc[i][j] = csc_coeff[i][j] * rgb_y_scalefactor
                else:
                    converted_csc[i][j] = csc_coeff[i][j] * cbcr_scalefactor

    return converted_csc


##
# @brief         Function to get offsets for range conversion
# @param[in]     bpc
# @param[in]     input- Colorspace Enum
# @param[in]     output Colorspace Enum
# @param[in]     conv_type ConversionType Enum
# @return        offsets
def get_offsets_for_range_conversion(bpc: int, input: ColorSpace, output: ColorSpace, conv_type: ConversionType):
    offsets = [0, 0, 0]
    max_pixel_val = (1 << bpc) - 1

    if bpc == 8:
        normalizing_factor = 1.0 / max_pixel_val
    else:
        normalizing_factor = (float)(1 << (bpc - 8)) / max_pixel_val

    ##
    # When the conversion type is RGB_FR_TO_RGB_LR
    offsets[0] = offsets[1] = offsets[2] = round(4096.0 * 16.0 * normalizing_factor)
    if input == ColorSpace.RGB and output == ColorSpace.RGB and conv_type == ConversionType.STUDIO_TO_FULL:
        offsets[0] = -offsets[0]
        offsets[1] = -offsets[1]
        offsets[2] = -offsets[2]
    if input == ColorSpace.RGB and output == ColorSpace.RGB and conv_type == ConversionType.FULL_TO_FULL:
        offsets[0] = 0
        offsets[1] = 0
        offsets[2] = 0
    elif input == ColorSpace.RGB and output == ColorSpace.YUV and conv_type == ConversionType.FULL_TO_STUDIO:
        offsets[0] = 2048
        offsets[2] = 2048
    elif input == ColorSpace.RGB and output == ColorSpace.YUV and conv_type == ConversionType.FULL_TO_FULL:
        offsets[0] = 2048
        offsets[1] = 0
        offsets[2] = 2048
    elif input == ColorSpace.YUV and output == ColorSpace.RGB and conv_type == ConversionType.FULL_TO_FULL:
        offsets[0] = 6144  # Here the value is representation of -2048 as a positive number
        offsets[1] = 0
        offsets[2] = 6144  # Here the value is representation of -2048 as a positive number
    elif input == ColorSpace.YUV and output == ColorSpace.RGB and conv_type == ConversionType.STUDIO_TO_FULL:
        offsets[0] = 6144  # Here the value is representation of -2048 as a positive number
        offsets[1] = 0
        offsets[2] = 6144  # Here the value is representation of -2048 as a positive number
    elif input == ColorSpace.YUV and output == ColorSpace.RGB and conv_type == ConversionType.FULL_TO_STUDIO:
        offsets[0] = 6144  # Here the value is representation of -2048 as a positive number
        offsets[1] = 0
        offsets[2] = 6144  # Here the value is representation of -2048 as a positive number
    return offsets


##
# @brief         Function to get pre and post offsets
# @param[in]     input - RGB/YCBCR Color space Enum
# @param[in]     output - RGB/YCBCR Color Space Enum
# @param[in]     conv_type - Conversion Type Enum
# @param[in]     bpc - 8/10/12
# @return        ref_pre_offset, ref_post_offset - offset list
def get_ref_pre_post_offsets(input: ColorSpace, output: ColorSpace, conv_type: ConversionType, bpc: int):
    ref_pre_offset = [0, 0, 0]
    ref_post_offset = [0, 0, 0]
    if input == ColorSpace.RGB and output == ColorSpace.YUV:
        ref_pre_offset = [0, 0, 0]
        ref_post_offset = get_offsets_for_range_conversion(bpc, input, output, conv_type)
    elif input == ColorSpace.YUV and output == ColorSpace.RGB:
        ref_pre_offset = get_offsets_for_range_conversion(bpc, input, output, conv_type)
        ref_post_offset = [0, 0, 0]
    elif input == ColorSpace.RGB and output == ColorSpace.RGB:
        ref_pre_offset = [0, 0, 0]
        ref_post_offset = get_offsets_for_range_conversion(bpc, input, output, conv_type)
    return ref_pre_offset, ref_post_offset


########################################################################################################################
# @todo All the functions in the block are skeletons, functions to be updated
########################################################################################################################


##
# @brief         Function to multiple csc with scale factor
# @param[in]     ref_val
# @param[in]     scale_factor
# @return        ref_val1
def multiply_csc_with_scale_factor(ref_val, scale_factor):
    ref_val1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(0, 3):
        for j in range(0, 3):
            ref_val1[i][j] = scale_factor * ref_val[i][j]
    return ref_val1


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


#
# Utility to prepare the coefficients to be passed as an input to the escape call
def create_15_16_format_csc_matrix(csc_coefficients):
    csc_matrix = [[],[],[]]
    coefficients = [ctypes.c_int32(i) for i in range(0, 9)]
    csc_matrix = convert_csc_to_16bit(csc_coefficients)
    csc_matrix = round_up(csc_matrix)
    coefficients = list(itertools.chain.from_iterable(csc_matrix))
    logging.debug("CSC Matrix as coefficients:{0}".format(coefficients))
    return coefficients



#
# Utility to get output range
def get_output_range(gfx_index, platform, plane, pipe, transcoder, mmio_interface):
    sys_util = system_utility.SystemUtility()
    exec_env = sys_util.get_execution_environment_type()
    if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_adapter_index='gfx_0'):
        start_plane_processing()
    quantization_range = None
    transcoder = DisplayRegs.DisplayRegsInterface.TranscoderType(transcoder).name
    trans_ddi_mode_dict = {0: "HDMI", 2: "DP_MST", 3: "DP_SST", 4: "DP2_0_32B_SYMBOL_MODE"}
    regs = DisplayRegs.get_interface(platform, gfx_index)
    trans_ddi_func_offset = regs.get_trans_ddi_offsets(transcoder)

    data = mmio_interface.read(gfx_index, trans_ddi_func_offset.FuncCtrlReg)
    trans_ddi_value = regs.get_trans_ddi_info(transcoder, TransDDiOffsetsValues(FuncCtrlReg=data))
    data_byte = 1
    time.sleep(1) # buffer after modeset for Quant range to set and AVI DIP Bit to set
    avi_dip_offsets = regs.get_avi_info_offsets(data_byte, pipe)
    vdip_ctl_value = mmio_interface.read(gfx_index, avi_dip_offsets.videoDipCtl)
    avi_dip_data = mmio_interface.read(gfx_index, avi_dip_offsets.QuantRange)
    avi_dip_value = regs.get_avi_info(data_byte, pipe, AviInfoOffsetsValues(QuantRange=avi_dip_data,
                                                                        videoDipCtl=vdip_ctl_value))

    if "HDMI" in trans_ddi_mode_dict[trans_ddi_value.DdiModeSelect]:
        logging.info("Output range -> HDMI")
        logging.info("HDMI -> avi_dip_value.vdipctlavi -> {0}".format(avi_dip_value.vdipctlavi))

        output_range = common_utility.get_bit_value(avi_dip_value.QuantRange, 26, 27)
        logging.info("Output range HDMI -> {0}".format(output_range))
        if output_range == 0:
            output_range = color_enums.RgbQuantizationRange.LIMITED.value
        if avi_dip_value.vdipctlavi:
            logging.info("HDMI -> avi_dip_value.vdipctlavi -> {0}".format(avi_dip_value.vdipctlavi))
        else:
            logging.error("HDMI -> avi_dip_value.vdipctlavi -> {0}".format(avi_dip_value.vdipctlavi))
        logging.info("Final Output range -> {0}".format(output_range))
        return int(output_range)
    else:
        vsc_sdp_data_offset = regs.get_vsc_sdp_offsets("5", pipe).QuantRange
        vsc_sdp_data_value = mmio_interface.read(gfx_index, vsc_sdp_data_offset)
        if avi_dip_value.vdipctlvsc:
            output_range = common_utility.get_bit_value(vsc_sdp_data_value, 15, 16)
            if output_range == 0:
                output_range = color_enums.RgbQuantizationRange.FULL.value
            logging.info("Final Output range -> {0}".format(output_range))
            return int(output_range)
        else:
            output_range = color_enums.RgbQuantizationRange.FULL.value
            logging.info("Final Output range -> {0}".format(output_range))
            return int(output_range)
