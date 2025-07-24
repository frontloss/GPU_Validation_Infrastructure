########################################################################################################################
# @file         hdr_verification.py
# @brief        This script contains register verification for color blocks.
# @author       Soorya R,Smitha B
########################################################################################################################

import math
import time
import logging
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core import flip
from Libs.Core.sw_sim import driver_interface
from registers.mmioregister import MMIORegister
from Tests.Color import color_common_utility
from Tests.Planes.Common import hdr_constants

##
# @brief    Types of blending mode
class BLENDINGMODE(object):
    SRGB_NON_LINEAR = 0
    BT2020_NON_LINEAR = 1
    BT2020_LINEAR = 2

##
# @brief    Different panel capabilities
class PANELCAPS(object):
    SDR_709_RGB = 0
    SDR_709_YUV420 = 1
    SDR_BT2020_RGB = 2
    SDR_BT2020_YUV420 = 3
    HDR_BT2020_RGB = 4
    HDR_BT2020_YUV420 = 5
    HDR_DCIP3_RGB = 6
    HDR_DCIP3_YUV420 = 7

##
# @brief    Type of panel
class PANELTYPE:
    LFP = 0
    EFP = 1

##
# @brief    Output range
class OUTPUTRANGE:
    STUDIO = 0
    FULL = 1

##
# @brief    Contains unittest setUp and tearDown functions along with other common helper functions
class HDRVerification(object):
    color_space = None  # RGB/YCBCR
    range = None  # FULL/STUDIO
    gamma = None  # G22/G2084/G10
    gamut = None  # P709/P2020/P601
    str_plane_pipe = None
    str_pipe = None
    platform = None
    plane_csc_scalefactor = 1.0
    color_ctl_reg = None
    threshold = 0.25
    driver_interface_ = driver_interface.DriverInterface()
    machine_info = SystemInfo()
    src_pixel_format = None

    ##
    # @brief        To decode colorspace
    # @param[in]    color_space_enum value
    # @return       None
    def decode_colorspace_enum(self, color_space_enum):

        # With reference to below structure
        # typedef enum D3DDDI_COLOR_SPACE_TYPE
        # {
        #    D3DDDI_COLOR_SPACE_RGB_FULL_G22_NONE_P709             = 0,
        #    D3DDDI_COLOR_SPACE_RGB_FULL_G10_NONE_P709             = 1,
        #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709           = 2,
        #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020          = 3,
        #    D3DDDI_COLOR_SPACE_RESERVED                           = 4,
        #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601      = 5,
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P601         = 6,
        #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P601           = 7,
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P709         = 8,
        #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P709           = 9,
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_LEFT_P2020        = 10,
        #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_LEFT_P2020          = 11,
        #    D3DDDI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020          = 12,
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G2084_LEFT_P2020      = 13,
        #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G2084_NONE_P2020        = 14,
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G22_TOPLEFT_P2020     = 15,
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_G2084_TOPLEFT_P2020   = 16,
        #    D3DDDI_COLOR_SPACE_RGB_FULL_G22_NONE_P2020            = 17,
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_GHLG_TOPLEFT_P2020    = 18,
        #    D3DDDI_COLOR_SPACE_YCBCR_FULL_GHLG_TOPLEFT_P2020      = 19,
        #    D3DDDI_COLOR_SPACE_CUSTOM                             = 0xFFFFFFFF
        # } D3DDDI_COLOR_SPACE_TYPE;

        # color_space
        if color_space_enum in (0, 1, 2, 3, 12, 14, 17):
            self.color_space = "RGB"
        elif color_space_enum in (6, 7, 8, 9, 10, 11, 13, 15, 16):
            self.color_space = "YCBCR"
        else:
            logging.error("ColorSpace enum type not supported !!")
            return False

        # range
        if color_space_enum in (0, 1, 7, 9, 11, 12, 17):
            self.range = "FULL"
        elif color_space_enum in (2, 3, 6, 8, 10, 13, 14, 15, 16):
            self.range = "STUDIO"

        # gamma
        if color_space_enum in (0, 2, 3, 6, 7, 8, 9, 10, 11, 15, 17):
            self.gamma = "G22"
        elif color_space_enum in (12, 13, 14, 16):
            self.gamma = "G2084"
        elif color_space_enum == 1:
            self.gamma = "G10"

        # gamut
        if color_space_enum in (0, 1, 2, 8, 9):
            self.gamut = "P709"
        elif color_space_enum in (6, 7):
            self.gamut = "P601"
        elif color_space_enum in (3, 10, 11, 12, 13, 14, 15, 16, 17):
            self.gamut = "P2020"

        logging.info("Plane Color Attributes : Gamut - %s Gamma - %s Color Space - %s Input range - %s" % (
            self.gamut, self.gamma, self.color_space, self.range))
        return

    ##
    # @brief        To map plane and pipe id to string
    # @param[in]    pipe_id  (0/1/2/3)
    # @param[in]    plane_id (0/1/2/3)
    # @param[in]    is_pipe boolean value to check whether only pipe is present
    # @return       Pipe name if is_pipe is true else string containing pipe and plane details
    def map_plane_pipe_id_to_string(self, pipe_id, plane_id, is_pipe=False):
        str1 = str(plane_id)
        str2 = chr(int(pipe_id) + 65)
        str_plane_pipe = str1 + "_" + str2
        str_pipe = str2
        if (is_pipe is True):
            return str_pipe
        else:
            return str_plane_pipe

    ##
    # @brief        To convert datatype in string to actual datatype
    # @param[in]    value CSC coefficient value
    # @param[in]    start start position of the bit
    # @param[in]    end end position of the bit
    # @return       retvalue value of the bit
    def get_bit_value(self, value, start, end):

        retvalue = value << (31 - end) & 0xffffffff
        retvalue = retvalue >> (31 - end + start) & 0xffffffff
        return retvalue

    ##
    # @brief        To convert CSC register format to coefficient
    # @param[in]    cscCoeff CSC Coefficient value
    # @return       out_val  Coefficients after converting csc register format values
    def convert_csc_regformat_to_coeff(self, cscCoeff):
        out_val = 0.0
        scale_factor = 0.0
        sign_bit = None
        exponent = None
        mantissa = None

        position_of_point_from_right = 0

        sign_bit = self.get_bit_value(cscCoeff, 15, 15)
        exponent = self.get_bit_value(cscCoeff, 12, 14)
        mantissa = int(self.get_bit_value(cscCoeff, 3, 11))

        if (exponent == 6):
            position_of_point_from_right = 7
        elif (exponent == 7):
            position_of_point_from_right = 8
        elif (exponent == 0):
            position_of_point_from_right = 9
        elif (exponent == 1):
            position_of_point_from_right = 10
        elif (exponent == 2):
            position_of_point_from_right = 11
        elif (exponent == 3):
            position_of_point_from_right = 12

        scale_factor = math.pow(2.0, float(position_of_point_from_right))
        out_val = float(mantissa) / scale_factor
        if (sign_bit == 1):
            out_val = out_val * -1

        return out_val

    ##
    # @brief        To get CSC-Coefficient matrix from register
    # @param[in]    unit_name register name
    # @param[in]    str current PIPE name (str_plane_pipe or str_pipe)
    # @return       csc_coeff coefficient matrix
    def get_csc_coeffmatrix_from_reg(self, unit_name, str):
        programmed_val = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        csc_coeff = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        module_name = unit_name + "_REGISTER"
        reg_name = unit_name + "_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
        base_offset = instance.offset
        for i in range(0, 3):
            offset = (base_offset + i * 8)  # 2 DWORDS for each row RGB
            reg_val = self.driver_interface_.mmio_read(offset, 'gfx_0')
            csc_reg = MMIORegister.get_instance(module_name, reg_name, self.platform, reg_val)
            programmed_val[i][0] = csc_reg.coeff1
            programmed_val[i][1] = csc_reg.coeff2
            reg_val = self.driver_interface_.mmio_read(offset + 4, 'gfx_0')
            csc_reg = MMIORegister.get_instance(module_name, reg_name, self.platform, reg_val)
            programmed_val[i][2] = csc_reg.coeff1

        for i in range(0, 3):
            for j in range(0, 3):
                csc_coeff[i][j] = self.convert_csc_regformat_to_coeff(programmed_val[i][j])

        return csc_coeff

    ##
    # @brief        To transform the YUV matrix to RGB matrix
    # @param[in]    csccoeff CSC coefficient matrix
    # @return       rescoeff RGB matrix
    def transform_yuv_to_rgb_matrix(self, csccoeff):
        rescoeff = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        # Programmed matrix [C3 C1 C2] recreate original matrix [C1 C2 C3]

        rescoeff[0][0] = csccoeff[0][1]
        rescoeff[1][0] = csccoeff[1][1]
        rescoeff[2][0] = csccoeff[2][1]

        rescoeff[0][1] = csccoeff[0][2]
        rescoeff[1][1] = csccoeff[1][2]
        rescoeff[2][1] = csccoeff[2][2]

        rescoeff[0][2] = csccoeff[0][0]
        rescoeff[1][2] = csccoeff[1][0]
        rescoeff[2][2] = csccoeff[2][0]

        return rescoeff

    ##
    # @brief        To transform the RGB matrix to YUV matrix
    # @param[in]    csccoeff CSC coefficient matrix
    # @return       rescoeff YUV matrix
    def transform_rgb_to_yuv_matrix(self, csccoeff):
        rescoeff = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # Programmed matrix [R3 R1 R2] recreate original matrix [R1 R2 R3]
        rescoeff[0][0] = csccoeff[1][0]
        rescoeff[0][1] = csccoeff[1][1]
        rescoeff[0][2] = csccoeff[1][2]

        rescoeff[1][0] = csccoeff[2][0]
        rescoeff[1][1] = csccoeff[2][1]
        rescoeff[1][2] = csccoeff[2][2]

        rescoeff[2][0] = csccoeff[0][0]
        rescoeff[2][1] = csccoeff[0][1]
        rescoeff[2][2] = csccoeff[0][2]

        return rescoeff

    ##
    # @brief        To get CSC-Coefficient matrix from register
    # @param[in]    unit_name register name
    # @param[in]    str current PIPE name (str_plane_pipe or str_pipe)
    # @return       csc_coeff coefficient matrix
    def get_csc_offsets_from_reg(self, unit_name, str):
        offsets = [0, 0, 0]
        module_name = unit_name + "_REGISTER"
        reg_name = unit_name + "_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
        base_offset = instance.offset
        for i in range(0, 3):
            base_offset += i * 4
            reg_val = self.driver_interface_.mmio_read(base_offset, 'gfx_0')
            off_reg = MMIORegister.get_instance(module_name, reg_name, self.platform, reg_val)
            offsets[i] = off_reg.precsc_offset
        return offsets

    ##
    # @brief        To compare the csc-coefficients
    # @param[in]    prog_val programmed value
    # @param[in]    ref_val reference value
    # @param[in]    reg_name name of the register
    # @return       True if programmed value and reference value match else False
    def compare_csc_coeff(self, prog_val, ref_val, reg_name):
        logging.info("Programmed Value : %s Reference Value %s" % (prog_val, ref_val))
        result = True
        for i in range(0, 3):
            for j in range(0, 3):
                if (prog_val[i][j] * ref_val[i][j] >= 0.0):  # Same sign
                    if (math.fabs(prog_val[i][j] - ref_val[i][j]) >= self.threshold):
                        logging.error(
                            "FAIL: %s - Coeff values didn't match pos : (%d,%d) Expected Val = %f Programmed Val = %f",
                            reg_name, i, j, ref_val[i][j], prog_val[i][j])
                        result = False
                else:
                    result = False
        return result

    ##
    # @brief        To get gammaLUT values from register
    # @param[in]    unit_name register name
    # @param[in]    no_samples number of samples required
    # @param[in]    str current PIPE name (str_plane_pipe or str_pipe)
    # @return       lut_data coefficient matrix
    def get_gamma_lut_from_reg(self, unit_name, no_samples, str):

        lut_data = []
        # Setting auto increment bit to 1 in index register
        module_name = unit_name + "_INDEX_REGISTER"
        reg_name = unit_name + "_INDEX_" + str
        logging.info("INDEX REGISTER : Module Name : %s  Reg Name : %s", module_name, reg_name)
        instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
        index_offset = instance.offset
        index_reg = MMIORegister.read(module_name, reg_name, self.platform)
        index_reg.index_auto_increment = 1
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
        module_name1 = unit_name + "_INDEX_REGISTER"
        reg_name1 = unit_name + "_INDEX_" + str
        module_name = unit_name + "_DATA_REGISTER"
        reg_name = unit_name + "_DATA_" + str

        for index in range(0, no_samples):
            index_reg.index_value = index
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
            index_reg = MMIORegister.read(module_name1, reg_name1, self.platform)
            data_reg = MMIORegister.read(module_name, reg_name, self.platform)
            lut_data.append(data_reg.gamma_value)

        lut_data.sort()
        return lut_data

    ##
    # @brief        To compare gamma lut
    # @param[in]    prog_lut programmed lut values
    # @param[in]    ref_lut reference lut values
    # @param[in]    reg_name name of the register
    # @return       True if programmed and reference value match else False
    def compare_gamma_lut(self, prog_lut, ref_lut, reg_name):
        result = True
        index = 0
        for reg_val, ref_val in zip(prog_lut, ref_lut):
            if (reg_val != ref_val):
                logging.error(
                    "FAIL: %s - Gamma LUT values not matching Index = %d, Expected Val = %d, Programmed Val = %d",
                    reg_name, index, ref_val, reg_val)
                result = False
            index += 1
        return result

    ##
    # @brief        To multiply csc with scale factor
    # @param[in]    ref_val reference value
    # @param[in]    scale_factor scaling factor
    # @return       ref_val1 matrix with scaled values
    def multiply_csc_with_scale_factor(self, ref_val, scale_factor):
        ref_val1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(0, 3):
            for j in range(0, 3):
                ref_val1[i][j] = scale_factor * ref_val[i][j]
        return ref_val1

    ##
    # @brief        To get pipe gamma lut from register
    # @param[in]    gamma_mode MULTI_SEGMENT or 12BIT_GAMMA mode
    # @param[in]    gamma_lut_unit_name name of the unit register
    # @param[in]    is_ext_registers_available True if external registers are available
    # @return       lut_data
    def get_pipe_gamma_lut_from_reg(self, gamma_mode, gamma_lut_unit_name, is_ext_registers_available=False):

        lut_data = []
        # Palette Prec Data
        if gamma_mode == "LOGARITHMIC":
            lut_size = 1020
        else:
            lut_size = 1024

        if gamma_mode == "MULTI_SEGMENT":
            module_name = "PAL_PREC_MULTI_SEG_INDEX_REGISTER"
            reg_name = "PAL_PREC_MULTI_SEG_INDEX_" + self.str_pipe
            instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
            index_offset = instance.offset
            index_reg = MMIORegister.read(module_name, reg_name, self.platform)
            index_reg.index_auto_increment = 1
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

            # MultiSegment Palette Prec Data
            module_name = "PAL_PREC_MULTI_SEG_DATA_REGISTER"
            reg_name = "PAL_PREC_MULTI_SEG_DATA_" + self.str_pipe
            for index in range(0, 18, 2):
                index_reg.index_value = index
                self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
                data_reg1 = MMIORegister.read(module_name, reg_name, self.platform)
                data_reg2 = MMIORegister.read(module_name, reg_name, self.platform)
                lsb = self.get_bit_value(data_reg1.asUint, 4, 9)
                msb = self.get_bit_value(data_reg2.asUint, 0, 9)
                value = (msb << 6 & 0xffff) + lsb
                lut_data.append(value)

        module_name = gamma_lut_unit_name + "_INDEX_REGISTER"
        reg_name = gamma_lut_unit_name + "_INDEX_" + self.str_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
        index_offset = instance.offset
        index_reg = MMIORegister.read(module_name, reg_name, self.platform)
        index_reg.index_auto_increment = 1
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

        module_name = gamma_lut_unit_name + "_DATA_REGISTER"
        reg_name = gamma_lut_unit_name + "_DATA_" + self.str_pipe
        for index in range(0, lut_size, 2):
            index_reg.index_value = index
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
            data_reg1 = MMIORegister.read(module_name, reg_name, self.platform)
            data_reg2 = MMIORegister.read(module_name, reg_name, self.platform)
            lsb = self.get_bit_value(data_reg1.asUint, 4, 9)
            msb = self.get_bit_value(data_reg2.asUint, 0, 9)
            value = (msb << 6 & 0xffff) + lsb
            lut_data.append(value)

        if is_ext_registers_available:
            reg_name = "PAL_GC_MAX_" + self.str_pipe
            pal_gc_max = MMIORegister.read("PAL_GC_MAX_REGISTER", reg_name, self.platform)
            lut_data.append(self.get_bit_value(pal_gc_max.asUint, 0, 16))

            reg_name = "PAL_EXT_GC_MAX_" + self.str_pipe
            pal_ext_gc_max = MMIORegister.read("PAL_EXT_GC_MAX_REGISTER", reg_name, self.platform)
            lut_data.append(self.get_bit_value(pal_ext_gc_max.asUint, 0, 18))

            reg_name = "PAL_EXT2_GC_MAX_" + self.str_pipe
            pal_ext2_gc_max = MMIORegister.read("PAL_EXT2_GC_MAX_REGISTER", reg_name, self.platform)
            lut_data.append(self.get_bit_value(pal_ext2_gc_max.asUint, 0, 18))

        return lut_data

    ##
    # @brief        To get BPC value from pixelformat
    # @param[in]    pixel_format
    # @return       BPC value
    def get_bpc_from_pixelformat(self, pixel_format):

        BPC = 8
        if ((pixel_format >= flip.SB_PIXELFORMAT.SB_8BPP_INDEXED) and (
                pixel_format < flip.SB_PIXELFORMAT.SB_R10G10B10X2)):
            BPC = 8
        elif ((pixel_format >= flip.SB_PIXELFORMAT.SB_R10G10B10X2) and (
                pixel_format < flip.SB_PIXELFORMAT.SB_R16G16B16X16F)):
            BPC = 10
        elif ((pixel_format >= flip.SB_PIXELFORMAT.SB_R16G16B16X16F) and (
                pixel_format < flip.SB_PIXELFORMAT.SB_MAX_PIXELFORMAT)):
            BPC = 16
        elif (pixel_format in (
                flip.SB_PIXELFORMAT.SB_NV12YUV420, flip.SB_PIXELFORMAT.SB_YUV422, flip.SB_PIXELFORMAT.SB_YUV444_8)):
            BPC = 8
        elif (pixel_format in (
                flip.SB_PIXELFORMAT.SB_P010YUV420, flip.SB_PIXELFORMAT.SB_YUV422_10, flip.SB_PIXELFORMAT.SB_YUV444_10)):
            BPC = 10
        elif (pixel_format in (
                flip.SB_PIXELFORMAT.SB_P012YUV420, flip.SB_PIXELFORMAT.SB_YUV422_12, flip.SB_PIXELFORMAT.SB_YUV444_12)):
            BPC = 12
        elif (pixel_format in (
                flip.SB_PIXELFORMAT.SB_P016YUV420, flip.SB_PIXELFORMAT.SB_YUV422_16, flip.SB_PIXELFORMAT.SB_YUV444_16)):
            BPC = 16

        return BPC

    ##
    # @brief        To scale csc for range conversion
    # @param[in]    bpc
    # @param[in]    input (RGB/YCbCr)
    # @param[in]    output (RGB/YCbCr)
    # @param[in]    convType type of conversion (STUDIO_TO_FULL/ FULL_TO_FULL)
    # @param[in]    cscCoeff csc coefficient matrix
    # @return       converted_csc matrix
    def scale_csc_for_range_conversion(self, bpc, input, output, convType, cscCoeff):
        converted_csc = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        max_pixel_val = (1 << bpc) - 1
        rgb_y_scalefactor = 1.0
        cbcr_scalefactor = 1.0
        if (bpc == 8):
            normalizing_factor = float(1.0 / max_pixel_val)
        else:
            normalizing_factor = (1 << (bpc - 8) & 0xffff) / float(max_pixel_val)
        logging.debug("Normalizing Factor : %s" % normalizing_factor)

        # Sacle factors calclated for FR to LR conversion
        rgb_y_scalefactor = float(219.0 * normalizing_factor)
        cbcr_scalefactor = float(224.0 * normalizing_factor)

        # Sacle factors are inverted for LR to FR conversion
        if convType == "STUDIO_TO_FULL":
            rgb_y_scalefactor = float(1.0 / rgb_y_scalefactor)
            cbcr_scalefactor = float(1.0 / cbcr_scalefactor)

        logging.debug("ScaleFactors : %s %s" % (rgb_y_scalefactor, cbcr_scalefactor))

        # All coefficients are scaled using same factor in case of RGB to RGB conversion
        if input == output:  # RGB and RGB
            for i in range(0, 3):
                for j in range(0, 3):
                    converted_csc[i][j] = cscCoeff[i][j] * rgb_y_scalefactor

        # Y and Cb/Cr are converted using different scale factors
        elif input != output:  # RGB and YCbCr or YCbCr and RGB
            for i in range(0, 3):
                for j in range(0, 3):
                    if (i == 0):
                        converted_csc[i][j] = cscCoeff[i][j] * rgb_y_scalefactor
                    else:
                        converted_csc[i][j] = cscCoeff[i][j] * cbcr_scalefactor

        return converted_csc

    ##
    # @brief        To get offsets for range conversion
    # @param[in]    bpc
    # @param[in]    input (RGB/YCbCr)
    # @param[in]    output (RGB/YCbCr)
    # @param[in]    convType type of conversion (STUDIO_TO_FULL/ FULL_TO_FULL)
    # @return       offsets
    def get_offsets_for_range_conversion(self, bpc, input, output, convType):
        # RGB (same as Y) FR to LR conversion. HW register has 12 bits. 4096 represents 1.0
        offsets = [0, 0, 0]
        max_pixel_val = (1 << bpc) - 1

        if bpc == 8:
            normalizing_factor = 1.0 / max_pixel_val
        else:
            normalizing_factor = (float)(1 << (bpc - 8)) / max_pixel_val

        ##
        # When the coversion type is RGB_FR_TO_RGB_LR
        offsets[0] = offsets[1] = offsets[2] = round(4096.0 * 16.0 * normalizing_factor)
        if input == "RGB" and output == "RGB" and convType == "STUDIO_TO_FULL":
            offsets[0] = -offsets[0]
            offsets[1] = -offsets[1]
            offsets[2] = -offsets[2]
        if input == "RGB" and output == "RGB" and convType == "FULL_TO_FULL":
            offsets[0] = 0
            offsets[1] = 0
            offsets[2] = 0
        elif input == "RGB" and output == "YCBCR" and convType == "FULL_TO_STUDIO":
            offsets[0] = 2048
            offsets[2] = 2048
        elif input == "YCBCR" and output == "RGB" and convType == "FULL_TO_FULL":
            offsets[0] = -2048
            offsets[1] = 0
            offsets[2] = -2048
        elif input == "YCBCR" and output == "RGB" and convType == "STUDIO_TO_FULL":
            offsets[0] = -2048
            offsets[1] = -offsets[1]
            offsets[2] = -2048

        return offsets

    ##
    # @brief        To verify fp16 normalizer programming
    # @param[in]    pixel_format
    # @param[in]    blending_mode
    # @return       True if fp16 normalizer programming is True else False
    def verify_fp16_normalizer_programming(self, pixel_format, blending_mode):
        ref_hdr_normalizing_factor = 0
        ref_sdr_normalizing_factor = 0
        ref_csc_scale_factor = 1.0
        reg_name = "PLANE_PIXEL_NORMALIZE" + "_" + self.str_plane_pipe
        normalizer_reg = MMIORegister.read("PLANE_PIXEL_NORMALIZE_REGISTER", reg_name, self.platform)
        if (pixel_format in (flip.SB_PIXELFORMAT.SB_R16G16B16A16F, flip.SB_PIXELFORMAT.SB_R16G16B16X16F)):
            if normalizer_reg.enable:
                logging.info("FP16 normalize : %s" % normalizer_reg.normalization_factor)
                ref_hdr_normalizing_factor = 0x2019
                ref_sdr_normalizing_factor = 0x3C00

                if blending_mode == BLENDINGMODE.BT2020_LINEAR:
                    logging.info("Blending Mode is Linear")
                    self.plane_csc_scalefactor = ref_csc_scale_factor
                    if normalizer_reg.normalization_factor != ref_hdr_normalizing_factor:
                        color_common_utility.gdhm_report_app_color(
                            title="[COLOR][HDR]Verification failed due to FP16 Normalizer value mismatch in HDR Linear blending mode")
                        logging.error(
                            "FAIL: %s - HDR Linear BlendingMode :FP16 Normalizer value not matching: Expected = %x Actual = %x",
                            reg_name, ref_hdr_normalizing_factor, normalizer_reg.normalization_factor)
                        return False
                    else:
                        logging.info(
                            "PASS: %s - HDR Linear BlendingMode :FP16 Normalizer value  matching: Expected = %x Actual = %x",
                            reg_name, ref_hdr_normalizing_factor, normalizer_reg.normalization_factor)
                else:
                    self.plane_csc_scalefactor = ref_csc_scale_factor
                    if normalizer_reg.normalization_factor != ref_sdr_normalizing_factor:
                        color_common_utility.gdhm_report_app_color(
                            title="[COLOR][HDR]Verification failed due to FP16 Normalizer value mismatch in HDR Non Linear blending mode")
                        logging.error(
                            "FAIL: %s - HDR Non Linear BlendingMode :FP16 Normalizer value not matching: Expected = %x Actual = %x",
                            reg_name, ref_sdr_normalizing_factor, normalizer_reg.normalization_factor)
                        return False
                    else:
                        logging.info(
                            "PASS: %s - HDR Non Linear BlendingMode :FP16 Normalizer value matching: Expected = %x Actual = %x",
                            reg_name, ref_sdr_normalizing_factor, normalizer_reg.normalization_factor)
            else:
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to FP16 normalizer not enabled for plane with FP16 format")
                logging.error("FP16 normalizer not enabled for plane with FP16 format!!")
                return False

        return True

    ##
    # @brief        To verify input CSC programming verification
    # @param[in]	pixel_format
    # @param[in]    color_ctl_reg_name name of the color control register
    # @return	    True if Input coefficient match else False
    def verify_input_csc_programming(self, pixel_format, color_ctl_reg_name):
        if self.color_ctl_reg.plane_input_csc_enable:
            logging.info("PASS: %s - Plane iCSC is enabled. Expected = ENABLE, Actual = ENABLE", color_ctl_reg_name)
            reg_name = "PLANE_INPUT_CSC_COEFF"
            prog_val = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            prog_val1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            ref_val = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            ref_val1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            prog_val = self.get_csc_coeffmatrix_from_reg(reg_name, self.str_plane_pipe)
            if self.color_space is "YCBCR":
                prog_val1 = self.transform_yuv_to_rgb_matrix(prog_val)
            else:
                prog_val1 = prog_val
            if self.color_space == "YCBCR" and self.gamut == "P2020":
                ref_val = hdr_constants.YCbCr2RGB_2020_FullRange
            elif self.color_space == "YCBCR" and self.gamut == "P709":
                ref_val = hdr_constants.YCbCr2RGB_709_FullRange
            elif self.color_space == "YCBCR" and self.gamut == "P601":
                ref_val = hdr_constants.YCbCr2RGB_601_FullRange
            logging.debug("iCSC RefValue : %s" % ref_val)
            logging.debug("Pixel Format : %s" % pixel_format)
            bpc = self.get_bpc_from_pixelformat(pixel_format)
            ##
            # If color space is YCBCR, iCSC is not used for full range to limited range conversion. So we don't need any
            # range conversion.
            if self.color_space != "YCBCR":
                if self.range == "STUDIO":
                    ref_val1 = self.scale_csc_for_range_conversion(bpc, self.color_space, "RGB", "STUDIO_TO_FULL",
                                                                   ref_val)
                elif self.range == "FULL":
                    ref_val1 = self.scale_csc_for_range_conversion(bpc, self.color_space, "RGB", "FULL_TO_STUDIO",
                                                                   ref_val)
                else:
                    ref_val1 = ref_val
            else:
                ref_val1 = ref_val

            reg_name = reg_name + "_REGISTER_" + self.str_plane_pipe
            result = self.compare_csc_coeff(prog_val1, ref_val1, reg_name)
            if result is False:
                logging.error("FAIL: %s - InputCSC coeff mismatch", reg_name)
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to InputCSC coeff mismatch")
                return False
            else:
                logging.info("PASS: %s - InputCSC coeff match", reg_name)

            prog_offsets = self.get_csc_offsets_from_reg("PLANE_INPUT_CSC_PREOFF", self.str_plane_pipe)
            if (self.range == "STUDIO" and self.color_space == "RGB"):
                ref_offsets = self.get_offsets_for_range_conversion(bpc, self.color_space, "RGB", "STUDIO_TO_FULL")
            elif (self.range == "FULL" and self.color_space == "YCBCR"):
                ref_offsets = self.get_offsets_for_range_conversion(bpc, self.color_space, "RGB", "FULL_TO_STUDIO")


        else:
            if (self.color_space == "YCBCR" or self.range == "STUDIO"):
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane InputCSC disabled")
                logging.error("FAIL: %s - Plane iCSC is not enabled. Expected = ENABLE, Actual = DISABLE",
                              color_ctl_reg_name)
                return False

        return True

    ##
    # @brief       To verify the plane degamma LUT programming
    # @param[in]   blending_mode
    # @param[in]   color_ctl_reg_name name of the color control register
    # @return	   True if plane degamma programming is correct else False
    def verify_plane_degamma_programming(self, blending_mode, color_ctl_reg_name):
        pixel_format_plane_content_dict = {'8BPC': [flip.SB_PIXELFORMAT.SB_B8G8R8X8, flip.SB_PIXELFORMAT.SB_B8G8R8A8, flip.SB_PIXELFORMAT.SB_R8G8B8X8, flip.SB_PIXELFORMAT.SB_R8G8B8A8, flip.SB_PIXELFORMAT.SB_NV12YUV420, flip.SB_PIXELFORMAT.SB_YUV422, flip.SB_PIXELFORMAT.SB_YUV444_8],
                                            '10BPC': [flip.SB_PIXELFORMAT.SB_R10G10B10X2, flip.SB_PIXELFORMAT.SB_R10G10B10A2,
                            flip.SB_PIXELFORMAT.SB_B10G10R10X2, flip.SB_PIXELFORMAT.SB_B10G10R10A2,
                            flip.SB_PIXELFORMAT.SB_B10G10R10A2, flip.SB_PIXELFORMAT.SB_R10G10B10A2_XR_BIAS,
                            flip.SB_PIXELFORMAT.SB_P010YUV420, flip.SB_PIXELFORMAT.SB_YUV444_10,
                            flip.SB_PIXELFORMAT.SB_YUV422_10]}

        if self.color_ctl_reg.plane_pre_csc_gamma_enable:
            logging.info("PASS: %s - Plane pre CSC Gamma Enabled. Expected = ENABLE, Actual = ENABLE",
                         color_ctl_reg_name)
            reg_name = "PLANE_PRE_CSC_GAMC"
            no_samples = 131
            ref_lut = None
            prog_lut = self.get_gamma_lut_from_reg(reg_name, no_samples, self.str_plane_pipe)
            if self.gamma == "G22":
                ref_lut = hdr_constants.SRGB_DECODE_131_SAMPLES_24BPC
                if self.platform in "adlp":
                    if blending_mode == BLENDINGMODE.SRGB_NON_LINEAR:
                        if self.color_ctl_reg.plane_csc_enable:
                            logging.debug("Plane CSC is enabled")
                            ##
                            # If the Plane Content is 8BPC, then the COMPENSATED LUT for 8BPC to be considered
                            if self.src_pixel_format in pixel_format_plane_content_dict['8BPC']:
                                logging.debug("Plane Content is 8BPC; Hence taking the "
                                             "COMPENSATED_SRGB_DECODE_8BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.COMPENSATED_SRGB_DECODE_8BPC_131_SAMPLES_24BPC

                            ##
                            # If the Plane Content is 10BPC, then the COMPENSATED LUT for 10BPC to be considered
                            if self.src_pixel_format in pixel_format_plane_content_dict['10BPC']:
                                logging.debug("Plane Content is 10BPC; Hence taking the "
                                             "COMPENSATED_SRGB_DECODE_10BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.COMPENSATED_SRGB_DECODE_10BPC_131_SAMPLES_24BPC
                        else:
                            logging.debug("Plane CSC is not enabled")
                            # # If the Plane Content is 8BPC, then the CORRECTION LUT for 8BPC to be considered as
                            # PlaneCSC is not enabled
                            if self.src_pixel_format in pixel_format_plane_content_dict['8BPC']:
                                logging.debug("Plane Content is 8BPC; Hence taking the "
                                             "CORRECTION_LUT_FOR_8BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.CORRECTION_LUT_FOR_8BPC_131_SAMPLES_24BPC
                            # # If the Plane Content is 10BPC, then the CORRECTION LUT for 10BPC to be considered as
                            # PlaneCSC is not enabled
                            if self.src_pixel_format in pixel_format_plane_content_dict['10BPC']:
                                logging.info("Plane Content is 10BPC; Hence taking the "
                                             "CORRECTION_LUT_FOR_10BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.CORRECTION_LUT_FOR_10BPC_131_SAMPLES_24BPC

            elif self.gamma == "G2084":
                ref_lut = hdr_constants.EOTF2084_DECODE_131_SAMPLES_24BPC

                if self.platform in "adlp":
                    if blending_mode == BLENDINGMODE.SRGB_NON_LINEAR:
                        if self.color_ctl_reg.plane_csc_enable:
                            logging.info("Plane CSC is enabled")
                            if self.src_pixel_format in pixel_format_plane_content_dict['8BPC']:
                                logging.info("Plane Content is 8BPC; Hence taking the "
                                             "COMPENSATED_EOTF2084_DECODE_8BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.COMPENSATED_EOTF2084_DECODE_8BPC_131_SAMPLES_24BPC
                            if self.src_pixel_format in pixel_format_plane_content_dict['10BPC']:
                                logging.info("Plane Content is 10BPC; Hence taking the "
                                             "COMPENSATED_EOTF2084_DECODE_10BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.COMPENSATED_EOTF2084_DECODE_10BPC_131_SAMPLES_24BPC
                        else:
                            logging.info("Plane CSC is not enabled")
                            if self.src_pixel_format in pixel_format_plane_content_dict['8BPC']:
                                logging.info("Plane Content is 8BPC; Hence taking the "
                                             "CORRECTION_LUT_FOR_8BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.CORRECTION_LUT_FOR_8BPC_131_SAMPLES_24BPC
                            if self.src_pixel_format in pixel_format_plane_content_dict['10BPC']:
                                logging.info("Plane Content is 10BPC; Hence taking the "
                                             "CORRECTION_LUT_FOR_10BPC_131_SAMPLES_24BPC")
                                ref_lut = hdr_constants.CORRECTION_LUT_FOR_10BPC_131_SAMPLES_24BPC

            reg_name = reg_name + "_DATA_" + self.str_plane_pipe
            result = self.compare_gamma_lut(prog_lut, ref_lut, reg_name)
            if result is False:
                logging.error("FAIL: %s - Plane PreCSC Gamma mismatch", reg_name)
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane PreCSC Gamma mismatch")
                return False
            else:
                logging.info("PASS: %s - Plane PreCSC Gamma match", reg_name)
        else:
            if self.gamut == "P709" and blending_mode != BLENDINGMODE.SRGB_NON_LINEAR and self.gamma != "G10":
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to Plane pre CSC Gamma  not enabled")
                logging.error(
                    "FAIL: %s - Plane pre CSC Gamma not enabled (with gamut = %s). Expected = ENABLE, Actual = DISABLE",
                    color_ctl_reg_name, self.gamut)
                return False
            elif (self.gamut == "P2020" and int(blending_mode) not in (
                    BLENDINGMODE.BT2020_LINEAR, BLENDINGMODE.BT2020_NON_LINEAR)):
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to Plane pre CSC Gamma  not enabled")
                logging.error(
                    "FAIL: %s - Plane pre CSC Gamma not enabled (with gamut = %s). Expected = ENABLE, Actual = DISABLE",
                    color_ctl_reg_name, self.gamut)
                return False
        return True

    ##
    # @brief       To verify the plane CSC programming
    # @param[in]   blending_mode
    # @param[in]   pixel_format
    # @param[in]   color_ctl_reg_name name of the color control register name
    # @return	   True if pane csc programming is correct else False
    def verify_plane_csc_programming(self, blending_mode, pixel_format, color_ctl_reg_name):
        if self.color_ctl_reg.plane_csc_enable:
            logging.info("PASS: %s - Plane CSC enabled. Expected = ENABLE Actual = ENABLE", color_ctl_reg_name)
            reg_name = "PLANE_CSC_COEFF"
            prog_val = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            ref_val = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            prog_val = self.get_csc_coeffmatrix_from_reg(reg_name, self.str_plane_pipe)
            logging.info("Blending Mode : %s %s" % (blending_mode, BLENDINGMODE.BT2020_LINEAR))

            if blending_mode == BLENDINGMODE.BT2020_LINEAR or int(blending_mode) == BLENDINGMODE.BT2020_NON_LINEAR:
                if self.gamut == "P709":
                    ref_val = hdr_constants.BT709_TO_BT2020_RGB
            elif blending_mode == BLENDINGMODE.SRGB_NON_LINEAR:
                if self.gamut == "P2020":
                    ref_val = hdr_constants.BT2020_TO_BT709_RGB
            ref_val1 = ref_val
            if pixel_format in (flip.SB_PIXELFORMAT.SB_R16G16B16A16F, flip.SB_PIXELFORMAT.SB_R16G16B16X16F):
                logging.debug("Plane CSC ScaleFactor : %s" % self.plane_csc_scalefactor)
                ref_val1 = self.multiply_csc_with_scale_factor(ref_val, self.plane_csc_scalefactor)

            reg_name = reg_name + "_" + self.str_plane_pipe
            result = self.compare_csc_coeff(prog_val, ref_val1, reg_name)
            if result is False:
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane CSC coeff mismatch")
                logging.error("FAIL: %s - Plane CSC coeff mismatch", reg_name)
                return False
            else:
                logging.info("PASS: %s - Plane CSC coeff match. ", reg_name)
        else:
            if blending_mode == BLENDINGMODE.BT2020_LINEAR or blending_mode == BLENDINGMODE.BT2020_NON_LINEAR:
                if self.gamut != "P2020":
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to Plane CSC not enabled for 709->2020 conversion")
                    logging.error(
                        "FAIL: %s - Plane CSC not enabled for 709->2020 conversion. Expected = ENABLE Actual = DISABLE",
                        color_ctl_reg_name)
                    return False
            elif blending_mode == BLENDINGMODE.SRGB_NON_LINEAR:
                if self.gamut != "P709":
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to Plane CSC not enabled for 2020->709 conversion")
                    logging.error(
                        "FAIL: %s - Plane CSC not enabled for 2020->709 conversion. Expected = ENABLE Actual = DISABLE",
                        color_ctl_reg_name)
                    return False

        return True

    ##
    # @brief       To verify the plane gamma programming
    # @param[in]   pixel_format
    # @param[in]   blending_mode
    # @param[in]   color_ctl_reg_name name of the color control register name
    # @return	   True if plane gamma programming is correct else False
    def verify_plane_gamma_programming(self, pixel_format, blending_mode, color_ctl_reg_name):
        result = True
        if self.color_ctl_reg.plane_gamma_disable == 0:
            logging.info("PASS: %s - Plane Gamma enabled. Expected = ENABLE Actual = ENABLE", color_ctl_reg_name)
            reg_name = "PLANE_POST_CSC_GAMC"
            no_samples = 35
            prog_lut = None
            ref_lut = None
            result = True
            prog_lut = self.get_gamma_lut_from_reg(reg_name, no_samples, self.str_plane_pipe)
            if blending_mode == BLENDINGMODE.SRGB_NON_LINEAR or blending_mode == BLENDINGMODE.BT2020_NON_LINEAR:
                ref_lut = hdr_constants.SRGB_ENCODE_35_SAMPLES_24BPC
                logging.debug("Gamma Mode : %s" % self.color_ctl_reg.plane_gamma_mode)
                if self.color_ctl_reg.plane_gamma_mode != 0:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to Plane gamma non linear mode programmed incorrectly")
                    logging.error(
                        "FAIL: %s - Plane gamma non linear mode programmed incorrectly. Expected = 0 Actual = %d",
                        reg_name, self.color_ctl_reg.plane_gamma_mode)
                    return False
                else:
                    logging.info(
                        "PASS: %s - Plane gamma non linear mode programmed correctly. Expected = 0 Actual = %d",
                        reg_name, self.color_ctl_reg.plane_gamma_mode)
            elif blending_mode == BLENDINGMODE.BT2020_LINEAR:
                if self.color_ctl_reg.plane_gamma_mode != 1:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to Plane gamma linear mode programmed incorrectly")
                    logging.error("FAIL: %s - Plane gamma linear mode programmed incorrectly. Expected = 1 Actual = %d",
                                  reg_name, self.color_ctl_reg.plane_gamma_mode)
                    return False
                else:
                    logging.info("PASS: %s - Plane gamma linear mode programmed incorrectly. Expected = 1 Actual = %d",
                                 reg_name, self.color_ctl_reg.plane_gamma_mode)
                    # if(self.gamma == "G2084" ):
                    #    #TODO :Tone mapping H2H
                    # elif(self.gamut =="P709" and self.gamma == "G10"):
                    #    #TODO :Tone mapping H2H
                    # elif(self.gamut == "P709" and self.gamma =="G22"):
                    #    #TODO :Tone mapping S2H
        else:
            logging.info("Skipped verifying Plane Gamma as it is not enabled")

        return result

    ##
    # @brief        To verify dithering programming
    # @param[in]    blending_mode
    # @param[in]    pipe_id name of the pipe(A/B/C/D)
    # @return       True if dithering bit behavior is as expected as False
    def verify_dithering_programming(self, blending_mode, pipe_id):
        trans_ddi_func_ctl_reg_name = "TRANS_DDI_FUNC_CTL" + "_" + self.str_pipe
        trans_ddi_func_ctl_value = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", trans_ddi_func_ctl_reg_name,
                                                     self.platform)
        gamma_mode_reg_name = "GAMMA_MODE" + "_" + self.str_pipe
        gamma_mode_reg = MMIORegister.read("GAMMA_MODE_REGISTER", gamma_mode_reg_name, self.platform)
        color_ctl_reg_name = "PLANE_COLOR_CTL" + "_" + self.str_plane_pipe
        color_ctl_reg = MMIORegister.read("PLANE_COLOR_CTL_REGISTER", color_ctl_reg_name, self.platform)

        # HDR mode and BPC 12 check
        if blending_mode == BLENDINGMODE.BT2020_LINEAR and trans_ddi_func_ctl_value.bits_per_color == 3:
            if color_ctl_reg.color_correction_dithering_enable:
                logging.info(
                    "PASS: %s - Plane Color correction dithering enabled for HDR mode. Expected = 1 Actual = 1",
                    color_ctl_reg_name)
            else:
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to Plane Color correction dithering not enabled for HDR mode")
                logging.error(
                    "FAIL:%s - Plane Color correction dithering not enabled for HDR mode. Expected = 1 Actual = 0",
                    color_ctl_reg_name)
                return False
            if pipe_id in (0, 1):
                if gamma_mode_reg.post_csc_cc2_dithering_enable:
                    logging.info(
                        "PASS: %s - CC2 Pipe Color correction dithering enabled for HDR mode. Expected = 1 Actual = 1",
                        gamma_mode_reg_name)
                else:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to CC2 Pipe Color correction dithering not enabled for HDR mode")
                    logging.error(
                        "FAIL:%s - CC2 Pipe Color correction dithering not enabled for HDR mode. Expected = 1 Actual = 0",
                        gamma_mode_reg_name)
                    return False
            else:
                if gamma_mode_reg.post_csc_cc1_dithering_enable:
                    logging.info(
                        "PASS: %s - CC1 Pipe Color correction dithering enabled for HDR mode. Expected = 1 Actual = 1",
                        gamma_mode_reg_name)
                else:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to  CC1 Pipe Color correction dithering not enabled for HDR mode")
                    logging.error(
                        "FAIL:%s - CC1 Pipe Color correction dithering not enabled for HDR mode. Expected = 1 Actual = 0",
                        gamma_mode_reg_name)
                    return False
        else:
            if self.platform not in ("adls"):
                if (color_ctl_reg.color_correction_dithering_enable == 1 or gamma_mode_reg.post_csc_cc2_dithering_enable or gamma_mode_reg.post_csc_cc1_dithering_enable):
                    logging.error(
                        "FAIL: Plane / Pipe Color correction dithering enabled while in non HDR mode / BPC <12 ")
                    return False
        return True

    ##
    # @brief      To verify the hdr mode programming
    # @param[in]  blending_mode
    # @return     True if HDR programming behavior is as expected else False
    def verify_hdr_mode_and_bpc_programming(self, blending_mode):
        ##
        # HDR Mode verification
        pipe_misc_reg_name = "PIPE_MISC" + "_" + self.str_pipe
        pipe_misc_value = MMIORegister.read("PIPE_MISC_REGISTER", pipe_misc_reg_name, self.platform)
        if blending_mode == BLENDINGMODE.BT2020_LINEAR:
            if pipe_misc_value.hdr_mode:
                logging.info("%s : HDR Mode in Linear blending mode Expected : 1 Actual : %d",
                             pipe_misc_reg_name, pipe_misc_value.hdr_mode)
            else:
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to  HDR was disabled in Linear blending mode")
                logging.error("%s : HDR Mode in Linear blending mode Expected : 1 Actual : %d",
                              pipe_misc_reg_name, pipe_misc_value.hdr_mode)
                return False
        elif blending_mode == BLENDINGMODE.SRGB_NON_LINEAR or BLENDINGMODE.BT2020_NON_LINEAR:
            if pipe_misc_value.hdr_mode == 0:
                logging.info("%s : HDR Mode in Linear blending mode Expected : 0 Actual : %d",
                             pipe_misc_reg_name, pipe_misc_value.hdr_mode)
            else:
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to HDR was enabled in Non Linear blending mode")
                logging.error("%s : HDR Mode in Linear blending mode Expected : 0 Actual : %d",
                              pipe_misc_reg_name, pipe_misc_value.hdr_mode)
                return False

        ##
        # BPC Verification
        # Verification added only for linear mode and force BPC is only done there
        trans_ddi_func_ctl_reg_name = "TRANS_DDI_FUNC_CTL" + "_" + self.str_pipe
        trans_ddi_func_ctl_value = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", trans_ddi_func_ctl_reg_name,
                                                     self.platform)
        if blending_mode == BLENDINGMODE.BT2020_LINEAR:
            # 10 BPC or 12 BPC
            if trans_ddi_func_ctl_value.bits_per_color == 1 or trans_ddi_func_ctl_value.bits_per_color == 3:
                logging.info("%s : BPC in Linear blending mode Expected : %d Actual : %d",
                             trans_ddi_func_ctl_reg_name, trans_ddi_func_ctl_value.bits_per_color,
                             trans_ddi_func_ctl_value.bits_per_color)
            # else:
            # logging.error("%s : HDR Mode in Linear blending mode Expected : 10/12BPC Actual : %d",
            #              trans_ddi_func_ctl_reg_name, trans_ddi_func_ctl_value.bits_per_color)
            # self.fail()
        return True

    ##
    # @brief      To verify the pipe de_gamma programming
    # @param[in]  pipe_id id of the pipe(A/B/C/D)
    # @param[in]  gamma_mode_reg name of the gamma mode register
    # @param[in]  blending_mode
    # @param[in]  panel_caps panel capabilities (SDR/HDR)
    # @param[in]  gamma_reg_name name of the gamma register
    # @return     True if value matches with expected values else False
    def verify_pipe_degamma_programming(self, pipe_id, gamma_mode_reg, blending_mode, panel_caps, gamma_reg_name):
        no_samples = 131
        lut_after_rounding = []
        prog_lut = []
        ref_lut = []

        ##
        # Generate LUT value for 0.0 to 1.0
        if self.platform in ("mtl", "elg", "lnl"):
            lut_values = color_common_utility.generate_srgb_decoding_lut(129)
            for i in lut_values:
                lut_after_rounding.append(min(round(i), 126777216))

        if blending_mode == BLENDINGMODE.SRGB_NON_LINEAR and pipe_id in (0, 1):

            ##
            # In case of DG2, in some of the Stepping the WA implemented for 16012296444 will take effect
            # This will result in switching to CC1 blocks on some stepping and CC2 in a few other
            # Currently in Val Infra, there is no method to check the display stepping.
            # Due to this limitation, verifying which bit in the Gamma Mode is enabled
            # and deciding to go with either CC1 or CC2 blocks
            ##
            # In case of ADLP, in A0 stepping owing to 16012296444, as WA reverting to CC1 block
            # This check will be reverted once the next stepping comes up
            # On PreSi, the stepping is different than A0; hence to comprehend the same
            # deciding to go with either CC1 or CC2 blocks
            if self.platform in ("dg2", "adlp"):
                if gamma_mode_reg.pre_csc_cc2_gamma_enable:
                    reg_name = "PRE_CSC_CC2_GAMC"
                    pre_csc_gamma_enable = gamma_mode_reg.pre_csc_cc2_gamma_enable
                else:
                    reg_name = "PRE_CSC_GAMC"
                    pre_csc_gamma_enable = gamma_mode_reg.pre_csc_gamma_enable
                ref_lut1 = hdr_constants.SRGB_DECODE_131SAMPLES_16BPC
                ref_lut = ref_lut1[0:no_samples]
            ##
            # In SDR Mode, for Pipe A and Pipe B, verifying with CC2 blocks in case of MTL, ELG
            else:
                no_samples = 129
                reg_name = "PRE_CSC_CC2_GAMC"
                pre_csc_gamma_enable = gamma_mode_reg.pre_csc_cc2_gamma_enable
                ref_lut = lut_after_rounding
                logging.debug("Reference_lut:129 samples : %s with 24 bit precision" % lut_after_rounding)

        elif blending_mode == BLENDINGMODE.SRGB_NON_LINEAR and pipe_id in (3, 4):
            if self.platform in ("mtl", "elg", "lnl"):
                no_samples = 131
                ##
                # For pipe C and D , need to generate ref_lut values for extended 3.0 and 7.0
                lut_after_rounding.append(50331648)
                lut_after_rounding.append(117440512)
                ref_lut = lut_after_rounding

            pre_csc_gamma_enable = gamma_mode_reg.pre_csc_gamma_enable
            reg_name = "PRE_CSC_GAMC"
            logging.debug("Reference_lut :131 samples : %s" % ref_lut)

        else:
            ##
            # Only Gen13+ platforms, have CC2 blocks, otherwise it is CC1 blocks by default
            if self.platform in ("dg2", "adlp", "mtl", "elg", "lnl"):
                if gamma_mode_reg.pre_csc_cc2_gamma_enable:
                    logging.error("FAIL : PreCSC CC2 : Expectation : DISABLED; Actual : ENABLED")
                    return False
                else:
                    logging.info("PASS : PreCSC CC2 : Expectation : DISABLED; Actual : DISABLED")
            reg_name = "PRE_CSC_GAMC"
            pre_csc_gamma_enable = gamma_mode_reg.pre_csc_gamma_enable

        ##
        # In SDR Mode, DeGamma block is expected to be enabled; comparing the DeGamma Reference and Programmed LUTs
        if blending_mode == BLENDINGMODE.SRGB_NON_LINEAR:
            if pre_csc_gamma_enable:
                logging.info("PASS: %s - Pipe Pre CSC Gamma enabled Expected = ENABLE Actual = ENABLE", gamma_reg_name)
                prog_lut = self.get_gamma_lut_from_reg(reg_name, no_samples, self.str_pipe)
            else:
                logging.error("FAIL: %s - Pipe Pre CSC Gamma disabled Expected = ENABLE Actual = DISABLE", gamma_reg_name)
                return False

        if blending_mode == BLENDINGMODE.BT2020_LINEAR:
            if pre_csc_gamma_enable:
                logging.error("FAIL : %s Pipe Pre CSC Gamma enabled for linear blending mode!!", gamma_reg_name)
                return False
            else:
                logging.info("PASS : %s Pipe Pre CSC Gamma disabled for linear blending mode", gamma_reg_name)

        if blending_mode == BLENDINGMODE.BT2020_LINEAR and int(panel_caps) in (PANELCAPS.SDR_709_RGB, panel_caps == PANELCAPS.SDR_709_YUV420):
            if pre_csc_gamma_enable:
                logging.error("%s - Pipe Pre CSC Gamma for linear blending mode 709 output. Expected = ENABLE Actual = DISABLE",gamma_reg_name)
                return False
        if (blending_mode == BLENDINGMODE.SRGB_NON_LINEAR and int(panel_caps) in (
                    PANELCAPS.SDR_BT2020_RGB, PANELCAPS.SDR_BT2020_YUV420, PANELCAPS.HDR_BT2020_RGB,
                    PANELCAPS.HDR_BT2020_YUV420)):

            if pre_csc_gamma_enable:
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to Pipe Pre CSC Gamma enabled for Non linear blending mode BT2020 output")
                logging.error(
                    "%s - Pipe Pre CSC Gamma for non linear blending mode BT2020 output.  Expected = ENABLE Actual = DISABLE",
                    gamma_reg_name)
                return False

        ##
        # TO-DO :Need to extend compare_gamma_lut() for all platforms
        if self.platform in ("mtl", "elg", "lnl"):
            result = self.compare_gamma_lut(prog_lut, ref_lut, reg_name)
            if result is False:
                logging.error("FAIL: %s - Pipe De-Gamma verification for programmed values and reference values mismatched", reg_name)
                return False
            else:
                logging.info("PASS: %s - Pipe De-Gamma verification for programmed values and reference values matched", reg_name)

        return True

    ##
    # @brief      To verify the pipe CSC programming
    # @param[in]  pipe_id ID of the pipe(A/B/C/D)
    # @param[in]  csc_mode_reg name of the csc mode register
    # @param[in]  blending_mode
    # @param[in]  panel_caps panel capabilities(SDR/HDR)
    # @param[in]  csc_reg_name name of the csc register
    # @return     True if csc programming is as expected else False
    def verify_pipe_csc_programming(self, pipe_id, csc_mode_reg, blending_mode, panel_caps, csc_reg_name):

        if blending_mode == BLENDINGMODE.SRGB_NON_LINEAR and pipe_id in (0, 1):
            ##
            # In case of DG2, in some of the Stepping the WA implemented for 16012296444 will take effect
            # This will result in switching to CC1 blocks on some stepping and CC2 in a few other
            # Currently in Val Infra, there is no method to check the display stepping.
            # Due to this limitation, verifying which bit in the Gamma Mode is enabled
            # and deciding to go with either CC1 or CC2 blocks
            ##
            # In case of ADLP, in A0 stepping owing to 16012296444, as WA reverting to CC1 block
            # This check will be reverted once the next stepping comes up
            # On PreSi, the stepping is different than A0; hence to comprehend the same
            # deciding to go with either CC1 or CC2 blocks
            if self.platform in ("dg2", "adlp"):
                if csc_mode_reg.pipe_csc_cc2_enable:
                    csc_enable = csc_mode_reg.pipe_csc_cc2_enable
                    reg_name = "CSC_CC2_COEFF"
                else:
                    csc_enable = csc_mode_reg.pipe_csc_enable
                    reg_name = "CSC_COEFF"
            ##
            # In SDR Mode, for Pipe A and Pipe B, going ahead with CC2 blocks in case of MTL, ELG
            else:
                csc_enable = csc_mode_reg.pipe_csc_cc2_enable
                reg_name = "CSC_CC2_COEFF"
        ##
        # In case of HDR Mode, for DG2 and ADLP platforms, revert to CC1 blocks due to precision issues
        else:
            ##
            # Only Gen13+ platforms, have CC2 blocks, otherwise it is CC1 blocks by default
            if self.platform in ("dg2", "adlp", "mtl", "elg", "lnl"):
                if csc_mode_reg.pipe_csc_cc2_enable:
                    logging.error("FAIL : CSC_Mode CC2 : Expectation : DISABLED; Actual : ENABLED")
                    return False
                else:
                    logging.info("PASS : CSC_Mode CC2 : Expectation : DISABLED; Actual : DISABLED")
            csc_enable = csc_mode_reg.pipe_csc_enable
            reg_name = "CSC_COEFF"

        if csc_enable:
            logging.info("PASS: %s - Pipe CSC enabled. Expected = ENABLE Actual = ENABLE ", csc_reg_name)

            ref_val = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            prog_val = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            prog_val = self.get_csc_coeffmatrix_from_reg(reg_name, self.str_pipe)
            if (blending_mode == BLENDINGMODE.BT2020_LINEAR or blending_mode == BLENDINGMODE.BT2020_NON_LINEAR):
                if (panel_caps == PANELCAPS.SDR_709_RGB or panel_caps == PANELCAPS.SDR_709_YUV420):
                    ref_val = hdr_constants.BT2020_TO_BT709_RGB
                elif (panel_caps == PANELCAPS.HDR_DCIP3_RGB or PANELCAPS == PANELCAPS.HDR_DCIP3_YUV420):
                    ref_val = hdr_constants.BT2020_TO_DCIP3_RGB

            elif (blending_mode == BLENDINGMODE.SRGB_NON_LINEAR):
                if (panel_caps in (PANELCAPS.SDR_BT2020_RGB, PANELCAPS.SDR_BT2020_YUV420, PANELCAPS.HDR_BT2020_RGB,
                                   PANELCAPS.HDR_BT2020_YUV420)):
                    ref_val = hdr_constants.BT709_TO_BT2020_RGB

            reg_name = reg_name + "_" + self.str_pipe
            result = self.compare_csc_coeff(prog_val, ref_val, reg_name)
            if (result is False):
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe CSC coeff mismatch")
                logging.error("FAIL: %s - Pipe CSC coeff mismatch", reg_name)
                return False
            else:
                logging.info("PASS: %s - Pipe CSC coeff match", reg_name)
        else:
            if (blending_mode == BLENDINGMODE.BT2020_LINEAR or blending_mode == BLENDINGMODE.BT2020_NON_LINEAR):
                if (panel_caps not in (PANELCAPS.SDR_BT2020_RGB, PANELCAPS.SDR_BT2020_YUV420, PANELCAPS.HDR_BT2020_RGB,
                                       PANELCAPS.HDR_BT2020_YUV420)):
                    color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe CSC disabled")
                    logging.error("%s - Pipe CSC  not enabled. Expected = ENABLE Actual = DISABLE", csc_reg_name)
                    return False
            elif (blending_mode == BLENDINGMODE.SRGB_NON_LINEAR):
                if (panel_caps in (PANELCAPS.SDR_BT2020_RGB, PANELCAPS.SDR_BT2020_YUV420, PANELCAPS.HDR_BT2020_RGB,
                                   PANELCAPS.HDR_BT2020_YUV420)):
                    color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe CSC disabled")
                    logging.error("%s - Pipe CSC  not enabled. Expected = ENABLE Actual = DISABLE", csc_reg_name)
                    return False

        return True

    ##
    # @brief      To verify the output CSC programming
    # @param[in]  csc_mode_reg name of the CSC mode register
    # @param[in]  panel_caps capabilities of the panel (SDR/HDR)
    # @param[in]  output_range (STUDIO/FULL)
    # @param[in]  csc_reg_name name of the csc register
    # @return     True if output csc value matches else False
    def verify_output_csc_programming(self, csc_mode_reg, panel_caps, output_range, csc_reg_name):
        instance = MMIORegister.get_instance('CSC_MODE_REGISTER', csc_reg_name, self.platform)
        csc_mode_register_offset = instance.offset
        csc_mode_register_val = self.driver_interface_.mmio_read(csc_mode_register_offset, 'gfx_0')
        output_csc_enable = self.get_bit_value(csc_mode_register_val, 30, 30)
        if output_csc_enable:
            logging.info("PASS: %s - Pipe Output CSC enabled. Expected = ENABLE Actual  = ENABLE", csc_reg_name)
            reg_name = "OUTPUT_CSC_COEFF"
            ref_val = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            ref_val1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            prog_val = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            prog_val1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            prog_val = self.get_csc_coeffmatrix_from_reg(reg_name, self.str_pipe)
            if (panel_caps == PANELCAPS.SDR_BT2020_YUV420 or panel_caps == PANELCAPS.HDR_BT2020_YUV420):
                prog_val1 = self.transform_rgb_to_yuv_matrix(prog_val)
                ref_val = hdr_constants.RGB2YCbCr_2020_FullRange

            elif panel_caps == PANELCAPS.SDR_709_YUV420:
                prog_val1 = self.transform_rgb_to_yuv_matrix(prog_val)
                ref_val = hdr_constants.RGB2YCbCr_709_FullRange

            else:
                prog_val1 = prog_val

            bpc = 8  # self.get_bpc_from_pixelformat(pixel_format)
            logging.debug("BPC is %s" % bpc)
            if (output_range == OUTPUTRANGE.STUDIO and panel_caps in (
                    PANELCAPS.HDR_BT2020_RGB, PANELCAPS.HDR_DCIP3_RGB, PANELCAPS.SDR_709_RGB,
                    PANELCAPS.SDR_BT2020_RGB)):
                logging.debug("Output Range is STUDIO")
                ref_val1 = self.scale_csc_for_range_conversion(bpc, "RGB", "RGB", "FULL_TO_STUDIO", ref_val)
            elif (output_range == OUTPUTRANGE.FULL and panel_caps in (
                    PANELCAPS.HDR_BT2020_YUV420, PANELCAPS.HDR_DCIP3_YUV420, PANELCAPS.SDR_709_YUV420,
                    PANELCAPS.SDR_BT2020_YUV420)):
                logging.debug("Output Range is FULL")
                ref_val1 = self.scale_csc_for_range_conversion(bpc, "RGB", "RGB", "FULL_TO_STUDIO", ref_val)

            reg_name = reg_name + "_" + self.str_pipe
            prog_val = prog_val1
            result = self.compare_csc_coeff(prog_val, ref_val1, reg_name)
            if result is False:
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to OutputCSC coeff mismatch")
                logging.error("FAIL: %s - OutputCSC coeff mismatch", reg_name)
                return False
            else:
                logging.info("PASS: %s - OutputCSC coeff match", reg_name)


        # TODO :Range converision STUDIO to full range
        elif (panel_caps in (
                PANELCAPS.SDR_BT2020_YUV420, PANELCAPS.HDR_BT2020_YUV420, PANELCAPS.SDR_709_YUV420,
                PANELCAPS.HDR_DCIP3_YUV420)
              or output_range == OUTPUTRANGE.STUDIO):
            color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to OutputCSC disabled")
            logging.error("FAIL: %s - OutputCSC:  Expected = ENABLE Actual = DISABLE", csc_reg_name)
            return False
        else:
            logging.info("%s - Output Range is FULL; hence OutputCSC need not be enabled", csc_reg_name)

        return True

    ##
    # On Post-Si, observing Gamma Lut mismatch if GammaMode register is not set to 0 before reading the GammaLUT Data

    ##
    # @brief        To fetch programmed gamma lut values
    # @param[in]    pipe_id  of the Pipe(A/B/C/D)
    # @param[in]    reg_name name of the register
    # @param[in]    gamma_mode MULTI_SEGMENT or 12BIT_GAMMA mode
    # @return       prog_lut programmed lut
    def fetch_programmed_gamma_lut(self, pipe_id, reg_name, gamma_mode):

        current_pipe = chr(int(pipe_id) + 65)
        gamma_mode_offset = color_common_utility.get_register_offset("GAMMA_MODE_REGISTER", "GAMMA_MODE", current_pipe,
                                                                     self.platform)
        gamma_mode_reg_value_before_resetting = self.driver_interface_.mmio_read(gamma_mode_offset, 'gfx_0')
        if self.driver_interface_.mmio_write(gamma_mode_offset, 0, 'gfx_0'):
            logging.debug("Successfully set GammaMode register to 0")
        else:
            logging.error("Failed set GammaMode register to 0")
        time.sleep(2)
        prog_lut = self.get_pipe_gamma_lut_from_reg(gamma_mode, reg_name, True)
        ##
        # Restore GammaMode register
        if self.driver_interface_.mmio_write(gamma_mode_offset, gamma_mode_reg_value_before_resetting, 'gfx_0'):
            logging.debug("Successfully Reset GammaMode register")
        else:
            logging.error("Failed Reset GammaMode register")

        return prog_lut

    ##
    # @brief      To verify the pipe gamma programming
    # @param[in]  pipe_id Id of the Pipe(A/B/C/D)
    # @param[in]  gamma_mode_reg name of the gamma mode register
    # @param[in]  panel_caps capabilities of the panel (SDR/HDR)
    # @param[in]  blending_mode
    # @return     True if pipe gamma verification is as expected else False
    def verify_pipe_gamma_programming(self, pipe_id, gamma_mode_reg, panel_caps, blending_mode):
        ref_lut = []
        if blending_mode == BLENDINGMODE.SRGB_NON_LINEAR and pipe_id in (0, 1):
            ref_lut = hdr_constants.SRGB_ENCODE_515_SAMPLES_16BPC
            ##
            # In case of DG2, in some of the Stepping the WA implemented for 16012296444 will take effect
            # This will result in switching to CC1 blocks on some stepping and CC2 in a few other
            # Currently in Val Infra, there is no method to check the display stepping.
            # Due to this limitation, verifying which bit in the Gamma Mode is enabled
            # and deciding to go with either CC1 or CC2 blocks
            ##
            # In case of ADLP, in A0 stepping owing to 16012296444, as WA reverting to CC1 block
            # This check will be reverted once the next stepping comes up;
            # On PreSi, the stepping is different than A0; hence to comprehend the same
            # deciding to go with either CC1 or CC2 blocks
            if self.platform in ("dg2", "adlp"):
                if gamma_mode_reg.post_csc_cc2_gamma_enable:
                    post_csc_gamma_enable = gamma_mode_reg.post_csc_cc2_gamma_enable
                    reg_name = "POST_CSC_CC2"
                    ref_lut = ref_lut[0:513]
                else:
                    post_csc_gamma_enable = gamma_mode_reg.post_csc_gamma_enable
                    reg_name = "PAL_PREC"
                    ref_lut[513] = ref_lut[514] = 65536
            ##
            # In case of MTL, ELG, currently in SDR Mode, for Pipe A and Pipe B, going ahead with CC2 blocks
            else:
                post_csc_gamma_enable = gamma_mode_reg.post_csc_cc2_gamma_enable
                reg_name = "POST_CSC_CC2"

        else:
            ##
            # Only Gen13+ platforms, have CC2 blocks, otherwise it is CC1 blocks by default
            if self.platform in ("dg2", "adlp", "mtl", "elg", "lnl"):
                if gamma_mode_reg.post_csc_cc2_gamma_enable:
                    logging.error("FAIL : PostCSC CC2 : Expectation : DISABLED; Actual : ENABLED")
                    return False
                else:
                    logging.info("PASS : PostCSC CC2 : Expectation : DISABLED; Actual : DISABLED")
            post_csc_gamma_enable = gamma_mode_reg.post_csc_gamma_enable
            reg_name = "PAL_PREC"

        if post_csc_gamma_enable:
            logging.info("PASS: %s - Pipe gamma enabled. Expected = 1, Actual = 1", reg_name)
            prog_lut = None
            if panel_caps in (
                    PANELCAPS.HDR_BT2020_RGB, PANELCAPS.HDR_BT2020_YUV420, PANELCAPS.HDR_DCIP3_RGB,
                    PANELCAPS.HDR_DCIP3_YUV420):
                if gamma_mode_reg.gamma_mode == 3:
                    if self.platform in "adls":
                        prog_lut = self.fetch_programmed_gamma_lut(pipe_id, reg_name, "MULTI_SEGMENT")
                        ref_lut = hdr_constants.OETF2084_ENCODE_524_SAMPLES_16BPC
                    else:
                        prog_lut = self.fetch_programmed_gamma_lut(pipe_id, reg_name, "LOGARITHMIC")
                        ref_lut = hdr_constants.OETF_2084_10KNits_513Samples_8_24_FORMAT
            else:
                if gamma_mode_reg.gamma_mode == 2:
                    prog_lut = self.fetch_programmed_gamma_lut(pipe_id, reg_name, "12BIT_GAMMA")
                    if self.platform not in "adls":
                        prog_lut = prog_lut[0:513]

            pal_reg_name = reg_name + self.str_pipe + " / " + reg_name + self.str_pipe
            result = color_common_utility.compare_ref_and_programmed_gamma_lut(ref_lut, prog_lut)

            if result is False:
                color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe Gamma verification mismatch")
                logging.error("FAIL: %s - Pipe Gamma verification mismatch", pal_reg_name)
                return False
            else:
                logging.info("PASS: %s - Pipe Gamma verification success", pal_reg_name)

        else:
            if (blending_mode == BLENDINGMODE.BT2020_LINEAR and int(panel_caps) in (
                    PANELCAPS.SDR_709_RGB, panel_caps == PANELCAPS.SDR_709_YUV420)):
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to Pipe Gamma not enabled for linear blending mode 709 output")
                logging.error("FAIL: %s - Pipe Gamma not enabled for linear blending mode 709 output", reg_name)
                return False
            elif (blending_mode == BLENDINGMODE.SRGB_NON_LINEAR and int(panel_caps) in (
                    PANELCAPS.SDR_BT2020_RGB, PANELCAPS.SDR_BT2020_YUV420, PANELCAPS.HDR_BT2020_RGB,
                    PANELCAPS.HDR_BT2020_YUV420)):
                color_common_utility.gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to Pipe Gamma not enabled for linear blending mode  BT2020 output")
                logging.error("FAIL: %s - Pipe Gamma not enabled for non linear blending mode BT2020 output", reg_name)
                return False
        return True

    ##
    # @brief      To verify scalar programming for SDR/HDR
    # @param[in]  pipe_id Id of the pipe(A/B/C/D)
    # @param[in]  blending_mode
    # @return     True if scalar type programming behaves as expected else False
    def verify_scalar_type_programming(self, pipe_id, blending_mode):
        scalar1_reg_name = "PS_CTRL_1" + "_" + self.str_pipe
        scalar_1_value = MMIORegister.read("PS_CTRL_REGISTER", scalar1_reg_name, self.platform)
        scalar2_reg_name = "PS_CTRL_2" + "_" + self.str_pipe
        scalar_2_value = MMIORegister.read("PS_CTRL_REGISTER", scalar2_reg_name, self.platform)

        if (scalar_1_value.enable_scaler == 1):
            logging.info(" %s : Scalar 1 on Pipe %s is enabled", scalar1_reg_name, self.str_pipe)
            if (blending_mode == BLENDINGMODE.BT2020_LINEAR):
                if (scalar_1_value.scaler_type == 1):
                    logging.info("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Linear",
                                 scalar1_reg_name)
                else:
                    color_common_utility.gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Scalar Type was Non Linear in  Linear blending mode")
                    logging.error("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Non Linear",
                                  scalar1_reg_name)
                    return False
            elif (blending_mode == BLENDINGMODE.SRGB_NON_LINEAR):
                if (scalar_1_value.scaler_type == 0):
                    logging.info(
                        "%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Non Linear",
                        scalar1_reg_name)
                else:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to Scalar Type was Linear in Non Linear blending mode")
                    logging.error("%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Linear",
                                  scalar1_reg_name)
                    return False
        else:
            logging.info(" %s : Scalar 1 on Pipe %s is disabled", scalar1_reg_name, self.str_pipe)

        if (scalar_2_value.enable_scaler == 1):
            logging.info(" %s : Scalar 2 on Pipe %s is enabled", scalar2_reg_name, self.str_pipe)
            if (blending_mode == BLENDINGMODE.BT2020_LINEAR):
                if (scalar_2_value.scaler_type == 1):
                    logging.info("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Linear",
                                 scalar2_reg_name)
                else:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to Scalar Type was Non Linear in  Linear blending mode")
                    logging.error("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Non Linear",
                                  scalar2_reg_name)
                    return False
            elif (blending_mode == BLENDINGMODE.SRGB_NON_LINEAR):
                if (scalar_2_value.scaler_type == 0):
                    logging.info(
                        "%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Non Linear",
                        scalar2_reg_name)
                else:
                    color_common_utility.gdhm_report_app_color(
                        title="[COLOR][HDR]Verification failed due to Scalar Type was Linear in Non Linear blending mode")
                    logging.error("%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Linear",
                                  scalar2_reg_name)
                    return False
        else:
            logging.info(" %s : Scalar 2 on Pipe %s is disabled", scalar2_reg_name, self.str_pipe)
        return True

    ##
    # @brief      To verify the plane programming for HDR
    # @param[in]  pipe_id Id of the Pipe(A/B/C/D)
    # @param[in]  plane_id (0/1/2/3)
    # @param[in]  pixel_format
    # @param[in]  color_space_enum
    # @param[in]  blending_mode
    # @return     True if all checks passes else False
    def verify_hdr_plane_programming(self, pipe_id, plane_id, pixel_format, color_space_enum, blending_mode):
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        logging.info("-------------------Plane %d ------------------", plane_id)
        logging.info("PixelFormat : %s ", pixel_format)
        self.src_pixel_format = pixel_format
        self.decode_colorspace_enum(color_space_enum)
        self.str_plane_pipe = self.map_plane_pipe_id_to_string(pipe_id, plane_id)
        reg_name = "PLANE_COLOR_CTL" + "_" + self.str_plane_pipe
        self.color_ctl_reg = MMIORegister.read("PLANE_COLOR_CTL_REGISTER", reg_name, self.platform)

        # FP16Normalizer
        if not self.verify_fp16_normalizer_programming(pixel_format, blending_mode):
            logging.info("verifyFP16NormalizerProgramming failed")
            return False
        # iCSC
        if not self.verify_input_csc_programming(pixel_format, reg_name):
            logging.info("verifyInputCSCProgramming failed")
            return False
        ##
        # If content range is limited and color space is YCbCr, then use HW for range correction
        if (self.range == "STUDIO") and (self.color_space == "YCBCR"):
            if self.color_ctl_reg.yuv_range_correction_disable == 1:
                logging.error("for limited range and YCBCR color space content : "
                              "expected yuv_range_correction_output = 0, actual yuv_range_correction_output = 1 ")
                return False
            if self.color_ctl_reg.yuv_range_correction_output != 0:
                logging.error("for limited range and YCBCR Colorspace content:"
                              "expected yuv_range_correction_output = 0, actual yuv_range_correction_output = 1")
                return False
            if self.color_ctl_reg.remove_yuv_offset != 0:
                logging.error("for limited range and YCBCR Colorspace content:"
                              " expected remove_yuv_offset = 0, actual remove_yuv_offset = 1")
                return False
        # Plane preCSC Gamma
        if not self.verify_plane_degamma_programming(blending_mode, reg_name):
            logging.info("verifyPlaneDegammaProgramming failed")
            return False
        # Plane CSC
        if not self.verify_plane_csc_programming(blending_mode, pixel_format, reg_name):
            logging.info("verifyPlaneCSCProgramming failed")
            return False
        # Plane gamma LUT
        if not self.verify_plane_gamma_programming(pixel_format, blending_mode, reg_name):
            logging.info("verifyPlaneGammaProgramming failed")
            return False

        ## TODO : Cursor programming verification

        return True

    ##
    # @brief      To verify the pipe programming for HDR
    # @param[in]  pipe_id ID of the pipe(A/B/C/D)
    # @param[in]  blending_mode
    # @param[in]  panel_caps capabilities of the panel (SDR/HDR)
    # @param[in]  output_range (STUDIO/FULL)
    # @return     True if all checks passes else False
    def verify_hdr_pipe_programming(self, pipe_id, blending_mode, panel_caps, output_range):
        logging.info("Verifying HDR pipe programming: Pipe Id: %d Blending Mode = %s Panel Caps = %s Output range = %s",
                     pipe_id, blending_mode, panel_caps, output_range)
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        self.str_pipe = self.map_plane_pipe_id_to_string(pipe_id, 0, True)
        gamma_reg_name = "GAMMA_MODE" + "_" + self.str_pipe
        gamma_mode_reg = MMIORegister.read("GAMMA_MODE_REGISTER", gamma_reg_name, self.platform)
        csc_reg_name = "CSC_MODE" + "_" + self.str_pipe
        csc_mode_reg = MMIORegister.read("CSC_MODE_REGISTER", csc_reg_name, self.platform)
        # HDR Mode
        if not self.verify_hdr_mode_and_bpc_programming(blending_mode):
            logging.info("verifyHDRModeandBPCProgramming failed")
            return False
        # Pipe Pre CSC gamma
        if not self.verify_pipe_degamma_programming(pipe_id, gamma_mode_reg, blending_mode, panel_caps, gamma_reg_name):
            logging.info("verifyPipeDegammaProgramming failed")
            return False
        # Pipe CSC
        if not self.verify_pipe_csc_programming(pipe_id, csc_mode_reg, blending_mode, panel_caps, csc_reg_name):
            logging.info("verifyPipeCSCProgramming failed")
            return False
        # Pipe Post CSC Gamma
        if not self.verify_pipe_gamma_programming(pipe_id, gamma_mode_reg, panel_caps, blending_mode):
            logging.debug("verifyPipeGammaProgramming failed")
            return False
        # Pipe Output CSC
        if not self.verify_output_csc_programming(csc_mode_reg, panel_caps, output_range, csc_reg_name):
            logging.info("verifyOutputCSCProgramming failed")
            return False
        # Scalar type programming
        if not self.verify_scalar_type_programming(pipe_id, blending_mode):
            logging.info("verifyScalarTypeProgramming failed")
            return False

        ##
        # Plane and pipe dithering programming
        if not self.verify_dithering_programming(blending_mode, pipe_id):
            logging.info("verifyDitheringProgramming failed")
            return False

        return True

    ##
    # @brief      To verify the DP1.4 HDR Metadata programming
    # @param[in]  pipeID Id of the pipe(A/B/C/D)
    # @param[in]  reference_metadata
    # @return     True if programmed value and expected value matches else False
    def verifyDP1_4HDRMetadataProgramming(self, pipeID, reference_metadata):
        current_pipe = chr(int(pipeID) + 65)

        vsc_ext_sdp_ctl_reg = 'VSC_EXT_SDP_CTL_0_' + current_pipe
        vsc_ext_sdp_ctl_reg_instance = MMIORegister.get_instance('VSC_EXT_SDP_CTL_REGISTER', vsc_ext_sdp_ctl_reg,
                                                                 self.platform)
        vsc_ext_sdp_ctl_reg_offset = vsc_ext_sdp_ctl_reg_instance.offset
        vsc_sdp_ctrl_value = self.driver_interface_.mmio_read(vsc_ext_sdp_ctl_reg_offset, 'gfx_0')

        vsc_ext_sdp_data_reg = 'VSC_EXT_SDP_DATA_0_' + current_pipe
        vsc_ext_sdp_data_reg_instance = MMIORegister.get_instance('VSC_EXT_SDP_DATA_REGISTER', vsc_ext_sdp_data_reg,
                                                                  self.platform)
        vsc_ext_sdp_data_reg_offset = vsc_ext_sdp_data_reg_instance.offset

        ##
        # 31st bit(VSC extension SDP metadata enable) should be set to 0 before doing any reads to VSC_EXT_SDP_DATA register
        self.driver_interface_.mmio_write(vsc_ext_sdp_ctl_reg_offset, vsc_sdp_ctrl_value & 0x7fffff00, 'gfx_0')
        vsc_sdp_ctrl_value = self.driver_interface_.mmio_read(vsc_ext_sdp_ctl_reg_offset, 'gfx_0')
        logging.debug(
            "VSC_EXT_CTRL_VALUE after setting the VSC extension SDP metadata enable bit = %s" % vsc_sdp_ctrl_value)
        meta_data = []

        ##
        # Fetch the programmed metadata
        for i in range(0, 8):
            data_value = self.driver_interface_.mmio_read(vsc_ext_sdp_data_reg_offset, 'gfx_0')
            meta_data.append(data_value)

        logging.debug("Metadata is %s" % meta_data)
        ##
        # Rearranging programmed metadata according to reference metadata
        programmed_metadata = [self.get_bit_value(meta_data[1], 16, 31),  # EOTF

                               self.get_bit_value(meta_data[2], 0, 15),  # GreenPrimaries_0
                               self.get_bit_value(meta_data[2], 16, 31),  # GreenPrimaries_1

                               self.get_bit_value(meta_data[3], 0, 15),  # Blue_0
                               self.get_bit_value(meta_data[3], 16, 31),  # Blue_1

                               self.get_bit_value(meta_data[4], 0, 15),  # Red_0
                               self.get_bit_value(meta_data[4], 16, 31),  # Red_1

                               self.get_bit_value(meta_data[5], 0, 15),  # WhitePoint_X
                               self.get_bit_value(meta_data[5], 16, 31),  # WhitePoint_Y
                               self.get_bit_value(meta_data[6], 0, 15),  # MaxMasteringLuminance
                               self.get_bit_value(meta_data[6], 16, 31),  # MinMasteringLuminance
                               self.get_bit_value(meta_data[7], 0, 15),  # MaxCLL
                               self.get_bit_value(meta_data[7], 16, 31)  # MaxFALL
                               ]
        logging.debug("Reference Metadata is %s" % reference_metadata)
        logging.debug("Programmed Metadata is %s" % programmed_metadata)

        index = 0
        for reg_val, ref_val in zip(programmed_metadata, reference_metadata):
            if reg_val != ref_val:
                logging.error(
                    "DP1.4 Metadata programming not matching at index: %d Programmed Val : %d Expected Val : %d", index,
                    reg_val, ref_val)
                # return False
            index += 1
        return True
