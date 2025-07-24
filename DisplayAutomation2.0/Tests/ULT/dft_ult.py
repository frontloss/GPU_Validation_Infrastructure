###############################################################################
# \ref dft_ult.py
# \brief dft_ult.py tests API's dft.py
# \ 'verify_crc' and 'check_underrun' are custom tags for this ult. Their default value is false.
# \ If user wants to verify CRC and check underrun, then he can pass true value from commandline.
# Commandline : 1.) dft_ult.py -check_underrun true -verify_crc true ( To verify crc and check underrun)
#               2.) dft_ult.py 
# \author   Ami Golwala, Bharath Venkatesh
###############################################################################
import os, sys
import unittest
from Libs.Core.cmd_parser import *
from Libs.Core.display_power import *
from Libs.Core.display_utility import *
from Libs.Core.system_utility import *
from Libs.Core.test_env.test_environment import *
from Libs.Core.display_config.display_config import *
from Libs.Core import reboot_helper, display_essential


class DftUlt(unittest.TestCase):
    DP_PANEL = {'EDID': 'DELL_U2711_SST_EDID.bin', 'DPCD': 'DELL_U2711_SST_DPCD.bin'}
    HDMI_PANEL = {'EDID': 'HDMI_Dell_3011.EDID'}
    sys_utility = SystemUtility()
    disp_config = DisplayConfiguration()
    disp_power = DisplayPower()

    # @unittest.skip("Skipping plug unplug simulation test in normal mode")
    def test_1_plug_unplug_normal(self):
        self.plug_unplug_sanity(None, False)

    # @unittest.skip("Skipping plug unplug simulation test in S3")
    def test_2_plug_unplug_s3(self):
        self.plug_unplug_sanity(self.goto_powerstate_s3, True)

    # @unittest.skip("Skipping plug unplug simulation test in S4")
    def test_3_plug_unplug_s4(self):
        self.plug_unplug_sanity(self.goto_powerstate_s4, True)

    @unittest.skip("Skipping plug unplug simulation test as persistence in Yangra isn't available")
    def test_3_plug_unplug_s5(self):
        self.plug_unplug_sanity(self.goto_powerstate_s5, True)

    @unittest.skip("Skipping eDP plug unplug simulation test")
    def test_4_eDP_plug_unplug(self):
        port = 'DP_A'
        edid = 'EDP_1920_1080.EDID'
        dpcd = 'EDP_1920_1080_DPCD.txt'

        logging.info("Trying to plug %s with EDID:%s and DPCD:%s" % (port, edid, dpcd))
        ##
        # Plugging the display
        is_display_plugged = plug(port, edid, dpcd)
        self.assertEquals(is_display_plugged, True, "Aborting the test as plugging of display is failed")
        logging.info("Edp is plugged")
        ##
        # Restart display driver
        result, reboot_required = display_essential.restart_gfx_driver()
        self.assertEquals(result, True, "Aborting the test as Display driver restart failed")

        ##
        # Verifying using enumerated display
        self.verify_using_enumerated_display(port, True)

        ##
        # Unplugging the display
        self.is_edp_display_unplugged = unplug(port, False)

        ##
        # Rebooting the system
        self.goto_powerstate_s5()

    def tearDown(self):
        logging.info("****** Tear Down ********")

    ##
    # @brief Verifying whether perticular display is attached or not using enumerated display.
    # @param[in] - port of type CONNECTOR_PORT_TYPE
    # @param[in] - is_plug of type Bool. True - if plugging the display, False - if unplugging the display
    # @return - None
    def verify_using_enumerated_display(self, port, is_plug):
        ##
        # Verifying using enumerated display
        self.enumerated_displays = self.disp_config.get_enumerated_display_info()
        is_disp_attached = is_display_attached(self.enumerated_displays, port)
        self.assertEquals(is_disp_attached, is_plug, "Aborting the test as verification of display failed")
        if is_plug:
            logging.info("Plug successful for : %s" % port)
        else:
            logging.info("UnPlug successful for : %s" % port)
        logging.info("Enumerated Display Information: %s", self.enumerated_displays.to_string())

    ##
    # Rebooting the system and saving the context
    def goto_powerstate_s3(self):
        self.disp_power.invoke_power_event(PowerEvent.S3, 30)

    ##
    # Rebooting the system and saving the context
    def goto_powerstate_s4(self):
        self.disp_power.invoke_power_event(PowerEvent.S4, 30)

    ##
    # Rebooting the system and saving the context
    def goto_powerstate_s5(self):
        if reboot_helper.reboot(self, 'test_2_step') is False:
            self.fail("Failed to reboot the system")

    def verify_display_topology(self, port, action, negative=False):
        enumerated_displays = self.disp_config.get_enumerated_display_info()
        is_disp_attached = is_display_attached(enumerated_displays, port)

        if action == "PLUG":
            expected_state = True
        else:
            expected_state = False

        if negative:
            expected_state = not expected_state

        logging.info("current display topology: %s", enumerated_displays.to_string())
        self.assertEquals(is_disp_attached, expected_state, "Verification of %s failed on port %s" % (action, port))
        logging.info("Verification of %s success on port %s" % (action, port))

    ##
    # Helper function to plug and unplug all supported ports in all possible
    # combination with different power state
    def plug_unplug_sanity(self, power_state_func, low_power_state):
        # currently get_free_ports isn't functional, hence hard-coding ports
        # ports = vbt_interface.get_free_ports()
        ports = ['DP_C', 'HDMI_B']
        sleep_time = 5
        # Avoiding DP_A simulation
        if 'DP_A' in ports:
            ports.remove('DP_A')

        port_vector = self.get_possible_plug_unplug(ports, True)

        for port_list in port_vector:
            logging.info("********[START] %s **********\n" % port_list)
            for port in port_list:
                if "DP" in port.upper():
                    edid_file = self.DP_PANEL['EDID']
                    dpcd_file = self.DP_PANEL['DPCD']
                elif "HDMI" in port.upper():
                    edid_file = self.HDMI_PANEL['EDID']
                    dpcd_file = None
                else:
                    raise Exception("Edid details not found for %s" % (port))

                logging.info(
                    "Plug %s EDID = %s DPCD = %s low_power_state = %s" % (port, edid_file, dpcd_file, low_power_state))
                plug(port, edid_file, dpcd_file, low_power_state)
                if low_power_state:
                    self.verify_display_topology(port, 'PLUG', negative=True)
                    power_state_func()
                    logging.info("Sleep after power state")
                    time.sleep(sleep_time)
                    logging.info("Done Sleep of %d secs" % sleep_time)

                self.verify_display_topology(port, 'PLUG', negative=False)

                logging.info("Unplug %s low_power_state = %s" % (port, low_power_state))
                unplug(port, low_power_state)
                if low_power_state:
                    self.verify_display_topology(port, 'UNPLUG', negative=True)
                    power_state_func()
                    logging.info("Sleep after power state")
                    time.sleep(sleep_time)
                    logging.info("Done Sleep of %d secs" % sleep_time)

                self.verify_display_topology(port, 'UNPLUG', negative=False)
            logging.info("********[END] %s **********\n" % port_list)

    # Generate possible permutation of display config using display list
    def get_possible_plug_unplug(self, display_list, combination=False):
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


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DftUlt'))
    TestEnvironment.cleanup(results)
