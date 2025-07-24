######################################################################################
# @file          scalar_base.py
# @brief         It contains setUp, tearDown and helper methods for all Scalar tests
#
# @author        Aafiya Kaleem, Veena Veluru
######################################################################################

import ctypes
import logging
import sys
import os
import unittest
import time
from xml.etree import ElementTree as ET

from Libs.Core import cmd_parser, registry_access, driver_escape, display_essential, display_utility, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.test_env import test_context
from Libs.Core.wrapper.driver_escape_args import CustomScalingArgs, CustomScalingOperation


##
# @brief Structure definition for -unit_test flags, that can be used with Scalar tests
class Flags(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('pipe_srcsz', ctypes.c_ubyte, 1),
                ('pipe_sz', ctypes.c_ubyte, 1),
                ('trans_sz', ctypes.c_ubyte, 1),
                ('reserved', ctypes.c_ubyte, 5)
                ]


##
# @brief Union represention of the -unit_test flag value passed in cmdline
class UserControlFlags(ctypes.Union):
    _fields_ = [("data", Flags),
                ("asbyte", ctypes.c_ubyte)]


##
# @brief This class has the base functions like setUp, process_cmdline, parse_xml_and_plug, plug_display, compare_modes, tearDown functions
class ScalarBase(unittest.TestCase):
    disp_count = 0
    max_downscale_amount = 0
    xml_file = dispConfig = None
    display_list = []
    target_id_list = []
    mst_port_list = []
    scalar_config_dict = {}
    platform = None
    platform_xml = None
    sku = ""
    enum_value = None
    controlFlag = None
    display_config = DisplayConfiguration()
    machine_info = SystemInfo()

    scale_dict = {'Unsupported': 0, 'CI': 1, 'FS': 2, 'MAR': 4, 'CAR': 8, 'MDS': 64}
    rscale_dict = {0: 'Unsupported', 1: 'CI', 2: 'FS', 4: 'MAR', 8: 'CAR', 64: 'MDS'}

    ##
    # @brief  Unit-test setup function. Parse the command line and XML file, Plug EDID/DPCD, and Set Config
    # @return None
    def setUp(self):
        logging.info("**************SCALAR VERIFICATION TEST START**************")
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = gfx_display_hwinfo[i].DisplayAdapterName
            break
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        max_cd_value, _ = registry_access.read(args=ss_reg_args, reg_name="MaxCdClockSupported")
        if max_cd_value is not None and self.platform == "DG2":
            self.sku = "B0"
        self.process_cmdline()
        self.parse_xml_and_plug()

        enumerated_displays = self.display_config.get_enumerated_display_info()
        if (self.dispConfig == 'SINGLE'):
            self.enum_value = enum.SINGLE
        else:
            self.enum_value = enum.EXTENDED

        # Apply display configuration for self.display_list
        logging.info("Display list to set config:{}".format(self.display_list))
        if self.display_config.set_display_configuration_ex(self.enum_value, self.display_list,
                                                            enumerated_displays) is False:
            self.fail()

    ##
    # @brief  Process input command line and custom tags supported ('-dispconfig','-xml','-downscale','-downscale_restrict')
    # @return None
    def process_cmdline(self):
        # Parse the command line arguments
        self.my_custom_tags = ['-dispconfig', '-xml', '-downscale', '-dsc', '-downscale_restrict', '-unit_test',
                               '-uncompressed', '-big_joiner', '-ultra_joiner']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        value = ""
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    if not (self.display_list.__contains__(value['connector_port'])):
                        self.display_list.append(value['connector_port'])
                else:
                    self.fail("Aborting the test as display is not passed in the command line")

            if (key == 'UNIT_TEST'):
                self.controlFlag = UserControlFlags()
                if (value != "NONE"):
                    self.controlFlag.asbyte = int(value[0], 16)
                else:
                    self.controlFlag.asbyte = 0x00
                logging.info("INFO : Unit Test flag value = %s" % (hex(self.controlFlag.asbyte)))

        self.disp_count = len(self.display_list)

        if 'XML' not in self.cmd_line_param.keys() and not self.cmd_line_param['XML']:
            self.fail("Aborting the test as xml file is not provided in command-line")
        self.xml_file = self.cmd_line_param['XML'][0]

        if 'DISPCONFIG' not in self.cmd_line_param.keys() and not self.cmd_line_param['DISPCONFIG']:
            self.fail("Aborting the test as display configuration is not provided in command-line")
        self.dispConfig = self.cmd_line_param['DISPCONFIG'][0]
        if not (((self.dispConfig == 'SINGLE') and (self.disp_count == 1)) or
                ((self.dispConfig == 'DUAL') and (self.disp_count == 2)) or (
                        (self.dispConfig == 'TRI') and (self.disp_count == 3))):
            logging.error("ERROR : Number of displays : %s, not equal to the display configuration : %s passed" % (
                self.disp_count, value[0]))
            self.fail()

    ##
    # @brief  Parse the XML file for EDID and DPCD and the mode to apply
    # @return None
    def parse_xml_and_plug(self):
        sup_platform = []
        tree = ET.parse(self.xml_file)

        self.platform_xml = tree.getroot()
        for plat_temp in self.platform_xml:
            plat_string = plat_temp.attrib['Name']
            platform_list_from_xml = plat_string.split(',')
            if ((plat_temp.tag == "Platform") and (self.platform in platform_list_from_xml)
                    and (self.sku == plat_temp.get('SKU'))):
                if 'TRUE' in self.cmd_line_param['DOWNSCALE'] or 'TRUE' in self.cmd_line_param[
                    'DOWNSCALE_RESTRICT']:
                    self.max_downscale_amount = int(plat_temp.attrib['Downscale_Max_Size'])
                    logging.info("Max Downscale amount for platform {} is {} Pixels".format(self.platform,
                                                                                            self.max_downscale_amount))
                sup_platform.append(self.platform)
                # Fetch the EDID/DPCD from XML and fetch the scalar mode to be applied, copy to self.scalar_config_dict
                for index in range(0, len(self.display_list)):
                    if 'TRUE' in self.cmd_line_param['DSC']:
                        display_node = plat_temp.find('DSCDisplayConfig')
                    elif 'TRUE' in self.cmd_line_param['UNCOMPRESSED']:
                        display_node = plat_temp.find('UCDisplayConfig')
                    elif 'TRUE' in self.cmd_line_param['BIG_JOINER']:
                        display_node = plat_temp.find('CPipeJoinerDisplayConfig')
                    elif 'TRUE' in self.cmd_line_param['ULTRA_JOINER']:
                        display_node = plat_temp.find('UltraJoinerDisplayConfig')
                    elif self.controlFlag.data.pipe_sz:
                        display_node = plat_temp.find('PipeSizeConfig')
                    elif 'TRUE' in self.cmd_line_param['DOWNSCALE_RESTRICT']:
                        display_node = plat_temp.find('RestrictDisplayConfig')
                    else:
                        display_node = plat_temp.find('GoldenDisplayConfig')

                    for displayConfig in display_node:
                        root_port_name = displayConfig.get('Port')
                        port_list_from_xml = root_port_name.split(',')
                        logging.debug(
                            "Port List from xml for platform {} -{}".format(self.platform, port_list_from_xml))

                        if (self.display_list[index] in port_list_from_xml):
                            modes_list = []
                            if display_utility.get_vbt_panel_type(self.display_list[index], 'gfx_0') in \
                                    [display_utility.VbtPanelType.LFP_DP,
                                     display_utility.VbtPanelType.LFP_MIPI]:  # no plug for LFP
                                enumerated_displays = self.display_config.get_enumerated_display_info()
                                target_id = self.display_config.get_target_id(self.display_list[index],
                                                                              enumerated_displays)
                            else:
                                edid = displayConfig.get('edid')
                                dpcd = displayConfig.get('dpcd')
                                display_tech = displayConfig.get('display_tech')
                                topology_path = displayConfig.get('topology_path')
                                self.plug_display(self.display_list[index], edid, dpcd, display_tech, topology_path)
                                target_id = self.get_target_id(self.display_list[index])
                                self.target_id_list.append(target_id)

                            if not 'TRUE' in self.cmd_line_param['DOWNSCALE'] and not 'TRUE' in self.cmd_line_param[
                                'DOWNSCALE_RESTRICT']:
                                if not self.controlFlag.asbyte:
                                    display = self.display_list[index].split("_")
                                    if 'TRUE' in self.cmd_line_param['DSC']:
                                        mode_list = plat_temp.find(display[0] + "DSCScalarModes")
                                    elif 'TRUE' in self.cmd_line_param['UNCOMPRESSED']:
                                        mode_list = plat_temp.find("UCScalarModes")
                                    elif 'TRUE' in self.cmd_line_param['BIG_JOINER']:
                                        mode_list = plat_temp.find("CPipeJoinerScalarModes")
                                    elif 'TRUE' in self.cmd_line_param['ULTRA_JOINER']:
                                        mode_list = plat_temp.find("UltraJoinerScalarModes")
                                    else:
                                        mode_list = plat_temp.find(display[0] + "ScalarModes")
                                    for modeInstance in mode_list:
                                        if (modeInstance.tag == "EDIDInstance"):
                                            mode = DisplayMode()
                                            mode.targetId = target_id
                                            mode.HzRes = int(modeInstance.get('HActive'))
                                            mode.VtRes = int(modeInstance.get('VActive'))
                                            mode.refreshRate = int(modeInstance.get('RefreshRate'))
                                            mode.BPP = 4  # Assuming RGB888
                                            mode.rotation = 1
                                            mode.scanlineOrdering = 1
                                            mode.scaling = self.scale_dict[modeInstance.get('Scaling')]
                                            modes_list.append(mode)

                                    self.scalar_config_dict[self.display_list[index]] = modes_list
                                break

        # If platform supported is not part of XML file, fail the test
        if not (self.platform in sup_platform):
            logging.error(
                "ERROR : XML file : %s specified is not valid for the %s platform" % (self.xml_file, self.platform))
            gdhm.report_bug(
                title="[Display_Interfaces][Scalar]{} - Platform is missing from Scalar XML".format(self.platform),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

    ##
    # @brief     Return target-id of the panel
    # @param[in] port is the Display to plug
    # @return    targetId of the panel
    def get_target_id(self, port):
        targetId = None
        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.info("Enumerated Displays after the plug: {}".format(enumerated_displays.to_string()))
        # Get Target-ID for connected port
        for display_index in range(enumerated_displays.Count):
            enum_port = (
                CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name
            if (enum_port == port):
                targetId = enumerated_displays.ConnectedDisplays[display_index].TargetID
        logging.info("INFO : Target-id for %s - %s" % (port, targetId))
        if (targetId is None):
            logging.error("FAIL : No target-id found for %s. Check if display is connected" % (port))
            gdhm.report_bug(
                title="[Display_Interfaces][Scalar] Target ID not found for plugged port %s".format(port),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        return targetId

    ##
    # @brief     Plug MST panel using topology details and non-MST panels using EDID and DPCD
    # @param[in] port is the Display to plug
    # @param[in] edid_file is the EDID to plug
    # @param[in] dpcd_file is the DPCD to pass
    # @param[in] display_tech is the parameter for plugging SST/MST panel
    # @param[in] plug_topology is the parameter to get the path for edid and dpcd to be plugged
    # @return    None
    def plug_display(self, port, edid_file, dpcd_file, display_tech, plug_topology):
        is_success = False
        if edid_file != "None":
            logging.info("INFO : Plug %s with EDID : %s DPCD : %s" % (port, edid_file, dpcd_file))
            is_success = display_utility.plug(port, edid_file, dpcd_file)
        elif display_tech is not None and plug_topology is not None:
            displayport = DisplayPort()
            path = os.path.join(test_context.TestContext.panel_input_data(), plug_topology)
            is_success = displayport.setdp(self.display_list[0], display_tech, path, False)
            self.mst_port_list.append(self.display_list[0])
            time.sleep(15)
        else:
            logging.error(f"Invalid data is provided for plugging the display on port {port}")

        if is_success is True:
            logging.info(f"Plug of display on {port} is successful")
        else:
            logging.error(f"Plug of display on {port} has failed")
            gdhm.report_driver_bug_di(
                title="[Display_Interfaces][Scalar] Plug of display on %s has failed".format(port)
            )
            self.fail(f"Plug of display on {port} has failed")

    ##
    # @brief     Set downscale percent through escape call
    # @param[in] target_id object of target_id
    # @param[in] xScaling x percent scaling
    # @param[in] yScaling y percent scaling
    # @param[in] get Get or Set scaling action
    # @return    True/False
    def get_set_downscale(self, target_id, xScaling=100, yScaling=100, get=True):
        display_adapter_info = self.display_config.get_display_and_adapter_info(target_id)
        if get == True:
            # get custom scaling details of the target id
            self.custom_scaling_args = CustomScalingArgs(xScaling, yScaling, target_id,
                                                         CustomScalingOperation.GET_STATE.value)
            status, self.custom_scaling_args = driver_escape.get_set_custom_scaling(display_adapter_info,
                                                                                    self.custom_scaling_args)
            logging.info(
                "Getting custom scaling info: Custom Scaling Info for target ID:{} - Enable status {}; CustomX {}; CustomY {}; Is Supported {} \n Return status: {}".format(
                    self.custom_scaling_args.target_id, self.custom_scaling_args.scalingEnabled,
                    self.custom_scaling_args.customScalingX, self.custom_scaling_args.customScalingY,
                    self.custom_scaling_args.scalingSupported, status))
            return True if self.custom_scaling_args.scalingSupported else False
        else:
            self.custom_scaling_args = CustomScalingArgs(xScaling, yScaling, target_id,
                                                         CustomScalingOperation.SET_STATE.value)
            status, self.custom_scaling_args = driver_escape.get_set_custom_scaling(display_adapter_info,
                                                                                    self.custom_scaling_args)
            logging.info(
                "After setting the custom scaling request: Custom Scaling Info for target ID:{} - Enable status {}; CustomX {}; CustomY {}; Is Supported {} \n Return status: {}".format(
                    self.custom_scaling_args.target_id, self.custom_scaling_args.scalingEnabled,
                    self.custom_scaling_args.customScalingX, self.custom_scaling_args.customScalingY,
                    self.custom_scaling_args.scalingSupported, status))

            return True

    ##
    # @brief     Compare mode to be applied with OS supported mode
    # @param[in] scalar_mode to apply
    # @param[in] supported_mode is the OS supported mode
    # @return    True/False
    def compare_modes(self, scalar_mode, supported_mode):
        if ((scalar_mode.HzRes == supported_mode.HzRes) and
                (scalar_mode.VtRes == supported_mode.VtRes) and
                (scalar_mode.refreshRate == supported_mode.refreshRate) and
                (scalar_mode.scaling == supported_mode.scaling)):
            return True
        else:
            return False

    ##
    # @brief  Unit-test teardown function.
    # @return None
    def tearDown(self):
        # Reset Downscale regkey with no Scaling value -100
        status = True
        displayport = DisplayPort()
        if 'TRUE' in self.cmd_line_param['DOWNSCALE'] or 'TRUE' in self.cmd_line_param['DOWNSCALE_RESTRICT']:
            for target_id in self.target_id_list:
                if self.get_set_downscale(target_id, 100, 100, False) is True:
                    logging.info("Downscale value restored to default(no scaling) in Teardown")
                else:
                    gdhm.report_driver_bug_di(title="[Display_Interfaces][Scalar] Downscaling restoration has failed.")
                    self.fail("Downscaling restoration has failed.")

        # clean-up : unplug the display plugged
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays == None:
            logging.error("enumerated_displays is None")
            self.fail("enumerated_displays is None")

        for count in range(enumerated_displays.Count):
            connector_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[count].ConnectorNPortType).name
            gfx_index = enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            connector_type = enumerated_displays.ConnectedDisplays[count].PortType
            if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI] and \
                    connector_port not in ['DispNone', 'VIRTUALDISPLAY'] and \
                    enumerated_displays.ConnectedDisplays[count].FriendlyDeviceName != "Raritan CIM":
                if connector_port in self.mst_port_list:
                    status = displayport.set_hpd(connector_port, False, gfx_index) and status
                else:
                    display_utility.unplug(connector_port, False, connector_type, gfx_index=gfx_index)
        if status:
            logging.info("Unplugging of display done properly")
        else:
            self.fail("FAIL: Unplug Failed")

        logging.info("**************SCALAR VERIFICATION TEST END**************")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
