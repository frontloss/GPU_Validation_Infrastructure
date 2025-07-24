########################################################################################################################
# @file         configure_lfp.py
# @brief        Usage:
#               To configure lfp display:
#                   configure_lfp.py -TEST [entire test command line]
#
# @note         We are restricting LFP ports simulation for Port_A and Port_B
# @author       Sri Sumanth Geesala, Rohit Kumar
########################################################################################################################

import logging
import os
import sys
import unittest
from xml.etree import ElementTree

from Libs import env_settings
from Libs.Core import cmd_parser, display_utility, reboot_helper, system_utility, driver_escape, gfx_assistant
from Libs.Core import display_essential
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.sw_sim import gfxvalsim
from Libs.Core.test_env import test_context, test_environment
from Libs.Core.vbt import vbt, vbt_context
from Libs.Core.wrapper.valsim_args import GfxPchFamily
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

DE_HPD_INTERRUPT_2 = 0x44478
MAX_LFP_COUNT = 2

##
# All simulated eDP EDIDs have serial abc1230. Byte representation of 'ab' 'c1' '23' '00' in reverse
SIMULATED_EDP_SERIAL = [0x00, 0x23, 0xC1, 0xAB]

# List of DPCD offsets that should be checked for 'is_same_panel' condition. All the values should match.
DPCD_CAPS_OFFSETS = [
    0x007, 0x310, 0x311, 0x312, 0x313,  # VRR caps
    0x02E, 0x070,  # PSR caps
    0x314,  # LRR caps
]
DPCD_CAPS_OFFSETS += list(range(0x340, 0x356))  # HDR & B3 caps
DPCD_CAPS_OFFSETS += list(range(0x060, 0x070))  # VDSC caps 60h to 6Fh


##
# @brief        ConfigureLfp Class
class ConfigureLfp(unittest.TestCase):
    system_utility_ = None
    display_config_ = None
    driver_interface_ = None
    param_list = {}  # Contains adapter wise display parameters {'gfx_0': {'DP_A': {'edid_name':''}}}
    requested_lfp_list = {}  # Contains adapter wise LFP list. {'gfx_0': ['DP_A']}
    platform_info = {}

    ##
    # @brief        Constructor
    # @param[in]   args command line arguments used to fill the instance members
    # @param[in]   kwargs keyword arguments used to fill the instance members
    def __init__(self, *args, **kwargs):
        super(ConfigureLfp, self).__init__(*args, **kwargs)

        self.system_utility_ = system_utility.SystemUtility()
        self.display_config_ = display_config.DisplayConfiguration()
        self.driver_interface_ = driver_interface.DriverInterface()

        self.platform_info = {
            gfx_index: {
                'gfx_index': gfx_index,
                'name': adapter_info.get_platform_info().PlatformName,
                'pch': GfxPchFamily(self.driver_interface_.get_platform_details(gfx_index).GfxPchFamily)
            }
            for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
        }

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        Setup method
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self) -> None:
        # Clear GDHM report (if any)
        gdhm.clear_report()

        for i, o in enumerate(sys.argv):
            if o.lower() == "-gas_id":
                gfx_assistant.add_simulation_files(test_context.TestContext.panel_input_data(), sys.argv[i + 1])
                break

        ##
        # prepare_display_setup.py takes entire command line as input, which includes all the custom tags present in the
        # command line. The command line parser asks to define custom tags beforehand. Hence, we need to pass all the
        # custom tags present in command line to parse_cmdline() API.
        custom_tags = cmd_parser.get_custom_tag()

        self.cmd_params = cmd_parser.parse_cmdline(sys.argv, custom_tags)

        # Handle multi-adapter scenario
        if not isinstance(self.cmd_params, list):
            self.cmd_params = [self.cmd_params]

        # Get display list, display parameters, LFPs, EFPs for each platform
        for platform in self.platform_info.values():
            adapter = platform['gfx_index']  # gfx_0

            # cmd_params contain adapter parameters based on index. index 0 represents parameters for gfx_0
            # Using the same to get display parameters for given adapter and display
            # See parse_cmdline() API in cmd_parser module for more info
            # param_list = {'gfx_0': {'DP_A': {'index': 0, 'edid_name': '', ...}}, 'gfx_1': {'HDMI_C': {...}, ...}}
            self.param_list[adapter] = {}
            self.requested_lfp_list[adapter] = []
            for display, params in self.cmd_params[int(adapter[-1])].items():
                if cmd_parser.display_key_pattern.match(display) is None:
                    continue
                display = '_'.join(display.split('_')[:2])
                if 'EDP' in display:
                    display = display[1:]

                self.param_list[adapter][display] = params
                if params['is_lfp'] is True:
                    self.requested_lfp_list[adapter].append(display)

        # Validate if LFP simulation flag present in config.ini
        force_lfp_tag = env_settings.get('SIMULATION', 'lfp_simulation')
        if any(self.requested_lfp_list.values()) and force_lfp_tag != 'ENABLE':
            gdhm.report_bug(
                f"[ConfigureLfp] LFP port requested for simulation, but LFP simulation is disabled in config.ini",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            self.fail(
                f'LFP port requested for simulation, but LFP simulation is disabled in config.ini')

    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        # @note WA for ValSim plug/unplug. If pre-si yangra, write 0x0 to 0x44478. Only after this register is reset
        # to 0x0 ValSim plug/unplug will work in pre-si yangra.
        if self.system_utility_.get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            for platform in self.platform_info.values():
                if self.driver_interface_.mmio_write(DE_HPD_INTERRUPT_2, 0x0, gfx_index=platform['gfx_index']) is False:
                    logging.error(f"Failed to write DE_HPD_INTERRUPT_2({hex(DE_HPD_INTERRUPT_2)}) "
                                  f"for {platform['name']}")
                else:
                    logging.info(f"DE_HPD_INTERRUPT_2({hex(DE_HPD_INTERRUPT_2)}) register offset is reset to 0x0 "
                                 f"for {platform['name']}")

        # Prepare_Display script should not fail due to UnderRun/TDR issue, it will be logged as warning.
        # UnderRun/TDR occurred during prepare display will be reported and tracked through gdhm.

        # Verify UnderRun and Clear underrun registry so that it will not fail during Test Environment cleanup
        UnderRunStatus.verify_underrun()
        UnderRunStatus.clear_underrun_registry()
        UnderRunStatus.skip_underrun_check = True
        VerifierCfg.underrun = Verify.SKIP
        VerifierCfg.tdr = Verify.SKIP

        # Verify and Clear TDR so that it will not fail during Test Environment cleanup
        for platform in self.platform_info.values():
            display_essential.detect_system_tdr(gfx_index=platform['gfx_index'])

    ##
    # @brief        Runtest Method
    # @return       None
    def runTest(self) -> None:
        is_reboot_required = False

        # Handle MIPI panel simulation
        is_reboot_required |= self.handle_mipi_simulation()

        # Handle eDP simulation if at least one Yangra platform is present
        is_reboot_required |= self.handle_edp_simulation()

        if is_reboot_required and reboot_helper.reboot(self, 'runTest') is False:
            self.fail("Failed to reboot the system")

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        Helper function for handling MIPI panel simulation
    # @return       status - Boolean, True if driver restart is required, False otherwise
    def handle_mipi_simulation(self) -> bool:
        if reboot_helper.is_reboot_scenario():
            # This block will be executed only after reboot
            self.verify_mipi_simulation()
            return False

        # Handle MIPI panel simulation
        is_reboot_required = False
        for platform in self.platform_info.values():
            gfx_index = platform['gfx_index']

            gfx_vbt = vbt.Vbt(gfx_index)
            mipi_ports_requested = [port for port in self.requested_lfp_list[gfx_index] if 'MIPI' in port]
            if len(mipi_ports_requested) == 0:
                continue

            logging.info(f"Step: Simulate requested MIPI(s) on {platform['name']}")

            platform_status = False
            for port in mipi_ports_requested:
                params = self.param_list[gfx_index][port]

                # if 'panel_index' is not passed in cmdline, filling default MIPI PanelIndex.
                if params['panel_index'] is None:
                    if platform['name'] == 'LKF1':
                        # LKF POR panel (contains both block 42 (for vbt_version < 229) and 58 (for vbt_version >= 229))
                        params['panel_index'] = 'MIP001'
                    elif platform['name'] == 'TGL':
                        if gfx_vbt.version < 229:
                            # using LKF POR panel since block 58 not present in VBT version < 229
                            params['panel_index'] = 'MIP001'
                        else:
                            # WA: using LKF panel for TGL since TGL panel has known underrun issue (1608585678).
                            # Change this to MIP005 once issue fixed.
                            params['panel_index'] = 'MIP001'
                            # TGL POR panel. Uses new block 58 for timing data (block 42 not doable for this panel)
                            # params['panel_index'] = 'MIP005'
                    else:
                        params['panel_index'] = 'MIP001'

                panel_index = gfx_vbt.get_lfp_panel_type(port)

                # parse MIPI xml, check if requested MIPI panel is already connected (check based on PnP Id)
                requested_panel_info = display_utility.get_panel_edid_dpcd_info(port, params['panel_index'], True)
                mipi_xml_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, "MIPI", requested_panel_info["edid"])
                if not os.path.exists(mipi_xml_file):
                    self.fail(f"No MIPI xml file present at location {mipi_xml_file}")

                xml_root = ElementTree.parse(mipi_xml_file).getroot()
                mfg_name = product_code = serial_num = week_of_mfg = year_of_mfg = 0
                for field in xml_root.findall('Field'):
                    path = field.find('Path').text
                    value = field.find('Value').text
                    if 'IdMfgName' in path:
                        mfg_name = int(value, 16)
                    if 'IdProductCode' in path:
                        product_code = int(value, 16)
                    if 'IDSerialNumber' in path:
                        serial_num = int(value, 16)
                    if 'WeekOfMfg' in path:
                        week_of_mfg = int(value, 16)
                    if 'YearOfMfg' in path:
                        year_of_mfg = int(value, 16)

                input_panel_pnp_id = str(mfg_name) + str(product_code) + str(serial_num) + str(week_of_mfg)
                input_panel_pnp_id += str(year_of_mfg)

                mfg_name = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].IdMfgName
                product_code = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].IdProductCode
                serial_num = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].IDSerialNumber
                week_of_mfg = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].WeekOfMfg
                year_of_mfg = gfx_vbt.block_42.FlatPanelDataStructureEntry[panel_index].YearOfMfg
                current_panel_pnp_id = str(mfg_name) + str(product_code) + str(serial_num) + str(week_of_mfg)
                current_panel_pnp_id += str(year_of_mfg)

                if input_panel_pnp_id == current_panel_pnp_id:
                    logging.info(f"\tVBT PNP ID is matched for {port}. Verifying Panel enumeration")
                    enumerated_displays = self.display_config_.get_enumerated_display_info()
                    if display_config.is_display_attached(enumerated_displays, port, gfx_index) is False:
                        self.fail(f"Panel is not enumerated on {port}")
                    logging.info(f"\tPanel is enumerated on {port}")
                    continue

                logging.info(f"\tPlugging {params['panel_index']} using {requested_panel_info['edid']} on port {port}")

                # parse MIPI xml, set MIPI panel data in VBT
                for field in xml_root.findall('Field'):
                    block_no = field.find('Block').text
                    path = field.find('Path').text
                    value = field.find('Value').text

                    vbt_expression = 'gfx_vbt.block_' + str(block_no) + '.' + str(path) + ' = ' + str(value)
                    vbt_expression = vbt_expression.replace('{panel_index}', str(panel_index))
                    cur_block = eval('gfx_vbt.block_' + str(block_no))
                    if cur_block is not None:
                        exec(vbt_expression)
                platform_status = True

            if platform_status:
                ################################################################################
                # check with Sumanth if it is required.
                ################################################################################
                # if we are simulating dual link MIPI panel, we have to disable MIPI_C (DSI_1) port,
                # since dual link will internally use both MIPI ports to drive single MIPI display
                self.disable_dual_link_mipi_port(gfx_vbt)
                ################################################################################
                # check with Sumanth if it is required.
                ################################################################################

                # apply VBT since MIPI panel related fields were updated in VBT
                if gfx_vbt.apply_changes() is False:
                    self.fail(f"Setting VBT block failed for {platform['name']}")

            # After MIPI panel simulation, reboot is recommended. Driver disable-enable causes issues with certain
            # cases.
            # e.g. In pre-si when changing from port_sync panel to non_port_sync panel, pre-si environment is crashing
            # if we do driver disable-enable. In all cases, system reboot works and is recommended.
            is_reboot_required |= platform_status

        # end of operations for this platform

        return is_reboot_required

    ##
    # @brief        Helper function for verifying status after performing MIPI panel simulation
    # @return       None
    def verify_mipi_simulation(self) -> None:

        status = True
        # after MIPI simulation in VBT, make sure all requested MIPI panels are simulated successfully or not
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        for platform in self.platform_info.values():
            logging.info(f"Step: Verify simulated MIPI(s) for {platform['name']}")
            for port in self.requested_lfp_list[platform['gfx_index']]:
                if 'MIPI' not in port:
                    continue
                if display_config.is_display_attached(
                        enumerated_displays, port, gfx_index=platform['gfx_index']) is False:
                    logging.error(f"\t{port}: NOT simulated")
                    status = False
                else:
                    logging.info(f"\t{port}: Simulated successfully")

        if status is False:
            gdhm.report_bug(
                f"[ConfigureLfp] MIPI simulation is not working",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            self.fail("Requested MIPI(s) are NOT simulated. MIPI simulation is NOT working.")
        logging.info("\tPASS: All requested MIPI panels are simulated successfully")

    ##
    # @brief        Helper function for handling eDP simulation
    # @return       status- Boolean, True if a reboot is required, False otherwise
    def handle_edp_simulation(self) -> bool:
        if reboot_helper.is_reboot_scenario():
            status = True
            for platform in self.platform_info.values():
                logging.info(f"Step: Verify simulated eDP(s) for {platform['name']}")
                # Make sure all requested eDP panels are simulated successfully or not
                enumerated_displays = self.display_config_.get_enumerated_display_info()
                for port in self.requested_lfp_list[platform['gfx_index']]:
                    if 'DP' not in port:
                        continue
                    if display_config.is_display_attached(
                            enumerated_displays, port, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\t{port}: NOT simulated")
                        status = False
                    else:
                        logging.info(f"\t{port}: Simulated successfully")

            if status is False:
                gdhm.report_bug(
                    f"[ConfigureLfp] eDP simulation is not working",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES
                )
                self.fail("Requested eDP(s) are NOT simulated. EDP simulation is NOT working.")
            logging.info("\tPASS: All requested eDP panels are simulated successfully")
            return False

        status = False
        for platform in self.platform_info.values():
            logging.info(f"Step: Simulate requested eDP(s) on {platform['name']}")

            enumerated_displays = self.display_config_.get_enumerated_display_info()
            target_id_mapping = dict()
            for display_index in range(enumerated_displays.Count):
                display = enumerated_displays.ConnectedDisplays[display_index]
                if platform['gfx_index'] == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
                    target_id_mapping[CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name] = int(display.TargetID)

            # Handle lfp_none : unplug already connected LFP if requested
            if self.cmd_params[int(platform['gfx_index'][-1])]['LFP_NONE'] != 'NONE':
                for port in target_id_mapping.keys():
                    vbt_panel_type = display_utility.get_vbt_panel_type(port, platform['gfx_index'])
                    if vbt_panel_type != display_utility.VbtPanelType.LFP_DP or not display_config.is_display_attached(
                            enumerated_displays, port, gfx_index=platform['gfx_index']):
                        continue

                    # Get EDID of connected panel
                    edid_flag, connected_panel_edid, _ = driver_escape.get_edid_data(target_id_mapping[port])
                    if not edid_flag:
                        logging.error(f"Failed to get EDID data for target_id : {target_id_mapping[port]}")
                        self.fail()
                    if connected_panel_edid[12:16] != SIMULATED_EDP_SERIAL:
                        logging.error(f"\t{port} is a physical LFP panel. Can not be unplugged. (Planning Issue)")
                        continue

                    if display_utility.unplug(port=port, is_lfp=True, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\tFailed to unplug {port}")
                    else:
                        logging.info(f"\tUnplugged {port} successfully")
                        status = True

            # Skip eDP simulation if there is no eDP panel present in command line
            if len(self.requested_lfp_list[platform['gfx_index']]) < 1:
                logging.info(f"\tNo eDP panel requested for {platform['name']}. Skipping eDP simulation.")
                continue

            for port in self.requested_lfp_list[platform['gfx_index']]:
                if 'DP' not in port:
                    continue

                params = self.param_list[platform['gfx_index']][port]

                # First check if there is any LFP present on requested port or not, if not, simulation is required.
                # No need to check any further
                if display_config.is_display_attached(
                        enumerated_displays, port, gfx_index=platform['gfx_index']) is False:
                    self.__initialize_lfp_port(platform['gfx_index'], port)
                    if display_utility.plug(
                            port=port, edid=params['edid_name'], dpcd=params['dpcd_name'],
                            panelindex=params['panel_index'], is_lfp=True, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\tFailed to plug {port}")
                    status = True
                    continue

                # If some panel is already present, check if connected and requested panels are same or not. If same,
                # skip eDP simulation, otherwise plug the requested panel

                # Get EDID of connected panel
                edid_flag, connected_panel_edid, _ = driver_escape.get_edid_data(target_id_mapping[port])
                if not edid_flag:
                    logging.error(f"Failed to get EDID data for target_id : {target_id_mapping[port]}")
                    self.fail()
                # Get EDID file path from PanelInputData.xml
                requested_panel_info = display_utility.get_panel_edid_dpcd_info(port, params['panel_index'], True)
                edid_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, "eDP_DPSST",
                                         requested_panel_info["edid"])
                dpcd_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST',
                                         requested_panel_info['dpcd'])
                if not os.path.exists(edid_file):
                    gdhm.report_bug(
                        f"[ConfigureLfp] No EDID File Found",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"No EDID file present at location {edid_file}")

                if not os.path.exists(dpcd_file):
                    gdhm.report_bug(
                        f"[ConfigureLfp] No DPCD File Found",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    self.fail(f"No DPCD file present at location {dpcd_file}")

                with open(edid_file, "rb") as f:
                    requested_edid_data = f.read()
                requested_edid_data = [int(b) for b in requested_edid_data]

                # Check number of extension blocks
                is_same_panel = True
                if connected_panel_edid[126] == requested_edid_data[126]:
                    # For each extension block, verify the checksum
                    for block_index in range(connected_panel_edid[126] + 1):
                        checksum_index = (128 * block_index) + 127
                        if connected_panel_edid[checksum_index] != requested_edid_data[checksum_index]:
                            is_same_panel = False
                            break
                else:
                    is_same_panel = False

                # Do a DPCD capability check to handle same EDID but different DPCD case.
                if is_same_panel:
                    # Get DPCD offsets and values present in DPCD file
                    requested_dpcd_data = {}
                    with open(dpcd_file) as f:
                        for line in f.readlines():
                            line = line.strip()
                            if line.startswith(';') or ':' not in line:
                                continue
                            start_offset = int(line.split(':')[0], 0)
                            values = line.split(':')[1].strip().split('.')[0].split(',')
                            for value in values:
                                requested_dpcd_data[start_offset] = int(value, 16)
                                start_offset += 1

                    # Read DPCD data from connected panel
                    current_dpcd_data = {}
                    for offset in DPCD_CAPS_OFFSETS:
                        dpcd_flag, dpcd_value = driver_escape.read_dpcd(target_id_mapping[port], offset)
                        if dpcd_flag is False:
                            logging.error(
                                f"Failed to read DPCD for target_id ({target_id_mapping[port]}) at offset ({offset})")
                        current_dpcd_data[offset] = dpcd_value[0]

                    for offset, value in current_dpcd_data.items():
                        if value != requested_dpcd_data.get(offset, 0):
                            is_same_panel = False
                            logging.debug(
                                f"\tDPCD offset {hex(offset)} value is not matching. "
                                f"Requested= {hex(requested_dpcd_data.get(offset, 0))}, Current= {hex(value)}")
                            logging.info(f"\tDPCD is not matching with panel connected on {port}")
                            break

                if is_same_panel:
                    logging.info(f"\tRequested eDP panel is already connected on {port}")
                else:
                    ##
                    # Check whether connected panel is Physical or Simulated
                    if connected_panel_edid[12:16] != SIMULATED_EDP_SERIAL:
                        logging.warning(f"\tA different physical eDP panel is connected on {port}")
                    self.__initialize_lfp_port(platform['gfx_index'], port)
                    if display_utility.plug(
                            port=port, edid=params['edid_name'], dpcd=params['dpcd_name'],
                            panelindex=params['panel_index'], is_lfp=True, gfx_index=platform['gfx_index']) is False:
                        logging.error(f"\tFailed to plug {port}")
                    status = True
        return status

    ##
    # @brief        Helper function for Disabling dual link mipi port(DSI_1/MIPI_C) in VBT
    # @param[in]    gfx_vbt- Vbt, VBT object from vbt module
    # @return       None
    def disable_dual_link_mipi_port(self, gfx_vbt: vbt.Vbt) -> bool:
        ddi = "B"
        if gfx_vbt.block_52.MipiDataStructureEntry[gfx_vbt.block_40.PanelType].DualLinkSupport == 0 and \
                gfx_vbt.block_52.MipiDataStructureEntry[gfx_vbt.block_40.PanelType2].DualLinkSupport == 0:
            logging.info("Dual Link MIPI not enabled.")
            return None

        # Check for already configured VBT for given ddi
        for temp_index in range(MAX_LFP_COUNT):
            if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[temp_index].DeviceClass == 0x0:
                continue

            display_name = vbt_context.DVO_PORT_NAMES[
                gfx_vbt.block_2.DisplayDeviceDataStructureEntry[temp_index].DVOPort]

            if ddi == display_name[-1]:
                gfx_vbt.block_2.DisplayDeviceDataStructureEntry[temp_index].DeviceClass = 0x0
                logging.info(f" VBT port index {temp_index} disabled for dual link MIPI scenario.")

    ##
    # @brief        Initialize LFP Ports
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    port - Graphics Port Index
    # @return       None
    def __initialize_lfp_port(self, gfx_index: str, port: str):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        status = self.driver_interface_.initialize_lfp_ports(adapter_info, [port])
        if status is False:
            self.fail(f"Failed to initialized LFP port {port} on {gfx_index}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    output = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ConfigureLfp'))
    test_environment.TestEnvironment.cleanup(output)
