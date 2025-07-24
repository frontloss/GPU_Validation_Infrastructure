#######################################################################################################################
# @file         ubrr_validate.py
# @brief        Contains tests covering below scenarios:
#               * DESKTOP
#
# @author       Vinod D S
#######################################################################################################################
from Tests.IDT.UBRR.ubrr_base import *

from Libs.Core import display_essential, display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.wrapper import control_api_wrapper
from Tests.IDT.UBRR import ubrr


##
# @brief        This class contains UBRR tests. This class inherits the UbrrBase class.
class UbrrValidate(UbrrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Feature enable via IGCL API
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["ENABLE_IN_IGCL"])
    # @endcond
    def t_11_igcl(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} ..")
                self.validate_ubrr(adapter, panel, skip_disable=True)

    ############################
    # Test Function
    ############################

    ##
    # @brief        Standard UBRR verification
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["STANDARD"])
    # @endcond
    def t_12_standard(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} ..")
                self.validate_ubrr(adapter, panel)

    ##
    # @brief        UBRR verification in CS/S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS", "S3"])
    # @endcond
    def t_13_cs_s3(self):
        display_power_ = display_power.DisplayPower()
        cs_supported = display_power_.is_power_state_supported(display_power.PowerEvent.CS)
        power_event = display_power.PowerEvent.CS if cs_supported else display_power.PowerEvent.S3

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} ..")
                self.validate_ubrr(adapter, panel, skip_disable=True)

                if display_power_.invoke_power_event(power_event) is False:
                    self.fail(f"FAILED to initiate and resume from {power_event.name}")

                current_status = ubrr.status(adapter, panel)
                if current_status is None:
                    self.fail(f"FAILED to get UBRR status on {panel.port}")
                if current_status.enabled is True or current_status.enabled_type != ubrr.UbrrType.NONE:
                    self.fail(f"UBRR {current_status.enabled_type.name} is still enabled "
                              f"(Expected to reset after CS/S3 on {panel.port}")
                logging.info(f"UBRR is disabled/reset after CS/S3 on {panel.port}")

                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} post CS/S3 ..")
                self.validate_ubrr(adapter, panel)

    ##
    # @brief        UBRR verification in S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_14_s4(self):
        display_power_ = display_power.DisplayPower()
        power_event = display_power.PowerEvent.S4

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} ..")
                self.validate_ubrr(adapter, panel, skip_disable=True)

                if display_power_.invoke_power_event(power_event) is False:
                    self.fail(f"FAILED to initiate and resume from {power_event.name}")

                current_status = ubrr.status(adapter, panel)
                if current_status is None:
                    self.fail(f"FAILED to get UBRR status on {panel.port}")
                if current_status.enabled is True or current_status.enabled_type != ubrr.UbrrType.NONE:
                    self.fail(f"UBRR {current_status.enabled_type.name} is still enabled "
                              f"(Expected to reset after S4 on {panel.port}")
                logging.info(f"UBRR is disabled/reset after S4 on {panel.port}")

                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} post S4 ..")
                self.validate_ubrr(adapter, panel)

    ##
    # @brief        UBRR verification with TDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["TDR"])
    # @endcond
    def t_15_tdr(self):
        VerifierCfg.tdr = Verify.SKIP
        logging.debug(f"Updated config under-run:{VerifierCfg.underrun.name}, tdr:{VerifierCfg.tdr.name}")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} ..")
                self.validate_ubrr(adapter, panel, skip_disable=True)

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

                current_status = ubrr.status(adapter, panel)
                if current_status is None:
                    self.fail(f"FAILED to get UBRR status on {panel.port}")
                if current_status.enabled is True or current_status.enabled_type != ubrr.UbrrType.NONE:
                    self.fail(f"UBRR {current_status.enabled_type.name} is still enabled "
                              f"(Expected to reset after TDR on {panel.port}")
                logging.info(f"UBRR is disabled/reset after TDR on {panel.port}")

                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} post TDR ..")
                self.validate_ubrr(adapter, panel)

    ##
    # @brief        UBRR verification with Driver Restart
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DRIVER_RESTART"])
    # @endcond
    def t_16_driver_restart(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} ..")
                self.validate_ubrr(adapter, panel, skip_disable=True)

                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail(f"FAILED to restart display driver for {adapter.name}")
                logging.info(f"\tSuccessfully restarted display driver for {adapter.name}")

                current_status = ubrr.status(adapter, panel)
                if current_status is None:
                    self.fail(f"FAILED to get UBRR status on {panel.port}")
                if current_status.enabled is True or current_status.enabled_type != ubrr.UbrrType.NONE:
                    self.fail(f"UBRR {current_status.enabled_type.name} is still enabled "
                              f"(Expected to reset after Driver Restart on {panel.port}")
                logging.info(f"UBRR is disabled/reset after Driver Restart on {panel.port}")

                logging.info(f"Validating UBRR on {panel.port} on {adapter.name} post Driver Restart ..")
                self.validate_ubrr(adapter, panel)


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(UbrrValidate))
    TestEnvironment.cleanup(test_result)
