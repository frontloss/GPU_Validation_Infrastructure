########################################################################################################################
# @file      writeback_basic.py
# @brief     The basic test scenario tests the following functionalities.
#            * Verifies writeback devices are correctly plugged and enumerated.
#            * Verifies writeback buffers are dumped successfully or not.
# @author    Patel, Ankurkumar G
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Writeback.writeback_base import *

##
# @brief    Contains helper functions to verify writeback device plug/unplug and to verify writeback buffer capture
class WritebackBasic(WritebackBase):

    ##
    # @brief         unittest runTest function
    # @param[in]     self; Object of writeback base class
    # @return        void
    def test_run(self):

        # Plug and verify writeback devices
        logging.info("Step1 - Plug and verify writeback devices")
        self.assertEquals(self.plug_and_verify_wb_devices(), True,
                          "Aborting the test as plug & Verify failed for writeback devices")
        logging.info("\tPASS: Writeback devices are plugged and enumerated successfully")

        # for debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)

        # Dump writeback buffer 
        logging.info("Step2 - Dump writeback buffer")
        self.assertEquals(self.dump_buffers(), True, "Aborting the test as failed to dump output of writeback devices")
        logging.info("\tPASS: Dumped writeback buffers successfully")

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('WritebackBasic'))
    TestEnvironment.cleanup(outcome)
