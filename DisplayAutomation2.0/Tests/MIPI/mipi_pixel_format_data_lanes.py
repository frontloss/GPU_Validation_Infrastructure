######################################################################################
# @file         mipi_pixel_format_data_lanes.py
# @brief        It verifies if pixel format and number of data lanes are programmed in accordance with VBT.
# @details      CommandLine: python mipi_pixel_format_data_lanes.py -mipi_a
#               Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_link_related
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains Mipitest to verify if pixel format and number of data lanes are programmed in
#               accordance with VBT.
class MipiPixelFormatDataLanes(MipiBase):

    ##
    # @brief        This function verifies if pixel format and number of data lanes are programmed in
    #               accordance with VBT for each DSI port
    # @return       None
    def runTest(self):
        ##
        # for each DSI port
        for port in self.port_list:
            mipi_link_related.verify_pixel_format_data_lanes(self.mipi_helper, port)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
