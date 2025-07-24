########################################################################################################################
# @file         writeback_power_events_persistance.py
# @brief        The test scenario tests the following functionalities.
#               * Verify whether the devices are correctly plugged and enumerated.
#               * Verify whether system can go to S3 and resume or not.
#               * Verify writeback devices are present after resuming from S3.
#               * Verify writeback devices are present after resuming from S4.
# @author       Patel, Ankurkumar G
########################################################################################################################
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Writeback.writeback_base import *

##
# @brief    Contains unitest runTest function to verify writeback device plug/unplug and persistance with powerevents(s3/s4)
class WritebackPowerEvents(WritebackBase):

    ##
    # @brief        unittest runTest function
    # @param[in]    self; Object of writeback base class
    # @return       void
    def test_run(self):

        # Plug and verify writeback devices
        logging.info("Step1 - Plug and verify writeback devices")
        self.assertEquals(self.plug_and_verify_wb_devices(), True,
                          "Aborting the test as plug & Verify failed for writeback devices")
        logging.info("\tPASS: Writeback devices are plugged and enumerated successfully")

        # Debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)

        # Go to S3 and resume, Go to CS and resume if S3 is not supported
        if self.disp_power.is_power_state_supported(display_power.PowerEvent.S3):
            self.assertEquals(self.disp_power.invoke_power_event(display_power.PowerEvent.S3, 60), True,
                              "System went to S3 and resume unsuccessful")
        elif self.disp_power.is_power_state_supported(display_power.PowerEvent.CS):
            self.assertEquals(self.disp_power.invoke_power_event(display_power.PowerEvent.CS, 60), True,
                              "System went to CS and resume unsuccessful")

        # Debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)


        # Verify writeback devices are present after resuming from S3
        logging.info("Step3 - Verify Writeback device persistence after resuming from S3")
        self.assertEquals(self.wb_verifier.is_wb_device_plugged(self.wb_device_count), True,
                          "Aborting the test as writeback device is not enumearated after plugging")
        logging.info("\tPASS: Writeback devices are enumerated correctly after resuming back from S3")

        # Go to S4 and resume
        if self.disp_power.is_power_state_supported(display_power.PowerEvent.S4):
            self.assertEquals(self.disp_power.invoke_power_event(display_power.PowerEvent.S4, 60), True,
                              "System went to S4 and resume unsuccessful")

        # Debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)


        # Verify writeback devices are present after resuming from S4
        logging.info("Step5 - Verify Writeback device persistence after resuming from S4")
        self.assertEquals(self.wb_verifier.is_wb_device_plugged(self.wb_device_count), True,
                          "Aborting the test as writeback device is not enumearated after plugging")
        logging.info("\tPASS: Writeback devices are enumerated correctly after resuming back from S4")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('WritebackPowerEvents'))
    TestEnvironment.cleanup(outcome)
