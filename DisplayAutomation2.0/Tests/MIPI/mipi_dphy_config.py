########################################################################################################################
# @file         mipi_dphy_config.py
# @brief        It verifies if DPHY and DSI registers are programmed with the DPHY values in accordance with VBT.
# @details      CommandLine: python mipi_dphy_config.py -mipi_a
#               Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @author       Sri Sumanth Geesala
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_dphy_config
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains test to verify DPHY and DSI registers are programmed with the DPHY values in
#               accordance with VBT
class MipiDphyConfig(MipiBase):

    ##
    # @brief        This function verifies if DPHY and DSI registers are programmed with the DPHY values in
    #               accordance with VBT
    # @return       None
    def runTest(self):
        for port in self.port_list:
            mipi_dphy_config.verify_dphy_config(self.mipi_helper, port)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
