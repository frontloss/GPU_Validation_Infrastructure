########################################################################################################################
# @file         blc_high_precision_levels.py
# @brief        Test for granularity in high precision brightness levels
#
# @author       Vinod D S
########################################################################################################################
import time

from Libs.Core.test_env import test_environment
from Libs.Feature.blc import brightness

from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains BLC tests with high precision brightness levels
class BlcHighPrecisionLevels(BlcBase):

    ##
    # @brief        This test verifies Blc with high precision levels
    # @return       None
    def test_blc_high_precision_levels(self):
        self.setup_and_validate_blc()
        if self.is_high_precision is False:
            self.fail("High Precision Brightness is NOT enabled via Test (Test Issue)")

        brightness.load_library()

        no_error = 0
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is True:
                    logging.info("Step: Applying milli-percent on {0}_{1}".format(panel.port_type, panel.port))
                    for milli_percent in range(10000, 10300):
                        # Applying milli percentage values
                        logging.info("Applying milli-percent= {0}".format(milli_percent))

                        if blc.set_brightness3(panel.gfx_index, panel.target_id, milli_percent, 200) is False:
                            logging.error("\tFAILED to apply milli-percent= {0}".format(milli_percent))
                            no_error += 1
                        else:
                            logging.info("\tSuccessfully applied milli-percent= {0}".format(milli_percent))
                            # Check the PWM register
                        time.sleep(4)

        if no_error != 0:
            self.fail("FAILED to set high precision brightness")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcHighPrecisionLevels'))
    test_environment.TestEnvironment.cleanup(outcome)
