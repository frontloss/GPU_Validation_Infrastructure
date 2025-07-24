###############################################################################
# @file               : display_mmio_access.py
# @brief              : Helper functions to read display registers
# @details            : display_mmio.py -action read -offset 0x1234
#                     : display_mmio.py -action read_poll -offset 0x1234 -value 10
#                     : display_mmio.py -action write -offset 0x1234 -value 0xabcd
# @author             : Bn, Praveen Kumar
###############################################################################

import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_environment import TestEnvironment


##
# @brief        DisplauMMIO
class DisplayMMIO(unittest.TestCase):
    custom_tags = ['-action', '-offset', '-value']

    ##
    # @brief        TestRun
    # @return       None
    def runTest(self):
        cmd_line_params = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        if type(cmd_line_params['ACTION']) is list and cmd_line_params['ACTION']:
            if cmd_line_params['ACTION'][0] == 'READ' and cmd_line_params['OFFSET']:
                self.read_mmio(cmd_line_params['OFFSET'][0])
            elif cmd_line_params['ACTION'][0] == 'WRITE' and cmd_line_params['OFFSET'] and cmd_line_params['VALUE']:
                self.write_mmio(cmd_line_params['OFFSET'][0], cmd_line_params['VALUE'][0])
            elif cmd_line_params['ACTION'][0] == 'READ_POLL' and cmd_line_params['OFFSET'] and cmd_line_params['VALUE']:
                self.read_mmio_polling(cmd_line_params['OFFSET'][0], cmd_line_params['VALUE'][0])
            else:
                self.fail("Wrong input to the script. Please read usage details provided in header")

    # Offset and data value in Hex
    ##
    # @brief        TestRun
    # @param[in]    offset - Offset Value
    # @return       None
    def read_mmio(self, offset):
        value = driver_interface.DriverInterface().mmio_read(int(offset, 16), 'gfx_0')
        if value is not None:
            logging.info("MMIO Read Offset [{0}] -> [{1}({2})]".format(offset, hex(value), value))
        else:
            self.fail("MMIO read failed")

    # offset and time_interval_ms in milli second, reads offset every specified ms through 100 iterations
    ##
    # @brief        TestRun
    # @param[in]    offset - Offset Value
    # @param[in]    time_interval_ms - Time Interval in ms
    # @return       None
    def read_mmio_polling(self, offset, time_interval_ms):
        iteration = 100
        while iteration:
            self.read_mmio(offset)
            time.sleep(int(time_interval_ms) / 1000.0)
            iteration -= 1

    ##
    # @brief        Write MMIO
    # @param[in]    offset - Offset Value
    # @param[in]    data - Write mmio data
    # @return       None
    def write_mmio(self, offset, data):
        status = driver_interface.DriverInterface().mmio_write(int(offset, 16), int(data, 16), 'gfx_0')
        if status:
            logging.info(
                "MMIO write Offset [{0}] -> [{1}({2})] -> status [{3}]".format(offset, data, int(data, 16), status))
        else:
            self.fail("MMIO write failed")

    ##
    # @brief        Tear Down
    # @return       None
    def tearDown(self):
        logging.info("ULT Complete")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
