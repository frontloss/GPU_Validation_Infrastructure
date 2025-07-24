#################################################################################################
# @file         quantization_persistence_gfx_events.py
# @brief        This scripts comprises of test functions test_01_power_events(), test_02_restart_display_driver()
#               each of the functions  will perform below functionalities
#               1.To configure avi info for the display
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantization range
#               3.Will perform  power_events(),restart_display_driver(),monitor_turn_offon()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import unittest
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import common_utility
from Tests.Color.Common.common_utility import invoke_power_event
from Tests.Color.Features.Quantization.quantization_test_base import *


##
# @brief - To perform persistence verification for quantization range
class QuantisationPersistenceGfxEvents(QuantizationTestBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief test_01_power events function - Function to perform
    #                                        power events S3,CS,S4 and perform register verification on all panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() not in ["POWER_EVENT_S3", "POWER_EVENT_S4", "POWER_EVENT_CS"],
                     "Skip the  test step as the action type is not power event S3/CS/S4")
    def test_01_power_events(self):

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_CS": display_power.PowerEvent.CS,
            "POWER_EVENT_S4": display_power.PowerEvent.S4}

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform, panel.pipe, plane_id,
                                           panel.transcoder, panel.connector_port_type, configure_avi=True)

        ##
        # Invoke power event
        if invoke_power_event(power_state_dict[self.scenario]) is False:
            self.fail(" Fail: Failed to invoke power event {0}".format(power_state_dict[self.scenario]))
        else:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp is False:
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform, panel.pipe, plane_id,
                                               panel.transcoder, panel.connector_port_type,
                                               configure_avi=False)

    ##
    # @brief test_02_restart display driver function - Function to perform restart display driver and perform register
    #                                                  verification on all supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_02_restart_display_driver(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform, panel.pipe, plane_id,
                                           panel.transcoder, panel.connector_port_type, configure_avi=True)
            ##
            # restart display driver
            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail('Fail: Failed to Restart Display driver')
            else:
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp is False:
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform, panel.pipe,
                                               plane_id, panel.transcoder, panel.connector_port_type,
                                               configure_avi=False)

    ##
    # @brief test_03_restart display driver function - Function to perform monitor turnoff_on and perform register
    #                                                  verification on all panels
    #                                                  .
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MONITOR_TURNOFFON",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_03_monitor_turnoffon(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform, panel.pipe, plane_id,
                                           panel.transcoder, panel.connector_port_type, configure_avi=True)

        ##
        # monitor turn off-on
        if common_utility.invoke_monitor_turnoffon() is False:
            self.fail("Failed to Turned Off-On Monitor event")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    self.enable_and_verify(panel.display_and_adapterInfo, adapter.platform, panel.pipe, plane_id,
                                           panel.transcoder, panel.connector_port_type, configure_avi=False)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the quantization range and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
