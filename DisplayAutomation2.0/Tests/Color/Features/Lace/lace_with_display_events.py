#################################################################################################
# @file         lace_with_display_events.py
# @brief        Test calls for get and set lace functionality with display events persistence
# @author       Vimalesh D
#################################################################################################
import sys
import unittest
import random

from Libs.Core import display_essential
from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_context
from Tests.Color.Common import color_constants
from Tests.Color.Features.Lace.lace_base import *
from Tests.Control_API.control_api_base import testBase
from Tests.Color.Common.common_utility import get_modelist_subset, apply_mode
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify


##
# @brief - To perform persistence verification for BPC and Encoding
class LaceDisplayEvents(LACEBase):
    ##
    # @brief        test_01_plug_unplug() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "HOTPLUG_UNPLUG",
                     "Skip the  test step as athe action type is not hotplug-unplug")
    def test_01_plug_unplug(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: lace enabled and verified successfully")
                        else:
                            logging.error("Fail: Failed to enable and verify Lace")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}"
                            .format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

        # Unplug External display and verifying LACE Persistence
        if panel.is_lfp is False and panel.is_active:
            if self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                   panel.port_type):
                self.fail("Fail : Fail to unplug the port")

        # Verify the Persistence
        if panel.is_active and panel.connector_port_type != "VIRTUALDISPLAY" and panel.is_lfp:
            if self.check_primary_display(port):
                logging.info("Step_1: get lace")
                if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                            "LEGACY") is False:
                    logging.error("Fail: Failed to enable and verify Lace")
                else:
                    logging.info("Pass: lace enabled and verified successfully")
            else:
                if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, False,
                                                            "LEGACY") is False:
                    self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))
                else:
                    logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(
                        panel.pipe))

        ##
        # plug the display
        gfx_adapter_details = self.config.get_all_gfx_adapter_details()
        display_details_list = self.context_args.test.cmd_params.display_details
        self.plug_display(display_details_list)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.connector_port_type != "VIRTUALDISPLAY" and panel.is_lfp:
                    if self.check_primary_display(port):
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                  panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: lace enabled and verified successfully")
                        else:
                            logging.error("Fail: Failed to enable and verify Lace")

                    else:
                        if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, False,
                                                                    "LEGACY") is False:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

                        else:
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}"
                            .format(panel.pipe))

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
                ##
                # Store the current mode
                current_mode = self.config.get_current_mode(panel.display_and_adapterInfo)
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        logging.info("Step_1: get lace")
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, True):
                            logging.info("Pass: lace enabled and verified successfully")
                        else:
                            logging.error("Fail: Failed to enable and verify Lace")

                        mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, random.choice(scaling))
                        # Mode_list should not be None for mode switch scenario. hardcoded to enum.MDS
                        if mode_list is None:
                            mode_list = get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                        for mode in mode_list:
                            apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                       mode.scaling)

                            # verify_lace_feature
                            if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                        "LEGACY") is False:
                                self.fail("Lace verification failed")

                            ##
                            # switch back to the previous current mode
                            apply_mode(panel.display_and_adapterInfo, current_mode.HzRes, current_mode.VtRes,
                                       current_mode.refreshRate, current_mode.scaling)

                            # Verify the registers
                            if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                        "LEGACY") is False:
                                self.fail("Lace verification failed")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info(
                                "Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(
                                    panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: COnfigure Lace and verify the persistence with display events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
