######################################################################################
# @file         mipi_video_enable.py
# @brief        It verifies if required register bits are programmed to enable MIPI in video mode. Test is applicable
#               for video mode only.
# @details      CommandLine: python mipi_video_enable.py -mipi_a
#
# Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @author   Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_video_mode
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains test to verify Mipi in video mode
class MipiVideoEnable(MipiBase):

    ##
    # @brief        This function verifies Mipi in video mode
    # @return       None
    def runTest(self):
        for port in self.port_list:
            ##
            # skip test for this port if MIPI is not in video mode in VBT (VBT is golden)
            panel_index = self.mipi_helper.get_panel_index_for_port(port)
            if (self.mipi_helper.get_mode_of_operation(panel_index) != mipi_helper.VIDEO_MODE):
                logging.info('Port %s: This verification is applicable for video mode only. '
                             'Current port is not configured to video mode. Skipping for this port.' % (port))
                continue
            mipi_video_mode.verify_video_mode_enable_bits(self.mipi_helper, port)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
