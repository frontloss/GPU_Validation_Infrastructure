#######################################################################################################################
# @file         dsc_definitions.py
# @brief        Contains PPS, RC Threshold, RC Range Parameter Structures as Per our H/W Registers.
#               Contains DSCPictureParameterSet, DSCRequiredPictureParameterSet, RcRangeParameters Classes Which Holds
#               All the Different Register Fields Programmed by Driver Which Forms as the 128byte Header in Each of the
#               Compressed Frame.
#
# @author       Praburaj Krishnan
#######################################################################################################################

from __future__ import annotations

import copy
import ctypes
import logging
from dataclasses import dataclass
from typing import List, Tuple, Optional

from Libs.Core import display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_struct import TARGET_ID
from Libs.Core.sw_sim.dp_mst import DisplayPort, NODE_RAD_INFO, MST_RELATIVEADDRESS
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.display_port.dp_enum_constants import VirtualDisplayportPeerDevice
from Libs.Feature.display_port.dp_helper import DPHelper
from Libs.Feature.vdsc.dsc_enum_constants import DSCEngine, DisplayType, DPCDOffsets
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from registers.mmioregister import MMIORegister


##
# @brief        This Class Holds All the Useful Information About DSC Display Which Would be Used Across All the DSC
#               Programming Verification.
class DSCDisplay:

    ##
    # @brief        Constructor to Initialize the Instance Variables Using the Port Name and Target id of the Display.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port_name: str
    #                   Port Name in Which the DSC Display is Plugged.
    # @param[in]    slave_port_name: Optional[str]
    #                   Contains the slave port name of SST Tiled display. Empty string otherwise.
    def __init__(self, gfx_index: str, port_name: str, slave_port_name: Optional[str] = '') -> None:
        self.gfx_index: str = gfx_index
        self.port_name: str = port_name
        self.slave_port: str = slave_port_name
        self.display_type: DisplayType = DisplayType.UNKNOWN_DISPLAY
        self.is_mst_display: bool = False
        self.is_sst_sbm_display: bool = False
        self.branch_rad_info: NODE_RAD_INFO = NODE_RAD_INFO()
        self.display_rad_info: NODE_RAD_INFO = NODE_RAD_INFO()
        self.virtual_dp_peer_device = VirtualDisplayportPeerDevice.VIRTUAL_DP_PEER_DEVICE_NOT_SUPPORTED
        self.target_id: int = 0
        self.pipe_list: List[str] = []
        self.transcoder_list: List[str] = []
        self.ddi_list: List[str] = []

    ##
    # @brief        Initialize display helps in initializing all the properties of the displays.
    # @return       None
    def initialize_display(self) -> None:
        self.set_display_type()
        self.set_mst_capabilities()
        self.set_branch_and_display_rad()
        self.set_virtual_dp_peer_device_type()
        self.set_target_id()
        self.set_pipe_ddi_transcoder()

    ##
    # @brief        Computed Property Which Returns Platform Name in Capital Based on gfx_index. E.g. 'ICLLP'
    # @return       Returns Platform name in Caps.
    @property
    def platform(self) -> str:
        index = int(self.gfx_index[-1])
        return DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName

    ##
    # @brief        This property checks if the tiled display bit is set in the target id to see if the plugged display
    #               is a tiled display or not
    # @return       Returns True if it's a Tiled display False otherwise
    @property
    def is_tiled_display(self) -> bool:
        target_id = TARGET_ID(Value=self.target_id)
        is_tiled_display = target_id.TiledDisplay == 1
        return is_tiled_display

    ##
    # @brief        Set Display Type Based on the Port on Which the Display is Plugged.
    # @return       None
    def set_display_type(self) -> None:
        port_name = self.port_name.upper()

        if display_utility.get_vbt_panel_type(port_name, 'gfx_0') == display_utility.VbtPanelType.LFP_DP:
            self.display_type = DisplayType.EMBEDDED_DISPLAY_PORT
        elif port_name.startswith('DP'):
            self.display_type = DisplayType.DISPLAY_PORT
        elif port_name.startswith('MIPI'):
            self.display_type = DisplayType.MIPI_DISPLAY
        elif port_name.startswith('HDMI'):
            self.display_type = DisplayType.HDMI_DISPLAY

    ##
    # @brief        Sets whether the display is capable of just handling sideband message or it can handle MST mode by
    #               reading SINGLE_STREAM_SIDEBAND_MESSAGE_SUPPORT and MST_CAP bit in the MSTM_CAP DPCD register.
    # @return       None
    def set_mst_capabilities(self) -> None:
        mstm_cap = DSCHelper.read_dpcd(self.gfx_index, self.port_name, DPCDOffsets.MSTM_CAP)[0]
        self.is_mst_display = bool(DSCHelper.extract_bits(mstm_cap, 1, 0))
        self.is_sst_sbm_display = mstm_cap == 0x2

    ##
    # @brief        Sets the branch and display relative address if it's a MST Display
    # @returns      None
    def set_branch_and_display_rad(self) -> None:
        if self.is_mst_display or self.is_sst_sbm_display:
            display_port = DisplayPort()
            is_success, topology_rad = display_port.get_mst_topology_rad(self.port_name)

            if not is_success and topology_rad.NumBranches != 1 and topology_rad.NumDisplays != 1:
                raise NotImplementedError("Multiple branch and multiple devices cases are not handled")

            # Create the copy of the branch device.
            self.branch_rad_info.ThisNodeIndex = topology_rad.BranchRADInfo[0].ThisNodeIndex
            self.branch_rad_info.ParentBranchIndex = topology_rad.BranchRADInfo[0].ParentBranchIndex
            self.branch_rad_info.NodeRAD = MST_RELATIVEADDRESS(topology_rad.BranchRADInfo[0].NodeRAD.TotalLinkCount,
                                                               topology_rad.BranchRADInfo[0].NodeRAD.RemainingLinkCount,
                                                               topology_rad.BranchRADInfo[0].NodeRAD.RadSize,
                                                               topology_rad.BranchRADInfo[0].NodeRAD.Address)

            # Create a copy of the display device
            self.display_rad_info.ThisNodeIndex = topology_rad.DisplayRADInfo[0].ThisNodeIndex
            self.display_rad_info.ParentBranchIndex = topology_rad.DisplayRADInfo[0].ParentBranchIndex
            self.display_rad_info.NodeRAD = MST_RELATIVEADDRESS(topology_rad.DisplayRADInfo[0].NodeRAD.TotalLinkCount,
                                                                topology_rad.DisplayRADInfo[
                                                                    0].NodeRAD.RemainingLinkCount,
                                                                topology_rad.DisplayRADInfo[0].NodeRAD.RadSize,
                                                                topology_rad.DisplayRADInfo[0].NodeRAD.Address)

    ##
    # @brief        Sets the type of virtual dp peer device
    # @return       None
    def set_virtual_dp_peer_device_type(self) -> None:
        if self.is_mst_display or self.is_sst_sbm_display:
            port_number = DPHelper.get_port_number(self.display_rad_info.NodeRAD)
            is_logical_port = DPHelper.is_logical_port(port_number)
            if is_logical_port:
                self.virtual_dp_peer_device = VirtualDisplayportPeerDevice.VIRTUAL_DP_SINK_PEER_DEVICE

    ##
    # @brief        Private Member Function to Sets the Target id of the Display by Using the Port and Enumerated
    #               Display Information.
    # @return       None
    def set_target_id(self) -> None:
        display_config = DisplayConfiguration()
        enumerated_displays = display_config.get_enumerated_display_info()
        self.target_id = display_config.get_target_id(self.port_name, enumerated_displays)

    ##
    # @brief        Private Member Function to Set Pipe, Transcoder and DDI Information About the Display.
    # @return       None
    def set_pipe_ddi_transcoder(self) -> None:
        display_base = DisplayBase(self.port_name)

        pipe_ddi_transcoder: Tuple[str, str, str] = display_base.GetPipeDDIAttachedToPort(self.port_name, True)
        self.pipe_list.append(pipe_ddi_transcoder[0].split('_')[-1].upper())
        self.ddi_list = pipe_ddi_transcoder[1].split('_')[-1].upper()
        self.transcoder_list.append(pipe_ddi_transcoder[2].split('_')[-1].upper())

        if self.slave_port != '':
            pipe_ddi_transcoder: Tuple[str, str, str] = display_base.GetPipeDDIAttachedToPort(self.slave_port, True)
            self.pipe_list.append(pipe_ddi_transcoder[0].split('_')[-1].upper())
            self.ddi_list = pipe_ddi_transcoder[1].split('_')[-1].upper()
            self.transcoder_list.append(pipe_ddi_transcoder[2].split('_')[-1].upper())

    ##
    # @brief        Public Member Function to Update the Pipe List if the Display Operated in Pipe Ganged Mode.
    # @param[in]    no_of_pipes_required: int
    #                   Required Number of Pipes to Drive the Display.
    # @return       None
    def update_pipe_list(self, no_of_pipes_required: int) -> None:
        if (len(self.pipe_list) == no_of_pipes_required) is False:
            for _ in range(no_of_pipes_required - 1):
                adjacent_pipe: str = DSCDisplay._get_adjacent_pipe(self.pipe_list[-1])
                self.pipe_list.append(adjacent_pipe)

    ##
    # @brief        Public Member Function to Update the Transcoder List if the Display Uses Multiple Transcoders.
    # @param[in]    transcoder: str
    #                   Name of the Transcoder Which the Display is Using.
    # @return       None
    def update_transcoder_list(self, transcoder: str) -> None:
        self.transcoder_list.append(transcoder)

    ##
    # @brief        Private Static Method to Get the Adjacent Pipe.
    # @param[in]    pipe_name: str
    #                   pipe_name to Which the Adjacent Pipe Has to be Found.
    # @return       adjacent_pipe: str
    #                   Returns the Adjacent pipe name to the input pipe name
    @staticmethod
    def _get_adjacent_pipe(pipe_name) -> str:
        adjacent_pipe = chr(ord(pipe_name) + 1)

        if adjacent_pipe not in ['B', 'C', 'D']:
            assert False, "Adjacent Pipe Doesn't Exist for Pipe {}".format(pipe_name)

        return adjacent_pipe


##
# @brief        From Gen13+ Fractional BPP is Supported for DP DSC Displays.This Structure is Needed to Store Fractional
#               and Integral Part of the BPP. Refer 0006Fh DPCD Register to Know about Precision that DP DSC Sink Device
#               Supports.
class _BPP(ctypes.Structure):
    _fields_ = [
        ("fractional_part", ctypes.c_uint16, 4),  # 0 to 3
        ("integral_part", ctypes.c_uint16, 6),  # 4 to 9
        ("reserved", ctypes.c_uint16, 6)  # 10 to 15
    ]


##
# @brief        Helps to store the BPP value as integer and also helps to access integral and fractional part of the
#               BPP.
class BPP(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _BPP),
        ("value", ctypes.c_uint16)
    ]


##
# @brief        RC Range Parameters From CFG
@dataclass
class RCRangeParametersFromCFG:
    initial_xmit_delay: int
    first_line_bpg_offset: int
    initial_offset: int
    flatness_min_qp: int
    flatness_max_qp: int
    rc_quant_inc_limit_0: int
    rc_quant_inc_limit_1: int
    rc_range_parameter_list: List[RcRangeParameters]


# Templates Which Should be Used for logging Success and Failure Case for PPS, RC Range and RC Threshold Parameters.
success_log_template = "{}.{} Expected: {} Actual: {}"
error_log_template = "[Driver Issue] - {}.{} [Mismatch] Expected: {} Actual: {}"


##
# @brief        Source: https://gfxspecs.intel.com/Predator/Home/Index/50151
class _Pps0Fields(ctypes.Structure):
    _fields_ = [
        ("dsc_version_major", ctypes.c_uint32, 4),
        ("dsc_version_minor", ctypes.c_uint32, 4),
        ("bits_per_component", ctypes.c_uint32, 4),
        ("linebuf_depth", ctypes.c_uint32, 4),
        ("block_pred_enable", ctypes.c_uint32, 1),
        ("convert_rgb", ctypes.c_uint32, 1),
        ("enable_422", ctypes.c_uint32, 1),
        ("vbr_enable", ctypes.c_uint32, 1),
        ("alt_ich_select", ctypes.c_uint32, 1),
        ("ich_state_invalidation", ctypes.c_uint32, 1),
        ("native_420", ctypes.c_uint32, 1),
        ("native_422", ctypes.c_uint32, 1),
        ("native_422_zero_padding_ctl", ctypes.c_uint32, 2),
        ("reserved1", ctypes.c_uint32, 5),
        ("allow_double_buf_update_disable", ctypes.c_uint32, 1)
    ]

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    expected_pps_0: _Pps0Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_pps_0: _Pps0Fields) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_0, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_0", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_0", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS0 Field read from the register and helps to access each of the
#               bit field values.
class PPS0Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps0Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Using Anonymous Field 'u' Which is of Type _Pps0Fields to Compare against the expected_pps_0
    #               Refer _Pps0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_0: PPS0Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_0) -> bool:
        return getattr(self, "u") == expected_pps_0


##
# @brief        Source: https://gfxspecs.intel.com/Predator/Home/Index/50152
class _Pps1Fields(ctypes.Structure):
    _fields_ = [
        ("bits_per_pixel", ctypes.c_uint32, 10),
        ("reserved2", ctypes.c_uint32, 10),
        ("psr2_slice_row_per_frame", ctypes.c_uint32, 12)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_1: _Pps1Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_1) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_1, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_1", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_1", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS1 Field read from the register and helps to access each of the
#               bit field values.
class PPS1Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps1Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_1: PPS1Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_1) -> bool:
        return getattr(self, "u") == expected_pps_1


##
# @brief           Source: https://gfxspecs.intel.com/Predator/Home/Index/50160
class _Pps2Fields(ctypes.Structure):
    _fields_ = [
        ("pic_height", ctypes.c_uint32, 16),
        ("pic_width", ctypes.c_uint32, 16)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_2: _Pps2Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_2) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_2, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_2", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_2", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS2 Field read from the register and helps to access each of the
#               bit field values.
class PPS2Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps2Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_2: PPS2Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_2) -> bool:
        return getattr(self, "u") == expected_pps_2


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class _Pps3Fields(ctypes.Structure):
    _fields_ = [
        ("slice_height", ctypes.c_uint32, 16),
        ("slice_width", ctypes.c_uint32, 16)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_3: _Pps3Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_3) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_3, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_3", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_3", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS3 Field read from the register and helps to access each of the
#               bit field values.
class PPS3Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps3Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_3: PPS3Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_3) -> bool:
        return getattr(self, "u") == expected_pps_3


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50162
class _Pps4Fields(ctypes.Structure):
    _fields_ = [
        ("initial_xmit_delay", ctypes.c_uint32, 10),
        ("reserved3", ctypes.c_uint32, 6),
        ("initial_dec_delay", ctypes.c_uint32, 16)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_4: _Pps4Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_4) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_4, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_4", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_4", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS4 Field read from the register and helps to access each of the
#               bit field values.
class PPS4Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps4Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_4: PPS4Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_4) -> bool:
        return getattr(self, "u") == expected_pps_4


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50163
class _Pps5Fields(ctypes.Structure):
    _fields_ = [
        ("scale_increment_interval", ctypes.c_uint32, 16),
        ("scale_decrement_interval", ctypes.c_uint32, 12),
        ("reserved4", ctypes.c_uint32, 4)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_5: _Pps5Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_5) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_5, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_5", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_5", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS5 Field read from the register and helps to access each of the
#               bit field values.
class PPS5Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps5Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_5: PPS5Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_5) -> bool:
        return getattr(self, "u") == expected_pps_5


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50164
class _Pps6Fields(ctypes.Structure):
    _fields_ = [
        ("initial_scale_value", ctypes.c_uint32, 6),
        ("reserved5", ctypes.c_uint32, 2),
        ("first_line_bpg_offset", ctypes.c_uint32, 5),
        ("reserved6", ctypes.c_uint32, 3),
        ("flatness_min_qp", ctypes.c_uint32, 5),
        ("reserved7", ctypes.c_uint32, 3),
        ("flatness_max_qp", ctypes.c_uint32, 5),
        ("reserved8", ctypes.c_uint32, 3)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_6: _Pps6Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_6) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_6, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_6", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_6", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS6 Field read from the register and helps to access each of the
#               bit field values.
class PPS6Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps6Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_6: PPS6Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_6) -> bool:
        return getattr(self, "u") == expected_pps_6


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50165
class _Pps7Fields(ctypes.Structure):
    _fields_ = [
        ("slice_bpg_offset", ctypes.c_uint32, 16),
        ("nfl_bpg_offset", ctypes.c_uint32, 16)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_7: _Pps7Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_7) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_7, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_7", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_7", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS7 Field read from the register and helps to access each of the
#               bit field values.
class PPS7Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps7Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_7: PPS7Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_7) -> bool:
        return getattr(self, "u") == expected_pps_7


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50166
class _Pps8Fields(ctypes.Structure):
    _fields_ = [
        ("final_offset", ctypes.c_uint32, 16),
        ("initial_offset", ctypes.c_uint32, 16)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_8: _Pps8Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_8) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_8, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_8", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_8", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS8 Field read from the register and helps to access each of the
#               bit field values.
class PPS8Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps8Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_8: PPS8Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_8) -> bool:
        return getattr(self, "u") == expected_pps_8


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50167
class _Pps9Fields(ctypes.Structure):
    _fields_ = [
        ("rc_model_Size", ctypes.c_uint32, 16),
        ("rc_edge_factor", ctypes.c_uint32, 4),
        ("reserved9", ctypes.c_uint32, 12)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_9: _Pps9Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_9) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_9, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_9", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_9", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS9 Field read from the register and helps to access each of the
#               bit field values.
class PPS9Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps9Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_9: PPS9Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_9) -> bool:
        return getattr(self, "u") == expected_pps_9


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50153
class _Pps10Fields(ctypes.Structure):
    _fields_ = [
        ("rc_quant_incr_limit0", ctypes.c_uint32, 5),
        ("reserved10", ctypes.c_uint32, 3),
        ("rc_quant_incr_limit1", ctypes.c_uint32, 5),
        ("reserved11", ctypes.c_uint32, 3),
        ("rc_tgt_offset_hi", ctypes.c_uint32, 4),
        ("rc_tgt_offset_lo", ctypes.c_uint32, 4),
        ("reserved12", ctypes.c_uint32, 8)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_10: _Pps10Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_10) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_10, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_10", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_10", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS10 Field read from the register and helps to access each of the
#               bit field values.
class PPS10Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps10Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_10: PPS10Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_10) -> bool:
        return getattr(self, "u") == expected_pps_10


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/50159
class _Pps16Fields(ctypes.Structure):
    _fields_ = [
        ("slice_chunk_size", ctypes.c_uint32, 16),
        ("slice_per_line", ctypes.c_uint32, 3),
        ("reserved13", ctypes.c_uint32, 1),
        ("slice_row_per_frame", ctypes.c_uint32, 12)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_16: _Pps16Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_16) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_16, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_16", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_16", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS16 Field read from the register and helps to access each of the
#               bit field values.
class PPS16Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps16Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_16: PPS16Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_16) -> bool:
        return getattr(self, "u") == expected_pps_16


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/54926
class _Pps17Fields(ctypes.Structure):
    _fields_ = [
        ("reserved14", ctypes.c_uint32, 27),
        ("second_line_bpg_offset", ctypes.c_uint32, 5)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_17: _Pps17Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_17) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_17, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_17", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_17", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS17 Field read from the register and helps to access each of the
#               bit field values.
class PPS17Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps17Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_17: PPS17Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_17) -> bool:
        return getattr(self, "u") == expected_pps_17


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/54927
class _Pps18Fields(ctypes.Structure):
    _fields_ = [
        ("second_line_offset_adj", ctypes.c_uint32, 16),
        ("nsl_bpg_offset", ctypes.c_uint32, 16)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_18: _Pps18Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_18) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_18, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_18", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_18", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of PPS18 Field read from the register and helps to access each of the
#               bit field values.
class PPS18Fields(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _Pps18Fields),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_pps_18: PPS18Fields
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_18) -> bool:
        return getattr(self, "u") == expected_pps_18


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13724
class _RcBufThresh00(ctypes.Structure):
    _fields_ = [
        ("rc_buf_thresh_0", ctypes.c_uint32, 8),
        ("rc_buf_thresh_1", ctypes.c_uint32, 8),
        ("rc_buf_thresh_2", ctypes.c_uint32, 8),
        ("rc_buf_thresh_3", ctypes.c_uint32, 8)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_00: _RcBufThresh00
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_00) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_buf_thresh_00, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_buff_thresh_00", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_buff_thresh_00", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCBuf00  read from the register and helps to access each of the
#               bit field values.
class RCBufThresh00(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcBufThresh00),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_00: RCBufThresh00
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_00) -> bool:
        return getattr(self, "u") == expected_rc_buf_thresh_00


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13724
class _RcBufThresh01(ctypes.Structure):
    _fields_ = [
        ("rc_buf_thresh_4", ctypes.c_uint32, 8),
        ("rc_buf_thresh_5", ctypes.c_uint32, 8),
        ("rc_buf_thresh_6", ctypes.c_uint32, 8),
        ("rc_buf_thresh_7", ctypes.c_uint32, 8)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_01: _RcBufThresh01
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_01) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_buf_thresh_01, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_buff_thresh_01", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_buff_thresh_01", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCBuf01  read from the register and helps to access each of the
#               bit field values.
class RCBufThresh01(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcBufThresh01),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_01: RCBufThresh01
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_01) -> bool:
        return getattr(self, "u") == expected_rc_buf_thresh_01


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13725
class _RcBufThresh10(ctypes.Structure):
    _fields_ = [
        ("rc_buf_thresh_8", ctypes.c_uint32, 8),
        ("rc_buf_thresh_9", ctypes.c_uint32, 8),
        ("rc_buf_thresh_10", ctypes.c_uint32, 8),
        ("rc_buf_thresh_11", ctypes.c_uint32, 8)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_10: _RcBufThresh10
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_10) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_buf_thresh_10, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_buff_thresh_10", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_buff_thresh_10", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCBuf10  read from the register and helps to access each of the
#               bit field values.
class RCBufThresh10(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcBufThresh10),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_10: RCBufThresh10
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_10) -> bool:
        return getattr(self, "u") == expected_rc_buf_thresh_10


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13725
class _RcBufThresh11(ctypes.Structure):
    _fields_ = [
        ("rc_buf_thresh_12", ctypes.c_uint32, 8),
        ("rc_buf_thresh_13", ctypes.c_uint32, 8),
        ("reserved14", ctypes.c_uint32, 16),
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_11: _RcBufThresh11
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_11) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_buf_thresh_11, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_buff_thresh_11", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_buff_thresh_11", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCBuf11  read from the register and helps to access each of the
#               bit field values.
class RCBufThresh11(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcBufThresh11),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_buf_thresh_11: RCBufThresh11
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_buf_thresh_11) -> bool:
        return getattr(self, "u") == expected_rc_buf_thresh_11


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13726
class _RcRange00(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_0", ctypes.c_uint32, 5),
        ("rc_max_qp_0", ctypes.c_uint32, 5),
        ("rc_bpg_offset_0", ctypes.c_uint32, 6),
        ("rc_min_qp_1", ctypes.c_uint32, 5),
        ("rc_max_qp_1", ctypes.c_uint32, 5),
        ("rc_bpg_offset_1", ctypes.c_uint32, 6)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_00: _RcRange00
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_00) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_00, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_00", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_00", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange00  read from the register and helps to access each of the
#               bit field values.
class RCRange00(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange00),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_00: RCRange00
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_00) -> bool:
        return getattr(self, "u") == expected_rc_range_00


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13726
class _RcRange01(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_2", ctypes.c_uint32, 5),
        ("rc_max_qp_2", ctypes.c_uint32, 5),
        ("rc_bpg_offset_2", ctypes.c_uint32, 6),
        ("rc_min_qp_3", ctypes.c_uint32, 5),
        ("rc_max_qp_3", ctypes.c_uint32, 5),
        ("rc_bpg_offset_3", ctypes.c_uint32, 6)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_01: _RcRange01
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_01) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_01, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_01", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_01", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange01  read from the register and helps to access each of the
#               bit field values.
class RCRange01(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange01),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_01: RCRange01
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_01) -> bool:
        return getattr(self, "u") == expected_rc_range_01


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13727
class _RcRange10(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_4", ctypes.c_uint32, 5),
        ("rc_max_qp_4", ctypes.c_uint32, 5),
        ("rc_bpg_offset_4", ctypes.c_uint32, 6),
        ("rc_min_qp_5", ctypes.c_uint32, 5),
        ("rc_max_qp_5", ctypes.c_uint32, 5),
        ("rc_bpg_offset_5", ctypes.c_uint32, 6)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_10: _RcRange10
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_10) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_10, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_10", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_10", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange10  read from the register and helps to access each of the
#               bit field values.
class RCRange10(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange10),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_10: RCRange10
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_10) -> bool:
        return getattr(self, "u") == expected_rc_range_10


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13727
class _RcRange11(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_6", ctypes.c_uint32, 5),
        ("rc_max_qp_6", ctypes.c_uint32, 5),
        ("rc_bpg_offset_6", ctypes.c_uint32, 6),
        ("rc_min_qp_7", ctypes.c_uint32, 5),
        ("rc_max_qp_7", ctypes.c_uint32, 5),
        ("rc_bpg_offset_7", ctypes.c_uint32, 6)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_11: _RcRange11
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_11) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_11, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_11", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_11", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange11  read from the register and helps to access each of the
#               bit field values.
class RCRange11(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange11),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_11: RCRange11
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_11) -> bool:
        return getattr(self, "u") == expected_rc_range_11


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13728
class _RcRange20(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_8", ctypes.c_uint32, 5),
        ("rc_max_qp_8", ctypes.c_uint32, 5),
        ("rc_bpg_offset_8", ctypes.c_uint32, 6),
        ("rc_min_qp_9", ctypes.c_uint32, 5),
        ("rc_max_qp_9", ctypes.c_uint32, 5),
        ("rc_bpg_offset_9", ctypes.c_uint32, 6)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_20: _RcRange20
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_20) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_20, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_20", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_20", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange20  read from the register and helps to access each of the
#               bit field values.
class RCRange20(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange20),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_20: RCRange20
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_20) -> bool:
        return getattr(self, "u") == expected_rc_range_20


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13728
class _RcRange21(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_10", ctypes.c_uint32, 5),
        ("rc_max_qp_10", ctypes.c_uint32, 5),
        ("rc_bpg_offset_10", ctypes.c_uint32, 6),
        ("rc_min_qp_11", ctypes.c_uint32, 5),
        ("rc_max_qp_11", ctypes.c_uint32, 5),
        ("rc_bpg_offset_11", ctypes.c_uint32, 6)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_21: _RcRange21
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_21) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_21, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_21", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_21", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange21  read from the register and helps to access each of the
#               bit field values.
class RCRange21(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange21),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_21: RCRange21
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_21) -> bool:
        return getattr(self, "u") == expected_rc_range_21


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13729
class _RcRange30(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_12", ctypes.c_uint32, 5),
        ("rc_max_qp_12", ctypes.c_uint32, 5),
        ("rc_bpg_offset_12", ctypes.c_uint32, 6),
        ("rc_min_qp_13", ctypes.c_uint32, 5),
        ("rc_max_qp_13", ctypes.c_uint32, 5),
        ("rc_bpg_offset_13", ctypes.c_uint32, 6)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_30: _RcRange30
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_30) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_30, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_30", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_30", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange30  read from the register and helps to access each of the
#               bit field values.
class RCRange30(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange30),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_30: RCRange30
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_30) -> bool:
        return getattr(self, "u") == expected_rc_range_30


##
# @brief          Source: https://gfxspecs.intel.com/Predator/Home/Index/13729
class _RcRange31(ctypes.Structure):
    _fields_ = [
        ("rc_min_qp_14", ctypes.c_uint32, 5),
        ("rc_max_qp_14", ctypes.c_uint32, 5),
        ("rc_bpg_offset_14", ctypes.c_uint32, 6),
        ("reserved15", ctypes.c_uint32, 16),
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_31: _RcRange31
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_31) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_range_31, field[0])
            if actual == expected:
                logging.info(success_log_template.format("rc_range_31", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("rc_range_31", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This helps to store the value of RCRange31  read from the register and helps to access each of the
#               bit field values.
class RCRange31(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcRange31),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Refer PPS0Fields for More Information about How __eq__ Works.
    # @param[in]    expected_rc_range_31: RCRange31
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_range_31) -> bool:
        return getattr(self, "u") == expected_rc_range_31


##
# @brief        Below are the Field that Describe RCRangeParameter used in DSC Programming.
class RcRangeParameters(object):

    ##
    # @brief        Initialize RcRangeParameters Values.
    # @param[in]   min_qp: int
    #                   Specifies the Minimum Quantization Parameter Adjustment that is allowed if the RC Model has
    #                   Tracked to the Current Range
    # @param[in]    max_qp: int
    #                   Specifies the Maximum Quantization Parameter Adjustment that is allowed if the RC Model has
    #                   Tracked to the Current Range
    # @param[in]    bpg_offset: int
    #                   Specifies the Target Bits Per Group Adjustment that is Performed if the RC Model has Tracked to
    #                   the Current Range
    def __init__(self, min_qp: int, max_qp: int, bpg_offset: int) -> None:
        self.range_min_qp: int = min_qp
        self.range_max_qp: int = max_qp
        self.range_bpg_offset: int = bpg_offset


##
# @brief        This Class Holds all the DSC Parameters that Needs to be Checked.
class DSCRequiredPictureParameterSet:

    ##
    # @brief        Initialize the Expected PPS, RC Threshold and RC Range Parameter Values.
    def __init__(self) -> None:
        self.info_frame_header = InfoFrameHeader()

        self.is_dsc_enabled: int = 0  # DSC enabled/disabled
        self.line_buffer_depth: int = 0  # Bits / component for previous reconstructed line buffer

        # Rate control buffer size (in bits); not in PPS, used only in C model for checking overflow
        self.rate_control_bits: int = 0

        self.bits_per_component: int = 0  # Bits / component to code (must be 8, 10, or 12)
        self.convert_rgb: int = 0  # Flag indicating to do RGB - YCoCg conversion and back (should be 1 for RGB input)
        self.slice_count: int = 0  # Slice count per line
        self.slice_width: int = 0  # Slice width
        self.slice_height: int = 0  # Slice height

        # 4:2:2 enable mode (from PPS, 4:2:2 conversion happens outside of DSC encode/decode algorithm)
        # simple 4:2:2 in DSC 1.2, enable 4:2:2 in DSC1.1
        self.simple_422: int = 0

        self.h_active: int = 0  # Actual HActive Timing.
        self.pic_width: int = 0  # Picture width
        self.pic_height: int = 0  # Picture height
        self.rc_tgt_offset_hi: int = 3  # Offset to bits/group used by RC to determine QP adjustment
        self.rc_tgt_offset_lo: int = 3  # Offset to bits/group used by RC to determine QP adjustment
        self.bits_per_pixel: BPP = BPP(value=0)  # Bits/pixel target << 4 (ie., 4 fractional bits)
        self.rc_edge_factor: int = 6  # Factor to determine if an edge is present based on the bits produced
        self.rc_quant_inc_limit_1: int = 11  # Slow down incrementing once the range reaches this value
        self.rc_quant_inc_limit_0: int = 11  # Slow down incrementing once the range reaches this value
        self.initial_xmit_delay: int = 170  # Number of pixels to delay the initial transmission
        self.initial_dec_delay: int = 0  # Number of pixels to delay the VLD on the decoder, not including SSM
        self.is_block_prediction_enabled: int = 0  # Block prediction range (in pixels)
        self.first_line_bpg_offset: int = -1  # Bits/group offset to use for first line of the slice
        self.second_line_bpg_offset: int = -1  # Bits/group for the second line of a slice in Native 4:2:0 mode
        self.initial_offset: int = 6144  # Value to use for RC model offset at slice start
        self.x_start: int = 0  # X position in the picture of top-left corner of slice
        self.y_start: int = 0  # Y position in the picture of top-left corner of slice
        self.rc_buf_thresh: List[int] = []  # Thresholds defining each of the buffer ranges
        self.rc_range_parameter_list: List[RcRangeParameters] = []
        self.rc_model_size: int = 8192  # Total size of RC model
        self.flatness_min_qp: int = 3  # Minimum QP where flatness information is sent
        self.flatness_max_qp: int = 12  # Maximum QP where flatness information is sent

        # MAX-MIN for all components is required to be <= this value for flatness to be used
        self.flatness_det_threshold: int = 2

        self.initial_scale_value: int = 0  # Initial value for scale factor
        self.scale_decrement_interval: int = 0  # Decrement scale factor every scale_decrement_interval groups
        self.scale_increment_interval: int = 0  # Increment scale factor every scale_increment_interval groups
        self.nfl_bpg_offset: int = 0  # Non-first line BPG offset to use
        self.slice_bpg_offset: int = 0  # BPG offset used to enforce slice bit constraint
        self.final_offset: int = 0  # Final RC linear transformation offset value
        self.is_vbr_enabled: int = 0  # Enable on-off VBR (i.e., disable stuffing bits)
        self.mux_word_size: int = 0  # Mux word size (in bits) for SSM mode
        self.chunk_size: int = 0  # The (max) size in bytes of the "chunks" that are used in slice multiplexing
        self.pps_identifier: int = 0  # Placeholder for PPS identifier
        self.dsc_version_minor: int = 0  # DSC minor version
        self.dsc_version_major: int = 0  # DSC major version
        self.vdsc_instances: int = 0  # number of VDSC engines
        self.native_420: int = 0  # 1 Indicates Native 4:2:0 Mode is enabled.
        self.native_422: int = 0  # 1 Indicates Native 4:2:2 Mode is enabled.

        # Specifies no of bits that are deallocated for each group not in second line of slice.
        self.nsl_bpg_offset: int = 0

        self.second_line_offset_adj: int = 0  # Used as an offset adjustment for the second line in Native 4:2:0 Mode


##
# @brief        DSCPictureParameterSet Holds All the PPS, RC Threshold, RC Range Registers that are Programmed by the
#               Driver as Part of DSC Programming.
class DSCPictureParameterSet(object):
    success_log_template = "Expected and Actual {} Fields are Matching"
    error_log_template = "[Driver Issue] -  Expected and Actual {} Fields are Mismatching"

    ##
    # @brief        Initialize the PPS, RC Threshold, RC Range Parameter Register Fields.
    def __init__(self):
        self.pps_0 = PPS0Fields()
        self.pps_1 = PPS1Fields()
        self.pps_2 = PPS2Fields()
        self.pps_3 = PPS3Fields()
        self.pps_4 = PPS4Fields()
        self.pps_5 = PPS5Fields()
        self.pps_6 = PPS6Fields()
        self.pps_7 = PPS7Fields()
        self.pps_8 = PPS8Fields()
        self.pps_9 = PPS9Fields()
        self.pps_10 = PPS10Fields()
        self.pps_16 = PPS16Fields()
        self.pps_17 = PPS17Fields()
        self.pps_18 = PPS18Fields()
        self.rc_thresh_00 = RCBufThresh00()
        self.rc_thresh_01 = RCBufThresh01()
        self.rc_thresh_10 = RCBufThresh10()
        self.rc_thresh_11 = RCBufThresh11()
        self.rc_range_00 = RCRange00()
        self.rc_range_01 = RCRange01()
        self.rc_range_10 = RCRange10()
        self.rc_range_11 = RCRange11()
        self.rc_range_20 = RCRange20()
        self.rc_range_21 = RCRange21()
        self.rc_range_30 = RCRange30()
        self.rc_range_31 = RCRange31()

    ##
    # @brief        Member Function to get the PPS Register Values Programmed by the Driver during Enabling Sequence of
    #               DSC.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    pipe_name: str
    #                   Pipe Name For Which Programmed Register Values Has to be Fetched.
    # @param[in]    engine: DSCEngine
    #                   DSC Engine(Left/Right) For Which Programmed Register Values Has to be Fetched.
    # @return       None
    def fill_actual_pps(self, gfx_index: str, platform: str, pipe_name: str, engine: DSCEngine) -> None:
        r_offset = '_' + str(engine.value) + '_' + pipe_name
        logging.info("platform name is {0}, {1}".format(platform, 'PPS0' + r_offset))

        dsc_pps0 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_0", 'PPS0' + r_offset, platform, gfx_index=gfx_index)
        self.pps_0.value = dsc_pps0.asUint
        logging.debug("PPS0 Value is {0},".format(hex(self.pps_0.value)))

        dsc_pps1 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_1", 'PPS1' + r_offset, platform, gfx_index=gfx_index)
        self.pps_1.value = dsc_pps1.asUint
        logging.debug("PPS1 Value is {0},".format(hex(self.pps_1.value)))

        dsc_pps2 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_2", 'PPS2' + r_offset, platform, gfx_index=gfx_index)
        self.pps_2.value = dsc_pps2.asUint
        logging.debug("PPS2 Value is {0},".format(hex(self.pps_2.value)))

        dsc_pps3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3", 'PPS3' + r_offset, platform, gfx_index=gfx_index)
        self.pps_3.value = dsc_pps3.asUint
        logging.debug("PPS3 Value is {0},".format(hex(self.pps_3.value)))

        dsc_pps4 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_4", 'PPS4' + r_offset, platform, gfx_index=gfx_index)
        self.pps_4.value = dsc_pps4.asUint
        logging.debug("PPS4 Value is {0},".format(hex(self.pps_4.value)))

        dsc_pps5 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_5", 'PPS5' + r_offset, platform, gfx_index=gfx_index)
        self.pps_5.value = dsc_pps5.asUint
        logging.debug("PPS5 Value is {0},".format(hex(self.pps_5.value)))

        dsc_pps6 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_6", 'PPS6' + r_offset, platform, gfx_index=gfx_index)
        self.pps_6.value = dsc_pps6.asUint
        logging.debug("PPS6 Value is {0},".format(hex(self.pps_6.value)))

        dsc_pps7 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_7", 'PPS7' + r_offset, platform, gfx_index=gfx_index)
        self.pps_7.value = dsc_pps7.asUint
        logging.debug("PPS7 Value is {0},".format(hex(self.pps_7.value)))

        dsc_pps8 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_8", 'PPS8' + r_offset, platform, gfx_index=gfx_index)
        self.pps_8.value = dsc_pps8.asUint
        logging.debug("PPS8 Value is {0},".format(hex(self.pps_8.value)))

        dsc_pps9 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_9", 'PPS9' + r_offset, platform, gfx_index=gfx_index)
        self.pps_9.value = dsc_pps9.asUint
        logging.debug("PPS9 Value is {0},".format(hex(self.pps_9.value)))

        dsc_pps10 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_10", 'PPS10' + r_offset, platform, gfx_index=gfx_index)
        self.pps_10.value = dsc_pps10.asUint
        logging.debug("PPS10 Value is {0},".format(hex(self.pps_10.value)))

        dsc_pps16 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_16", 'PPS16' + r_offset, platform, gfx_index=gfx_index)
        self.pps_16.value = dsc_pps16.asUint
        logging.debug("PPS16 Value is {0},".format(hex(self.pps_16.value)))

        # PPS17 and PPS18 are applicable only GEN14+ platforms
        if platform in ['MTL', 'ELG', 'LNL', 'PTL', 'NVL', 'CLS']:
            dsc_pps17 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_17", 'PPS17' + r_offset, platform,
                                          gfx_index=gfx_index)
            self.pps_17.value = dsc_pps17.asUint
            logging.debug("PPS17 Value is {0},".format(hex(self.pps_17.value)))

            dsc_pps18 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_18", 'PPS18' + r_offset, platform,
                                          gfx_index=gfx_index)
            self.pps_18.value = dsc_pps18.asUint
            logging.debug("PPS18 Value is {0},".format(hex(self.pps_18.value)))
        else:
            self.pps_17.value = 0
            self.pps_18.value = 0

        rc_buf00 = MMIORegister.read("DSC_RC_BUF_THRESH_00", 'RC_BUF00' + r_offset, platform, gfx_index=gfx_index)
        self.rc_thresh_00.value = rc_buf00.asUint
        logging.debug("self.rc_thresh_00.value Value is {0},".format(hex(self.rc_thresh_00.value)))

        rc_buf01 = MMIORegister.read("DSC_RC_BUF_THRESH_01", 'RC_BUF01' + r_offset, platform, gfx_index=gfx_index)
        self.rc_thresh_01.value = rc_buf01.asUint
        logging.debug("self.rc_thresh_01.value Value is {0},".format(hex(self.rc_thresh_01.value)))

        rc_buf10 = MMIORegister.read("DSC_RC_BUF_THRESH_10", 'RC_BUF10' + r_offset, platform, gfx_index=gfx_index)
        self.rc_thresh_10.value = rc_buf10.asUint
        logging.debug("self.rc_thresh_10.value Value is {0},".format(hex(self.rc_thresh_10.value)))

        rc_buf11 = MMIORegister.read("DSC_RC_BUF_THRESH_11", 'RC_BUF11' + r_offset, platform, gfx_index=gfx_index)
        self.rc_thresh_11.value = rc_buf11.asUint
        logging.debug("self.rc_thresh_11.value Value is {0},".format(hex(self.rc_thresh_11.value)))

        rc_range00 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_00", 'RC_RANGE00' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_00.value = rc_range00.asUint
        logging.debug("self.rc_range_00.value Value is {0},".format(hex(self.rc_range_00.value)))

        rc_range01 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_01", 'RC_RANGE01' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_01.value = rc_range01.asUint
        logging.debug("self.rc_range_01.value Value is {0},".format(hex(self.rc_range_01.value)))

        rc_range10 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_10", 'RC_RANGE10' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_10.value = rc_range10.asUint
        logging.debug("self.rc_range_10.value Value is {0},".format(hex(self.rc_range_10.value)))

        rc_range11 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_11", 'RC_RANGE11' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_11.value = rc_range11.asUint
        logging.debug("self.rc_range_11.value Value is {0},".format(hex(self.rc_range_11.value)))

        rc_range20 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_20", 'RC_RANGE20' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_20.value = rc_range20.asUint
        logging.debug("self.rc_range_20.value Value is {0},".format(hex(self.rc_range_20.value)))

        rc_range21 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_21", 'RC_RANGE21' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_21.value = rc_range21.asUint
        logging.debug("self.rc_range_21.value Value is {0},".format(hex(self.rc_range_21.value)))

        rc_range30 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_30", 'RC_RANGE30' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_30.value = rc_range30.asUint
        logging.debug("self.rc_range_30.value Value is {0},".format(hex(self.rc_range_30.value)))

        rc_range31 = MMIORegister.read("DSC_RC_RANGE_PARAMETERS_31", 'RC_RANGE31' + r_offset, platform,
                                       gfx_index=gfx_index)
        self.rc_range_31.value = rc_range31.asUint
        logging.debug("self.rc_range_31.value Value is {0},".format(hex(self.rc_range_31.value)))

    ##
    # @brief        Class Method to Get the DSCPictureParameterSet From DSCRequiredPictureParameterSet.
    #               Does Mapping of Each Field in the DSCRequiredPictureParameterSet to DSCPictureParameterSet
    # @param[in]    calculated_pps: DSCRequiredPictureParameterSet
    #                   Computed PPS, RC Threshold, RC Range Values Which has to be Mapped to DSCPictureParameterSet
    #                   Which Would Help in Comparison of the Expected and Actual Values.
    # @return       expected_pps: DSCPictureParameterSet
    #                   Returns the mapped DSCPictureParameterSet object from DSCRequiredPictureParameterSet object
    @classmethod
    def from_calculated_pps(cls, calculated_pps: DSCRequiredPictureParameterSet) -> DSCPictureParameterSet:
        expected_pps = DSCPictureParameterSet()
        rc_range_params = []

        # PPS0
        expected_pps.pps_0.dsc_version_major = calculated_pps.dsc_version_major
        expected_pps.pps_0.dsc_version_minor = calculated_pps.dsc_version_minor
        expected_pps.pps_0.bits_per_component = calculated_pps.bits_per_component
        expected_pps.pps_0.linebuf_depth = calculated_pps.line_buffer_depth

        expected_pps.pps_0.block_pred_enable = calculated_pps.is_block_prediction_enabled
        expected_pps.pps_0.convert_rgb = calculated_pps.convert_rgb
        expected_pps.pps_0.enable_422 = calculated_pps.simple_422
        expected_pps.pps_0.vbr_enable = calculated_pps.is_vbr_enabled
        expected_pps.pps_0.alt_ich_select = 1 if calculated_pps.dsc_version_minor == 2 else 0  # Enabled for DSC1.2
        expected_pps.pps_0.ich_state_invalidation = 0
        expected_pps.pps_0.native_420 = calculated_pps.native_420
        expected_pps.pps_0.native_422 = calculated_pps.native_422
        expected_pps.pps_0.reserved1 = 0
        expected_pps.pps_0.allow_double_buf_update_disable = 0

        # PPS1
        expected_pps.pps_1.bits_per_pixel = calculated_pps.bits_per_pixel.value
        expected_pps.pps_1.reserved2 = 0
        expected_pps.pps_1.psr2_slice_row_per_frame = 0

        # PPS2
        expected_pps.pps_2.pic_height = calculated_pps.pic_height
        expected_pps.pps_2.pic_width = calculated_pps.pic_width

        # PPS3
        expected_pps.pps_3.slice_height = calculated_pps.slice_height
        expected_pps.pps_3.slice_width = calculated_pps.slice_width

        # PPS4
        expected_pps.pps_4.initial_xmit_delay = calculated_pps.initial_xmit_delay
        expected_pps.pps_4.initial_dec_delay = calculated_pps.initial_dec_delay
        expected_pps.pps_4.reserved3 = 0

        # PPS5
        expected_pps.pps_5.scale_increment_interval = calculated_pps.scale_increment_interval
        expected_pps.pps_5.scale_decrement_interval = calculated_pps.scale_decrement_interval
        expected_pps.pps_5.reserved4 = 0

        # PPS6
        expected_pps.pps_6.initial_scale_value = calculated_pps.initial_scale_value
        expected_pps.pps_6.first_line_bpg_offset = calculated_pps.first_line_bpg_offset
        expected_pps.pps_6.flatness_min_qp = calculated_pps.flatness_min_qp
        expected_pps.pps_6.flatness_max_qp = calculated_pps.flatness_max_qp
        expected_pps.pps_6.reserved5 = 0
        expected_pps.pps_6.reserved6 = 0
        expected_pps.pps_6.reserved7 = 0
        expected_pps.pps_6.reserved8 = 0

        # PPS7
        expected_pps.pps_7.slice_bpg_offset = calculated_pps.slice_bpg_offset
        expected_pps.pps_7.nfl_bpg_offset = calculated_pps.nfl_bpg_offset

        # PPS8
        expected_pps.pps_8.final_offset = calculated_pps.final_offset
        expected_pps.pps_8.initial_offset = calculated_pps.initial_offset

        # PPS9
        expected_pps.pps_9.rc_model_Size = calculated_pps.rc_model_size
        expected_pps.pps_9.rc_edge_factor = calculated_pps.rc_edge_factor
        expected_pps.pps_9.reserved9 = 0

        # PPS10
        expected_pps.pps_10.rc_quant_incr_limit0 = calculated_pps.rc_quant_inc_limit_0
        expected_pps.pps_10.rc_quant_incr_limit1 = calculated_pps.rc_quant_inc_limit_1
        expected_pps.pps_10.rc_tgt_offset_hi = calculated_pps.rc_tgt_offset_hi
        expected_pps.pps_10.rc_tgt_offset_lo = calculated_pps.rc_tgt_offset_lo
        expected_pps.pps_10.reserved10 = 0
        expected_pps.pps_10.reserved11 = 0
        expected_pps.pps_10.reserved12 = 0

        # PPS16
        expected_pps.pps_16.slice_chunk_size = calculated_pps.chunk_size
        expected_pps.pps_16.slice_per_line = calculated_pps.slice_count // calculated_pps.vdsc_instances
        expected_pps.pps_16.slice_row_per_frame = calculated_pps.pic_height // calculated_pps.slice_height
        expected_pps.pps_16.reserved13 = 0

        # PPS17
        expected_pps.pps_17.reserved14 = 0
        expected_pps.pps_17.second_line_bpg_offset = calculated_pps.second_line_bpg_offset

        # PPS18
        expected_pps.pps_18.second_line_offset_adj = calculated_pps.second_line_offset_adj
        expected_pps.pps_18.nsl_bpg_offset = calculated_pps.nsl_bpg_offset

        expected_pps.rc_thresh_00.rc_buf_thresh_0 = calculated_pps.rc_buf_thresh[0]
        expected_pps.rc_thresh_00.rc_buf_thresh_1 = calculated_pps.rc_buf_thresh[1]
        expected_pps.rc_thresh_00.rc_buf_thresh_2 = calculated_pps.rc_buf_thresh[2]
        expected_pps.rc_thresh_00.rc_buf_thresh_3 = calculated_pps.rc_buf_thresh[3]

        expected_pps.rc_thresh_01.rc_buf_thresh_4 = calculated_pps.rc_buf_thresh[4]
        expected_pps.rc_thresh_01.rc_buf_thresh_5 = calculated_pps.rc_buf_thresh[5]
        expected_pps.rc_thresh_01.rc_buf_thresh_6 = calculated_pps.rc_buf_thresh[6]
        expected_pps.rc_thresh_01.rc_buf_thresh_7 = calculated_pps.rc_buf_thresh[7]

        expected_pps.rc_thresh_10.rc_buf_thresh_8 = calculated_pps.rc_buf_thresh[8]
        expected_pps.rc_thresh_10.rc_buf_thresh_9 = calculated_pps.rc_buf_thresh[9]
        expected_pps.rc_thresh_10.rc_buf_thresh_10 = calculated_pps.rc_buf_thresh[10]
        expected_pps.rc_thresh_10.rc_buf_thresh_11 = calculated_pps.rc_buf_thresh[11]

        expected_pps.rc_thresh_11.rc_buf_thresh_12 = calculated_pps.rc_buf_thresh[12]
        expected_pps.rc_thresh_11.rc_buf_thresh_13 = calculated_pps.rc_buf_thresh[13]
        expected_pps.rc_thresh_11.reserved14 = 0

        for rc_ra_param in calculated_pps.rc_range_parameter_list:
            val = (rc_ra_param.range_bpg_offset << 10) | (rc_ra_param.range_max_qp << 5)
            val = val | rc_ra_param.range_min_qp
            rc_range_params.append(val)

        expected_pps.rc_range_00.value = ((rc_range_params[1] << 16) | rc_range_params[0])
        expected_pps.rc_range_01.value = ((rc_range_params[3] << 16) | rc_range_params[2])
        expected_pps.rc_range_10.value = ((rc_range_params[5] << 16) | rc_range_params[4])
        expected_pps.rc_range_11.value = ((rc_range_params[7] << 16) | rc_range_params[6])
        expected_pps.rc_range_20.value = ((rc_range_params[9] << 16) | rc_range_params[8])
        expected_pps.rc_range_21.value = ((rc_range_params[11] << 16) | rc_range_params[10])
        expected_pps.rc_range_30.value = ((rc_range_params[13] << 16) | rc_range_params[12])
        expected_pps.rc_range_31.value = rc_range_params[14]

        return expected_pps

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    expected_pps: DSCPictureParameterSet
    #                   Object Which Contains the Expected Value Calculated Using DPCD and Other Display Information
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_pps: DSCPictureParameterSet) -> bool:
        is_equal: bool = True

        zip_iterator = zip(self.__dict__.items(), expected_pps.__dict__.items())

        for (a_key, a_value), (e_key, e_value) in zip_iterator:
            if a_value == e_value:
                logging.info(DSCPictureParameterSet.success_log_template.format(a_key))
            else:
                logging.error(DSCPictureParameterSet.error_log_template.format(a_key))
                is_equal = False

        return is_equal


##
# @brief        This class contains all the bit fields related to PPS header byte and helps them to access them
#               individually
class _InfoFrameHeader(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_uint8),
        ("version", ctypes.c_uint8),
        ("length", ctypes.c_uint8),
        ("checksum", ctypes.c_uint8),
    ]

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    expected_info_frame_header: _InfoFrameHeader
    #                   Object Which Contains the Expected Values Calculated as per DP spec / Bspec (For HDMI)
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_info_frame_header: _InfoFrameHeader) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_info_frame_header, field[0])
            if actual == expected:
                logging.info(success_log_template.format("if_header", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("if_header", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the entire 4 bytes of data for PPS header field
class InfoFrameHeader(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _InfoFrameHeader),
        ("value", ctypes.c_uint32)
    ]

    ##
    # @brief        Using Anonymous Field 'u' Which is of Type _InfoFrameHeader to Compare against the expected info
    #               frame header bytes
    #               Refer _InfoFrameHeader for More Information about How __eq__ Works.
    # @param[in]    expected_info_frame_header: InfoFrameHeader
    #                    Refer _InfoFrameHeader
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_info_frame_header: InfoFrameHeader) -> bool:
        return getattr(self, "u") == expected_info_frame_header


##
# @brief        This class contains all the bit fields related to PPS 0 and helps them to access them individually
class _DSCVersion(ctypes.Structure):
    _fields_ = [
        ("minor_version", ctypes.c_uint8, 4),
        ("major_version", ctypes.c_uint8, 4),
    ]

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    expected_dsc_version: _DSCVersion
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications.
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_dsc_version: _DSCVersion) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_dsc_version, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_0", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_0", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the entire 1 byte of data for PPS 0 field
class DSCVersion(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _DSCVersion),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Using Anonymous Field 'u' Which is of Type _DSCVersion to Compare against the expected_dsc_version
    #               Refer _DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_dsc_version: DSCVersion
    #                    Refer _DSCVersion
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_dsc_version: DSCVersion) -> bool:
        return getattr(self, "u") == expected_dsc_version


##
# @brief        This class contains all the bit fields related to PPS 1, 2 and helps them to access them individually
class _PPSIdentifier(ctypes.Structure):
    _fields_ = [
        ("pps_identifier", ctypes.c_uint16, 8),
        ("reserved", ctypes.c_uint16, 8),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_pps_identifier: _PPSIdentifier
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_pps_identifier: _PPSIdentifier) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_pps_identifier, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_1_and_2", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_1_and_2", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 2 bytes of data for PPS 1, 2 field
class PPSIdentifier(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _PPSIdentifier),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_pps_identifier: PPSIdentifier
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_pps_identifier: PPSIdentifier) -> bool:
        return getattr(self, "u") == expected_pps_identifier


##
# @brief        This class contains all the bit fields related to PPS 3 and helps them to access them individually
class _BpcLbd(ctypes.Structure):
    _fields_ = [
        ("line_buffer_depth", ctypes.c_uint8, 4),
        ("bits_per_component", ctypes.c_uint8, 4),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_bpc_and_lbd: _BpcLbd
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_bpc_and_lbd: _BpcLbd) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_bpc_and_lbd, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_3", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_3", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 3 field
class BpcLbd(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _BpcLbd),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_bpc_and_lbd: BpcLbd
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_bpc_and_lbd: BpcLbd) -> bool:
        return getattr(self, "u") == expected_bpc_and_lbd


##
# @brief        This class contains all the bit fields related to PPS 4, 5 and helps them to access them individually
class _GeneralPpsParams(ctypes.Structure):
    _fields_ = [
        ("bpp_low", ctypes.c_uint16, 2),
        ("vbr_enable", ctypes.c_uint16, 1),
        ("simple_422", ctypes.c_uint16, 1),
        ("convert_rgb", ctypes.c_uint16, 1),
        ("block_pred_enable", ctypes.c_uint16, 1),
        ("reserved", ctypes.c_uint16, 2),
        ("bpp_high", ctypes.c_uint16, 8),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_general_pps_params: _GeneralPpsParams
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_general_pps_params: _GeneralPpsParams) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_general_pps_params, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_4_and_5", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_4_and_5", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 2 bytes of data for PPS 4, 5 field
class GeneralPpsParams(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _GeneralPpsParams),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_general_pps_params: GeneralPpsParams
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_general_pps_params: GeneralPpsParams) -> bool:
        return getattr(self, "u") == expected_general_pps_params


##
# @brief        This class contains all the bit fields related to PPS 16, 17 and helps them to access them individually
class _InitialTransmissionDelay(ctypes.Structure):
    _fields_ = [
        ("transmission_delay_low", ctypes.c_uint16, 2),
        ("reserved", ctypes.c_uint16, 6),
        ("transmission_delay_high", ctypes.c_uint16, 8),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_initial_trans_delay: _InitialTransmissionDelay
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_initial_trans_delay: _InitialTransmissionDelay) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_initial_trans_delay, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_16_and_17", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_16_and_17", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 2 bytes of data for PPS 16, 17 field
class InitialTransmissionDelay(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _InitialTransmissionDelay),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_initial_trans_delay: InitialTransmissionDelay
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_initial_trans_delay: InitialTransmissionDelay) -> bool:
        return getattr(self, "u") == expected_initial_trans_delay


##
# @brief        This class contains all the bit fields related to PPS 20, 21 and helps them to access them individually
class _InitialScaleValue(ctypes.Structure):
    _fields_ = [
        ("reserved1", ctypes.c_uint16, 8),
        ("initial_scale", ctypes.c_uint16, 6),
        ("reserved2", ctypes.c_uint16, 2),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_initial_scale_value: _InitialScaleValue
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_initial_scale_value: _InitialScaleValue) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_initial_scale_value, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_20_and_21", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_20_and_21", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 2 bytes of data for PPS 20, 21 field
class InitialScaleValue(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _InitialScaleValue),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_initial_scale_value: InitialScaleValue
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_initial_scale_value: InitialScaleValue) -> bool:
        return getattr(self, "u") == expected_initial_scale_value


##
# @brief        This class contains all the bit fields related to PPS 24, 25 and helps them to access them individually
class _ScaleDecrementInterval(ctypes.Structure):
    _fields_ = [
        ("scale_decrement_low", ctypes.c_uint16, 4),
        ("reserved", ctypes.c_uint16, 4),
        ("scale_decrement_high", ctypes.c_uint16, 8),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_scale_incr_interval: _ScaleDecrementInterval
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_scale_incr_interval: _ScaleDecrementInterval) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_scale_incr_interval, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_24_25", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_24_25", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 2 bytes of data for PPS 24, 25 field
class ScaleDecrementInterval(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _ScaleDecrementInterval),
        ("value", ctypes.c_uint16)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_scale_incr_interval: ScaleDecrementInterval
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_scale_incr_interval: ScaleDecrementInterval) -> bool:
        return getattr(self, "u") == expected_scale_incr_interval


##
# @brief        This class contains all the bit fields related to PPS 27 and helps them to access them individually
class _FirstLineBpgOffset(ctypes.Structure):
    _fields_ = [
        ("bpg_offset", ctypes.c_uint8, 5),
        ("reserved", ctypes.c_uint8, 3),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_first_line_bpg_offset: _FirstLineBpgOffset
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_first_line_bpg_offset: _FirstLineBpgOffset) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_first_line_bpg_offset, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_27", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_27", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 27 field
class FirstLineBpgOffset(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _FirstLineBpgOffset),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_first_line_bpg_offset: FirstLineBpgOffset
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_first_line_bpg_offset: FirstLineBpgOffset) -> bool:
        return getattr(self, "u") == expected_first_line_bpg_offset


##
# @brief        This class contains all the bit fields related to PPS 36 and helps them to access them individually
class _FlatnessMinQp(ctypes.Structure):
    _fields_ = [
        ("min_qp", ctypes.c_uint8, 5),
        ("reserved", ctypes.c_uint8, 3),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_flatness_min_qp: _FlatnessMinQp
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_flatness_min_qp: _FlatnessMinQp) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_flatness_min_qp, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_36", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_36", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 36 field
class FlatnessMinQp(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _FlatnessMinQp),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_flatness_min_qp: FlatnessMinQp
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_flatness_min_qp: FlatnessMinQp) -> bool:
        return getattr(self, "u") == expected_flatness_min_qp


##
# @brief        This class contains all the bit fields related to PPS 37 and helps them to access them individually
class _FlatnessMaxQp(ctypes.Structure):
    _fields_ = [
        ("max_qp", ctypes.c_uint8, 5),
        ("reserved", ctypes.c_uint8, 3),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_flatness_max_qp: _FlatnessMaxQp
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_flatness_max_qp: _FlatnessMaxQp) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_flatness_max_qp, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_37", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_37", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 37 field
class FlatnessMaxQp(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _FlatnessMaxQp),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_flatness_max_qp: FlatnessMaxQp
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_flatness_max_qp: FlatnessMaxQp) -> bool:
        return getattr(self, "u") == expected_flatness_max_qp


##
# @brief        This class contains all the bit fields related to PPS 40 and helps them to access them individually
class _RcEdgeFactor(ctypes.Structure):
    _fields_ = [
        ("rc_edge_factor", ctypes.c_uint8, 4),
        ("reserved", ctypes.c_uint8, 4),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_edge_factor: _RcEdgeFactor
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_rc_edge_factor: _RcEdgeFactor) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_edge_factor, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_40", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_40", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 40 field
class RcEdgeFactor(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcEdgeFactor),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_edge_factor: RcEdgeFactor
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_edge_factor: RcEdgeFactor) -> bool:
        return getattr(self, "u") == expected_rc_edge_factor


##
# @brief        This class contains all the bit fields related to PPS 41 and helps them to access them individually
class _RcQuantIncrLmt0(ctypes.Structure):
    _fields_ = [
        ("rc_quant_incr_lmt0", ctypes.c_uint8, 5),
        ("reserved", ctypes.c_uint8, 3),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_quant_incr_lmt0: _RcQuantIncrLmt0
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_rc_quant_incr_lmt0: _RcQuantIncrLmt0) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_quant_incr_lmt0, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_41", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_41", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 41 field
class RcQuantIncrLmt0(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcQuantIncrLmt0),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_quant_incr_lmt0: RcQuantIncrLmt0
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_quant_incr_lmt0: RcQuantIncrLmt0) -> bool:
        return getattr(self, "u") == expected_rc_quant_incr_lmt0


##
# @brief        This class contains all the bit fields related to PPS 42 and helps them to access them individually
class _RcQuantIncrLmt1(ctypes.Structure):
    _fields_ = [
        ("rc_quant_incr_lmt1", ctypes.c_uint8, 5),
        ("reserved", ctypes.c_uint8, 3),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_quant_incr_lmt1: _RcQuantIncrLmt1
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_rc_quant_incr_lmt1: _RcQuantIncrLmt1) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_quant_incr_lmt1, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_42", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_42", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 42 field
class RcQuantIncrLmt1(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcQuantIncrLmt1),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_quant_incr_lmt1: RcQuantIncrLmt1
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_quant_incr_lmt1: RcQuantIncrLmt1) -> bool:
        return getattr(self, "u") == expected_rc_quant_incr_lmt1


##
# @brief        This class contains all the bit fields related to PPS 43 and helps them to access them individually
class _RcTargeOffset(ctypes.Structure):
    _fields_ = [
        ("rc_target_offset_high", ctypes.c_uint8, 4),
        ("rc_target_offset_low", ctypes.c_uint8, 4),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_target_offset: _RcTargeOffset
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_rc_target_offset: _RcTargeOffset) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_rc_target_offset, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_43", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_43", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 43 field
class RcTargeOffset(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _RcTargeOffset),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_rc_target_offset: RcTargeOffset
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_rc_target_offset: RcTargeOffset) -> bool:
        return getattr(self, "u") == expected_rc_target_offset


##
# @brief        This class contains all the bit fields related to PPS 88 and helps them to access them individually
class _GeneralPpsParams2(ctypes.Structure):
    _fields_ = [
        ("native_422", ctypes.c_uint8, 1),
        ("native_420", ctypes.c_uint8, 1),
        ("reserved", ctypes.c_uint8, 5),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_general_pps_params2: _GeneralPpsParams2
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_general_pps_params2: _GeneralPpsParams2) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_general_pps_params2, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_88", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_88", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 88 field
class GeneralPpsParams2(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _GeneralPpsParams2),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_general_pps_params2: GeneralPpsParams2
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_general_pps_params2: GeneralPpsParams2) -> bool:
        return getattr(self, "u") == expected_general_pps_params2


##
# @brief        This class contains all the bit fields related to PPS 89 and helps them to access them individually
class _SecondLineBpgOffset(ctypes.Structure):
    _fields_ = [
        ("second_line_bpg_offset", ctypes.c_uint8, 5),
        ("reserved", ctypes.c_uint8, 3),
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_second_line_bpg_offset: _SecondLineBpgOffset
    #                   Object Which Contains the Expected Values Retrieved From DPCD Registers and Calculated Using
    #                   DSC Algorithm Defined in the DSC Specifications
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_second_line_bpg_offset: _SecondLineBpgOffset) -> bool:
        is_equal: bool = True
        for field in self._fields_:
            actual, expected = getattr(self, field[0]), getattr(expected_second_line_bpg_offset, field[0])
            if actual == expected:
                logging.info(success_log_template.format("pps_89", field[0], expected, actual))
            else:
                logging.error(error_log_template.format("pps_89", field[0], expected, actual))
                is_equal = False

        return is_equal


##
# @brief        This is an exposed/wrapper class that holds the 1 byte of data for PPS 89 field
class SecondLineBpgOffset(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", _SecondLineBpgOffset),
        ("value", ctypes.c_uint8)
    ]

    ##
    # @brief        Refer DSCVersion for More Information about How __eq__ Works.
    # @param[in]    expected_second_line_bpg_offset: SecondLineBpgOffset
    #                  Refer __eq__ in _PPSIdentifier class
    # @return       Returns True if expected and actual value matches else false
    def __eq__(self, expected_second_line_bpg_offset: SecondLineBpgOffset) -> bool:
        return getattr(self, "u") == expected_second_line_bpg_offset


##
# @brief        This class holds the 128 bytes PPS data (PPS0 - PPS127)
class PictureParameterSetPayload(object):
    success_log_template = "Expected and Actual {} Fields are Matching"
    error_log_template = "[Driver Issue] -  Expected and Actual {} Fields are Mismatching"

    ##
    # @brief    Initializes all the PPS data (PPS0 - PPS127)
    def __init__(self):
        self.dsc_version: DSCVersion = DSCVersion()  # PPS 0
        self.pps_identifier: PPSIdentifier = PPSIdentifier()  # PPS 1, 2
        self.bpc_and_lbd: BpcLbd = BpcLbd()  # PPS 3
        self.general_pp_params: GeneralPpsParams = GeneralPpsParams()  # PPS 4, 5

        self.picture_height: int = 0  # PPS 6, 7
        self.picture_width: int = 0  # PPS 8, 9
        self.slice_height: int = 0  # PPS 10, 11
        self.slice_width: int = 0  # PPS 12, 13
        self.chunk_size: int = 0  # PPS 14, 15

        self.initial_trans_delay: InitialTransmissionDelay = InitialTransmissionDelay()  # PPS 16, 17
        self.initial_decode_delay: int = 0  # PPS 18, 19
        self.initial_scale_value: InitialScaleValue = InitialScaleValue()  # PPS 20, 21
        self.scale_increment_interval: int = 0  # PPS 22, 23
        self.scale_decrement_interval: ScaleDecrementInterval = ScaleDecrementInterval()  # PPS 24, 25

        self.reserved1: int = 0  # PPS 26

        self.first_line_bpg_offset: FirstLineBpgOffset = FirstLineBpgOffset()  # PPS 27
        self.nfl_bpg_offset: int = 0  # PPS 28, 29
        self.slice_bpg_offset: int = 0  # PPS 30, 31
        self.initial_offset: int = 0  # PPS 32, 33
        self.final_offset: int = 0  # PPS 34, 35

        self.flatness_min_qp: FlatnessMinQp = FlatnessMinQp()  # PPS 36
        self.flatness_max_qp: FlatnessMaxQp = FlatnessMaxQp()  # PPS 37

        self.rc_model_size: int = 0  # PPS 38, 39
        self.rc_edge_factor: RcEdgeFactor = RcEdgeFactor()  # PPS 40
        self.rc_quant_incr_lmt0: RcQuantIncrLmt0 = RcQuantIncrLmt0()  # PPS 41
        self.rc_quant_incr_lmt1: RcQuantIncrLmt1 = RcQuantIncrLmt1()  # PPS 42
        self.rc_target_offset: RcTargeOffset = RcTargeOffset()  # PPS 43

        self.rc_buffer_threshold0: int = 0  # PPS 44
        self.rc_buffer_threshold1: int = 0  # PPS 45
        self.rc_buffer_threshold2: int = 0  # PPS 46
        self.rc_buffer_threshold3: int = 0  # PPS 47
        self.rc_buffer_threshold4: int = 0  # PPS 48
        self.rc_buffer_threshold5: int = 0  # PPS 49
        self.rc_buffer_threshold6: int = 0  # PPS 50
        self.rc_buffer_threshold7: int = 0  # PPS 51
        self.rc_buffer_threshold8: int = 0  # PPS 52
        self.rc_buffer_threshold9: int = 0  # PPS 53
        self.rc_buffer_threshold10: int = 0  # PPS 54
        self.rc_buffer_threshold11: int = 0  # PPS 55
        self.rc_buffer_threshold12: int = 0  # PPS 56
        self.rc_buffer_threshold13: int = 0  # PPS 57

        self.rc_range_parameter0: int = 0  # PPS 58, 59
        self.rc_range_parameter1: int = 0  # PPS 60, 61
        self.rc_range_parameter2: int = 0  # PPS 62, 63
        self.rc_range_parameter3: int = 0  # PPS 64, 65
        self.rc_range_parameter4: int = 0  # PPS 66, 67
        self.rc_range_parameter5: int = 0  # PPS 68, 69
        self.rc_range_parameter6: int = 0  # PPS 70, 71
        self.rc_range_parameter7: int = 0  # PPS 72, 73
        self.rc_range_parameter8: int = 0  # PPS 74, 75
        self.rc_range_parameter9: int = 0  # PPS 76, 77
        self.rc_range_parameter10: int = 0  # PPS 78, 79
        self.rc_range_parameter11: int = 0  # PPS 80, 81
        self.rc_range_parameter12: int = 0  # PPS 82, 83
        self.rc_range_parameter13: int = 0  # PPS 84, 85
        self.rc_range_parameter14: int = 0  # PPS 86, 87

        self.general_pp_params2: GeneralPpsParams2 = GeneralPpsParams2()  # PPS 88
        self.second_line_bpg_offset: SecondLineBpgOffset = SecondLineBpgOffset()  # PPS 89

        self.nsl_bpg_offset: int = 0  # PPS 90, 91

        self.second_line_offset_adj: int = 0  # PPS 92, 93

        self.reserved2: int = 0  # PPS 94 - 127 (32 bytes)

    ##
    # @brief        This class method helps to convert byte array into object of type PictureParameterSetPayload
    # @param[in]    byte_array: List[int]
    #                   This byte array contains 128 bytes of PPS data which driver has programmed in the DIP
    #                   registers.
    # @return       pps_payload: PictureParameterSetPayload
    #                   Constructs the readable/printable/comparable object which can be used for comparing with the
    #                   expected pps payload
    @classmethod
    def from_byte_array(cls, byte_array: List[int]) -> PictureParameterSetPayload:
        pps_payload = PictureParameterSetPayload()

        pps_payload.dsc_version = DSCVersion(value=byte_array[0])
        pps_payload.pps_identifier = PPSIdentifier(value=int.from_bytes(byte_array[1:3], "little"))  # PPS 1, 2
        pps_payload.bpc_and_lbd = BpcLbd(value=byte_array[3])  # PPS 3

        # PPS 4, 5
        pps_payload.general_pp_params = GeneralPpsParams(value=int.from_bytes(byte_array[4:6], "little"))

        pps_payload.picture_height = int.from_bytes(byte_array[6:8], "little")  # PPS 6, 7
        pps_payload.picture_width = int.from_bytes(byte_array[8:10], "little")  # PPS 8, 9
        pps_payload.slice_height = int.from_bytes(byte_array[10:12], "little")  # PPS 10, 11
        pps_payload.slice_width = int.from_bytes(byte_array[12:14], "little")  # PPS 12, 13
        pps_payload.chunk_size = int.from_bytes(byte_array[14:16], "little")  # PPS 14, 15

        # PPS 16, 17
        pps_payload.initial_trans_delay = InitialTransmissionDelay(value=int.from_bytes(byte_array[16:18], "little"))

        pps_payload.initial_decode_delay = int.from_bytes(byte_array[18:20], "little")  # PPS 18, 19

        # PPS 20, 21
        pps_payload.initial_scale_value = InitialScaleValue(value=int.from_bytes(byte_array[20:22], "little"))
        pps_payload.scale_increment_interval = int.from_bytes(byte_array[22:24], "little")  # PPS 22, 23

        # PPS 24, 25
        pps_payload.scale_decrement_interval = ScaleDecrementInterval(value=int.from_bytes(byte_array[24:26], "little"))

        pps_payload.reserved1 = 0  # PPS 26

        pps_payload.first_line_bpg_offset = FirstLineBpgOffset(value=byte_array[27])  # PPS 27
        pps_payload.nfl_bpg_offset = int.from_bytes(byte_array[28:30], "little")  # PPS 28, 29
        pps_payload.slice_bpg_offset = int.from_bytes(byte_array[30:32], "little")  # PPS 30, 31
        pps_payload.initial_offset = int.from_bytes(byte_array[32:34], "little")  # PPS 32, 33
        pps_payload.final_offset = int.from_bytes(byte_array[34:36], "little")  # PPS 34, 35

        pps_payload.flatness_min_qp = FlatnessMinQp(value=byte_array[36])  # PPS 36
        pps_payload.flatness_max_qp = FlatnessMaxQp(value=byte_array[37])  # PPS 37

        pps_payload.rc_model_size = int.from_bytes(byte_array[38:40], "little")  # PPS 38, 39
        pps_payload.rc_edge_factor = RcEdgeFactor(value=byte_array[40])  # PPS 40
        pps_payload.rc_quant_incr_lmt0 = RcQuantIncrLmt0(value=byte_array[41])  # PPS 41
        pps_payload.rc_quant_incr_lmt1 = RcQuantIncrLmt1(value=byte_array[42])  # PPS 42
        pps_payload.rc_target_offset = RcTargeOffset(value=byte_array[43])  # PPS 43

        pps_payload.rc_buffer_threshold0 = byte_array[44]  # PPS 44
        pps_payload.rc_buffer_threshold1 = byte_array[45]  # PPS 45
        pps_payload.rc_buffer_threshold3 = byte_array[46]  # PPS 47
        pps_payload.rc_buffer_threshold4 = byte_array[47]  # PPS 48
        pps_payload.rc_buffer_threshold2 = byte_array[48]  # PPS 46
        pps_payload.rc_buffer_threshold5 = byte_array[49]  # PPS 49
        pps_payload.rc_buffer_threshold6 = byte_array[50]  # PPS 50
        pps_payload.rc_buffer_threshold7 = byte_array[51]  # PPS 51
        pps_payload.rc_buffer_threshold8 = byte_array[52]  # PPS 52
        pps_payload.rc_buffer_threshold9 = byte_array[53]  # PPS 53
        pps_payload.rc_buffer_threshold10 = byte_array[54]  # PPS 54
        pps_payload.rc_buffer_threshold11 = byte_array[55]  # PPS 55
        pps_payload.rc_buffer_threshold12 = byte_array[56]  # PPS 56
        pps_payload.rc_buffer_threshold13 = byte_array[57]  # PPS 57

        pps_payload.rc_range_parameter0 = int.from_bytes(byte_array[58: 60], "little")  # PPS 58, 59
        pps_payload.rc_range_parameter1 = int.from_bytes(byte_array[60: 62], "little")  # PPS 60, 61
        pps_payload.rc_range_parameter2 = int.from_bytes(byte_array[62: 64], "little")  # PPS 62, 63
        pps_payload.rc_range_parameter3 = int.from_bytes(byte_array[64: 66], "little")  # PPS 64, 65
        pps_payload.rc_range_parameter4 = int.from_bytes(byte_array[66: 68], "little")  # PPS 66, 67
        pps_payload.rc_range_parameter5 = int.from_bytes(byte_array[68: 70], "little")  # PPS 68, 69
        pps_payload.rc_range_parameter6 = int.from_bytes(byte_array[70: 72], "little")  # PPS 70, 71
        pps_payload.rc_range_parameter7 = int.from_bytes(byte_array[72: 74], "little")  # PPS 72, 73
        pps_payload.rc_range_parameter8 = int.from_bytes(byte_array[74: 76], "little")  # PPS 74, 75
        pps_payload.rc_range_parameter9 = int.from_bytes(byte_array[76: 78], "little")  # PPS 76, 77
        pps_payload.rc_range_parameter10 = int.from_bytes(byte_array[78: 80], "little")  # PPS 78, 79
        pps_payload.rc_range_parameter11 = int.from_bytes(byte_array[80: 82], "little")  # PPS 80, 81
        pps_payload.rc_range_parameter12 = int.from_bytes(byte_array[82: 84], "little")  # PPS 82, 83
        pps_payload.rc_range_parameter13 = int.from_bytes(byte_array[84: 86], "little")  # PPS 84, 85
        pps_payload.rc_range_parameter14 = int.from_bytes(byte_array[86: 88], "little")  # PPS 86, 87

        pps_payload.general_pp_params2 = GeneralPpsParams2(value=byte_array[88])  # PPS 88

        pps_payload.second_line_bpg_offset = SecondLineBpgOffset(value=byte_array[89])  # PPS 89

        pps_payload.nsl_bpg_offset = int.from_bytes(byte_array[90:92], "little")  # PPS 90, 91

        pps_payload.second_line_offset_adj = int.from_bytes(byte_array[92:94], "little")  # PPS 92, 93

        pps_payload.reserved2 = int.from_bytes(byte_array[94:128], "little")  # PPS 92 - 127 (34 bytes)

        return pps_payload

    ##
    # @brief        This class method helps to convert DSCRequiredPictureParameterSet object into object of type
    #               PictureParameterSetPayload
    # @param[in]    calculated_pps: DSCRequiredPictureParameterSet
    #                   This object contains all the calculated PPS parameters based on the DSC algorithm and DPCD
    #                   register values and our driver policies.
    # @return       pps_payload: PictureParameterSetPayload
    #                   Constructs the readable/printable/comparable object which can be used for comparing with the
    #                   expected pps payload
    @classmethod
    def from_calculate_pps(cls, calculated_pps: DSCRequiredPictureParameterSet) -> PictureParameterSetPayload:
        pps_payload: PictureParameterSetPayload = PictureParameterSetPayload()

        # PPS 0
        pps_payload.dsc_version.minor_version = calculated_pps.dsc_version_minor
        pps_payload.dsc_version.major_version = calculated_pps.dsc_version_major

        pps_payload.pps_identifier.pps_identifier = 0  # PPS 1

        # PPS 3
        pps_payload.bpc_and_lbd.bits_per_component = calculated_pps.bits_per_component
        pps_payload.bpc_and_lbd.line_buffer_depth = calculated_pps.line_buffer_depth

        # PPS 4, 5
        bpp = calculated_pps.bits_per_pixel.value
        pps_payload.general_pp_params.bpp_low = DSCHelper.extract_bits(bpp, 2, 8, '010b')
        pps_payload.general_pp_params.bpp_high = DSCHelper.extract_bits(bpp, 8, 0, '010b')
        pps_payload.general_pp_params.vbr_enable = calculated_pps.is_vbr_enabled
        pps_payload.general_pp_params.simple_422 = calculated_pps.simple_422
        pps_payload.general_pp_params.convert_rgb = calculated_pps.convert_rgb
        pps_payload.general_pp_params.block_pred_enable = calculated_pps.is_block_prediction_enabled
        pps_payload.general_pp_params.reserved = 0

        pps_payload.picture_height = int.from_bytes(calculated_pps.pic_height.to_bytes(2, "little"), "big")  # PPS 6, 7

        # To the panel we will be sending the actual h_active data. So we shouldn't be using pic_width from calculated
        # DSC here because pic_width * vdsc_instance can give wrong h_active in some cases.
        # For E.g. say h_active = 8192, no of slice is 12, then pic_width will be 683, so when multiplied with 12 we
        # will get pic width as 8196 which is incorrect.
        pps_payload.picture_width = int.from_bytes(calculated_pps.h_active.to_bytes(2, "little"), "big")  # PPS 8, 9

        # PPS 10, 11
        pps_payload.slice_height = int.from_bytes(calculated_pps.slice_height.to_bytes(2, "little"), "big")

        pps_payload.slice_width = int.from_bytes(calculated_pps.slice_width.to_bytes(2, "little"), "big")  # PPS 12, 13
        pps_payload.chunk_size = int.from_bytes(calculated_pps.chunk_size.to_bytes(2, "little"), "big")  # PPS 14, 15

        # PPS 16, 17
        delay = calculated_pps.initial_xmit_delay
        pps_payload.initial_trans_delay.transmission_delay_low = DSCHelper.extract_bits(delay, 2, 8, '010b')
        pps_payload.initial_trans_delay.transmission_delay_high = DSCHelper.extract_bits(delay, 8, 0, '010b')
        pps_payload.initial_trans_delay.reserved = 0

        # PPS 18, 19
        pps_payload.initial_decode_delay = int.from_bytes(calculated_pps.initial_dec_delay.to_bytes(2, "little"), "big")

        # PPS 20, 21
        pps_payload.initial_scale_value.initial_scale = calculated_pps.initial_scale_value
        pps_payload.initial_scale_value.reserved1 = 0
        pps_payload.initial_scale_value.reserved2 = 0

        # PPS 22, 23
        scale_incr_interval = calculated_pps.scale_increment_interval
        pps_payload.scale_increment_interval = int.from_bytes(scale_incr_interval.to_bytes(2, "little"), "big")

        # PPS 24, 25
        dec_interval = calculated_pps.scale_decrement_interval
        pps_payload.scale_decrement_interval.scale_decrement_low = DSCHelper.extract_bits(dec_interval, 4, 8, '016b')
        pps_payload.scale_decrement_interval.scale_decrement_high = DSCHelper.extract_bits(dec_interval, 8, 0, '016b')
        pps_payload.scale_decrement_interval.reserved = 0

        pps_payload.reserved1 = 0  # PPS 26

        pps_payload.first_line_bpg_offset.bpg_offset = calculated_pps.first_line_bpg_offset  # PPS 27
        pps_payload.first_line_bpg_offset.reserved = 0

        # PPS 28, 29
        pps_payload.nfl_bpg_offset = int.from_bytes(calculated_pps.nfl_bpg_offset.to_bytes(2, "little"), "big")

        # PPS 30, 31
        pps_payload.slice_bpg_offset = int.from_bytes(calculated_pps.slice_bpg_offset.to_bytes(2, "little"), "big")

        # PPS 32, 33
        pps_payload.initial_offset = int.from_bytes(calculated_pps.initial_offset.to_bytes(2, "little"), "big")

        # PPS 34, 35
        pps_payload.final_offset = int.from_bytes(calculated_pps.final_offset.to_bytes(2, "little"), "big")

        # PPS 36
        pps_payload.flatness_min_qp.min_qp = calculated_pps.flatness_min_qp
        pps_payload.flatness_min_qp.reserved = 0

        # PPS 37
        pps_payload.flatness_max_qp.max_qp = calculated_pps.flatness_max_qp
        pps_payload.flatness_max_qp.reserved = 0

        # PPS 38, 39
        pps_payload.rc_model_size = int.from_bytes(calculated_pps.rc_model_size.to_bytes(2, "little"), "big")

        # PPS 40
        pps_payload.rc_edge_factor.rc_edge_factor = calculated_pps.rc_edge_factor
        pps_payload.rc_edge_factor.reserved = 0

        # PPS 41
        pps_payload.rc_quant_incr_lmt0.rc_quant_incr_lmt0 = calculated_pps.rc_quant_inc_limit_0
        pps_payload.rc_quant_incr_lmt0.reserved = 0

        # PPS 42
        pps_payload.rc_quant_incr_lmt1.rc_quant_incr_lmt1 = calculated_pps.rc_quant_inc_limit_1
        pps_payload.rc_quant_incr_lmt1.reserved = 0

        # PPS 43
        pps_payload.rc_target_offset.rc_target_offset_high = calculated_pps.rc_tgt_offset_hi
        pps_payload.rc_target_offset.rc_target_offset_low = calculated_pps.rc_tgt_offset_lo

        pps_payload.rc_buffer_threshold0 = calculated_pps.rc_buf_thresh[0]  # PPS 44
        pps_payload.rc_buffer_threshold1 = calculated_pps.rc_buf_thresh[1]  # PPS 45
        pps_payload.rc_buffer_threshold3 = calculated_pps.rc_buf_thresh[2]  # PPS 47
        pps_payload.rc_buffer_threshold4 = calculated_pps.rc_buf_thresh[3]  # PPS 48
        pps_payload.rc_buffer_threshold2 = calculated_pps.rc_buf_thresh[4]  # PPS 46
        pps_payload.rc_buffer_threshold5 = calculated_pps.rc_buf_thresh[5]  # PPS 49
        pps_payload.rc_buffer_threshold6 = calculated_pps.rc_buf_thresh[6]  # PPS 50
        pps_payload.rc_buffer_threshold7 = calculated_pps.rc_buf_thresh[7]  # PPS 51
        pps_payload.rc_buffer_threshold8 = calculated_pps.rc_buf_thresh[8]  # PPS 52
        pps_payload.rc_buffer_threshold9 = calculated_pps.rc_buf_thresh[9]  # PPS 53
        pps_payload.rc_buffer_threshold10 = calculated_pps.rc_buf_thresh[10]  # PPS 54
        pps_payload.rc_buffer_threshold11 = calculated_pps.rc_buf_thresh[11]  # PPS 55
        pps_payload.rc_buffer_threshold12 = calculated_pps.rc_buf_thresh[12]  # PPS 56
        pps_payload.rc_buffer_threshold13 = calculated_pps.rc_buf_thresh[13]  # PPS 57

        rc_ra_params = []
        for rc_ra_param in calculated_pps.rc_range_parameter_list:
            val = (rc_ra_param.range_min_qp << 11) | (rc_ra_param.range_max_qp << 6 | rc_ra_param.range_bpg_offset)
            rc_ra_params.append(val)

        pps_payload.rc_range_parameter0 = int.from_bytes(rc_ra_params[0].to_bytes(2, "little"), "big")  # PPS 58, 59
        pps_payload.rc_range_parameter1 = int.from_bytes(rc_ra_params[1].to_bytes(2, "little"), "big")  # PPS 60, 61
        pps_payload.rc_range_parameter2 = int.from_bytes(rc_ra_params[2].to_bytes(2, "little"), "big")  # PPS 62, 63
        pps_payload.rc_range_parameter3 = int.from_bytes(rc_ra_params[3].to_bytes(2, "little"), "big")  # PPS 64, 65
        pps_payload.rc_range_parameter4 = int.from_bytes(rc_ra_params[4].to_bytes(2, "little"), "big")  # PPS 66, 67
        pps_payload.rc_range_parameter5 = int.from_bytes(rc_ra_params[5].to_bytes(2, "little"), "big")  # PPS 68, 69
        pps_payload.rc_range_parameter6 = int.from_bytes(rc_ra_params[6].to_bytes(2, "little"), "big")  # PPS 70, 71
        pps_payload.rc_range_parameter7 = int.from_bytes(rc_ra_params[7].to_bytes(2, "little"), "big")  # PPS 72, 73
        pps_payload.rc_range_parameter8 = int.from_bytes(rc_ra_params[8].to_bytes(2, "little"), "big")  # PPS 74, 75
        pps_payload.rc_range_parameter9 = int.from_bytes(rc_ra_params[9].to_bytes(2, "little"), "big")  # PPS 76, 77
        pps_payload.rc_range_parameter10 = int.from_bytes(rc_ra_params[10].to_bytes(2, "little"), "big")  # PPS 78, 79
        pps_payload.rc_range_parameter11 = int.from_bytes(rc_ra_params[11].to_bytes(2, "little"), "big")  # PPS 80, 81
        pps_payload.rc_range_parameter12 = int.from_bytes(rc_ra_params[12].to_bytes(2, "little"), "big")  # PPS 82, 83
        pps_payload.rc_range_parameter13 = int.from_bytes(rc_ra_params[13].to_bytes(2, "little"), "big")  # PPS 84, 85
        pps_payload.rc_range_parameter14 = int.from_bytes(rc_ra_params[14].to_bytes(2, "little"), "big")  # PPS 86, 87

        # PPS 88
        pps_payload.general_pp_params2.native_422 = calculated_pps.native_422
        pps_payload.general_pp_params2.native_420 = calculated_pps.native_420
        pps_payload.general_pp_params2.reserved = 0

        # PPS 89
        pps_payload.second_line_bpg_offset.second_line_bpg_offset = calculated_pps.second_line_bpg_offset
        pps_payload.second_line_bpg_offset.reserved = 0

        # PPS 90, 91
        pps_payload.nsl_bpg_offset = int.from_bytes(calculated_pps.nsl_bpg_offset.to_bytes(2, "little"), "big")

        # PPS 92, 93
        offset_adj = calculated_pps.second_line_offset_adj
        pps_payload.second_line_offset_adj = int.from_bytes(offset_adj.to_bytes(2, "little"), "big")
        pps_payload.reserved2 = 0  # PPS 92 - 127 (34 bytes)

        return pps_payload

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    expected_pps_payload: PictureParameterSetPayload
    #                   Object Which Contains the Expected Value Calculated Using DPCD, dsc algorithm and other display
    #                   related parameters
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_pps_payload: PictureParameterSetPayload) -> bool:
        is_equal: bool = True

        zip_iterator = zip(self.__dict__.items(), expected_pps_payload.__dict__.items())

        for (a_key, a_value), (e_key, e_value) in zip_iterator:
            if a_value == e_value:
                if isinstance(a_value, int):
                    logging.info(success_log_template.format(a_key, a_key, e_value, a_value))
                logging.info(PictureParameterSetPayload.success_log_template.format(a_key))
            else:
                if isinstance(a_value, int):
                    logging.error(error_log_template.format(a_key, a_key, e_value, a_value))
                logging.error(PictureParameterSetPayload.error_log_template.format(a_key))
                is_equal = False

        return is_equal


##
# @brief        This class hold the 132 byte of PPS SDP data (4 bytes of header + 128 bytes of PPS)
class PictureParameterSDP(object):
    success_log_template = "Expected and Actual {} Fields are Matching"
    error_log_template = "[Driver Issue] -  Expected and Actual {} Fields are Mismatching"

    ##
    # @brief    Initializes all the PPS SDP data (4 bytes of header + 128 bytes of PPS)
    def __init__(self):
        self.info_frame_header = InfoFrameHeader()
        self.pps_payload = PictureParameterSetPayload()

    ##
    # @brief        This class method helps to convert byte array into object of type PictureParameterSDP
    # @param[in]    byte_array: List[int]
    #                   This byte array contains 132 bytes of PPS SDP data which driver has programmed in the DIP
    #                   registers.
    # @return       pps_payload: PictureParameterSetPayload
    #                   Constructs the readable/printable/comparable object which can be used for comparing with the
    #                   expected pps payload
    @classmethod
    def from_byte_array(cls, byte_array: List[int]) -> PictureParameterSDP:
        pps_sdp = PictureParameterSDP()
        pps_sdp.info_frame_header = InfoFrameHeader(value=int.from_bytes(byte_array[:4], "little"))  # Header - 4 bytes
        pps_sdp.pps_payload = PictureParameterSetPayload.from_byte_array(byte_array[4:])    # Send 128 bytes of data

        return pps_sdp

    ##
    # @brief        This class method helps to convert DSCRequiredPictureParameterSet object into object of type
    #               PictureParameterSDP
    # @param[in]    calculated_pps_sdp: DSCRequiredPictureParameterSet
    #                   This object contains all the calculated PPS parameters based on the DSC algorithm and DPCD
    #                   register values and our driver policies and bspec calculations.
    # @return       pps_sdp: PictureParameterSDP
    #                   Constructs the readable/printable/comparable object which can be used for comparing with the
    #                   expected pps sdp
    @classmethod
    def from_calculated_pps_sdp(cls, calculated_pps_sdp: DSCRequiredPictureParameterSet) -> PictureParameterSDP:
        pps_sdp = PictureParameterSDP()

        pps_sdp.info_frame_header = copy.deepcopy(calculated_pps_sdp.info_frame_header)
        pps_sdp.pps_payload = PictureParameterSetPayload.from_calculate_pps(calculated_pps_sdp)

        return pps_sdp

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    expected_pps_sdp: PictureParameterSDP
    #                   Object Which Contains the Expected Value Calculated Using DPCD, dsc algorithm and other display
    #                   related parameters
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def __eq__(self, expected_pps_sdp: PictureParameterSDP) -> bool:
        is_equal: bool = True

        zip_iterator = zip(self.__dict__.items(), expected_pps_sdp.__dict__.items())

        for (a_key, a_value), (e_key, e_value) in zip_iterator:
            if a_value == e_value:
                if isinstance(a_value, int):
                    logging.info(success_log_template.format(a_key, a_key, e_value, a_value))
                logging.info(PictureParameterSDP.success_log_template.format(a_key))
            else:
                if isinstance(a_value, int):
                    logging.error(error_log_template.format(a_key, a_key, e_value, a_value))
                logging.error(PictureParameterSDP.error_log_template.format(a_key))
                is_equal = False

        return is_equal
