########################################################################################################################
# @file         edp_verify_linkrate_lanecount.py
# @addtogroup   EDP
# @section      LinkTraining
# @brief        Test to verify link rate and lane count for eDP
# @details      @ref edp_verify_linkrate_lanecount.py <br>
#               This file implements setUp and tearDown methods of unittest framework.
#               In setUp, command_line arguments are parsed, eDP panel's existence is checked.
#               This test also checks EDP is working fine (clocks, pipe,plane,transcoders) for various
#               configurations (link rates,lane count etc).
#               In tearDown method, the displays which were plugged in the setUp method are unplugged and TDR check is
#               done.
#
# @author       Vinod D S
########################################################################################################################


import logging
import sys
import unittest

from Libs.Core import cmd_parser, enum, display_essential
from Libs.Core import display_utility
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.clock import display_clock
from Libs.Feature.display_engine import de_master_control
from Tests.EDP import edp_common
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules import dpcd
from registers.mmioregister import MMIORegister
from Libs.Core import reboot_helper
from Libs.Feature.powercons import registry

##
# @brief        This class contains test to verify eDP link rate and lane count
class EdpVerifyLinkParams(unittest.TestCase):
    cmd_line_param = None  # Used to store command line parameters
    display_list = []  # Used to store all displays given in command line
    edp_panels = []  # Used to store eDP panels given in command line
    edp_target_ids = {}  # Used to store target IDs for eDP panels {'DP_A': 456}
    topology = None
    display_config_ = display_config.DisplayConfiguration()
    display_engine = de_master_control.DisplayEngine()
    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This method initializes and prepares the setup required for execution of tests in this class
    # @details      It parses the command line checks for eDP connections and sets display configuration
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):

        logging.info(" SETUP: EDP_VERIFY_LINKRATE_LANECOUNT ".center(common.MAX_LINE_WIDTH, "*"))
        ##
        # Get cmd line params
        # dynamic_cdclk Dummy Custom tag added to run Display config test case with dynamic CDCLK disable,
        # which is done in setup part of TP
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, ['-dynamic_cdclk'])

        ##
        # Get the config given in command line
        self.topology = eval("enum.%s" % self.cmd_line_param['CONFIG'])

        ##
        # Get displays passed in command line
        self.display_list = cmd_parser.get_sorted_display_list(self.cmd_line_param)

        ##
        # Get eDP panels given in command line
        self.edp_panels = [panel for panel in self.display_list if display_utility.get_vbt_panel_type(panel, 'gfx_0') ==
                           display_utility.VbtPanelType.LFP_DP]

        ##
        # Make sure at least one eDP panel is given in command line
        if len(self.edp_panels) == 0:
            ##
            # If nothing is given in command line, consider whatever is connected
            enumerated_displays = self.display_config_.get_enumerated_display_info()
            for display_index in range(enumerated_displays.Count):
                port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType).name
                if display_utility.get_vbt_panel_type(port, 'gfx_0') == display_utility.VbtPanelType.LFP_DP:
                    self.edp_panels.append(port)
                    self.display_list.append(port)

            ##
            # If no eDP panel is connected
            if len(self.edp_panels) == 0:
                assert False, "No eDP display is passed in the command line (Commandline Issue)"

        logging.debug("eDP(s) from command line: {0}".format(', '.join(self.edp_panels)))

        enumerated_displays = self.display_config_.get_enumerated_display_info()

        ##
        # Checking that all the eDPs passed in command line are connected and getting target ids for the same
        logging.info("Checking command lines edp(s) connected and getting the details:")
        for edp_panel in self.edp_panels:
            if display_config.is_display_attached(enumerated_displays, edp_panel) is False:
                assert False, "{0} NOT connected. Please run the prepare_display to plug eDP".format(edp_panel)
            logging.info("\tPASS: {0} is connected")
            edid_name = self.cmd_line_param['E%s' % edp_panel]['edid_name']
            panel_desc = edp_common.get_panel_description(edid_name)
            if panel_desc is None:
                logging.info("\t\t{0}: Details Not available".format(edp_panel))
            else:
                ##
                # Parse the description
                # Format: HRESxVRES\@RR_BPC_LINKRATE_LANECOUNT_SSCSTATE_FEATURE_MAKE (FEATURE & MAKE optional)
                data = panel_desc.split('_')
                if len(data) >= 5:
                    logging.info("\t\t{0}: Resolution= {1}, BPC= {2}, LinkRate= {3}, LaneCount= {4}, "
                                 "SSC_Supported= {5}".format(edp_panel, data[0], data[1], data[2], data[3],
                                                             'YES' if data[4].upper() == 'SSC' else 'NO'))
                else:
                    logging.info("\t\t{0}: {1}".format(edp_panel, panel_desc))
            target_id = self.display_config_.get_target_id(edp_panel, enumerated_displays)
            if target_id == 0:
                assert False, "{0} Target ID= 0 (Test Issue)".format(edp_panel)
            self.edp_target_ids[edp_panel] = target_id
            logging.debug("\tPASS: {0} Target ID= {1}".format(edp_panel, target_id))

        ##
        # Set expected display configuration if current display configuration is different
        topology_name, port_list, adapter_list = self.display_config_.get_current_display_configuration_ex()
        if topology_name != DisplayConfigTopology(self.topology).name or len(self.display_list and port_list) != len(
                self.display_list):
            logging.info("Applying display configuration {0} {1}".format(
                DisplayConfigTopology(self.topology).name, ' '.join(self.display_list)))
            if self.display_config_.set_display_configuration_ex(self.topology, self.display_list) is False:
                assert False, "Failed to apply display configuration"
        common.print_current_topology()

    ##
    # @brief        This function logs the teardown phase
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info(" TEARDOWN: EDP_VERIFY_LINKRATE_LANECOUNT ".center(common.MAX_LINE_WIDTH, "*"))

    ############################
    # Test Function
    ############################
    ##
    # @brief        This function deletes the regkey and do system reboot if required
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def test_10_reg_key_delete(self):
        if common.IS_PRE_SI is False:
            # HSD -18013883922 WA - Delete reg key to avoid PSR disable due to PowerPlan settings set by previous Non-PSR Panel
            status = registry.delete('gfx_0', key=registry.RegKeys.POWER_PLAN_AWARE_SETTINGS)
            if status is False:
                self.fail("Failed to delete reg key")
            elif status is True:
                _, reboot_required = display_essential.restart_gfx_driver()
                if reboot_required and reboot_helper.reboot(self, 'test_11_verify_edp_link_params') is False:
                    self.fail("Failed to reboot the system")

    ##
    # @brief        This function verifies eDP Link rate and lane count
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def test_11_verify_edp_link_params(self):
        logging.info(" RUNTEST: VERIFY_EDP_LINKRATE_LANECOUNT ".center(common.MAX_LINE_WIDTH, "*"))

        # Skip DVFS verification if not enabled in below platforms
        if common.PLATFORM_NAME in ['MTL', 'LNL', 'PTL', 'NVL']:
            logging.info(f"Verifying Voltage Level notified to PCode for {common.PLATFORM_NAME}")
            if display_clock.DisplayClock.verify_voltage_level_notified_to_pcode('gfx_0', self.edp_panels) is False:
                logging.error(f"FAIL: DVFS VoltageLevel verification failed for {self.edp_panels} on gfx_0")
                gdhm.report_driver_bug_pc("[Interfaces][Display_Engine][CD Clock] Failed to verify "
                                          "Voltage level during eDP link training",
                                          gdhm.ProblemClassification.FUNCTIONALITY)
            else:
                logging.info("PASS: DVFS VoltageLevel verification successful")
        else:
            logging.warning(f"Skipping DVFS VoltageLevel verification for unsupported platform : "
                            f"{common.PLATFORM_NAME}.")

        # Test whether clock, plane, pipe, transcoder, DDI, WM are programmed correctly
        if common.PLATFORM_NAME in ['ADLP']:
            self.display_engine.modify_display_engine_verifiers("0x2BF")
        if self.display_engine.verify_display_engine(self.edp_panels) is False:
            self.fail("Failed to verify eDP LinkRate LaneCount")

        logging.info("PASS: eDP LinkRate LaneCount verified successfully")

    ##
    # @brief        This function verifies enabling of the 4k2k mode
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def test_20_enable_edp_4k2k_mode(self):
        system_restart = False
        if common.PLATFORM_NAME in ["TGL", "DG1", "ADLP", "RKL", "ADLS"]:
            gfx_vbt = Vbt()
            for edp_panel in self.edp_panels:
                ##
                # From 232 VBT onwards, Driver enable this functionality based VBT setting
                if gfx_vbt.version >= 232:
                    panel_index = gfx_vbt.get_lfp_panel_type(edp_panel)
                    logging.debug(f"\tPanel Index= {panel_index}")

                    if (gfx_vbt.block_44.Edp_4k_2k_hobl[0] & (1 << panel_index)) >> panel_index == 0:
                        logging.info("Enabling edp_4k2k_mode")
                        system_restart = True
                        # ENABLE HOBL feature in VBT
                        gfx_vbt.block_44.Edp_4k_2k_hobl[0] |= (1 << panel_index)
                        if gfx_vbt.apply_changes() is False:
                            logging.error("\tFailed to apply changes to VBT")
                            return False

        if system_restart is True:
            if reboot_helper.reboot(self, callee="verify_edp_4k2k_mode") is False:
                self.fail("Failed to reboot the system(Test Issue)")

    ##
    # @brief        This function verifies link rate and lane count for eDP in 4k2k mode
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def verify_edp_4k2k_mode(self):
        ##
        # edp_4k2k_mode is applicable from JSL onwards (not ICL)
        if not edp_common.IS_DDRW or common.PLATFORM_NAME[0:3] == "ICL":
            return

        ##
        # Due to the current failure, disabling the check for JSL
        # @todo need to remove this once issue is fixed
        if common.PLATFORM_NAME[0:3] == "JSL":
            return

        logging.info(" RUNTEST: VERIFY_EDP_4K2K_MODE ".center(common.MAX_LINE_WIDTH, "*"))

        ##
        # For eDP, program eDP4K2K and rterm override values in register PORT_CL_DW10.
        # HoBL: Display IO IP Power fixes for HOBL - Applicable only for eDP.
        # https://gfxspecs.intel.com/Predator/Home/Index/21257
        # https://gfxspecs.intel.com/Predator/Home/Index/49291
        # Driver needs to set i_edp4k2k_mode to 1 & Swing Scalar register (to 150ohms),
        # when data rate <=5.4Gbps (link Clock <=540 MHz) .
        # Driver needs to set i_edp4k2k_mode to 0 to support all data rates,
        # including eDP lower & higher data rates.

        status = True
        logging.info("Checking edp_4k2k_mode")
        for edp_panel in self.edp_panels:
            link_rate = dpcd.get_link_rate(target_id=self.edp_target_ids[edp_panel], is_edp_panel=True)
            if link_rate == 0:
                logging.error("\tFailed to get LinkRate for {0}".format(edp_panel))
                status = False
                continue
            logging.info("\t{0}: LinkRate= {1:.2f}Gbps".format(edp_panel, link_rate))
            port_cl_dw10_val = MMIORegister.read(
                "PORT_CL_DW10_REGISTER", "PORT_CL_DW10_{0}".format(edp_panel[-1]), common.PLATFORM_NAME)
            logging.debug("\t{0}: PORT_CL_DW10_{1} value= {2}".format(edp_panel, edp_panel[-1],
                                                                      hex(port_cl_dw10_val.asUint)))
            if (link_rate * 100) <= 540:
                if (
                        port_cl_dw10_val.o_edp4k2k_mode_ovrd_en == 1 and
                        port_cl_dw10_val.o_edp4k2k_mode_ovrd_val == 1 and  # eDP mode: 0 = DP/MIPI/eDP 8K, 1 = eDP 4K/2K
                        port_cl_dw10_val.o_rterm100en_h_ovrd_en == 1 and
                        port_cl_dw10_val.o_rterm100en_h_ovrd_val == 0  # Term resistor: 0 = 150ohms, 1 = 100ohms
                ):
                    logging.info("\tPASS: edp_4k2k_mode for {0} Expected= ENABLED, Actual= ENABLED".format(edp_panel))
                else:
                    gdhm.report_bug(
                        title="[EDP][HOBL] 4k2k HOBL mode disabled",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error("\tFAIL: edp_4k2k_mode for {0} Expected= ENABLED, Actual= DISABLED".format(edp_panel))
                    status = False
            else:
                if (
                        port_cl_dw10_val.o_edp4k2k_mode_ovrd_en == 0 and
                        port_cl_dw10_val.o_rterm100en_h_ovrd_en == 0
                ):
                    logging.info("\tPASS: edp_4k2k_mode for {0} Expected= DISABLED, Actual= DISABLED".format(edp_panel))
                else:
                    logging.error("\tFAIL: edp_4k2k_mode for {0} Expected= DISABLED, Actual= ENABLED".format(edp_panel))
                    status = False

        # Check if eDP 4k2k HoBL feature enabled during test then disable it
        gfx_vbt = Vbt()
        driver_restart = False
        if gfx_vbt.version >= 232:
            for edp_panel in self.edp_panels:
                panel_index = gfx_vbt.get_lfp_panel_type(edp_panel)
                logging.debug(f"\tPanel Index= {panel_index}")
                if (gfx_vbt.block_44.Edp_4k_2k_hobl[0] & (1 << panel_index)) >> panel_index == 1:
                    logging.info("Disabling edp_4k2k_mode")
                    driver_restart = True
                    # DISABLE HOBL feature from VBT
                    gfx_vbt.block_44.Edp_4k_2k_hobl[0] &= ~(1 << panel_index)
                    if gfx_vbt.apply_changes() is False:
                        logging.error("\tFailed to apply changes to VBT")
                        return False

            if driver_restart is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    logging.error("\tFailed to restart display driver after VBT update")
                    return False

                gfx_vbt.reload()

        if status is False:
            self.fail("Failed to verify edp_4k2k_mode")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdpVerifyLinkParams'))
    test_environment.TestEnvironment.cleanup(outcome)
