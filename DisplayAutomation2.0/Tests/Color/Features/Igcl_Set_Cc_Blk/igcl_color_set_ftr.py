########################################################################################################################
# @file         igcl_color_set_ftr.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API.
#               We can configure either each block independently or in combination
# @author       Smitha B
########################################################################################################################
from Tests.Color.Features.Igcl_Set_Cc_Blk.igcl_color_test_base import *
from Libs.Core import reboot_helper

##
# @brief - Set Pixel Transformation Control Library Test
class IGCLColorSetFtr(IGCLColorTestBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def test_before_reboot(self):
        color_etl_utility.stop_etl_capture("name")
        ## Rebooting system
        reboot_helper.reboot(self,"test_after_reboot")

        
    def test_after_reboot(self):
        self.prepare_color_properties()
        #
        # ##
        # # Enable only the CSC block on all the supported panels and perform register level verification
        logging.info("*** Step 1 : Enable any/all the Color block on all supported panels and verify ***")
        if self.enable_igcl_color_ftr_and_verify() is False:
            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set Color Ftr API Verification')
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('IGCLColorSetFtr'))
    TestEnvironment.cleanup(outcome)
