########################################################################################################################
# @file         plug_unplug_plug_multiple_times_within_750ms.py
# @brief        Validate Hot Plug given display in all supported DDI
#               displays are edp_a, dp_b, dp_c, hdmi_b, hdmi_c, etc
# @details      This test_script follows:
#               1. Hot Plug, unplug and plug Display1 within 750 millisec. This is repeated for 5 times.
#               2. Make Display Active for last Iteration.
#               3. Follows same for other Displays
#               CommandLine:
#                     python plug_unplug_plug_multiple_times_within_750ms.py [Display1][Display2][Display3][.....]
# @author       Neha Kumari
########################################################################################################################
import logging
import unittest
import sys
import time

from Libs.Core.logger import gdhm
from Libs.Core import reboot_helper, display_utility, enum, cmd_parser
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Detection.display_hpd_base import DisplayHPDBase

##
# @brief        PlugUnplugPlugMultipleTimesWithin750ms base class : To be used in Display Detection tests
class PlugUnplugPlugMultipleTimesWithin750ms(DisplayHPDBase):

    ##
    # @brief  Unit-test setup function. Parse the command line and XML file, Plug EDID/DPCD.
    # @return None
    def setUp(self):
        logging.debug("Entry: setUpClass")
        # Variable Initializing
        self.cmd_line_param = []
        self.input_display_list = []
        self.iteration_count = 0
        self.adapter_list = []

        self.config = display_config.DisplayConfiguration()

        cmdline_args = sys.argv

        # Parse the commandline params
        my_custom_tags = ['-iteration']
        self.cmd_line_param = cmd_parser.parse_cmdline(cmdline_args, my_custom_tags)
        logging.info(f"cmd line param = {self.cmd_line_param}")

        if type(self.cmd_line_param) is not list:
            self.cmd_line_param = [self.cmd_line_param]

        # input_display_list[] is a list of Port Names from user args
        for i in self.cmd_line_param:
            cmd_line_param_adapter = i
            for key, value in cmd_line_param_adapter.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if value['gfx_index'] is None:
                            value['gfx_index'] = 'gfx_0'
                        if str(value['gfx_index']).lower() in self.adapter_display_dict.keys():
                            self.adapter_display_dict[str(value['gfx_index']).lower()].append(
                                value['connector_port'])
                        else:
                            self.adapter_display_dict.update({str(value['gfx_index']).lower():
                                                              [value['connector_port']]})
                            
                        self.input_display_list.insert(value['index'], (str(value['gfx_index']).lower(), value['connector_port'],
                                                                            value['connector_port_type'], value['panel_index']))
                        logging.info(f"self.input_display_list = {self.input_display_list}")

                if key == 'ITERATION':
                    self.iteration_count = int(value[0].upper())

        logging.info("Test Flow : Plug and UnPlug of given display ports on respective port for number of Iterations given.")
        logging.info("Current Display Config Topology : {}".format(self.config.get_current_display_configuration_ex()))
        logging.debug("Exit: setUpClass")

    
    ##
    # @brief        unittest to test the plug
    # @details      Plug, unplugs and plug every display in cmdline for no. of iteration given in cmd line times within 750 millisec.
    #               Validating driver chnages done for QE : https://hsdes.intel.com/appstore/article/#/16016110111
    # @return       None
    def test_plug_unplug_within_750ms(self):
        logging.debug("Entry: plug_unplug_plug_multiple_times_within_750ms()")
        for gfx_index, display_port, port_connector_type, panel_index in self.input_display_list:
            # Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                               display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display on adapter {}".format(display_port, gfx_index))
                continue
            
            if display_port not in self.get_display_names().keys():
                # Plug, unplug and plug display within 750ms.
                for iteration in range(1, self.iteration_count + 1):
                    logging.info("{0} Iteration Count: for {1} {0}".format("*" * 20, display_port))
                    logging.info(f"    ITERATION {iteration} : Plugging Display {display_port} on {gfx_index}")
                    if not display_utility.plug(port=display_port, port_type=port_connector_type, panelindex=panel_index, gfx_index=gfx_index, is_delay_required=False):
                        gdhm.report_driver_bug_di(f"[Interfaces][Display_Detect] {display_port} plug failed on {gfx_index}")
                        self.fail(f"{display_port} PLUG failed on {gfx_index}.")
                    # Adding delay of 200 millisec between plug and unplug.
                    time.sleep(200/1000)

                    logging.info(f"Un-Plugging Display {display_port} on {gfx_index}")
                    if not display_utility.unplug(port=display_port, port_type=port_connector_type, gfx_index=gfx_index, is_delay_required=False):
                        gdhm.report_driver_bug_di(f"[Interfaces][Display_Detect] {display_port} unplug failed on {gfx_index}")
                        self.fail(f"{display_port} UNPLUG failed on {gfx_index}.")
                    
                    # Adding total delay of 400 millisec between two consecutive plug call, to check the driver's behavor and blankout should not be seen.
                    # Adding delay of 200 millisec between unplug and plug.
                    time.sleep(200/1000)

                    logging.info(f"Plugging Display {display_port} on {gfx_index}")
                    if not display_utility.plug(port=display_port, port_type=port_connector_type, panelindex=panel_index, gfx_index=gfx_index, is_delay_required=False):
                        gdhm.report_driver_bug_di(f"[Interfaces][Display_Detect] {display_port} plug failed on {gfx_index}")
                        self.fail(f"{display_port} PLUG failed on {gfx_index}.")
                    
                time.sleep(5)

                # Verifying display engine.
                enumerated_displays = self.config.get_enumerated_display_info()
                logging.debug(f'Enumerated Display Information: {enumerated_displays.to_string()}')
                if display_config.is_display_attached(enumerated_displays, display_port, gfx_index=gfx_index) is True:
                    logging.info(f'{display_port} PLUG Successful on {gfx_index}')
                    self.verify_display_engine(self.adapter_display_dict)
                else:
                    gdhm.report_driver_bug_di(f"[Interfaces][Display_Detect] {display_port} plug failed on {gfx_index}")
                    self.fail(f"{display_port} PLUG failed on {gfx_index}.")
                if (len(self.de_flag) < 1) or (False in self.de_flag):
                    gdhm.report_driver_bug_di(f"[Interfaces][Display_Detect] {display_port} display engine verification failed on {gfx_index}")
                    self.fail(f'{display_port} display engine verification failed on {gfx_index}')      


        logging.debug("Exit: plug_unplug_plug_multiple_times_within_750ms()")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('PlugUnplugPlugMultipleTimesWithin750ms'))
    TestEnvironment.cleanup(outcome)
