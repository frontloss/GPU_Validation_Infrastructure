########################################################################################################################
# @file         mipi_dual_link_config.py
# @brief        It verifies if required register bits are programmed for MIPI to run in dual link mode.
# @details      CommandLine: python mipi_dual_link_config.py -mipi_a
#               Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @author       Sri Sumanth Geesala
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_dual_link
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains test to verify if required register bits are programmed for MIPI to run in
#               dual link mode.
class MipiDualLinkConfig(MipiBase):

    ##
    # @brief        This function verifies if if required register bits are programmed for MIPI to run in
    #               dual link mode.
    # @return       None
    def runTest(self):
        ##
        # abort test if MIPI is not in dual link config in VBT (VBT is golden)
        if self.mipi_helper.dual_link != 1:
            self.fail('This test is applicable only for MIPI dual link. Aborting test.')

        mipi_dual_link.verify_dual_link_config(self.mipi_helper)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
