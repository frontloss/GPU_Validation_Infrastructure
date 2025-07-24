#####################################################################################################################################
# \file
# \ref display_config_ult.py
# \verbatim
# Sample code for Get/Set Display Configuration, Get All Supported Modes,
# Get Current Mode, Set Display Mode using Display Config API
# \endverbatim
# \author       Amit Sau, Bharath
###################################################################################################################################

import unittest

from Libs.Core.test_env.test_environment import *
from Tests.ULT.display_sink_simulation_ult import get_dp_ports
from Libs.Core.gta import gta_state_manager
from Libs.Core import test_header


class display_config_ult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = DisplayConfiguration()
        plug_dp_port()
        cls.enumerated_display = cls.config.get_enumerated_display_info()

    def setUp(self):
        logging.info("ULT Start")

    def test_0_1_get_dll_version(self):
        logging.info("Test started")
        dll_version = self.config.get_display_config_interface_version()
        self.assertEqual(dll_version, 16, "Display config DLL version mismatch")
        logging.info("Test passed")

    def test_0_2_get_all_display_configuration(self):
        logging.info("Test started")
        all_config = self.config.get_all_display_configuration()
        # Assuming EDP is always connected
        self.assertGreater(all_config.numberOfDisplays, 0, "No display connected")
        self.assertEqual(all_config.status, enum.DISPLAY_CONFIG_SUCCESS, "Getting display configuration failed")

        # print all the received display configurations
        print_display_config(all_config)
        logging.info("Test passed")

    def test_0_3_set_display_configuration_single(self):
        logging.info("Test started")
        current_config = self.config.get_all_display_configuration()
        result = set_topology_and_verify(enum.SINGLE, current_config, self.enumerated_display)
        self.assertTrue(result, "Setting SINGLE display configuration failed")
        logging.info("Test passed")

    def test_0_4_set_display_configuration_clone(self):
        logging.info("Test started")
        current_config = self.config.get_all_display_configuration()
        result = set_topology_and_verify(enum.CLONE, current_config, self.enumerated_display)
        self.assertTrue(result, "Setting CLONE display configuration failed")
        logging.info("PASS: Successfully applied CLONE display configuration")

    def test_0_5_set_display_configuration_extended(self):
        logging.info("Test started")
        current_config = self.config.get_all_display_configuration()
        result = set_topology_and_verify(enum.EXTENDED, current_config, self.enumerated_display)
        self.assertTrue(result, "Setting EXTENDED display configuration failed")
        logging.info("PASS: Successfully applied EXTENDED display configuration")

    def tearDown(self):
        logging.info("ULT Complete")

    @classmethod
    def tearDownClass(self):
        unplug_dp_port()


def set_topology_and_verify(topology, current_config, enumerated_display):
    config = DisplayConfiguration()
    new_config = DisplayConfig()
    new_path_info = DisplayPathInfo()

    logging.info("Before applying configuration : %s", current_config.to_string(enumerated_display))
    if topology == enum.SINGLE:
        current_config.numberOfDisplays = 1

    # updating to new topology
    new_config.topology = topology
    new_config.numberOfDisplays = current_config.numberOfDisplays

    for index in range(0, current_config.numberOfDisplays):
        new_path_info.pathIndex = index
        new_path_info.targetId = current_config.displayPathInfo[index].targetId
        new_config.displayPathInfo[index] = new_path_info
        new_config.displayPathInfo[index].displayAndAdapterInfo = enumerated_display.ConnectedDisplays[
            index].DisplayAndAdapterInfo

    logging.info("Applying new configuration : %s", new_config.to_string(enumerated_display))
    config.set_display_configuration(new_config)

    get_config = config.get_current_display_configuration()
    logging.info("After applying configuration : %s", get_config.to_string(enumerated_display))

    return get_config.equals(new_config)


def plug_dp_port():
    edid = 'DP_3011.EDID'
    dpcd = 'DP_3011_DPCD.txt'
    dp_ports = get_dp_ports()
    if dp_ports is not None:
        plug(dp_ports[0], edid, dpcd, False)


def unplug_dp_port():
    dp_ports = get_dp_ports()
    if dp_ports is not None:
        unplug(dp_ports[0], False)


##
# Sample code to get display configuration which includes both active and inactive displays.
def print_display_config(all_config):
    logging.info("******************* Display Configurations *******************")
    logging.info("Number of displays: %d", all_config.numberOfDisplays)
    logging.info("Topology Type: %s", DisplayConfigTopology(all_config.topology))
    logging.info("")
    for display_index in range(0, all_config.numberOfDisplays):
        logging.info("Display %d :", display_index)
        logging.info("Target ID: %d", all_config.displayPathInfo[display_index].targetId)
        logging.info("Source ID: %d", all_config.displayPathInfo[display_index].sourceId)
        logging.info("IsActive: %d", all_config.displayPathInfo[display_index].isActive)
        logging.info("Monitor Friendly Device Name: %s",
                     all_config.displayPathInfo[display_index].displayAndAdapterInfo.MonitorFriendlyDeviceName)
        logging.info("")
    logging.info("Status: %s", DisplayConfigErrorCode(all_config.status))
    logging.info("")
    logging.info("*************************************************")


if __name__ == '__main__':
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_header.cleanup(outcome.result)
    gta_state_manager.update_test_result(outcome.result, status)
    display_logger._cleanup()

