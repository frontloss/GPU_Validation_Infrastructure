########################################################################################################################
# @file         pnp_id_panel_detection_base.py
# @brief        Contains base class for all PNP ID class
# @author       Tulika, Simran Setia
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import display_power, cmd_parser, display_essential
from Libs.Core import driver_escape
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.vbt.vbt import Vbt
from Tests.LFP_Common.PnpIdPanelDetection import pnp_id_panel_detection as pnp_id_lib
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut, workload
from registers.mmioregister import MMIORegister


##
# @brief        This class contains test to set Panel FF and PNP ID to validate feature in VBT.

class PnpIdPanelDetectionBase(unittest.TestCase):
    cmd_line_param = None
    test_expected_ftr_list = None
    vbt_panel_index = None
    test_supported_ftr_list = ['PSR', 'DPST', 'LACE', 'DRRS', 'DMRRS']
    initial_vbt_status = {'PSR': None, 'DPST': None, 'LACE': None, 'DRRS': None, 'DMRRS': None}
    final_vbt_status = {'PSR': None, 'DPST': None, 'LACE': None, 'DRRS': None, 'DMRRS': None}

    display_power_ = display_power.DisplayPower()
    machine_info = SystemInfo()
    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This method initializes and prepares the setup required for execution of tests in this class
    # @details      It parses the command line checks for eDP connections and sets display configuration
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: PNP ID BASED PANEL DETECTION".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + [
            '-VBT_PANEL_INDEX', '-FEATURE_VBT'])

        if cls.cmd_line_param['VBT_PANEL_INDEX'] != 'NONE':
            cls.vbt_panel_index = int(cls.cmd_line_param['VBT_PANEL_INDEX'][0])
            if 0 < cls.vbt_panel_index < 17 is False:
                assert False, f"Invalid VBT Panel Index. Expected= (1 to 16), Actual= {cls.vbt_panel_index}"

        if cls.cmd_line_param['FEATURE_VBT'] != 'NONE':
            cls.test_expected_ftr_list = (cls.cmd_line_param['FEATURE_VBT'])

        dut.prepare()

    ##
    # @brief        This method checks for LFP panel and validates panel caps
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                logging.info(f"\t\t{panel.psr_caps}")
                logging.info(f"\t\t{panel.drrs_caps}")
                logging.info(f"\t\t{panel.lrr_caps}")

    ##
    # @brief        This method will set FF, set the PNP ID in VBT and can enable/disable the feature accordingly
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_prepare_test(self):
        match_found = None
        for adapter in dut.adapters.values():
            gfx_vbt = Vbt(adapter.gfx_index)
            if gfx_vbt.version < 228:
                self.fail("FAIL: VBT version not supported")

            for panel in adapter.panels.values():
                # Take panel index to apply FF
                panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

                if panel_index != 255:
                    logging.info(f"Step: Set Panel FF in VBT {panel.port}")
                    gfx_vbt.block_40.PanelType = 255

            if gfx_vbt.apply_changes() is False:
                self.fail("FAIL: Failed to apply panel FF")
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                self.fail("FAIL: Failed to restart display driver after VBT update")
            gfx_vbt.reload()

            do_driver_restart = False
            for panel in adapter.panels.values():
                # Case 1: If both VBT panel index and feature are None, iterate through all the index in VBT,
                #         find the matching index else fallback to the vbt panel index 1,
                #         set PNP ID in panel index 1, read the feature status in VBT and validate in driver
                if self.test_expected_ftr_list is None and self.vbt_panel_index is None:
                    for panel_index in range(0, 16):
                        match_found = pnp_id_lib.is_pnp_id_matching(panel, panel_index)
                        if match_found is False:
                            self.fail(f"No Match found for PNP ID in VBT Panel Index: {panel_index} and {panel.port}")

                        if match_found is True:
                            self.vbt_panel_index = panel_index
                            logging.debug(f"\tVBT panel index: {self.vbt_panel_index}")
                            break

                    if match_found is None:
                        self.vbt_panel_index = 1

                    if pnp_id_lib.update_vbt_pnp_id(adapter, panel, self.vbt_panel_index) is False:
                        self.fail(f"FAIL: Failed to set PNP ID in {self.vbt_panel_index}")

                    self.initial_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, self.test_supported_ftr_list, self.vbt_panel_index, self.initial_vbt_status)

                    if get_feature_status is False:
                        self.fail(f"Get feature status failed")

                # Case 2: If feature is None, based on the VBT panel index, get the feature status (no feature
                #         enable/disable required) for all the features and validate in driver
                elif self.test_expected_ftr_list is None:
                    if pnp_id_lib.update_vbt_pnp_id(adapter, panel, self.vbt_panel_index) is False:
                        self.fail(f"FAIL: Failed to set PNP ID in {self.vbt_panel_index} ")

                    self.initial_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, self.test_supported_ftr_list, self.vbt_panel_index, self.initial_vbt_status)

                    if get_feature_status is False:
                        self.fail(f"Get feature status failed")

                # Case 3: If VBT panel index is None, iterate through all the index in VBT, find the matching index else
                #         fallback to vbt panel index 1,set PNP ID in 1,modify the given features and validate in driver
                elif self.vbt_panel_index is None:
                    for panel_index in range(0, 16):
                        match_found = pnp_id_lib.is_pnp_id_matching(panel, panel_index)
                        if match_found is False:
                            self.fail(
                                f"FAILED to find PNP ID match between VBT Panel Index: {panel_index} and {panel.port}")

                        if match_found is True:
                            self.vbt_panel_index = panel_index
                            logging.debug(f"\tVBT panel index: {self.vbt_panel_index}")
                            break

                    if match_found is None:
                        self.vbt_panel_index = 1
                        if pnp_id_lib.update_vbt_pnp_id(adapter, panel, self.vbt_panel_index) is False:
                            self.fail(f"FAIL: Failed to set PNP ID in {self.vbt_panel_index}")

                    self.initial_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, self.test_expected_ftr_list, self.vbt_panel_index, self.initial_vbt_status)

                    if get_feature_status is False:
                        self.fail("Get feature status failed for")

                    status, restart_status = pnp_id_lib.enable_feature(
                        adapter, self.test_expected_ftr_list, self.vbt_panel_index, self.initial_vbt_status)
                    if status is False:
                        self.fail("feature enabling failed")
                    do_driver_restart |= restart_status

                    disable_feature = set(self.test_supported_ftr_list) - set(self.test_expected_ftr_list)

                    self.initial_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, disable_feature, self.vbt_panel_index, self.initial_vbt_status)

                    if get_feature_status is False:
                        self.fail("Get feature status failed")

                    status, restart_status = pnp_id_lib.disable_feature(
                        adapter, disable_feature, self.vbt_panel_index, self.initial_vbt_status)
                    if status is False:
                        self.fail("feature disabled failed")
                    do_driver_restart |= restart_status

                    if do_driver_restart is True:
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            self.fail("Failed to restart display driver after VBT update")
                        gfx_vbt.reload()

                    self.final_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, self.test_supported_ftr_list, self.vbt_panel_index, self.final_vbt_status)

                    if get_feature_status is False:
                        self.fail("Get feature status failed")

                # Case 4: If both VBT panel index and feature are given, set the PNP ID in the given VBT panel index,
                #         enable the given feature, disable the rest and validate in driver
                else:
                    if pnp_id_lib.update_vbt_pnp_id(adapter, panel, self.vbt_panel_index) is False:
                        self.fail(f"FAIL: Failed to set PNP ID in {self.vbt_panel_index}")

                    self.initial_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, self.test_expected_ftr_list, self.vbt_panel_index, self.initial_vbt_status)
                    if get_feature_status is False:
                        self.fail("Get feature status failed")

                    status, restart_status = pnp_id_lib.enable_feature(
                        adapter, self.test_expected_ftr_list, self.vbt_panel_index, self.initial_vbt_status)
                    if status is False:
                        self.fail("feature enabling failed")
                    do_driver_restart |= restart_status

                    disable_feature = set(self.test_supported_ftr_list) - set(self.test_expected_ftr_list)
                    self.initial_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, disable_feature, self.vbt_panel_index, self.initial_vbt_status)
                    if get_feature_status is False:
                        self.fail("Get feature status failed")

                    status, restart_status = pnp_id_lib.disable_feature(
                        adapter, disable_feature, self.vbt_panel_index, self.initial_vbt_status)
                    if status is False:
                        logging.error("feature disabled failed")
                    do_driver_restart |= restart_status

                    if do_driver_restart is True:
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            self.fail("Failed to restart display driver after VBT update")
                        gfx_vbt.reload()

                    self.final_vbt_status, get_feature_status = pnp_id_lib.get_feature_status(
                        adapter, self.test_supported_ftr_list, self.vbt_panel_index, self.final_vbt_status)
                    if get_feature_status is False:
                        self.fail("Get feature status failed")

        logging.info(f"Initial VBT Status= {self.initial_vbt_status}")
        logging.info(f"Final VBT Status= {self.final_vbt_status}")

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function will check the feature status in driver
    # @param[in]    feature
    # @return       status, True if feature enabled in driver, else False
    @staticmethod
    def verify_feature_status(feature):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if feature == 'DRRS':
                    logging.info(f"Step: Validating DRRS in driver for {panel.port}")
                    # For enabling DRRS, disable PSR in LRR2.0/LRR2.5 supported panel
                    if panel.lrr_caps.is_lrr_2_0_supported or panel.lrr_caps.is_lrr_2_5_supported:
                        psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                        if psr_status is True:
                            status, reboot_required = display_essential.restart_gfx_driver()
                    etl_file, _ = workload.run(workload.IDLE_DESKTOP, [30])
                    status &= drrs.verify(adapter, panel, etl_file)
                    logging.debug(f"\tDRRS status verification: {bool(status)}")
                    if panel.lrr_caps.is_lrr_2_0_supported or panel.lrr_caps.is_lrr_2_5_supported:
                        logging.info("Enabling PSR back after test")
                        psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                        if psr_status is True:
                            result, reboot_required = display_essential.restart_gfx_driver()
                            if result is False:
                                logging.error("FAILED ot restart driver")
                                return False

                if feature == 'DMRRS':
                    logging.info(f"Step: Validating DMRRS in driver for {panel.port}")
                    etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [dmrrs.MediaFps.FPS_24_000, 30])
                    status &= dmrrs.verify(adapter, panel, etl_file, dmrrs.MediaFps.FPS_24_000)
                    logging.debug(f"\tDMRRS status verification: {bool(status)}")

                if feature == 'PSR':
                    logging.info(f"Step: Validating PSR in driver for {panel.port}")
                    if panel.psr_caps.is_psr2_supported:
                        psr2_register_instance = MMIORegister.read("PSR2_CTL_REGISTER",
                                                                   "PSR2_CTL_" + panel.transcoder,
                                                                   adapter.name)
                        element_value = psr2_register_instance.__getattribute__(str("psr2_enable"))
                        logging.debug("PSR2_CTL_" + panel.transcoder + ":{}".format(element_value))
                        status &= bool(element_value)
                        logging.debug(f"\tPSR status verification: {bool(status)}")
                    else:
                        logging.error("Panel does not support PSR2")

                if feature == 'DPST':
                    logging.info(f"Step: Validating DPST in driver for {panel.port}")
                    display_power_ = display_power.DisplayPower()
                    if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
                        logging.error("Failed to switch powerline to DC")
                        status &= False
                    else:
                        logging.debug(f"\tPower line state : {display_power_.get_current_powerline_status()}")
                        dpst_etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL)
                        status &= dpst.verify(adapter, panel, dpst_etl_file)
                        logging.debug(f"\tDPST status verification: {bool(status)}")

                if feature == 'LACE':
                    logging.info(f"Step: Validating LACE in driver for {panel.port}")
                    if PnpIdPanelDetectionBase.final_vbt_status[feature] is False:
                        if driver_escape.als_aggressiveness_level_override(panel.target_id, 551, True) is False:
                            logging.error(f"Driver escape for aggressiveness failed for feature {feature}")
                            status &= False
                        else:
                            time.sleep(2)
                            status &= pc_external.get_lace_status(adapter, panel)
                    else:
                        if driver_escape.als_aggressiveness_level_override(panel.target_id, 10000, True) is False:
                            logging.error(f"Driver escape for aggressiveness failed for feature {feature}")
                            status &= False
                        else:
                            time.sleep(2)
                            status &= pc_external.get_lace_status(adapter, panel)
                    logging.debug(f"\tLACE status verification: {bool(status)}")
        return bool(status)

    ##
    # @brief        This function validates PNP ID and feature status in driver
    # @return       None
    @staticmethod
    def validate_feature(self):
        validate_status = True
        feature_failed = []
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # Case 1 & 2: If feature is not passed, get the feature status for all the features and validate in driver
                if self.test_expected_ftr_list is None:
                    for feature in self.test_supported_ftr_list:
                        status = self.verify_feature_status(feature)
                        if self.initial_vbt_status[feature] == status:
                            logging.info(f"PASS: {feature} {'Enabled' if status else 'Disabled'} in driver".center(
                                common.MAX_LINE_WIDTH, "-"))
                        else:
                            logging.error(f"{feature} status check failed in driver")
                            validate_status &= False
                            feature_failed.append(feature)

                # Case 3 & 4:  Feature passed in the command line will be enabled and the rest will be disabled
                else:
                    # Case a: Validate the feature status passed in the command line
                    for feature in self.test_expected_ftr_list:
                        status = self.verify_feature_status(feature)
                        if self.initial_vbt_status[feature] is False and self.final_vbt_status[feature] is False:
                            logging.error(f"{feature} feature toggle failed in VBT")
                            validate_status &= False
                            feature_failed.append(feature)
                        elif status is False:
                            logging.error(f"{feature} status check failed in driver")
                            validate_status &= False
                            feature_failed.append(feature)
                        else:
                            logging.info(f"PASS: {feature} Enabled in driver".center(common.MAX_LINE_WIDTH, "-"))

                    # Case b: Validate the feature status which are not passed in the command line
                    for feature in (set(self.test_supported_ftr_list) - set(self.test_expected_ftr_list)):
                        status = self.verify_feature_status(feature)
                        if self.initial_vbt_status[feature] is True and self.final_vbt_status[feature] is True:
                            logging.error(f"{feature} feature toggle failed in VBT")
                            validate_status &= False
                            feature_failed.append(feature)
                        elif status is True:
                            logging.error(f"{feature} status check failed in driver")
                            validate_status &= False
                            feature_failed.append(feature)
                        else:
                            logging.info(f"PASS: {feature} Disabled in driver".center(common.MAX_LINE_WIDTH, "-"))

                if validate_status is False:
                    self.fail(f"FAIL: PNP ID test failed for {feature_failed}")

    ##
    # @brief        This function logs the teardown phase
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: PNP ID BASED PANEL DETECTION ".center(common.MAX_LINE_WIDTH, "*"))
        logging.info("Test Cleanup Completed")

        dut.reset()
        vbt = Vbt()
        if vbt.reset() is False:
            assert False, "Failed to restore VBT from driver"
        logging.info("Successfully restored VBT from driver")
        status, reboot_required = display_essential.restart_gfx_driver()
        assert status, "Failed to restart driver"
        logging.info("Successfully restarted driver")
