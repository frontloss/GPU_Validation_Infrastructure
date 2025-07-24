#######################################################################################################################
# @file                 elp_vbt_updates.py
# @brief                This test script is a basic script where optimization levels are applied
#                       in both increasing and decreasing orders. Read of DPCD address 0x358
#                       to verify if the optimization levels are set correctly
# Sample CommandLines:  python elp_vbt_updates.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import display_essential
from Tests.Color.Features.ELP.elp_test_base import *


class elpVBTUpdates(ELPTestBase):
    ##
    # @brief - ELP Stress test
    def test_01_basic(self):
        # ##
        # # Enable ELP on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 2: Verifying persistence of both OPST and ELP in the VBT***")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    gfx_vbt = Vbt(gfx_index)
                    panel_index = gfx_vbt.get_lfp_panel_type(port)
                    logging.info("**** Enabling OPST in the VBT ****")
                    if common_utility.update_color_feature_status_in_vbt(gfx_index, gfx_vbt, panel_index, feature="OPST", enable_status=True) is False:
                        self.fail()

                    vbt_status_after_update = common_utility.read_feature_status_in_vbt(gfx_vbt, "ELP", panel_index)

                    if vbt_status_after_update['ELP']:
                        logging.info("*** Step 3 : Enable the ELP optimization on all supported panels when both ELP "
                                     "and OPST are enabled in the VBT ***")

                        while True:
                            new_level = random.randint(1, 3)
                            if new_level != self.user_opt_level:
                                break
                        logging.info("New User Level updated is {0}".format(self.user_opt_level))

                        if self.enable_elp_optimization_and_verify(new_level):
                            logging.error(
                                "FAIL : IGCL Escape call successful although support for ELP is Disabled in VBT")
                        else:
                            logging.info(
                                "PASS : DPCD is updated with 0 as both ELP and OPST are enabled in the VBT; Here "
                                "OPST will have a higher preference than ELP")

                            logging.info("*** Step 4: Disabling OPST support in the VBT ***")
                            if common_utility.update_color_feature_status_in_vbt(gfx_index, gfx_vbt, panel_index,
                                                                                 feature="OPST",
                                                                                 enable_status=False) is False:
                                logging.error("Failed to disable OPST in the VBT")
                                self.fail()

                            time.sleep(5)

                            vbt_status_after_update = common_utility.read_feature_status_in_vbt(gfx_vbt, "ELP", panel_index)
                            if vbt_status_after_update['ELP'] is False:
                                logging.error(
                                    "Status of ELP is DISABLED for Port {0} with panel_index {1}".format(
                                        panel.connector_port_type, panel_index))
                                self.fail()

                            if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                                self.fail()

    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    gfx_vbt = Vbt(gfx_index)
                    panel_index = gfx_vbt.get_lfp_panel_type(port)
                    vbt_status = common_utility.read_feature_status_in_vbt(gfx_vbt, "OPST", panel_index)
                    if vbt_status['OPST']:
                        if common_utility.update_color_feature_status_in_vbt(gfx_index, gfx_vbt, panel_index,
                                                                             feature="OPST",
                                                                             enable_status=False) is False:
                            logging.error("Failed to disable OPST in the VBT")
                            self.fail()

        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Set the optimization on supported panels by iterating through all the optimization levels"
        " in both increasing and decreasing orders"
        " and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
