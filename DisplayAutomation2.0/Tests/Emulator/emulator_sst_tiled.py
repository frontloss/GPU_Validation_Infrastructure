#######################################################################################################################
# @file         emulator_sst_tiled.py
# @section      Tests
# @brief        Test cases to plug and verify one input sst and two input sst tiled displays.
# @author       Praburaj Krishnan
#######################################################################################################################
import logging
from typing import List
from unittest import TextTestRunner

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Emulator.emulator_test_base import EmulatorTestBase
from Tests.PowerCons.Modules import common


##
# @brief        This class contains a test that plugs SST tiled display and verifies tiled mode if both master and slave
#               port are plugged or verifies non-tiled mode if only master port is plugged
class SingleStreamTransportTiled(EmulatorTestBase):
    sst_tiled_master_port_list: List[str] = []

    ##
    # @brief        A private class method that is used to get the master port of the SST Tiled displays by using
    #               dictionary constructed using the command line.
    # @return       sst_tiled_master_port_list: List[str]
    #                   Returns master port list of the tiled displays.
    @classmethod
    def _get_sst_tiled_master_port_list(cls) -> List[str]:
        sst_tiled_master_port_list: List[str] = []

        if bool(cls.sst_port_panel_dict) is True:
            for key_tuple in cls.sst_port_panel_dict.keys():
                sst_tiled_master_port_list.append(key_tuple[0])

        return sst_tiled_master_port_list

    ##
    # @brief        Handles One Input SST Tiled as well as Two Input SST Tiled display.
    # @return       None
    def t_0_sst_tiled(self) -> None:
        cls = SingleStreamTransportTiled

        # Parse the command and get the tiled panel info and the master port associated with each of the tiled display.
        cls.sst_port_panel_dict = cls.emulator_command_parser.get_sst_port_panel_dict()
        cls.sst_tiled_master_port_list = cls._get_sst_tiled_master_port_list()

        enumerated_displays = cls.display_config.get_enumerated_display_info()
        logging.debug("Enumerated Displays Before Plug: {}".format(enumerated_displays.to_string()))

        # Iterate through each of the Tiled display info constructed from the command line.
        for port_pair, tiled_panel_info in cls.sst_port_panel_dict.items():
            m_port, s_port = port_pair

            is_success = cls.she_utility.plug_sst_tiled_display('gfx_0', m_port, s_port, tiled_panel_info)
            self.assertTrue(is_success, f"Plug of SST Tiled display failed on m_port={m_port}, s_port={s_port}")
            logging.info(f"Plug of SST tiled display successful on m_port={m_port}, s_port={s_port}")

            enumerated_displays = cls.display_config.get_enumerated_display_info()
            logging.debug("Enumerated Displays After Plug: {}".format(enumerated_displays.to_string()))

            is_success = cls.apply_config([m_port])
            self.assertTrue(is_success, "[Driver Issue] - Applying Display Config Failed")
            common.print_current_topology()

            # Get the Tiled Target Id list by using the Master port of each of the tiled displays.
            port_target_id_dict = cls.get_port_target_id_dict(cls.sst_tiled_master_port_list)
            tiled_target_id_list = cls.get_target_id_list_from_dict(port_target_id_dict)

            # If slave port is not none, it means plugged display is operating in tiled mode and hence verify tiled mode
            # else verify non tiled mode.
            if s_port is not None:
                is_success = cls.verify_tiled_mode(tiled_target_id_list)
                self.assertTrue(is_success, "[Driver Issue] - Tiled Mode Verification Failed")
                logging.info(f"Successfully Verified Tiled mode for display connected to ={m_port}")
            else:
                is_success = cls.verify_non_tiled_mode(tiled_target_id_list)
                self.assertTrue(is_success, "[Driver Issue] - Non Tiled Mode Verification Failed")
                logging.info(f"Successfully Verified Non Tiled mode for display connected to ={m_port}")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(SingleStreamTransportTiled))
    TestEnvironment.cleanup(test_result)
