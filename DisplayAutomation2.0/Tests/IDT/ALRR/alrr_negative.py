######################################################################################################################
# @file         alrr_negative.py
# @brief        Contains tests covering below scenarios:
#               PSR2 Disable
#
# @author       Ravichandran M
#######################################################################################################################
from Tests.IDT.ALRR.alrr_base import *
from Libs.Core import display_essential
from Libs.Core.test_env import test_environment
from Libs.Feature.powercons import registry
from Libs.Core import registry_access


##
# @brief        This class contains ALRR negative tests. This class inherits the AlrrBase class.
class AlrrNegativeTest(Alrrbase):

    ##
    # @brief        ALRR verification with PSR2 Disable
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR2_REGKEY"])
    # @endcond
    def t_18_alrr_psr2_disable(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} ..")
                logging.info(f"\tUpdating {registry.RegKeys.PSR.PSR2_DISABLE}= 0x1 for {adapter.gfx_index}")
                # Disabling PSR2 via Regkey
                psr2_status = registry.write(adapter.gfx_index, registry.RegKeys.PSR.PSR2_DISABLE,
                                             registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
                if psr2_status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to do Driver restart post Regkey updates")
                    logging.info("Successfully restarted display driver")
                if psr2_status is False:
                    self.fail(f"\tFAILED to update {registry.RegKeys.PSR.PSR2_DISABLE} reg-key")
                logging.info(f"\tPASS: Updated {registry.RegKeys.PSR.PSR2_DISABLE} reg-key")

                self.validate_alrr(adapter, panel, expect_alrr=True, expect_psr2=False)

                # Enabling PSR2 via Regkey
                psr2_disable = registry.write(adapter.gfx_index, registry.RegKeys.PSR.PSR2_DISABLE,
                                              registry_access.RegDataType.DWORD, registry.RegValues.DISABLE)

                if psr2_disable is False:
                    self.fail(f"\tFAILED to update {registry.RegKeys.PSR.PSR2_DISABLE} reg-key")
                logging.info(f"\tPASS: Updated {registry.RegKeys.PSR.PSR2_DISABLE} reg-key")

                if psr2_disable is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to do Driver restart post Regkey updates")
                    logging.info("Successfully restarted display driver")

                self.validate_alrr(adapter, panel)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(AlrrNegativeTest))
    test_environment.TestEnvironment.cleanup(test_result)