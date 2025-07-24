###################################################################################################################
# @file         assr_base.py
# @brief        This file contains common setUp and tearDown steps for all ASSR tests. Also contains the
#               common test functions used across all the ASSR verification scenarios.
# @note         For dual eDP scenarios, considering either both the panels will support ASSR or none of the panels will
#               support
# @author       Vinod D S, Bhargav Adigarla, Rohit Kumar
###################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, registry_access, display_essential
from Libs.Core import display_power
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules import dpcd
from registers.mmioregister import MMIORegister

GDHM_EDP_ASSR = "[Display_Interfaces][EDP][ASSR]"


##
# @brief        Exposed Base class for ASSR tests
class AssrBase(unittest.TestCase):
    cmd_line_param = None
    edp_panels = []
    edp_target_ids = {}

    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This function creates setup required for execution ASSR tests
    # @details      It checks for feature support, parses the command line and performs other enabling and checks
    #               required for execution of EDP tests
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: ASSR_BASE ".center(common.MAX_LINE_WIDTH, "*"))

        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, common.CUSTOM_TAGS)

        ##
        # Check for all the eDPs given in command line
        cmd_line_displays = cmd_parser.get_sorted_display_list(cls.cmd_line_param)
        for display in cmd_line_displays:
            if display_utility.get_vbt_panel_type(display, 'gfx_0') == display_utility.VbtPanelType.LFP_DP:
                cls.edp_panels.append(display)

        ##
        # Get displays passed in command line
        cls.display_list = cmd_parser.get_sorted_display_list(cls.cmd_line_param)

        ##
        # Get eDP panels given in command line
        cls.edp_panels = [panel for panel in cls.display_list if display_utility.get_vbt_panel_type(panel, 'gfx_0') ==
                          display_utility.VbtPanelType.LFP_DP]

        enumerated_displays = cls.display_config_.get_enumerated_display_info()
        if enumerated_displays is None:
            assert False, "API get_enumerated_display_info() FAILED (Test Issue)"

        ##
        # Make sure at least one eDP panel is given in command line
        if len(cls.edp_panels) == 0:
            ##
            # If nothing is given in command line, consider whatever is connected
            for display_index in range(enumerated_displays.Count):
                port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType).name
                if display_utility.get_vbt_panel_type(port, 'gfx_0') == display_utility.VbtPanelType.LFP_DP:
                    cls.edp_panels.append(port)
                    cls.display_list.append(port)

            ##
            # If no eDP panel is connected
            if len(cls.edp_panels) == 0:
                assert False, "No eDP display is passed in the command line (Commandline Issue)"

        logging.debug("eDP(s) from command line: {0}".format(', '.join(cls.edp_panels)))

        # Get the config given in command line
        if cls.cmd_line_param['CONFIG'] == 'NONE':
            ##
            # If nothing is given in command line, consider based on active panels
            cls.topology = enum.SINGLE
            if len(cls.edp_panels) > 1:
                cls.topology = enum.CLONE
        else:
            cls.topology = eval("enum.%s" % cls.cmd_line_param['CONFIG'])

        for edp_panel in cls.edp_panels:
            target_id = cls.display_config_.get_target_id(edp_panel, enumerated_displays)
            if target_id == 0:
                assert False, "Target ID for {0}(eDP) is 0 (Test Issue)".format(edp_panel)
            cls.edp_target_ids[edp_panel] = target_id
            logging.debug("\tTarget ID= {0}".format(target_id))

        ##
        # Set expected display configuration if current display configuration is different
        topology_name, port_list, adapter_list = cls.display_config_.get_current_display_configuration_ex()
        if topology_name != DisplayConfigTopology(cls.topology).name or len(cls.display_list and port_list) != len(
                cls.display_list):
            logging.info("Applying display configuration {0} {1}".format(DisplayConfigTopology(cls.topology).name,
                                                                         ' '.join(cls.display_list)))
            if cls.display_config_.set_display_configuration_ex(cls.topology, cls.display_list) is False:
                assert False, "Failed to apply display configuration"

        common.print_current_topology()

    ############################
    # Test Functions
    ############################

    ##
    # @brief        This test verifies all the requirements to start the ASSR tests
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        if enumerated_displays is None:
            self.fail("API get_enumerated_display_info() FAILED (Test Issue)")

        ##
        # Check whether panels support ASSR
        for edp_panel in self.edp_panels:
            logging.info("Verifying test requirements for {0}".format(edp_panel))

            result = display_config.is_display_attached(enumerated_displays, edp_panel)
            if result is False:
                self.fail("{0}(eDP) NOT connected. Please run the prepare_display to plug eDP".format(edp_panel))
            logging.info("\tPASS: Connection status Expected= Connected, Actual= Connected")

            edp_configuration_cap = dpcd.EdpConfigurationCap(self.edp_target_ids[edp_panel])
            if edp_configuration_cap.alternate_scrambler_reset_capable == 1:
                logging.info("\tPASS: Expected Panel ASSR status= SUPPORTED, Actual= SUPPORTED")
            else:
                self.fail("ASSR is NOT supported on {0}(eDP)(Planning Issue)".format(edp_panel))

    ##
    # @brief        Test to Enable and verify ASSR. Only for Legacy driver
    # @return       None
    # @cond
    @common.configure_test(selective=["LEGACY"], critical=True)
    # @endcond
    def t_10_enable_assr(self):
        ##
        # Enabling the feature in INF
        logging.info("Step: Enabling ASSR")
        status = registry.write('gfx_0', registry.RegKeys.ASSR.ALTERNATE_SCRAMBLER_SUPPORT,
                                registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
        if status is False:
            self.fail("Failed to update {0} key in registry".format(registry.RegKeys.ASSR.ALTERNATE_SCRAMBLER_SUPPORT))
        if status:
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                self.fail("Failed to restart display driver")
        logging.info("\tPASS: Expected ASSR status= ENABLED, Actual= ENABLED")

    ##
    # @brief        Disable and verify ASSR. Only for Legacy driver.
    # @return       None
    # @cond
    @common.configure_test(selective=["LEGACY", "BLOCKED"], critical=True)
    # @endcond
    def t_20_disable_assr(self):
        ##
        # Disabling the feature in INF
        logging.info("Step: Disabling ASSR")
        status = registry.write('gfx_0', registry.RegKeys.ASSR.ALTERNATE_SCRAMBLER_SUPPORT,
                                registry_access.RegDataType.DWORD, registry.RegValues.DISABLE)
        if status is False:
            self.fail("Failed to update {0} key in registry".format(registry.RegKeys.ASSR.ALTERNATE_SCRAMBLER_SUPPORT))
        if status:
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                self.fail("Failed to restart display driver")
        logging.info("\tPASS: Expected ASSR status= DISABLED, Actual= DISABLED")

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        Check ASSR in both driver and the panel
    # @param[in]    edp_panel Panel object
    # @param[in]    enabled boolean indicates expected Driver ASSR status
    # @return       status
    def verify_assr(self, edp_panel, enabled=True):
        status = True
        enabled_bit = 1
        if enabled is False:
            enabled_bit = 0

        logging.info("Step: Verifying ASSR for {0}".format(edp_panel))

        # @Todo Remove the below caps once dut is used:
        # Check EDP version:
        edp_revision = dpcd.get_edp_revision(self.edp_target_ids[edp_panel])
        if edp_revision <= dpcd.EdpDpcdRevision.EDP_DPCD_1_1_OR_LOWER:
            logging.info(f"PASS: ASSR not supported for EDP_DPCD_1_1_OR_LOWER")
            return True

        ##
        # Check whether ASSR is enabled in the driver or not
        offset_name = "DP_TP_CTL_{0}".format(edp_panel.split('_')[-1])
        dp_tp_ctl = MMIORegister.read("DP_TP_CTL_REGISTER", offset_name, common.PLATFORM_NAME)
        if dp_tp_ctl.alternate_sr_enable == enabled_bit:
            logging.info(
                "\tPASS: Expected Driver ASSR status for {0}= {1}, Actual= {1}".format(
                    edp_panel, "ENABLED" if enabled else "DISABLED"))
        else:
            logging.error(
                "\tFAIL: Expected Driver ASSR status for {0}= {1}, Actual= {2}".format(
                    edp_panel, "ENABLED" if enabled else "DISABLED", "DISABLED" if enabled else "ENABLED"))
            gdhm.report_driver_bug_di(f"{GDHM_EDP_ASSR} ASSR is not getting enabled by driver")

            status = False

        ##
        # Check whether ASSR is enabled in the panel or not
        edp_configuration_set = dpcd.EdpConfigurationSet(self.edp_target_ids[edp_panel])
        if edp_configuration_set.alternate_scrambler_reset_enable == 1:
            if enabled:
                logging.info(
                    "\tPASS: Expected Panel ASSR status for {0}= ENABLED, Actual= ENABLED".format(edp_panel))
            else:
                logging.error(
                    "\tFAIL: Expected Panel ASSR status for {0}= DISABLED, Actual= ENABLED".format(edp_panel))
                gdhm.report_driver_bug_di(f"{GDHM_EDP_ASSR} ASSR is enabled in panel when not expected")

                status = False
        else:
            if not enabled:
                logging.info(
                    "\tPASS: Expected Panel ASSR status for {0}= DISABLED, Actual= DISABLED".format(edp_panel))
            else:
                logging.error(
                    "\tFAIL: Expected Panel ASSR status for {0}= ENABLED, Actual= DISABLED".format(edp_panel))
                gdhm.report_driver_bug_di(f"{GDHM_EDP_ASSR} ASSR is disabled in panel")
                status = False

        return status
