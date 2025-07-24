#######################################################################################################################
# @file                 elp_persistence_with_display_events.py
# @brief                This scripts comprises modularized tests, where :
#                       1. test_02_mode_switch() - Intends to verify ELP Persistence with various modesets
#                       2. test_03_display_switch() - Intends to verify ELP Persistence with different topologies
#                       3. test_03_video_playback() - Intends to verify ELP with Videoplayback scenario
#                       Each of the test modules perform the following :
#               		The test script enables ELP on the internal displays supporting ELP.
#               		The test scripts then performs various events such as Modeset, Display Switching, VideoPlayback
#                       and then verifies if ELP is persisting after the events.
#                       The ETLs will be captured during the events and parsed to verify
#                       if there is any Blc Optimization DDI by OS.
#                       If there is None, then the optimization values should persist,
#                       if not, need to verify if the new optimization levels are updated in accordance to the DDI.

# Sample CommandLines:  python elp_persistence_with_display_events.py -edp_a SINK_EDP50 -hdmi_b -scenario HOTPLUG_UNPLUG
#                       python elp_persistence_with_display_events.py -edp_a SINK_EDP50 -scenario MODE_SWITCH
#                       python elp_persistence_with_display_events.py -edp_a SINK_EDP50 -dp_d -scenario DISPLAY_SWITCH
#                       python elp_persistence_with_display_events.py -edp_a SINK_EDP50 -dp_d -scenario VIDEO_PLAYBACK
#
# @author       Smitha B
#######################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Tests.Color.Features.ELP.elp_test_base import *


class elpPersistenceWithDisplayEvents(ELPTestBase):

    @unittest.skipIf(common_utility.get_action_type() != "MODE_SWITCH", "Skipped the test step as the action type is "
                                                                        "not MODE_SWITCH")
    def test_01_mode_switch(self):
        scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        logging.info("*** Step 2 : Perform Mode Switch and verify ***")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                    ##
                    # Store the current mode
                    current_mode = self.config.get_current_mode(panel.display_and_adapterInfo)
                    mode_list = common_utility.get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))
                    if mode_list is None:
                        mode_list = common_utility.get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                    for mode in mode_list:
                        common_utility.apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                   mode.scaling)

                        if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                            self.fail()

                    ##
                    # Switch back to the previous current mode
                    common_utility.apply_mode(panel.display_and_adapterInfo, current_mode.HzRes, current_mode.VtRes,
                               current_mode.refreshRate, current_mode.scaling)

                    if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                        self.fail()

    @unittest.skipIf(common_utility.get_action_type() != "DISPLAY_SWITCH",
                     "Skipped the  test step as the action type is not DISPLAY_SWITCH")
    def test_02_display_switch(self):
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        display_list: list = []
        ##
        logging.info("*** Step 2 : Apply different display configs and verify ***")
        # Applying Single Display Config on each of the panels and performing register verification
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                display_list.append(panel.display_and_adapterInfo)
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                    if common_utility.display_switch(topology=enum.SINGLE,
                                                     display_and_adapter_info_list=[panel.display_and_adapterInfo]):
                        logging.info(
                            "Pass : Applied {0} config on {1}".format(DisplayConfigTopology(enum.SINGLE).name, port))

                        if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                            self.fail()

        # If commandline topology was Extended then applied config will be Clone
        # If commandline topology was Clone then applied config will be Extended
        if self.test_params_from_cmd_line.topology != 1:
            topology = enum.CLONE if self.test_params_from_cmd_line.topology == 3 else enum.EXTENDED
            if common_utility.display_switch(topology, display_list):
                logging.info("Pass : Applied {0} config".format(DisplayConfigTopology(topology).name))
                for gfx_index, adapter in self.context_args.adapters.items():
                    for port, panel in adapter.panels.items():
                        if panel.is_active and panel.is_lfp:
                            if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                                self.fail()
            else:
                self.fail("Failed to apply display config")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Set the optimization on supported panels and perform persistence verification")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
