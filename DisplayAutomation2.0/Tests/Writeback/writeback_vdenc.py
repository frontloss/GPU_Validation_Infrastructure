########################################################################################################################
# @file         writeback_vdenc.py
# @brief        The test scenario tests the following functionalities.
#               * Verify whether the devices are correctly plugged and enumerated.
#               * Verify display-vdenc interface improvement, caching and frame number programming.
# @author       Patel, Ankurkumar G
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Writeback.writeback_base import *

##
# @brief    Contains unittest runTest function
#           to verify writeback device plug/unplug and display-vdenc interface improvement.
class WritebackVdenc(WritebackBase):

    ##
    # @brief        unittest runTest function
    ##
    # @brief        unittest runTest function
    # @return       None
    def test_run(self):

        # Plug and verify writeback devices
        logging.info("Step1 - Plug and verify writeback devices")
        self.assertEquals(self.plug_and_verify_wb_devices(), True,
                          "Aborting the test as plug & Verify failed for writeback devices")
        logging.info("\tPASS: Writeback devices are plugged and enumerated successfully")

        # for debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)

        # Verify diaplay-vdenc control pointers
        logging.info("Step2 - Verify diaplay-vdenc interface improvement")
        self.assertEquals(self.wb_verifier.verify_display_vdenc_improvement(self.wb_device_list), True,
                          "Aborting the test as Verify failed for display-vdenc interface improvement")
        logging.info("\tPASS: Display-Vdenc interface improvement verified successfully")

        # Verify caching
        logging.info("Step3 - Verify Caching")
        self.assertEquals(self.wb_verifier.verify_caching(self.wb_device_list), True,
                          "Aborting the test as Verify failed for writeback Caching")
        logging.info("\tPASS: Write caching verified")

        # Verify Frame number programming
        logging.info("Step4 - Verify frame number programming")
        self.assertEquals(self.wb_verifier.verify_frame_number_programming(self.wb_device_list), True,
                          "Aborting the test as Verify failed for writeback frame number programming")
        logging.info("\tPASS: Frame number programming verified")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('WritebackVdenc'))
    TestEnvironment.cleanup(outcome)
