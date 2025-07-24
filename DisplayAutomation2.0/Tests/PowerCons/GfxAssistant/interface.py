#######################################################################################################################
# @file         interface.py
# @brief        Contains APIs required for interfacing DisplayAutomation and GfxAssistant
#
# @author       Ashish Tripathi, Rohit Kumar
#######################################################################################################################
import json
import logging
import os
import sys
import unittest
import urllib.request
from typing import Dict

from Libs.Core import cmd_parser, display_utility, registry_access, display_essential
from Libs.Core.display_config import display_config_enums
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower, PowerEvent
from Libs.Core.logger import html
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_fbc import fbc
from Tests.PowerCons.Functional.CFPS import cfps
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.PSR import psr, psr_util
from Tests.PowerCons.GfxAssistant import workload
from Tests.PowerCons.GfxAssistant.interface_context import *
from Tests.PowerCons.Modules import dut
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Tests.VRR import vrr

GFX_ASSISTANT_SERVER = r"http://10.223.161.17/triageTask/id/"


##
# @brief       This class contains GfxAssistant test cases.
# @details     This class inherits the TestCase class from unit test framework.
#              It implements the setup and teardown methods which can be used initialise and reset the changes done for
#              executing the GfxAssistant test cases
class GfxAssistantTriageTest(unittest.TestCase):
    data = None
    adapter: Adapter = None
    panels: Dict[str, Panel] = None

    ##
    # @brief       This method is used to initialise the required parameters and setup required test cases in this class
    # @return       None
    def setUp(self) -> None:
        options = cmd_parser.parse_cmdline(sys.argv, ['-ID'])
        task_id = options['ID'][0].lower()
        contents = urllib.request.urlopen(GFX_ASSISTANT_SERVER + task_id).read()
        self.data = json.loads(contents)
        self.adapter = dut.adapters['gfx_0']

    ##
    # @brief       This method executes all the steps in the Json one by one
    # @return       None
    def runTest(self):
        for step in self.data['steps']:
            self.run_step(step)

    ##
    # @brief       This method executes a step according to the Triage event
    # @param[in]    step contains details related to an event in actual test
    # @return       None
    def run_step(self, step):
        if step["id"] == TriageEvents.SET_POWER_SOURCE:
            self.set_power_source(step["arguments"])
        elif step["id"] == TriageEvents.DRIVER_RESTART:
            status, reboot_required = display_essential.restart_gfx_driver()
        elif step["id"] == TriageEvents.DISABLE_DISPLAY_FEATURE:
            self.toggle_feature(step["arguments"], True)
        elif step["id"] == TriageEvents.ENABLE_DISPLAY_FEATURE:
            self.toggle_feature(step["arguments"], False)
        elif step["id"] == TriageEvents.INVOKE_POWER_EVENT:
            self.invoke_power_event(step["arguments"])
        elif step["id"] == TriageEvents.GAME_PLAYBACK:
            self.invoke_workload(step["arguments"], Scenario.GAME_PLAYBACK)
        elif step["id"] == TriageEvents.VIDEO_PLAYBACK:
            self.invoke_workload(step["arguments"], Scenario.VIDEO_PLAYBACK)
        elif step["id"] == TriageEvents.IDLE_DESKTOP:
            self.invoke_workload(step["arguments"], Scenario.IDLE_DESKTOP)
        elif step["id"] == TriageEvents.SCREEN_UPDATE:
            self.invoke_workload(step["arguments"], Scenario.SCREEN_UPDATE)
        elif step["id"] == TriageEvents.HOT_PLUG:
            self.hot_plug(step["arguments"])
        elif step["id"] == TriageEvents.UNPLUG:
            self.unplug(step["arguments"])
        elif step["id"] == TriageEvents.SET_DISPLAY_CONFIG:
            self.set_display_config(step["arguments"])
        elif step["id"] == TriageEvents.REPEAT:
            for _ in range(int(step["arguments"]["iteration"]["value"])):
                for child in step["children"]:
                    self.run_step(child)

    ##
    # @brief       This is a helper method used to set power source
    # @param[in]   arguments
    # @return      None
    @staticmethod
    def set_power_source(arguments):
        __display_power = DisplayPower()
        power_line = arguments['powerSource']["value"]
        __display_power.enable_disable_simulated_battery(True)
        __display_power.set_current_powerline_status(
            PowerLineStatus.POWER_LINE_DC.value if power_line == "DC" else PowerLineStatus.POWER_LINE_AC.value)

    ##
    # @brief       This is a helper method used to toggle a feature
    # @param[in]   arguments
    # @param[in]   disable boolean indicating if the feature has to be enables or disabled
    # @return      None
    @staticmethod
    def toggle_feature(arguments, disable=False):
        feature = arguments['feature']['value']
        adapter = dut.adapters['gfx_0']
        gfx_index = 'gfx_0'

        status = None
        if feature == RequestedFeature.DRRS_REG_KEY:
            status = drrs.disable(adapter) if disable else drrs.enable(adapter)
        elif feature == RequestedFeature.DMRRS_REG_KEY:
            status = dmrrs.disable(adapter) if disable else dmrrs.enable(adapter)
        elif feature == RequestedFeature.FBC_REG_KEY:
            status = fbc.disable(gfx_index) if disable else fbc.enable(gfx_index)
        elif feature == RequestedFeature.PSR1_REG_KEY:
            status = psr.disable(adapter, PsrVersion.PSR_1) if disable else psr.enable(adapter, PsrVersion.PSR_1)
        elif feature == RequestedFeature.PSR2_REG_KEY:
            status = psr.disable(adapter, PsrVersion.PSR_2) if disable else psr.enable(adapter, PsrVersion.PSR_2)
        elif feature == RequestedFeature.PSR2_FFSU_REG_KEY:
            status = psr.disable(adapter, PsrVersion.PSR2_FFSU) if disable else psr.enable(adapter, PsrVersion.PSR2_FFSU)
        elif feature == RequestedFeature.PSR2_SFSU_REG_KEY:
            status = psr.disable(adapter, PsrVersion.PSR2_SFSU) if disable else psr.enable(adapter, PsrVersion.PSR2_SFSU)
        elif feature == RequestedFeature.LRR_REG_KEY:
            status = lrr.disable(adapter) if disable else lrr.enable(adapter)
        elif feature == RequestedFeature.VRR_ESCAPE_CALL:
            vrr.disable(adapter) if disable else vrr.enable(adapter)
        elif feature == RequestedFeature.CFPS_ESCAPE_CALL:
            cfps.disable(adapter) if disable else cfps.enable(adapter)

        if status is True:
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                logging.error(f"Failed to restart display driver for {adapter.name}")
            else:
                logging.info(f"Successfully to restart display driver for {adapter.name}")

    ##
    # @brief       This is a helper method used to invoke a power event
    # @param[in]   arguments
    # @return      None
    @staticmethod
    def invoke_power_event(arguments):
        __display_power = DisplayPower()
        if arguments['event']['value'] == PowerEvent.S3:
            power_event = PowerEvent.S3
        elif arguments['event']['value'] == PowerEvent.S4:
            power_event = PowerEvent.S4
        else:
            power_event = PowerEvent.CS
        __display_power.invoke_power_event(power_event, int(arguments['duration']['value']))

    ##
    # @brief       This is a helper method used to invoke a workload
    # @param[in]   arguments
    # @param[in]   workload_type type of workload to be used for test (IDLE_DESKTOP/VIDEO_PLAYBACK/GAME_PLAYBACK ...)
    # @return      None
    @staticmethod
    def invoke_workload(arguments, workload_type):
        if workload_type == Scenario.VIDEO_PLAYBACK:
            # [video, duration, pause=None, power_event=None, power_source=None]
            workload_args = [arguments['video']['value'], int(arguments['duration']['value'])]
            workload.run(Scenario.VIDEO_PLAYBACK, workload_args)
        elif workload_type == Scenario.VIDEO_PLAYBACK_WITH_MOUSE_MOVE:
            # [video, duration, start_delay=5, mouse_move_count=1, move_delay=15]
            workload_args = [arguments['video']['value'], int(arguments['duration']['value'])]
            workload.run(Scenario.VIDEO_PLAYBACK_WITH_MOUSE_MOVE, workload_args)
        elif workload_type == Scenario.GAME_PLAYBACK:
            # [game, full-screen, power_event=None, power_source=None, app_config=None]
            workload_args = [Apps.AngryBotsGame, True]
            workload.run(Scenario.GAME_PLAYBACK, workload_args)
        elif workload_type == Scenario.IDLE_DESKTOP:
            # [duration]
            workload_args = [int(arguments['duration']['value'])]
            workload.run(Scenario.IDLE_DESKTOP, workload_args)
        elif workload_type == Scenario.SCREEN_UPDATE:
            monitors = psr_util.app_controls.get_enumerated_display_monitors()
            workload_args = [_[0] for _ in monitors]
            workload.run(Scenario.SCREEN_UPDATE, workload_args)

    ##
    # @brief       This is a instance method used to handle hot plug of a display
    # @param[in]   arguments
    # @return      None
    def hot_plug(self, arguments):
        panel = self.get_panel(arguments)
        dut.plug_wrapper(self.adapter, panel)
        dut.refresh_panel_caps(self.adapter)
        logging.info("\t{0}".format(panel))

    ##
    # @brief       This is a instance method used to unplug a display
    # @param[in]   arguments
    # @return      None
    def unplug(self, arguments):
        display_utility.unplug(self.get_port(arguments['port']['value']))

    ##
    # @brief       This is a instance method used to set display config
    # @param[in]   arguments
    # @return      Boolean True if display config set successfully, False otherwise
    def set_display_config(self, arguments):
        topology = eval("enum.{}".format(arguments['topology']['value']))
        display_list = []
        for i in range(4):
            port_number = 'port{}'.format(i + 1)
            if arguments[port_number]['value'] != "NONE":
                display_list.append(self.get_port(arguments[port_number]['value']))

        if len(display_list) == 0:
            logging.error("Invalid display list passed in SET_DISPLAY_CONFIG step")
            return
        DisplayConfiguration().set_display_configuration_ex(topology, display_list)

    ##
    # @brief       This is a instance method used to get panel details
    # @param[in]   arguments
    # @param[in]   is_lfp boolean indicating if the display if a local flat panel
    # @return      Panel object
    def get_panel(self, arguments, is_lfp=False):
        connector_port = arguments['displayType']['value'] + "_" + arguments['port']['value']
        port_type = arguments['portType']['value']
        panel_index = arguments['panel']['value'].upper().replace('SINK_', '')
        panel_data = display_utility.get_panel_edid_dpcd_info(connector_port, panel_index, is_lfp)
        if panel_data is None:
            raise Exception("Invalid panel index found: {0}".format(panel_index))

        if 'HDMI' in connector_port:
            edid_path = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'HDMI', panel_data['edid'])
            assert os.path.exists(edid_path)
            panel_data['edid'] = edid_path
        elif 'DP' in connector_port:
            if os.path.exists(os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST', panel_data['edid'])):
                panel_data['edid'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST', panel_data['edid'])
                panel_data['dpcd'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST', panel_data['dpcd'])
            elif os.path.exists(
                    os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'DP_MST_TILE', panel_data['edid'])):
                panel_data['edid'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'DP_MST_TILE', panel_data['edid'])
                panel_data['dpcd'] = os.path.join(
                    test_context.PANEL_INPUT_DATA_FOLDER, 'DP_MST_TILE', panel_data['dpcd'])
            else:
                raise Exception(
                    "EDID file {0} given for {1} doesn't exist in [eDP_DPSST, DP_MST_TILE] directories".format(
                        panel_data['edid'], connector_port))
        return Panel(
            gfx_index=self.adapter.gfx_index,
            port=connector_port,
            port_type=port_type,
            is_lfp=is_lfp,
            panel_index=panel_index,
            edid_path=panel_data['edid'],
            dpcd_path=panel_data['dpcd'],
            description=panel_data['desc']
        )

    ##
    # @brief       This is a instance method used to get the port name
    # @param[in]   port
    # @return      string name of the port
    def get_port(self, port):
        # Add display_info, target_id, transcoder, pipe
        enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
        assert enumerated_displays

        for display_index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[display_index]
            if port == display_config_enums.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name.split("_")[-1]:
                return display_config_enums.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)

    system_utility = SystemUtility()

    # reset the changed registry keys
    html.step_start("Setting all display features to default via INF")
    for reg_key in Registry.SKU_DEFAULT[dut.adapters['gfx_0'].name]:
        reg_value = Registry.SKU_DEFAULT[dut.adapters['gfx_0'].name][reg_key]
        reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        registry_access.write(reg_args, reg_key, registry_access.RegDataType.DWORD, reg_value)
    status, reboot_required = display_essential.restart_gfx_driver()
    html.step_end()
