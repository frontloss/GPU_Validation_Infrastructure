#######################################################################################################################
# @file         alrr_validate.py
# @brief        Contains tests covering below scenarios:
#               Basic, Power Events, Driver Restart, TDR
#
# @author       Ravichandran M
#######################################################################################################################
from Tests.IDT.ALRR.alrr_base import *
from Libs.Core import display_essential, display_power
from Libs.Core.test_env import test_environment
from Libs.Core.Verifier import common_verification_args


##
# @brief        This class contains ALRR tests. This class inherits the AlrrBase class.
class AlrrValidate(Alrrbase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Standard ALRR verification
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["STANDARD"])
    # @endcond
    def t_12_alrr_standard(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} ..")
                self.validate_alrr(adapter, panel)

    ##
    # @brief        ALRR verification in CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_13_alrr_cs(self):
        display_power_ = display_power.DisplayPower()
        if display_power_.is_power_state_supported(display_power.PowerEvent.S3) is True:
            self.fail("Test needs CS enabled system, but it is having CS disabled (Planning Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} ..")
                self.validate_alrr(adapter, panel)

                if display_power_.invoke_power_event(display_power.PowerEvent.CS) is False:
                    self.fail(f"FAILED to initiate and resume from {display_power.PowerEvent.CS.name}")

                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} post CS ..")
                self.validate_alrr(adapter, panel)

    ##
    # @brief        ALRR verification in S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_14_alrr_s3(self):
        display_power_ = display_power.DisplayPower()
        if display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("Test needs CS disabled system, but it is having CS enabled (Planning Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} ..")
                self.validate_alrr(adapter, panel)

                if display_power_.invoke_power_event(display_power.PowerEvent.S3) is False:
                    self.fail(f"FAILED to initiate and resume from {display_power.PowerEvent.S3.name}")

                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} post S3 ..")
                self.validate_alrr(adapter, panel)

    ##
    # @brief        ALRR verification in S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_15_alrr_s4(self):
        display_power_ = display_power.DisplayPower()

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} ..")
                self.validate_alrr(adapter, panel)

                if display_power_.invoke_power_event(display_power.PowerEvent.S4) is False:
                    self.fail(f"FAILED to initiate and resume from {display_power.PowerEvent.S4.name}")

                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} post S4 ..")
                self.validate_alrr(adapter, panel)

    ##
    # @brief        ALRR verification with TDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["TDR"])
    # @endcond
    def t_16_alrr_tdr(self):
        common_verification_args.VerifierCfg.tdr = common_verification_args.Verify.SKIP
        logging.debug(f"Updated config under-run:{common_verification_args.VerifierCfg.underrun.name}, "
                      f"tdr:{common_verification_args.VerifierCfg.tdr.name}")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} ..")
                self.validate_alrr(adapter, panel)

                if display_essential.detect_system_tdr(gfx_index=adapter.gfx_index) is True:
                    self.fail("TDR found before triggering the force TDR")

                # Generate TDR
                if display_essential.generate_tdr(gfx_index=adapter.gfx_index, is_displaytdr=True) is False:
                    self.fail("FAILED to generate force TDR")

                # Detect TDR generation
                if display_essential.detect_system_tdr(gfx_index=adapter.gfx_index) is False:
                    self.fail("FAILED to detect force TDR")

                # Clear TDR dumps from system
                if display_essential.clear_tdr() is True:
                    logging.info("TDR cleared successfully post force TDR generation")

                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} post TDR ..")
                self.validate_alrr(adapter, panel)

    ##
    # @brief        ALRR verification with Driver Restart
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["ALRR_REG_KEY"])
    # @endcond
    def t_17_alrr_reg_key(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} ..")

                alrr_status = alrr.disable(adapter)  # Disable ALRR via Regkey
                if alrr_status is False:
                    self.fail(f"Failed to disable ALRR in{adapter.name}")
                if alrr_status is True:
                    alrr_status, reboot_required = display_essential.restart_gfx_driver()
                    if alrr_status is False:
                        self.fail(f"Failed to do Driver restart post Regkey updates")
                    logging.info("Successfully restarted display driver")

                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} with ALRR disable ..")
                self.validate_alrr(adapter, panel, expect_alrr=True)

                alrr_status = alrr.enable(adapter)  # Enable ALRR via Regkey
                if alrr_status is False:
                    self.fail(f"Failed to disable ALRR in{adapter.name}")
                if alrr_status is True:
                    alrr_status, reboot_required = display_essential.restart_gfx_driver()
                    if alrr_status is False:
                        self.fail(f"Failed to do Driver restart post Regkey updates")
                    logging.info("Successfully restarted display driver")

                logging.info(f"Validating ALRR on {panel.port} on {adapter.name} with ALRR enable ..")
                self.validate_alrr(adapter, panel)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(AlrrValidate))
    test_environment.TestEnvironment.cleanup(test_result)
