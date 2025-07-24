#######################################################################################################################
# @file         context.py
# @brief        Context APIs provide interface to get live test context, update the context after events such as
#               modeset, driver restart, power events etc and an API to log the live context about all the displays
# @author       Soorya R
#######################################################################################################################
import os
import logging
import platform
import subprocess
from enum import Enum
from typing import Dict
from typing import List
from dataclasses import *
from Libs.Core import registry_access
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_struct as config_struct
from Libs.Core.core_base import singleton
from Libs.Core.sw_sim import driver_interface
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.state_machine_manager import StateMachine
import re

LEGACY_PLATFORMS = ['SKL', 'KBL', 'CFL', 'CML', 'WHL', 'GLK', 'CNL', 'APL']


##
# @brief        ExecutionEnv Enum
class ExecutionEnv(Enum):
    POST_SI = 0,
    PRE_SI_SIM = 1,
    PRE_SI_EMU = 2


##
# @brief        GfxDriverType Enum
class GfxDriverType(Enum):
    LEGACY = 0,
    YANGRA = 1


##
# @brief        CmdLineDisplayAttributes Class
@dataclass()
class CmdLineDisplayAttributes:
    index: int = 0,
    connector_port: str = None,
    edid_name: str = None,
    dpcd_name: str = None,
    panel_index: str = None,
    connector_port_type: str = None,
    is_lfp: bool = False,
    gfx_index: str = None


##
# @brief        CmdLineParams Class
@dataclass
class CmdLineParams:
    topology: str = None
    file_name: str = None
    log_level: str = None
    test_custom_tags: Dict[str, list] = field(default_factory=dict)
    display_details: List[CmdLineDisplayAttributes] = field(default_factory=list)


##
# @brief        PathInfo Class
class PathInfo:
    root_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    test_store_path: str = os.path.join(root_path, 'TestStore')
    bin_path: str = os.path.join(root_path, 'Bin')
    log_path: str = os.path.join(root_path, 'Logs')
    panel_input_data_path: str = os.path.join(test_store_path, 'PanelInputData')


##
# @brief        TestParams Class
@dataclass
class TestParams:
    test_name: str = None
    feature_name: str = None
    path_info: PathInfo = PathInfo()
    cmd_params: CmdLineParams = None
    exec_env: ExecutionEnv = None

    # @todo : TBD - Assess requirement and implement
    # env_settings = None
    # result: bool = None
    # log_level = None
    # reboot_state = None

    ##
    # @brief        Overridden repr method
    # @return       str - Test Details
    def __repr__(self):
        return "\n Test Params : TestName = {0} \t Featurename = {1} \t " \
               "ExecutionEnv = {2}\n".format(self.test_name, self.feature_name, self.exec_env)

    ##
    # @brief        Overridden str method
    # @return       str - Test Params and Enivornment Details
    def __str__(self):
        return "\n Test Params : TestName = {0} \t Featurename = {1} \t " \
               "ExecutionEnv = {2}\n".format(self.test_name, self.feature_name, self.exec_env)


##
# @brief        Panel Class
@dataclass
class Panel:
    # Ctype Struct
    display_and_adapterInfo: config_struct.DisplayAndAdapterInfo = None
    # DisplayAttributes
    target_id: int = None
    source_id: int = None
    is_active: bool = None
    is_lfp: bool = None
    pipe: int = None
    transcoder: int = None
    connector_port_type: str = None
    port_type: str = None

    ##
    # @brief        Overridden repr method
    # @return       str - Panel Details
    def __repr__(self):
        return "\n Panel : TargetID = {0} \t SourceID = {1} \t Connector Port Type = {2} \t" \
               " Pipe = {3} \t Is_LFP={4} \t IsActive={5}".format(self.connector_port_type, self.target_id,
                                                                  self.source_id, self.pipe, self.is_lfp,
                                                                  self.is_active)

    ##
    # @brief        Overridden str method
    # @return       str - Panel Details
    def __str__(self):
        return "\n Panel : TargetID={0} \t SourceID={1} \t ConnectorPortType={2} \t Pipe={3} \t Transcoder={4} \t " \
               "Is_LFP={5} \t IsActive={6} \t PortType={7} \t Feature Caps YCbCr :  FeatureCaps HDR :".format(
            self.target_id, self.source_id,
            self.connector_port_type, self.pipe,
            self.transcoder,
            self.is_lfp,
            self.is_active, self.port_type)

##
# @brief        OS Class
@dataclass
class OsInfo:
    # Ctype Struct
    build_number: str = None
    build_revision_number: str = None

    ##
    # @brief        Overridden str method
    # @return       str - OS details
    def __str__(self):
        return "build_number = {0} \t build_revision_number = {1}".format(self.build_number, self.build_revision_number)

    ##
    # @brief        Overridden repr method
    # @return       str - OS Details
    def __repr__(self):
        return "build_number = {0} \t build_revision_number = {1}".format(self.build_number, self.build_revision_number)


##
# @brief        Adapter Class
@dataclass
class Adapter:
    # Ctype Struct
    adapter_info: GfxAdapterInfo = None
    # Adapter Attributes
    gfx_index: str = None
    platform: str = None
    platform_type: str = None
    gfx_status: int = None
    cpu_stepping: str = None
    supported_ports: List = field(default_factory=list)
    free_ports: List = field(default_factory=list)
    panels: Dict[str, Panel] = field(default_factory=dict)

    # @todo : TBD - Assess requirement and implement
    # is_dod: bool = None

    ##
    # @brief        Overridden str method
    # @return       str - Adapter Details
    def __str__(self):
        return "\n Adapter : Gfx_Index = {0}\t Platform = {1}\t PlatformType = {2} \t CPU Stepping = {3} " \
               "\tSupportedPorts = {4} \t FreePorts = {5}".format(self.gfx_index, self.platform,
                                                                  self.platform_type, self.cpu_stepping,
                                                                  self.supported_ports, self.free_ports)

    ##
    # @brief        Overridden repr method
    # @return       str - Adapter Details
    def __repr__(self):
        return "\n Adapter : Gfx_Index = {0}\t Platform = {1}\t PlatformType = {2}".format(self.gfx_index,
                                                                                           self.platform,
                                                                                           self.platform_type)


##
# @brief        Context Class
@singleton
class Context:
    ##
    # @brief        Constructor
    def __init__(self):
        self.__test: TestParams = TestParams()
        self.__adapters: Dict[str, Adapter] = dict()
        self.StateMachine_ = StateMachine()
        self.__os_info: OsInfo = OsInfo()

    ##
    # @brief        test method
    # @return       __test - Test Instance
    @property
    def test(self):
        return self.__test

    ##
    # @brief        os_info
    # @return       os information
    @property
    def os_info(self):
        self.__get_os_info()
        return self.__os_info

    ##
    # @brief        Adapter Initialization
    # @return       __adapters - Adapter Instance
    @property
    def adapters(self):
        if self.StateMachine_.init_adapters:
            self.init_adapter_context()
            self.StateMachine_.reset_init_adapters()
        if self.StateMachine_.adapter_display_change:
            self.update_adapter_display_context()
            self.StateMachine_.reset_adapter_display_change()
        if self.StateMachine_.display_inactive_change:
            self.update_inactive_display_context()
            self.StateMachine_.reset_display_inactive_change()
        if self.StateMachine_.adapter_state_change:
            for gfx_index, state in self.StateMachine_.adapter_state_dict.items():
                self.__adapters[gfx_index].gfx_status = state
            self.StateMachine_.reset_adapter_state_change()

        return self.__adapters

    ##
    # @brief        Initialize Test Context
    # @param[in]    cmd_params - Command Line Parameters
    # @return       None
    def init_test_context(self, cmd_params: CmdLineParams):
        self.__test.cmd_params = cmd_params
        self.__test.test_name = os.path.basename(cmd_params.file_name).split(".")[0]
        self.__test.feature_name = os.path.basename(os.path.dirname(cmd_params.file_name))
        self.__test.exec_env = self.__get_execution_environment_type()
        # @todo : Env setting dict

    ##
    # @brief        Get Execution Environment Type
    # @return       ExecutionEnv - Execution Environment PostSI or PreSI based on Value and registry Type
    def __get_execution_environment_type(self):
        # Read Reg key IsDisplayPreSilicon.
        key_name = "IsDisplayPreSilicon"
        reg_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, r"SYSTEM\Setup")
        value, reg_type = registry_access.read(args=reg_args, reg_name=key_name)
        if value is None and reg_type is None:
            return ExecutionEnv.POST_SI
        elif value == 1:
            return ExecutionEnv.PRE_SI_SIM
        # @todo : Currently the PreSiBKC updates this registry as 1 for both SIM & EMU
        #        Need to update requirement to identify EMU/PIPE 2D uniquely
        # elif value == 2:
        #    return ExecutionEnv.PRE_SI_EMU
        else:
            return ExecutionEnv.POST_SI

    ##
    # @brief        Initialize Adapter Display Context
    # @return       None
    def __init_adapter_display_context(self):
        self.init_adapter_context()
        # Build panel list for each adapter
        self.__init_display_context()

    ##
    # @brief        Initialize Adapter Context
    # @return       None
    def init_adapter_context(self):
        # List of Adapters
        gfx_adapter_details = display_config.DisplayConfiguration().get_all_gfx_adapter_details()
        for adapter_index in range(gfx_adapter_details.numDisplayAdapter):
            gfx_index = str(gfx_adapter_details.adapterInfo[adapter_index].gfxIndex)
            platform = gfx_adapter_details.adapterInfo[adapter_index].get_platform_info().PlatformName
            platform_type = GfxDriverType.LEGACY if platform in LEGACY_PLATFORMS else GfxDriverType.YANGRA
            cpustepping = self.__get_cpu_stepping()
            adapter = Adapter(adapter_info=gfx_adapter_details.adapterInfo[adapter_index],
                              gfx_index=gfx_index,
                              platform=platform,
                              platform_type=platform_type,
                              gfx_status=gfx_adapter_details.adapterInfo[adapter_index].isActive,
                              cpu_stepping=cpustepping,
                              supported_ports=driver_interface.DriverInterface().get_supported_ports(gfx_index),
                              free_ports=display_config.get_free_ports(gfx_index))
            logging.info(str(adapter))
            self.__adapters[gfx_index] = adapter

    ##
    # @brief        Get CPU Stepping
    # @return       processor_info - If Caption found in Keys, None Otherwise
    def __get_cpu_stepping(self):
        output = platform.processor()
        std_out = re.compile(r'[\r\n]').sub(" ", output)
        # search for the numbers after the match of "Stepping "
        match_output = re.match(r".*Stepping (?P<Stepping>[0-9]+)", std_out)
        if match_output is None:
            logging.error(f"FAILED to get info for CPU Stepping. Output= {output}")
            return None
        return match_output.group("Stepping")

    ##
    # @brief        Get OS Info
    # @return       os_info
    def __get_os_info(self):
        if self.__os_info.build_number is not None:
            return self.__os_info
        output = os.popen('ver.exe').read().replace('\n', '')
        result = re.findall(r"\b\d+\.\d+\.\d+\.\d+\b", output)[0].split(".")
        if result and len(result) >= 4:
            self.__os_info.build_number = result[2]
            self.__os_info.build_revision_number = result[3]

    ##
    # @brief        Initialize Display Context
    # @return       None
    def __init_display_context(self):
        # List of displays
        enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
        if enumerated_displays is None or enumerated_displays.Count < 1:
            logging.info("Either enumerated displays is none or count is <1")
            return
        for index in range(enumerated_displays.Count):
            adapter_index = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            display_adapterinfo = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo
            port = str(CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType))
            ##
            # Update the Pipe and Transcoder information iff both Adapter and Display are active
            if display_adapterinfo.adapterInfo.isActive and enumerated_displays.ConnectedDisplays[
                index].IsActive and port not in ['DispNone', 'VIRTUALDISPLAY', 'COLLAGE_0', 'COLLAGE_1', 'COLLAGE_2']:
                from Libs.Feature.display_engine.de_base.display_base import DisplayBase
                logging.debug("Port {0}".format(port))
                try:
                    display_base_obj = DisplayBase(port, platform=self.__adapters[adapter_index].platform,
                                                   gfx_index=adapter_index)
                    trans, pipe = display_base_obj.get_transcoder_and_pipe(port, adapter_index)
                    pipe = chr(int(pipe) + 65)
                except Exception as e:
                    logging.error("Exception : {0}".format(e))
                    trans, pipe = (-1, -1)

                from Libs.Core import display_utility
                try:
                    is_lfp = display_utility.get_vbt_panel_type(port, adapter_index) in \
                             [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]
                except Exception as e:
                    logging.error("Exception : {0}".format(e))
                    is_lfp = False

                panel_info = Panel(
                    display_and_adapterInfo=display_adapterinfo,
                    target_id=enumerated_displays.ConnectedDisplays[index].TargetID,
                    source_id=enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.SourceID,
                    is_active=enumerated_displays.ConnectedDisplays[index].IsActive,
                    connector_port_type=port,
                    port_type=enumerated_displays.ConnectedDisplays[index].PortType,
                    is_lfp=is_lfp,
                    pipe=pipe,
                    transcoder=trans
                )
                logging.info(str(panel_info))

                self.__adapters[adapter_index].panels[panel_info.connector_port_type] = panel_info

    ##
    # @brief        Update Adapter Display Context
    # @return       None
    def update_adapter_display_context(self):
        self.__adapters = {}
        self.__init_adapter_display_context()

    ##
    # @brief        Update Display Context
    # @return       None
    def update_inactive_display_context(self):
        for gfx_index, adapter in self.__adapters.items():
            for display, display_attributes in adapter.panels.items():
                display_attributes.is_active = False

    ##
    # @brief        Overridden str method
    # @return       context_string - Context String with Adapter Configuration
    def __str__(self):
        context_string = ""
        for gfx_index, adapter in self.__adapters.items():
            context_string += str(adapter)
            for display, display_attributes in adapter.panels.items():
                context_string += str(display_attributes)
        return context_string

    ##
    # @brief        Overridden repr method
    # @return       context_repr - Context Representation of Graphics Driver
    def __repr__(self):
        context_repr = ""
        for gfx_index, adapter in self.__adapters.items():
            context_repr += repr(adapter)
            for display, display_attributes in adapter.panels.items():
                context_repr += repr(display_attributes)
        return context_repr
