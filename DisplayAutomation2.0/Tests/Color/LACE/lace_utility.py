###################################################################################################
# \file         lace_base.py
# \section      lace_base
# \remarks      This script contains helper functions that will be used by
#               LACE test scripts
# \ref          lace_utility.py \n
# \author       Smitha B
###################################################################################################
import ctypes
import logging
import os

from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core import registry_access, display_essential
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.mmioregister import MMIORegister
from Libs.Core import enum

TILE_SIZE = 256.0
HIST_BIN_SIZE = 32
NUM_OF_IE_ENTRIES = 33
MAX_TILE_SIZE = 20  # Generic for both portrait(9X16)/landscape(16X9) until Gen12. In Gen12 5k LACE
# is supported hence max tiles is 20X13
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


def convert_png_to_bin(input_file, width, height, pixel_format, display_index):
    input_file = os.path.join(test_context.SHARED_BINARY_FOLDER, input_file)
    str1 = '_' + str(display_index) + '.bin'
    input_file = input_file.lower()
    output_file = input_file.replace('.png', str1)
    output_file = input_file.replace('.bmp', str1)
    if os.path.exists(output_file):
        os.remove(output_file)
    executable = 'ImageFormater.exe'
    commandline = executable + ' -i ' + input_file + ' -w ' + str(width) + ' -h ' + str(height) + ' -f ' + str(
        pixel_format) + ' -o ' + output_file
    logging.info("ImageFormatter commandline : %s", commandline)
    currentdir = os.getcwd()
    os.chdir(os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'HDR'))
    # logging.info("Current path : %s",  os.getcwd())
    os.system(commandline)
    os.chdir(currentdir)

    return output_file


def get_current_pipe(display):
    display_base_obj = DisplayBase(display)
    current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display)
    current_pipe_notation = chr(int(current_pipe) + 65)
    logging.info("Current pipe : Pipe %s ", current_pipe_notation)
    return current_pipe_notation


##
# @brief            Reads the histogram generated from SW module and stores it into structure
# @param[in]        File name
# @return           None

def read_histogram_from_file(file_name):
    path = os.path.join(test_context.LOG_FOLDER, file_name)
    with open(path, 'r') as file_obj:
        # file_obj.readline() # If ================Histogram File +++++++++++++++ is there
        start_string = file_obj.readline()  # Read Bin Data :

        ##        if (start_string != START_OF_HISTOGRAM_DATA):
        ##            logging.error("Histogram File CORRUPTED!!")
        ##            return False
        line = file_obj.readline()  # Read line Bin x = ?,y = ?:

        while True:
            str_split = line.split()  # Bin x = ?,y = ?:
            row = int(str_split[3].split(",")[0])
            col = int(str_split[6].split(":")[0])

            file_obj.readline()  # BlankLine
            for b in range(0, HIST_BIN_SIZE):
                val = file_obj.readline()
                LaceParams.HistogramDataSW[row][col].Bins[b] = int(val, 16)

            file_obj.readline()  # BlankLine
            line = file_obj.readline()
            if line == "":
                break
    return LaceParams


##
# @brief            Writes the histogram generated by HW to a file
# @param[in]        File name
# @param[in]        Tiles per row
# @param[in]        Tiles per column
# @return           None

def write_histogram_to_file(file_name, LaceParams, tiles_per_row, tiles_per_col):
    path = os.path.join(test_context.LOG_FOLDER, file_name)
    with open(path, 'w') as file_obj:
        file_obj.write(START_OF_HISTOGRAM_DATA + "\n")
        for i in range(0, tiles_per_col):
            for j in range(0, tiles_per_row):
                str1 = "Bin x = " + str(i) + ", y = " + str(j) + ":"  # Construct line Bin x = ?,y = ?:
                file_obj.write(str1 + "\n")
                file_obj.write("\n")  # Blank line

                for b in range(0, HIST_BIN_SIZE):
                    val = hex(LaceParams.HistogramDataHW[i][j].Bins[b]).rstrip("L").lstrip("0x")
                    val = format(LaceParams.HistogramDataHW[i][j].Bins[b], '05x')
                    file_obj.write(val + "\n")
                file_obj.write("\n")  # Blank line


def compare_histograms(ref_file_name, prog_lace_params, tiles_per_row, tiles_per_col):
    status = True
    ref_lace_params = read_histogram_from_file(ref_file_name)
    for row in range(0, tiles_per_col):
        for col in range(0, tiles_per_row):
            for b in range(0, HIST_BIN_SIZE):
                if (ref_lace_params.HistogramDataSW[row][col].Bins[b] !=
                        prog_lace_params.HistogramDataSW[row][col].Bins[b]):
                    logging.error(
                        "Histogram mistmatch at Tile Row : %d  Col : %d Bin %d --> Expected : %d  Actual : %d ", row,
                        col, b,
                        ref_lace_params.HistogramDataSW[row][col].Bins[b],
                        prog_lace_params.HistogramDataSW[row][col].Bins[b])
                    return status

    return status


##
# @brief            Reads the histogram from HW registers
# @param[in]        Current pipe
# @param[in]        Tiles per row
# @param[in]        Tiles per column
# @return           None

def read_histogram_from_registers(current_pipe, tiles_per_row, tiles_per_col):
    driver_interface_ = driver_interface.DriverInterface()
    current_pipe_notation = chr(int(current_pipe) + 65)
    dplc_histogram_index_regname = "DPLC_HIST_INDEX_" + current_pipe_notation
    dplc_histogram_data_regname = "DPLC_HIST_DATA_" + current_pipe_notation

    index_instance = reg_read.get_instance("DPLC_HIST_INDEX_REGISTER", dplc_histogram_index_regname, platform)
    index_offset = index_instance.offset
    driver_interface_.mmio_write(index_offset, 0x0, 'gfx_0')

    for row in range(0, tiles_per_col):
        for col in range(0, tiles_per_row):
            dplc_hist_index_reg = reg_read.read("DPLC_HIST_INDEX_REGISTER", dplc_histogram_index_regname, platform)
            logging.debug("dplc_hist_index_reg.x_index %d, dplc_hist_index_reg.y_index %d" % (
                dplc_hist_index_reg.x_index, dplc_hist_index_reg.y_index))
            dplc_hist_index_reg.x_index = col
            dplc_hist_index_reg.y_index = row
            for bin in range(0, HIST_BIN_SIZE):
                dplc_hist_index_reg.dw_index = bin
                driver_interface_.mmio_write(index_offset, dplc_hist_index_reg.asUint, 'gfx_0')
                dplc_hist_data_reg = reg_read.read("DPLC_HIST_DATA_REGISTER", dplc_histogram_data_regname,
                                                   platform)
                LaceParams.HistogramDataHW[row][col].Bins[bin] = dplc_hist_data_reg.bin

    return LaceParams


##
# @brief            Reads the IET from HW registers
# @param[in]        Current pipe
# @param[in]        Tiles per row
# @param[in]        Tiles per column
# @return           None

def read_iet_from_registers(current_pipe, tiles_per_row, tiles_per_col):
    result = True
    driver_interface_ = driver_interface.DriverInterface()
    current_pipe_notation = chr(int(current_pipe) + 65)
    dplc_iet_index_regname = "DPLC_IE_INDEX_" + current_pipe_notation
    dplc_iet_data_regname = "DPLC_IE_DATA_" + current_pipe_notation

    index_instance = reg_read.get_instance("DPLC_IE_INDEX_REGISTER", dplc_iet_index_regname, platform)
    index_offset = index_instance.offset
    driver_interface_.mmio_write(index_offset, 0x0, 'gfx_0')

    for row in range(0, tiles_per_col):
        for col in range(0, tiles_per_row):
            dplc_iet_index_reg = reg_read.read("DPLC_IE_INDEX_REGISTER", dplc_iet_index_regname, platform)
            dplc_iet_index_reg.x_index = col
            dplc_iet_index_reg.y_index = row
            index = 0
            for n in range(0, NUM_OF_IE_ENTRIES, 2):
                dplc_iet_index_reg.dw_index = index
                index = index + 1
                driver_interface_.mmio_write(index_offset, dplc_iet_index_reg.asUint, 'gfx_0')
                dplc_iet_index_reg = reg_read.read("DPLC_IE_INDEX_REGISTER", dplc_iet_index_regname, platform)
                dplc_iet_data_reg = reg_read.read("DPLC_IE_DATA_REGISTER", dplc_iet_data_regname,
                                                  platform)
                # print dplc_iet_data_reg.odd_point , dplc_iet_data_reg.even_point
                LaceParams.IEDataHW[row][col].Entries[n] = dplc_iet_data_reg.even_point
                if (n != 32):
                    LaceParams.IEDataHW[row][col].Entries[n + 1] = dplc_iet_data_reg.odd_point
    return LaceParams


def read_iet_from_registers_for_single_tile(current_pipe, tilex, tiley):
    IET_Data = []
    driver_interface_ = driver_interface.DriverInterface()
    current_pipe_notation = chr(int(current_pipe) + 65)
    dplc_iet_index_regname = "DPLC_IE_INDEX_" + current_pipe_notation
    dplc_iet_data_regname = "DPLC_IE_DATA_" + current_pipe_notation

    index_instance = reg_read.get_instance("DPLC_IE_INDEX_REGISTER", dplc_iet_index_regname, platform)
    index_offset = index_instance.offset
    driver_interface_.mmio_write(index_offset, 0x0, 'gfx_0')

    dplc_iet_index_reg = reg_read.read("DPLC_IE_INDEX_REGISTER", dplc_iet_index_regname, platform)

    dplc_iet_index_reg.x_index = tilex
    dplc_iet_index_reg.y_index = tiley
    index = 0
    for n in range(0, NUM_OF_IE_ENTRIES, 2):
        dplc_iet_index_reg.dw_index = index
        index = index + 1
        driver_interface_.mmio_write(index_offset, dplc_iet_index_reg.asUint, 'gfx_0')
        dplc_iet_data_reg = reg_read.read("DPLC_IE_DATA_REGISTER", dplc_iet_data_regname,
                                          platform)
        IET_Data.append(dplc_iet_data_reg.even_point)
        if (n != 32):
            IET_Data.append(dplc_iet_data_reg.odd_point)

    return IET_Data


##
# @brief            Reads the IET from HW registers for a particular tile
# @param[in]        Current pipe
# @param[in]        Tile row index
# @param[in]        Tile column index
# @return           None

def read_tile_iet_from_registers(current_pipe, tile_row_index, tile_col_index):
    result = True
    driver_interface_ = driver_interface.DriverInterface()
    current_pipe_notation = chr(int(current_pipe) + 65)
    dplc_iet_index_regname = "DPLC_IE_INDEX_" + current_pipe_notation
    dplc_iet_data_regname = "DPLC_IE_DATA_" + current_pipe_notation

    index_instance = reg_read.get_instance("DPLC_IE_INDEX_REGISTER", dplc_iet_index_regname, platform)
    index_offset = index_instance.offset
    driver_interface_.mmio_write(index_offset, 0x0, 'gfx_0')

    dplc_iet_index_reg = reg_read.read("DPLC_IE_INDEX_REGISTER", dplc_iet_index_regname, platform)

    dplc_iet_index_reg.x_index = tile_col_index
    dplc_iet_index_reg.y_index = tile_row_index
    index = 0
    for n in range(0, NUM_OF_IE_ENTRIES, 2):
        dplc_iet_index_reg.dw_index = index
        index = index + 1
        driver_interface_.mmio_write(index_offset, dplc_iet_index_reg.asUint, 'gfx_0')
        dplc_iet_data_reg = reg_read.read("DPLC_IE_DATA_REGISTER", dplc_iet_data_regname,
                                          platform)
        LaceParams.IEDataHW[tile_row_index][tile_col_index].Entries[n] = dplc_iet_data_reg.even_point
        if (n != 32):
            LaceParams.IEDataHW[tile_row_index][tile_col_index].Entries[n + 1] = dplc_iet_data_reg.odd_point


def perform_registry_customization(lux_customization_list):
    reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
    if not registry_access.write(args=reg_args, reg_name=lux_customization_list[0],
                                 reg_type=registry_access.RegDataType.DWORD, reg_value=lux_customization_list[1]):
        return False
    else:
        status, reboot_required = display_essential.restart_gfx_driver()
        return True