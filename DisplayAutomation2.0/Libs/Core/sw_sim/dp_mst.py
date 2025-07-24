###################################################################################################################
# @file     dp_mst.py
# @brief    Python Wrapper exposes API's related to DisplayPort DLL
# @author   Amanpreet Kaur Khurana
##########################################################################################################################

import copy
import ctypes
import logging
import os
import time

from Libs.Core import enum, driver_escape
from Libs.Core import system_utility
from Libs.Core.core_base import singleton
from Libs.Core.display_config import display_config
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import valsim_args

DISPLAYPORT_INTERFACE_VERSION = 0x1
OPERATION_FAILED = 0

MAX_ENCODERS = 10
BUFFER_SIZE = 512
LENGTH = 7
MAX_RAD = 7
MAX_NUM_BRANCHES = 15
MAX_NUM_DISPLAYS = 30


##
# @brief        Structure Definition to Get Master DisplayID and Slave DisplayID for Tiled Display.
class TargetIDsOfTiles(ctypes.Structure):
    _fields_ = [('MasterDisplayID', ctypes.c_ulong),
                ('SlaveDisplayID', ctypes.c_ulong)]


##
# @brief        RX Types.
class RXTypes(enum.Enum):
    _members_ = {
        'RxInvalidType': 0,
        'DP': 1,
        'HDMI': 2,
        'MAX_RX_TYPES': 3}


##
# @brief        DP Topology Types.
class DPType(enum.Enum):
    _members_ = {
        'InvalidTopology': 0,
        'SST': 1,
        'MST': 2}


##
# @brief        Plug Request Types.
class PLUG_REQUEST(enum.Enum):
    _members_ = {
        'PlugRequestInvalid': 0,
        'PlugSink': 1,
        'UnplugSink': 2,
        'UnPlugOldPlugNew': 3}


##
# @brief        Status Code for VerifyTopology function
class TOPOLOGY_STATUS_CODE(enum.Enum):
    _members_ = {
        'GFXSIM_DISPLAY_TOPOLOGIES_MATCHING': 0,
        'GFXSIM_DISPLAY_FAILURE': 1,
        'GFXSIM_DISPLAY_DISPLAYS_MISMATCH': 2,
        'GFXSIM_DISPLAY_BRANCHES_MISMATCH': 3,
        'GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT': 4}


##
# @brief        Structure Definition to Get Port Information.
class PortInfo(ctypes.Structure):
    _fields_ = [('PortNum', ctypes.c_uint),
                ('RxTypes', ctypes.c_int)]


##
# @brief        Structure Definition to Get Port Array Information.
class PortInfoArray(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('NumPorts', ctypes.c_uint),
                ('PortInfoArr', PortInfo * MAX_ENCODERS)]


##
# @brief        Structure Definition to DP Init Information.
class DPInitInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('PortNum', ctypes.c_uint),
                ('TopologyType', ctypes.c_int)]


##
# @brief        Structure Definition for MST Relative address
class MST_RELATIVEADDRESS(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('TotalLinkCount', ctypes.c_char),
                ('RemainingLinkCount', ctypes.c_char),
                ('RadSize', ctypes.c_char),
                ('Address', ctypes.c_char * LENGTH)]

    ##
    # @brief        Constructor for MST_RELATIVEADDRESS Structure
    # @param[in]    total_link_count: Optional[ctypes.c_char]
    #                   Represent the total number of links a sideband message traverses from message originator to the
    #               message target
    # @param[in]    remaining_link_count: Optional[ctypes.c_char]
    #                   Represent the remaining number of links a sideband message has to traverse to get to the target
    # @param[in]    rad_size: Optional[ctypes.char]
    #                   Number of valid bytes in the Address field
    # @param[in]    address: Optional[ctypes.c_char * LENGTH]
    #                   Holds the address of the device relative to the orignator of the sideband message
    def __init__(self, total_link_count=b'\x00', remaining_link_count=b'\x00', rad_size=b'\x00', address=b''):
        self.TotalLinkCount = total_link_count
        self.RemainingLinkCount = remaining_link_count
        self.RadSize = rad_size
        self.Address = address


##
# @brief        Structure Definition for Node Rad Info
class NODE_RAD_INFO(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('ThisNodeIndex', ctypes.c_ulong),
                ('ParentBranchIndex', ctypes.c_ulong),
                ('NodeRAD', MST_RELATIVEADDRESS)]

##
# @brief        Structure Definition for Branchdisp Rad Array
class BRANCHDISP_RAD_ARRAY(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('NumBranches', ctypes.c_ulong),
        ('BranchRADInfo', NODE_RAD_INFO * MAX_NUM_BRANCHES),
        ('NumDisplays', ctypes.c_ulong),
        ('DisplayRADInfo', NODE_RAD_INFO * MAX_NUM_DISPLAYS)
    ]


##
# @brief        Structure Definition for DPCD Info
class DPCDInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('PortNum', ctypes.c_ulong),
                ('Native', ctypes.c_bool),
                ('NodeRAD', MST_RELATIVEADDRESS),
                ('DPCPAddress', ctypes.c_ulong),
                ('ReadLength', ctypes.c_ulong)]


##
# @brief        Structure Definition to Port Low Power State
class S3S4_DP_PLUGUNPLUG_DATA(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('PlugOrUnPlugAtSource', ctypes.c_bool),
                ('TopologyAfterResume', ctypes.c_int)]


##
# @brief        Structure Definition to Port Low Power State
class GFXS3S4_PORT_PLUGUNPLUG_DATA(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('PortNum', ctypes.c_ulong),
                ('SinkPlugReq', ctypes.c_int),
                ('ConnectorInfoAfterResume', ctypes.c_char),
                ('DongleType', ctypes.c_uint),
                ('S3S4DPPlugUnplugData', S3S4_DP_PLUGUNPLUG_DATA)]


##
# @brief        Structure Definition to All Ports Low Power State
class GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('NumPorts', ctypes.c_ulong),
                ('S3S4PortPlugUnplugData', GFXS3S4_PORT_PLUGUNPLUG_DATA * MAX_ENCODERS)]


##
# @brief        Structure Definition to Get Tiled Information.
class TiledInformation(object):

    ##
    # @brief    Constructor
    def __init__(self):
        self.TiledStatus = False
        self.NoOfHorizontalTiles = 0
        self.NoOfVerticalTiles = 0
        self.HorizontalLocation = 0
        self.VerticalLocation = 0
        self.TileHorizontalSize = 0
        self.TileVerticalSize = 0
        self.EnclosureDetails = 0
        self.BezelInfo = 0
        self.HzRes = 0
        self.VtRes = 0
        self.TopBezelSize = 0
        self.BottomBezelSize = 0
        self.RightBezelSize = 0
        self.LeftBezelSize = 0
        self.HorizontalActive = 0
        self.VerticalActive = 0


##
# @brief        Status Code for VerifyTiledBytes function
class VERIFY_TILED_BYTES(enum.Enum):
    _members_ = {
        'TILED_TAG': 5,
        'NO_OF_HORIZONTAL_TILES_BYTE11': 11,
        'NO_OF_HORIZONTAL_TILES_BYTE9': 9,
        'NO_OF_VERTICAL_TILES_BYTE11': 11,
        'NO_OF_VERTICAL_TILES_BYTE9': 9,
        'HORIZONTAL_TILE_LOCATION_BYTE11': 11,
        'HORIZONTAL_TILE_LOCATION_BYTE10': 10,
        'VERTICAL_TILE_LOCATION_BYTE11': 11,
        'VERTICAL_TILE_LOCATION_BYTE10': 10,
        'HORIZONTAL_TILE_SIZE_BYTE12': 12,
        'HORIZONTAL_TILE_SIZE_BYTE13': 13,
        'VERTICAL_TILE_SIZE_BYTE14': 14,
        'VERTICAL_TILE_SIZE_BYTE15': 15,
        'HORIZONTAL_ACTIVE_BYTE38': 38,
        'HORIZONTAL_ACTIVE_BYTE37': 37,
        'VERTICAL_ACTIVE_BYTE46': 46,
        'VERTICAL_ACTIVE_BYTE45': 45,
        'DISPLAY_ENCLOSURE': 8,
        'BEZEL': 8,
        'TOP_BEZEL_SIZE': 17,
        'BOTTOM_BEZEL_SIZE': 18,
        'RIGHT_BEZEL_SIZE': 19,
        'LEFT_BEZEL_SIZE': 20,
        'DETAILED_TIMING_DESCRIPTOR': 30
    }


## 
# @brief        DisplayPort Class
@singleton
class DisplayPort(object):
    # This will contain the list of free DP PORT Type Name for all the curresponding Port Numbers Ex DP_B,DP_C, etc
    free_dp_ports = []

    # @brief    Display Port constructor.
    def __init__(self):
        # Load DisplayPort C library.
        self.display_port_dll = ctypes.cdll.LoadLibrary(
            os.path.join(test_context.TestContext.bin_store(), 'DisplayPort.dll'))

        ##
        # Create SystemUtility object
        self.system_utility = system_utility.SystemUtility()
        self.driver_interface_ = driver_interface.DriverInterface()

        # Intialize the CUI SDK
        status = self.init_sdk()
        if status:
            logging.info("Graphics CUI SDK Initialized Successfully")
        else:
            logging.error("Graphics CUI SDK Initialization Failed")

    ##
    # @brief        Plug DP display on the port specified
    # @param[in]    port_type - connector port type.
    # @param[in]    topology_type - topology to be applied
    # @param[in]    xml_file - encoded XML File
    # @param[in]    lowpower - True if Low Power State, False otherwise
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       retstatus - True if HPD applied successfully, False otherwise
    def setdp(self, port_type, topology_type, xml_file, lowpower, gfx_index='gfx_0'):
        # Initialize the DP Port
        status = True
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        retstatus = self.init_dp(port_type, topology_type)
        if retstatus is False:
            return retstatus
        # Parse and Send Topology details to Gfx Sim driver from user
        retstatus = self.parse_send_topology(port_type, topology_type, xml_file, lowpower)
        if retstatus is False:
            return retstatus

        # Connect DP 1.2 display(s) by issuing HPD
        retstatus = self.driver_interface_.set_hpd(adapter_info, port_type, True, 'NATIVE')
        if retstatus is False:
            return retstatus
        return status

    ##
    # @brief        Report out whether tiled display is plugged or not.
    # @param[in]    master_plug - True if master plug required, False otherwise
    # @param[in]    slave_plug - True if slave plug required, False otherwise
    # @param[in]    master_port_type - Master connector port type
    # @param[in]    slave_port_type - Slave connector port type
    # @param[in]    master_tile_edid - Master Tiled EDID Path
    # @param[in]    slave_tile_edid - Slave tile EDID Path
    # @param[in]    tile_dpcd - Tile DPCD Path
    # @param[in]    low_power - True if Low Power State, False otherwise
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       bool - True if both Master and Slave Plug are successful, False otherwise
    def plug_unplug_tiled_display(self, master_plug, slave_plug, master_port_type, slave_port_type, master_tile_edid,
                                  slave_tile_edid, tile_dpcd, low_power, gfx_index='gfx_0'):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        # Master Tiled Edid file absolute path.
        master_tile_edid_path = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE",
                                             master_tile_edid)
        # Load Slave Tiled Edid file absolute path.
        slave_tile_edid_path = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE", slave_tile_edid)
        # DPCD file absolute path.
        tile_dpcd_path = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE", tile_dpcd)

        if master_plug:
            master_plug_status = self.driver_interface_.simulate_plug(adapter_info, master_port_type,
                                                                      master_tile_edid_path, tile_dpcd_path, low_power)
        else:
            master_plug_status = self.driver_interface_.simulate_unplug(adapter_info, master_port_type, low_power)
        # Delay time for stable plug and enumeration
        time.sleep(5)
        if slave_plug:
            slave_plug_status = self.driver_interface_.simulate_plug(adapter_info, slave_port_type,
                                                                     slave_tile_edid_path, tile_dpcd_path, low_power)
        else:
            slave_plug_status = self.driver_interface_.simulate_unplug(adapter_info, slave_port_type, low_power)
        # Delay time for stable plug and enumeration
        time.sleep(5)
        logging.info("master_plug_status = %s slave_plug_status = %s" % (master_plug_status, slave_plug_status))
        return (master_plug_status and slave_plug_status)

    ##
    # @brief        Report out whether only master port is plugged or not/only slave port is unplugged or not.
    # @param[in]    action - Action to be performed on master port else slave port
    # @param[in]    master_port_type - connector port type for master port
    # @param[in]    slave_port_type - connector port type for slave port
    # @param[in]    master_tile_edid - Master Tiled EDID path
    # @param[in]    slave_tile_edid - Slave tile EDID path
    # @param[in]    tile_dpcd - Tile DPCD path
    # @param[in]    low_power - True if Low Power State, False otherwise
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       status - plug status
    def plug_master_or_unplug_slave_port(self, action, master_port_type, slave_port_type, master_tile_edid,
                                         slave_tile_edid,
                                         tile_dpcd, low_power, gfx_index='gfx_0'):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        # Master Tiled Edid file absolute path.
        master_tile_edid_path = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE",
                                             master_tile_edid)
        # DPCD file absolute path.
        tile_dpcd_path = os.path.join(test_context.TestContext.panel_input_data(), "DP_MST_TILE", tile_dpcd)

        if action == 'MASTER_PORT_PLUG':
            status = self.driver_interface_.simulate_plug(adapter_info, master_port_type, master_tile_edid_path,
                                                          tile_dpcd_path, low_power)
        else:
            status = self.driver_interface_.simulate_unplug(adapter_info, slave_port_type, low_power)
        # Delay time for stable plug/unplug and enumeration
        time.sleep(5)
        logging.info("GfxValSim Tiled panel plug/unplug status = %s" % status)
        return status

    ##
    # @brief        Retrieve display port interface version
    # @return       ver.value - Version value as INT.
    def display_port_interface_version(self):
        ver = ctypes.c_int()
        prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(ctypes.c_int))
        func = prototype(('GetDisplayPortInterfaceVersion', self.display_port_dll))
        func(ctypes.byref(ver))
        return ver.value

    ##
    # @brief        Get number of free DP ports
    # @return       int - Length of free dp ports
    def get_number_of_free_dp_ports(self):
        # Get the list for all free ports
        free_ports = display_config.get_free_ports()
        # filter out only DP ports from list of all free ports
        for port in free_ports:
            if port.startswith('DP_'):
                # Create a list of free DP port
                self.free_dp_ports.append(port)
        if 'DP_A' in self.free_dp_ports:
            self.free_dp_ports.remove('DP_A')

        logging.info(self.free_dp_ports)
        return len(self.free_dp_ports)

    ##
    # @brief        Get free DP port
    # @param[in]    index - Index of the DP Port
    # @return       str - Free DP port name
    def get_free_dp_port_type(self, index):
        return self.free_dp_ports[index]

    ##
    # @brief        Exposed API to verify DisplayPortUtility to initialize display port
    # @param[in]    port_type - connector port type
    # @param[in]    topology_type - Display Topology to be applied
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       retStatus - True if display port init is successful, False otherwise
    def init_dp(self, port_type, topology_type, gfx_index='gfx_0'):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        port_num = getattr(valsim_args.ValSimPort, port_type).value
        tp_type = eval("enum.%s" % (topology_type))
        # Create DP Info Object
        dp_info = DPInitInfo()
        dp_info.PortNum = port_num
        dp_info.TopologyType = tp_type
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool,
                                      ctypes.POINTER(GfxAdapterInfo), ctypes.c_uint,
                                      ctypes.POINTER(DPInitInfo))
        func = prototype(('DisplayportInit', self.display_port_dll))
        retStatus = func(ctypes.byref(adapter_info), ctypes.sizeof(GfxAdapterInfo),
                         ctypes.byref(dp_info))
        if not retStatus:
            gdhm.report_bug(
                title="[DP_MSTLib] Graphics simulation driver failed to initialize DP ports",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return retStatus

    ##
    # @brief        Exposed API to verify DisplayPortUtility to send the topology data to Gfx val simulation driver.
    # @param[in]    port_type - connector port type
    # @param[in]    topology_type - Display topology to be applied
    # @param[in]    xmlfile - encoded XML File.
    # @param[in]    lowpower - True if Low Power State, False otherwise
    # @return       retStatus - True if XML parsing is successful, False otherwise
    def parse_send_topology(self, port_type, topology_type, xmlfile, lowpower):
        xmlfile = xmlfile.encode()
        port_num = getattr(valsim_args.ValSimPort, port_type).value
        tp_type = eval("enum.%s" % (topology_type))
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_uint, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool)
        func = prototype(('ParseNSendTopology', self.display_port_dll))
        retStatus = func(port_num, tp_type, xmlfile, lowpower)
        if not retStatus:
            gdhm.report_bug(
                title="[DP_MSTLib] Parsing of xml or send to simulation driver by ParseNSendTopology failed",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return retStatus

    ##
    # @brief        Exposed API to verify DisplayPortUtility to set the HPD event
    # @param[in]    port_type - connector port type
    # @param[in]    attach_dettach - True if connector port has to be attached, False otherwise
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       bool - True if HPD is successful, False otherwise
    def set_hpd(self, port_type, attach_dettach, gfx_index='gfx_0'):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        return driver_interface.DriverInterface().set_hpd(adapter_info, port_type, attach_dettach, 'NATIVE')

    ##
    # @brief        Exposed API to Read DPCD from offset address
    # @param[in]    port_type - connector port type
    # @param[in]    native - True for Native DPCD read, False otherwise
    # @param[in]    length - length of DPCD Values to be read
    # @param[in]    addr - DPCD Offset
    # @param[in]    noderad - MST Relative address object
    # @return       (retStatus,regValue) - (True if DPCD read is successful False otherwise, register Value)
    def read_dpcd(self, port_type, native, length, addr, noderad):
        port_num = getattr(valsim_args.ValSimPort, port_type).value
        dpcd_args = DPCDInfo()
        size = ctypes.sizeof(DPCDInfo)
        dpcd_args.PortNum = port_num
        dpcd_args.Native = native
        dpcd_args.ReadLength = length
        dpcd_args.DPCPAddress = addr
        if noderad is not None:
            dpcd_args.NodeRAD = copy.deepcopy(noderad)
        reg_value = (ctypes.c_ulong * length)()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DPCDInfo), ctypes.c_ulong * length)
        func = prototype(('ReadDPCD', self.display_port_dll))
        retStatus = func(ctypes.byref(dpcd_args), reg_value)
        return retStatus, reg_value

    ##
    # @brief        Exposed API to verify MST Topology
    # @param[in]    port_type - connector port type
    # @return       retStatus - True if MST Topology is verified, False otherwise
    def verify_topology(self, port_type):
        port_num = getattr(valsim_args.ValSimPort, port_type).value
        prototype = ctypes.PYFUNCTYPE(ctypes.c_uint, ctypes.c_ulong)
        func = prototype(('VerifyMSTTopology', self.display_port_dll))
        retStatus = func(port_num)
        return retStatus

    ##
    # @brief        Exposed API to get MST Topology RAD
    # @param[in]    port_type - connector port type
    # @return       (retStatus, disp_rad) - (True if get MST Topology RAD is successful False otherwise,
    #                branchdisp rad array Object)
    def get_mst_topology_rad(self, port_type):
        port_num = getattr(valsim_args.ValSimPort, port_type).value
        disp_rad = BRANCHDISP_RAD_ARRAY()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_ulong, ctypes.POINTER(BRANCHDISP_RAD_ARRAY))
        func = prototype(('GetMSTTopologyRAD', self.display_port_dll))
        retStatus = func(port_num, ctypes.byref(disp_rad))
        if not retStatus:
            gdhm.report_bug(
                title="[DP_MSTLib] GetMSTTopologyRAD failed to retrieve RAD information",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return retStatus, disp_rad

    ##
    # @brief        Exposed API to attach or detach , branch or display in MST Topology
    # @param[in]    port_type - connector port type
    # @param[in]    attach_dettach - True if connector port has to be attached, False otherwise
    # @param[in]    noderad - MST Relative address object
    # @param[in]    xmlfile - encoded XML File
    # @param[in]    lowpower - True if Low Power State, False otherwise
    # @return       retStatus -  True if MST Partial Topology set is successful, False otherwise
    def set_mst_partial_topology(self, port_type, attach_dettach, noderad, xmlfile, lowpower):
        port_num = getattr(valsim_args.ValSimPort, port_type).value
        relative_address = MST_RELATIVEADDRESS()
        relative_address = copy.deepcopy(noderad)
        xmlfile = None if xmlfile is None else xmlfile.encode()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_ulong, ctypes.c_bool, ctypes.POINTER(MST_RELATIVEADDRESS),
                                      ctypes.c_char_p, ctypes.c_bool)
        func = prototype(('AddRemoveSubTopology', self.display_port_dll))
        retStatus = func(port_num, attach_dettach, ctypes.byref(relative_address), xmlfile, lowpower)
        if not retStatus:
            gdhm.report_bug(
                title="[Interfaces][DP_MST] AddRemoveSubTopology failed to attach/detach branch/display"
                      " from the current topology",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return retStatus

    ##
    # @brief        Exposed API to Plug or Unplug Topology during Lowe Power State.
    # @param[in]    num_of_ports - Number of connector ports
    # @param[in]    port_type - connector port type
    # @param[in]    sink_plugreq - Sink Plug
    # @param[in]    plug_unplug_atsource - True if plug, False otherwise
    # @param[in]    topology_after_resume - topology type used after Display is resumed.
    # @return       retStatus - True if low power state is applied, False otherwise
    def set_low_power_state(self, num_of_ports, port_type, sink_plugreq, plug_unplug_atsource, topology_after_resume):
        # get value from Class : Ports
        port_num = getattr(valsim_args.ValSimPort, port_type).value
        # get value from Enum : DPType
        topology_type = eval("enum.%s" % (topology_after_resume))
        # create variable of structure GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA
        lowpower_hpd_data = GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA()
        # populate structure GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA
        lowpower_hpd_data.NumPorts = num_of_ports
        for index in range(num_of_ports):
            lowpower_hpd_data.S3S4PortPlugUnplugData[index].PortNum = port_num
            lowpower_hpd_data.S3S4PortPlugUnplugData[index].SinkPlugReq = sink_plugreq
            lowpower_hpd_data.S3S4PortPlugUnplugData[
                index].S3S4DPPlugUnplugData.PlugOrUnPlugAtSource = plug_unplug_atsource
            lowpower_hpd_data.S3S4PortPlugUnplugData[index].S3S4DPPlugUnplugData.TopologyAfterResume = topology_type
            lowpower_hpd_data.S3S4PortPlugUnplugData[index].S3S4DPPlugUnplugData.DongleType = valsim_args.DongleType.Default
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GFXS3S4_ALLPORTS_PLUGUNPLUG_DATA))
        func = prototype(('SetLowPowerState', self.display_port_dll))
        retStatus = func(ctypes.byref(lowpower_hpd_data))
        if not retStatus:
            gdhm.report_bug(
                title="[DP_MSTLib] SetLowPowerState failed to plug/unplug display in low power mode",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return retStatus

    ##
    # @brief        Exposed API to get TiledDisplayInformation
    # @param[in]    display_id - target ID
    # @return       tiled_obj - TiledInformation Class object.
    def get_tiled_display_information(self, display_id):
        tiled_obj = TiledInformation()
        blocktagbyte = []
        # Read the EDID for Given Display ID
        edid_flag, display_edid, _ = driver_escape.get_edid_data(display_id)
        if not edid_flag:
            logging.error(f"Failed to get EDID data for target_id : {display_id}")
            assert edid_flag, "EDID read failed"
        DID_EXTENSION_BLOCK_TAG = 0X70
        didStatus = False
        # EDID data 126 byte represents Extention block availability and EDID data 128 byte represnets CEA block and
        # 131 byte - 6th bit represents audio capability
        no_of_extension_blocks = display_edid[126]  # Refer's to Extension block count in BaseBlock
        if no_of_extension_blocks >= 1:
            for extension_block_index in range(1, no_of_extension_blocks + 1):
                if display_edid[(extension_block_index) * 128] == DID_EXTENSION_BLOCK_TAG:
                    for i in range(0, 127):
                        hex(display_edid[(extension_block_index) * 128 + i])
                        blocktagbyte.append(display_edid[(extension_block_index) * 128 + i])
                    didStatus = True
                    break

        if didStatus is True:
            # Check whether the Tile details are present in the DID extension Block or not
            # 0x12 -> In case of DID 1.3
            # 0x28 -> In case of DID 2.0
            if hex(blocktagbyte[enum.TILED_TAG]) == '0x12' or hex(blocktagbyte[enum.TILED_TAG]) == '0x28':

                TiledStatus = True
                tiled_obj.TiledStatus = TiledStatus
                # logging.debug("Status %s",TiledStatus)

                # No.of Horizontal Tiles
                hTile = ((((blocktagbyte[enum.NO_OF_HORIZONTAL_TILES_BYTE11] & 0xC0) >> 6) << 4) | (
                        (blocktagbyte[enum.NO_OF_HORIZONTAL_TILES_BYTE9] & 0xF0) >> 4)) + 1
                NoOfHorizontalTiles = hTile
                tiled_obj.NoOfHorizontalTiles = NoOfHorizontalTiles
                # logging.debug(" No. of Horizontal Tiles: {} ".format(NoOfHorizontalTiles))

                # No.of Vertical Tiles
                vTile = ((blocktagbyte[enum.NO_OF_VERTICAL_TILES_BYTE11] & 0x30) | (
                        blocktagbyte[enum.NO_OF_VERTICAL_TILES_BYTE9] & 0X0F)) + 1
                NoOfVerticalTiles = vTile
                tiled_obj.NoOfVerticalTiles = NoOfVerticalTiles
                # logging.debug(" No. of Vertical Tiles: {} ".format(NoOfVerticalTiles))

                # Horizontal Tile Location
                hLocation = ((((blocktagbyte[enum.HORIZONTAL_TILE_LOCATION_BYTE11] & 0x0C) >> 2) << 4) | (
                        (blocktagbyte[enum.HORIZONTAL_TILE_LOCATION_BYTE10] & 0xF0) >> 4)) + 1
                HorizontalLocation = hLocation
                tiled_obj.HorizontalLocation = HorizontalLocation
                # logging.debug(" Horizontal Tile Location: {} ".format(HorizontalLocation))

                # Vertical Tile Location
                vLocation = (((blocktagbyte[enum.VERTICAL_TILE_LOCATION_BYTE11] & 0x03) << 4) | (
                    (blocktagbyte[enum.VERTICAL_TILE_LOCATION_BYTE10] & 0x0F))) + 1
                VerticalLocation = vLocation
                tiled_obj.VerticalLocation = VerticalLocation
                # logging.debug(" Vertical Tile Location: {} ".format(VerticalLocation))

                # Tile Horizontal Size
                hTileSize = (blocktagbyte[enum.HORIZONTAL_TILE_SIZE_BYTE12] | (
                        blocktagbyte[enum.HORIZONTAL_TILE_SIZE_BYTE13] << 8)) + 1
                TileHorizontalSize = hTileSize
                tiled_obj.TileHorizontalSize = TileHorizontalSize
                # logging.debug(" Tile Horizontal Size : {} ".format(TileHorizontalSize))

                # Tile Vertical Size
                vTileSize = (blocktagbyte[enum.VERTICAL_TILE_SIZE_BYTE14] | (
                        blocktagbyte[enum.VERTICAL_TILE_SIZE_BYTE15] << 8)) + 1
                TileVerticalSize = vTileSize
                tiled_obj.TileVerticalSize = TileVerticalSize
                # logging.debug(" Tile Vertical Size : {} ".format(TileVerticalSize))

                # Horizontal Resolution
                hzResolution = hTile * hTileSize
                HzRes = hzResolution
                tiled_obj.HzRes = HzRes
                # logging.debug(" Horizontal Resolution: {} ".format(HzRes))

                # Vertical Resolution
                vtResolution = vTile * vTileSize
                VtRes = vtResolution
                tiled_obj.VtRes = VtRes
                # logging.debug(" Vertical Resolution: {} ".format(VtRes))

                # Tiled Capability
                # Physical Display Enclosure
                displayEnclosure = (blocktagbyte[enum.DISPLAY_ENCLOSURE] & 0x80) >> 7
                EnclosureDetails = displayEnclosure
                tiled_obj.EnclosureDetails = EnclosureDetails
                # logging.debug(" Physical enclosure details : {} ".format(EnclosureDetails))

                # Bezel Info
                bezel = (blocktagbyte[enum.BEZEL] & 0x40) >> 6
                BezelInfo = bezel
                tiled_obj.BezelInfo = BezelInfo
                if bezel == 1:
                    # logging.debug(" Bezel Info is available.")

                    # Top Bezel Size
                    topBezelSize = blocktagbyte[enum.TOP_BEZEL_SIZE]
                    TopBezelSize = topBezelSize
                    tiled_obj.TopBezelSize = TopBezelSize
                    # logging.debug("  Top Bezel Size : {} ".format(TopBezelSize))

                    # Bottom Bezel Size
                    bottomBezelSize = blocktagbyte[enum.BOTTOM_BEZEL_SIZE]
                    BottomBezelSize = bottomBezelSize
                    tiled_obj.BottomBezelSize = BottomBezelSize
                    # logging.debug(" Bottom Bezel Size : {} ".format(BottomBezelSize))

                    # Right Bezel Size
                    rightBezelSize = blocktagbyte[enum.RIGHT_BEZEL_SIZE]
                    RightBezelSize = rightBezelSize
                    tiled_obj.RightBezelSize = RightBezelSize
                    # logging.debug(" Right Bezel Size : {} ".format(RightBezelSize))

                    # Left Bezel Size
                    leftBezelSize = blocktagbyte[enum.LEFT_BEZEL_SIZE]
                    LeftBezelSize = leftBezelSize
                    tiled_obj.LeftBezelSize = LeftBezelSize
                    # logging.debug("  Left Bezel Size : {} ".format(LeftBezelSize))
                else:
                    logging.debug("Bezel Info not available. ")

                # Check whether the Detailed Timing Descriptor Block is present in the DID Extension Block of the EDID or not
                # 0x3 -> In case of DID 1.3
                # 0x22 -> In case of DID 2.0
                if hex(blocktagbyte[enum.DETAILED_TIMING_DESCRIPTOR]) == '0x3' or hex(blocktagbyte[enum.DETAILED_TIMING_DESCRIPTOR]) == '0x22':

                    # Horizontal Active
                    hActive = ((blocktagbyte[enum.HORIZONTAL_ACTIVE_BYTE38] << 8) | blocktagbyte[
                        enum.HORIZONTAL_ACTIVE_BYTE37]) + 1
                    HorizontalActive = hActive
                    tiled_obj.HorizontalActive = HorizontalActive
                    # logging.debug(" Horizontal Active: {} ".format(HorizontalActive))

                    # Vertical Active
                    vActive = ((blocktagbyte[enum.VERTICAL_ACTIVE_BYTE46] << 8) | blocktagbyte[
                        enum.VERTICAL_ACTIVE_BYTE45]) + 1
                    VerticalActive = vActive
                    tiled_obj.VerticalActive = VerticalActive
                    # logging.debug(" Vertical Active : {} ".format(VerticalActive))
                else:
                    HorizontalActive = 0
                    VerticalActive = 0
                    tiled_obj.HorizontalActive = HorizontalActive
                    tiled_obj.VerticalActive = VerticalActive
                    # logging.debug(" Horizontal Active: {} ".format(HorizontalActive))
                    # logging.debug(" Vertical Active : {} ".format(VerticalActive))
                return tiled_obj
            else:
                logging.debug(
                    " Display does not support tiled information, only DID Extension Block is present in the EDID.")
                return tiled_obj
        else:
            TiledStatus = "FALSE"
            logging.debug(" Status: {} ".format(TiledStatus))
            logging.debug(" Neither the DID Extension Block, nor the Tiled information is present in the EDID.")
            return tiled_obj

    ##
    # @brief        Exposed API to initialize CUI SDK
    # @return       conn_flag - True if SDK initialized, False otherwise
    def init_sdk(self):
        conn_flag = True

        # Initialize CUI SDK only for legacy platforms.
        # Return True for all other platforms.
        if self.system_utility.is_ddrw() is False:
            prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
            func = prototype(('InitializeCUISDK', self.display_port_dll))
            conn_flag = func()

        return conn_flag

    ##
    # @brief        Exposed API to un-initialize CUI SDK
    # @return       conn_flag - True if SDK is uninitialized, False otherwise
    def uninitialize_sdk(self):
        conn_flag = True

        # Un-initialize CUI SDK only for legacy platforms.
        # Return True for all other platforms.
        if self.system_utility.is_ddrw() is False:
            prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
            func = prototype(('UninitializeCUISDK', self.display_port_dll))
            conn_flag = func()

        return conn_flag
