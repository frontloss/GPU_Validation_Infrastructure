import logging
import math
import os
import sys

import Tests.Color.ColorTransforms.color_transforms_constants as const
from Libs.Core import cmd_parser
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.mmioregister import MMIORegister

MAX_CSC_VAL = 3.99


class BlendingMode(object):
    SRGB_NON_LINEAR = 0
    BT2020_NON_LINEAR = 1
    BT2020_LINEAR = 2


class ColorTransforms_Verification(object):
    driver_interface_ = driver_interface.DriverInterface()
    machine_info = SystemInfo()
    custom_tags = ["-ICCPROFILENAME", "-HDRMODE", "-CUIBRIGHTNESS"]
    my_tags = ["ICCPROFILENAME", "HDRMODE", "CUIBRIGHTNESS"]
    custom_opt = {}
    platform = None
    str_pipe = None
    profile_matrix = [None, None, None]
    cui_lut = []
    csc_threshold = 0.25
    lut_threshold = 2
    dir_name = os.path.dirname(os.path.realpath(__file__))
    connected_list = []

    def setup(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        profiles_list = []

        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])
            elif key in self.my_tags and value != 'NONE':
                self.custom_opt[key] = value

        display_config = DisplayConfiguration()
        current_config = display_config.get_current_display_configuration()
        NoOfDisplays = current_config.numberOfDisplays

        if ("ICCPROFILENAME" in colortransforms.custom_opt.keys()):
            profiles_list = colortransforms.custom_opt["ICCPROFILENAME"][0].split(",")
        for current_pipe in range(0, NoOfDisplays):
            profile_name = profiles_list[current_pipe]

            if (profile_name in "MHC2_SRGB_IDENTITYCSC_400NITS.ICM"):
                self.profile_matrix[current_pipe] = const.ICC_Profile_Identity_Matrix
            elif (profile_name.lower() in "MHC2_sRGB_RgbSwapCSC_400nits.icm".lower()):
                self.profile_matrix[current_pipe] = const.ICC_Profile_RGBSwap_Matrix

    def GetValue(self, value, start, end):

        retvalue = value << (31 - end) & 0xffffffff
        retvalue = retvalue >> (31 - end + start) & 0xffffffff
        return retvalue

    def GetValue64(self, value, start, end):

        retvalue = value << (63 - end) & 0xffffffffffffffff
        retvalue = retvalue >> (63 - end + start) & 0xffffffffffffffff
        return retvalue

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

    def compareCSCCoeff(self, progVal, refVal):
        logging.info("Programmed Value : %s Reference Value %s" % (progVal, refVal))
        result = True
        for i in range(0, 3):
            for j in range(0, 3):

                ref = round(refVal[i][j], 5)
                prog = round(progVal[i][j], 5)
                if (ref * prog >= 0.0):  # Same sign
                    if (math.fabs(prog - ref) >= self.csc_threshold):
                        logging.info("Coeff Values didnt match Pos : %d,%d Programmed Val : %f Expected Val : %f", i, j,
                                     progVal[i][j], refVal[i][j])
                        result = False
                elif (abs(prog - ref) >= self.csc_threshold):
                    logging.info("Coeff Values didnt match Pos : %d,%d Programmed Val : %f Expected Val : %f", i, j,
                                 progVal[i][j], refVal[i][j])
                    result = False
        return result

    def matrix_multiply_3X3(self, matrix1, matrix2):
        resultant_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # iterate through rows of X
        for i in range(len(matrix1)):
            # iterate through columns of Y
            for j in range(len(matrix2[0])):
                # iterate through rows of Y
                for k in range(len(matrix2)):
                    resultant_matrix[i][j] += round(matrix1[i][k], 5) * round(matrix2[k][j], 5)

        return resultant_matrix

    def scaleCoeffWithHWLimits(self, refVal):
        # Find the max value in the coeff
        max_val = 0
        for i in range(0, 3):
            for j in range(0, 3):
                coeff = abs(refVal[i][j])
                if (coeff > max_val):
                    max_val = coeff

        if (max_val > MAX_CSC_VAL):
            scale_factor = MAX_CSC_VAL / max_val
            for i in range(0, 3):
                for j in range(0, 3):
                    refVal[i][j] = refVal[i][j] * scale_factor
        return refVal

    def verify_pipe_csc_programming(self, csc_mode_reg, blendingMode, icc_profile_matrix):
        status = True
        if (csc_mode_reg.pipe_csc_enable == 1):
            logging.info("Pipe CSC - Enabled")
            reg_name = "CSC_COEFF"
            refVal = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            progVal = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            rgb_xyz_matrix = []
            xyz_rgb_matrix = []
            progVal = self.getCSCCoeffMatrixFromReg(reg_name, self.str_pipe)
            if (blendingMode == BlendingMode.BT2020_LINEAR):
                rgb_xyz_matrix = const.BT2020_RGB_to_XYZ_conversion
                xyz_rgb_matrix = const.XYZ_to_BT2020_RGB_conversion
            elif (blendingMode == BlendingMode.SRGB_NON_LINEAR):
                rgb_xyz_matrix = const.BT709_RGB_to_XYZ_conversion
                xyz_rgb_matrix = const.XYZ_to_BT709_RGB_conversion

            # Convert RGB->XYZ matrix based on blending mode
            inter_matrix = self.matrix_multiply_3X3(icc_profile_matrix, rgb_xyz_matrix)
            refVal = self.matrix_multiply_3X3(xyz_rgb_matrix, inter_matrix)

            refVal = self.scaleCoeffWithHWLimits(refVal)
            for i in range(0, 3):
                for j in range(0, 3):
                    refVal[i][j] = round(refVal[i][j], 5)
            logging.info("***********************PIPE CSC***************************")
            logging.info("Programmed Matrix : %s" % progVal)
            logging.info("Reference Matrix : %s" % refVal)
            result = True
            result = self.compareCSCCoeff(progVal, refVal)
            if (result is False):
                logging.error(" PipeCSC coeff mismatch!!")
                status = False

        else:
            logging.error("Pipe CSC  NOT ENABLED")
            status = False
        return status

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
        return lut_data

    def compareGammaLUT(self, progLUT, refLUT):
        result = True
        index = 0
        for reg_val, ref_val in zip(progLUT, refLUT):
            if (math.fabs(reg_val - ref_val) >= self.lut_threshold):
                logging.info("Gamma LUT values not matching Index : %d Programmed Val : %d Expected Val : %d", index,
                             reg_val, ref_val)
                result = False
            index += 1
        return result

    def verify_pipe_degamma_programming(self, gamma_mode_reg, blendingMode):
        status = True
        if (gamma_mode_reg.pre_csc_gamma_enable == 1):
            logging.info("Pipe pre CSC Gamma - Enabled")
            reg_name = "PRE_CSC_GAMC"
            no_samples = 35
            progLUT = None
            refLUT = None
            result = True
            progLUT = self.getGammLUTFromReg(reg_name, no_samples, self.str_pipe)
            if (blendingMode == BlendingMode.SRGB_NON_LINEAR or blendingMode == BlendingMode.BT2020_NON_LINEAR):
                refLUT = const.SRGB_Decode_35_Samples_16bpc
            elif (blendingMode == BlendingMode.BT2020_LINEAR):
                logging.info(
                    "Pipe Pre CSC Gamma enabled for linear blending mode when not required for Colortransforms.Skipping pipe degamma verification")
                status = True
                return
            logging.info("**********************PIPE PRE CSC GAMMA**************************")
            logging.info("ProgLUT : %s" % progLUT)
            logging.info("Reference LUT : %s" % refLUT)

            result = self.compareGammaLUT(progLUT, refLUT)

            if (result is False):
                logging.error(" Pipe DeGamma mismatch!!")
                status = False

        else:
            if (blendingMode == BlendingMode.SRGB_NON_LINEAR):
                logging.error("Pipe Pre CSC Gamma not enabled for non linear blending mode!!")
                status = False
        return status

    def getPipeGammaLUTFromReg(self, gamma_mode):

        lut_data = []

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
        index_reg.asUint = 0
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

        module_name = "PAL_PREC_DATA_REGISTER"
        reg_name = "PAL_PREC_DATA_" + self.str_pipe
        for index in range(0, 1024, 2):
            index_reg.index_value = index
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
            data_reg1 = MMIORegister.read(module_name, reg_name, self.platform)
            index_reg.index_value = index + 1
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
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

    def read_profile_lut_from_file(self, file_name):
        profile_lut = []
        file_name_path = os.path.join(self.dir_name, file_name)
        with open(file_name_path, 'r') as file_obj:
            while True:
                string = file_obj.readline()
                if string == "":
                    break
                val = int(string, 16)
                profile_lut.append(val)

        return profile_lut

    def combineLUT(self, base_lut, baselut_no_samples, relative_lut, relativelut_no_samples):
        dest_lut = []
        for index in range(0, baselut_no_samples):
            dest_lut.append(self.applyLUT(relative_lut, relativelut_no_samples, base_lut[index]))
        return dest_lut

    def applyLUT(self, lut_data, lut_no_samples, input_val):
        # print "InputVal",input_val
        correction = 0
        resIndex = (lut_no_samples - 1) * input_val
        # print "resIndex",hex(resIndex)
        weight = self.GetValue64(resIndex, 0, 23)
        # print "Weight",hex(weight)
        index = self.GetValue64(resIndex, 24, 63)
        # print "Index",hex(index)
        next_index = index + 1

        out_val = lut_data[index]
        # print "bEFORE CORRECTION", hex(out_val)
        if (next_index < (lut_no_samples - 1)):
            correction = lut_data[next_index] - lut_data[index]
            correction = correction * weight
            correction = correction >> 24
        # print " Correction",hex(correction)
        out_val = out_val + correction
        # print "OtVal",hex(out_val)
        return out_val

    def scale_values_from_24_to_16bpc(self, refLUT, no_of_samples):
        resultantLUT = []
        for index in range(0, no_of_samples):
            if (refLUT[index] < 16777216):  # 2^24
                val = refLUT[index] >> 8
            else:
                val = 16777216 >> 8
            resultantLUT.append(val)
        return resultantLUT

    def apply_cui_brightness_scalar(self, cui_brightness_val, refLUT, no_of_samples):
        resultant_lut = []
        for index in range(0, no_of_samples):
            adder = 257 * cui_brightness_val
            val = refLUT[index] + adder
            if (val > 65536):
                val = 65536
            resultant_lut.append(val)
        return resultant_lut

    def verify_pipe_gamma_programming(self, gamma_mdoe_reg, cui_brightness_val, ref_profile_filename):
        no_of_samples = 0
        status = True
        if (gamma_mode_reg.post_csc_gamma_enable == 1):
            progLUT = None
            refLUT = None
            baseLUT = []
            logging.info("Pipe post CSC Gamma  Enabled")
            if (gamma_mode_reg.gamma_mode == 3):
                progLUT = self.getPipeGammaLUTFromReg("MULTI_SEGMENT")
                baseLUT = const.OETF_2084_10KNits_524Samples_8_24_FORMAT
                no_of_samples = 524
            else:
                if (gamma_mode_reg.gamma_mode == 2):
                    progLUT = self.getPipeGammaLUTFromReg("12BIT_GAMMA")
                    baseLUT = const.OETF_SRGB_515Samples_8_24_FORMAT
                    no_of_samples = 515

            profile_lut = self.read_profile_lut_from_file(ref_profile_filename)

            refLUT = self.combineLUT(baseLUT, no_of_samples, profile_lut, 4096)

            refLUT = self.scale_values_from_24_to_16bpc(refLUT, no_of_samples)

            if (cui_brightness_val != 0):
                refLUT = self.apply_cui_brightness_scalar(cui_brightness_val, refLUT, no_of_samples)

            logging.info("**********************PIPE POST  CSC GAMMA**************************")
            logging.info("ProgLUT : %s" % progLUT)
            logging.info("Reference LUT : %s" % refLUT)

            result = self.compareGammaLUT(progLUT, refLUT)

            if (result is False):
                logging.error(" Pipe Gamma mismatch!!")
                status = False

        else:
            logging.error("Pipe Gamma NOT ENABLED !!!")
            status = False

        return status


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=FORMAT)
    logger = logging.getLogger("")

    logger.setLevel(logging.INFO)

    test_result = True
    hdrmode_list = []
    blending_mode = BlendingMode.SRGB_NON_LINEAR
    colortransforms = ColorTransforms_Verification()

    ##
    # Call setup to initialize
    colortransforms.setup()

    display_config = DisplayConfiguration()
    current_config = display_config.get_current_display_configuration()
    NoOfDisplays = current_config.numberOfDisplays

    if ("HDRMODE" in colortransforms.custom_opt.keys()):
        hdrmode_list = colortransforms.custom_opt["HDRMODE"][0].split(",")
    for current_index in range(0, NoOfDisplays):
        if (hdrmode_list[current_index] == "ON"):
            blending_mode = BlendingMode.BT2020_LINEAR
        elif (hdrmode_list[current_index] == "OFF"):
            blending_mode = BlendingMode.SRGB_NON_LINEAR

        if ("CUIBRIGHTNESS" in colortransforms.custom_opt.keys()):
            cui_brightness_val = int(colortransforms.custom_opt["CUIBRIGHTNESS"][current_index])
        else:
            cui_brightness_val = 0

        display_base_obj = DisplayBase(colortransforms.connected_list[current_index])
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(
            colortransforms.connected_list[current_index])
        colortransforms.str_pipe = chr(int(current_pipe) + 65)
        reg_name = "GAMMA_MODE" + "_" + colortransforms.str_pipe
        gamma_mode_reg = MMIORegister.read("GAMMA_MODE_REGISTER", reg_name, colortransforms.platform)
        reg_name = "CSC_MODE" + "_" + colortransforms.str_pipe
        csc_mode_reg = MMIORegister.read("CSC_MODE_REGISTER", reg_name, colortransforms.platform)

        csc_status = colortransforms.verify_pipe_csc_programming(csc_mode_reg, blending_mode,
                                                                 colortransforms.profile_matrix[current_index])
        degamma_status = colortransforms.verify_pipe_degamma_programming(gamma_mode_reg, blending_mode)
        gamma_status = colortransforms.verify_pipe_gamma_programming(gamma_mode_reg, cui_brightness_val,
                                                                     "RealUnity_OSLUT.txt")
        if (gamma_status is False):
            logging.info("^^^^^^^^Rechecking with UnityOS LUT^^^^^^^^^^^^^^^")
            gamma_status = colortransforms.verify_pipe_gamma_programming(gamma_mode_reg, cui_brightness_val,
                                                                         "Unity_OSLUT.txt")
        if (gamma_status is False):
            logging.info("^^^^^^^^Rechecking with 19H1 UnityOS LUT^^^^^^^^^^^^^^^")
            gamma_status = colortransforms.verify_pipe_gamma_programming(gamma_mode_reg, cui_brightness_val,
                                                                         "19H1_OS_Unity_LUT.txt")

        logging.info("=========================================================================================")
        logging.info("Display - %d", current_index)
        if (csc_status is False or degamma_status is False or gamma_status is False):
            test_result = False
            logging.error("                      TEST STATUS = FAIL                 ")
        else:
            logging.info("                      TEST STATUS = PASS                 ")
        logging.info("=========================================================================================")

    logging.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if (test_result is False):
        logging.error("                           FINAL TEST RESULT = FAIL !!!                   ")
    else:
        logging.info("                           FINAL TEST RESULT = PASS                       ")
    logging.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
