#################################################################################################
# @file         hw_3d_lut_persistence_gfx_events.py
# @brief        This scripts comprises of test functions test_01_power_events(), test_02_monitor_turnoffon(),
#               test_03_dc_state() and test_04_restart_display_driver(). Each of the functions  will perform below functionalities
#               1.To configure 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               3.Will perform  invoke_power_events(),monitor_turn_offon(), dc_state(), restart_display_driver()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import unittest
from Libs.Core import display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common import common_utility
from Tests.Color.Common.common_utility import invoke_power_event
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *


##
# @brief - To perform persistence verification for HW_3D_LUT
from Tests.PowerCons.Functional.DCSTATES import dc_state


class Hw3DLutPersistenceGfxEvents(Hw3DLUTBase):

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
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()

        ##
        # Invoke power event
        if invoke_power_event(power_state_dict[self.scenario]) is False:
            self.fail(" Fail: Failed to invoke power event {0}".format(power_state_dict[self.scenario]))

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    logging.info("Verifying 3DLUT support after power event for panel connected to port {0} pipe {1} on adapter {2}"
                                  .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                    if panel.pipe in self.three_dlut_enable_pipe:
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            logging.info(
                                "Started 3DLUT verification for enabled pipe {0} available in the list".format(
                                    panel.pipe))
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe,
                                               panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                               enable=True, via_igcl=False) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                        else:
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                               panel.is_lfp,
                                               enable=True, via_igcl=True) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support via IGCL after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                    else:
                        logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                panel.pipe))

    ##
    # @brief test_02_monitor turnoff-on function - Function to perform monitor and perform register verification
    #                                              on all panels
    #                                                  .
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MONITOR_TURNOFFON",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_02_monitor_turnoffon(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()

        ##
        # monitor turn off on
        if common_utility.invoke_monitor_turnoffon() is False:
            self.fail("Failed to Turned Off Monitor")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    logging.info("Verifying 3DLUT support after monitor_turnoffon for panel connected to port {0} pipe {1} on adapter {2}"
                                  .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                    if panel.pipe in self.three_dlut_enable_pipe:
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            logging.info(
                                "Started 3DLUT verification for enabled pipe {0} available in the list".format(
                                    panel.pipe))
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe,
                                               panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                               enable=True, via_igcl=False) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                        else:
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                               panel.is_lfp,
                                               enable=True, via_igcl=True) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support via IGCL after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                    else:
                        logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                panel.pipe))

    ##
    # @brief test_03_dc_state_events function - Function to perform
    #                                           dc state events and perform register verification on all panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "DC_STATE",
                     "Skip the  test step as the action type is not DC state event")
    def test_03_dc_state(self):
        from Tests.PowerCons.Modules.dut_context import Adapter
        from Tests.PowerCons.Functional.DCSTATES.dc_state import verify_dc5_dc6

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()
        for gfx_index, adapter in self.context_args.adapters.items():
            adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
            adapter_info = adapter_info_dict[gfx_index.lower()]
            temp = Adapter(gfx_index, adapter_info)
            if verify_dc5_dc6(temp, method="APP"):
                logging.info("DC5/6 verification is successful")
            else:
                logging.info("Platform is {0}".format(adapter.platform))
                if adapter.platform in ('TGL', 'RKL', 'DG1', 'ADLS'):
                    logging.info("HW3DLUT + DC5/6 coexistence not supported on Gen12 platforms, "
                                 "hence DC5/6 will not be enabled when HW 3D LUT is already enabled")
                else:
                    self.fail()

            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if panel.pipe in self.three_dlut_enable_pipe:
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            logging.info(
                                "Started 3DLUT verification for enabled pipe {0} available in the list".format(
                                    panel.pipe))
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe,
                                               panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                               enable=True, via_igcl=False) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                        else:
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                               panel.is_lfp,
                                               enable=True, via_igcl=True) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support via IGCL after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                    else:
                        logging.info(
                            "Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                panel.pipe))
        ##
        # Invoke power event
        if invoke_power_event(display_power.PowerEvent.S3) is False:
            self.fail("Fail: Failed to invoke POWER_STATE_S3")
        for gfx_index, adapter in self.context_args.adapters.items():
            adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
            adapter_info = adapter_info_dict[gfx_index.lower()]
            temp = Adapter(gfx_index, adapter_info)
            if verify_dc5_dc6(temp, method="IDLE"):
                logging.info("DC5/6 verification is successful")
            else:
                logging.info("Platform is {0}".format(adapter.platform))
                if adapter.platform in ('TGL', 'RKL', 'DG1', 'ADLS'):
                    logging.info("HW3DLUT + DC5/6 coexistence not supported on Gen12 platforms, "
                                 "hence DC5/6 will not be enabled when HW 3D LUT is already enabled")
                else:
                    self.fail()

            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if panel.pipe in self.three_dlut_enable_pipe:
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            logging.info(
                                "Started 3DLUT verification for enabled pipe {0} available in the list".format(
                                    panel.pipe))
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe,
                                               panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                               enable=True, via_igcl=False) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                        else:
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                               panel.is_lfp,
                                               enable=True, via_igcl=True) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support via IGCL after mode_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                    else:
                        logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                panel.pipe))

    ##
    # @brief test_04_restart display driver function - Function to perform restart display driver and perform register
    #                                                  verification for hw_3d_lut on all supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_04_restart_display_driver(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()

            ##
            # restart display driver
            status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            if status is False:
                self.fail('Fail: Failed to Restart Display driver')
            else:
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.pipe in self.three_dlut_enable_pipe:
                        logging.info("Verifying 3DLUT support after RESTART_DRIVER for panel connected to port {0} pipe {1} on adapter {2}"
                                     .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            logging.info("Started 3DLUT verification for enabled pipe {0} available in the list".format(
                                panel.pipe))
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,panel.pipe,
                                               panel.transcoder, panel.target_id, self.inputfile,panel.is_lfp, enable=False, via_igcl=False) is False:
                                logging.error("Verification failed for 3DLUT support after RESTART_DRIVER for panel connected to port {0} pipe {1} on adapter {2}"
                                              .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                        else:
                            logging.info(
                                "Verifying 3DLUT support via IGCL after RESTART_DRIVER for panel connected to port {0} pipe {1} on adapter {2}"
                                .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe, panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                               enable=True, via_igcl=True) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support via IGCL after RESTART_DRIVER for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                            
                    else:
                        logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                panel.pipe))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)