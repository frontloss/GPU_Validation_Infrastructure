######################################################################################
# \file         hw_3d_lut_verification.py
# \section      hw_3d_lut_verification
# \remarks      This script contains all helper functions which help in verification of HW3DLUT
# \ref          hw_3d_lut_verification.py \n
# \author       Smitha B
######################################################################################
import logging
import time

from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from registers.mmioregister import MMIORegister

machine_info = SystemInfo()
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break


class Hw3DLutVerification(object):

    def get_value(self, value, start, end):
        ret_value = (value << (31 - end)) & 0xFFFFFFFF
        ret_value = (ret_value >> (31 - end + start)) & 0xFFFFFFFF
        return ret_value

    def verify_3dlut(self, current_pipe, input_file):
        driver_interface_ = driver_interface.DriverInterface()
        hw_3d_lut_status = "DISABLED"
        hw_lut_buffer_status = "NOT_LOADED"
        lut_3d_ctl_reg = 'LUT_3D_CTL' + '_' + current_pipe
        instance = MMIORegister.get_instance('LUT_3D_CTL_REGISTER', lut_3d_ctl_reg, platform)
        lut_3d_ctl_reg_offset = instance.offset

        ##
        # LUT INDEX REGISTER
        lut_index_reg = 'LUT_3D_INDEX' + '_' + current_pipe
        instance = MMIORegister.get_instance('LUT_3D_INDEX_REGISTER', lut_index_reg, platform)
        lut_index_reg_offset = instance.offset

        ##
        # LUT DATA REGISTER
        lut_data_reg = 'LUT_3D_DATA' + '_' + current_pipe
        instance = MMIORegister.get_instance('LUT_3D_DATA_REGISTER', lut_data_reg, platform)
        lut_data_reg_offset = instance.offset

        driver_interface_.mmio_write(lut_index_reg_offset, 0x00002000, 'gfx_0')
        lut_3d_enable = (driver_interface_.mmio_read(lut_3d_ctl_reg_offset, 'gfx_0') >> 31)
        if (lut_3d_enable == 1):
            logging.info("Hw 3D LUT is enabled on pipe %c", current_pipe)
            hw_3d_lut_status = "Enabled"
            new_lut_ready = (driver_interface_.mmio_read(lut_3d_ctl_reg_offset, 'gfx_0') >> 30) & 1
            time.sleep(30)
            if new_lut_ready == 0:

                logging.info("Hardware finished loading the lut buffer into internal working RAM")
                hw_lut_buffer_status = "Finished"
            else:
                logging.error("Hardware did not load the lut buffer into internal working RAM")
                hw_lut_buffer_status = "NOT_LOADED"
                return hw_3d_lut_status, hw_lut_buffer_status
            prog_lut = []
            for i in range(0, 4913):
                reg_data_offset = driver_interface_.mmio_read(lut_index_reg_offset, 'gfx_0') & 0xFFF
                reg_val_lut_3d_data = driver_interface_.mmio_read(lut_data_reg_offset, 'gfx_0')
                reg_blue = self.get_value(reg_val_lut_3d_data, 0, 9)
                reg_green = self.get_value(reg_val_lut_3d_data, 10, 19)
                reg_red = self.get_value(reg_val_lut_3d_data, 20, 29)
                prog_lut.append(reg_red)
                prog_lut.append(reg_green)
                prog_lut.append(reg_blue)
            self.verify_lut_data(prog_lut, input_file)
        else:
            logging.error("Hw 3D LUT is disabled on pipe %s", current_pipe)
            hw_3d_lut_status = "DISABLED"
        driver_interface_.mmio_write(lut_index_reg_offset, 0x00000000, 'gfx_0')
        return hw_3d_lut_status, hw_lut_buffer_status

    def verify_lut_data(self, prog_lut, input):
        logging.info("Input file is %s" % input)
        red_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                    0x300, 0x340, 0x380, 0x3C0, 0x3FC]
        green_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                      0x300, 0x340, 0x380, 0x3C0, 0x3FC]
        blue_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                     0x300, 0x340, 0x380, 0x3C0, 0x3FC]
        ref_lut = []
        count = 0
        if (input == "CustomLUT_no_R.bin"):
            for i in range(0, 17):
                red_data[i] = 0
        elif (input == "CustomLUT_no_G.bin"):
            for i in range(0, 17):
                green_data[i] = 0
        elif (input == "CustomLUT_no_B.bin"):
            for i in range(0, 17):
                blue_data[i] = 0
        for i in range(0, 17):
            for j in range(0, 17):
                for k in range(0, 17):
                    ref_lut.append(red_data[i])
                    ref_lut.append(green_data[j])
                    ref_lut.append(blue_data[k])
                    count = count + 3
        index = 0
        for reg_val, ref_val in zip(prog_lut, ref_lut):
            if (reg_val != ref_val):
                logging.error("LUT values not matching Index : %d ProgrammedVal : %d Expected val : %d ", index,
                              reg_val,
                              ref_val)
                return False
            index += 1
