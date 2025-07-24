#################################################################################################
# @file         override_bpc_encoding_display_events.py
# @brief        This is a custom script which can used to display configurations with supported bpc and encoding
#               will perform below functionalities
#               1.To configure bpc and encoding through escape
#               2.To perform register verification for bpc and encoding
#               3.Will perform the scenario based on input hotplug_unplug(), mode_switch()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
from Libs.Core import enum
from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *


##
# @brief - To perform persistence verification for BPC and Encoding
class OverrideBpcEncoding(OverrideBpcEncodingBase):
    ##
    # @brief        test_01_plug_unplug() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "HOTPLUG_UNPLUG", "Skip the  test step as athe action type is not hotplug-unplug")
    def test_01_plug_unplug(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    self.enable_and_verify(adapter.gfx_index,panel.display_and_adapterInfo,panel.pipe, panel.transcoder
                                           ,adapter.platform, adapter.platform_type,port,panel.is_lfp,panel.connector_port_type)

                    if panel.is_lfp is False:
                        ##
                        # Verify the persistence
                        if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                               panel.port_type):
                            for gfx_index, adapter in self.context_args.adapters.items():
                                for port, panel in adapter.panels.items():
                                    if panel.is_active and panel.connector_port_type != "VIRTUALDISPLAY":
                                        self.enable_and_verify(adapter.gfx_index,panel.display_and_adapterInfo,
                                                               panel.pipe,panel.transcoder, adapter.platform,
                                                               adapter.platform_type,port,panel.is_lfp,panel.connector_port_type)

                        else:
                            self.fail("Fail : Fail to unplug the port")

        ##
        # plug the display
        gfx_adapter_details = self.config.get_all_gfx_adapter_details()
        display_details_list = self.context_args.test.cmd_params.display_details
        self.plug_display(display_details_list)
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.connector_port_type != "VIRTUALDISPLAY":
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id, panel.transcoder,
                              self.panel_props_dict[gfx_index, port].Bpc,
                              self.panel_props_dict[gfx_index, port].Encoding) is False:
                        self.fail()

    ##
    # @brief test_02_mode switch function - Function to perform
    #                                       mode switch,which applies min and max mode and perform register verification
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MODE_SWITCH", "Skip the test step as the action type is not mode switch")
    def test_02_mode_switch(self):

        scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    ##
                    # Store the current mode
                    current_mode = self.config.get_current_mode(panel.display_and_adapterInfo)
                    self.enable_and_verify(adapter.gfx_index, panel.display_and_adapterInfo, panel.pipe,
                                           panel.transcoder, adapter.platform, adapter.platform_type,port,panel.is_lfp,
                                           panel.connector_port_type)
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
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id, panel.transcoder,
                                      self.panel_props_dict[gfx_index, port].Bpc,
                                      self.panel_props_dict[gfx_index, port].Encoding) is False:
                                self.fail()

                        ##
                        # switch back to the previous current mode
                        apply_mode(panel.display_and_adapterInfo, current_mode.HzRes, current_mode.VtRes,
                                   current_mode.refreshRate, current_mode.scaling)
                        ##
                        # Verify the registers
                        if panel.is_active:
                            plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                            if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id, panel.transcoder,
                                      self.panel_props_dict[gfx_index, port].Bpc,
                                      self.panel_props_dict[gfx_index, port].Encoding) is False:
                                self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the bpc and encoding for the panel and verify the persistence")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)