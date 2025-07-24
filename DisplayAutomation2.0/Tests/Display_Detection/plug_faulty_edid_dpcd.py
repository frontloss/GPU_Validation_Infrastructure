########################################################################################################################
# @file         plug_faulty_edid_dpcd.py
# @brief        This script tests Display detection and modeset during the plug of EDIDs with Violations
# @details      Plugs the custom EDIDs with violations, and checks for driver's graceful exit in such cases
# @author       Veena Veluru
########################################################################################################################
import logging
import os
import sys
import time
import unittest
from xml.etree import ElementTree as ET

from Libs.Core import cmd_parser, reboot_helper
from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Detection.display_hpd_base import *
from Libs.Core.test_env import test_context


##
# @brief        PlugFaultyEDIDDPCD base class to be used in Plug_faulty_edid_dpcd tests
class PlugFaultyEDIDDPCD(unittest.TestCase):
    status = True
    status_list = []
    panel_index_list = []
    case_list = []
    adapter_list = []
    cmd_line_param = []
    input_display_list = []
    preferred_mode_list = []
    display_and_adapter_info = []
    panel_index = {}
    prune_mode_dict = {}
    display_engine = DisplayEngine()
    config = display_config.DisplayConfiguration()

    scale_dict = {'Unsupported': 0, 'CI': 1, 'FS': 2, 'MAR': 4, 'CAR': 8, 'MDS': 64}

    ##
    # @brief        setup function. Parse displays to plug from cmdline params
    # @return       None
    def setUp(self):
        logging.debug("Entry: setUpClass")
        cmdline_args = sys.argv

        # Parse the commandline params
        self.cmd_line_param = cmd_parser.parse_cmdline(cmdline_args)

        if type(self.cmd_line_param) is not list:
            self.cmd_line_param = [self.cmd_line_param]

        # input_display_list[] is a list of Port Names from user args
        for param in self.cmd_line_param:
            cmd_line_param_adapter = param
            for key, value in cmd_line_param_adapter.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if self.input_display_list.__contains__(value['connector_port']):
                            adapter = self.adapter_list[self.input_display_list.index(value['connector_port'])]
                        if not self.input_display_list.__contains__(value['connector_port']) or (
                                self.input_display_list.__contains__(value['connector_port']) and adapter != value[
                            'gfx_index']):
                            if (value['gfx_index'] == None):
                                value['gfx_index'] = 'gfx_0'
                            self.adapter_list.insert(value['index'], str(value['gfx_index']).lower())
                            self.input_display_list.insert(value['index'], value['connector_port'])
                            self.panel_index[str(value['gfx_index']).lower() + "_" + value['connector_port']] = value[
                                'panel_index']

        logging.info(
            "Test Flow : Plug and UnPlug given EDIDs from XML in order on respective ports mentioned in cmdline")
        logging.info("Current Display Config Topology : {}".format(self.config.get_current_display_configuration_ex()))
        logging.debug("Exit: setUpClass")

    ##
    # @brief        unittest to test the plug
    # @details      Plugs and unplugs every EDID from faulty_edid_dpcd_list xml, on the display port in cmdline
    # @return       None
    def test_edid_violations(self):
        logging.debug("Entry: test_edid_violations()")
        for display_port, gfx_index in zip(self.input_display_list, self.adapter_list):
            # Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display".format(display_port))
                continue

            # populate EDIDs, DPCDs and panel indices to plug into respective lists
            self.get_displays_to_plug(display_port)

            # for each EDP/DP/HDMI plugged, verify driver behavior in case of each faulty EDID plugged
            for each_display, case, preferred_res in zip(self.panel_index_list, self.case_list,
                                                         self.preferred_mode_list):
                self.status = True
                logging.info("******Entered Case {}******".format(str(case).upper()))
                # plug the display, set display config and verify
                self.plug_set_config_verify(display_port, each_display, gfx_index, case)
                if not ("HDMI" in display_port and case in ['header_mismatch', 'base_checksum_mismatch', 'edid_rev_mismatch',
                                  'edid_version_mismatch']):
                    if self.status:
                        # get current mode to verify in case of single display configuration source mode should be same
                        # as transcoder timing given by get_display_timings() below
                        source_mode = self.config.get_current_mode(self.display_and_adapter_info)

                        # get Display timings to verify
                        current_mode = self.config.get_display_timings(self.display_and_adapter_info)

                        # Below Violation conditions are in extension block, driver is expected to pass the EDID read and
                        # take the panel info from base EDID
                        if case in ['ext_block_mismatch_1', 'ext_block_mismatch_2', 'ext_checksum_mismatch',
                                    'range_limits_inclusion_violation', 'feature_support_not_set_1',
                                    'feature_support_not_set_2', 'feature_support_not_set_3']:
                            # case ext_block_mismatch_1: No of Extension Blocks in the EDID are wrongly reported(Actual- 0 blocks; reported- 1 block )
                            # case ext_block_mismatch_2: No of Extension Blocks in the EDID are wrongly reported(Actual- 2 blocks; reported- 1 block )
                            # case ext_checksum_mismatch: Checksum of the extension block is incorrect
                            # range_limits_inclusion_violation: Range Limits not present in the BASE EDID and bit0 of feature support byte is 1
                            # feature_support_not_set_1: video timing supported is Default GTF, but feature support bit is 0
                            # feature_support_not_set_2: video timing supported is Secondary GTF, but feature support bit is 0
                            # feature_support_not_set_3: video timing supported is CVT, but feature support bit is 0

                            # Preferred mode of planned EDID has to be fed in the xml, driver is expected to apply
                            # preferred mode despite the violation in EDID
                            if str(current_mode.hActive) == preferred_res[0] and str(current_mode.vActive) == \
                                    preferred_res[1]:
                                logging.info(
                                    "PASS: Case {}: Base EDID Read passed, Driver able to apply preferred "
                                    "mode {} X {}".format(str(case).upper(), current_mode.hActive,
                                                          current_mode.vActive))

                                if str(source_mode.HzRes) != preferred_res[0] and str(source_mode.VtRes) != \
                                        preferred_res[
                                            1]:
                                    logging.warning("WARN: Source mode is not preferred mode, Scaling got enabled")
                                # for Extension block checksum mismatch case, skipping DE Verification
                                if case not in ['ext_checksum_mismatch', 'ext_block_mismatch_1',
                                                'ext_block_mismatch_2']:
                                    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
                                    platform = adapter_info.get_platform_info().PlatformName.upper()

                                    enum_display_list = self.config.get_enumerated_display_info()
                                    ports = []
                                    for i in range(enum_display_list.Count):
                                        connector_port = CONNECTOR_PORT_TYPE(
                                            enum_display_list.ConnectedDisplays[i].ConnectorNPortType).name
                                        if enum_display_list.ConnectedDisplays[i].IsActive and \
                                                enum_display_list.ConnectedDisplays[
                                                    i].DisplayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index:
                                            ports.append(connector_port)
                                    if bool(ports):
                                        # Skip DVFS verification if not enabled in below platforms
                                        if platform in ['MTL']:
                                            logging.info(f"Verifying Voltage Level notified to PCode for {platform}")
                                            if display_clock.DisplayClock.verify_voltage_level_notified_to_pcode(
                                                    gfx_index, ports) is False:
                                                logging.error(f"FAIL: DVFS VoltageLevel verification failed for {ports}"
                                                              f" on {gfx_index}")
                                                gdhm.report_driver_bug_pc(
                                                    "[Interfaces][Display_Engine][CD Clock] Failed to verify "
                                                    "Voltage level during plug of faulty EDID/DPCD",
                                                    gdhm.ProblemClassification.FUNCTIONALITY)
                                            else:
                                                logging.info("PASS: DVFS VoltageLevel verification successful")
                                        else:
                                            logging.warning(f"Skipping DVFS VoltageLevel verification for unsupported "
                                                            f"platform : {platform}.")
                                    else:
                                        logging.warning(
                                            f"No displays connected in {platform}. Skipping DVFS verification!")

                                    # verify display engine
                                    self.status = self.status and self.display_engine.verify_display_engine(
                                        gfx_index=gfx_index)

                                if case == 'ext_block_mismatch_2':
                                    # Apply a mode from the pruned extension block and check if it is not getting set
                                    if self.prune_mode_dict[each_display] is not None:
                                        mode = DisplayMode()
                                        target_id = self.config.get_target_id(display_port, gfx_index=gfx_index)
                                        mode.targetId = target_id
                                        mode.HzRes = int(self.prune_mode_dict[each_display][0])
                                        mode.VtRes = int(self.prune_mode_dict[each_display][1])
                                        mode.refreshRate = int(self.prune_mode_dict[each_display][2])
                                        mode.BPP = 4  # Assuming RGB888
                                        mode.rotation = 1
                                        mode.scanlineOrdering = 1
                                        mode.scaling = self.scale_dict[self.prune_mode_dict[each_display][3]]
                                        if self.config.set_display_mode([mode], virtual_mode_set_aware=False) is False:
                                            logging.info("PASS: Mode not applied. Extension Block successfully Pruned")
                                        else:
                                            logging.error("FAIL: Mode in extension Block got applied, Block not pruned")
                                            self.status = False

                            elif str(current_mode.hActive) == '1920' and str(current_mode.vActive) == '1080':
                                self.status = False
                                logging.error(
                                    "FAIL: Case {}: EDID Read failed, Driver not considering "
                                    "Base Block".format(case))
                            else:
                                self.status = False
                                logging.error(
                                    "FAIL: Case {}: Mode applied is not Preferred: Applied: {} X {} Preferred: {} X {}".format(
                                        case, current_mode.hActive,
                                        current_mode.vActive, preferred_res[0], preferred_res[1]))

                        # Below Violation conditions are in Base block, driver is expected to fail the EDID read and set
                        # default resolution 1920x1080
                        elif case in ['header_mismatch', 'base_checksum_mismatch', 'edid_rev_mismatch',
                                      'edid_version_mismatch']:
                            # case header_mismatch: Header is incorrect
                            # case base_checksum_mismatch: Checksum of the base block is incorrect
                            # case edid_rev_mismatch: EDID revision is incorrect
                            # case edid_version_mismatch: EDID version is incorrect

                            if str(current_mode.hActive) == '1920' and str(current_mode.vActive) == '1080':
                                logging.info(
                                    "PASS: Case {} - EDID Read failed as expected,EDID Read failed and driver brought up "
                                    "display with 1920x1080 mode as expected".format(
                                        str(case).upper()))
                            else:
                                self.status = False
                                logging.error("FAIL: Case {}: EDID Read is expected to fail and driver is supposed to "
                                              "bring up display with 1920X1080. But resolution found is {} X {}".format(
                                    case, current_mode.hActive, current_mode.vActive))
                        else:
                            self.status = False
                            logging.error("FAIL: Invalid EDID Violation Case - {}".format(case))
                    else:
                        logging.error("FAIL: Case {} - Plug and Verify Modeset failed".format(case))

                    # unplug the plugged display
                self.unplug_verify(display_port, gfx_index)
                self.status_list.append(self.status)

            time.sleep(10)

        logging.info("Status List for all unit tests: {}".format(self.status_list))
        if False in self.status_list:
            self.fail("Test EDID Violations Failed")
        logging.debug("Exit: test_edid_violations()")

    ##
    # @brief        Parse aulty_edid_dpcd_list.xml and get panel index to plug
    # @param[in]    display_port display to plug
    # @return       None
    def get_displays_to_plug(self, display_port):
        display_list = []
        # Parse XML file
        tree = ET.parse("Tests\Display_Detection\edid_config_xmls\Faulty_edid_dpcd_list.xml")
        display_list_root = tree.getroot()
        if str(display_port).__contains__('DP_'):
            display_list = display_list_root.find('DP')
        elif str(display_port).__contains__('HDMI_'):
            display_list = display_list_root.find('HDMI')
        else:
            logging.error("FAIL: Invalid Display {} pass to the test".format(display_port))
        for display in display_list:
            self.panel_index_list.append(display.get('panelindex'))
            self.case_list.append(display.get('case'))
            preferred_res = (display.get('hzRes'), display.get('vtRes'))
            self.preferred_mode_list.append(preferred_res)
            if 'hzRes1' in display.attrib and 'vtRes1' in display.attrib:
                self.prune_mode_dict[display.get('panelindex')] = (
                    display.get('hzRes1'), display.get('vtRes1'), display.get('rr1'), display.get('scaling1'))

    ##
    # @brief Plug the specified panel, set config and verify
    # @param[in] display_port display to plug
    # @param[in] panel_index panel index of the display
    # @param[in] gfx_index graphics adapter
    # @param[in] case of EDID
    # @return  None
    def plug_set_config_verify(self, display_port, panel_index, gfx_index='gfx_0', case = None):
        self.status = True
        logging.info(" Plugging Display {} on {}".format(display_port, gfx_index))
        # plug the display
        if not display_utility.plug(port=display_port, panelindex=panel_index, gfx_index=gfx_index):
            self.status = False

        # In case of HDMI if EDID read fails display enumeration will not happen with Fake EDID
        if ("HDMI" in display_port and case in ['header_mismatch', 'base_checksum_mismatch', 'edid_rev_mismatch',
                                                    'edid_version_mismatch']):
            logging.info("Skipping {} verification for HDMI Panels.".format(case))
            self.status = True
            return
        else:
            # set display config
            self.display_and_adapter_info = self.config.get_display_and_adapter_info_ex(display_port, gfx_index)
            if self.config.set_display_configuration_ex(enum.SINGLE, [self.display_and_adapter_info]) is False:
                logging.error("FAIL: SetDisplayConfigurationEX returned false")
        # Check if panel came active or not by checking panel timings
        _driver_interface = driver_interface.DriverInterface()
        adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
        self.status = self.status and _driver_interface.is_panel_timings_non_zero(adapter_info, display_port)

        # Verify Plugged Display is enumerated
        if self.status:
            time.sleep(15)
            enumerated_displays = self.config.get_enumerated_display_info()
            logging.debug("Enumerated Display Information: {}".format(enumerated_displays.to_string()))
            if display_config.is_display_attached(enumerated_displays, display_port, gfx_index) is True:
                logging.info("Plug of {} successful on {}".format(display_port, gfx_index))
                self.status = self.status and True
            else:
                self.status = False
                logging.error(" Display not Enumerated. Plug of {} failed on {}".format(display_port, gfx_index))
        else:
            self.status = False
            logging.error("Panel timing is zero. Plug of {} failed on {}".format(display_port, gfx_index))

    ##
    # @brief        Unplug the panel and verify
    # @param[in]    display_port display to plug
    # @param[in]    gfx_index graphics adapter
    # @return       None
    def unplug_verify(self, display_port, gfx_index='gfx_0'):
        if not display_utility.unplug(port=display_port, gfx_index=gfx_index):
            self.status = False
        enumerated_displays = self.config.get_enumerated_display_info()

        if display_config.is_display_attached(enumerated_displays, display_port, gfx_index) is False:
            logging.info("Unplug of {} successful on {}".format(display_port, gfx_index))
        else:
            logging.error("FAIL: Display still attached. Unplug of {} failed on {}".format(display_port, gfx_index))
            self.status = False
        # Exception for Platforms [DG2,DG1, ELG and CLS]
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        platform = adapter_info.get_platform_info().PlatformName.upper()
        if platform in ['DG1', 'DG2', 'ELG', 'CLS']:
            logging.warning(
                "WARN: Display {} reported as still Attached. Sometimes OS doesnot update Unplug Status for last display, in case where "
                "Virtual Display not plugged by driver. Ignoring unplug status for such cases".format(
                    display_port))
            self.status = True


    ##
    # @brief        teardown function
    # @details      Unplugs all the displays connected in the test
    # @return       None
    def tearDown(self):
        logging.debug("ENTRY: TearDown")

        # Unplug all EFP displays
        logging.debug("Unplugging all Displays")
        enum_display_list = self.config.get_enumerated_display_info()

        for count in range(enum_display_list.Count):
            connector_port = CONNECTOR_PORT_TYPE(enum_display_list.ConnectedDisplays[count].ConnectorNPortType).name
            gfx_index = enum_display_list.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in [
                display_utility.VbtPanelType.LFP_DP,
                display_utility.VbtPanelType.LFP_MIPI] and connector_port not in [
                'DispNone', 'VIRTUALDISPLAY']:
                    self.unplug_verify(connector_port, gfx_index=gfx_index)

        logging.info("Test Completed")
        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PlugFaultyEDIDDPCD'))
    TestEnvironment.cleanup(outcome)
