###############################################################################
# Script Name         : read_register
# Script Owner        : Vinod D S 
# Description         : Helper functions to read display registers
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


def read_register_value(reg_offset):
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


def read_register_value_poll(reg_offset, interval_time):
    driver_interface_ = driver_interface.DriverInterface()
    try:
        while True:
            reg_val = driver_interface_.mmio_read(reg_offset, 'gfx_0')
            print("Value of %s = 0x%s (%s)" % (hex(reg_offset), format(reg_val, '08x').upper(), reg_val))
            sleep(1.0 * interval_time / 1000.0)
    except KeyboardInterrupt:
        print("*** Ctrl+C is pressed to terminate ***")


if __name__ == '__main__':
    test_environment.TestEnvironment.load_dll_module()
    system('cls')
    if len(sys.argv) >= 2:
        dll_logger.initialize(True)
        offset, delay = 0, 0
        try:
            offset = int(sys.argv[1], 16)
        except ValueError:
            print("Invalid offset value")

        if len(sys.argv) == 2:
            read_register_value(offset)
        else:
            try:
                delay = int(sys.argv[2])
            except ValueError:
                print("Invalid delay value")
            read_register_value_poll(offset, delay)
        dll_logger.cleanup()
    else:
        print("Invalid arguments, refer below 2 ways to use this functionality.")
        print("1. For single read: read_register.py <offset_value> --> read_register.py 0x70180")
        print(
            "2. For polling: read_register.py <offset_value> <delay_in_milliseconds> --> read_register.py 0x70040 100")
