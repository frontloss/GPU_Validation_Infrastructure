#######################################################################################################################
# @file     gfxvalsim.py
# @brief    Python wrapper exposes API's related to GfxValSim DLL
# @author   Pabolu, Chandrakanth, Amit Sau
########################################################################################################################
import ctypes
import logging
import sys
from enum import Enum

from Libs.Core import cmd_parser, registry_access
from Libs.Core import reboot_helper
from Libs.Core.core_base import singleton
from Libs.Core.display_config import adapter_info_struct
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import dpcd_model_data_struct, dpcd_container
from Libs.Core.test_env import test_context, state_machine_manager
from Libs.Core.vbt import oprom_parser
from Libs.Core.wrapper import valsim_args
from Libs.Core.wrapper import valsim_wrapper

GFXVALSIM_ETL_GUID = "9B2C7A57-929C-4E06-8E92-40056D608525"

# Registry key constant used by GfxValSim driver
GFXVALSIM_REGISTRY_ROOT_PATH = r'SYSTEM\CurrentControlSet\Services\GfxValSimDriver'
GFXVALSIM_FEATURE_CONTROL_REG_KEY = "FeatureControl"
REG_KEY_CUSTOM_VBT = "_CustomVBT"
REG_KEY_CUSTOM_VBT_SIZE = "_CustomVBTSize"
REG_KEY_ACTUAL_VBT = "_ActualVBT"
REG_KEY_VBT_SIMULATION = "VBTSimulation"

REG_KEY_ACTUAL_OPREGION = "_ActualOpRegion"

# Features supported in GfxValSim driver
GFXVALSIM_FEATURE_VBT_SIMULATION = "VBT_SIMULATION"
GFXVALSIM_FEATURE_SINK_SIMULATION = "SINK_SIMULATION"
REG_KEY_VAL_SIM_INSTALLED = "GfxValSimEnabled"
GFXVALSIM_FEATURE_HYBRID_SIMULATION = "HYBRID_SIMULATION"
GFXVALSIM_FEATURE_INIT_TEST_MMIO = "INIT_TEST_MMIO"

REG_KEY_CUSTOM_OPROM = "_CustomOprom"
REG_KEY_CUSTOM_OPROM_SIZE = "_CustomOpromSize"

REG_KEY_INIT_TEST_MMIO = "_TestMmioData"

RETRY_LIMIT = 1  # Donot change this without approval from val-infra team


##
# @brief        Class to hold the feature control details for GfxValSim driver
class Features(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('sink_simulation', ctypes.c_int, 1),
        ('vbt_simulation', ctypes.c_int, 1),
        ('hybrid_simulation', ctypes.c_int, 1),
        ('init_test_mmio', ctypes.c_int, 1),
        ('reserved', ctypes.c_int, 28),
    ]


##
# @brief        Feature Control Initialising
class FeatureControl(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", Features),
        ("value", ctypes.c_uint32)]


##
# @brief        Values of DP Topology
class DpTopology(Enum):
    InvalidTopology = 0
    DPSST = 1
    DPMST = 2
    DPEDP = 3


##
# @brief        Val Sim IOCTL Code
class ValSimIoctlCode(Enum):
    GET_ALL_ADAPTER_CAPS = 15


##
# @brief        GfxValSim Class
@singleton
class GfxValSim(object):

    ##
    # @brief        API to configure feature (VBT simulation, Sink simulation) in GfxValSim driver through registry
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    feature_name - name of the Feature
    # @param[in]    flag - specify enable(1) or disable(0)
    # @return       status - True on Success, False otherwise
    def configure_feature(self, gfx_index, feature_name, flag):
        if feature_name not in [GFXVALSIM_FEATURE_SINK_SIMULATION, GFXVALSIM_FEATURE_VBT_SIMULATION,
                                GFXVALSIM_FEATURE_HYBRID_SIMULATION, GFXVALSIM_FEATURE_INIT_TEST_MMIO]:
            raise Exception("Invalid GfxValSim feature")

        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]

        reg_args = registry_access.StateSeparationRegArgs(gfx_index=None, feature=registry_access.Feature.VALSIM)
        value, _ = registry_access.read(args=reg_args, reg_name=GFXVALSIM_FEATURE_CONTROL_REG_KEY)
        if value is None:
            value = 0
            registry_access.write(args=reg_args, reg_name=GFXVALSIM_FEATURE_CONTROL_REG_KEY,
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=value)

        feature_control = FeatureControl()
        feature_control.value = value

        if feature_name == GFXVALSIM_FEATURE_VBT_SIMULATION:
            feature_control.vbt_simulation = flag
        elif feature_name == GFXVALSIM_FEATURE_SINK_SIMULATION:
            feature_control.sink_simulation = flag
        elif feature_name == GFXVALSIM_FEATURE_HYBRID_SIMULATION:
            feature_control.hybrid_simulation = flag
        elif feature_name == GFXVALSIM_FEATURE_INIT_TEST_MMIO:
            feature_control.init_test_mmio = flag

        status = registry_access.write(args=reg_args, reg_name=GFXVALSIM_FEATURE_CONTROL_REG_KEY,
                                       reg_type=registry_access.RegDataType.DWORD, reg_value=feature_control.value)
        if status is not True:
            raise Exception("Failed to write ValSim registry with key = {} & value = {}".format(
                GFXVALSIM_FEATURE_CONTROL_REG_KEY, feature_control.value))
        return status

    ##
    # @brief    API to initialize Gfx val simulation driver.
    # @return   driver_handle - val sim handle
    def _init_gfx_val_sim(self):
        driver_handle = valsim_wrapper.init_gfx_val_sim()
        if driver_handle is not None:
            logging.info("Graphics Simulation Mode Successful")
        else:
            logging.error("Graphics Simulation Mode Failed")
            gdhm.report_bug(
                f'[GfxValSim] Failed to initialize gfx val sim',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return driver_handle

    ##
    # @brief        Exposed API to initialize all efp ports for all the adapter.
    # @return       status - True on Success, False otherwise
    def _init_all_efp_ports(self):
        from Libs.Core import display_utility
        from Libs.Core.display_config import display_config
        gfx_adapter_details = test_context.TestContext.get_gfx_adapter_details()
        if len(gfx_adapter_details) == 0:
            raise Exception("Failed to get gfx adapter details")

        status = True
        for gfx_index, adapterInfo in gfx_adapter_details.items():
            efp_port_list = []
            # ignore init port if gfx driver is not running
            if reboot_helper.is_reboot_scenario():
                # ToDo Cleanup needed : Remove display config get_free_ports
                free_port_list = display_config.get_free_ports(gfx_index)
                for port_name in free_port_list:
                    if display_utility.get_vbt_panel_type(port_name, gfx_index) not in \
                            [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                        efp_port_list.append(port_name)
            else:
                efp_port_list = self.__get_port(gfx_index, lfp=False)

            if len(efp_port_list) == 0:
                continue

            status = status & valsim_wrapper.init_efp_ports(gfx_adapter_details[gfx_index], efp_port_list)
            if status is False:
                logging.error(f'Failed to initialize EFP ports {efp_port_list} on {gfx_index}')
        return status

    ##
    # @brief        Exposed API to initialize all lfp ports.
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    lfp_port_list - list of LFP Ports
    # @return       status - True on Success, False otherwise
    def _init_lfp_ports(self, gfx_adapter_info, lfp_port_list):
        status = valsim_wrapper.init_lfp_ports(gfx_adapter_info, lfp_port_list)
        if status is False:
            logging.error(f'Failed to initialize LFP ports {lfp_port_list} on {gfx_adapter_info.gfxIndex}')
            gdhm.report_bug(
                f'[GfxValSim] Failed to initialize LFP ports',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    ##
    # @brief        API to simulate plug
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @param[in]    edid_path - EDID file path
    # @param[in]    dpcd_path - DPCD file path
    # @param[in]    is_low_power - True if Low Power State, False otherwise
    # @param[in]    port_type - connector port type
    # @param[in]    is_lfp - True if LFP, False otherwise
    # @param[in]    dp_dpcd_model_data - DPCD model data object
    # @return       status - True on Success, False otherwise
    def _plug(self, gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type, is_lfp, dp_dpcd_model_data,
              dongle_type):
        counter = 0
        status = False
        dpcd_file = dpcd_path
        if dpcd_path and (dpcd_path.endswith('.txt') or dpcd_path.endswith('.TXT')):
            dpcd_file = dpcd_container._convert_dpcd_to_bin(dpcd_path)

        if ('DP' in port) and (dp_dpcd_model_data is None):
            logging.debug(
                "Filling default link training transactions in DPCD model data for port {0}".format(
                    port + "_" + port_type))
            dp_dpcd_model_data = dpcd_model_data_struct.DPDPCDModelData()
            self._fill_default_dpcd_model_data(dp_dpcd_model_data, port)
        while counter <= RETRY_LIMIT:  # WA: HSD-18012027898, race condition between HW ISR and Valsim ISR
            status = valsim_wrapper.plug(gfx_adapter_info, port, edid_path, dpcd_file, is_low_power,
                                         port_type, is_lfp, dp_dpcd_model_data, dongle_type)
            counter += 1
            if status is True:
                break

        if status is False:
            logging.error(f'Failed to simulate plug, port={port} on {gfx_adapter_info.gfxIndex}')
        return status

    ##
    # @brief        API to simulate unplug
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @param[in]    is_low_power - True if Low Power State, False otherwise
    # @param[in]    port_type - connector port type
    # @return       status - True on Success, False otherwise
    def _unplug(self, gfx_adapter_info, port, is_low_power, port_type):
        counter = 0
        status = False
        while counter <= RETRY_LIMIT:  # WA: HSD-18012027898, race condition between HW ISR and Valsim ISR
            status = valsim_wrapper.unplug(gfx_adapter_info, port, is_low_power, port_type)
            counter += 1
            if status is True:
                break

        if status is False:
            logging.error(f'Failed to simulate unplug, port={port} on {gfx_adapter_info.gfxIndex}')
        return status

    ##
    # @brief        API to simulate hpd
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @param[in]    attach_dettach - The status of Display port being connected or disconnected
    # @param[in]    port_type - connector port type
    # @return       status - True on Success, False otherwise.
    def _set_hpd(self, gfx_adapter_info, port, attach_dettach, port_type):
        counter = 0
        status = False
        while counter <= RETRY_LIMIT:  # WA: HSD-18012027898, race condition between HW ISR and Valsim ISR
            status = valsim_wrapper.set_hpd(gfx_adapter_info, port, attach_dettach, port_type)
            counter += 1
            if status is True:
                break

        if status is False:
            logging.error(f'Failed to simulate hpd, port={port} on {gfx_adapter_info.gfxIndex}')
            gdhm.report_bug(
                f'[GfxValSim] Failed to simulate hpd',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    ##
    # @brief        API to trigger long pulse interrupt.
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @param[in]    attach_dettach - The status of Display being connected or disconnected
    # @param[in]    port_type - connector port type
    # @return       status - True on Success, False otherwise.
    def _trigger_interrupt(self, gfx_adapter_info, port, attach_dettach, port_type):
        counter = 0
        status = False
        while counter <= RETRY_LIMIT:  # WA: HSD-18012027898, race condition between HW ISR and Valsim ISR
            status = valsim_wrapper.trigger_interrupt(gfx_adapter_info, port, attach_dettach, port_type)
            counter += 1
            if status is True:
                break

        if status is False:
            logging.error(f'Failed to trigger interrupt, port={port} on {gfx_adapter_info.gfxIndex}')
            gdhm.report_bug(
                f'[GfxValSim] Failed to trigger interrupt',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    ##
    # @brief        API to simulate spi
    # @param[in]    gfx_adapter_info - Graphics Adapter Info
    # @param[in]    port - connector port
    # @param[in]    port_type - connector port type
    # @return       status - True on Success False, otherwise
    def _set_spi(self, gfx_adapter_info, port, port_type):
        counter = 0
        status = False
        connector_type = 'NATIVE' if port_type == 'PLUS' else port_type
        port_phy_type = getattr(valsim_args.PortPhyType, connector_type).value
        port_num = getattr(valsim_args.ValSimPort, port).value

        port_details = valsim_args.ValsimPortHpdArgs()
        port_details.PortNum = port_num
        port_details.AttachorDettach = True
        port_details.PortConnectorInfo = port_phy_type

        while counter <= RETRY_LIMIT:  # WA: HSD-18012027898, race condition between HW ISR and Valsim ISR
            status = valsim_wrapper.perform_ioctl_call(gfx_adapter_info, 12, port_details)
            counter += 1
            if status is True:
                break

        if status is False:
            logging.error(f'Failed to simulate spi, port={port} on {gfx_adapter_info.gfxIndex}')
            gdhm.report_bug(
                f'[GfxValSim] Failed to simulate spi',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    ##
    # @brief        API to generate MIPI TE
    # @param[in]    gfx_adapter_info - Graphics Adapter Info
    # @param[in]    port - connector port
    # @return       status - True on Success, False otherwise
    def _generate_mipi_te(self, gfx_adapter_info, port):
        status = valsim_wrapper.generate_mipi_te(gfx_adapter_info, port)
        if status is False:
            logging.error(f'Failed to generate mipi TE, port={port} on {gfx_adapter_info.gfxIndex}')
            gdhm.report_bug(
                f'[GfxValSim] Failed to generate mipi TE',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P3,
                gdhm.Exposure.E3
            )
        return status

    ##
    # @brief        Fills the link training related default DPCD model data (for PASSing link training in
    #               first two transactions itself) in the object passed
    # @param[in]    dpcd_model_data - object to be filled with DPCD model data
    # @param[in]    connector_port - port for which we are filling this data
    # @return       None
    def _fill_default_dpcd_model_data(self, dpcd_model_data, connector_port):
        transaction_count = 2
        num_input_dpcd_sets = 0
        input_dpcd_set_length = 0
        num_response_dpcd_sets = 1
        response_dpcd_set_length = 3
        # 1st transaction for CR Pass, and 2nd transaction for CHEQ pass
        input_starting_offsets = [0x102, 0x102]
        input_values = [[0x0],
                        [0x0]]
        response_starting_offsets = [0x202, 0x202]
        response_values = [[0x11, 0x11, 0x80],
                           [0x77, 0x77, 0x8D]]
        trigger_offset_for_trans = 0x103

        dpcd_model_data.uiPortNum = getattr(valsim_args.ValSimPort, connector_port).value
        dpcd_model_data.eTopologyType = getattr(DpTopology, 'DPSST').value
        model_data = dpcd_model_data.stDPCDModelData
        model_data.ucTransactionCount = transaction_count
        model_data.ulTriggerOffset = trigger_offset_for_trans

        for trans_index in range(model_data.ucTransactionCount):
            dpcd_trans = model_data.stDPCDTransactions[trans_index]

            dpcd_trans.ucNumInputDpcdSets = num_input_dpcd_sets
            dpcd_trans.stInputDpcdSets[0].ulStartingOffset = input_starting_offsets[trans_index]
            dpcd_trans.stInputDpcdSets[0].ucLength = input_dpcd_set_length
            for i in range(input_dpcd_set_length):
                dpcd_trans.stInputDpcdSets[0].ucValues[i] = input_values[trans_index][i]

            dpcd_trans.ucNumResponseDpcdSets = num_response_dpcd_sets
            dpcd_trans.stResponseDpcdSets[0].ulStartingOffset = response_starting_offsets[trans_index]
            dpcd_trans.stResponseDpcdSets[0].ucLength = response_dpcd_set_length
            for i in range(response_dpcd_set_length):
                dpcd_trans.stResponseDpcdSets[0].ucValues[i] = response_values[trans_index][i]

    ##
    # @brief        API to read display MMIO register.
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    offset - Offset value in Hex
    # @return       value - MMIO offset value
    def read_mmio(self, gfx_adapter_info, offset):
        value = valsim_wrapper.read_mmio(gfx_adapter_info, offset)
        if value is None:
            logging.error(f'{gfx_adapter_info.gfxIndex} - mmio read failed for offset={offset}')
            gdhm.report_bug(
                f'[GfxValSim] MMIO read failed',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return value

    ##
    # @brief        API to write display MMIO register
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    offset - register offset in Hex.
    # @param[in]    value - value in Hex.
    # @return       status - True on Success, False otherwise
    def write_mmio(self, gfx_adapter_info, offset, value):
        status = valsim_wrapper.write_mmio(gfx_adapter_info, offset, value)
        if status is False:
            logging.error(f'{gfx_adapter_info.gfxIndex} - mmio write failed for offset={offset} value={value}')
            gdhm.report_bug(
                f'[GfxValSim] MMIO write failed',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    ##
    # @brief        API write generated vbt data and vbt size to regkey 'VBT' and 'VBTSIZE'
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    custom_vbt - modified VBT Block
    # @param[in]    vbt_size - modified VBT size.
    # @return       status - True on Success, False otherwise
    def _configure_vbt(self, gfx_index, custom_vbt, vbt_size):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]

        is_vbt_in_oprom = oprom_parser._is_vbt_in_oprom(gfx_index)
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=None, feature=registry_access.Feature.VALSIM)

        if is_vbt_in_oprom:
            custom_oprom_key = str(adapter_info.busDeviceID) + REG_KEY_CUSTOM_OPROM
            custom_oprom_size_key = str(adapter_info.busDeviceID) + REG_KEY_CUSTOM_OPROM_SIZE

            status, oprom_data = oprom_parser._get_merged_oprom_data(gfx_index, custom_vbt)
            if status is True:
                status = registry_access.write(args=reg_args, reg_name=custom_oprom_key,
                                               reg_type=registry_access.RegDataType.BINARY, reg_value=bytes(oprom_data))
                if status is True:
                    status = registry_access.write(args=reg_args, reg_name=custom_oprom_size_key,
                                                   reg_type=registry_access.RegDataType.DWORD,
                                                   reg_value=len(oprom_data))
        else:
            custom_vbt_key = str(adapter_info.busDeviceID) + REG_KEY_CUSTOM_VBT
            custom_vbt_size_key = str(adapter_info.busDeviceID) + REG_KEY_CUSTOM_VBT_SIZE

            status = registry_access.write(args=reg_args, reg_name=custom_vbt_key,
                                           reg_type=registry_access.RegDataType.BINARY, reg_value=bytes(custom_vbt))
            if status is True:
                status = registry_access.write(args=reg_args, reg_name=custom_vbt_size_key,
                                               reg_type=registry_access.RegDataType.DWORD, reg_value=vbt_size)

        if status is False:
            logging.error(f'{gfx_index} - Failed to configure VBT')
            gdhm.report_bug(
                f'[GfxValSim] Failed to configure VBT',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        else:
            self.configure_feature(gfx_index, GFXVALSIM_FEATURE_VBT_SIMULATION, True)

        return status

    ##
    # @brief        API get default VBT
    # @param[in]    gfx_index - Graphics Adapter index
    # @return       vbt_data - default VBT data
    def _get_default_vbt(self, gfx_index):
        status = True
        vbt_data = None

        # Call check from test environment Phase only.
        # Fetch VBT only if gfx driver and ValSim driver are running
        if state_machine_manager.StateMachine().test_phase != state_machine_manager.TestPhase.TEST:
            ret_status = True
            if machine_info.check_gfx_drivers_running() is False:
                gdhm.report_bug(
                    f"[GfxValSim] Intel Graphics Driver is not running while fetching default VBT",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES,
                    gdhm.Priority.P1,
                    gdhm.Exposure.E1
                )
                logging.error("Gfx driver(s) is/are not running, VBT fetch failed")
                ret_status = False

            if machine_info.check_gfxvalsim_running() is False:
                gdhm.report_bug(
                    f"[GfxValSim] Valsim driver is not running, while fetching default VBT",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES,
                    gdhm.Priority.P1,
                    gdhm.Exposure.E1
                )
                logging.error("GfxValsim is not running, VBT fetch failed")
                ret_status = False
            if not ret_status:
                return None

        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=None, feature=registry_access.Feature.VALSIM)
        actual_vbt_key = str(adapter_info.busDeviceID) + REG_KEY_ACTUAL_VBT

        size, reg_type = registry_access.read(args=reg_args, reg_name=actual_vbt_key)
        if size is None or size == 0:
            logging.error(f'{gfx_index} - Failed to read VBT data length')
            status = False

        if status is True:
            vbt_data, data_type = registry_access.read(args=reg_args, reg_name=actual_vbt_key)
            if vbt_data is None:
                logging.error(f'{gfx_index} - Failed to read default VBT')
                status = False
            if data_type is not None and registry_access.RegDataType(data_type) == registry_access.RegDataType.BINARY:
                vbt_data = list(vbt_data)

        if status is False:
            gdhm.report_bug(
                f'[GfxValSim] Failed to read default VBT',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return vbt_data

    ##
    # @brief        API to reset default VBT
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       status - True if VBT reset is successful, False otherwise
    def _reset_vbt(self, gfx_index):
        status = self.configure_feature(gfx_index, GFXVALSIM_FEATURE_VBT_SIMULATION, False)
        if status is False:
            logging.error(f'{gfx_index} - Failed to reset VBT')
            gdhm.report_bug(
                f'[GfxValSim] Failed to reset VBT',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    ##
    # @brief        API to close val sim handle
    # @return       status - True on Success, False otherwise
    def _cleanup_val_sim(self):
        status = valsim_wrapper.close_gfx_val_simulator()
        if status is False:
            logging.error(f'Failed to cleanup val sim')
            gdhm.report_bug(
                f'[GfxValSim] Failed to cleanup val sim',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    ##
    # @brief        Get all port info from cmd line argument.
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    lfp - True if LFP , False otherwise.
    # @return       port_list - list of Ports
    def __get_port(self, gfx_index, lfp):
        custom_tags = cmd_parser.get_custom_tag()
        buffer = {}
        port_list = []
        result_dict = cmd_parser.parse_cmdline(sys.argv, custom_tags=custom_tags)
        if not isinstance(result_dict, list):
            result_dict = [result_dict] + [{}] * (cmd_parser.MAX_ADAPTER_COUNT - 1)

        for element in result_dict:
            for key, value in element.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if gfx_index.upper() == value['gfx_index']:
                        buffer[key] = value

        for key, value in buffer.items():
            if value['is_lfp'] is lfp:
                port_name = value['connector_port']

                # if connector port type is plus, we need to initialize both encoder for specific DDI's
                if 'PLUS' == str(value['connector_port_type']).upper():
                    encoder_ddi_name = port_name.split('_')
                    port_list.append('DP' + '_' + str(encoder_ddi_name[1]).upper())
                    port_list.append('HDMI' + '_' + str(encoder_ddi_name[1]).upper())
                else:
                    port_list.append(port_name)

        port_list = list(dict.fromkeys(port_list))  # Remove duplicate entry from list
        return port_list

    ##
    # @brief        API to get platform details
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       platform_info - Platform details
    def get_platform_details(self, gfx_index):
        platform_info = valsim_args.ValSimPlatformInfo()
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        status = valsim_wrapper.perform_ioctl_call(adapter_info, 11, platform_info)
        if status is not True:
            logging.error(f'{gfx_index} - Failed to get platform details')
            gdhm.report_bug(
                f'[GfxValSim] {gfx_index} - Failed to get platform details',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        elif machine_info.check_gfx_drivers_running() is False:
            gdhm.report_bug(
                f"[GfxValSim] Intel Graphics Driver is not running, failed to get platform details",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("Gfx driver(s) is/are not running, failed to get platform details")

        elif machine_info.check_gfxvalsim_running() is False:
            gdhm.report_bug(
                f"[GfxValSim] Valsim is not running, failed to get platform details",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("GfxValsim is not running, failed to get platform details")
        else:
            logging.info(f"GfxPlatform:{valsim_args.GfxPlatform(platform_info.GfxPlatform).name}, "
                         f"GfxPchFamily:{valsim_args.GfxPchFamily(platform_info.GfxPchFamily).name}, "
                         f"GmdId-Rev:{platform_info.GfxGmdId.RevisionID}, GmdArch:{platform_info.GfxGmdId.GmdArch},"
                         f" GmdRelease:{platform_info.GfxGmdId.GmdRelease}")

        return platform_info

    ##
    # @brief        API to get driver WA table
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    driver_wa - Driver WA type
    # @return       data - True / false
    def get_driver_wa_table(self, gfx_index: str, driver_wa: valsim_args.DriverWa):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        status, data = valsim_wrapper.get_driver_wa_table(adapter_info, driver_wa.value)
        if status is None or status is False:
            logging.error(f'{gfx_index} - Failed to get driver wa table')
            gdhm.report_bug(
                f'[GfxValSim] Failed to get driver wa table data',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
            return None
        logging.info(f'{valsim_args.DriverWa(driver_wa).name} value {data}')
        return bool(data)

    ##
    # @brief            Get Display Adapter caps
    # @return           (status, str) - (status of display adapter, details of display adapter)
    def get_all_adapter_caps(self) -> (bool, adapter_info_struct.DisplayAdapterCapsDetails):
        disp_adapter_caps_details = adapter_info_struct.DisplayAdapterCapsDetails()
        adapter_info = adapter_info_struct.GfxAdapterInfo()
        status = valsim_wrapper.perform_ioctl_call(adapter_info, ValSimIoctlCode.GET_ALL_ADAPTER_CAPS.value,
                                                   disp_adapter_caps_details)
        if status is True:
            logging.debug(f'Display Adapter Capabilities obtained successfully')
        return status, disp_adapter_caps_details

    ##
    # @brief        API get default OpRegion
    # @param[in]    gfx_index - Graphics Adapter index
    # @return       opregion_data - default OpRegion data
    def get_default_opregion(self, gfx_index):
        # Fetch OpRegion only if gfx driver and ValSim driver are running
        ret_status = True
        if machine_info.check_gfx_drivers_running() is False:
            gdhm.report_bug(
                f"[GfxValSim] Intel Graphics Driver is not running, OpRegion fetch failed",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("Gfx driver(s) is/are not running, OpRegion fetch failed")
            ret_status = False

        if machine_info.check_gfxvalsim_running() is False:
            gdhm.report_bug(
                f"[GfxValSim] Valsim is not running, OpRegion fetch failed",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("GfxValsim is not running, OpRegion fetch failed")
            ret_status = False

        if not ret_status:
            return None, None

        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index, feature=registry_access.Feature.VALSIM)
        actual_opregion_key = str(adapter_info.busDeviceID) + REG_KEY_ACTUAL_OPREGION
        actual_opregion_size_key = actual_opregion_key + "_Size"

        status = True
        opregion_data = None
        opregion_size, _ = registry_access.read(args=reg_args, reg_name=actual_opregion_size_key)
        if opregion_size is None or opregion_size == 0:
            logging.error(f'Failed to read OpRegion size for adapter {gfx_index}')
            status = False
        else:
            opregion_data, data_type = registry_access.read(args=reg_args, reg_name=actual_opregion_key)
            if opregion_data is None or not (data_type is not None and registry_access.RegDataType(
                    data_type) == registry_access.RegDataType.BINARY):
                logging.error(f'Failed to read default OpRegion for adapter {gfx_index} ')
                status = False
            else:
                opregion_data = list(opregion_data)

        if status is False:
            gdhm.report_bug(
                f'[GfxValSim] Failed to read default OpRegion',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return opregion_data, opregion_size

    ##
    # @brief        API to update panel dpcd
    # @param[in]    gfx_index Gfx_0/GFX_1
    # @param[in]    port - connector port
    # @param[in]    offset - DPCD offset
    # @param[in]    val - DPCD value
    # @return       status - True on Success False, otherwise
    def set_panel_dpcd(self, gfx_index: str, port: str, offset: int, val: int) -> bool:
        status = False
        # update dpcd only if gfx driver and ValSim driver are running
        ret_status = True
        if machine_info.check_gfx_drivers_running() is False:
            gdhm.report_bug(
                f"[GfxValSim] Intel Graphics Driver is not running, failed to update panel DPCD",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("Gfx driver(s) is/are not running, failed to update panel DPCD")
            ret_status = False

        if machine_info.check_gfxvalsim_running() is False:
            gdhm.report_bug(
                f"[GfxValSim] Valsim is not running, failed to update panel DPCD",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P1,
                gdhm.Exposure.E1
            )
            logging.error("GfxValsim is not running, failed to update panel DPCD")
            ret_status = False

        if not ret_status:
            return None

        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        port = getattr(valsim_args.ValSimPort, port).value
        status = valsim_wrapper.set_panel_dpcd(adapter_info, port, offset, val)
        if status is False:
            logging.error(f'Failed to update panel dpcd {hex(offset)} on PortId={port}')
            gdhm.report_bug(
                f'[GfxValSim] Failed to update panel dpcd',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status

    # @brief        API to trigger SCDC interrupt.
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @return       status - True on Success, False otherwise.
    def _trigger_scdc_interrupt(self, gfx_adapter_info: adapter_info_struct.GfxAdapterInfo, port: str,
                                scdc_failure_type: valsim_args.SpiEventType) -> bool:
        status = valsim_wrapper.trigger_scdc_interrupt(gfx_adapter_info, port, scdc_failure_type)

        if status is False:
            logging.error(f'Failed to trigger SCDC interrupt, port={port} on {gfx_adapter_info.gfxIndex}')
            gdhm.report_bug(
                f'[GfxValSim] Failed to trigger SCDC interrupt',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        return status


    ##
    # @brief        API write to initialize Test MMIO
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    test_mmio_list - List of Lists containing mmio offset and value like [(70180,0),(0x51004, 0x40)].
    # @return       status - True on Success, False otherwise
    def initialize_test_mmio(self, gfx_index, test_mmio_list):
        if (len(test_mmio_list)) ==0:
            return

        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        test_mmio = valsim_args.ValsimTestMmmioInitArgs()

        test_mmio.ulNumRegisters = len(test_mmio_list)
        for i in range(len(test_mmio_list)):
            test_mmio.stMMIOList[i].ulMMIOOffset = test_mmio_list[i][0]
            test_mmio.stMMIOList[i].ulMMIOData = test_mmio_list[i][1]

        reg_args = registry_access.StateSeparationRegArgs(gfx_index=None, feature=registry_access.Feature.VALSIM)

        custom_vbt_key = str(adapter_info.busDeviceID) + REG_KEY_INIT_TEST_MMIO
        status = registry_access.write(args=reg_args, reg_name=custom_vbt_key,
                                       reg_type=registry_access.RegDataType.BINARY, reg_value=bytes(test_mmio))

        if status is False:
            logging.error(f'{gfx_index} - Failed to configure Test MMIO')
            gdhm.report_bug(
                f'[GfxValSim] Failed to configure Test MMIO',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
        else:
            self.configure_feature(gfx_index, GFXVALSIM_FEATURE_INIT_TEST_MMIO, True)

        return status

    ##
    # @brief        API to Acquire or release wakelock
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    acquire_release - flag to specify request type as wakelock acquire or release
    # @return       status - True / false
    def handle_wakelock(self, gfx_index: str, acquire_release):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        status = valsim_wrapper.Handle_Wakelock(adapter_info, acquire_release)
        if status is None or status is False:
            logging.error(f'{gfx_index} - Failed to perform wakelock access.')
            gdhm.report_bug(
                f'[GfxValSim] Failed to  perform wakelock access',
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES,
                gdhm.Priority.P2,
                gdhm.Exposure.E2
            )
            return None
        return status
