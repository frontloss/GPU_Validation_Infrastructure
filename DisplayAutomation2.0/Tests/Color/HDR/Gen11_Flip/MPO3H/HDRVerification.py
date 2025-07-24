import logging
import math
import os

import Tests.Color.HDR.Gen11_Flip.MPO3H.HDRConstants as const
import Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3enums as Enums
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core import display_utility, enum, registry_access
from registers.mmioregister import MMIORegister
from Tests.Color.color_common_constants import *
from Tests.Color.color_common_utility import fetch_dpcd_data , gdhm_report_app_color


class BlendingMode(object):
    SRGB_NON_LINEAR = 0
    BT2020_NON_LINEAR = 1
    BT2020_LINEAR = 2


class PanelCaps(object):
    SDR_709_RGB = 0
    SDR_709_YUV420 = 1
    SDR_BT2020_RGB = 2
    SDR_BT2020_YUV420 = 3
    HDR_BT2020_RGB = 4
    HDR_BT2020_YUV420 = 5
    HDR_DCIP3_RGB = 6
    HDR_DCIP3_YUV420 = 7


class PanelType:
    LFP = 0
    EFP = 1


class OutputRange:
    STUDIO = 0
    FULL = 1


class HDRVerification(object):
    colorSpace = None  # RGB/YCBCR
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

    def decodeColorSpaceEnumValue(self, colorSpaceEnum):

        # With reference to below structure
        # typedef enum D3DDDI_COLOR_SPACE_TYPE
        # {
        #    D3DDDI_COLOR_SPACE_RGB_FULL_G22_NONE_P709             = 0,
        #    D3DDDI_COLOR_SPACE_RGB_FULL_G10_NONE_P709             = 1,
        #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P709           = 2,
        #    D3DDDI_COLOR_SPACE_RGB_STUDIO_G22_NONE_P2020          = 3,
        #    D3DDDI_COLOR_SPACE_RESERVED                           = 4,
        #    D3DDDI_COLOR_SPACE_YCBCR_FULL_G22_NONE_P709_X601      = 5,..??
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
        #    D3DDDI_COLOR_SPACE_YCBCR_STUDIO_GHLG_TOPLEFT_P2020    = 18,   ??
        #    D3DDDI_COLOR_SPACE_YCBCR_FULL_GHLG_TOPLEFT_P2020      = 19,   ??
        #    D3DDDI_COLOR_SPACE_CUSTOM                             = 0xFFFFFFFF
        # } D3DDDI_COLOR_SPACE_TYPE;

        # colorSpace
        if colorSpaceEnum in (0, 1, 2, 3, 12, 14, 17):
            self.colorSpace = "RGB"
        elif colorSpaceEnum in (6, 7, 8, 9, 10, 11, 13, 15, 16):
            self.colorSpace = "YCBCR"
        else:
            logging.error("ColorSpace enum type not supported !!")
            return False

        # range
        if colorSpaceEnum in (0, 1, 7, 9, 11, 12, 17):
            self.range = "FULL"
        elif colorSpaceEnum in (2, 3, 6, 8, 10, 13, 14, 15, 16):
            self.range = "STUDIO"

        # gamma
        if colorSpaceEnum in (0, 2, 3, 6, 7, 8, 9, 10, 11, 15, 17):
            self.gamma = "G22"
        elif colorSpaceEnum in (12, 13, 14, 16):
            self.gamma = "G2084"
        elif colorSpaceEnum == 1:
            self.gamma = "G10"

        # gamut
        if colorSpaceEnum in (0, 1, 2, 8, 9):
            self.gamut = "P709"
        elif colorSpaceEnum in (6, 7):
            self.gamut = "P601"
        elif colorSpaceEnum in (3, 10, 11, 12, 13, 14, 15, 16, 17):
            self.gamut = "P2020"

        logging.info("Plane Color Attributes : %s %s %s %s" % (self.gamut, self.gamma, self.colorSpace, self.range))
        return

    def mapPlanePipeIDToStringForRegVerification(self, pipeID, planeID, IsPipe=False):
        str1 = str(planeID)
        str2 = ""
        if (pipeID == 0):
            str2 = "A"
        elif (pipeID == 1):
            str2 = "B"
        elif (pipeID == 2):
            str2 = "C"
        elif (pipeID == 3):
            str2 = "D"

        str_plane_pipe = str1 + "_" + str2
        str_pipe = str2

        if (IsPipe is True):
            return str_pipe
        else:
            return str_plane_pipe

    def GetValue(self, value, start, end):

        retvalue = value << (31 - end) & 0xffffffff
        retvalue = retvalue >> (31 - end + start) & 0xffffffff
        return retvalue

    def convert_CSC_RegFormat_to_Coeff(self, cscCoeff):

        outVal = 0.0
        scale_factor = 0.0

        signBit = None
        exponent = None
        mantissa = None

        positionOfPointFromRight = 0

        signBit = self.GetValue(cscCoeff, 15, 15)
        exponent = self.GetValue(cscCoeff, 12, 14)
        mantissa = int(self.GetValue(cscCoeff, 3, 11))

        if (exponent == 6):
            positionOfPointFromRight = 7
        elif (exponent == 7):
            positionOfPointFromRight = 8
        elif (exponent == 0):
            positionOfPointFromRight = 9
        elif (exponent == 1):
            positionOfPointFromRight = 10
        elif (exponent == 2):
            positionOfPointFromRight = 11
        elif (exponent == 3):
            positionOfPointFromRight = 12

        scale_factor = math.pow(2.0, float(positionOfPointFromRight))
        outVal = float(mantissa) / scale_factor
        if (signBit == 1):
            outVal = outVal * -1

        return outVal

    def getCSCCoeffMatrixFromReg(self, unit_name, str):
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
                csc_coeff[i][j] = self.convert_CSC_RegFormat_to_Coeff(programmed_val[i][j])
        return csc_coeff

    def transformYUV_RGBMatrix(self, csccoeff):
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

    def transformRGB_YUVMatrix(self, csccoeff):
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

    def getCSCOffsetsFromReg(self, unit_name, str):
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

    def compareCSCCoeff(self, progVal, refVal, reg_name):
        logging.info("Programmed Value : %s Reference Value %s" % (progVal, refVal))
        result = True
        for i in range(0, 3):
            for j in range(0, 3):
                if (progVal[i][j] * refVal[i][j] >= 0.0):  # Same sign
                    if (math.fabs(progVal[i][j] - refVal[i][j]) >= self.threshold):
                        logging.error(
                            "FAIL: %s - Coeff values didn't match pos : (%d,%d) Expected Val = %d Programmed Val = %d",
                            reg_name, i, j, refVal[i][j], progVal[i][j])
                        result = False
                else:
                    result = False
        return result

    def getGammLUTFromReg(self, unit_name, no_samples, str):

        lut_data = []
        # Setting auto increment bit to 1 in index register
        module_name = unit_name + "_INDEX_REGISTER"
        reg_name = unit_name + "_INDEX_" + str
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

    def compareGammaLUT(self, progLUT, refLUT, reg_name):
        result = True
        index = 0
        for reg_val, ref_val in zip(progLUT, refLUT):
            if (reg_val != ref_val):
                logging.error(
                    "FAIL: %s - Gamma LUT values not matching Index = %d, Expected Val = %d, Programmed Val = %d",
                    reg_name, index, ref_val, reg_val)
                result = False
            index += 1
        return result

    def multiplyCSCWithScaleFactor(self, refVal, scaleFactor):
        refVal1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(0, 3):
            for j in range(0, 3):
                refVal1[i][j] = scaleFactor * refVal[i][j]
        return refVal1

    def getPipeGammaLUTFromReg(self, gamma_mode):

        lut_data = []
        index_reg = None
        index_offset = 0
        if (gamma_mode == "MULTI_SEGMENT"):
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
            lsb = self.GetValue(data_reg1.asUint, 4, 9)
            msb = self.GetValue(data_reg2.asUint, 0, 9)
            value = (msb << 6 & 0xffff) + lsb
            lut_data.append(value)

        # Palette Prec Data
        module_name = "PAL_PREC_INDEX_REGISTER"
        reg_name = "PAL_PREC_INDEX_" + self.str_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
        index_offset = instance.offset
        index_reg = MMIORegister.read(module_name, reg_name, self.platform)
        index_reg.index_auto_increment = 1
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

        module_name = "PAL_PREC_DATA_REGISTER"
        reg_name = "PAL_PREC_DATA_" + self.str_pipe
        for index in range(0, 1024, 2):
            index_reg.index_value = index
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
            data_reg1 = MMIORegister.read(module_name, reg_name, self.platform)
            data_reg2 = MMIORegister.read(module_name, reg_name, self.platform)
            lsb = self.GetValue(data_reg1.asUint, 4, 9)
            msb = self.GetValue(data_reg2.asUint, 0, 9)
            value = (msb << 6 & 0xffff) + lsb
            lut_data.append(value)

        reg_name = "PAL_GC_MAX_" + self.str_pipe
        pal_gc_max = MMIORegister.read("PAL_GC_MAX_REGISTER", reg_name, self.platform)
        lut_data.append(self.GetValue(pal_gc_max.asUint, 0, 16))

        reg_name = "PAL_EXT_GC_MAX_" + self.str_pipe
        pal_ext_gc_max = MMIORegister.read("PAL_EXT_GC_MAX_REGISTER", reg_name, self.platform)
        lut_data.append(self.GetValue(pal_ext_gc_max.asUint, 0, 18))

        reg_name = "PAL_EXT2_GC_MAX_" + self.str_pipe
        pal_ext2_gc_max = MMIORegister.read("PAL_EXT2_GC_MAX_REGISTER", reg_name, self.platform)
        lut_data.append(self.GetValue(pal_ext2_gc_max.asUint, 0, 18))

        return lut_data

    def getBPCFromPixelFormat(self, pixelFormat):

        BPC = 8
        if ((pixelFormat >= Enums.SB_PIXELFORMAT.SB_8BPP_INDEXED) and (
                pixelFormat < Enums.SB_PIXELFORMAT.SB_R10G10B10X2)):
            BPC = 8
        elif ((pixelFormat >= Enums.SB_PIXELFORMAT.SB_R10G10B10X2) and (
                pixelFormat < Enums.SB_PIXELFORMAT.SB_R16G16B16X16F)):
            BPC = 10
        elif ((pixelFormat >= Enums.SB_PIXELFORMAT.SB_R16G16B16X16F) and (
                pixelFormat < Enums.SB_PIXELFORMAT.SB_MAX_PIXELFORMAT)):
            BPC = 16
        elif (pixelFormat in (
                Enums.SB_PIXELFORMAT.SB_NV12YUV420, Enums.SB_PIXELFORMAT.SB_YUV422, Enums.SB_PIXELFORMAT.SB_YUV444_8)):
            BPC = 8
        elif (pixelFormat in (
                Enums.SB_PIXELFORMAT.SB_P010YUV420, Enums.SB_PIXELFORMAT.SB_YUV422_10,
                Enums.SB_PIXELFORMAT.SB_YUV444_10)):
            BPC = 10
        elif (pixelFormat in (
                Enums.SB_PIXELFORMAT.SB_P012YUV420, Enums.SB_PIXELFORMAT.SB_YUV422_12,
                Enums.SB_PIXELFORMAT.SB_YUV444_12)):
            BPC = 12
        elif (pixelFormat in (
                Enums.SB_PIXELFORMAT.SB_P016YUV420, Enums.SB_PIXELFORMAT.SB_YUV422_16,
                Enums.SB_PIXELFORMAT.SB_YUV444_16)):
            BPC = 16

        return BPC

    def scaleCSCForRangeConversion(self, bpc, input, output, convType, cscCoeff):
        convertedCSC = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        maxPixelVal = (1 << bpc) - 1
        rgb_yScaleFactor = 1.0
        cbcrScaleFactor = 1.0
        if (bpc == 8):
            normalizingFactor = float(1.0 / maxPixelVal)

        else:
            normalizingFactor = (1 << (bpc - 8) & 0xffff) / float(maxPixelVal)
        logging.debug("Normalizing Factor : %s" % normalizingFactor)

        # Sacle factors calclated for FR to LR conversion
        rgb_yScaleFactor = float(219.0 * normalizingFactor)
        cbcrScaleFactor = float(224.0 * normalizingFactor)

        # Sacle factors are inverted for LR to FR conversion
        if convType == "STUDIO_TO_FULL":
            rgb_yScaleFactor = float(1.0 / rgb_yScaleFactor)
            cbcrScaleFactor = float(1.0 / cbcrScaleFactor)

        # All coefficients are scaled using same factor in case of RGB to RGB conversion
        if input == output:  # RGB and RGB
            for i in range(0, 3):
                for j in range(0, 3):
                    convertedCSC[i][j] = cscCoeff[i][j] * rgb_yScaleFactor

        # Y and Cb/Cr are converted using different scale factors
        elif input != output:  # RGB and YCbCr or YCbCr and RGB
            for i in range(0, 3):
                for j in range(0, 3):
                    if (i == 0):
                        convertedCSC[i][j] = cscCoeff[i][j] * rgb_yScaleFactor
                    else:
                        convertedCSC[i][j] = cscCoeff[i][j] * cbcrScaleFactor

        return convertedCSC

    def getOffsetsForRangeConversion(self, bpc, input, output, convType):
        # RGB (same as Y) FR to LR conversion. HW register has 12 bits. 4096 represents 1.0
        offsets = [0, 0, 0]
        maxPixelVal = (1 << bpc) - 1

        if bpc == 8:
            normalizingFactor = 1.0 / maxPixelVal
        else:
            normalizingFactor = float((1 << (bpc - 8))) / maxPixelVal

        ##
        # When the coversion type is RGB_FR_TO_RGB_LR
        offsets[0] = offsets[1] = offsets[2] = round(4096.0 * 16.0 * normalizingFactor)
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

    def verifyFP16NormalizerProgramming(self, pixelFormat, blendingMode):
        ref_hdr_normalizing_factor = 0
        ref_sdr_normalizing_factor = 0
        ref_csc_scale_factor = 1.0
        reg_name = "PLANE_PIXEL_NORMALIZE" + "_" + self.str_plane_pipe
        normalizer_reg = MMIORegister.read("PLANE_PIXEL_NORMALIZE_REGISTER", reg_name, self.platform)
        if (pixelFormat in (Enums.SB_PIXELFORMAT.SB_R16G16B16A16F, Enums.SB_PIXELFORMAT.SB_R16G16B16X16F)):
            if normalizer_reg.enable == 1:
                logging.info("FP16 normalize : %s" % normalizer_reg.normalization_factor)
                if self.platform == "icllp" or self.platform == "iclhp" or self.platform == "lkf1" or self.platform == "jsl":
                    ref_hdr_normalizing_factor = 0x1CEF
                    ref_sdr_normalizing_factor = 0x38D1
                    ref_csc_scale_factor = 1.661
                else:
                    ref_hdr_normalizing_factor = 0x2019
                    ref_sdr_normalizing_factor = 0x3C00
                if (blendingMode == BlendingMode.BT2020_LINEAR):
                    logging.info("Blending Mode is Linear")
                    self.plane_csc_scalefactor = ref_csc_scale_factor

                    if normalizer_reg.normalization_factor != ref_hdr_normalizing_factor:
                        gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to FP16 Normalizer value mismatch in HDR Linear blending mode")
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
                    if (normalizer_reg.normalization_factor != ref_sdr_normalizing_factor):
                        gdhm_report_app_color(
                            title="[COLOR][HDR]Verification failed due to FP16 Normalizer value mismatch in HDR Non Linear blending mode")
                        logging.error(
                            "FAIL: %s - HDR Non Linear BlendingMode :FP16 Normalizer value not matching: Expected = %x Actual = %x",
                            reg_name, ref_sdr_normalizing_factor, normalizer_reg.normalization_factor)
                        return False
                    else:
                        logging.info(
                            "PASS: %s - HDR Non Linear BlendingMode :FP16 Normalizer value not matching: Expected = %x Actual = %x",
                            reg_name, ref_sdr_normalizing_factor, normalizer_reg.normalization_factor)
            else:
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to FP16 normalizer not enabled for plane with FP16 format")
                logging.error("FP16 normalizer not enabled for plane with FP16 format!!")
                return False

        return True

    ##
    # @brief        Inout CSC programming verification
    # @param[in]	Pixel format - Enums.SB_PIXELFORMAT enum
    # @return		None
    def verifyInputCSCProgramming(self, pixelFormat, color_ctl_reg_name):
        if (self.color_ctl_reg.plane_input_csc_enable == 1):
            logging.info("PASS: %s - Plane iCSC is enabled. Expected = ENABLE, Actual = ENABLE", color_ctl_reg_name)
            reg_name = "PLANE_INPUT_CSC_COEFF"
            progVal = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            refVal = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            refVal1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal = self.getCSCCoeffMatrixFromReg(reg_name, self.str_plane_pipe)
            if (self.colorSpace == "YCBCR"):
                progVal1 = self.transformYUV_RGBMatrix(progVal)
            else:
                progVal1 = progVal
            if (self.colorSpace == "YCBCR" and self.gamut == "P2020"):
                refVal = const.YCbCr2RGB_2020_FullRange
            elif (self.colorSpace == "YCBCR" and self.gamut == "P709"):
                refVal = const.YCbCr2RGB_709_FullRange
            elif (self.colorSpace == "YCBCR" and self.gamut == "P601"):
                refVal = const.YCbCr2RGB_601_FullRange
            logging.debug("iCSC RefValue : %s" % refVal)
            logging.debug("Pixel Format : %s" % pixelFormat)
            bpc = self.getBPCFromPixelFormat(pixelFormat)
            ##
            # If color space is YCBCR, iCSC is not used for full range to limited range conversion. So we don't need any
            # range conversion.
            if (self.colorSpace != "YCBCR"):
                if (self.range == "STUDIO"):
                    refVal1 = self.scaleCSCForRangeConversion(bpc, self.colorSpace, "RGB", "STUDIO_TO_FULL", refVal)
                elif (self.range == "FULL"):
                    refVal1 = self.scaleCSCForRangeConversion(bpc, self.colorSpace, "RGB", "FULL_TO_STUDIO", refVal)
                else:
                    refVal1 = refVal
            else:
                refVal1 = refVal

            reg_name = reg_name + "_REGISTER_" + self.str_plane_pipe
            result = self.compareCSCCoeff(progVal1, refVal1, reg_name)
            if (result is False):
                logging.error("FAIL: %s - InputCSC coeff mismatch", reg_name)
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to InputCSC coeff mismatch")
                return False
            else:
                logging.info("PASS: %s - InputCSC coeff match", reg_name)

        # prog_offsets = getCSCOffsetsFromReg("PLANE_INPUT_CSC_PREOFF",self.str_plane_pipe)
        # if(self.range == "STUDIO" and self.colorSpace == "RGB"):
        #  ref_offsets = self.getOffsetsForRangeConversion(bpc,self.colorSpace,"RGB","STUDIO_TO_FULL")
        # elif(self.range == "FULL" and self.colorSpace == "YCBCR"):
        # ref_offsets = self.getOffsetsForRangeConversion(bpc,self.colorSpace,"RGB","FULL_TO_STUDIO")
        else:
            if (self.colorSpace == "YCBCR" or self.range == "STUDIO"):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane InputCSC disabled")
                logging.error("FAIL: %s - Plane iCSC is not enabled. Expected = ENABLE, Actual = DISABLE",
                              color_ctl_reg_name)
                return False
        return True

    ##
    # @brief       To verify the plane degamma LUT programming
    # @param[in]	None
    # @return		None
    def verifyPlaneDegammaProgramming(self, blendingMode, color_ctl_reg_name):
        if (self.color_ctl_reg.plane_pre_csc_gamma_enable == 1):
            logging.info("PASS: %s - Plane pre CSC Gamma Enabled. Expected = ENABLE, Actual = ENABLE",
                         color_ctl_reg_name)
            reg_name = "PLANE_PRE_CSC_GAMC"
            no_samples = 131
            progLUT = None
            refLUT = None
            result = True
            progLUT = self.getGammLUTFromReg(reg_name, no_samples, self.str_plane_pipe)
            if (self.gamma == "G22"):
                refLUT = const.SRGB_Decode_131_Samples
            elif (self.gamma == "G2084"):
                refLUT = const.EOTF2084_Decode_131_Samples

            reg_name = reg_name + "_DATA_" + self.str_plane_pipe
            result = self.compareGammaLUT(progLUT, refLUT, reg_name)
            if result is False:
                logging.error("FAIL: %s - Plane PreCSC Gamma mismatch", reg_name)
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane PreCSC Gamma mismatch")
                return False
            else:
                logging.info("PASS: %s - Plane PreCSC Gamma match", reg_name)
        else:
            if (self.gamut == "P709" and blendingMode != BlendingMode.SRGB_NON_LINEAR and self.gamma != "G10"):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane pre CSC Gamma  not enabled with P709 gamut")
                logging.error(
                    "FAIL: %s - Plane pre CSC Gamma not enabled (with gamut = %s). Expected = ENABLE, Actual = ENABLE",
                    color_ctl_reg_name, self.gamut)
                return False
            elif (self.gamut == "P2020" and int(blendingMode) not in (
                    BlendingMode.BT2020_LINEAR, BlendingMode.BT2020_NON_LINEAR)):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane pre CSC Gamma  not enabled with P2020 gamut")
                logging.error(
                    "FAIL: %s - Plane pre CSC Gamma not enabled (with gamut = %s). Expected = ENABLE, Actual = ENABLE",
                    color_ctl_reg_name, self.gamut)
                return False
        return True

    ##
    # @brief       To verify the plane degamma LUT programming
    # @param[in]	Blending Mode -
    # @return		None
    def verifyPlaneCSCProgramming(self, blendingMode, pixelFormat, color_ctl_reg_name):
        if (self.color_ctl_reg.plane_csc_enable == 1):
            logging.info("PASS: %s - Plane CSC enabled. Expected = ENABLE Actual = ENABLE", color_ctl_reg_name)
            reg_name = "PLANE_CSC_COEFF"
            progVal = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            refVal = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal = self.getCSCCoeffMatrixFromReg(reg_name, self.str_plane_pipe)
            logging.info("Blending Mode : %s %s" % (blendingMode, BlendingMode.BT2020_LINEAR))

            if blendingMode == BlendingMode.BT2020_LINEAR or int(blendingMode) == BlendingMode.BT2020_NON_LINEAR:
                if self.gamut == "P709":
                    refVal = const.BT709_TO_BT2020_RGB
            elif blendingMode == BlendingMode.SRGB_NON_LINEAR:
                if self.gamut == "P2020":
                    refVal = const.BT2020_TO_BT709_RGB
            refVal1 = refVal
            if pixelFormat in (Enums.SB_PIXELFORMAT.SB_R16G16B16A16F, Enums.SB_PIXELFORMAT.SB_R16G16B16X16F):
                logging.debug("Plane CSC ScaleFactor : %s" % self.plane_csc_scalefactor)
                refVal1 = self.multiplyCSCWithScaleFactor(refVal, self.plane_csc_scalefactor)

            reg_name = reg_name + "_" + self.str_plane_pipe
            result = self.compareCSCCoeff(progVal, refVal1, reg_name)
            if result is False:
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane CSC coeff mismatch")
                logging.error("FAIL: %s - Plane CSC coeff mismatch", reg_name)
                return False
            else:
                logging.info("PASS: %s - Plane CSC coeff match. ", reg_name)
        else:
            if (blendingMode == BlendingMode.BT2020_LINEAR or blendingMode == BlendingMode.BT2020_NON_LINEAR):
                if (self.gamut != "P2020"):
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane CSC not enabled for 709->2020 conversion")
                    logging.error(
                        "FAIL: %s - Plane CSC not enabled for 709->2020 conversion. Expected = ENABLE Actual = ENABLE",
                        color_ctl_reg_name)
                    return False
            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR):
                if (self.gamut != "P709"):
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane CSC not enabled for 2020->709 conversion")
                    logging.error(
                        "FAIL: %s - Plane CSC not enabled for 2020->709 conversion. Expected = ENABLE Actual = ENABLE",
                        color_ctl_reg_name)
                    return False

        return True

    ##
    # @brief        To verify the plane gamma programming
    # @param[in]	Pixel format - Enums.SB_PIXELFORMAT enum
    # @param[in]	Blending Mode -
    # @return		None

    def verifyPlaneGammaProgramming(self, pixelFormat, blendingMode, color_ctl_reg_name):
        if (self.color_ctl_reg.plane_gamma_disable == 0):
            logging.info("PASS: %s - Plane Gamma enabled. Expected = ENABLE Actual = ENABLE", color_ctl_reg_name)
            reg_name = "PLANE_POST_CSC_GAMC"
            no_samples = 35
            progLUT = None
            refLUT = None
            result = True
            progLUT = self.getGammLUTFromReg(reg_name, no_samples, self.str_plane_pipe)
            if (blendingMode == BlendingMode.SRGB_NON_LINEAR or blendingMode == BlendingMode.BT2020_NON_LINEAR):
                refLUT = const.SRGB_Encode_35_Samples24bpc
                logging.debug("Gamma Mode : %s" % self.color_ctl_reg.plane_gamma_mode)
                if self.color_ctl_reg.plane_gamma_mode != 0:
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane gamma non linear mode programmed incorrectly")
                    logging.error(
                        "FAIL: %s - Plane gamma non linear mode programmed incorrectly. Expected = 0 Actual = %d",
                        reg_name, self.color_ctl_reg.plane_gamma_mode)
                    return False
                else:
                    logging.info(
                        "PASS: %s - Plane gamma non linear mode programmed correctly. Expected = 0 Actual = %d",
                        reg_name, self.color_ctl_reg.plane_gamma_mode)
            elif blendingMode == BlendingMode.BT2020_LINEAR:
                if self.color_ctl_reg.plane_gamma_mode != 1:
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Plane gamma linear mode programmed incorrectly")
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

        return True

    ##
    # @brief      To verify the pipe de_gamma programming
    # @param[in]  Gamma mode register instance
    # @param[in]  Blending Mode -
    # @return   None
    def verifyPipeDegammaProgramming(self, gamma_mode_reg, blendingMode, panelCaps, gamma_reg_name):
        if (gamma_mode_reg.pre_csc_gamma_enable == 1):
            logging.info("PASS: %s - Pipe Pre CSC Gamma enabled Expected = ENABLE Actual = ENABLE", gamma_reg_name)
            reg_name = "PRE_CSC_GAMC"
            no_samples = 35
            progLUT = None
            refLUT = None
            result = True
            progLUT = self.getGammLUTFromReg(reg_name, no_samples, self.str_pipe)

            if (blendingMode == BlendingMode.SRGB_NON_LINEAR or blendingMode == BlendingMode.BT2020_NON_LINEAR):
                refLUT = const.SRGB_Decode_35_Samples_16bpc
            elif (blendingMode == BlendingMode.BT2020_LINEAR):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe Pre CSC Gamma enabled for linear blending mode")
                logging.error("%s - Pipe Pre CSC Gamma enabled for linear blending mode", gamma_reg_name)
                return False

        else:
            if (blendingMode == BlendingMode.BT2020_LINEAR and int(panelCaps) in (
                    PanelCaps.SDR_709_RGB, panelCaps == PanelCaps.SDR_709_YUV420)):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe Pre CSC Gamma enabled for linear blending mode 709 output")
                logging.error(
                    "%s - Pipe Pre CSC Gamma for linear blending mode 709 output. Expected = ENABLE Actual = DISABLE",
                    gamma_reg_name)
                return False
            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR and int(panelCaps) in (
                    PanelCaps.SDR_BT2020_RGB, PanelCaps.SDR_BT2020_YUV420, PanelCaps.HDR_BT2020_RGB,
                    PanelCaps.HDR_BT2020_YUV420)):
                gdhm_report_app_color(
                    title="[COLOR][HDR]Verification failed due to Pipe Pre CSC Gamma enabled for non linear blending mode BT2020 output")
                logging.error(
                    "%s - Pipe Pre CSC Gamma for non linear blending mode BT2020 output.  Expected = ENABLE Actual = DISABLE",
                    gamma_reg_name)
                return False
        return True

    ##
    # @brief      To verify the pipe CSC programming
    # @param[in]  Blending Mode -
    # @param[in]  Panel Type LFP/EFP
    # @param[in]  PanelCaps - SDR/HDR ; Gamut ; RGB/YUV420
    # @return   None
    def verifyPipeCSCProgramming(self, csc_mode_reg, blendingMode, panelCaps, csc_reg_name):

        if (csc_mode_reg.pipe_csc_enable == 1):
            logging.info("PASS: %s - Pipe CSC enabled. Expected = ENABLE Actual = ENABLE ", csc_reg_name)
            reg_name = "CSC_COEFF"
            refVal = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            progVal = self.getCSCCoeffMatrixFromReg(reg_name, self.str_pipe)
            if (blendingMode == BlendingMode.BT2020_LINEAR or blendingMode == BlendingMode.BT2020_NON_LINEAR):
                if (panelCaps == PanelCaps.SDR_709_RGB or panelCaps == PanelCaps.SDR_709_YUV420):
                    refVal = const.BT2020_TO_BT709_RGB
                elif (panelCaps == PanelCaps.HDR_DCIP3_RGB or panelCaps == PanelCaps.HDR_DCIP3_YUV420):
                    refVal = const.BT2020_TO_DCIP3_RGB

            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR):
                if (panelCaps in (PanelCaps.SDR_BT2020_RGB, PanelCaps.SDR_BT2020_YUV420, PanelCaps.HDR_BT2020_RGB,
                                  PanelCaps.HDR_BT2020_YUV420)):
                    refVal = const.BT709_TO_BT2020_RGB

            # TODO : Tone mapping for LFP - how to verify ?

            reg_name = reg_name + "_" + self.str_pipe
            result = self.compareCSCCoeff(progVal, refVal, reg_name)
            if (result is False):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe CSC coeff mismatch")
                logging.error("FAIL: %s - Pipe CSC coeff mismatch", reg_name)
                return False
            else:
                logging.info("PASS: %s - Pipe CSC coeff match", reg_name)
        else:
            if (blendingMode == BlendingMode.BT2020_LINEAR or blendingMode == BlendingMode.BT2020_NON_LINEAR):
                if (panelCaps not in (PanelCaps.SDR_BT2020_RGB, PanelCaps.SDR_BT2020_YUV420, PanelCaps.HDR_BT2020_RGB,
                                      PanelCaps.HDR_BT2020_YUV420)):
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe CSC disabled")
                    logging.error("%s - Pipe CSC  not enabled. Expected = ENABLE Actual = ENABLE", csc_reg_name)
                    return False
            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR):
                if (panelCaps in (PanelCaps.SDR_BT2020_RGB, PanelCaps.SDR_BT2020_YUV420, PanelCaps.HDR_BT2020_RGB,
                                  PanelCaps.HDR_BT2020_YUV420)):
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe CSC disabled")
                    logging.error("%s - Pipe CSC  not enabled. Expected = ENABLE Actual = ENABLE", csc_reg_name)
                    return False

        return True

    ##
    # @brief      To verify the output CSC programming
    # @param[in]  CSC mode register instance
    # @param[in]  PanelCaps - SDR/HDR ; Gamut ; RGB/YUV420
    # @param[in]  Output Range STUDIO/Full
    # @return   None
    def verifyOutputCSCProgramming(self, csc_mode_reg, panelCaps, outputRange, csc_reg_name):
        if (csc_mode_reg.pipe_output_csc_enable == 1):
            logging.info("PASS: %s - Pipe Output CSC enabled. Expected = ENABLE Actual  = ENABLE", csc_reg_name)
            reg_name = "OUTPUT_CSC_COEFF"
            refVal = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            refVal1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal = self.getCSCCoeffMatrixFromReg(reg_name, self.str_pipe)
            if (panelCaps == PanelCaps.SDR_BT2020_YUV420 or panelCaps == PanelCaps.HDR_BT2020_YUV420):
                progVal1 = self.transformRGB_YUVMatrix(progVal)
                refVal = const.RGB2YCbCr_2020_FullRange

            elif panelCaps == PanelCaps.SDR_709_YUV420:
                progVal1 = self.transformRGB_YUVMatrix(progVal)
                refVal = const.RGB2YCbCr_709_FullRange

            else:
                progVal1 = progVal

            bpc = 8  # self.getBPCFromPixelFormat(pixel_format)
            logging.debug("BPC is %s" % bpc)
            if (outputRange == OutputRange.STUDIO and panelCaps in (
                    PanelCaps.HDR_BT2020_RGB, PanelCaps.HDR_DCIP3_RGB, PanelCaps.SDR_709_RGB,
                    PanelCaps.SDR_BT2020_RGB)):
                logging.debug("Output Range is STUDIO")
                refVal1 = self.scaleCSCForRangeConversion(bpc, "RGB", "RGB", "FULL_TO_STUDIO", refVal)
            elif (outputRange == OutputRange.FULL and panelCaps in (
                    PanelCaps.HDR_BT2020_YUV420, PanelCaps.HDR_DCIP3_YUV420, PanelCaps.SDR_709_YUV420,
                    PanelCaps.SDR_BT2020_YUV420)):
                logging.debug("Output Range is FULL")
                refVal1 = self.scaleCSCForRangeConversion(bpc, "RGB", "RGB", "FULL_TO_STUDIO", refVal)

            progVal = progVal1
            reg_name = reg_name + "_" + self.str_pipe
            result = self.compareCSCCoeff(progVal, refVal1, reg_name)

            if (result is False):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to OutputCSC coeff mismatch")
                logging.error("FAIL: %s - OutputCSC coeff mismatch", reg_name)
                return False
            else:
                logging.info("PASS: %s - OutputCSC coeff match", reg_name)


        # TODO :Range converision STUDIO to full range
        elif (panelCaps in (
                PanelCaps.SDR_BT2020_YUV420, PanelCaps.HDR_BT2020_YUV420, PanelCaps.SDR_709_YUV420,
                PanelCaps.HDR_DCIP3_YUV420)
              or outputRange == OutputRange.STUDIO):
            logging.debug("Should not be here")
            gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to OutputCSC disabled")
            logging.error("FAIL: %s - OutputCSC:  Expected = ENABLE Actual = DISABLE", csc_reg_name)
            return False
        else:
            logging.debug("%s - Output Range is FULL; hence OutputCSC need not be enabled", csc_reg_name)
        return True

    ##
    # @brief      To verify the pipe gamma programming
    # @param[in]  Gamma mode register instance
    # @param[in]  PanelCaps - SDR/HDR ; Gamut ; RGB/YUV420
    # @return   None
    def verifyPipeGammaProgramming(self, gamma_mode_reg, panelCaps, blendingMode, reg_name):

        if (self.color_ctl_reg.pipe_gamma_enable == 1 or gamma_mode_reg.post_csc_gamma_enable == 1):
            logging.info("PASS: %s - Pipe gamma enabled. Expected = 1, Actual = 1", reg_name)
            progLUT = None
            refLUT = None
            if (panelCaps in (PanelCaps.HDR_BT2020_RGB, PanelCaps.HDR_BT2020_YUV420, PanelCaps.HDR_DCIP3_RGB,
                              PanelCaps.HDR_DCIP3_YUV420)):
                if (gamma_mode_reg.gamma_mode == 3):
                    progLUT = self.getPipeGammaLUTFromReg("MULTI_SEGMENT")
                    refLUT = const.OETF_2084_Encode_524_Samples_16bpc

                    # HDR mode should be set in register
            else:
                if (gamma_mode_reg.gamma_mode == 2):
                    progLUT = self.getPipeGammaLUTFromReg("12BIT_GAMMA")
                    refLUT = const.SRGB_Encode_515_Samples_16bpc
            # index = 0
            # for reg_val, ref_val in zip(progLUT, refLUT):
            #     logging.info("Index = %d Programmed Val = %d Reference Val = %d", index, reg_val, ref_val)
            #     index += 1

            pal_reg_name = "PAL_PREC_MULTI_SEG_DATA_" + self.str_pipe + " / PAL_PREC_INDEX_" + self.str_pipe
            result = self.compareGammaLUT(progLUT, refLUT, pal_reg_name)

            if result is False:
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe Gamma verification mismatch")
                logging.error("FAIL: %s - Pipe Gamma verification mismatch", pal_reg_name)
                return False
            else:
                logging.info("PASS: %s - Pipe Gamma verification success", pal_reg_name)

        else:
            if (blendingMode == BlendingMode.BT2020_LINEAR and int(panelCaps) in (
                    PanelCaps.SDR_709_RGB, panelCaps == PanelCaps.SDR_709_YUV420)):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe Gamma not enabled for linear blending mode 709 output")
                logging.error("FAIL: %s - Pipe Gamma not enabled for linear blending mode 709 output", reg_name)
                return False
            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR and int(panelCaps) in (
                    PanelCaps.SDR_BT2020_RGB, PanelCaps.SDR_BT2020_YUV420, PanelCaps.HDR_BT2020_RGB,
                    PanelCaps.HDR_BT2020_YUV420)):
                gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Pipe Gamma not enabled for non linear blending mode  BT2020 output")
                logging.error("FAIL: %s - Pipe Gamma not enabled for non linear blending mode BT2020 output", reg_name)
                return False
        return True

    ##
    # @brief        To verify scalar programming for SDR/HDR
    # @param[in]  Pipe ID (starts with 0)
    # @param[in]  Blending Mode
    # @return   None
    def verifyScalarTypeProgramming(self, pipeID, blendingMode):
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        self.str_pipe = self.mapPlanePipeIDToStringForRegVerification(pipeID, 0, True)
        scalar1_reg_name = "PS_CTRL_1" + "_" + self.str_pipe
        scalar_1_value = MMIORegister.read("PS_CTRL_REGISTER", scalar1_reg_name, self.platform)
        scalar2_reg_name = "PS_CTRL_2" + "_" + self.str_pipe
        scalar_2_value = MMIORegister.read("PS_CTRL_REGISTER", scalar2_reg_name, self.platform)

        if (scalar_1_value.enable_scaler == 1):
            logging.info(" %s : Scalar 1 on Pipe %s is enabled", scalar1_reg_name, self.str_pipe)
            if (blendingMode == BlendingMode.BT2020_LINEAR):
                if (scalar_1_value.scaler_type == 1):
                    logging.info("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Linear",
                                 scalar1_reg_name)
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Scalar Type was non Linear in  Linear blending mode")

                    logging.error("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Non Linear",
                                  scalar1_reg_name)
                    return False
            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR):
                if (scalar_1_value.scaler_type == 0):
                    logging.info(
                        "%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Non Linear",
                        scalar1_reg_name)
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Scalar Type was Linear in Non Linear blending mode")
                    logging.error("%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Linear",
                                  scalar1_reg_name)
                    return False
        else:
            logging.info(" %s : Scalar 1 on Pipe %s is disabled", scalar1_reg_name, self.str_pipe)

        if (scalar_2_value.enable_scaler == 1):
            logging.info(" %s : Scalar 2 on Pipe %s is enabled", scalar2_reg_name, self.str_pipe)
            if (blendingMode == BlendingMode.BT2020_LINEAR):
                if (scalar_2_value.scaler_type == 1):
                    logging.info("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Linear",
                                 scalar2_reg_name)
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Scalar Type was Non Linear in  Linear blending mode")
                    logging.error("%s : Scalar Type in Linear blending mode Expected : Linear Actual : Non Linear",
                                  scalar2_reg_name)
                    return False
            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR):
                if (scalar_2_value.scaler_type == 0):
                    logging.info(
                        "%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Non Linear",
                        scalar2_reg_name)
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Verification failed due to Scalar Type was Linear in Non Linear blending mode")
                    logging.error("%s : Scalar Type in Non Linear blending mode Expected : Non Linear Actual : Linear",
                                  scalar2_reg_name)
                    return False
        else:
            logging.info(" %s : Scalar 2 on Pipe %s is disabled", scalar2_reg_name, self.str_pipe)
        return True

    ##
    # @brief        To verify the plane programming for HDR
    # @param[in]  Plane ID (starts with 0)
    # @param[in]  Pipe ID (starts with 0)
    # @param[in]  Pixel format - Enums.SB_PIXELFORMAT enum
    # @param[in]  ColorSpace - D3DDDI_COLOR_SPACE_TYPE enum
    # @param[in]  Blending Mode -
    # @return   None
    def verifyHDRPlaneProgramming(self, pipeID, planeID, pixelFormat, colorSpaceEnum, blendingMode):
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        self.decodeColorSpaceEnumValue(colorSpaceEnum)
        self.str_plane_pipe = self.mapPlanePipeIDToStringForRegVerification(pipeID, planeID)
        reg_name = "PLANE_COLOR_CTL" + "_" + self.str_plane_pipe
        self.color_ctl_reg = MMIORegister.read("PLANE_COLOR_CTL_REGISTER", reg_name, self.platform)

        # FP16Normalizer
        if not self.verifyFP16NormalizerProgramming(pixelFormat, blendingMode):
            logging.debug("verifyFP16NormalizerProgramming failed")
            return False
        # iCSC
        if not self.verifyInputCSCProgramming(pixelFormat, reg_name):
            logging.debug("verifyInputCSCProgramming failed")
            return False
        ##
        # If content range is limited and color space is YCbCr, then use HW for range correction
        if (self.range == "STUDIO") and (self.colorSpace == "YCBCR"):
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
        if not self.verifyPlaneDegammaProgramming(blendingMode, reg_name):
            logging.debug("verifyPlaneDegammaProgramming failed")
            return False

        # Plane CSC
        if not self.verifyPlaneCSCProgramming(blendingMode, pixelFormat, reg_name):
            logging.debug("verifyPlaneCSCProgramming failed")
            return False
        # Plane gamma LUT
        if not self.verifyPlaneGammaProgramming(pixelFormat, blendingMode, reg_name):
            logging.debug("verifyPlaneGammaProgramming failed")
            return False

        ## TODO : Scalar : inear/NOn linear based on blending mode
        ## TODO : Cursor programming verification

        return True

    ##
    # @brief      To verify the pipe programming for HDR
    # @param[in]	Pipe ID (starts with 0)
    # @param[in]	Blending Mode -
    # @param[in]  Panel Type LFP/EFP
    # @param[in]  PanelCaps - SDR/HDR ; Gamut ; RGB/YUV420
    # @param[in]  Output Range STUDIO/Full
    # @return   None
    def verifyHDRPipeProgramming(self, pipeID, blendingMode, panelCaps, outputRange):
        logging.info("Verifying HDR pipe programming: Pipe Id: %d Blending Mode = %s Panel Caps = %s Output range = %s",
                     pipeID, blendingMode, panelCaps, outputRange)
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        self.str_pipe = self.mapPlanePipeIDToStringForRegVerification(pipeID, 0, True)
        gamma_reg_name = "GAMMA_MODE" + "_" + self.str_pipe
        gamma_mode_reg = MMIORegister.read("GAMMA_MODE_REGISTER", gamma_reg_name, self.platform)
        csc_reg_name = "CSC_MODE" + "_" + self.str_pipe
        csc_mode_reg = MMIORegister.read("CSC_MODE_REGISTER", csc_reg_name, self.platform)

        # Pipe Pre CSC gamma
        if not self.verifyPipeDegammaProgramming(gamma_mode_reg, blendingMode, panelCaps, gamma_reg_name):
            logging.error("verifyPipeDegammaProgramming failed")
            return False
        # Pipe CSC
        if not self.verifyPipeCSCProgramming(csc_mode_reg, blendingMode, panelCaps, csc_reg_name):
            logging.error("verifyPipeCSCProgramming failed")
            return False
        # Pipe Post CSC Gamma()
        # if not self.verifyPipeGammaProgramming(gamma_mode_reg,panelCaps,blendingMode, gamma_reg_name):
        #     return False
        # Pipe Output CSC
        if not self.verifyOutputCSCProgramming(csc_mode_reg, panelCaps, outputRange, csc_reg_name):
            logging.error("verifyOutputCSCProgramming failed")
            return False
        if not self.verifyScalarTypeProgramming(pipeID, blendingMode):
            logging.error("verifyScalarTypeProgramming failed")
            return False

        ## TODO : Scalar linear/non linear check

        return True

    ##
    # @brief      To verify the DP1.4 HDR Metadata programming
    # @param[in]	Pipe ID (starts with 0)
    # @param[in]	Reference Metadata
    # @return   Result(True/False)
    def verifyDP1_4HDRMetadataProgramming(self, pipeID, reference_metadata):
        current_pipe = chr(int(pipeID) + 65)
        meta_data = []
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
        ##
        # Fetch the programmed metadata
        for i in range(0, 10):
            data_value = self.driver_interface_.mmio_read(vsc_ext_sdp_data_reg_offset, 'gfx_0')
            meta_data.append(data_value)

        logging.debug("Metadata is %s" % meta_data)

        ##
        # Rearranging programmed metadata according to reference metadata
        programmed_metadata = [self.GetValue(meta_data[1], 16, 31),  # EOTF
                               self.GetValue(meta_data[2], 0, 15),  # GreenPrimaries_0
                               self.GetValue(meta_data[2], 16, 31),  # GreenPrimaries_1
                               self.GetValue(meta_data[3], 0, 15),  # Blue_0
                               self.GetValue(meta_data[3], 16, 31),  # Blue_1
                               self.GetValue(meta_data[4], 0, 15),  # Red_0
                               self.GetValue(meta_data[4], 16, 31),  # Red_1
                               self.GetValue(meta_data[5], 0, 15),  # WhitePoint_X
                               self.GetValue(meta_data[5], 16, 31),  # WhitePoint_Y
                               self.GetValue(meta_data[6], 0, 15),  # MaxMasteringLuminance
                               self.GetValue(meta_data[6], 16, 31),  # MinMasteringLuminance
                               self.GetValue(meta_data[7], 0, 15),  # MaxCLL
                               self.GetValue(meta_data[7], 16, 31)  # MaxFALL
                               ]
        logging.debug("Programmed Metadata is %s" % programmed_metadata)
        logging.debug("Reference Metadata is %s" % reference_metadata)

        index = 0
        for reg_val, ref_val in zip(programmed_metadata, reference_metadata):
            if reg_val != ref_val:
                logging.error(
                    "DP1.4 Metadata programming not matching at index: %d Programmed Val : %d Expected Val : %d", index,
                    reg_val, ref_val)
                gdhm_report_app_color(title="[Color][HDR]Verification of DP1.4 Static Metadata Programming failed")
                return False
            index += 1
        return True

    ##
    # Parse the programmed metadata and re-arrange according to reference metadata
    def parse_and_rearrange_prog_metadata(self, display, programmed_metadata, pcon=False):
        meta_data = []
        if display[:4] == 'HDMI':
            meta_data = [          self.GetValue(programmed_metadata[1], 8, 9),  # EOTF
                                   (self.GetValue(programmed_metadata[2], 0, 7) << 8) | self.GetValue(programmed_metadata[1], 24, 31),  # GreenPrimaries_0
                                   self.GetValue(programmed_metadata[2], 8, 23), # GreenPrimaries_1
                                   (self.GetValue(programmed_metadata[3], 0, 7) << 8) | self.GetValue(programmed_metadata[2], 24, 31),  # Blue_0
                                   self.GetValue(programmed_metadata[3], 8, 23),  # Blue_1
                                   (self.GetValue(programmed_metadata[4], 0, 7) << 8) | self.GetValue(programmed_metadata[3], 24, 31),  # Red_0
                                   self.GetValue(programmed_metadata[4], 8, 23),  # Red_1
                                   (self.GetValue(programmed_metadata[5], 0, 7) << 8) | self.GetValue(programmed_metadata[4], 24, 31),  # WhitePoint_X
                                   self.GetValue(programmed_metadata[5], 8, 23),  # WhitePoint_Y
                                   (self.GetValue(programmed_metadata[6], 0, 7) << 8) | self.GetValue(programmed_metadata[5], 24, 31),  # MaxMasteringLuminance
                                   self.GetValue(programmed_metadata[6], 8, 23),  # MinMasteringLuminance
                                   (self.GetValue(programmed_metadata[7], 0, 7)<< 8) | self.GetValue(programmed_metadata[6], 24, 31),  # MaxCLL
                                   self.GetValue(programmed_metadata[7], 8, 23),  # GreenPrimaries_0
                        ]
        elif display[:2] == 'DP':
            meta_data = [
                                self.GetValue(programmed_metadata[1], 16, 17),
                                self.GetValue(programmed_metadata[2], 0, 15),
                                self.GetValue(programmed_metadata[2], 16, 31),
                                self.GetValue(programmed_metadata[3], 0, 15),
                                self.GetValue(programmed_metadata[3], 16, 31),
                                self.GetValue(programmed_metadata[4], 0, 15),
                                self.GetValue(programmed_metadata[4], 16, 31),
                                self.GetValue(programmed_metadata[5], 0, 15),
                                self.GetValue(programmed_metadata[5], 16, 31),
                                self.GetValue(programmed_metadata[6], 0, 15),
                                self.GetValue(programmed_metadata[6], 16, 31),
                                self.GetValue(programmed_metadata[7], 0, 15),
                                self.GetValue(programmed_metadata[7], 16, 31)
                ]
        logging.debug("After parsing and re-arranging the metadata %s" %meta_data)
        return meta_data

    ##
    # Perform DPCD verification for Aux based eDP HDR panels
    def verify_edp_hdr_display_caps_and_ctrl_params(self, edp_hdr_caps, edp_hdr_ctrl_params):
        ##
        # If the display caps support 2084 decode, then driver should enable 2084 decode in HDR Mode
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        hdr_mode = registry_access.read(args=reg_args, reg_name="ForceHDRMode")
        if self.GetValue(edp_hdr_caps, 0, 0) == ENABLE_2084_DECODE:
            logging.info("Display Caps ENABLE_2084_DECODE - Expected : ENABLE; Actual : ENABLE")
            if hdr_mode:
                ##
                # In HDR mode, driver should enable 2084_DECODE
                if self.GetValue(edp_hdr_ctrl_params, 0, 0) == ENABLE_2084_DECODE:
                    logging.info("Driver support for ENABLE_2084_DECODE - Expected : ENABLE; Actual : ENABLE")
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver disabled support for ENABLE_2084_DECODE in HDR Mode")
                    logging.error("Driver support for ENABLE_2084_DECODE - Expected : ENABLE; Actual : DISABLE")
                    return False
            else:
                ##
                # In SDR Mode, driver should not enable 2084_DECODE
                if self.GetValue(edp_hdr_ctrl_params, 0, 0) != ENABLE_2084_DECODE:
                    logging.info("Driver support for ENABLE_2084_DECODE - Expected : DISABLE; Actual : DISABLE")
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver enabled support for ENABLE_2084_DECODE in SDR Mode")
                    logging.error("Driver support for ENABLE_2084_DECODE - Expected : DISABLE; Actual : ENABLE")
                    return False
        else:
            logging.error("Display Caps ENABLE_2084_DECODE - Expected : ENABLE; Actual : DISABLE")
            return False

        ##
        # If the display caps support 2020 Gamut, then driver should support 2020 Gamut in HDR Mode
        if self.GetValue(edp_hdr_caps, 1, 1) == ENABLE_2020_GAMUT :
            logging.info("Display Caps ENABLE_2020_GAMUT - Expected : ENABLE; Actual : ENABLE")
            if hdr_mode:
                ##
                # In HDR mode, driver should enable ENABLE_2020_GAMUT
                if self.GetValue(edp_hdr_ctrl_params, 1, 1) == ENABLE_2020_GAMUT:
                    logging.info("Driver support for ENABLE_2020_GAMUT - Expected : ENABLE; Actual : ENABLE")
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver disabled support for ENABLE_2020_GAMUT in HDR Mode")
                    logging.error("Driver support for ENABLE_2020_GAMUT - Expected : ENABLE; Actual : DISABLE")
                    return False
            else:
                ##
                # In SDR mode, driver should enable ENABLE_2020_GAMUT
                if self.GetValue(edp_hdr_ctrl_params, 1, 1) != ENABLE_2020_GAMUT:
                    logging.info("Driver support for ENABLE_2020_GAMUT - Expected : DISABLE; Actual : DISABLE")
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver enabled support for ENABLE_2020_GAMUT in SDR Mode")
                    logging.error("Driver support for ENABLE_2020_GAMUT - Expected : DISABLE; Actual : ENABLE")
                    return False
        else:
            logging.info("Display Caps ENABLE_2020_GAMUT - Expected : ENABLE; Actual : DISABLE")
            return False
        ##
        # If the display caps support segmented backlight, then driver should enable support for segmented backlight
        if self.GetValue(edp_hdr_caps, 3, 3) == ENABLE_SEGMENTED_BKLGHT :
            logging.info("Display Caps ENABLE_SEGMENTED_BKLGHT - Expected : ENABLE; Actual : ENABLE")
            if self.GetValue(edp_hdr_ctrl_params, 3, 3) == ENABLE_SEGMENTED_BKLGHT:
                logging.info("Driver support for ENABLE_SEGMENTED_BKLGHT - Expected : ENABLE; Actual : ENABLE")
            else:
                gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver disabled support for ENABLE_SEGMENTED_BKLGHT")
                logging.error("Driver support for ENABLE_SEGMENTED_BKLGHT - Expected : ENABLE; Actual : DISABLE")
                return False
        else:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to display caps has no support for segmented backlight")
            logging.error("Display Caps ENABLE_SEGMENTED_BKLGHT - Expected : ENABLE; Actual : DISABLE")
            return False

        ##
        # If the display caps support brightness control via aux, then driver should enable support for brightness control via aux
        if self.GetValue(edp_hdr_caps, 4, 4) == ENABLE_BRIGHTNESS_CONTROL_USING_AUX:
            logging.info("Display Caps ENABLE_BRIGHTNESS_CONTROL_USING_AUX - Expected : ENABLE; Actual : ENABLE")
            if self.GetValue(edp_hdr_ctrl_params, 4, 4) == ENABLE_BRIGHTNESS_CONTROL_USING_AUX:
                logging.info("Driver support for ENABLE_BRIGHTNESS_CONTROL_USING_AUX - Expected : ENABLE; Actual : ENABLE")
            else:
                gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver disabled support for ENABLE_BRIGHTNESS_CONTROL_USING_AUX")
                logging.error("Driver support for ENABLE_BRIGHTNESS_CONTROL_USING_AUX - Expected : ENABLE; Actual : DISABLE")
                return False
        else:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to display caps has no support for brightness control")
            logging.error("Display Caps ENABLE_BRIGHTNESS_CONTROL_USING_AUX - Expected : ENABLE; Actual : DISABLE")
            return False

        ##
        # If the display caps support sdp support for colorimetry should be disabled,
        # then driver should enable support sdp support for colorimetry should be disabled
        if self.GetValue(edp_hdr_caps, 6, 6) == DISABLE_SDP_SUPPORT_FOR_COLORIMETRY:
            logging.info("Display Caps DISABLE_SDP_SUPPORT_FOR_COLORIMETRY - Expected : ENABLE; Actual : ENABLE")
            if self.GetValue(edp_hdr_ctrl_params, 6, 6) == DISABLE_SDP_SUPPORT_FOR_COLORIMETRY:
                logging.info(
                    "Driver support for DISABLE_SDP_SUPPORT_FOR_COLORIMETRY - Expected : ENABLE; Actual : DISABLE")
            else:
                gdhm_report_app_color(title="[COLOR][HDR]Driver enabled support for DISABLE_SDP_SUPPORT_FOR_COLORIMETRY")
                logging.error(
                    "Driver support for DISABLE_SDP_SUPPORT_FOR_COLORIMETRY - Expected : DISABLE; Actual : ENABLE")
                return False
        else:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to display caps support for brightness control enabled")
            logging.error("Display Caps DISABLE_SDP_SUPPORT_FOR_COLORIMETRY - Expected : DISABLE; Actual : ENABLE")
            return False

        ##
        # Supports sRGB Panel gamut conversion : This is needed only in SDR Mode, hence should be disabled in HDR Mode
        if self.GetValue(edp_hdr_caps, 7, 7) == DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION:
            logging.info("Display Caps DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : ENABLE ")
            ##
            # In HDR Mode, sRGB Panel Gamut conversion should be disabled
            if hdr_mode:
                if self.GetValue(edp_hdr_ctrl_params, 7, 7) == DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION:
                    logging.info("Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : ENABLE")
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver disabled support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION")
                    logging.error("Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : ENABLE; Actual : DISABLE")
                    return False
            ##
            # In SDR Mode, sRGB Panel Gamut conversion should be disabled
            else:
                if self.GetValue(edp_hdr_ctrl_params, 7, 7) != DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION:
                    logging.info("Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : DISABLE; Actual : DISABLE")
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Failed due to Driver enabled support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION")
                    logging.error("Driver support for DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : DISABLE; Actual : ENABLE")
                    return False
        else:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to in Display Caps  ENABLE_SEGMENTED_BKLGHT was disabled")
            logging.error("Display Caps DISABLE_SRGB_TO_PANEL_GAMUT_CONVERSION - Expected : DISABLE; Actual : ENABLE")
            return False
        return True

    def verify_hdr_content_maxcll_maxfall(self, content_luminance_address_list, target_id):
        dpcd_lum = []
        for addr_index in range(len(content_luminance_address_list)):
            dpcd_lum.append(fetch_dpcd_data(content_luminance_address_list[addr_index], target_id))

        max_cll_val = self.GetValue(dpcd_lum[1], 0, 7) << 8 | self.GetValue(dpcd_lum[0], 0, 7)
        logging.info("Expected MaxCLL : %s; Actual MaxCLL : %s" % (GOLDEN_CONTENT_LUMINANCE_MAX_CLL, max_cll_val))
        if max_cll_val != GOLDEN_CONTENT_LUMINANCE_MAX_CLL:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to mismatch of luminace MaxCLL")
            return False

        max_fall_val = self.GetValue(dpcd_lum[3], 0, 7) << 8 | self.GetValue(dpcd_lum[2], 0, 7)
        logging.info("Expected MaxFALL : %s; Actual MaxFALL : %s" % (GOLDEN_CONTENT_LUMINANCE_MAX_FALL, max_fall_val))
        if max_fall_val != GOLDEN_CONTENT_LUMINANCE_MAX_FALL:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to mismatch of luminace MaxFALL")
            return False

        return True

    def verify_hdr_panel_override_maxcll_maxfall(self, edp_hdr_caps,edp_hdr_ctrl_params,panel_override_address_list, target_id, target_nits):
        dpcd_lum = []
        for addr_index in range(len(panel_override_address_list)):
            dpcd_lum.append(fetch_dpcd_data(panel_override_address_list[addr_index], target_id))

        max_cll_val = self.GetValue(dpcd_lum[1], 0, 7) << 8 | self.GetValue(dpcd_lum[0], 0, 7)
        logging.info("Expected MaxCLL : %s; Actual MaxCLL : %s" % (GOLDEN_PANEL_OVERRIDE_MAX_CLL, max_cll_val))
        if max_cll_val != GOLDEN_PANEL_OVERRIDE_MAX_CLL:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to mismatch of override MaxCLL")
            return False

        max_fall_val = self.GetValue(dpcd_lum[3], 0, 7) << 8 | self.GetValue(dpcd_lum[2], 0, 7)
        logging.info("Expected MaxFALL : %s; Actual MaxFALL : %s" % (GOLDEN_PANEL_OVERRIDE_MAX_FALL, max_fall_val))
        if max_fall_val != GOLDEN_PANEL_OVERRIDE_MAX_FALL:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to mismatch of override MaxFALL")
            return False

        ##
        # If the display caps support panel tone mapping, driver should enable support for panel tone mapping
        if self.GetValue(edp_hdr_caps, 2, 2) == ENABLE_PANEL_TONE_MAPPING:
            logging.info("Display Caps ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : ENABLE")
            ##
            # Driver enables support for panel tone mapping only when target nits is greater than panel nits
            if target_nits > max_cll_val:
                if self.GetValue(edp_hdr_ctrl_params, 3, 3) == ENABLE_PANEL_TONE_MAPPING:
                    logging.info("Driver support for ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : ENABLE")
                else:
                    gdhm_report_app_color(title="[COLOR][HDR]Failed due to driver disabled the support for ENABLE_PANEL_TONE_MAPPING")
                    logging.error("Driver support for ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : DISABLE")
                    return False
        else:
            gdhm_report_app_color(title="[COLOR][HDR]Failed due to in display caps ENABLE_PANEL_TONE_MAPPING was disabled")
            logging.error("Display Caps ENABLE_PANEL_TONE_MAPPING - Expected : ENABLE; Actual : DISABLE")
            return False

        return True

    def perform_dpcd_verification(self, target_id, target_nits):
        ##
        # Verify the eDP_HDR Caps details
        edp_hdr_caps = fetch_dpcd_data(EDP_HDR_CAPS_BYTE1, target_id)
        edp_hdr_ctrl_params = fetch_dpcd_data(EDP_HDR_GET_SET_CTRL_PARAMS_BYTE0, target_id)
        if not self.verify_edp_hdr_display_caps_and_ctrl_params(edp_hdr_caps, edp_hdr_ctrl_params):
            return False

        ##
        # Verify the Content MaxCLL and MaxFALL
        content_luminance_address_list = [EDP_HDR_CONTENT_LUMINANCE_BYTE0, EDP_HDR_CONTENT_LUMINANCE_BYTE1,
                                          EDP_HDR_CONTENT_LUMINANCE_BYTE2, EDP_HDR_CONTENT_LUMINANCE_BYTE3]
        if not self.verify_hdr_content_maxcll_maxfall(content_luminance_address_list, target_id):
            return False

        ##
        # Verify the PanelOverride MaxCLL and MaxFALL
        panel_override_address_list = [EDP_HDR_PANEL_LUMINANCE_OVERRIDE_BYTE0, EDP_HDR_PANEL_LUMINANCE_OVERRIDE_BYTE1,
                                          EDP_HDR_PANEL_LUMINANCE_OVERRIDE_BYTE2, EDP_HDR_PANEL_LUMINANCE_OVERRIDE_BYTE3]
        if not self.verify_hdr_panel_override_maxcll_maxfall(edp_hdr_caps,edp_hdr_ctrl_params,panel_override_address_list, target_id, target_nits):
            return False

        return True

    ##
    # Perform register level verification for Metadata
    def verify_metadata(self, display, current_pipe,target_id, blending_mode, reference_metadata, pcon=False):
        logging.debug("Reference Metadata : %s" % reference_metadata)
        programmed_metadata = []
        base_offset = 0
        self.str_pipe = self.mapPlanePipeIDToStringForRegVerification(current_pipe, 0, True)
        if display[:4] == 'HDMI':
            ##
            # Read from DRM_DATA
            module_name = "VIDEO_DIP_DRM_DATA_REGISTER"
            reg_name = "VIDEO_DIP_DRM_DATA_0" + "_" + self.str_pipe
            instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
            base_offset = instance.offset

        elif display[:2] == 'DP':
            if display_utility.get_vbt_panel_type(display, 'gfx_0') in [display_utility.VbtPanelType.LFP_DP,
                                                                        display_utility.VbtPanelType.LFP_MIPI]:
                edp_hdr_caps = fetch_dpcd_data(EDP_HDR_CAPS_BYTE1, target_id)
                sdp_enable = self.GetValue(edp_hdr_caps, 6, 6)
                ##
                # If sdp_support is not enabled, then it indicates Aux
                if sdp_enable:
                    logging.debug("SDP Based eDP; Hence verify from the GMP Registers")
                else:
                    target_nits = reference_metadata[12]
                    if not self.perform_dpcd_verification(target_id, target_nits):
                        return False
                    return True
            ##
            # For both SDP based eDP and DP, read from GMP_DATA
            module_name = "VIDEO_DIP_GMP_DATA_REGISTER"
            reg_name = "VIDEO_DIP_GMP_DATA_0_" + self.str_pipe
            instance = MMIORegister.get_instance(module_name, reg_name, self.platform)
            base_offset = instance.offset
        else:
            logging.error("Invalid Display passed for metadata verification")
            return False

        for index in range(0, METADATA_LENGTH):
            programmed_metadata.append(self.driver_interface_.mmio_read(base_offset, 'gfx_0'))
            base_offset = base_offset + 4

        parsed_metadata = self.parse_and_rearrange_prog_metadata(display, programmed_metadata, pcon)

        index = 0
        for reg_val, ref_val in zip(parsed_metadata, reference_metadata):
            if reg_val != ref_val:
                logging.error(
                    "Metadata programming not matching at index: %d Programmed Val : %d Expected Val : %d", index,
                    reg_val, ref_val)
                gdhm_report_app_color(title="[COLOR][HDR]Verification of Metadata programming failed due to mismatch")
                return False
            index += 1
        return True


if __name__ == "__main__":
    # print os.getcwd()
    hdr = HDRVerification()
    hdr.verifyHDRPlaneProgramming(0, 0, Enums.SB_PIXELFORMAT.SB_YUV422, 10, BlendingMode.BT2020_LINEAR)
    # hdr.verifyHDRPipeProgramming(0,BlendingMode.BT2020_LINEAR,PanelType.EFP,PanelCaps.HDR_BT2020_YUV420,OutputRange.STUDIO)
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

# End
