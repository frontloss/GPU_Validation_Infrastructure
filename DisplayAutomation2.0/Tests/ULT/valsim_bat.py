#######################################################################################################################
# @file         valsim_bat.py
# @addtogroup   Tests_Display_Val_BAT
# @brief        Test suite to catch issues due to prepare_display and valsim hotplug events for Yangra platforms.
# @details      Valsim Bat ensures all ports are simulated properly. Also validates prepare_display_setup functionality.
#               Always run the test for one adapter at a time (-gfx_0/-gfx_1).
#               Test Flow:
#                   1. Enable Ports to be supported on a platform for requested adapter index.
#                   2. Perform Plug/Unplug and verify for all supported ports.
#                   3. Validate display enumeration status for individual tests.
#               CommandLine : python Tests\Display_Val_BAT\valsim_bat.py <-gfx_0/-gfx_1> [<-skip_edp/-skip_mipi>]
#               Example :
#                   python valsim_bat.py -gfx_0
#                   python valsim_bat.py -gfx_1 -skip_edp
#
# @author      Kiran Kumar Lakshmanan
#######################################################################################################################
import logging
import sys
import time
import unittest

from Libs import prepare_display_setup
from Libs.Core import reboot_helper, display_utility
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.display_config import display_config, display_config_enums as cfg_enum
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt

PLATFORM_PORT_INFO = {
    'ICLLP': {'EDP': ['EDP_A'],
              'HEADLESS': ['EDP_NONE'],
              'MIPI': [],
              'TC': ['DP_C', 'DP_D', 'DP_E', 'DP_F'],
              'PLUS': ['DP_B', 'DP_C', 'DP_D', 'DP_E', 'DP_F'],
              'NATIVE': ['HDMI_B', 'HDMI_C', 'HDMI_D', 'HDMI_E', 'HDMI_F'],
              'TBT': ['DP_C', 'DP_D', 'DP_E', 'DP_F']},
    'LKF1': {'EDP': [],
             'HEADLESS': ['EDP_NONE'],
             'MIPI': ['MIPI_A'],
             'TC': ['DP_D', 'DP_E'],
             'PLUS': ['DP_D', 'DP_E'],
             'NATIVE': [],
             'TBT': []},
    'TGL': {'EDP': ['EDP_A', 'EDP_B'],
            'HEADLESS': ['EDP_NONE'],
            'MIPI': ['MIPI_A'],
            'TC': ['DP_D', 'DP_E', 'DP_F', 'DP_G'],
            'PLUS': ['DP_A', 'DP_B', 'DP_D', 'DP_E', 'DP_F'],
            'NATIVE': ['HDMI_B'],
            'TBT': ['DP_D', 'DP_E', 'DP_F', 'DP_G']},
    'ADLP': {'EDP': ['EDP_A', 'EDP_B'],
             'HEADLESS': ['EDP_NONE'],
             'MIPI': ['MIPI_A', 'MIPI_C'],
             'TC': ['DP_F', 'DP_G', 'DP_I'],
             'PLUS': ['DP_A', 'DP_B', 'DP_F', 'DP_G', 'DP_H', 'DP_I'],
             'NATIVE': ['HDMI_B', 'HDMI_F', 'HDMI_G', 'HDMI_H', 'HDMI_I'],
             'TBT': ['DP_F', 'DP_G']},
    'ADLS': {'EDP': ['EDP_A'],
             'HEADLESS': ['EDP_NONE'],
             'MIPI': [],
             'TC': [],
             'PLUS': ['DP_A', 'DP_B', 'DP_C', 'DP_D'],
             'NATIVE': ['HDMI_B', 'HDMI_C', 'HDMI_D'],
             'TBT': []},
    'DG1': {'EDP': ['EDP_A'],
            'HEADLESS': ['EDP_NONE'],
            'MIPI': [],
            'TC': [],
            'PLUS': ['DP_A', 'DP_B', 'DP_C', 'DP_D'],
            'NATIVE': ['HDMI_B', 'HDMI_C', 'HDMI_D'],
            'TBT': []},
    'DG2': {'EDP': ['EDP_A'],
            'HEADLESS': ['EDP_NONE'],
            'MIPI': [],
            'TC': ['DP_F'],
            'PLUS': ['DP_A', 'DP_B', 'DP_C', 'DP_D'],
            'NATIVE': ['HDMI_B', 'HDMI_C', 'HDMI_D'],
            'TBT': []},
    'MTL': {'EDP': ['EDP_A'],
            'HEADLESS': ['EDP_NONE'],
            'MIPI': [],
            'TC': [],
            'PLUS': ['DP_A', 'DP_B'],
            'NATIVE': [],
            'TBT': []},
    'ELG': {'EDP': ['EDP_A'],
            'HEADLESS': ['EDP_NONE'],
            'MIPI': [],
            'TC': [],
            'PLUS': ['DP_A'],
            'NATIVE': [],
            'TBT': []},
    'LNL': {'EDP': ['EDP_A'],
            'HEADLESS': ['EDP_NONE'],
            'MIPI': [],
            'TC': [],
            'PLUS': ['DP_A', 'DP_B'],
            'NATIVE': [],
            'TBT': []},
    'PTL': {'EDP': ['EDP_A'],
            'HEADLESS': ['EDP_NONE'],
            'MIPI': [],
            'TC': [],
            'PLUS': ['DP_A', 'DP_B'],
            'NATIVE': [],
            'TBT': []},
    'NVL': {'EDP': ['EDP_A'],
             'HEADLESS': ['EDP_NONE'],
             'MIPI': [],
             'TC': [],
             'PLUS': ['DP_A', 'DP_B'],
             'NATIVE': [],
             'TBT': []}
}


##
# @brief        Helper Function to check if test has to be skipped
#               Usage: pass "<-skip_edp/-skip_mipi>" in commandline
# @param[in]    port name string which has to be skipped
# @return       Bool (True if test has to skipped, else False)
def is_skip(port: str):
    skip_flag = False
    for arg in sys.argv:
        arg = arg.strip().upper()
        if arg.startswith("-SKIP_"):
            port_name = arg.replace('-SKIP_', '')
            if port == port_name:
                skip_flag = True
                break
    return skip_flag


##
# @brief This class contains functions that helps in running plug and unplug of all supported ports
class DisplayValBat(unittest.TestCase):

    ##
    # @brief       This class method is the entry point for valsim_bat
    # @param[in]   args command line arguments used to fill the instance members
    # @param[in]   kwargs keyword arguments used to fill the instance members
    def __init__(self, *args, **kwargs):
        # WA: Do not remove. Added as a workaround for reboot_helper functionality
        super(DisplayValBat, self).__init__(*args, **kwargs)
        self.prepare_display_setup_ = prepare_display_setup.PrepareDisplaySetup()
        self.display_config_ = display_config.DisplayConfiguration()

        self.gfx_index: str = ""
        self.platform_name: str = ""
        self.platform_info: dict = {
            gfx_index: {
                'gfx_index': gfx_index,
                'name': adapter_info.get_platform_info().PlatformName
            }
            for gfx_index, adapter_info in TestContext.get_gfx_adapter_details().items()
        }
        self.connector_port_type: str = ""
        self.display_list: list = []
        self.initial_args: tuple = tuple(sys.argv)
        self.prepare_display_setup_.skip_reboot = True

    ##
    # @brief        This function helps to parse the commandline and prepare ports to run the test
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self) -> None:
        self.test_status: bool = True
        stripped_test_name = self._testMethodName.replace("test_", "").upper()
        self.connector_port_type = stripped_test_name if stripped_test_name != "EDP_NONE" else "HEADLESS"

        logging.info(f"{'=' * 32}START: {self._testMethodName}{'=' * 32}")
        self.parse_val_bat_cmdline()

        self.prepare_ports()
        logging.info(f"Commandline after prepare_ports(): {sys.argv}")

        # Skip underrun checks after each plug/unplug calls.
        # Utilize diana to check for underrun at the end of suite.
        VerifierCfg.underrun = Verify.SKIP

    ##
    # @brief        This function helps to clean the ports configured by previous test and verify underrun and TDR
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self) -> None:
        self.cleanup_ports()
        if Vbt().reset() is False:
            logging.error("Failed to Reset VBT")
        else:
            logging.info("Reset VBT Successful.")
        # check for underrun and tdr
        VerifierCfg.underrun = Verify.LOG_CRITICAL
        VerifierCfg.tdr = Verify.LOG_CRITICAL
        logging.info(f"{'=' * 32}END: {self._testMethodName}{'=' * 32}")

    ##
    # @brief        This function helps to run the EDP test
    # @return       True if test is successful or False if test fails to configure EDP
    @unittest.skipIf(is_skip('EDP'), "Skipping EDP test")
    def test_edp(self):
        if self.display_list:
            logging.info(f"Validating for ({self.connector_port_type}) on gfx_index ({self.gfx_index})")
            if reboot_helper.is_reboot_scenario() is False:
                self.vbt_simulation()

                if reboot_helper.reboot(self, self._testMethodName) is False:
                    logging.error("Failed to reboot the system")
                    self.fail()
            else:
                self.verify_embedded_display_enumeration(display_ls=self.display_list)
        else:
            logging.info(f"Skipping {self._testMethodName} since No ports available on {self.platform_name}!!")
        self.analyze_test_result()

    ##
    # @brief        This function helps to run without EDP and only external displays
    # @return       pass
    @unittest.skipIf(is_skip('EDP_NONE'), "Skipping EDP_NONE test")
    def test_edp_none(self):
        # TBD: Implementation for headless display (EDP_NONE)
        pass

    ##
    # @brief        This function helps to run the TypeC test on the supported port
    # @return       True if test is successful or False if test fails to configure tc
    @unittest.skipIf(is_skip('TC'), "Skipping TC test")
    def test_tc(self):
        if self.display_list:
            logging.info(f"Validating for ({self.connector_port_type}) on gfx_index ({self.gfx_index})")
            self.vbt_simulation()
            # Generate plug display list for calling display_utility.[plug()/unplug()]
            plug_disp_list = ["_".join(disp.split("_")[:2]) for disp in self.display_list]
            self.verify_plug_unplug(display_list=plug_disp_list)
        else:
            logging.info(f"Skipping {self._testMethodName} since No ports available on {self.platform_name}!!")
        self.analyze_test_result()

    ##
    # @brief        This function helps to run the TBT test on the supported port
    # @return       True if test is successful or False if test fails to configure tbt
    @unittest.skipIf(is_skip('TBT'), "Skipping TBT test")
    def test_tbt(self):
        if self.display_list:
            logging.info(f"Validating for ({self.connector_port_type}) on gfx_index ({self.gfx_index})")
            self.vbt_simulation()
            # Generate plug display list for calling display_utility.[plug()/unplug()]
            plug_disp_list = ["_".join(disp.split("_")[:2]) for disp in self.display_list]
            self.verify_plug_unplug(display_list=plug_disp_list)
        else:
            logging.info(f"Skipping {self._testMethodName} since No ports available on {self.platform_name}!!")
        self.analyze_test_result()

    ##
    # @brief        This function helps to run the Native port test
    # @return       True if test is successful or False if test fails to configure native port
    @unittest.skipIf(is_skip('NATIVE'), "Skipping NATIVE test")
    def test_native(self):
        if self.display_list:
            logging.info(f"Validating for ({self.connector_port_type}) on gfx_index ({self.gfx_index})")
            self.vbt_simulation()
            # Generate HDMI plug display list for calling display_utility.[plug()/unplug()]
            plug_disp_list = ["_".join(disp.split("_")[:2]) for disp in self.display_list]
            # Plug/Unplug for HDMI in native port scenario
            self.verify_plug_unplug(display_list=plug_disp_list)
        else:
            logging.info(f"Skipping {self._testMethodName} since No ports available on {self.platform_name}!!")
        self.analyze_test_result()

    ##
    # @brief        This function helps to run the DP and HDMI PLUS port test
    # @return       True if test is successful or False if test fails to configure plus port
    @unittest.skipIf(is_skip('PLUS'), "Skipping PLUS test")
    def test_plus(self):
        if self.display_list:
            logging.info(f"Validating for ({self.connector_port_type}) on gfx_index ({self.gfx_index})")
            if all(isinstance(display, list) for display in self.display_list):
                for display in self.display_list:
                    self.vbt_simulation(custom_display_list=display)
                    # Plug/Unplug for HDMI and DP in plus port scenario
                    if self.platform_name == "TGL":
                        # TGL supports only Ports A, B for PLUS through valsim
                        additional_disp_list = [disp.replace("DP_", "HDMI_") for disp in display if
                                                disp.split("_")[-1].upper() in ["A", "B"]]
                    else:
                        additional_disp_list = [disp.replace("DP_", "HDMI_") for disp in display]
                    display.extend(additional_disp_list)
                    self.verify_plug_unplug(display_list=display)
            else:
                # Condition hits when less than 3 PLUS ports are supported
                self.vbt_simulation()
                plug_disp_list = self.display_list
                # Plug/Unplug for HDMI and DP in plus port scenario
                additional_disp_list = [disp.replace("DP_", "HDMI_") for disp in plug_disp_list]
                plug_disp_list.extend(additional_disp_list)
                self.verify_plug_unplug(display_list=plug_disp_list)
        else:
            logging.info(f"Skipping {self._testMethodName} since No ports available on {self.platform_name}!!")
        self.analyze_test_result()

    ##
    # @brief        This function helps to run the MIPI test on supported port
    # @return       True if test is successful or False if test fails to configure MIPI
    @unittest.skipIf(is_skip('MIPI'), "Skipping MIPI test")
    def test_mipi(self):
        if self.display_list:
            logging.info(f"Validating for ({self.connector_port_type}) on gfx_index ({self.gfx_index})")
            if reboot_helper.is_reboot_scenario() is False:
                self.vbt_simulation()

                if reboot_helper.reboot(self, self._testMethodName) is False:
                    logging.error("Failed to reboot the system")
                    self.fail()
            else:
                self.verify_embedded_display_enumeration(display_ls=self.display_list)
        else:
            logging.info(f"Skipping {self._testMethodName} since No ports available on {self.platform_name}!!")
        self.analyze_test_result()

    ##
    # @brief        Capture failures within test and update unittest. Call within test only.
    # @return       None
    def analyze_test_result(self) -> None:
        if not self.test_status:
            self.fail(f"-----------Test failure(s) observed in {self._testMethodName}-----------")

    ##
    # @brief        Generates display_list to be simulated for current test case
    #               based on platform info, gfx_index and connector_port_type.
    # @return       None
    def prepare_ports(self) -> None:
        if self.gfx_index not in self.platform_info.keys():
            # Exit on invalid gfx_index in commandline
            self.fail(
                f"Invalid gfx_index passed ({self.gfx_index}). Available gfx list: ({list(self.platform_info.keys())})")
        # Get platform name
        self.platform_name = self.platform_info[self.gfx_index]['name']
        logging.info(f"Platform Name identified as ({self.platform_name}).")

        # Get supported ports list for identified platform
        port_suffix_list = PLATFORM_PORT_INFO[self.platform_name][self.connector_port_type]

        # Generate the ports based on supported port list
        if len(port_suffix_list) == 0:
            # since there is no known supported ports for this connector_port_type, we will skip this step
            logging.warning(f"No ports identified to be simulated for connector_port ({self.connector_port_type})!!")
        if self.connector_port_type in ["EDP", "MIPI", "HEADLESS"]:
            self.display_list = port_suffix_list
        elif self.connector_port_type in ["TC", "TBT", "NATIVE"]:
            self.display_list.extend([port + "_" + self.connector_port_type for port in port_suffix_list])
        elif self.connector_port_type == "PLUS":
            self.display_list.extend([port for port in port_suffix_list])
            # Need to run PLUS test in 2 separate runs since free vbt ports are limited
            self.display_list = self.split_display_list(self.display_list)
        else:
            # Possibly Unknown port type in testMethodName or split for testMethodName is incorrect
            logging.error(f"Invalid connector port type identified ({self.connector_port_type})")
            self.test_status = False

        logging.info(f"Generated Display List to be simulated - {self.display_list}")

    ##
    # @brief        This function calls prepare_display_setup to configure VBT and init all ports required.
    # @param[in]    custom_display_list of displays which needs to be simulated.
    # @return       None
    def vbt_simulation(self, custom_display_list=None) -> None:
        if custom_display_list:
            logging.info(f"Adding display to be simulated {custom_display_list} to sys.argv - {sys.argv}")
            self.update_args_list(display_list=custom_display_list)
        else:
            logging.info(f"Adding displays to be simulated {self.display_list} to sys.argv - {sys.argv}")
            self.update_args_list(display_list=self.display_list)

        # Note: Current scenario will require the implementation of prepare_display's setup and runTest to be called for
        # vbt simulation for enabling the specific ports from the generated commandline.
        # ToDo: Call a library reusable function instead of calling a setup, runTest and teardown from prepare_display
        # Prepare display validation
        self.prepare_display_setup_.setUp()
        self.prepare_display_setup_.runTest()
        # In case of Embedded displays, test will handle verification of ports
        if self.connector_port_type not in ["EDP", "MIPI", "HEADLESS"]:
            self.prepare_display_setup_.tearDown()
            driver_interface.DriverInterface().initialize_all_efp_ports()

    ##
    # @brief        Verify if Embedded displays are enumerated successfully.
    # @param[in]    display_ls : Display list to be validated
    # @return       None
    def verify_embedded_display_enumeration(self, display_ls: list) -> None:
        if self.connector_port_type == "EDP":
            display_ls = [disp.replace("EDP_", "DP_") for disp in display_ls]
        for display in display_ls:
            if not self.verify_display_enumeration(display=display, connector_port_type="EMBEDDED"):
                logging.error(f"Display verification failed for {display} on {self.connector_port_type} port.")
                self.test_status = False
            else:
                logging.info(f"Current display ({display}) is enumerated as {self.connector_port_type} port.")

    ##
    # @brief        Verify individual display enumeration for specified connector_port_type
    # @param[in]    display name
    # @param[in]    connector_port_type for this display
    # @return       Bool - True if display is enumerated, else False
    def verify_display_enumeration(self, display: str, connector_port_type=None) -> bool:
        verify_flag = False
        if connector_port_type is None:
            connector_port_type = self.connector_port_type
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        logging.info(f"#Displays: {enumerated_displays.Count} | Enumerated Displays: {enumerated_displays.to_string()}")
        for disp_count in range(enumerated_displays.Count):
            current_display = enumerated_displays.ConnectedDisplays[disp_count]
            if current_display.DisplayAndAdapterInfo.adapterInfo.gfxIndex == self.gfx_index and cfg_enum.CONNECTOR_PORT_TYPE(
                    current_display.ConnectorNPortType).name == display and current_display.PortType == connector_port_type:
                logging.info(f"Current Display {display} is Enumerated as {self.connector_port_type}.")
                verify_flag = True
                break
        return verify_flag

    ##
    # @brief        Perform Plug/Unplug actions for a single port.
    # @param[in]    display to be simulated
    # @return       None
    def plug_unplug(self, display: str) -> None:
        plugged = display_utility.plug(port=display, port_type=self.connector_port_type, gfx_index=self.gfx_index)
        logging.info(f"Plug_status for display ({display}) on port ({self.connector_port_type}) - {plugged}")
        time.sleep(15)  # Wait for some time

        if not self.verify_display_enumeration(display):
            logging.error(f"PLUG: Display verification failed for {display} on {self.connector_port_type} port.")
            self.test_status = False

        if plugged:
            unplugged = display_utility.unplug(port=display, port_type=self.connector_port_type,
                                               gfx_index=self.gfx_index)
            logging.info(f"Unplug_status for display ({display}) on port ({self.connector_port_type}) - {unplugged}")
            time.sleep(15)  # Wait for some time

            if self.verify_display_enumeration(display):
                logging.error(f"UNPLUG: Display verification failed for {display} on {self.connector_port_type} port.")
                self.test_status = False
        else:
            logging.error(f"Skipping Unplug call since Plug for display ({display}) failed!!!")
            self.test_status = False

    ##
    # @brief        Perform Plug/Unplug actions as required for each port.
    # @param[in]    display_list - list of displays to be simulated
    # @return       None
    def verify_plug_unplug(self, display_list: list) -> None:
        logging.info(
            f"Plug-Unplug for list - {display_list} and gfx_index - {self.gfx_index} conn_port - {self.connector_port_type}")
        if self.connector_port_type not in ["EDP", "MIPI", "HEADLESS"]:
            for display in display_list:
                self.plug_unplug(display=display)

    ##
    # @brief        Appends displays to sys.argv which is passed to prepare_display
    # @param[in]    display_list - list of displays to be simulated
    # @return       None
    def update_args_list(self, display_list: list) -> None:
        sys.argv = [arg for arg in self.initial_args]
        sys.argv.extend(["-" + port for port in display_list])
        logging.info(f"Updated args list info for current test run - {sys.argv}")

    ##
    # @brief        Commandline parser for val_bat commandline.
    #               Generates gfx_index, connector_port_type and displays to be simulated for current test case.
    # @return       None
    def parse_val_bat_cmdline(self) -> None:
        gfx_index = [args.lower() for args in sys.argv if args.lower().startswith("-gfx_")]
        if len(gfx_index) == 0:
            self.gfx_index = "gfx_0"
            logging.info("Assuming gfx_0 as default gfx_index to be validated.")
        elif len(gfx_index) > 1:
            logging.error("Usage: python valsim_bat.py -<gfx_0/gfx_1/..> -<skip_edp/skip_mipi>")
            self.fail("Invalid commandline.")
        else:
            self.gfx_index = gfx_index[0].replace("-", "")
        logging.info(f"gfx_index identified as {self.gfx_index}")

    ##
    # @brief        Split list into 2 halves
    # @param[in]    ls : Display list from platform_port_info dict
    # @return       ret_list: list of displays
    def split_display_list(self, ls: list) -> list:
        ret_list = []
        if len(ls) > 2:
            ret_list.append(ls[:len(ls) // 2])
            ret_list.append(ls[len(ls) // 2:])
        else:
            ret_list = ls
        return ret_list

    ##
    # @brief        Reset the sys.argv list for next test
    # @return       None
    def cleanup_ports(self) -> None:
        sys.argv = [arg for arg in self.initial_args]
        logging.info(f"sys.argv after cleaning: {sys.argv}")


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite("DisplayValBat"))
    TestEnvironment.cleanup(results)
