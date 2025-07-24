########################################################################################################################
# @file         mipi_command_enable.py
# @brief        It verifies if required register bits are programmed to enable MIPI in command mode. Test is applicable
#               for command mode only.
# @details      CommandLine: python mipi_command_enable.py -mipi_a
#               Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @author       Sri Sumanth Geesala
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.mipi_base import *
from Tests.MIPI.Verifiers import mipi_command_mode


##
# @brief        This class contains test to verify MIPI enable in command mode
class MipiCommandEnable(MipiBase):

    ##
    # @brief        This function verifies if required register bits are programmed to enable MIPI in command mode.
    # @return       None
    def runTest(self):
        for port in self.port_list:
            ##
            # skip test for this port if MIPI is not in command mode in VBT (VBT is golden)
            panel_index = self.mipi_helper.get_panel_index_for_port(port)
            if self.mipi_helper.get_mode_of_operation(panel_index) != mipi_helper.COMMAND_MODE:
                logging.info('Port %s: This verification is applicable for command mode only. Current port is not '
                             'configured to command mode. Skipping for this port.' % (port))
                continue
            mipi_command_mode.verify_command_mode_enable_bits(self.mipi_helper, port)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
