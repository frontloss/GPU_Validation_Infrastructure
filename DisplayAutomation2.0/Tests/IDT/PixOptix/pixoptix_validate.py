#######################################################################################################################
# @file         pixoptix_validate.py
# @brief        Contains tests covering below scenarios:
#               Basic, Power Events, Driver Restart, TDR
#
# @author       Ravichandran M
#######################################################################################################################

from Tests.IDT.PixOptix.pixoptix_base import *
from Libs.Core.test_env import test_environment
from Libs.Core import display_essential, display_power
from Libs.Core.Verifier import common_verification_args


##
# @brief        This class contains PixOptix tests. This class inherits the Pixoptixbase class.
class PixoptixValidate(PixoptixBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Standard Pixoptix verification
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["STANDARD"])
    # @endcond
    def t_11_pixoptix_standard(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} ..")
                self.validate_pixoptix(adapter, panel)

    ##
    # @brief        PixOptix verification in CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_12_pixoptix_cs(self):
        display_power_ = display_power.DisplayPower()
        if display_power_.is_power_state_supported(display_power.PowerEvent.S3) is True:
            self.fail("Test needs CS enabled system, but it is having CS disabled (Planning Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} ..")
                self.validate_pixoptix(adapter, panel)

                if display_power_.invoke_power_event(display_power.PowerEvent.CS) is False:
                    self.fail(f"FAILED to initiate and resume from {display_power.PowerEvent.CS.name}")

                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} post CS ..")
                self.validate_pixoptix(adapter, panel)

    ##
    # @brief        PixOptix verification in S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_13_pixoptix_s4(self):
        display_power_ = display_power.DisplayPower()

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} ..")
                self.validate_pixoptix(adapter, panel)

                if display_power_.invoke_power_event(display_power.PowerEvent.S4) is False:
                    self.fail(f"FAILED to initiate and resume from {display_power.PowerEvent.S4.name}")

                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} post S4 ..")
                self.validate_pixoptix(adapter, panel)

    ##
    # @brief        PixOptix verification with TDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["TDR"])
    # @endcond
    def t_14_pixoptix_tdr(self):
        common_verification_args.VerifierCfg.tdr = common_verification_args.Verify.SKIP
        logging.debug(f"Updated config under-run:{common_verification_args.VerifierCfg.underrun.name}, "
                      f"tdr:{common_verification_args.VerifierCfg.tdr.name}")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} ..")
                self.validate_pixoptix(adapter, panel)

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

                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} post TDR ..")
                self.validate_pixoptix(adapter, panel)

    ##
    # @brief        PixOptix verification with Driver Restart
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DRIVER_RESTART"])
    # @endcond
    def t_15_pixoptix_driver_restart(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} ..")

                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} before driver restart")
                self.validate_pixoptix(adapter, panel)

                # Driver restart
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("\tFailed to restart display driver ")
                logging.info("Successfully restarted display driver")

                logging.info(f"Validating PixOptix on {panel.port} on {adapter.name} after driver restart")
                self.validate_pixoptix(adapter, panel)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PixoptixValidate))
    test_environment.TestEnvironment.cleanup(test_result)
