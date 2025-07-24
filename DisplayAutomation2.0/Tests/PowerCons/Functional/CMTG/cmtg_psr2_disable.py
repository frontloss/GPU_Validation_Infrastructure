########################################################################################################################
# @file         cmtg_psr2_disable.py
# @brief        Contains basic functional tests covering below scenarios:
#               * CMTG verification in with PSR2 disable and enable in SD EDP and Dual eDP combinations
# @author       Bhargav Adigarla
########################################################################################################################
from Libs.Core import display_essential
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.CMTG.cmtg_base import *
from Tests.PowerCons.Functional.PSR import psr


##
# @brief        Contains basic CMTG tests
class CmtgPsr2Disable(CmtgBase):
    ##
    # @brief        This function verifies CMTG with SD and Dual edp scenarios
    # @return       None
    def t_10_psr2_disable_enable(self):
        for adapter in dut.adapters.values():
            logging.info("Verifying CMTG before disabling PSR2")
            self.verify_cmtg()
            psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
            if psr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
            logging.info("Verifying CMTG status after disabling PSR2")
            if cmtg.verify_cmtg_status(adapter) is True:
                self.fail("CMTG enabled after disabling PSR2")
            psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
            if psr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
            logging.info("Verifying CMTG after enabling PSR2")
            self.verify_cmtg()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CmtgPsr2Disable))
    test_environment.TestEnvironment.cleanup(test_result)
