#######################################################################################################################
# @file                 elp_with_cabc.py
# @brief                This test script is a basic script where optimization levels are applied
#                       in both increasing and decreasing orders. Read of DPCD address 0x358
#                       to verify if the optimization levels are set correctly
# Sample CommandLines:  python elp_with_cabc.py -edp_a SINK_EDP076 -opt_level 2
# @author       Smitha B
#######################################################################################################################
from Libs.Core import registry_access
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.ELP.elp_test_base import *


class elpWithCabc(ELPTestBase):

    ##
    # @brief - ELP Stress test
    def test_01_basic(self):
        # ##
        # # Enable ELP on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        for gfx_index, adapter in self.context_args.adapters.items():
            reg_args = registry_access.StateSeparationRegArgs(gfx_index)
            logging.info("Exec env is Post Si hence the driver restart needs to be done")

            reg_value, reg_type = registry_access.read(args=reg_args, reg_name="DisplayPcFeatureControl")

            cabc_value = common_utility.get_bit_value(reg_value, 23, 23)
            logging.debug("23rd Bit CABC value {0}".format(cabc_value))
            logging.debug("DisplayPcFeatureCtl Reg Value is {0}".format(reg_value))
            enable_cabc = ((1 << 23) | reg_value)

            logging.debug("After Setting CABC Value {0}".format(enable_cabc))

            if not registry_access.write(args=reg_args, reg_name="DisplayPcFeatureControl",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=enable_cabc):
                logging.error("Registry key add to disable ForceHDRMode failed")
                self.fail()

            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail()

            for port, panel in adapter.panels.items():
                ##
                # Invoke the verification function for verification of the DPCD values
                expected_dpcd_level = mapping_user_level_to_dpcd(self.user_opt_level)
                if verify_opt_level_in_dpcd(gfx_index, panel, port, expected_dpcd_level):
                    logging.error("CABC and ELP are mutually exclusive; DPCD values not reflecting 0 as expected")
                    self.fail()
                else:
                    logging.info("PASS : CABC and ELP are mutually; DPCD is updated with 0 as expected")

    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            reg_args = registry_access.StateSeparationRegArgs(gfx_index)
            reg_value, reg_type = registry_access.read(args=reg_args, reg_name="DisplayPcFeatureControl")
            disable_cabc = reg_value & 0xFF7FFFFF
            if not registry_access.write(args=reg_args, reg_name="DisplayPcFeatureControl",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=disable_cabc):
                logging.error("Registry update to disable CABC in DisplayPcFeatureControl failed")
                self.fail()

            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail()

            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if get_elp_optimization_and_verify(panel.target_id, 0) is False:
                        return False

                    ##
                    # Invoke the verification function for verification of the DPCD values
                    expected_dpcd_level = mapping_user_level_to_dpcd(self.user_opt_level)
                    if verify_opt_level_in_dpcd(gfx_index, panel, port, expected_dpcd_level) is False:
                        return False

        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Set the optimization on supported panels by iterating through all the optimization levels"
        " in both increasing and decreasing orders"
        " and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
