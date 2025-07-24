##
# @file tdr_config_change.py
# @brief The script tests whether the driver is able to set various display configurations after returning from a TDR.
# @details For tests on pre-si, please add/change below registry keys to enable TDR in pre-silicon fulsim guest system
#        *  at location HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Control\\GraphicsDrivers TdrLevel to value 0x3
#        *  and TdrDebugMode to 0x2
# @author Patel, Ankurkumar G, Doriwala, Nainesh P

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify

from Tests.TDR.tdr_base import *


##
# @brief It contains the methods to verify whether the driver is able to set various display configurations after TDR
class TDRConfigChange(TDRBase):
    ##
    # @brief step 1 rebooting system to handle reg key update
    # @return None
    def test_1_step(self):
        logging.debug("Entry: test_1_step()")

        if reboot_helper.reboot(self, 'test_2_step') is False:
            self.is_teardown_required = True
            self.fail("Failed to reboot the system")

    ##
    # @brief tdr generate and verify able to apply display config
    # @return None
    def test_2_step(self):
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("in TDR test under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))
        self.assertEqual(display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True), True,
                         "TDR is not generated")
        logging.info("TDR generated Successfully")

        self.assertEqual(display_essential.detect_system_tdr(gfx_index='gfx_0'), True, "TDR is not detected")
        logging.info("TDR detected Successfully")

        if display_essential.clear_tdr() is True:
            logging.info("TDR cleared successfully post TDR generation")

        logging.info("Verification of Underrun after TDR")
        self.underrun.verify_underrun()

        # Set valid configuration Post TDR
        logging.info("Verifying enumerated display and Apply config post TDR generation on GFX_0"),
        self.enumerated_display = self.config.get_enumerated_display_info()
        # enumerated_display is a list of plugged displays, verify for match in both list
        if len([item for item in self.plugged_display if item not in self.input_display_list]) != 0:
            self.is_teardown_required = True
            self.fail("Required displays are not enumerated")
        self.assertNotEqual(self.enumerated_display.Count, 0, "Aborting the test as enumerated display count is zero")
        display_adapter_info_list = []
        for item in self.input_display_list:
            logging.info("0: {}, 1: {}".format(item[0], item[1]))
            display_adapter_info_list.append(self.config.get_display_and_adapter_info_ex(item[0], item[1]))
        self.assertEqual(self.config.set_display_configuration_ex(self.cmd_config, display_adapter_info_list,
                                                                  self.config.get_enumerated_display_info()),
                         True, "failed to apply display configuration")
        self.is_teardown_required = True


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('TDRConfigChange'))
    TestEnvironment.cleanup(outcome)
