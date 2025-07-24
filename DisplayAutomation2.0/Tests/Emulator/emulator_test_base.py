#######################################################################################################################
# @file         emulator_test_base.py
# @section      Tests
# @brief        Emulator Base class contains Setup and Tear down class methods to initialize and cleanup the tests
#               respectively. Apart from that it also contains common methods used across different Emulator test cases.
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
from typing import Dict, Tuple, List, Optional
from unittest import TestCase

from Libs.Core import enum
from Libs.Core.display_config import display_config_enums
from Libs.Core.display_config.display_config_struct import DisplayMode, EnumeratedDisplaysEx, DisplayTimings
from Libs.Core.display_power import DisplayPower
from Libs.Core.hw_emu.emulator_helper import ConfigData, EmulatorTestCommandParser, TiledPanelInfo, HubDisplayInfo
from Libs.Core.hw_emu.she_emulator import SheUtility
from Libs.Core.sw_sim.dp_mst import DisplayPort, TiledInformation
from Libs.Core.sw_sim.driver_interface import DriverInterface
from Libs.Core.display_config.display_config import DisplayConfiguration


tbt_port_pairs = {
    "ICLLP": {
        "DP_C": ("DP_C", "DP_D"),
        "DP_E": ("DP_E", "DP_F")
    },
    "TGL": {
        "DP_D": ("DP_D", "DP_E"),
        "DP_F": ("DP_F", "DP_G")
    },
    "ADLP": {
        "DP_F": ("DP_F", "DP_G"),
        "DP_H": ("DP_H", "DP_I")
    }
}


##
# @brief        This class has to be inherited by all the test cases that tests scenarios related to MST Tiled.
class EmulatorTestBase(TestCase):
    she_utility: SheUtility
    display_power: DisplayPower
    display_config: DisplayConfiguration
    display_port: DisplayPort
    emulator_command_parser: EmulatorTestCommandParser
    mst_port_panel_dict: Dict[str, TiledPanelInfo]
    sst_port_panel_dict: Dict[Tuple[str, Optional[str]], TiledPanelInfo]
    tbt_hub_port_display_info_dict: Dict[str, List[HubDisplayInfo]]

    ##
    # @brief        A class method which initializes all the required class members.
    # @return       None
    @classmethod
    def setUpClass(cls) -> None:
        cls.she_utility = DriverInterface().she_utility  # Using the same object defined during test env initialization.
        cls.display_port = DisplayPort()
        cls.display_power = DisplayPower()
        cls.display_config = DisplayConfiguration()
        cls.emulator_command_parser = EmulatorTestCommandParser()
        cls.mst_port_panel_dict = {}
        cls.sst_port_panel_dict = {}
        cls.tbt_hub_port_display_info_dict = {}

    ##
    # @brief        A class method to to apply the configuration(SINGLE/EXTENDED) based on the no of displays passed.
    # @param[in]    port_list: List[str]
    #                   List of port name for which display config has to be applied
    # @return       is_success: bool
    #                   Return True if set display config succeeds else False
    @classmethod
    def apply_config(cls, port_list: List[str]) -> bool:
        config: ConfigData = cls.get_config_to_apply(port_list)

        logging.info("Applying Display Config {} for {}".format(config.name, config.port_list))
        is_success = cls.display_config.set_display_configuration_ex(config.topology, config.port_list)

        return is_success

    ##
    # @brief        A class method that sets the max mode for each of the target id in the target_id_list.
    # @param[in]    target_id_list: List[int]
    #                   List of Target id's for which max mode has to be set.
    # @return       is_success: bool
    #                   Returns True if Set mode is succeeds for all the target id's in the list False otherwise and the mode that is applied for each target_id
    @classmethod
    def set_max_mode(cls, target_id_list: List[int]):
        supported_mode_dict = cls.display_config.get_all_supported_modes(target_id_list, sorting_flag=True)
        is_success = bool(supported_mode_dict)
        applied_mode = {}
        for target_id, supported_mode_list in supported_mode_dict.items():
            logging.debug("List of supported modes for Target id: {}".format(target_id))
            for display_mode in supported_mode_list:
                logging.debug('HRes:{} VRes:{} RR:{} BPP:{}, SamplingMode: {}, ScanlineOrdering: {}'.format(
                    display_mode.HzRes, display_mode.VtRes, display_mode.refreshRate, display_mode.BPP,
                    display_mode.samplingMode.Value, display_mode.scanlineOrdering
                ))
                applied_mode[target_id] = [display_mode.HzRes, display_mode.VtRes, display_mode.refreshRate]

            max_mode = supported_mode_list[-1]
            is_success &= cls.display_config.set_display_mode([max_mode])

        return is_success, applied_mode

    ##
    # @brief        A class method which verifies the Tiled Mode by comparing the Edid mode(parsed from edid) and the
    #               mode set by the driver.
    # @param[in]    tiled_target_id_list: List[int]
    #                   List of target id's for which tiled mode has to be verified.
    # @return       is_success: bool
    #                   Returns True if tiled mode is successfully verified for all the target id's False otherwise.
    @classmethod
    def verify_tiled_mode(cls, tiled_target_id_list: List[int]) -> bool:
        is_success, applied_mode = cls.set_max_mode(tiled_target_id_list)

        if is_success is True:
            for tiled_target_id in tiled_target_id_list:
                tiled_panel_info: TiledInformation = cls.display_port.get_tiled_display_information(tiled_target_id)

                native_mode = cls.display_config.get_native_mode(tiled_target_id)
                native_h_res, native_v_res, native_rr = cls.parse_native_mode(native_mode)

                current_mode: DisplayMode = cls.display_config.get_current_mode(tiled_target_id)
                actual_h_res, actual_v_res, actual_rr = current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate

                if tiled_panel_info.TiledStatus is True:
                    exp_h_res, exp_v_res, exp_rr = tiled_panel_info.HzRes, tiled_panel_info.VtRes, native_rr
                else:
                    logging.error("Tiled information not available in the Tiled display. Exiting ...")
                    is_success = False
                    return is_success

                # TODO: Currently we RR might vary by ~1.5%. Need to discuss on this.
                if current_mode.HzRes == exp_h_res and current_mode.VtRes == exp_v_res:
                    logging.info(
                        "Tiled mode [Driver Enumerated] = {}x{}@{}hz and Tiled mode [From EDID] = {}x{}@{}hz "
                        "are identical".format(
                            actual_h_res, actual_v_res, actual_rr, exp_h_res, exp_v_res, exp_rr
                        )
                    )
                else:
                    logging.error(
                        "[Driver Issue] - Tiled Mode [Driver Enumerated]= {}x{}@{}hz and Tiled Mode "
                        "[From Edid] = {}x{}@{}hz are different".format(
                            actual_h_res, actual_v_res, actual_rr, exp_h_res, exp_v_res, exp_rr
                        )
                    )
                    is_success = False

            return is_success

    ##
    # @brief        A class method which verifies the max non tiled mode comparing the Native mode with the current
    #               mode(max mode)
    # @param[in]    non_tiled_target_id_list: List[int]
    #                   List of target id's for which non tiled mode has to be verified.
    # @return       is_success: bool
    #                   Returns True if non tiled mode is successfully verified for all the target id's False otherwise.
    @classmethod
    def verify_non_tiled_mode(cls, non_tiled_target_id_list: List[int]) -> bool:
        is_success, applied_mode = cls.set_max_mode(non_tiled_target_id_list)

        if is_success is True:
            for tiled_target_id in non_tiled_target_id_list:

                native_mode = cls.display_config.get_native_mode(tiled_target_id)
                exp_h_res, exp_v_res, exp_rr = cls.parse_native_mode(native_mode)
                current_mode: DisplayMode = cls.display_config.get_current_mode(tiled_target_id)
                actual_h_res, actual_v_res, actual_rr = current_mode.HzRes, current_mode.VtRes, current_mode.refreshRate

                # TODO: Currently RR might vary by ~1.5%. Need to discuss on this.
                if actual_h_res == exp_h_res and actual_v_res == exp_v_res:
                    logging.info(
                        "Tiled Disabled Mode [Driver Enumerated] = {0}x{1}@{2}hz and Tiled Disabled Mode [From EDID] = "
                        "{0}x{1}@{3}hz are identical".format(
                            actual_h_res, actual_v_res, actual_rr, exp_rr
                        )
                    )
                else:
                    logging.error(
                        "[Driver Issue] - Tiled Mode [Driver Enumerated]= {}x{}@{}hz and Tiled Mode [From Edid] = "
                        "{}x{}@{}hz are different".format(
                            actual_h_res, actual_v_res, actual_rr, exp_h_res, exp_v_res, exp_rr
                        )
                    )
                    is_success = False

        return is_success

    ##
    # @brief        A class method which maps the port with the target id and returns target_id_list
    # @param[in]    port_list: List[str]
    #                   List of port names for which target id's has to be found.
    # @return       port_target_id_dict: Dict[str, List[int]]
    #                   Returns a dictionary which maps port name with the target ids.
    @classmethod
    def get_port_target_id_dict(cls, port_list: List[str]) -> Dict[str, List[int]]:
        port_target_id_dict: Dict[str, List[int]] = {}

        enumerated_displays: EnumeratedDisplaysEx = cls.display_config.get_enumerated_display_info()
        logging.info("Enumerated Displays: {}".format(enumerated_displays.to_string()))

        for each_display in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[each_display]
            port_name = display_config_enums.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            if port_name in port_list:
                port_target_id_dict.setdefault(port_name, []).append(display_info.DisplayAndAdapterInfo.TargetID)

        logging.debug("Port Target Id dict: {}".format(port_target_id_dict))
        return port_target_id_dict

    ##
    # @brief            A static method that parses the dictionary and converts to list of target ids
    # @param[in]        port_target_id_dict: Dict[str, List[int]]
    # @return           target_id_list: List[int]
    #                       List of target id parsed from the dictionary
    @staticmethod
    def get_target_id_list_from_dict(port_target_id_dict: Dict[str, List[int]]) -> List[int]:
        all_target_id_list: List[int] = []

        for port_name, target_id_list in port_target_id_dict.items():
            all_target_id_list.extend(target_id_list)

        logging.debug("All Target Id List: {}".format(all_target_id_list))
        return all_target_id_list

    ##
    # @brief        A Class Method to Get the Display Config and Port List Based on the No of Tiled Panel Plugged.
    # @param[in]     port_list: List[str]
    #                   List of port names for which display config has to be applied.
    # @return       config_data: ConfigData
    #                   Returns the Topology and Port List on Which the Config has to Applied.
    @staticmethod
    def get_config_to_apply(port_list: List[str]) -> ConfigData:
        if len(port_list) == 1:
            config_data = ConfigData(enum.SINGLE, [port_list[0]])
        elif len(port_list) == 2:
            config_data = ConfigData(enum.EXTENDED, [port_list[0], port_list[1]])
        elif len(port_list) == 3:
            config_data = ConfigData(enum.EXTENDED, [port_list[0], port_list[1], port_list[2]])
        else:
            config_data = None
            assert True, "[Planning Issue] - Invalid Command Line"

        return config_data

    ##
    # @brief        A Static method which parses the mode string and returns horizontal resolution, vertical
    #               resolution and refresh rate
    # @param[in]    mode: str
    #                   A string which contains mode information of the format hor_resXver_res\@rr
    # @return       hor_resolution, ver_resolution, refresh_rate: Tuple[int, int, int]
    #                   Returns Horizontal Resolution, Vertical Resolution and Refresh Rate
    @staticmethod
    def parse_native_mode(mode: DisplayTimings) -> Tuple[int, int, int]:
        if mode is None:
            return 0, 0, 0
        hor_resolution = mode.hActive
        ver_resolution = mode.vActive
        refresh_rate = mode.refreshRate

        logging.debug("HorRes: {}, VerRes: {}, RR: {}".format(hor_resolution, ver_resolution, refresh_rate))
        return hor_resolution, ver_resolution, refresh_rate

    ##
    # @brief        Method to Enable or Disable Os HDR
    # @param        port - Current Port on which display is Plugged
    # @param        to_be_enabled - Tells if HDR is to be enabled or disable
    # @return       status - True/False
    def enable_or_disable_os_hdr(self, port, to_be_enabled):
        os_hdr_verify = os_hdr_verification.OSHDRVerification()

        display_and_adapter_info = self.display_config.get_display_and_adapter_info_ex(port)
        hdr_error_code = configure_hdr(display_and_adapter_info, enable=to_be_enabled)

        if to_be_enabled:
            status = os_hdr_verify.is_error("OS_HDR", hdr_error_code, "ENABLE")
        else:
            status = os_hdr_verify.is_error("OS_HDR", hdr_error_code, "DISABLE")

        return status

    ##
    # @brief        Method to read timing information from Emulator after Plug/Unplug of the display
    # @param        emulator_port - Port of the emulator which is plugged
    # @param        is_plugged - Tells if display is plugged or not
    # @return       status - True/False
    def check_timing_info_from_emulator(self, emulator_port, is_plugged):
        status, msa_values = self.she_utility.read_MSA_parameters_from_emulator(emulator_port)

        if is_plugged:
            # Checking if MSA is non zero after plugging display
            if status is True and msa_values.X_value != 0 and msa_values.Y_value != 0 and msa_values.refresh_rate != 0:
                logging.info(f'PASS: Valid Timings found after Plugging the Display')
            else:
                status = False
                logging.error(f'FAIL: Invalid Timings found after Plugging the Display')

        else:
            # Checking if MSA is zero after unplugging display
            if status is False and (msa_values.X_value == 0 or msa_values.Y_value == 0 or msa_values.refresh_rate == 0):
                status = True
                logging.info(f'PASS: Timing Info is Zero after Unplugging the display')
            else:
                status = False
                logging.error(f'FAIL: Timing Info is non Zero after Unplugging the display')

        return status

    ##
    # @brief        Method to check if blankout is observed on the display using CRC from Emulator
    # @param        emulator_port - Port of the emulator which is plugged
    # @param        is_plugged - Tells if display is plugged or not
    # @return       status - True/False
    def check_blankout_using_crc_from_emulator(self, emulator_port, is_plugged):
        status, rgb_values = self.she_utility.read_CRC_values_from_emulator(emulator_port, 1)

        if not status:
            logging.info("CRC Read Failed from Emulator Port {}".format(emulator_port))
            return status

        rvalue, gvalue, bvalue = rgb_values[0][0], rgb_values[0][1], rgb_values[0][2]

        if is_plugged:
            # Checking if CRC is non zero after plugging display
            if rvalue != "0000" or gvalue != "0000" or bvalue != "0000":
                logging.info(f'RValue: {rvalue} GValue: {gvalue} BValue: {bvalue}')
                logging.info("PASS: CRC Found after Plugging the Display")

            elif rvalue == "0000" and gvalue == "0000" and bvalue == "0000":
                status = False
                logging.info(f'RValue: {rvalue} GValue: {gvalue} BValue: {bvalue}')
                logging.error("FAIL: Blankout Observed after Plugging the Display")

        else:
            # Checking if CRC is zero after unplugging display
            if rvalue == "0000" and gvalue == "0000" and bvalue == "0000":
                logging.info(f'RValue: {rvalue} GValue: {gvalue} BValue: {bvalue}')
                logging.info("PASS: CRC not found after Unplugging display")
            else:
                status = False
                logging.info(f'RValue: {rvalue} GValue: {gvalue} BValue: {bvalue}')
                logging.error("FAIL: Display is still active after Unplug call")

        return status


    ##
    # @brief        A class method which cleans up/resets the environment just as before running the test.
    # @return       None
    @classmethod
    def tearDownClass(cls) -> None:

        # Unplug MST Tiled Displays.
        if bool(cls.mst_port_panel_dict) is True:
            logging.debug("Unplugging MST Tiled Displays")
            for port, _ in cls.mst_port_panel_dict.items():
                is_success = cls.she_utility.unplug_mst_tiled_display('gfx_0', port)
                assert is_success, "Unplug of MST tiled display failed on Port={}".format(port)

        # Unplug SST Tiled Displays.
        if bool(cls.sst_port_panel_dict) is True:
            logging.debug("Unplugging SST Tiled Displays")
            for port_pair, _ in cls.sst_port_panel_dict.items():
                m_port, s_port = port_pair
                is_success = cls.she_utility.unplug_sst_tiled_display('gfx_0', m_port, s_port)
                assert is_success, "Unplug of SST tiled display failed on m_port={}, s_port={}".format(m_port, s_port)

        # Unplug Displays connected to TBT Hub
        if bool(cls.tbt_hub_port_display_info_dict) is True:
            logging.debug("Unplugging Displays Connected to TBT hub")
            for tbt_hub_port, hub_port_display_info_list in cls.tbt_hub_port_display_info_dict.items():
                for hub_display_info in hub_port_display_info_list:
                    is_success = cls.she_utility.unplug_display_to_tbt_hub('gfx_0', tbt_hub_port, hub_display_info)
                    assert is_success, "Unplug of display failed on Port={}".format(tbt_hub_port)
