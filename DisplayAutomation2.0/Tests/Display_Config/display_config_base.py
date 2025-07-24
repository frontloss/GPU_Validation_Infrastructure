######################################################################################
# @file     display_config_base.py
# @brief    Has base functions to be used by display_config_switching.py
# @details  It contains setUp and tearDown methods of unittest framework. For all Display Config tests
#           which is derived from this, will make use of setup/teardown of this base class.
#           This class will also contain other helper functions
# @author   rradhakr
######################################################################################
import copy
import ctypes
import logging
import os
import sys
import time
import unittest
from xml.etree import ElementTree as ET

from Libs import env_settings
from Libs.Core import reboot_helper, cmd_parser, display_utility, enum, display_essential, registry_access
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core import display_power
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.logger import html
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_port import usb4

Delay_After_Power_Event = 10
Delay_5_Secs = 5
COMBO_PHY = 0
TC_PHY = 1
MAX_PLANE_COUNT = 2


##
# @brief Structure definition for -user_event flags, that can be used with config tests
# @details More information about these flag values present in README.txt
class Flags(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('apply_CS', ctypes.c_ubyte, 1),
                ('apply_S3', ctypes.c_ubyte, 1),
                ('apply_S4', ctypes.c_ubyte, 1),
                ('reboot', ctypes.c_ubyte, 1),
                ('dynamic_cd_clk_gfx_0', ctypes.c_ubyte, 1),
                ('dynamic_cd_clk_gfx_1', ctypes.c_ubyte, 1),
                ('disable_mpo_gfx_0', ctypes.c_ubyte, 1),
                ('enable_efp_ssc_gfx_0', ctypes.c_ubyte, 1),
                ('enable_efp_ssc_gfx_1', ctypes.c_ubyte, 1),
                ('verify_usb4', ctypes.c_ubyte, 1),
                ('disable_mpo_gfx_1', ctypes.c_ubyte, 1),
                ]

##
# @brief Union represention of the -user_event flag value passed in cmdline
class UserControlFlags(ctypes.Union):
    _fields_ = [("data", Flags),
                ("asbyte", ctypes.c_uint)]


##
# @brief: Display Config Base class : To be used in Display Config tests
class DisplayConfigBase(unittest.TestCase):
    enumerated_displays = None
    display_list = []
    adapter_list = []
    sequence_list = []
    platform_dict = {}
    port_type = []

    display_config = disp_cfg.DisplayConfiguration()
    system_utility = SystemUtility()
    display_clock = DisplayClock()
    display_power = display_power.DisplayPower()
    machine_info = SystemInfo()
    test_context = test_context.TestContext()
    underrunstatus = UnderRunStatus()
    pre_si = False
    selected_group3 = False
    edid_dpcd_list1 = edid_dpcd_list2 = edid_dpcd_list3 =  []
    display_edid_dpcd = {}
    display_and_adapter_list = []
    adapter_display_name_list = []
    ss_reg_args = []

    gfx_display_hwinfo_list = machine_info.get_gfx_display_hardwareinfo()
    for gfx_display_hwinfo in gfx_display_hwinfo_list:
        platform_dict[gfx_display_hwinfo.gfxIndex] = gfx_display_hwinfo.DisplayAdapterName
    all_gfx_adapter_details = test_context.get_gfx_adapter_details()
    for gfx_index, value in all_gfx_adapter_details.items():
        ss_reg_args.append(registry_access.StateSeparationRegArgs(gfx_index=gfx_index))

    ##
    # @brief Unit-test setup function.
    # @details Parses the cmdline params and creates set of edid-dpcd lists to be plugged from edid_dpcd_config_switching
    #          Prepares Display Sequence from DisplaySequence.xml
    # @return - None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.display_list = []
        self.adapter_list = []
        self.port_type = []
        # dynamic_cdclk Dummy Custom tag added to run Display config test case with dynamic CDCLK disable,
        # which is done in setup part of TP
        # select_group3 is a Custom tag added to select group3 edid having 19x10 display.
        self.my_custom_tags = ['-user_event', '-dynamic_cdclk', '-select_group3']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        self.display_config = disp_cfg.DisplayConfiguration()
        ##
        if (
                self.system_utility.get_execution_environment_type() is not None and self.system_utility.get_execution_environment_type() in [
            "SIMENV_FULSIM", "SIMENV_PIPE2D"]):
            self.pre_si = True

        if type(self.cmd_line_param) is not list:
            self.cmd_line_param = [self.cmd_line_param]

        ##
        # Process command line params. For edp/dp/hdmi displays, get appropriate edid-dpcd info from xml
        for i in self.cmd_line_param:
            self.cmd_line_param_adapter = i
            for key, value in self.cmd_line_param_adapter.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if self.display_list.__contains__(value['connector_port']):
                            adapter = self.adapter_list[self.display_list.index(value['connector_port'])]
                        if not self.display_list.__contains__(value['connector_port'])or (
                                self.display_list.__contains__(value['connector_port']) and adapter != value['gfx_index']):
                            if (value['gfx_index'] == None):
                                value['gfx_index'] = 'gfx_0'
                            self.adapter_list.insert(value['index'], value['gfx_index'].lower())
                            self.display_list.insert(value['index'], value['connector_port'])
                            self.port_type.insert(value['index'], value['connector_port_type'])
                            if value['connector_port'].startswith('MIPI'):
                                continue
                            elif display_utility.get_vbt_panel_type(value['connector_port'], value['gfx_index'].lower()) == \
                                    display_utility.VbtPanelType.LFP_DP:
                                display = 'EDP'
                            elif value['connector_port'].startswith('DP'):
                                display = 'DP'
                            elif value['connector_port'].startswith('HDMI'):
                                display = 'HDMI'
                            if value['edid_name'] is not None:
                                self.edid_dpcd_list1 = value['edid_name'], value['dpcd_name']
                                self.edid_dpcd_list2 = value['edid_name'], value['dpcd_name']
                                self.edid_dpcd_list3 = value['edid_name'], value['dpcd_name']
                            else:
                                self.edid_dpcd_list1 = self.edid_dpcd_list2 = self.edid_dpcd_list3 = []
                                self.get_edid_dpcd_from_xml(display, value['gfx_index'].lower())
                            self.display_edid_dpcd[value['gfx_index'] + "_" + value['connector_port'] + "_" + value[
                                'connector_port_type']] = [self.edid_dpcd_list1, self.edid_dpcd_list2, self.edid_dpcd_list3]

                if (key == 'USER_EVENT'):
                    self.controlFlag = UserControlFlags()
                    if (value != "NONE"):
                       self.controlFlag.asbyte = int(value[0],16)
                    else:
                       self.controlFlag.asbyte = 0x00
                    logging.debug("INFO : User Event flag value = %s" % (hex(self.controlFlag.asbyte)))

                if (key == 'SELECT_GROUP3'):
                    if (value != "NONE"):
                        self.selected_group3 = True if value[0] == "TRUE" else False

        self.prepare_sequence()

    ##
    # @brief Unit-test teardown function.
    # @return - None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        html.step_start("Test Clean Up")

        ##
        # Check TDR
        result = display_essential.detect_system_tdr(gfx_index='gfx_0')
        if result:
            gdhm.report_bug(
                title="[Interfaces][Display_Config] Test failure due to TDR on gfx_adapter : gfx_0",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertNotEquals(result, True, "Aborting the test as TDR happened while executing the test")
        html.step_end()


    ##
    # @brief Creates dictionary from the root tag passed
    # @param[in] r Root tag of the xml in use
    # @param[in] root Bool value to specify if it is a root tag
    # @return dictionary created with the xml data
    def dictify(self, r, root=True):
        if root:
            return {r.tag: self.dictify(r, False)}
        d = copy.copy(r.attrib)
        # if r.text:
        #     d["_text"]=r.text
        for x in r.findall("./*"):
            if x.tag not in d:
                d[x.tag] = []
            d[x.tag].append(self.dictify(x, False))
        return d

    ##
    # @brief create a list with edid/dpcd for the display passed from the xml
    # @param[in] display eg. EDP_A/DP_B etc.
    # @param[in] gfx_index gfx_adapter passed
    # @return None
    def get_edid_dpcd_from_xml(self, display, gfx_index='gfx_0'):
        tree = ET.parse(test_context.ROOT_FOLDER + r'\Tests\Display_Config\edid_dpcd_config.xml')
        root = tree.getroot()
        root_index_current_platform = None
        root_index_default_platform = None
        sku = ""
        platform = self.platform_dict[gfx_index]

        max_cd_value, _ = registry_access.read(args=self.ss_reg_args[int(gfx_index[-1])], reg_name="MaxCdClockSupported")
        if max_cd_value is not None and platform == "DG2":
            self.sku = "B0"
        # root of the platform assigned to respective variable if platform found in xml
        for root_index in root:
            root_platform_name = root_index.attrib['Name']
            platform_list_from_xml = root_platform_name.split(',')
            if platform in platform_list_from_xml and sku == root_index.attrib['SKU']:
                root_index_current_platform = root_index
            if "DEFAULT" in platform_list_from_xml:
                root_index_default_platform = root_index

        # if current platform is not found in xml, use default platform data
        if root_index_current_platform is None:
            root_index = root_index_default_platform
        else:
            root_index = root_index_current_platform
        for config_data in root_index.find('Group1'):
            if ((config_data.tag == "DisplayConfig") and (config_data.get('display') == display)):
                self.edid_dpcd_list1 = config_data.get('edid'), config_data.get('dpcd')
        for config_data in root_index.find('Group2'):
            if ((config_data.tag == "DisplayConfig") and (config_data.get('display') == display)):
                self.edid_dpcd_list2 = config_data.get('edid'), config_data.get('dpcd')
        for config_data in root_index.find('Group3'):
            if ((config_data.tag == "DisplayConfig") and (config_data.get('display') == display)):
                self.edid_dpcd_list3 = config_data.get('edid'), config_data.get('dpcd')

    ##
    # @brief  Create a map for the displays and sequences
    # @return None
    def prepare_sequence(self):
        is_pre_si_environment = SystemUtility().get_execution_environment_type() in ["SIMENV_FULSIM",
                                                                                     "SIMENV_PIPE2D"]
        tree = ET.parse(test_context.ROOT_FOLDER + r'\Tests\Display_Config\DisplaySequence.xml')
        root = tree.getroot()
        dd = self.dictify(root)
        aa = dd["Sequences"]

        if is_pre_si_environment:
            logging.info("PreSi Platform, Picking Presi specific Sequences from XML")
            # limiting the Display Switch combinations to a max of 5
            self.sequence_list = list(dict(aa['Presi'][0]).values())[0]
        elif self.controlFlag.asbyte:
            self.sequence_list = list(dict(aa['Powereventsseq'][0]).values())[0]
        else:
            self.sequence_list = list(dict(aa['Seq1'][0]).values())[0]

    ##
    # @brief create a map for the displays and sequences
    # @param[in] display_str display sequence prepared from DisplaySequence.xml
    # @param[in] new_display_sequence display sequence prepared from plugged displays
    # @return None
    def map_seq_displays(self, display_str, new_display_sequence):
        disp_str_list = str(display_str).split(",")
        index_list = []

        for disp in disp_str_list:
            index_list.append(new_display_sequence.index(disp))

        if (len(self.adapter_list) == 0):
            adapter_list = ['gfx_0'] * len(self.display_list)
        else:
            adapter_list = list(map(lambda x: str(self.adapter_list[int(x) - 1]).lower(), index_list))
        return adapter_list, list(map(lambda x: self.display_list[int(x) - 1], index_list)), \
               list(map(lambda x: self.port_type[int(x) - 1],
                                 index_list))

    ##
    # @brief Set the given config along with displays
    # @param[in] config SINGLE/CLONE/EXTENDED
    # @param[in] displays Display list to set config with
    # @param[in] adapters adapter list to set the config ['GFX_0','GFX_1',..'GFX_N']
    # @return None
    def set_and_validate_config(self, config, displays, adapters):
        if len(self.display_list) < len(displays):
            logging.info("Ignoring the config {0} in "
                         "sequence since planned test has only {1} displays".format(config,
                                                                                    str(len(self.display_list))))
        else:
            cfg = enum.SINGLE
            if config == 'SINGLE':
                cfg = enum.SINGLE
            elif config == 'CLONE':
                cfg = enum.CLONE
            elif config == 'EXTENDED':
                cfg = enum.EXTENDED

            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            self.display_and_adapter_list *= 0
            logging.info("Enumerated display count:{0}, Displays count:{1}".format(range(self.enumerated_displays.Count),len(displays)))
            for i in range(len(displays)):
                for count in range(self.enumerated_displays.Count):
                    display_name = ((CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[count].ConnectorNPortType)).name)
                    gfx_adapter = self.enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                    if ((display_name == displays[i]) and (gfx_adapter == adapters[i].lower())):
                        logging.debug("Adapter:{0}, Display added to set config params:{1}".format(adapters[i], display_name))
                        self.display_and_adapter_list.append(self.enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo)

            if self.display_config.set_display_configuration_ex(cfg,self.display_and_adapter_list) is False:
                self.fail("SetDisplayConfigurationEX returned false")
                # GDHM will be handled in set_display_configuration_ex()

            # check if panel came active or not by checking panel timings
            _driver_interface = driver_interface.DriverInterface()
            ret = []
            for display, adapter in zip(displays, adapters):
                adapter_info = test_context.TestContext.get_gfx_adapter_details()[adapter]
                ret.append(_driver_interface.is_panel_timings_non_zero(adapter_info, display))
            if not all(ret):
                self.fail('One of the displays did not come active')

    ##
    # @brief Perform power events CS,S3,S4 and set dynamic CD clk from user event
    # @return Bool value based on power event successful or not
    def set_and_validate_powerevents(self):
        if (self.controlFlag.data.dynamic_cd_clk_gfx_0 or self.controlFlag.data.dynamic_cd_clk_gfx_1):
            # Check if Dynamic CD clock enabled in VBT
            if self.controlFlag.data.dynamic_cd_clk_gfx_0:
                gfx0_vbt = Vbt('gfx_0')
                logging.info("INFO : Dynamic CD CLK from VBT : %s" % ((gfx0_vbt.block_1.BmpBits2 and 64) == 64))
            if self.controlFlag.data.dynamic_cd_clk_gfx_1:
                gfx1_vbt = Vbt('gfx_1')
                logging.info("INFO : Dynamic CD CLK from VBT : %s"%((gfx1_vbt.block_1.BmpBits2 and 64 ) == 64))
        if (self.controlFlag.data.enable_efp_ssc_gfx_0 or self.controlFlag.data.enable_efp_ssc_gfx_1):
            if self.controlFlag.data.enable_efp_ssc_gfx_0:
                # Check if DP SSC for EFP enabled in VBT for adapter 1
                gfx0_vbt = Vbt('gfx_0')
                logging.info("INFO : DP SSC from VBT : {0}".
                             format(gfx0_vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Enable))
                logging.info("INFO : DP SSC for dongles from VBT : {0}".
                             format(gfx0_vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Dongle_Enable))
            if self.controlFlag.data.enable_efp_ssc_gfx_1:
                gfx1_vbt = Vbt('gfx_1')
                logging.info("INFO : DP SSC from VBT : {0}".
                             format(gfx1_vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Enable))
                logging.info("INFO : DP SSC for dongles from VBT : {0}".
                             format(gfx1_vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Dongle_Enable))

        if self.controlFlag.data.apply_CS:
            # Invoke CS state
            if self.display_power.invoke_power_event(display_power.PowerEvent.CS, 60):
                time.sleep(Delay_5_Secs)
            else:
                return False
            time.sleep(Delay_After_Power_Event)
            current_config = self.display_config.get_current_display_configuration_ex()
            logging.info("After CS, Current config is {0}:{1}".format(current_config[0], current_config[1]))

        if self.controlFlag.data.apply_S3:
            # Invoke S3 state
            if self.display_power.invoke_power_event(display_power.PowerEvent.S3, 60):
                time.sleep(Delay_5_Secs)
            else:
                return False
            time.sleep(Delay_After_Power_Event)
            current_config = self.display_config.get_current_display_configuration_ex()
            logging.info("After S3, Current config is {0}:{1}".format(current_config[0], current_config[1]))

        if self.controlFlag.data.apply_S4:
            # Invoke S4 state
            if self.display_power.invoke_power_event(display_power.PowerEvent.S4, 60):
                time.sleep(Delay_5_Secs)
            else:
                return False
            time.sleep(Delay_After_Power_Event)
            current_config = self.display_config.get_current_display_configuration_ex()
            logging.info("After S4, Current config is {0}:{1}".format(current_config[0], current_config[1]))

        if self.controlFlag.data.verify_usb4:
            if self.verify_usb4_display_detection() is False:
                self.fail("USB4 Verification failed.")

        return True

    ##
    # @brief Make Display list from xml
    # @param[in] xml_list
    # @return List of Values from xml
    def make_display_list(self, xml_list):
        return list(map(lambda x: list(dict(x).values())[0], xml_list))

    ##
    # @brief Unplug all the displays connected if they are unpluggable
    # @return None
    def unplug_displays(self):
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        total_displays_connected = self.enumerated_displays.Count
        if self.enumerated_displays == None:
            logging.error("enumerated_displays is None")
            self.fail("enumerated_displays is None")

        for count in range(self.enumerated_displays.Count):
            connector_port = CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[count].ConnectorNPortType).name
            gfx_index = self.enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            connector_type = self.enumerated_displays.ConnectedDisplays[count].PortType
            if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI] and \
                    connector_port not in ['DispNone','VIRTUALDISPLAY'] and \
                    self.enumerated_displays.ConnectedDisplays[count].FriendlyDeviceName != "Raritan CIM":
                display_utility.unplug(connector_port, False, connector_type, gfx_index= gfx_index)
            else:
                continue
            enumerated_displays_updated = self.display_config.get_enumerated_display_info()
            logging.debug("Enumerated Displays after unplug of {} :\n {}".format(connector_port, enumerated_displays_updated.to_string()))

            if self.enumerated_displays is None:
                # GDHM already handled in display_config.get_enumerated_display_info()
                logging.error("enumerated_displays is None")
                self.fail("enumerated_displays is None")

            if not disp_cfg.is_display_attached(enumerated_displays_updated, connector_port, gfx_index):
                logging.info("Successfully  unplugged display %s on adapter %s", connector_port, gfx_index)
            else:
                # WA for DG platforms to not check unplug status due to OS behavior
                platform = self.platform_dict[gfx_index]
                if count + 1 == total_displays_connected and platform in ['DG1', 'DG2', 'ELG', 'CLS']:
                    logging.warning("WARN: Display {} reported as still Attached. Sometimes OS doesnot update Unplug Status for last display, in case where "
                                    "Virtual Display not plugged by driver. Ignoring unplug status for such cases".format(connector_port))
                else:
                    if connector_port != "VIRTUALDISPLAY":
                        gdhm.report_bug(
                            title="[Interfaces][Display_Config] Display is still attached on port {} for adapter {} even "
                                  "after unplug".format(connector_port, gfx_index),
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Test.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        logging.error("Unable to unplug display %s on adapter %s", connector_port, gfx_index)

        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug("Enumerated Displays after unplug of all:{}".format(self.enumerated_displays.to_string()))


    ##
    # @brief based on platform, function returns the phy type for the input ddi
    # @param[in] platform Platform passed
    # @param[in] ddi A/B/C..etc.
    # @return type of Phy being used
    def phy_type(self, platform, ddi):
        type = None

        if platform == 'ICLLP':
            type = COMBO_PHY if ddi in ['A', 'B'] else TC_PHY
        elif platform == 'ICLHP':
            type = COMBO_PHY if ddi in ['A', 'B', 'C'] else TC_PHY
        elif platform == 'JSL':
            type = COMBO_PHY
        elif platform == 'LKF1':
            type = TC_PHY
        elif platform == 'TGL':
            type = COMBO_PHY if ddi in ['A', 'B', 'C'] else TC_PHY
        elif platform == 'DG1':
            type = COMBO_PHY
        elif platform == 'DG2':
            type = COMBO_PHY if ddi in ['A', 'B', 'C', 'D'] else TC_PHY
        elif platform == 'ADLP':
            type = COMBO_PHY if ddi in ['A', 'B', 'C', 'D'] else TC_PHY
        elif platform == 'RYF':
            type = COMBO_PHY if ddi in ['A', 'B'] else TC_PHY
        elif platform == 'RKL':
            type = COMBO_PHY
        elif platform == 'ADLS':
            type = COMBO_PHY
        elif platform in ['MTL', 'LNL', 'PTL']:
            type = COMBO_PHY if ddi in ['A', 'B'] else TC_PHY
        elif platform == ['ELG', 'CLS']:
            type = COMBO_PHY if ddi in ['A'] else TC_PHY
        return type

    ##
    # @brief Generate ETL file by stopping and starting etl and returns path.
    # @return etl_file_path Returns None if etl file not generated.
    def get_current_test_etl(self):
        # Stopping ETL tracing
        if etl_tracer.stop_etl_tracer() is False:
            return None

        # Renaming the ETL file
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTrace_USB4-' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
        else:
            logging.error("[Test Issue]: Default etl file does not exist")
            gdhm.report_bug(
                title="[Interfaces][USB4] Default etl file is not present in the system",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None

        # Starting ETL Again
        if etl_tracer.start_etl_tracer(etl_tracer.TraceType.TRACE_ALL) is False:
            return None

        return etl_file_path

    ##
    # @brief Verifies the plugged DP displays are detected as USB4 comparing from etl file.
    # @return usb4_detect_status True if USB4 Displays detected else false
    def verify_usb4_display_detection(self):
        usb4_detect_status = True
        etl_file_path = self.get_current_test_etl()
        if etl_file_path is None:
            self.fail("Unable to get ETL File.")

        usb4_displays = usb4.get_connected_usb4_displays(etl_file_path)
        for display_index in range(len(self.display_list)):
            port_name = self.display_list[display_index]
            gfx_index = self.adapter_list[display_index].lower()
            vbt_panel_type = display_utility.get_vbt_panel_type(port_name, gfx_index)

            if "DP" in port_name and vbt_panel_type not in [display_utility.VbtPanelType.LFP_DP,
                                               display_utility.VbtPanelType.LFP_MIPI]:
                target_id = self.display_config.get_target_id(port_name, None, gfx_index)

                if target_id in usb4_displays and usb4_displays[target_id] == "USB4_DP_MONITOR":
                    logging.info(f"[PASS] : {gfx_index}:{port_name} detected as USB4")
                else:
                    usb4_detect_status = False
                    logging.error(f"[FAIL] : {gfx_index}:{port_name} not detected as USB4")

        return usb4_detect_status

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
