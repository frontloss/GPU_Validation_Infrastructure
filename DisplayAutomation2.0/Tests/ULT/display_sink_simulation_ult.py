###############################################################################
# \ref display_sink_simulation_ult.py
# \brief This script try all possible Plug and UnPlug on the target machine
# Commandline : 1.) display_sink_simulation_ult.py - Run all test
#               2.) display_sink_simulation_ult.py display_sink_simulation.test_0_1_driver_restart - Run targeted test
# \author   Beeresh
###############################################################################

'''
TODO: Add testcase to plug display together
'''

import os, sys, time
import collections
import logging
import win32api
import unittest

import win32con

from Libs.Core.cmd_parser import *
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import *
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env.test_environment import *
from Libs.Core import display_utility, display_essential
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.sw_sim.gfxvalsim import *
from Libs.Core.display_config.display_config import *
from Libs.Core.gta import gta_state_manager
from Libs.Core.test_env import test_environment

from Tests.ULT.system_utility_ult import is_postSi

GFXSIM_DISPLAY_TOPOLOGIES_MATCHING = 0
GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT = 4

'''
WARM_UP required only for GTA environment. 
 Due to multiple power cycles, heart beat of DUT has not reached runner within expected time frame and GTA Runner 
 interpret DUT unreacheable and aborts JOB. 
'''
POWER_CYCLE_WARM_UP_TIME = 120

'''
Duration in seconds DUT will be in specified power state
'''
POWER_CYCLE_DURATION = 10


def do_nothing():
    logging.info("Sleep for 5 seconds")
    time.sleep(5)


def goto_powerstate_s3():
    disp_power = DisplayPower()
    ret = disp_power.invoke_power_event(PowerEvent.S3, POWER_CYCLE_DURATION)
    time.sleep(POWER_CYCLE_WARM_UP_TIME)
    return ret


def goto_powerstate_s4():
    disp_power = DisplayPower()
    ret = disp_power.invoke_power_event(PowerEvent.S4, POWER_CYCLE_DURATION)
    time.sleep(POWER_CYCLE_WARM_UP_TIME)
    return ret


def monitor_turnoff():
    disp_power = DisplayPower()
    ret = disp_power.invoke_monitor_turnoff(MonitorPower.OFF_ON, POWER_CYCLE_DURATION)
    if ret:
        win32api.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        logging.info("Wake-up machine using key press event successful !!")
    time.sleep(POWER_CYCLE_WARM_UP_TIME)
    return ret


def get_current_displays():
    config = DisplayConfiguration()
    enumerated_displays = config.get_enumerated_display_info()
    return enumerated_displays


def get_supported_external_ports():
    supported_ports = get_supported_ports()
    external_ports = [port_name for port_name in supported_ports if '_A' not in port_name.upper()]
    return external_ports


def get_hdmi_ports():
    ports = get_supported_external_ports()
    hdmi_ports = [port for port in ports if "HDMI_" in port.upper()]
    return hdmi_ports


def get_dp_ports():
    ports = get_supported_external_ports()
    dp_ports = [port for port in ports if "DP_" in port.upper()]
    return dp_ports


def get_external_free_ports():
    free_ports = display_utility.get_free_ports()
    external_ports = [port_name for port_name in free_ports if '_A' not in port_name.upper()]
    return external_ports


def get_port_targetid_mapping(reverse: bool, gfx_index: str = 'gfx_0') -> dict:
    enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
    target_id_mapping = dict()

    for display_index in range(enumerated_displays.Count):
        display = enumerated_displays.ConnectedDisplays[display_index]
        if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
            if reverse:
                target_id_mapping[int(display.TargetID)] = CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name
            else:
                target_id_mapping[CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name] = int(display.TargetID)

    return target_id_mapping


def get_modes(port_name):
    port_and_targetid = get_port_targetid_mapping(reverse=False)
    port_target_id = port_and_targetid[port_name]
    target_list = [port_target_id]
    cfg = DisplayConfiguration()
    port_and_targetid = get_port_targetid_mapping(reverse=True)
    target_list = port_and_targetid.keys()
    modes = cfg.get_all_supported_modes(target_list)
    port_modes = modes[port_target_id]
    return port_modes


def flush_log():
    [h_weak_ref().flush() for h_weak_ref in logging._handlerList]


def port_name_weight(port_list, new_item):
    update_set = list(port_list)
    update_set.append(new_item)
    ports_suffix = [port[-1:] for port in update_set]
    duplicate_ports_suffix = [item for item, count in collections.Counter(ports_suffix).items() if count > 1]
    return len(port_list) + len(duplicate_ports_suffix)


def find_partition(port_list):
    external_ports = [port_name for port_name in port_list if '_A' not in port_name.upper()]

    "returns: An attempt at a partition of `int_list` into two sets of equal sum"
    A = set()
    B = set()
    for port in sorted(external_ports):
        if port_name_weight(A, port) < port_name_weight(B, port):
            A.add(port)
        else:
            B.add(port)
    return (A, B)


def verify_tiled_status():
    disp_config = DisplayConfiguration()
    display_port = DisplayPort()

    # get the current display config from DisplayConfig
    config = disp_config.get_all_display_configuration()
    for index in range(config.numberOfDisplays):
        target_id = config.displayPathInfo[index].targetId
        tile_info = display_port.get_tiled_display_information(target_id)

        # check for tiled status
        if tile_info.TiledStatus:
            logging.info("Display is in tiled mode and Tiled target ID : %s", target_id)
            return
        else:
            continue
    logging.error("No tiled display found")


# Generate possible permutation of display config using display list
def get_possible_plug_unplug(display_list, combination=False):
    MAX_LEN = 3
    set_len = MAX_LEN

    def duplicate_port(display_list):
        suffix = []
        for display in display_list:
            display_suffix = display[-1:]

            if display_suffix in suffix:
                del suffix
                return False

            suffix.append(display_suffix)
        del suffix
        return True

    display_permute_list = []
    for i in range(1, set_len):
        if combination:
            permute_list = (itertools.combinations(display_list, i))
        else:
            permute_list = (itertools.permutations(display_list, i))

        for new_config in permute_list:
            display_permute_list.append(list(new_config))

    output_list = []
    for input_list in display_permute_list:
        if duplicate_port(input_list):
            output_list.append(input_list)

    return output_list


##
# Stress test case to verify DFT with CRC and Underrun check
class display_sink_simulation_ult(unittest.TestCase):
    log_handle = None

    DP_PANEL = {'EDID': 'DP_3011.EDID', 'DPCD': 'DP_3011_dpcd.txt'}
    HDMI_PANEL = {'EDID': 'HDMI_DELL.EDID'}
    HDMI_2_0_PANEL = {'EDID': 'HDMI_EDID_NON_PRMODES_SET2_SCDC.bin'}
    PLUG_UNPLUG_TEST = {'action': 'PLUG', 'port': 'DP_A'}
    DP_MST_PANEL = {'XML': 'DPMST_1Branch_1MSTDisplay.xml'}
    DFT_TEST_PARAMETERS = {}

    disp_port = DisplayPort()
    underrunstatus = UnderRunStatus()
    under_run_tolerance = True

    ##
    # Check Underrun
    def verify_underrun(self):
        result = self.underrunstatus.verify_underrun()

        logging.info("Under run verification status %s" % result)
        if not self.under_run_tolerance:
            self.assertEquals(result, False, "Aborting the test as underrun is observed.")

    ##
    #  Verify corruption using CRC mechanism
    def verify_corruption(self):
        # pattern_match = ComputeCRC(stimuli="DIRECTXAPP")
        # self.assertTrue(pattern_match, "Aborting test due to failure in verification step")
        pass

    ##
    # @brief Verifying whether particular display is attached or not using enumerated display.
    # @param[in] - port of type CONNECTOR_PORT_TYPE
    # @param[in] - is_plug of type Bool. True - if plugging the display, False - if unplugging the display
    # @return - None
    def verify_display_topology(self, port, action, negative=False):
        ##
        # Verifying using enumerated display
        enumerated_displays = get_current_displays()
        is_disp_attached = is_display_attached(enumerated_displays, port)

        if action == "PLUG":
            expected_state = True
        else:
            expected_state = False

        if negative:
            expected_state = not expected_state

        logging.info("Current Display Topology \n %s", enumerated_displays.to_string())
        self.assertEquals(is_disp_attached, expected_state, "Verification of %s port %s failed" % (action, port))
        logging.info("Verification for %s successful for action: %s" % (port, action))

    def plug_device(self, port, is_low_power):
        self.PLUG_UNPLUG_TEST['action'] = "PLUG"
        self.PLUG_UNPLUG_TEST['port'] = port

        if "DP" in port.upper():
            edid_file = self.DP_PANEL['EDID']
            dpcd_file = self.DP_PANEL['DPCD']
        elif "HDMI" in port.upper():
            edid_file = self.HDMI_PANEL['EDID']
            dpcd_file = None
        else:
            raise Exception("Edid details not found for %s" % (port))

        # Plugging the display
        logging.info("plug %s with EDID:%s and DPCD:%s with Low power state:%s" %
                     (port, edid_file, dpcd_file, is_low_power))
        result = plug(port, edid_file, dpcd_file, is_low_power)
        time.sleep(3)
        self.assertEquals(result, True, "plug API failed for %s" % (port))

    def plug_and_verify_hdmi_2_0(self, native_hdmi_port):
        edid_file = self.HDMI_2_0_PANEL['EDID']
        dpcd_file = None
        result = plug(native_hdmi_port, edid_file, dpcd_file, False)
        self.assertEquals(result, True, "plug API failed for %s" % native_hdmi_port)

        do_nothing()
        self.verify_display_topology(native_hdmi_port, 'PLUG')

        hdmi_modes = get_modes(native_hdmi_port)
        found = False
        for hdmi_mode in hdmi_modes:
            logging.info(hdmi_mode.HzRes, hdmi_mode.VtRes, hdmi_mode.refreshRate, hdmi_mode.scaling)
            if hdmi_mode.HzRes == 3840 and hdmi_mode.VtRes == 2160 and hdmi_mode.refreshRate == 60:
                found = True
                break
        unplug(native_hdmi_port)
        # self.assertTrue(found,"4K mode not found")

    ##
    #  verify the Plug/Unplug API's's ofr MST Topology
    #
    def verify_mst(self, port, low_power_state, action="PLUG"):
        self.verify_display_topology(port, action, negative=low_power_state)

        if action == "PLUG":
            dpcd_flag, dpcd_reg_val = self.disp_port.read_dpcd(port, True, 1, 0x0, None)
            logging.info("DPCD flag = %s dpcd_reg_val = %s" % (dpcd_flag, dpcd_reg_val))
            if dpcd_flag and dpcd_reg_val[0] == 0x12:
                logging.info("The Connected Display is a MST Display: Version: 0x%x", dpcd_reg_val[0])
            else:
                self.fail("The Connected Display is not a MST Display")

        '''
        ************************************** NOTE **********************************
        **This below verification should be enabled once CUI COM supported in Yangra*
        ************************************** NOTE **********************************
        
        if action not in ['PLUG', 'UNPLUG']:
            logging.error("Invalid plug action for MST display. Exiting .....")
            self.fail()
        retStatus = self.disp_port.verify_topology(port)
        if action is 'PLUG' and retStatus == GFXSIM_DISPLAY_TOPOLOGIES_MATCHING:
           logging.info("MST Topology Verification Success, Applied and Expected topologies are matching")
        elif action is 'UNPLUG' and retStatus == GFXSIM_DISPLAY_TOPOLOGY_NOT_PRESENT:
            logging.info("MST Topology Verification Success: HPD(UNPLUG) event")
        else:
            try:
                logging.error("MST Topology Verification Failed.. Status Code:%s" % (TOPOLOGY_STATUS_CODE(retStatus).name))
                self.fail()
            except ValueError as Error:
                logging.error("MST Topology Verification Failed.. No Matching Status Code Found...%s" % (Error))
                self.fail()
        '''

    ##
    #  Plug/Unlug MST for normal/power events
    # verify the Plug/Unplug API's's
    def plug_unplug_mst(self, power_state_func, low_power_state):
        xml_file = os.path.join(TestContext.panel_input_data(), "DP_MST_TILE", self.DP_MST_PANEL['XML'])
        ports = get_external_free_ports()
        free_dp_ports = [port for port in ports if "DP_" in port.upper()]

        logging.info("free port_vector %s" % ports)
        logging.info("free DP port_vector %s" % free_dp_ports)

        if len(free_dp_ports) < 1:
            self.fail("No free DP Ports are available")

        for port in free_dp_ports:
            # Plugging the display
            logging.info("plug %s with XML:%s with Low power state:%s" %
                         (port, self.DP_MST_PANEL['XML'], low_power_state))
            self.disp_port.setdp(port, 'MST', xml_file, low_power_state)

            power_state_func()

            self.verify_mst(port, low_power_state)

            logging.info("Unplug %s " % (port))
            self.disp_port.set_hpd(port, False)

            power_state_func()

            self.verify_mst(port, low_power_state, 'UNPLUG')

    def restart_gfxvalsim_driver(self):
        # Close the handle of valsim driver
        gfxvalsim_closehandle()
        result = self.enable_disable_gfxvalsim_driver(False)
        self.assertEqual(result, True, "ValSimDriver disable failed")
        logging.info("ValSimDriver disable Success")
        result = self.enable_disable_gfxvalsim_driver(True)
        self.assertEqual(result, True, "ValSimDriver enable failed")
        logging.info("ValSimDriver enable Success")
        # restart the Gfx driver to re-initiate the
        # communication between Gfx driver and valsim driver
        # refer VSDI-4098 for more details
        result, reboot_required = display_essential.restart_gfx_driver()
        self.assertEqual(result, True, "GfxDriver restart failed")
        logging.info("GfxDriver restart Success")

        gfxvalsim_initializehandle()
        gfx_adapter_details = TestContext.get_gfx_adapter_details()
        for adapter_str in gfx_adapter_details:
            result = gfxvalsim_initallports(gfx_adapter_details[adapter_str])
            self.assertEqual(result, False, "Init AllPorts failed")

    def check_cap(self, cap_name):
        if not self.__class__.caps[cap_name]:
            self.fail("%s capability not support on this target" % cap_name)

    ##
    # @brief API to disable and enable the valsim driver
    #
    # Disable and enable the display driver
    #
    # @param[in] none
    # @return bool: True if successful, otherwise False
    def enable_disable_gfxvalsim_driver(self, enable):
        exe_path = os.path.join(TestContext.bin_store(), valsim_devcon_exe)
        if enable:
            cmd_opt1 = "enable"
        else:
            cmd_opt1 = "disable"
        cmd_opt2 = os.path.join(TestContext.bin_store(), valsim_inf_path)
        cmd_opt3 = "root\\umbus"
        disable_status = subprocess.call([exe_path, cmd_opt1, cmd_opt2, cmd_opt3])
        time.sleep(10)
        return disable_status == 0

    @classmethod
    def setUpClass(cls):
        cls.caps = dict()
        if is_postSi():
            cls.caps["S3"] = goto_powerstate_s3()
            cls.caps["S4"] = goto_powerstate_s4()
            cls.caps["MONITOR_OFF"] = monitor_turnoff()
        else:
            cls.caps["S3"] = False
            cls.caps["S4"] = False
            cls.caps["MONITOR_OFF"] = False

    def setUp(self):
        log_file = os.path.basename(__file__)
        self.log_handle = display_logger.add_file_handler(log_file)
        logging.info(display_logger.formatted_line_separator())
        test_preamble = ("START TEST CASE %s" % (self._testMethodName)).center(78, ' ')
        logging.info(display_logger.format_line(test_preamble))

        target_type = env_settings.get('GENERAL', 'silicon_type')
        if target_type != "SOC":
            test_name = self._testMethodName.lower()
            if ("s3" in test_name) or ("s4" in test_name):
                raise unittest.SkipTest("Power related test cases skipped in presi environment")
            elif "mst" in test_name:
                raise unittest.SkipTest("MST test cases skipped in presi environment")

    def plug_unplug_sanity(self, operation_between_plug_and_unplug, low_power_state):
        ports = get_supported_external_ports()
        possible_vectors = find_partition(ports)
        if possible_vectors[0] > possible_vectors[1]:
            port_vector = possible_vectors[0]
        else:
            port_vector = possible_vectors[1]

        logging.info("Plug/UnPlug sanity with ports %s in sequence of %s" % (ports, port_vector))
        for port in port_vector:
            if "DP" in port.upper():
                edid_file = self.DP_PANEL['EDID']
                dpcd_file = self.DP_PANEL['DPCD']
            elif "HDMI" in port.upper():
                edid_file = self.HDMI_PANEL['EDID']
                dpcd_file = None
            else:
                raise Exception("Edid details not found for %s" % port)

            logging.info(
                "Requesting plug to %s with EDID = %s and DPCD = %s in low_power_state = %s" % (
                    port, edid_file, dpcd_file, low_power_state))
            plug(port, edid_file, dpcd_file, low_power_state)

            if low_power_state:
                sysutil_handle = SystemUtility()
                if sysutil_handle.is_ddrw():
                    self.verify_display_topology(port, 'PLUG', negative=True)
                else:
                    '''
                        Re-entrant issue observed with DFTPanelSimulator, hence punting negative verification
                        1. Plug using DFT Panel Simulator
                        2. Call DFT Panel simulator to list free port
                        Effect: The previous plug request will be lost, this get exposed only during low power state
                    '''
                    pass

            operation_between_plug_and_unplug()
            self.verify_display_topology(port, 'PLUG', negative=False)

            logging.info("Requesting Unplug for %s with low_power_state = %s" % (port, low_power_state))
            unplug(port, low_power_state)

            if low_power_state:
                self.verify_display_topology(port, 'UNPLUG', negative=True)

            operation_between_plug_and_unplug()
            self.verify_display_topology(port, 'UNPLUG', negative=False)

    ##
    # @brief tiled_display_helper() plugs/unplugs the tiled display.
    # @param[in] - action for display i.e. plug/unplug or master_plug etc.
    # @param[in] - low_power state
    # @return - None
    def plug_unplug_tiled_display_sanity(self, power_state_func, low_power_state):
        master_tile_edid = "DELL_U2715_M.EDID"
        master_tile_dpcd = "DELL_U2715_DPCD.bin"
        slave_tile_edid = "DELL_U2715_S.EDID"
        slave_tile_dpcd = "DELL_U2715_DPCD.bin"

        ports = get_external_free_ports()
        free_dp_ports = [port for port in ports if "DP_" in port.upper()]

        if len(free_dp_ports) < 2:
            self.fail("Tile display requires atleast 2 DP port free but found %s!!" % (str(free_dp_ports)))

        master_dp_port = free_dp_ports[0]
        slave_dp_port = free_dp_ports[1]

        ''' ********* PLUG *********'''
        logging.info("Requesting plug %s EDID = %s and DPCD = %s  low_power_state = %s" % (
            master_dp_port, master_tile_edid, master_tile_dpcd, low_power_state))
        ##
        #  call plug_unplug_tiled_display() from DisplayPort DLL to plug the tiled display
        result = self.disp_port.plug_unplug_tiled_display(True, True, master_dp_port,
                                                          slave_dp_port, master_tile_edid,
                                                          slave_tile_edid, slave_tile_dpcd, low_power_state)
        # Verify topology after plug call
        if low_power_state:
            self.verify_display_topology(master_dp_port, 'PLUG', negative=True)
        else:
            self.verify_display_topology(master_dp_port, 'PLUG', negative=False)

        # Enter low power state
        power_state_func()

        # Verify topology after resuming from low power state
        self.verify_display_topology(master_dp_port, 'PLUG', negative=False)

        # Confirming if the plugged display is in tiled mode
        verify_tiled_status()

        ''' ********* UNPLUG *********'''

        logging.info(
            "Requesting unplug of Tile display at %s with low_power_state = %s" % (master_dp_port, low_power_state))
        result = self.disp_port.plug_unplug_tiled_display(False, False, master_dp_port,
                                                          slave_dp_port, master_tile_edid,
                                                          slave_tile_edid, master_tile_dpcd, low_power_state)
        # Verify topology after unplug call
        if low_power_state:
            self.verify_display_topology(master_dp_port, 'UNPLUG', negative=True)
        else:
            self.verify_display_topology(master_dp_port, 'UNPLUG', negative=False)
        # Enter low power state
        power_state_func()

        # Verify topology after resuming from low power state
        self.verify_display_topology(master_dp_port, 'UNPLUG', negative=False)

    '''
    ******************** TESTS *************************
    '''

    def test_0_1_available_ports_check(self):
        logging.info(display_logger.formatted_line_separator())

        ports = get_supported_external_ports()
        if len(ports) == 0:
            self.fail("FAIL: Insufficient supported port list")
        logging.info("PASS: %s external display port available" % ports)
        flush_log()

    def test_0_2_plug_unplug_sanity_with_do_nothing(self):
        self.plug_unplug_sanity(do_nothing, False)
        logging.info("PASS:Sanity check without any power events")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_3_plug_unplug_sanity_with_s3_negative(self):
        self.check_cap("S3")
        self.plug_unplug_sanity(goto_powerstate_s3, False)
        logging.info("PASS: Plug and Unplug performed and state persisted with S3 transition")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_4_plug_unplug_sanity_with_s4_negative(self):
        self.check_cap("S4")
        self.plug_unplug_sanity(goto_powerstate_s4, False)
        logging.info("PASS: Plug and Unplug performed and state persisted with S4 transition")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_5_plug_unplug_sanity_with_monitor_turn_off(self):
        self.check_cap("MONITOR_OFF")
        self.plug_unplug_sanity(monitor_turnoff, False)
        logging.info("PASS: Plug and Unplug performed and state persisted with Monitor Turn off event")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_6_plug_unplug_sanity_during_s3(self):
        self.check_cap("S3")
        self.plug_unplug_sanity(goto_powerstate_s3, True)
        logging.info("PASS: Plug and Unplug performed successfully during S3")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_7_plug_unplug_sanity_during_s4(self):
        self.check_cap("S4")
        self.plug_unplug_sanity(goto_powerstate_s4, True)
        logging.info("PASS: Plug and Unplug performed successfully during S4")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_8_HDMI_2_0_with_native_port(self):
        hdmi_ports = get_hdmi_ports()
        ports = get_supported_external_ports()

        suffix_list = [port[-1:] for port in ports]
        self.assertGreater(len(hdmi_ports), 0, "HDMI ports not available")
        compatible_ddi = [item for item, count in collections.Counter(suffix_list).items() if count > 1]

        native_ports = [hdmi_port for hdmi_port in hdmi_ports if hdmi_port[-1:] not in compatible_ddi]
        if len(native_ports) != 0:
            self.assertGreater(len(native_ports), 0, "Native HDMI ports not available")
            for native_hdmi_port in native_ports:
                self.plug_and_verify_hdmi_2_0(native_hdmi_port)
            logging.info("PASS: HDMI 2.0 simulation through native HDMI port")
        else:
            logging.info("Skipping Test, since Native HDMI ports are Not Available")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_9_HDMI_2_0_with_dongle_path(self):
        hdmi_ports = get_hdmi_ports()
        ports = get_supported_external_ports()

        suffix_list = [port[-1:] for port in ports]
        self.assertGreater(len(hdmi_ports), 0, "HDMI ports not available")
        compatible_ddi = [item for item, count in collections.Counter(suffix_list).items() if count > 1]
        dongle_ports = [hdmi_port for hdmi_port in hdmi_ports if hdmi_port[-1:] in compatible_ddi]
        self.assertGreater(len(dongle_ports), 0, "Dongle HDMI ports not available")

        compatible_ddi = [item for item, count in collections.Counter(suffix_list).items() if count > 1]
        native_ports = [hdmi_port for hdmi_port in hdmi_ports if hdmi_port[-1:] not in compatible_ddi]
        if len(native_ports) != 0:
            for dongle_hdmi_port in dongle_ports:
                self.plug_and_verify_hdmi_2_0(dongle_hdmi_port)

            logging.info("PASS: HDMI 2.0 simulation through DP port")
        else:
            logging.info("Skipping Test, since Native HDMI ports are Not Available")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_0_DP_Tiled_Plug_UnPlug(self):
        self.plug_unplug_tiled_display_sanity(do_nothing, False)
        logging.info("PASS: Tiled DP plug and unplug peformed successfully")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_1_DP_Tiled_Plug_UnPlug_with_S3_negative(self):
        self.check_cap("S3")
        self.plug_unplug_tiled_display_sanity(goto_powerstate_s3, False)
        logging.info("PASS: Tiled DP plug and unplug and persisted with S3 transition")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_2_DP_Tiled_Plug_UnPlug_with_S4_negative(self):
        self.check_cap("S4")
        self.plug_unplug_tiled_display_sanity(goto_powerstate_s4, False)
        logging.info("PASS: Tiled DP plug and unplug and persisted with S3 transition")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_3_DP_Tiled_Plug_UnPlug_with_S3(self):
        self.check_cap("S3")
        self.plug_unplug_tiled_display_sanity(goto_powerstate_s3, True)
        logging.info("PASS: Tiled DP plug and unplug during S3 ")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_4_DP_Tiled_Plug_UnPlug_with_S4(self):
        self.check_cap("S4")
        self.plug_unplug_tiled_display_sanity(goto_powerstate_s4, True)
        logging.info("PASS: Tiled DP plug and unplug during S4")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_5_DP_MST_Plug_UnPlug(self):
        # Initialize GfxValSim
        obj = GfxValSim()
        self.plug_unplug_mst(do_nothing, False)
        logging.info("PASS: DP MST plug and unplug done successfully")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_6_DP_MST_Plug_UnPlug_with_S3_negative(self):
        obj = GfxValSim()
        self.plug_unplug_mst(goto_powerstate_s3, False)
        logging.info("PASS: DP MST plug and unplug done with S3 successfully")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_7_DP_MST_Plug_UnPlug_with_S4_negative(self):
        obj = GfxValSim()
        self.plug_unplug_mst(goto_powerstate_s4, False)
        logging.info("PASS: DP MST plug and unplug done with S4 successfully")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_8_DP_MST_Plug_UnPlug_with_S3(self):
        obj = GfxValSim()
        self.check_cap("S3")
        self.plug_unplug_mst(goto_powerstate_s3, False)
        logging.info("PASS: DP MST plug and unplug and persisted with S3 transition")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_1_9_DP_MST_Plug_UnPlug_with_S4(self):
        obj = GfxValSim()
        self.check_cap("S4")
        self.plug_unplug_mst(goto_powerstate_s4, False)
        logging.info("PASS: DP MST plug and unplug and persisted with S4 transition")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_2_0_ValSim_driver_disable_safely(self):
        ret = display_essential.disable_driver()
        self.assertTrue(ret, "Failed to disable Graphics driver")

        ret = self.enable_disable_gfxvalsim_driver(False)
        self.assertTrue(ret, "Failed to disable GfxValSim driver")

        ret = display_essential.enable_driver()
        self.assertTrue(ret, "Failed to enable Graphics driver")
        logging.info("PASS: GfxValSim driver disable was successfull during Gfx driver disabled")

        ret = display_essential.disable_driver()
        self.assertTrue(ret, "Failed to disable Graphics driver")
        ret = self.enable_disable_gfxvalsim_driver(True)
        self.assertTrue(ret, "Failed to enable GfxValSim driver")
        ret = display_essential.enable_driver()
        self.assertTrue(ret, "Failed to enable Graphics driver")
        flush_log()

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def todo_2_1_dft_plug_unplug_stress(self):
        self.DFT_TEST_PARAMETERS['lower_power_state'] = [False, True]
        self.DFT_TEST_PARAMETERS['display_configs'] = ['enum.SINGLE', 'enum.CLONE', 'enum.EXTENDED']
        self.DFT_TEST_PARAMETERS['power_states'] = ['S0', 'S3']

        # if 'CHECK_UNDERRUN' in self.cmd_line_param.keys() and self.cmd_line_param['CHECK_UNDERRUN'] != 'NONE':
        #    self.under_run_tolerance = False

        low_power_vector = self.DFT_TEST_PARAMETERS["low_power_state"]
        config_vector = self.DFT_TEST_PARAMETERS['display_configs']
        power_state_vector = self.DFT_TEST_PARAMETERS['power_states']
        port_vector = get_possible_plug_unplug(get_external_free_ports(), True)

        unfiltered_test_variations = list(
            itertools.product(port_vector, low_power_vector, config_vector, power_state_vector))
        filtered_test_variations = []

        '''
        #Prune variation for single port with CLONE and EXTENDED
        for variation in unfiltered_test_variations:
            port_list = variation[0]
            display_config = variation[2]

            if len(port_list) == 1 and 'SINGLE' in display_config:
                continue
            filtered_test_variations.append(variation)
        '''
        filtered_test_variations = unfiltered_test_variations

        test_variations = []
        variation_count = len(filtered_test_variations)
        if variation_count > 2:
            test_variations.append(filtered_test_variations[0])
            # test_variations.append(filtered_test_variations[variation_count//2])
            test_variations.append(filtered_test_variations[variation_count - 1])
        else:
            test_variations = filtered_test_variations

        test_variations = filtered_test_variations
        logging.info(
            "Selecting %d variation from %d variations" % (len(test_variations), len(filtered_test_variations)))

        iteration_count = 1

        for variation in test_variations:
            logging.info("**************** Started iteration %d ****************" % (iteration_count))

            port_list = variation[0]
            is_low_power = variation[1]
            display_config = variation[2]
            power_transition_state = variation[3]

            logging.info("Prepare setup for variation : %s" % str(variation))
            for port in port_list:
                self.plug_device(port, is_low_power)
                self.verify_display_topology(port, 'PLUG')

            logging.info("Apply configuration %s" % display_config)
            # TODO: Apply display_config
            self.verify_underrun()

            if power_transition_state == "S3":
                logging.info("Apply power state %s" % power_transition_state)
                self.goto_powerstate_s3()
                self.verify_underrun()

            # self.verify_corruption()

            for port in port_list:
                self.PLUG_UNPLUG_TEST['action'] = "UNPLUG"
                self.PLUG_UNPLUG_TEST['port'] = port
                result = unplug(port, is_low_power)
                self.assertEquals(result, True, "UnPlug API failed for %s" % (port))

                self.verify_display_topology(port, 'UNPLUG')

            logging.info("**************** Ended iteration %d ****************" % iteration_count)
            iteration_count += 1

    def tearDown(self):
        for port in get_supported_external_ports():
            unplug(port, False)
        logging.info("ULT Complete")


if __name__ == '__main__':
    test_environment.TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_header.cleanup(outcome.result)
    gta_state_manager.update_test_result(outcome.result, status)
    display_logger._cleanup()
