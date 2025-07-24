########################################################################################################################
# @file         writeback_tdr.py
# @brief        The test scenario tests the following functionalities.
#               * Verify whether the devices are correctly plugged and enumerated.
#               * Generate TDR and verify whether the writeback devices are enumerated post TDR
#               * Verify configuration applied on writeback devices post TDR.
# @author       Patel, Ankurkumar G
########################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.Writeback.writeback_base import *

##
# @brief    Contains unitest runTest function to verify writeback device are enumerated and config is applied post TDR
class WritebackTdr(WritebackBase):

    ##
    # @brief        unittest runTest function
    # @param[in]    self; Object of writeback base class
    # @return       void
    def test_run(self):
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("Updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))


        # Plug and verify writeback devices
        logging.info("Step1 - Plug and verify writeback devices")
        self.assertEquals(self.plug_and_verify_wb_devices(), True,
                          "Aborting the test as plug & Verify failed for writeback devices")
        logging.info("\tPASS: Writeback devices are plugged and enumerated successfully")

        # for debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)

        # Generate TDR
        logging.info("Step2 - Generate TDR")
        self.assertEquals(display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True), True,
                          "TDR is not generated successfully")
        self.assertEquals(display_essential.detect_system_tdr(gfx_index='gfx_0'), True,
                          "Aborting the test as TDR generation failed.")
        logging.info("\tPASS: TDR generated Successfully")

        # Verify writeback devices are enumerated post TDR
        logging.info("Step3 - Verify writeback devices enumeration post TDR")
        self.assertEquals(self.wb_verifier.is_wb_device_plugged(self.wb_device_count), True,
                          "Aborting the test as writeback devices enumerated after TDR")
        logging.info("\tPASS: Writeback devices are enumerated successfully post TDR")

        # for debug purpose only
        self.wb_verifier.log_wd_register_proggramming(self.wb_device_list)

        # Verify config apply on writeback devices post TDR
        logging.info("Step4 - Verify config apply on writeback devices post TDR")
        self.apply_config_on_all_devices(enum.EXTENDED)
        logging.info("\tPASS: Applied config successfully on writeback devices post TDR")

        if display_essential.clear_tdr() is True:
            logging.info("TDR cleared successfully")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('WritebackTdr'))
    TestEnvironment.cleanup(outcome)
