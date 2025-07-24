#################################################################################################
# @file         apply_csc_persistence_display_events.py
# @brief        This scripts comprises of test functions  test_01_hotplug_unplug(), test_02_mode_switch() and
#               test_03_display_switch() and each of the functions  will perform below functionalities
#               1.To configure avi info for the display
#               2.To perform register verification for csc and gamma
#               3.Will perform the scenario based on input as hotplug_unplug(), mode_switch(), display_switch()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import unittest
import random
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common.common_utility import display_switch, get_modelist_subset, apply_mode
from Tests.Color.Features.ApplyCSC.apply_csc_base import *


##
# @brief - To perform persistence verification for apply csc
class ApplyCscTestPersistenceDisplayEvents(ApplyCSCTestBase):
    ############################
    # Test Function
    ############################

    ##
    # @brief test_01_hotplug unplug function - Function to perform hotplug unplug the display and perform register
    #                                          verification supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "HOTPLUG_UNPLUG",
                     "Skip the  test step as the action type is not hotplug unplug")
    def test_01_hotplug_unplug(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                              panel.display_and_adapterInfo, port, True) is False:
                        self.fail()

                    if panel.is_lfp is False:
                        if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False, panel.port_type):
                            for gfx_index, adapter in self.context_args.adapters.items():
                                for port, panel in adapter.panels.items():
                                    if panel.is_active and panel.is_lfp is False:
                                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                                  panel.display_and_adapterInfo, port, False) is False:
                                            self.fail()
                        else:
                            self.fail("Fail : Fail to unplug the port")

        ##
        # plug the display
        gfx_adapter_details = self.config.get_all_gfx_adapter_details()
        display_details_list = self.context_args.test.cmd_params.display_details
        self.plug_display(display_details_list=display_details_list)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                              panel.display_and_adapterInfo, port, False) is False:
                        self.fail()

    ##
    # @brief test_02_display switch function - Function to perform apply single config on each display and
    #                                          perform register verification on all panels and apply all display as
    #                                          extended or clone based on commandline and perform register verification
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "DISPLAY_SWITCH",
                     "Skip the  test step as the action type is not display switch")
    def test_02_display_switch(self):

        display_list: list = []
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                display_list.append(panel.display_and_adapterInfo)
                if panel.is_active and panel.is_lfp:
                    if display_switch(topology=enum.SINGLE,
                                      display_and_adapter_info_list=[panel.display_and_adapterInfo]):
                        logging.info("Pass : Applied single config on {0}".format(port))
                        if panel.is_active:
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                 panel.display_and_adapterInfo, port, True) is False:
                                self.fail()

        # If commandline topology was Extended then applied config will be Clone
        # If commandline topology was Clone then applied config will be Extended
        if self.test_params_from_cmd_line.topology != 1:
            if display_switch(enum.CLONE if self.test_params_from_cmd_line.topology == 3 else enum.EXTENDED,
                              display_list):
                config_str = "CLONE" if self.test_params_from_cmd_line.topology else "EXTENDED"
                logging.info("Pass : Applied {0} config on".format(config_str))

                for gfx_index, adapter in self.context_args.adapters.items():
                    for port, panel in adapter.panels.items():
                        if panel.is_active and panel.is_lfp:
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                 panel.display_and_adapterInfo, port, True) is False:
                                self.fail()
            else:
                self.fail("Failed to apply display config")

    ##
    # @brief test_03_mode switch function - Function to perform
    #                                       mode switch,which applies min and max mode and perform register verification
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MODE_SWITCH", "Skip the test step as the action type is not mode switch")
    def test_03_mode_switch(self):
        bpc = None
        encoding = None
        scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    ##
                    # Store the current mode
                    current_mode = self.config.get_current_mode(panel.display_and_adapterInfo)
                    if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                         panel.display_and_adapterInfo, port, True) is False:
                        self.fail()

                    mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))

                    # Mode_list should not be None for mode switch scenario. hardcoded to enum.MDS
                    if mode_list is None:
                        mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                    for mode in mode_list:
                        apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                   mode.scaling)

                        ##
                        # Verify the registers
                        if panel.is_active:
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                 panel.display_and_adapterInfo, port, False) is False:
                                self.fail()

                        ##
                        # switch back to the previous current mode
                        apply_mode(panel.display_and_adapterInfo, current_mode.HzRes, current_mode.VtRes,
                                   current_mode.refreshRate, current_mode.scaling)
                        ##
                        # Verify the registers
                        if panel.is_active:
                            if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                 panel.display_and_adapterInfo, port, False) is False:
                                self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)