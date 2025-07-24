######################################################################################
# @file         driver_interface.py
# @brief        Python wrapper helper to Simulate displays and MMIO Access
# @author       Amit Sau
######################################################################################
from ctypes.wintypes import HANDLE

from Libs import env_settings
from Libs.Core.core_base import singleton
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import gfxvalsim
from Libs.Core.sw_sim import hybrid
from Libs.Core.test_env import test_context, state_machine_manager


##
# @brief        DriverInterface Class
# @details      Provides interface methods with driver
@singleton
class DriverInterface(object):
    __hybrid_sink = False
    __valsim_sink = False
    __she_emu_sink = False

    ##
    # @brief        Constructor
    # @details      Initialize Gfx Val sim and SHE Utility
    def __init__(self):
        self.__gfx_val_sim = None
        self.she_utility = None

        # Creating Valsim obj, since Valsim is by default required (like MMIO and VBT).
        self.__gfx_val_sim = gfxvalsim.GfxValSim()
        self.__gfx_valsim_handle = None
        self.__supported_ports: dict = {}

        simulation_type = env_settings.get('SIMULATION', 'simulation_type')
        if simulation_type is not None and simulation_type == 'HYBRID':
            self.__hybrid_sink = True
        elif simulation_type is not None and simulation_type == 'SHE':
            # she_emulator imports serial package. This package won't be installed on Valsim based test TPs.
            # So importing this here and not globally.
            from Libs.Core.hw_emu.she_emulator import SheUtility
            self.__she_emu_sink = True
            self.she_utility = SheUtility()
        else:
            self.__valsim_sink = True

    ##
    # @brief        API to get Valsim handle
    # @return       int - Valsim Handle
    def get_driver_handle(self) -> HANDLE:
        return self.__gfx_valsim_handle

    ##
    # @brief        Initialize Driver Interface modules.
    # @return       None
    def init_driver_interface(self) -> None:
        # Initializing Valsim, since Valsim is by default required (like MMIO and VBT).
        if self.__gfx_valsim_handle is None:
            self.__gfx_valsim_handle = self.__gfx_val_sim._init_gfx_val_sim()

        if self.__she_emu_sink:
            self.she_utility.initialize()

    ##
    # @brief        Initialize all EFP ports
    # @return       None
    def initialize_all_efp_ports(self) -> None:
        if self.__valsim_sink is True:
            self.__gfx_val_sim._init_all_efp_ports()

    ##
    # @brief        Initialize all LFP ports
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    lfp_port_list - list of LFP ports
    # @return       bool - True if LFP ports are initialized, False if not initialized, else None
    def initialize_lfp_ports(self, gfx_adapter_info, lfp_port_list) -> bool:
        if self.__valsim_sink is True:
            return self.__gfx_val_sim._init_lfp_ports(gfx_adapter_info, lfp_port_list)

    ##
    # @brief    Get all adapter caps
    # @return   (status, disp_adapter_caps) - (ioctl call status, display adapter caps details)
    def get_all_adapter_caps(self):
        return self.__gfx_val_sim.get_all_adapter_caps()

    ##
    # @brief        Read display MMIO register value
    # @param[in]    offset - Register offset value in hex
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       int - Register value
    def mmio_read(self, offset: int, gfx_index: str) -> int:
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        self.handle_wakelock(gfx_index, True)
        value = self.__gfx_val_sim.read_mmio(adapter_info, offset)
        self.handle_wakelock(gfx_index, False)
        return value

    ##
    # @brief        Write display MMIO register value
    # @param[in]    offset - Register offset in Hex
    # @param[in]    value - Register value in Hex
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       bool - True on successful MMIO write, False otherwise
    def mmio_write(self, offset: int, value: int, gfx_index: str) -> bool:
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        self.handle_wakelock(gfx_index, True)
        status = self.__gfx_val_sim.write_mmio(adapter_info, offset, value)
        self.handle_wakelock(gfx_index, False)
        return status

    ##
    # @brief        Simulate Plug on Specified Port
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @param[in]    edid_path - EDID File Path
    # @param[in]    dpcd_path - DPCD File path
    # @param[in]    is_low_power - True if Low power state, False otherwise
    # @param[in]    port_type -  connector Port Type
    # @param[in]    is_lfp - True if requested port is LFP , False if it's EFP
    # @param[in]    dp_dpcd_model_data - model data containing DPCD transactions to be done
    # @param[in]    dongle_type -  Dongle Type
    # @return       bool - True on plug simulation success, False otherwise
    def simulate_plug(self, gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type='NATIVE',
                      is_lfp=False, dp_dpcd_model_data=None, dongle_type=None) -> bool:
        if self.__hybrid_sink is True:
            return hybrid.hybrid_plug(gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type, is_lfp)
        elif self.__she_emu_sink is True:
            return self.she_utility.plug(gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type)
        else:
            return self.__gfx_val_sim._plug(gfx_adapter_info, port, edid_path, dpcd_path, is_low_power, port_type,
                                            is_lfp, dp_dpcd_model_data, dongle_type)

    ##
    # @brief        Simulate Unplug on Specified Port
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @param[in]    is_low_power - True if Low power state, False otherwise
    # @param[in]    port_type - connector port type
    # @return       bool - True on simulate unplug success, False otherwise
    def simulate_unplug(self, gfx_adapter_info, port, is_low_power, port_type="NATIVE") -> bool:
        if self.__hybrid_sink is True:
            return hybrid.hybrid_unplug(gfx_adapter_info, port, is_low_power, port_type)
        elif self.__she_emu_sink is True:
            return self.she_utility.unplug(gfx_adapter_info, port, is_low_power, port_type)
        else:
            return self.__gfx_val_sim._unplug(gfx_adapter_info, port, is_low_power, port_type)

    ##
    # @brief        Get Supported ports for given adapter
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       dict - Supported port dictionary
    def get_supported_ports(self, gfx_index='gfx_0'):
        from Libs.Core.vbt.vbt import Vbt
        # check for VBT state change or requested supported ports availablity in __supported_ports dictionary
        if gfx_index not in state_machine_manager.StateMachine().vbt_state_change.keys() or \
                state_machine_manager.StateMachine().vbt_state_change[gfx_index] is True or \
                gfx_index not in self.__supported_ports.keys():
            self.__supported_ports[gfx_index] = Vbt(gfx_index)._get_supported_ports()
            state_machine_manager.StateMachine().update_vbt_state_change(gfx_index, False)
        return self.__supported_ports[gfx_index]

    ##
    # @brief        Checks if panel timings whether non zero.
    # @details      Using only with SHE emulator as of now, where we read back the timing info from emulator.
    # @param[in]    gfx_adapter_info - Graphics Adapter Information
    # @param[in]    port - connector port
    # @param[in]    sink_index - Sink index
    # @return       bool - True if timings are non-zero, False otherwise.
    def is_panel_timings_non_zero(self, gfx_adapter_info, port, sink_index=0) -> bool:
        if self.__she_emu_sink is True:
            return self.she_utility.is_emulator_timing_non_zero(gfx_adapter_info, port, sink_index)
        else:
            return True

    ##
    # @brief        API to simulate HPD
    # @param[in]    gfx_adapter_info - gfx adapter info
    # @param[in]    port - port name
    # @param[in]    attach_dettach - flag to specify request type as attach or detach
    # @param[in]    port_type - connector port type
    # @return       bool - True on Success otherwise return False
    def set_hpd(self, gfx_adapter_info, port, attach_dettach, port_type) -> bool:
        if self.__valsim_sink is True:
            return self.__gfx_val_sim._set_hpd(gfx_adapter_info, port, attach_dettach, port_type)

    ##
    # @brief        API to trigger long pulse interrupt
    # @param[in]    gfx_adapter_info - gfx adapter info
    # @param[in]    port - port name
    # @param[in]    attach_dettach - flag to specify request type as attach or detach
    # @param[in]    port_type - connector port type
    # @return       bool - True on Success otherwise return False
    def trigger_interrupt(self, gfx_adapter_info, port, attach_dettach, port_type) -> bool:
        if self.__valsim_sink is True:
            return self.__gfx_val_sim._trigger_interrupt(gfx_adapter_info, port, attach_dettach, port_type)

    ##
    # @brief        API to simulate SPI
    # @param[in]    gfx_adapter_info - gfx adapter info
    # @param[in]    port - port name
    # @param[in]    port_type - connector port type
    # @return       bool - True on Success otherwise return False
    def set_spi(self, gfx_adapter_info, port, port_type) -> bool:
        if self.__valsim_sink is True:
            return self.__gfx_val_sim._set_spi(gfx_adapter_info, port, port_type)

    ##
    # @brief        API to generate MIPI TE
    # @param[in]    gfx_adapter_info - gfx adapter info
    # @param[in]    port - port name
    # @return       bool - True on Success otherwise return False
    def generate_mipi_te(self, gfx_adapter_info, port) -> bool:
        return self.__gfx_val_sim._generate_mipi_te(gfx_adapter_info, port)

    ##
    # @brief        Method to verify both gfx driver and ValSim Driver status
    # @details      If current simulation_type config requires GfxValSim driver, this method will verify it's status
    # @return       None
    @staticmethod
    def verify_graphics_driver_status():
        return machine_info.check_gfx_drivers_running(), machine_info.check_gfxvalsim_running()

    ##
    # @brief        API to get platform details
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       platform_info - Platform details
    def get_platform_details(self, gfx_index):
        return self.__gfx_val_sim.get_platform_details(gfx_index)

    ##
    # @brief        API to get default OpRegion
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       opregion_data - OpRegion data
    def get_default_opregion(self, gfx_index):
        return self.__gfx_val_sim.get_default_opregion(gfx_index)

    ##
    # @brief        API to update Panel DPCD's at run time
    # @param[in]    gfx_index gfx_0/gfx_1
    # @param[in]    port - port name
    # @param[in]    offset - DPCD offset
    # @param[in]    value - DPCD value
    # @return       bool - True on Success otherwise return False
    def set_panel_dpcd(self, gfx_index: str, port: str, offset: int, value: int) -> bool:
        if self.__valsim_sink is True:
            return self.__gfx_val_sim.set_panel_dpcd(gfx_index, port, offset, value)

    ##
    # @brief        API to trigger SCDC interrupt
    # @param[in]    gfx_adapter_info - gfx adapter info
    # @param[in]    port - port name
    # @param[in]    scdc_failure_type - flag to specify request type
    # @return       bool - True on Success otherwise return False
    def trigger_scdc_interrupt(self, gfx_adapter_info, port, scdc_failure_type) -> bool:
        if self.__valsim_sink is True:
            return self.__gfx_val_sim._trigger_scdc_interrupt(gfx_adapter_info, port, scdc_failure_type)

    ##
    # @brief        API to get default OpRegion
    # @param[in]    gfx_index gfx_0/gfx_1
    # @param[in]    wa_data driver_wa data
    # @return       (status,data) - (IOCTL Call status, WA Data)
    def get_driver_wa_table(self, gfx_index, wa_data):
        return self.__gfx_val_sim.get_driver_wa_table(gfx_index, wa_data)

    ##
    # @brief        API to get default OpRegion
    # @param[in]    gfx_index gfx_0/gfx_1
    # @param[in]    acquire_release - flag to specify request type as wakelock acquire or release
    # @return       bool - True on Success otherwise return False
    def handle_wakelock(self, gfx_index, acquire_release):
        return self.__gfx_val_sim.handle_wakelock(gfx_index, acquire_release)