######################################################################################
# @file         mipi_timings.py
# @brief        It verifies if registers are programmed with timing values in accordance with VBT.
# @details      CommandLine: python mipi_timings.py -mipi_a
#               Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_timings
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains test to verify timing values in registers for MIPI
class MipiTimings(MipiBase):

    ##
    # @brief        This function verifies if registers are programmed with timing values in accordance with the VBT
    #               for every port
    # @return       None
    def runTest(self):
        for port in self.port_list:
            mipi_timings.verify_timings(self.mipi_helper, port)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
