########################################################################################################################
# @file         hw_accuracy_programregisters.py
# @brief        This script contains test to flip single plane on single with specified parameters . Disable all color
#               blocks and capture the output dump for image comparison
# @author       R Soorya
########################################################################################################################
import math

from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from registers.mmioregister import MMIORegister

machine_info = SystemInfo()
platform = None

gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break

##
# @brief    Contains various functions to verify hardware accuracy of program registers
class HW_Accuracy_Programming(object):
    driver_interface_ = driver_interface.DriverInterface()
    str_pipe = ""

    ##
    # @brief        To reset all color registers
    # @param[in]    str_plane_pipe string containing details about plane and pipe
    # @param[in]    str_pipe string contains details of the pipe(A/B/C/D)
    # @return       None
    def resetAllColorRegisters(self, str_plane_pipe, str_pipe):
        module_name = "PLANE_COLOR_CTL_REGISTER"
        reg_name = "PLANE_COLOR_CTL" + "_" + str_plane_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        color_ctl_offset = instance.offset

        module_name = "PLANE_PIXEL_NORMALIZE_REGISTER"
        reg_name = "PLANE_PIXEL_NORMALIZE" + "_" + str_plane_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        plane_pixel_normalize_offset = instance.offset

        module_name = "GAMMA_MODE_REGISTER"
        reg_name = "GAMMA_MODE" + "_" + str_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        gamma_mode_offset = instance.offset

        module_name = "CSC_MODE_REGISTER"
        reg_name = "CSC_MODE" + "_" + str_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        csc_mode_offset = instance.offset

        module_name = "PIPE_MISC_REGISTER"
        reg_name = "PIPE_MISC" + "_" + str_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        pipe_misc_offset = instance.offset
        pipe_misc_value = self.driver_interface_.mmio_read(pipe_misc_offset, 'gfx_0')
        pipe_misc_override = pipe_misc_value & 0xFF7FFFEF  # Display Dithering & HDR Mode

        self.driver_interface_.mmio_write(color_ctl_offset, 0x10002000, 'gfx_0')
        self.driver_interface_.mmio_write(plane_pixel_normalize_offset, 0x0, 'gfx_0')
        self.driver_interface_.mmio_write(gamma_mode_offset, 0x0, 'gfx_0')
        self.driver_interface_.mmio_write(csc_mode_offset, 0x0, 'gfx_0')
        self.driver_interface_.mmio_write(pipe_misc_offset, pipe_misc_override, 'gfx_0')

    ##
    # @brief        To program plane alpha
    # @param[in]    str_plane_pipe string containing details about plane and pipe
    # @return       None
    def programPlaneAlpha(self, str_plane_pipe):
        module_name = "PLANE_COLOR_CTL_REGISTER"
        reg_name = "PLANE_COLOR_CTL" + "_" + str_plane_pipe
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        color_ctl_offset = instance.offset
        color_ctl_data = MMIORegister.read(module_name, reg_name, platform)
        color_ctl_data.alpha_mode = 1

        self.driver_interface_.mmio_write(color_ctl_offset, color_ctl_data, 'gfx_0')

    ##
    # @brief        To program plane color control register
    # @return       None
    def program_plane_color_ctrl_register(self):
        pass

    ##
    # @brief        To program gamma mode register
    # @return       None
    def program_gamma_mode_register(self):
        pass

    ##
    # @brief        To program csc mode register
    # @return       None
    def program_csc_mode_register(self):
        pass

    ##
    # @brief        To program gamma lut registers
    # @param[in]    unit_name instance of the register
    # @param[in]    no_samples number of samples
    # @param[in]    lut_data lut values
    # @param[in]    str Id of the pipe (A/B/C/D)
    # @return       None
    def program_gamma_lut_registers(self, unit_name, no_samples, lut_data, str):

        # Setting auto increment bit to 1 in index register
        module_name = unit_name + "_INDEX_REGISTER"
        reg_name = unit_name + "_INDEX_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        index_offset = instance.offset
        index_reg = MMIORegister.read(module_name, reg_name, platform)
        index_reg.index_auto_increment = 1
        index_reg.index_value = 0
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

        module_name = unit_name + "_DATA_REGISTER"
        reg_name = unit_name + "_DATA_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        data_offset = instance.offset

        for index in range(0, no_samples):
            self.driver_interface_.mmio_write(index_offset, index, 'gfx_0')
            self.driver_interface_.mmio_write(data_offset, lut_data[index], 'gfx_0')

        return

    ##
    # @brief        To program multi segment gamma lut registers
    # @param[in]    seg0_unit_name instance of the register
    # @param[in]    seg0_no_samples number of samples for segment 0
    # @param[in]    seg1_unit_name instance of the register
    # @param[in]    seg1_no_samples number of samples for segment 1
    # @param[in]    lut_data lut values
    # @param[in]    str Id of the pipe(A/B/C/D)
    # @return       True if dithering bit behavior is as expected as False
    def program_multisegment_gamma_lut_registers(self, seg0_unit_name, seg0_no_samples, seg1_unit_name, seg1_no_samples,
                                                 lut_data, str):

        # Setting auto increment bit to 1 in index register
        module_name = seg0_unit_name + "_INDEX_REGISTER"
        reg_name = seg0_unit_name + "_INDEX_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        index_offset = instance.offset
        index_reg = MMIORegister.read(module_name, reg_name, platform)
        index_reg.index_auto_increment = 1
        index_reg.index_value = 0
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

        count = 0

        module_name = seg0_unit_name + "_DATA_REGISTER"
        reg_name = seg0_unit_name + "_DATA_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        data_offset = instance.offset

        for index in range(0, seg0_no_samples):
            self.driver_interface_.mmio_write(data_offset, lut_data[count], 'gfx_0')
            count = count + 1

        module_name = seg1_unit_name + "_INDEX_REGISTER"
        reg_name = seg1_unit_name + "_INDEX_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        index_offset = instance.offset
        index_reg = MMIORegister.read(module_name, reg_name, platform)
        index_reg.index_auto_increment = 1
        index_reg.index_value = 0
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

        module_name = seg1_unit_name + "_DATA_REGISTER"
        reg_name = seg1_unit_name + "_DATA_" + str
        instance = MMIORegister.get_instance(module_name, reg_name, platform)
        data_offset = instance.offset

        for index in range(0, seg1_no_samples):
            self.driver_interface_.mmio_write(data_offset, lut_data[index], 'gfx_0')
            count = count + 1
        return

    ##
    # @brief        To program pipe palette registers
    # @param[in]    gamma_mode (MULTI_SEGMENT/12_BIT_GAMMA_MODE)
    # @param[in]    multi_segment_unit_name instance of the multi segment register
    # @param[in]    gamma_lut_unit_name instance of the gamma lut register
    # @param[in]    no_samples number of samples
    # @param[in]    lut_data lut values
    # @param[in]    is_ext_registers_available boolean value True if extra registers are available
    # @return       None
    def program_pipe_palette_registers(self, gamma_mode, multi_segment_unit_name, gamma_lut_unit_name, no_samples,
                                       lut_data, is_ext_registers_available=False):

        if (gamma_mode == "MULTI_SEGMENT"):
            module_name = multi_segment_unit_name + "_INDEX_REGISTER"
            reg_name = multi_segment_unit_name + "_INDEX_" + self.str_pipe
            index_reg = MMIORegister.get_instance(module_name, reg_name, platform)
            index_offset = index_reg.offset
            index_reg.index_auto_increment = 1
            index_reg.index_value = 0
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

            # MultiSegment Palette Prec Data
            module_name = multi_segment_unit_name + "_DATA_REGISTER"
            reg_name = multi_segment_unit_name + "_DATA_" + self.str_pipe
            data_reg = MMIORegister.get_instance(module_name, reg_name, platform)
            data_offset = data_reg.offset

            count = 0

            for index in range(0, 18, 2):
                even_data = (lut_data[count] & 0x3f) << 4
                odd_data = (lut_data[count + 1] >> 6) & 0x3ff
                index_reg.index_value = index
                self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
                data_reg.blue_precision_palette_entry = even_data
                data_reg.green_precision_palette_entry = even_data
                data_reg.red_precision_palette_entry = even_data
                self.driver_interface_.mmio_write(data_offset, data_reg.asUint, 'gfx_0')

                index_reg.index_value = index + 1
                self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
                data_reg.blue_precision_palette_entry = odd_data
                data_reg.green_precision_palette_entry = odd_data
                data_reg.red_precision_palette_entry = odd_data
                self.driver_interface_.mmio_write(data_offset, data_reg.asUint, 'gfx_0')

                count = count + 2

        # Palette Prec Data
        module_name = gamma_lut_unit_name + "_INDEX_REGISTER"
        reg_name = gamma_lut_unit_name + "_INDEX_" + self.str_pipe
        index_reg = MMIORegister.get_instance(module_name, reg_name, platform)
        index_offset = index_reg.offset
        index_reg.index_auto_increment = 1
        index_reg.index_value = 1
        self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')

        module_name = gamma_lut_unit_name + "_DATA_REGISTER"
        reg_name = gamma_lut_unit_name + "_DATA_" + self.str_pipe
        data_reg = MMIORegister.get_instance(module_name, reg_name, platform)
        data_offset = data_reg.offset
        count = 0
        for index in range(0, no_samples, 2):
            even_data = (lut_data[count] & 0x3f) << 4
            odd_data = (lut_data[count + 1] >> 6) & 0x3ff
            index_reg.index_value = index
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
            data_reg.blue_precision_palette_entry = even_data
            data_reg.green_precision_palette_entry = even_data
            data_reg.red_precision_palette_entry = even_data
            self.driver_interface_.mmio_write(data_offset, data_reg.asUint, 'gfx_0')

            index_reg.index_value = index + 1
            self.driver_interface_.mmio_write(index_offset, index_reg.asUint, 'gfx_0')
            data_reg.blue_precision_palette_entry = odd_data
            data_reg.green_precision_palette_entry = odd_data
            data_reg.red_precision_palette_entry = odd_data
            self.driver_interface_.mmio_write(data_offset, data_reg.asUint, 'gfx_0')

            count = count + 2

        if (is_ext_registers_available):
            module_name = "PAL_GC_MAX_REGISTER"
            reg_name = "PAL_GC_MAX_" + self.str_pipe
            pal_gc_max = MMIORegister.get_instance(module_name, reg_name, platform)
            pal_gc_max_offset = pal_gc_max.offset
            pal_gc_max.red_max_gc_point = lut_data[count]

            self.driver_interface_.mmio_write(pal_gc_max_offset, pal_gc_max.red_max_gc_point, 'gfx_0')
            self.driver_interface_.mmio_write(pal_gc_max_offset + 4, pal_gc_max.red_max_gc_point, 'gfx_0')
            self.driver_interface_.mmio_write(pal_gc_max_offset + 8, pal_gc_max.red_max_gc_point, 'gfx_0')

            module_name = "PAL_EXT_GC_MAX_REGISTER"
            reg_name = "PAL_EXT_GC_MAX_" + self.str_pipe
            pal_ext_gc_max = MMIORegister.get_instance(module_name, reg_name, platform)
            pal_ext_gc_max_offset = pal_ext_gc_max.offset
            pal_ext_gc_max.red_max_gc_point = lut_data[count]

            self.driver_interface_.mmio_write(pal_ext_gc_max_offset, pal_ext_gc_max.red_max_gc_point, 'gfx_0')
            self.driver_interface_.mmio_write(pal_ext_gc_max_offset + 4, pal_ext_gc_max.red_max_gc_point, 'gfx_0')
            self.driver_interface_.mmio_write(pal_ext_gc_max_offset + 8, pal_ext_gc_max.red_max_gc_point, 'gfx_0')

            module_name = "PAL_EXT2_GC_MAX_REGISTER"
            reg_name = "PAL_EXT2_GC_MAX_" + self.str_pipe
            pal_ext2_gc_max = MMIORegister.get_instance(module_name, reg_name, platform)
            pal_ext2_gc_max_offset = pal_ext2_gc_max.offset
            pal_ext2_gc_max.red_max_gc_point = lut_data[count]

            self.driver_interface_.mmio_write(pal_ext2_gc_max_offset, pal_ext2_gc_max.red_max_gc_point, 'gfx_0')
            self.driver_interface_.mmio_write(pal_ext2_gc_max_offset + 4, pal_ext2_gc_max.red_max_gc_point, 'gfx_0')
            self.driver_interface_.mmio_write(pal_ext2_gc_max_offset + 8, pal_ext2_gc_max.red_max_gc_point, 'gfx_0')

    ##
    # @brief        To program csc registers
    # @param[in]    unit_name instance of the register
    # @param[in]    csc_matrix
    # @return       None
    def program_csc_registers(self, unit_name, csc_matrix):
        csc_coeff = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        module_name = unit_name + "_REGISTER"
        reg_name = unit_name + "_" + str
        csc_reg = MMIORegister.get_instance(module_name, reg_name, platform)
        base_offset = csc_reg.offset

        for i in range(0, 3):
            for j in range(0, 3):
                csc_coeff[i][j] = self.convert_csc_coeff_to_regformat(csc_matrix[i][j])

        for i in range(0, 3):
            offset = (base_offset + i * 8)  # 2 DWORDS for each row RGB
            csc_reg.coeff1 = csc_coeff[i][0]
            csc_reg.coeff2 = csc_coeff[i][1]
            self.driver_interface_.mmio_write(offset, csc_reg.asUint, 'gfx_0')
            csc_reg.coeff1 = csc_coeff[i][2]
            self.driver_interface_.mmio_write(offset + 4, csc_reg.asUint, 'gfx_0')

    ##
    # @brief        To convert csc coefficients to register format
    # @param[in]    coeff
    # @return       outVal value in register format
    def convert_csc_coeff_to_regformat(coeff):
        outVal = 0
        sign = 0
        exponent = 0
        shift_factor = 0
        mantissa = 0

        if coeff < 0:
            sign = 1
        # range check
        if coeff > 3.99:
            coeff = 3.9921875  # 11.1111111b -> 511/128
        if coeff < -4.00:
            coeff = -3.9921875

        coeff = math.fabs(coeff)

        if (coeff < 0.125):  # 0.000bbbbbbbbb
            exponent = 3
            shift_factor = 12
        elif (coeff >= 0.125 and coeff < 0.25):  # 0.00bbbbbbbbb
            exponent = 2
            shift_factor = 11
        elif (coeff >= 0.25 and coeff < 0.5):  # 0.0bbbbbbbbb
            exponent = 1
            shift_factor = 10
        elif (coeff >= 0.5 and coeff < 1.0):  # 0.bbbbbbbbb
            exponent = 0
            shift_factor = 9
        elif (coeff >= 1.0 and coeff < 2.0):  # b.bbbbbbbb
            exponent = 7
            shift_factor = 8
        elif (coeff >= 2.0):
            exponent = 6
            shift_factor = 7

        mantissa = round(coeff * (1 << shift_factor))

        outVal = sign << 15
        outVal = outVal | (exponent << 12)
        outVal = outVal | (mantissa << 3)

        return outVal
