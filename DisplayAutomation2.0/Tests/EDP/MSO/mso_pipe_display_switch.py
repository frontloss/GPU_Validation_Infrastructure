#######################################################################################################################
# @file         mso_pipe_display_switch.py
# @brief        This file contains test to drive MSO panel using PIPE_C or PIPE_D
#
# @author       Akshaya Nair
#######################################################################################################################
from Libs.Core import display_utility, enum
from Libs.Core.display_config import display_config, display_config_enums as cfg_enum
from Libs.Core.test_env import test_environment
from Libs.Feature.display_engine.de_base import display_base
from Tests.EDP.MSO.mso_base import *
from Tests.PowerCons.Modules import dpcd


##
# @brief        Contains tests to check if MSO eDP panel is allocated pipe C/D
#               instead of pipe A/B as preferred by driver policy for eDP panels.
#               DCN - https://wiki.ith.intel.com/display/GfxDisplay/Removal+Of+Pipe+Dependency+For+MSO+Support
class MsoPipeDisplaySwitch(unittest.TestCase):
    cmd_line_param = None  # Used to store command line parameters
    display_list = []
    edp_panels = []
    external_panels = []
    last_connected_display = []  # Used to store config of display to be connected at last
    target_id = None
    disp_config_ = display_config.DisplayConfiguration()
    config_list = []
    pipe_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This method initializes and prepares the setup required for execution of tests in this class
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info("SETUP: MSO Pipe C/D Display Switching Scenario".center(common.MAX_LINE_WIDTH, "*"))

        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, common.CUSTOM_TAGS)
        cls.display_list = cmd_parser.get_sorted_display_list(cls.cmd_line_param)
        cls.last_connected_display = cls.cmd_line_param.popitem()[-1]
        cls.edp_panels = [panel for panel in cls.display_list if display_utility.get_vbt_panel_type(panel, 'gfx_0') ==
                           display_utility.VbtPanelType.LFP_DP]
        cls.external_panels = [panel for panel in cls.display_list if panel not in cls.edp_panels]
        plugged_display, enumerated_displays = display_utility.plug_displays(cls, cls.cmd_line_param)

        cls.target_id = cls.disp_config_.get_target_id(cls.edp_panels[0], enumerated_displays)
        if not mso.is_mso_supported_in_panel(cls.target_id):
            assert False, f"FAIL: Connected panel on {cls.edp_panels[0]} is not supporting MSO (Planning Issue)"

        # Need to connect panels to all external ports, such that all pipes will be occupied
        if len(cls.external_panels) != 4:
            assert False, "FAIL: All external ports are not occupied (Planning Issue)"

        cls.config_list = [(enum.SINGLE,    [cls.external_panels[0]]),
                            (enum.EXTENDED,  [cls.external_panels[0], cls.external_panels[1], cls.external_panels[2]]),
                            (enum.SINGLE,    [cls.external_panels[0]]),
                            (enum.EXTENDED,  [cls.external_panels[0], cls.external_panels[1], cls.external_panels[2],
                                              cls.external_panels[3]])]

    ##
    # @brief        This function logs the teardown phase
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: MSO Pipe C/D Display Switching Scenario ".center(common.MAX_LINE_WIDTH, "*"))

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function creates display switch scenarios with MSO + four external panels
    #               and verifies eDP is allocated pipe C
    # @return       None
    # @cond
    @common.configure_test(selective=["PIPE_C"])
    # @endcond
    def t_00_verify_mso_pipe_c(self):
        # Disabling eDP
        self.__apply_config(self.config_list[0:2])

        # Plugging fourth display
        if not self.__plug_last_display():
            self.fail(f"FAIL: Failed to plug display on {self.external_panels[-1]}")

        # Enabling all four pipes by applying extended on all EFP panels
        self.__apply_config(self.config_list[2:])

        # Unplugging display to which PIPE_C got allocated
        if not self.__unplug_display(pipe=2):
            self.fail(f"FAIL: Failed to unplug display to which PIPE_C is allocated")

        # Validating if MSO panel is allocated PIPE_C
        if self.__verify_pipe(pipe=2):
            logging.info(f"PASS: MSO {self.edp_panels[0]} panel is driven through PIPE_C")
        else:
            self.fail(f"FAIL: MSO {self.edp_panels[0]} panel is not driven through PIPE_C")

        # MSO verification
        if self.__mso_verification(pipe=2):
            logging.info(f"PASS: MSO verification successful")
        else:
            self.fail(f"FAIL: MSO verification")

    ##
    # @brief        This function creates display switch scenarios with MSO + four external panels
    #               and verifies eDP is allocated pipe D
    # @return       None
    # @cond
    @common.configure_test(selective=["PIPE_D"])
    # @endcond
    def t_01_verify_mso_pipe_d(self):
        # Disabling eDP
        self.__apply_config(self.config_list[0:2])

        # Plugging fourth display
        if not self.__plug_last_display():
            self.fail(f"FAIL: Failed to plug display on {self.external_panels[-1]}")

        # Enabling all four pipes by applying extended on all EFP panels
        self.__apply_config(self.config_list[2:])

        # Unplugging display to which PIPE_D got allocated
        if not self.__unplug_display(pipe=3):
            self.fail(f"FAIL: Failed to unplug display to which PIPE_D is allocated")

        # Validating if MSO panel is allocated PIPE_D
        if self.__verify_pipe(pipe=3):
            logging.info(f"PASS: MSO {self.edp_panels[0]} panel is driven through PIPE_D")
        else:
            self.fail(f"FAIL: MSO {self.edp_panels[0]} panel is not driven through PIPE_D")

        # MSO verification
        if self.__mso_verification(pipe=3):
            logging.info(f"PASS: MSO verification successful")
        else:
            self.fail(f"FAIL: MSO verification")

    ############################
    # Helper Function
    ############################

    ##
    # @brief        This function applies required config on connected panels
    # @param[in]    config_list - List of display config to be applied
    # @return       None
    def __apply_config(self, config_list):
        for i, config in enumerate(config_list):
            if self.disp_config_.set_display_configuration_ex(config[0], config[1]) is False:
                logging.error("Applying Display config {0} Failed".format(
                    str(config[0]) + " " + " ".join(str(x) for x in config[1])))

    ##
    # @brief        This function verifies if the MSO panel is connected on required pipe
    # @param[in]    pipe   - Display Pipe in range 0-4 for PIPE_A to PIPE_D respectively
    # @return       True if MSO is allocated required pipe else False
    def __verify_pipe(self, pipe):
        enumerated_displays = self.disp_config_.get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[index]
            if display_info.IsActive:
                display = str(cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name)
                display_base_obj = display_base.DisplayBase(display)
                _, display_pipe = display_base_obj.get_transcoder_and_pipe(display)
                if display == 'DP_A' and display_pipe == pipe:
                    return True
        return False

    ##
    # @brief        This function plugs display on last port passed in commandline
    # @return       True if external panel is plugged else False
    def __plug_last_display(self):
        panel_edid = self.last_connected_display['edid_name'] if self.last_connected_display[
                                                                     'edid_name'] is not None else 'DP_3011.EDID'
        panel_dpcd = self.last_connected_display['dpcd_name'] if self.last_connected_display[
                                                                     'dpcd_name'] is not None else 'DP_3011_dpcd.txt'
        result = display_utility.plug(self.external_panels[-1], edid=panel_edid, dpcd=panel_dpcd)
        return result

    ##
    # @brief        This function unplugs the panel connected on required pipe
    # @param[in]    pipe   - Display Pipe in range 0-4 for PIPE_A to PIPE_D respectively
    # @return       True if unplug is successful else False
    def __unplug_display(self, pipe):
        enumerated_displays = self.disp_config_.get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[index]
            if display_info.IsActive:
                display = str(cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name)
                display_base_obj = display_base.DisplayBase(display)
                _, display_pipe = display_base_obj.get_transcoder_and_pipe(display)
                if display_pipe == pipe:
                    result = display_utility.unplug(display)
                    if not result:
                        logging.error(f"FAIL: Failed to unplug display {display} to which PIPE_{self.pipe_mapping[pipe]} is allocated ")
                        return False
                    return True
        logging.error(f"FAIL: Failed to get display to which PIPE_{self.pipe_mapping[pipe]} is allocated")
        return False

    ##
    # @brief        This function does MSO verification for pipe C/D allocated panel
    # @param[in]    pipe   - Display Pipe in range 0-4 for PIPE_A to PIPE_D respectively
    # @return       True if MSO verification successful else False
    def __mso_verification(self, pipe):
        panel = dut.Panel(pipe=self.pipe_mapping[pipe],
                          target_id=self.target_id,
                          )
        caps = dpcd.EdpMsoCaps(panel.target_id)
        if caps.no_of_links in [2, 4]:
            panel.mso_caps.no_of_segments = caps.no_of_links

        if mso.verify(panel):
            return True
        return False


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(MsoPipeDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)
