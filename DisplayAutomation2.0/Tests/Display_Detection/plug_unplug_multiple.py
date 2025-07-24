########################################################################################################################
# @file         plug_unplug_multiple.py
# @brief        Validate Hot Plug given display in all supported DDI
#               displays are edp_a, dp_b, dp_c, hdmi_b, hdmi_c, etc
# @details      This test_script follows:
#               1. Hot Plug and unplug Display1 based on number of iterations mentioned
#               2. Make Display Active for last Iteration.
#               3. Hot Plug and unplug Display2 based on number of iterations mentioned
#               4. Make Display Active for last Iteration.
#               5. Follows same for other Displays
#               CommandLine:
#                     python hpd_plug_unplug_multiple.py [Display1][Display2][Display3][.....] -iteration != <-SIM/-EMU>
#                     Where param1 is main display and param2 is secondary displays and "-SIM" for Plug Mode.
# @author       Raghupathy, Dushyanth Kumar, Balaji Gurusamy
########################################################################################################################
import sys

from Libs.Core import cmd_parser, reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Detection.display_hpd_base import *


##
# @brief        PlugUnplugMultipleTimes base class : To be used in Display Detection tests
class PlugUnplugMultipleTimes(DisplayHPDBase):

    ##
    # @brief        setup function. Parse displays to plug and hpd_mode from cmdline params
    # @return       None
    def setUp(self):
        logging.debug("Entry: setUpClass")
        # Variable Initializing
        self.cmd_line_param = []
        self.input_display_list = []
        self.adapter_list = []
        self.panel_index = {}
        self.hpd_mode = None
        self.iteration_count = 0
        self.she_mst = False
        self.verify_connector_type = False
        self.she_mst_panels = []

        cmdline_args = sys.argv
        # Set control variable based on command line options
        for arg in cmdline_args:
            if arg.upper() == "-SIM":
                self.hpd_mode = "SIM"
                cmdline_args.remove("-SIM")
            elif arg.upper() == "-EMU":
                self.hpd_mode = "EMU"
                cmdline_args.remove("-EMU")

        if self.hpd_mode is None:
            self.hpd_mode = "SIM"

        # Parse the commandline params
        my_custom_tags = ['-iteration', '-she_mst_hub', '-verify_connector_type']
        self.cmd_line_param = cmd_parser.parse_cmdline(cmdline_args, my_custom_tags)

        if type(self.cmd_line_param) is not list:
            self.cmd_line_param = [self.cmd_line_param]

        # input_display_list[] is a list of Port Names from user args
        for i in self.cmd_line_param:
            cmd_line_param_adapter = i
            for key, value in cmd_line_param_adapter.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if self.input_display_list.__contains__(value['connector_port']):
                            adapter = self.adapter_list[self.input_display_list.index(value['connector_port'])]
                        if not self.input_display_list.__contains__(value['connector_port']) or (
                                self.input_display_list.__contains__(value['connector_port']) and
                                adapter != value['gfx_index']):
                            if (value['gfx_index'] == None):
                                value['gfx_index'] = 'gfx_0'
                            if str(value['gfx_index']).lower() in self.adapter_display_dict.keys():
                                self.adapter_display_dict[str(value['gfx_index']).lower()].append(
                                    value['connector_port'])
                            else:
                                self.adapter_display_dict.update({str(value['gfx_index']).lower():
                                                                      [value['connector_port']]})
                            self.adapter_list.insert(value['index'], str(value['gfx_index']).lower())
                            self.input_display_list.insert(value['index'], (value['connector_port'],
                                                                            value['connector_port_type']))
                            self.panel_index[str(value['gfx_index']).lower() + "_" +
                                             value['connector_port']] = value['panel_index']

                # Set control variable based on command line options for CS/S3
                if (key == 'ITERATION'):
                    self.iteration_count = int(value[0].upper())
                if key == 'SHE_MST_HUB' and value != 'NONE':
                    self.she_mst = True
                    self.she_mst_panels.extend([item.upper().replace('SINK_', '') for item in value])
                if key == 'VERIFY_CONNECTOR_TYPE' and value[0].upper() == 'TRUE':
                    self.verify_connector_type = True


        logging.info(
            "Test Flow : Plug and UnPlug of given display ports on respective port for number of Iterations given.")
        logging.info("Current Display Config Topology : {}".format(self.config.get_current_display_configuration_ex()))
        logging.debug("Exit: setUpClass")

    ##
    # @brief        unittest to test the plug
    # @details      Plugs and unplugs every display in cmdline for 'iteration' no of times
    # @return       None
    def test_plug_unplug(self):
        """
        Description:
        This test step HotPlug and Unplug given(input_display_list) display for given(iteration_count) iterations
        :return: None
        """
        logging.debug("Entry: test_plug_unplug()")
        result = True
        EFP_plugged_displays = {}
        step_count = 1
        for (display_port, port_connector_type), gfx_index in zip(self.input_display_list, self.adapter_list):
            # Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display on adapter {}".format(display_port, gfx_index))
                continue

            for counter in range(1, self.iteration_count + 1):
                logging.info("{0} Iteration Count: {1} for {2} {0}".format("*" * 20, counter, display_port))
                if display_port not in self.get_display_names().keys():
                    # Plug Display
                    num_displays_to_plug = len(self.she_mst_panels) if self.she_mst else 1
                    for index in range(num_displays_to_plug):
                        logging.info("    STEP {} : Plugging Display on {}".format(step_count, display_port))
                        step_count += 1
                        if self.she_mst:
                            panel_index = self.she_mst_panels[index]
                        else:
                            panel_index = self.panel_index.get(gfx_index + "_" + display_port)
                        if not self.plug_display(port=display_port, panel_index=panel_index,
                                                 port_type=port_connector_type, hpd_mode=self.hpd_mode,
                                                 she_mst_index=index if self.she_mst else None, gfx_index=gfx_index):
                            result = False

                    time.sleep(10)

                    # UnPlug Display
                    num_displays_to_unplug = len(self.she_mst_panels) if self.she_mst else 1
                    for index2 in range(num_displays_to_unplug):
                        logging.info("    STEP {} : Un-Plugging {} on {}".format(step_count, display_port, gfx_index))
                        step_count += 1
                        if not self.unplug_display(port=display_port, port_type=port_connector_type,
                                                   hpd_mode=self.hpd_mode,
                                                   she_mst_index=index2 if self.she_mst else None, gfx_index=gfx_index):
                            result = False

                    time.sleep(10)
                # Leave display in Plugged state after last iteration
                if counter == self.iteration_count:
                    logging.info(
                        "    STEP {} : Plugging {} on {} for Last Iteration to make Display Active".format(
                            step_count, display_port, gfx_index))
                    step_count += 1
                    # Plug Display for last Iteration
                    if not self.plug_display(port=display_port,
                                             panel_index=self.panel_index.get(gfx_index + "_" + display_port),
                                             port_type=port_connector_type, hpd_mode=self.hpd_mode,
                                             she_mst_index=0 if self.she_mst else None, gfx_index=gfx_index):
                        result = False
                    else:
                        EFP_plugged_displays[(gfx_index, display_port)] = port_connector_type
                step_count += 1

        if result is False:
            self.fail("Plug/Unplug failure detected")

        if not self.she_mst:
            if (len(self.de_flag) < 1) or (False in self.de_flag):
                self.fail("Display Engine Verification Failed")

        # after plug, verify whether plugged port is enumerated and also came with same connector_type. This is to
        # address issues where Valsim plug some connector type but driver enables different one (HSD 18012290188)
        # for connector type, we need to parse ETL, as the get_enumerated_display_info gets its connector type from VBT.
        if len(EFP_plugged_displays) > 0 and self.hpd_mode == "SIM" and self.verify_connector_type:
            etl_enumerated_ports = self.get_hpd_live_state_data_from_ETL()
            enumerated_displays = self.config.get_enumerated_display_info()
            os_enumerated_ports = {}
            for index in range(enumerated_displays.Count):
                connector_port = CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
                gfx_index = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                if gfx_index in os_enumerated_ports.keys():
                    os_enumerated_ports[gfx_index].append(connector_port)
                else:
                    os_enumerated_ports[gfx_index] = [connector_port]

            for adapter_and_port, plugged_connector_type in EFP_plugged_displays.items():
                gfx_index = adapter_and_port[0]
                plugged_connector_port = adapter_and_port[1]
                plugged_connector_type = 'NATIVE' if plugged_connector_type == 'PLUS' else plugged_connector_type

                # verifying the adapter and port, based on the os_enumerated_ports
                if gfx_index not in os_enumerated_ports.keys() or \
                        plugged_connector_port not in os_enumerated_ports[gfx_index]:
                    gdhm.report_bug(title=f'[Interfaces][Display_Config] {plugged_connector_port}_'
                                          f'{plugged_connector_type} not enumerated after plug',
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E3)
                    self.fail(f'FAIL: {plugged_connector_port}_{plugged_connector_type} not enumerated after plug')

                # verifying the port connector type based on etl_enumerated_ports
                etl_enumerated_port_connector_type = etl_enumerated_ports.get('PORT_' +
                                                                              plugged_connector_port.split('_')[-1])
                if plugged_connector_type == etl_enumerated_port_connector_type:
                    logging.info(f'PASS: enumerated port and connector type '
                                 f'({plugged_connector_port}_{etl_enumerated_port_connector_type}) is same as that '
                                 f'plugged by test ({plugged_connector_port}_{plugged_connector_type})')
                else:
                    gdhm.report_bug(
                        title=f'[Interfaces][Display_Config] enumerated port connector type '
                              f'({plugged_connector_port}_{etl_enumerated_port_connector_type}) is '
                              f'not same as that plugged by test ({plugged_connector_port}_{plugged_connector_type})',
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E3
                    )
                    self.fail(f'FAIL: enumerated port connector type '
                              f'({plugged_connector_port}_{etl_enumerated_port_connector_type}) is '
                              f'not same as that plugged by test ({plugged_connector_port}_{plugged_connector_type})')

        logging.debug("Exit: test_plug_unplug()")


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
            port_type = enum_display_list.ConnectedDisplays[count].PortType
            gfx_index = enum_display_list.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                num_displays_to_unplug = len(self.she_mst_panels) if self.she_mst else 1
                for index in range(num_displays_to_unplug):
                    self.unplug_display(connector_port, port_type=port_type, hpd_mode=self.hpd_mode,
                                        de_verification=False, she_mst_index=index if self.she_mst else None,
                                        gfx_index=gfx_index)

        logging.info("Test Completed")
        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PlugUnplugMultipleTimes'))
    TestEnvironment.cleanup(outcome)
