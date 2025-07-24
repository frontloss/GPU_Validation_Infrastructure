###############################################################################
# Script Name         : write_mmio
# Script Owner        : Veluru, Veena
# Description         : Helper functions to write to display mmios
###############################################################################

import sys
from os import system
from time import sleep

from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_environment
from Libs.Core.wrapper import dll_logger

_BIT_OFFSET_NAME = ['B31', 'B30', 'B29', 'B28', 'B27', 'B26', 'B25', 'B24',
                    'B23', 'B22', 'B21', 'B20', 'B19', 'B18', 'B17', 'B16',
                    'B15', 'B14', 'B13', 'B12', 'B11', 'B10', 'B09', 'B08',
                    'B07', 'B06', 'B05', 'B04', 'B03', 'B02', 'B01', 'B00']

reg_value = 0


def write_register_value(reg_offset, reg_value):
    driver_interface_ = driver_interface.DriverInterface()
    try:
        status = driver_interface_.mmio_write(reg_offset, reg_value, 'gfx_0')
        if status:
            print("\n Register Write Successful")
        read_register_value(reg_offset)
    except Exception as ex:
        print("Exception: {}".format(ex))


def read_register_value(reg_offset):
    global reg_value
    driver_interface_ = driver_interface.DriverInterface()
    try:
        reg_value = driver_interface_.mmio_read(reg_offset, 'gfx_0')
        output = [i for i in format(reg_value, '032b')]
        print("\nRegister Value of Offset {0} = 0x{1} ({2})".format(
            hex(reg_offset), format(reg_value, '08x').upper(), reg_value))
        print(" : ".join(map(lambda x: '{}'.format(x), _BIT_OFFSET_NAME)))
        print("  :  ".join(map(lambda x: '{}'.format(x), output)))
    except Exception as ex:
        print("Exception: {}".format(ex))


if __name__ == '__main__':
    test_environment.TestEnvironment.load_dll_module()
    system('cls')
    if len(sys.argv) >= 3:
        dll_logger.initialize(True)
        offset, value = 0, 0
        try:
            offset = int(sys.argv[1], 16)
            value = int(sys.argv[2], 16)
        except ValueError:
            print("Invalid offset or register values")
        if "-force" in sys.argv:
            write_register_value(offset, value)
        else:
            read_register_value(offset)
            if read_reg_value == value:
                print("MMIO value is same as current requested value, skipping reg write")
            else:
                write_register_value(offset, value)
    else:
        print("Invalid arguments, refer below to use this functionality.")
        print("1. For Force write: write_mmio.py <offset_value> <value>--> write_mmio.py -DP_F 0x70180 0x9000 -force\n"
              "2. To skip reg write if input value is same: write_mmio.py <offset_value> <value>--> write_mmio.py -DP_F 0x70180 0x9000")
