#################################################################################################
# @file         hw_3d_lut_display_persistence.py
# @brief        This scripts comprises of test functions  test_01_mode_switch() ,test_02_display_switch()
#               test_03_display_swap()
#               Each of the functions  will perform below functionalities
#               1.To configure 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               3.Will perform the scenario based on input mode_switch(), display_switch() and
#                 monitor_turnoff_on() and display_swap()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import unittest
import random
import time
from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common.common_utility import display_switch, get_modelist_subset, apply_mode
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *


##
# @brief - To perform persistence verification for HW_3D_LUT range
class HwTestPersistenceDisplayEvents(Hw3DLUTBase):
    ############################
    # Test Function
    ############################

    ##
    # @brief        test_01_plug_unplug() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "HOTPLUG_UNPLUG", "Skip the  test step as athe action type is not hotplug-unplug")
    def test_01_plug_unplug(self):
        bpc = None
        encoding = None
        # Enabling 3DLUT on all active panel
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
                        
        # Unplug External display and verifying 3DLUT Persistence
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_lfp is False and panel.is_active:
                    if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                           panel.port_type):
                        for gfx_index, adapter in self.context_args.adapters.items():
                            for port, panel in adapter.panels.items():
                                if panel.is_active and panel.connector_port_type != "VIRTUALDISPLAY":
                                    logging.info("Verifying 3DLUT support for panel connected to port {0} pipe {1} on adapter {2}"
                                                 .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                    if panel.pipe in self.three_dlut_enable_pipe:
                                        logging.info("Started 3DLUT verification for enabled pipe {0} available in the list" .format(panel.pipe))
                                        if not hw_3dlut.verify(adapter.gfx_index, adapter.platform,
                                                               panel.connector_port_type, panel.pipe,
                                                               panel.transcoder, panel.target_id, self.inputfile,
                                                               panel.is_lfp, enable=True,via_igcl=True):
                                            logging.error("Verification failed for 3DLUT support for panel connected to port {0} pipe {1} on adapter {2} after unplug display"
                                                          .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                            self.fail()
                                    else:
                                        logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list" .format(panel.pipe))
                    else:
                        self.fail("Fail : Fail to unplug the port")

        ##
        # Verify 3DLUT persistence after plug of the display
        gfx_adapter_details = self.config.get_all_gfx_adapter_details()
        display_details_list = self.context_args.test.cmd_params.display_details
        self.plug_display(display_details_list)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.connector_port_type != "VIRTUALDISPLAY":
                    logging.info(
                        "Verifying 3DLUT support for panel connected to port {0} pipe {1} on adapter {2} after plug display"
                        .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                    if panel.pipe in self.three_dlut_enable_pipe:
                        if adapter.platform in ('TGL', 'DG1', 'RKL'):
                            logging.info("Started 3DLUT verification for enabled pipe {0} available in the list".format(
                                panel.pipe))
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe,
                                               panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                               enable=True, via_igcl=False) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support after plug_unplug for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                        else:
                            if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                               panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                               panel.is_lfp,
                                               enable=True, via_igcl=True) is False:
                                logging.error(
                                    "Verification failed for 3DLUT support via IGCL after plug_unplug for panel connected to port {0} pipe {1} on adapter {2}"
                                    .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                self.fail()
                    
                    else:
                        logging.info(
                            "Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                panel.pipe))
    
        # # Disable Hw3DLut in all the panels and verify
        # for gfx_index, adapter in self.context_args.adapters.items():
        #     for port, panel in adapter.panels.items():
        #         if panel.is_active:
        #             if self.enable_and_verify_via_igcl(adapter, panel, False) is False:
        #                 self.fail()

    ##
    # @brief test_01_mode switch function - Function to perform
    #                                       mode switch,which applies min and max mode and perform register verification
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MODE_SWITCH", "Skip the test step as the action type is not mode switch")
    def test_01_mode_switch(self):
        scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    ##
                    # Store the current mode
                    current_mode = self.config.get_current_mode(panel.display_and_adapterInfo)
                    ##
                    # add verify
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()

                    mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))
                    if mode_list is None:
                        mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                    for mode in mode_list:
                        apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                   mode.scaling)

                        ##
                        # Verify the registers
                        if panel.is_active:
                            ##
                            logging.debug("Verifying 3DLUT support for panel connected to port {0} pipe {1} on adapter {2}"
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
                                            "Verification failed for 3DLUT support for panel connected to port {0} pipe {1} on adapter {2}"
                                            .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                        self.fail()
                                else:
                                    if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                                       panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                                       panel.is_lfp,
                                                       enable=True, via_igcl=True) is False:
                                        logging.error(
                                            "Verification failed for 3DLUT support via IGCL for panel connected to port {0} pipe {1} on adapter {2}"
                                            .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                        self.fail()
                            else:
                                logging.info(
                                    "Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                        panel.pipe))
                        
                        ##
                        # switch back to the previous current mode
                        apply_mode(panel.display_and_adapterInfo, current_mode.HzRes, current_mode.VtRes,
                                   current_mode.refreshRate, current_mode.scaling)

                        ##
                        # Verify the registers
                        if panel.is_active:
                            logging.info("Verifying 3DLUT support after mode switch for panel connected to port {0} pipe {1} on adapter {2}"
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
                                logging.info(
                                    "Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                        panel.pipe))
                        
                        # # Disable Hw3DLut in all the panels and verify
                        # for gfx_index, adapter in self.context_args.adapters.items():
                        #     for port, panel in adapter.panels.items():
                        #         if panel.is_active:
                        #             if self.enable_and_verify_via_igcl(adapter, panel, False) is False:
                        #                 self.fail()

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
                if panel.is_active:
                    display_list.append(panel.display_and_adapterInfo)
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if display_switch(topology=enum.SINGLE,
                                      display_and_adapter_info_list=[panel.display_and_adapterInfo]):
                        logging.info("Pass : Applied single config on {0}".format(port))

                        if panel.is_active:
                            logging.info("Verifying 3DLUT support for panel connected to port {0} pipe {1} on adapter {2}"
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
                                            "Verification failed for 3DLUT support before display_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                            .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                        self.fail()
                                else:
                                    if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                                       panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                                       panel.is_lfp,
                                                       enable=True, via_igcl=True) is False:
                                        logging.error(
                                            "Verification failed for 3DLUT support via IGCL before display_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                            .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                        self.fail()
                            else:
                                logging.info(
                                    "Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                        panel.pipe))
        
        # If commandline topology was Extended then applied config will be Clone
        # If commandline topology was Clone then applied config will be Extended
        if self.test_params_from_cmd_line.topology != 1:
            if display_switch(enum.CLONE if self.test_params_from_cmd_line.topology == 3 else enum.EXTENDED,
                              display_list):
                config_str = "CLONE" if self.test_params_from_cmd_line.topology else "EXTENDED"
                logging.info("Pass : Applied {0} config on".format(config_str))

                for gfx_index, adapter in self.context_args.adapters.items():
                    for port, panel in adapter.panels.items():
                        if panel.is_active:
                            logging.debug("Verifying 3DLUT support after display switch for panel connected to port {0} pipe {1} on adapter {2}"
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
                                            "Verification failed for 3DLUT support after display_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                            .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                        self.fail()
                                else:
                                    if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                                       panel.pipe, panel.transcoder, panel.target_id, self.inputfile,
                                                       panel.is_lfp,
                                                       enable=True, via_igcl=True) is False:
                                        logging.error(
                                            "Verification failed for 3DLUT support via IGCL after display_switch for panel connected to port {0} pipe {1} on adapter {2}"
                                            .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                                        self.fail()
                            else:
                                logging.info(
                                    "Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                                        panel.pipe))
            
            
            else:
                self.fail("Failed to apply display config")
                
        # # Disable Hw3DLut in all the panels and verify
        # for gfx_index, adapter in self.context_args.adapters.items():
        #     for port, panel in adapter.panels.items():
        #         if panel.is_active:
        #             if self.enable_and_verify_via_igcl(adapter, panel, False) is False:
        #                 self.fail()

    ##
    # @brief test_03_display_swap function -   Function to perform displays swap and perform register
    #                                          verification for hw_3d_lut on all supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "DISPLAY_SWAP",
                     "Skip the  test step as the action type is not display swap")
    def test_03_display_swap(self):

        display_list: list = []
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    display_list.append(panel.display_and_adapterInfo)
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()

        random.shuffle(display_list)
        if display_switch(topology=enum.EXTENDED,
                          display_and_adapter_info_list=display_list):
            logging.info("Pass : Display Swapped")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    logging.info("Verifying 3DLUT support after display swap for panel connected to port {0} pipe {1} on adapter {2}"
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
                            
        # # Disable Hw3DLut in all the panels and verify
        # for gfx_index, adapter in self.context_args.adapters.items():
        #     for port, panel in adapter.panels.items():
        #         if panel.is_active:
        #             if self.enable_and_verify_via_igcl(adapter, panel, False) is False:
        #                 self.fail()
  
                    
if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: .")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
