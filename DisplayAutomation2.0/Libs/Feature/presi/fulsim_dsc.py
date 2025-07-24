#######################################################################################################################
# @file         fulsim_dsc.py
# @brief        Python wrapper helper module which will parse fulsim generated vdsc dumps.
# @author       Chandrakanth pabolu
#######################################################################################################################
import logging
import os
import re
import sys
import time
from subprocess import call

from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature.display_engine.de_base import display_base

if '-pre_silicon' in sys.argv:
    import serial

VDSC_CMODEL_PATH = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VdscCModel")


##
# @brief        Get pps data
# @param[in]    display - PPS Register Display
# @return       None
def get_pps_data(display):
    _DSS_CTL1_DICT = {0: 0x6F350, 1: 0x0, 2: 0x61350, 3: 0x62350}  # DSS CTRL registers corresponds to pipes A, B and C
    pps_data = []
    display_base_obj = display_base.DisplayBase(display)
    transcoder_id = display_base_obj.get_transcoder_and_pipe(display)[0]
    reg_offset = _DSS_CTL1_DICT[transcoder_id]

    for count in range(1, 33):  # Reading 32 registers consequently which contains 128 bytes PPS header data
        reg_val = driver_interface.DriverInterface().mmio_read(reg_offset + count * 4, 'gfx_0')
        logging.debug("offset: {0}, value: {1}".format(hex(reg_offset + count * 4), hex(reg_val)))
        for i in range(4):
            result = (reg_val >> (8 * i)) & 0xFF
            pps_data.append(result)

    if len(pps_data) != 128:
        logging.error("Insufficient pps data")
    return pps_data


##
# @brief        Dump pps registers
# @param[in]    display - PPS Register Display
# @return       None
def dump_pps_registers(display):
    pps_registers = get_pps_data(display)
    out_file = open("pps_" + display + ".txt", 'a')

    for reg_val in pps_registers:
        out_file.write('{0:02x}'.format(int(reg_val)) + ' 0\n')
    out_file.write('{0:02x}'.format(int(0)) + ' 1\n')
    out_file.close()


##
# @brief        Get pps registers
# @param[in]    display - PPS Register Display
# @return       None
def get_pps_registers(display):
    counter = 0
    pps_data = []
    pps_registers = []
    with open("pps_" + display + ".txt", 'r') as f:
        for line in f:
            g = re.match('^([0-9a-fA-F]{2})\s(\d)$', line)
            if g is not None:
                if int(g.group(2)) == 1:
                    pps_data.append(pps_registers)
                    pps_registers = []
                    counter = counter + 1
                else:
                    pps_registers.append(int(g.group(1), 16))
    return pps_data


##
# @brief        Compress Data
# @param[in]    filename - file to be launched
# @return       None
def launch_dsc(filename):
    dsc_exe_path = os.path.join(VDSC_CMODEL_PATH, "DSC.exe")
    file_path = os.path.join(VDSC_CMODEL_PATH, filename)
    p = call([dsc_exe_path, "-F", file_path])


##
# @brief        Compress Data
# @param[in]    pps_data - PPS Data
# @param[in]    png_filename - PNG Image filename
# @param[in]    cfg_filename - Configuration File name
# @return       files
def compress_data(pps_data, png_filename, cfg_filename="test_comp.cfg"):
    ppm_filename = png_filename[:-4] + '.ppm'
    p = call(["magick.exe", png_filename, os.path.join(VDSC_CMODEL_PATH, ppm_filename)])
    out_dscfile = open(os.path.join(VDSC_CMODEL_PATH, 'test_list.txt'), 'w')
    out_dscfile.write(os.path.join(VDSC_CMODEL_PATH, ppm_filename))
    out_dscfile.close()

    slice_height = pps_data[10] << 8 | pps_data[11]
    slice_width = pps_data[12] << 8 | pps_data[13]
    bpp = ((pps_data[4] & 0x3) << 8 | pps_data[5]) // 16
    bpc = pps_data[3] >> 4

    out_file = open(os.path.join(VDSC_CMODEL_PATH, cfg_filename), 'w')
    out_file.write("SRC_LIST   " + os.path.join(VDSC_CMODEL_PATH, "test_list.txt\n"))
    out_file.write("FUNCTION  1\n")

    out_file.write("SLICE_WIDTH  " + str(slice_width) + "\n")
    out_file.write("SLICE_HEIGHT  " + str(slice_height) + "\n")

    out_file.write("LINE_BUFFER_BPC    9\n")
    out_file.write("ENABLE_422     0\n")
    out_file.write("USE_YUV_INPUT  0\n")
    out_file.write("BLOCK_PRED_ENABLE    1\n")
    out_file.write("VBR_ENABLE     0\n")
    out_file.write("SWAP_R_AND_B_OUT 0\n")
    out_file.write("DPX_PAD_LINE_ENDS  1\n")

    rc_file = "rc_" + str(bpc) + "bpc_" + str(bpp) + "bpp.cfg\n"
    rc_filepath = os.path.join(VDSC_CMODEL_PATH, rc_file)
    out_file.write("INCLUDE    " + rc_filepath)
    out_file.close()

    launch_dsc(cfg_filename)


##
# @brief        get_fulsim_images
# @param[in]    image_pattern - Image Pattern
# @return       files
def get_fulsim_images(image_pattern):
    files = [f for f in os.listdir('.') if os.path.isfile(f) and image_pattern in f]
    return files


##
# @brief        Helper function which generates compressed data for each frame from D-Mux output with C-Model.
# @param[in]    display type for which vdsc dumps to be retrieved from C-Model.
# @return       dsc_filenames - List of filenames contains compressed data for each frame.
def get_dsc_from_cmodel(display):
    dsc_filenames = []
    display_base_obj = display_base.DisplayBase(display)
    pipe_id = display_base_obj.get_transcoder_and_pipe(display)[1]

    pipe = 'A' if pipe_id == 0 else 'B' if pipe_id == 1 else 'C'

    files = get_fulsim_images('Dmux{0}'.format(pipe))

    pps_data = get_pps_registers(display)

    for each_item in range(len(pps_data)):
        filename = files[each_item]
        if os.path.exists(filename):
            compress_data(pps_data[each_item], filename)
            dsc_filenames.append(filename[:-4] + '.dsc')
        else:
            logging.error("{0} doesn't exists.".format(filename))

    return dsc_filenames


##
# @brief        Helper function which parses vdsc fulsim file and generate compressed data for each frame.
# @param[in]    display type for which vdsc dumps to be retrieved from fulsim raw dumps.
# @param[in]    dsc_file name without the extention type.
# @return       List of filenames contains compressed data for each frame.
def get_dsc_from_fulsim(display, dsc_file="fulsim"):
    frame_count = 0
    dsc_filenames = []
    header = [0x44, 0x53, 0x43, 0x46]  # DSC default header
    pps_data = get_pps_registers(display)

    if display == 'DP_A':
        compressed_raw_file = 'edp_dss_0_dpt.txt'
    elif display[:2] == "DP":
        display_base_obj = display_base.DisplayBase(display)
        pipe_id = display_base_obj.get_transcoder_and_pipe(display)[1]
        compressed_raw_file = 'tcb_dss_dpt.txt' if pipe_id == 1 else 'tcc_dss_dpt.txt'
    else:
        compressed_raw_file = None

    filename = dsc_file + display[-1:] + str(frame_count) + ".dsc"
    logging.debug(filename)
    out_file = open(filename, 'wb')
    out_file.write(bytearray(header))
    out_file.write(bytearray(pps_data[frame_count]))

    reached_end = False
    with open(compressed_raw_file, 'r') as f:
        for line in f:
            g = re.match('^\s+\d{8}\s([0-9a-fA-F]{9})\s(\d)\s\d+\s\d{2}$', line)
            if g is not None:
                reached_end = False
                data = g.group(1)
                pixel_data = [int(data[0:2], 16), int(data[3:5], 16), int(data[6:8], 16)]
                out_file.write(bytearray(pixel_data))
                if int(g.group(2)) == 1:
                    reached_end = True
                    frame_count = frame_count + 1
                    out_file.close()
                    dsc_filenames.append(filename)
                    logging.debug(str(frame_count) + "th frame extracted.")
                    if len(pps_data) == frame_count:
                        break
                    else:
                        filename = dsc_file + display[-1:] + str(frame_count) + ".dsc"
                        out_file = open(filename, 'wb')
                        out_file.write(bytearray(header))
                        out_file.write(bytearray(pps_data[frame_count]))

    out_file.close()

    if not reached_end:
        os.remove(filename)

    return dsc_filenames


##
# @brief        Helper function to retrieve vdsc dumps from host os to guest os.
# @param[in]    None
# @return       None
def get_vdsc_dumps_from_host_os():
    with serial.Serial() as ser:
        ser.port = 'COM1'
        ser.open()
        ser.write('start_copy_vdsc')
    logging.info("Copying VDSC dumps from Host machine to Guest OS.")

    while not os.path.exists("dump_copy_done.txt"):
        logging.debug("Waiting for copy of the file")
        time.sleep(5)


if __name__ == "__main__":
    print(get_dsc_from_fulsim("dp_a"))
    print(get_dsc_from_cmodel("dp_a"))
