#################################################################################################
# @file         ycbcr_persistence_display_events.py
# @brief        This scripts comprises of test_01_hotplug_unplug(), test_02_mode_switch(),test_03_display_switch() and
#               of functions and each of the functions  will perform below functionalities
#               1.enable/disable ycbcr feature
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantisation range
#               3.Will perform hotplug_unplug(),mode_switch(), display_switch()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import sys
import unittest
import random

from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common.common_utility import display_switch, get_modelist_subset, apply_mode
from Tests.Color.Features.YCbCr.ycbcr_test_base import *


##
# @brief - To perform persistence verification for ycbcr
class YcbcrPersistenceDisplayEvents(YcbcrBase):
    ############################
    # Test Function
    ############################

    ##
    # @brief test_01_hotplug unplug function - Function to perform enable disable ycbcr feature on display and
    #                                          hotplug unplug the display and perform register verification on all ycbcr
    #                                          supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "HOTPLUG_UNPLUG",
                     "Skip the  test step as the action type is not hotplug unplug")
    def test_01_hotplug_unplug(self):

        self.enable_and_verify()

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False and panel.connector_port_type != "VIRTUALDISPLAY":
                    ##
                    # unplug and verify
                    if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                           panel.port_type):

                        for gfx_index, adapter in self.context_args.adapters.items():
                            for port, panel in adapter.panels.items():
                                update_ycbcr_caps_in_context(panel.connector_port_type,panel.display_and_adapterInfo,self.context_args.adapters[gfx_index].panels[port])
                                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                                    # Verify the registers
                                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                                    if verify(port, adapter.platform, panel.display_and_adapterInfo,
                                              panel.pipe, plane_id, panel.transcoder, self.sampling, True):
                                        logging.info(
                                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                                panel.connector_port_type,
                                                adapter.gfx_index))
                                    else:
                                        self.fail("Register verification for YCbCr panel {0} on {1} failed".format(
                                            panel.connector_port_type,
                                            adapter.gfx_index))
                    else:
                        self.fail("Failed to unplug the port {0}".format(panel.port_type))
        ##
        # plug the display
        gfx_adapter_details = self.config.get_all_gfx_adapter_details()
        display_details_list = self.context_args.test.cmd_params.display_details
        self.plug_display(display_details_list)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                # Verify the registers

                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo,
                              panel.pipe, plane_id, panel.transcoder, self.sampling, True):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                panel.connector_port_type,
                                adapter.gfx_index))
                    else:
                        self.fail("Register verification for YCbCr panel {0} on {1} failed".format(
                            panel.connector_port_type,
                            adapter.gfx_index))

    ##
    # @brief test_02_mode switch function - Function to perform enable disable ycbcr feature on display and
    #                                       mode switch,which applies min and max mode and perform register verification
    #                                       on all ycbcr supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MODE_SWITCH", "Skip the test step as the action type is not mode switch")
    def test_02_mode_switch(self):
        scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
        self.enable_and_verify()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    mode_list = get_modelist_subset(panel.display_and_adapterInfo, 2, random.choice(scaling))
                    if mode_list is None:
                        mode_list = get_modelist_subset(panel.display_and_adapterInfo, 2, enum.MDS)
                    for mode in mode_list:

                        apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                   mode.scaling)
                        ##
                        # Verify the registers
                        update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                                     self.context_args.adapters[gfx_index].panels[port])
                        if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe,
                                      plane_id, panel.transcoder, self.sampling, True):
                                logging.info(
                                    "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                        panel.connector_port_type,
                                        adapter.gfx_index))
                            else:
                                self.fail("Register verification for YCbCr panel {0} on {1} failed".format(
                                    panel.connector_port_type,
                                    adapter.gfx_index))

    ##
    # @brief test_03_display switch function - Function to perform enable disable ycbcr feature on display and
    #                                          apply single config on each display and perform register verification on
    #                                          all ycbcr supported panles and apply all display as extended or clone
    #                                          based on commandline and perform register verification
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "DISPLAY_SWITCH",
                     "Skip the  test step as the action type is not display switch")
    def test_03_display_switch(self):
        self.enable_and_verify()
        display_list: list = []
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                display_list.append(panel.display_and_adapterInfo)
                if panel.is_active and panel.FeatureCaps.YCbCrSupport and panel.is_lfp is False:
                    if display_switch(topology=enum.SINGLE,
                                      display_and_adapter_info_list=[panel.display_and_adapterInfo]):
                        logging.info("Pass : Applied single config on {0}".format(port))

                        update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                                     self.context_args.adapters[gfx_index].panels[port])
                        if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                            ##
                            # Verify the registers
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe,
                                      plane_id,panel.transcoder, self.sampling, True):
                                logging.info(
                                    "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                        panel.connector_port_type,
                                        adapter.gfx_index))
                            else:
                                self.fail("Register verification for YCbCr panel {0} on {1} failed".format(
                                    panel.connector_port_type,
                                    adapter.gfx_index))

        # If commandline topology was Extended then applied config will be Clone
        # If commandline topology was Clone then applied config will be Extended
        if self.test_params_from_cmd_line.topology != 1:
            if display_switch(enum.CLONE if self.test_params_from_cmd_line.topology == 3 else enum.EXTENDED,
                              display_list):
                config_str = "CLONE" if self.test_params_from_cmd_line.topology else "EXTENDED"
                logging.info("Pass : Applied {0} config".format(config_str))
                for gfx_index, adapter in self.context_args.adapters.items():
                    for port, panel in adapter.panels.items():
                        update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                                     self.context_args.adapters[gfx_index].panels[port])
                        if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe,
                                      plane_id,panel.transcoder, self.sampling, True):
                                logging.info(
                                    "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                        panel.connector_port_type,
                                        adapter.gfx_index))
                            else:
                                self.fail("Register verification for YCbCr panel {0} on {1} failed".format(
                                    panel.connector_port_type,
                                    adapter.gfx_index))
            else:
                self.fail("Failed to apply display config")

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables YCbCr on supported panels and perform verification on all panels when "
        "YCbCr is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
