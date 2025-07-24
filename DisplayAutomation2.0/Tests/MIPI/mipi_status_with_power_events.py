######################################################################################
# @file         mipi_status_with_power_events.py
# @brief        It verifies MIPI transcoder and powerwell status with power events
# @details      CommandLine: python mipi_status_with_power_events.py -mipi_a -mipi_c
#               Test will pass only if MIPI status is as expected in various power events, otherwise it fails.
# @author       Kruti Vadhavaniya
######################################################################################
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_status
from Tests.MIPI.mipi_base import *

##
# @brief        This class contains test to verify MIPI status with different power events
class MipiStatusWithPowerEvents(MipiBase):

    ##
    # @brief        This verifies MIPI status after the invocation of different power events before reboot
    # @return       None
    def test_mipi_status_with_power_events(self):
        verify = True

        # Perform CS/S3 power event and check MIPI status
        if self.disp_power.is_power_state_supported(display_power.PowerEvent.CS):
            logging.info("Performing CS power event and Checking MIPI status")
            power_state = self.disp_power.invoke_power_event(display_power.PowerEvent.CS, 60)
            if power_state is True:
                verify &= mipi_status.check_mipi_status_bits(self.mipi_helper, self.port_list)
        else:
            logging.info("Performing S3 power event and Checking MIPI status")
            power_state = self.disp_power.invoke_power_event(display_power.PowerEvent.S3, 60)
            if power_state is True:
                verify &= mipi_status.check_mipi_status_bits(self.mipi_helper, self.port_list)

        logging.info("Performing S4 power event and Checking MIPI status")
        power_state = self.disp_power.invoke_power_event(display_power.PowerEvent.S4, 60)

        if power_state is True:
            verify &= mipi_status.check_mipi_status_bits(self.mipi_helper, self.port_list)

        if verify is not True:
            self.fail("Before S5 power event some checks from MIPI status are programmed wrong!")

        logging.info("Performing S5 power event and Checking MIPI status")
        if reboot_helper.reboot(self, 'test_mipi_status_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This verifies MIPI status after reboot
    # @return       None
    def test_mipi_status_after_reboot(self):
        verify = True
        logging.info("After Reboot")
        self.mipi_helper = mipi_helper.MipiHelper(self.platform)
        verify &= mipi_status.check_mipi_status_bits(self.mipi_helper, self.port_list)

        if verify is not True:
            self.fail("After S5 power event some checks from MIPI status are programmed wrong!")

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('MipiStatusWithPowerEvents'))
    TestEnvironment.cleanup(results)
