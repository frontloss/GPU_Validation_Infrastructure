#################################################################################################
# @file         ycbcr_persistence_gfx_events.py
# @brief        This scripts comprises of test functions_01_power_events(), test_02_restart_display_driver(),
#               test_03_monitor_turnoffon() of and each of the functions  will perform below functionalities
#               1.enable/disable ycbcr feature
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantisation range
#               3.Will perform  power_events(),restart_display_driver(),monitor_turnoffon()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import sys
import unittest
from Libs.Core import display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common.common_utility import invoke_power_event
from Tests.Color.Features.YCbCr.ycbcr_test_base import *

##
# @brief - To perform persistence verification for ycbcr
class YcbcrPersistenceGfxEvents(YcbcrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief test_01_power events function - Function to perform enable disable ycbcr feature on display and invoke
    #                                        power events S3,CS,S4 and perform register verification on all ycbcr
    #                                        supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() not in ["POWER_EVENT_S3", "POWER_EVENT_S4", "POWER_EVENT_CS"],
                     "Skip the  test step as the action type is not power event S3/CS/S4")
    def test_01_power_events(self):

        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_CS": display_power.PowerEvent.CS,
            "POWER_EVENT_S4": display_power.PowerEvent.S4}
        self.enable_and_verify()
        ##
        # Invoke power event
        if invoke_power_event(power_state_dict[self.scenario]) is False:
            self.fail("Failed to invoke power event {0}".format(power_state_dict[self.scenario]))
        else:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                                 self.context_args.adapters[gfx_index].panels[port])
                    if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                        ##
                        # Verify the registers
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe,
                                  plane_id, panel.transcoder, self.sampling, True):
                            logging.info(
                                "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format
                                (panel.connector_port_type, adapter.gfx_index))
                        else:
                            self.fail("Register verification for YCbCr panel {0} on {1} failed".format
                                      (panel.connector_port_type, adapter.gfx_index))

    ##
    # @brief test_02_restart display driver function - Function to perform enable disable ycbcr feature on display and
    #                                                  restart display driver and perform register verification on all
    #                                                  ycbcr supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_02_restart_display_driver(self):
        self.enable_and_verify()
        ##
        # restart display driver
        for gfx_index, adapter in self.context_args.adapters.items():
            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail("Failed to restart display driver")
            logging.info('Pass: Display driver restarted successfully')
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    ##
                    # Verify the registers
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, True):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format
                            (panel.connector_port_type, adapter.gfx_index))
                    else:
                        self.fail("Register verification for YCbCr panel {0} on {1} failed".format(panel.connector_port_type,
                                                                                              adapter.gfx_index))

    ##
    # @brief test_03_monitor_turnoffon function - Function to perform enable disable ycbcr feature on display and
    #                                              invoke monitor turnoff on event and perform register
    #                                              verification on all ycbcr supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MONITOR_TURNOFFON",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_03_monitor_turnoffon(self):

        self.enable_and_verify()
        ##
        # monitor turn off on
        if common_utility.invoke_monitor_turnoffon() is False:
            self.fail("Failed to turn off monitor")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    ##
                    # Verify the registers
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, True):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                                panel.connector_port_type,
                                adapter.gfx_index))
                    else:
                            self.fail("Register verification for YCbCr panel {0} on {1} failed".format(panel.connector_port_type,
                                                                                              adapter.gfx_index))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables and Disables YCbCr on supported panels and perform verification on all panels"
        " when YCbCr is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
