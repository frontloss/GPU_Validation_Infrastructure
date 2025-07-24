##
# @file install_uninstall2_base.py
# @brief The script accepts the display list and Driver type from the command line.
#       The following script has below api along with the unittest setup and teardown function.
# @details * To verify whether drivers are running or not
#          * To install graphics driver from device manager
#          * To install/uninstall graphics driver and to check the driver version
#          * To set the display configuration according to the Configuration mentioned by the user.
# @author Patel, Ankurkumar G, Chandrashekhar, SomashekarX, Doriwala, Nainesh P

import logging
import os
import shutil
import subprocess
import sys
import unittest

from Libs.Core import cmd_parser, registry_access
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo, SystemDriverType
from Libs.Core.test_env import test_context, verification_manager
from Libs.Core.test_env.test_context import TestContext
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

# higher version driver/primary driver
DRIVER_PATH = "C:\Driver\Gfxinstaller"

# lower version driver/secondary driver
SEC_DRIVER_PATH = r"C:\Driver\Gfxinstaller\Sec_Gfx_Dvr\64bit"


##
# @brief This contains helper functions/API along with unittest setup and teardown functions
class InstallUninstall2Base(unittest.TestCase):
    config = DisplayConfiguration()
    under_run_status = UnderRunStatus()
    obj_machine_info = SystemInfo()

    plugged_display = []
    enumerated_displays = None
    input_display_list = []
    driver_type = "NON_UWD"  # Default installation will be of non UWD driver
    custom_tags = ['-driver_type']
    is_teardown_required = False

    devcon_exe_path = TestContext.devcon_path()
    cert_install_path = os.path.join(test_context.COMMON_BIN_FOLDER, "CertificateInstall.exe")

    ##
    # @brief setUp Function for Install_Uninstall
    # @return None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.debug("Entry: setUpClass")
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        self.input_display_list[:] = []
        # input_display_list[] is a list of Port Names from user args
        # Handle multi-adapter scenario
        if not isinstance(self.cmd_line_param, list):
            self.cmd_line_param = [self.cmd_line_param]

        for index in range(len(self.cmd_line_param)):
            adapter_dict = self.cmd_line_param[index]
            for key, value in iter(adapter_dict.items()):
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if value['gfx_index'] is not None:
                            self.input_display_list.append((value['connector_port'], value['gfx_index']))

                ##
                # Fetch type of driver to be installed from command line (if provided)
                if key == 'DRIVER_TYPE':
                    if value:
                        self.driver_type = str(value[0])
                        logging.debug('driver type provided via the command-line is : %s'
                                      % self.driver_type)
                    else:
                        logging.debug('Value for driver_type not provided in command-line. '
                                      'Using the default value as : %s' % self.driver_type)

                if key == 'CONFIG':
                    if value:
                        self.config_type = eval('enum.%s' % value)
                    else:
                        self.config_type = enum.SINGLE

        if self.driver_type not in ['NON_UWD', 'UWD', 'UWD_DC', 'UWD_DCH', 'UWD_DCH_D', 'UWD_DCH_I']:
            self.fail('Invalid driver_type provided')

        logging.debug("Exit: setUpClass")

    ##
    # @brief Function to verify drivers are running or not
    # @param[in] gfx_index - Graphics Index to which verify status of driver
    # @return boolean value true (running) or false(Not running)
    def is_driver_running(self, gfx_index):
        adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
        drivers_info = self.obj_machine_info.get_driver_info(SystemDriverType.GFX)
        for driver in range(drivers_info.Count):
            if drivers_info.DriverInfo[driver].DeviceID == adapter_info.deviceID:
                logging.debug("Device ID:{}".format(drivers_info.DriverInfo[driver].DeviceID))
                if drivers_info.DriverInfo[driver].Status != "Running":
                    logging.info("GFX driver is not running for Device ID: {}"
                                 .format(drivers_info.DriverInfo[driver].DeviceID))
                    return False
                logging.info("GFX driver is running for Device ID: {}"
                             .format(drivers_info.DriverInfo[driver].DeviceID))
        return True

    ##
    # @brief Function to check that driver is installed or not
    # @param[in] gfx_index - Graphics Index to which verify driver installation status
    # @return boolean value True(Installed) or False(not-installed)
    def is_driver_installed(self, gfx_index):
        driver_inf = ''
        adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
        drivers_info = self.obj_machine_info.get_driver_info(SystemDriverType.GFX)
        for driver in range(drivers_info.Count):
            if drivers_info.DriverInfo[driver].DeviceID == adapter_info.deviceID:
                logging.debug("Device ID:{}, Driver INF:{}".format(drivers_info.DriverInfo[driver].DeviceID,
                                                                   drivers_info.DriverInfo[driver].DriverInf))
                driver_inf = drivers_info.DriverInfo[driver].DriverInf
                driver_inf = driver_inf.split('INF\\')[1]
                if driver_inf == "display.inf":
                    logging.info("GFX driver is not installed for Device ID: {}"
                                 .format(drivers_info.DriverInfo[driver].DeviceID))
                    return False
        return True

    ##
    # @brief Function to install graphics driver through device manager
    # @param[in] dvr_path - Driver path for installation
    # @param[in] driver_type - tells the type of driver ("NON_UWD"/"UWD_DC"/"UWD_DCH"/"UWD_DCH_D"/"UWD_DCH_I")
    # @return boolean value true(Installation Successful) or false (Installation fail)
    def install_graphics_driver_through_device_manager(self, dvr_path, driver_type):
        cert_path = os.path.join(dvr_path, r"Graphics\igdlh.cat")
        inf_path = ""

        if not os.path.exists(cert_path):
            cert_path = os.path.join(dvr_path, r"igdlh.cat")
            if not os.path.exists(cert_path):
                logging.info("cat file not found in driver package")
                return False
        if not os.path.exists(self.cert_install_path):
            logging.info("CertificateInstall.exe not found in TestStore\\bin folder")
            return False
        cert_install_process = subprocess.call([self.cert_install_path, cert_path])
        if cert_install_process != 0:
            logging.info("Certificate installation failed")
            return False
        if driver_type == "NON_UWD":
            inf_path = os.path.join(dvr_path, r"Graphics\igdlh64.inf")
            logging.info("Installing NON_UWD Driver")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"igdlh64.inf")
        elif driver_type == "UWD_DC":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dc.inf")
            logging.info("Installing DC Driver")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dc.inf")
        elif driver_type == "UWD_DCH":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dch.inf")
            logging.info("Installing DCH Driver")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch.inf")
        elif driver_type == "UWD_DCH_D":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dch_d.inf")
            logging.info("Installing DCH Discrete Driver")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch_d.inf")
        elif driver_type == "UWD_DCH_I":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dch_i.inf")
            logging.info("Installing DCH integrated Driver")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch_i.inf")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch.inf")
        else:
            if not os.path.exists(inf_path):
                logging.info("inf file not found at specified location")
                return False

        install_status = subprocess.call(["C:\Windows\System32\pnputil.exe", "/add-driver", inf_path, "/install"])
        verification_manager.configure_skip_driver_check(False)
        return True

    ##
    # @brief Function to uninstall graphics drivers
    # @param[in] gfx_index - Graphics Index on which adapter driver need to uninstall
    # @return boolean value true
    def uninstall_graphics_driver(self, gfx_index):
        driver_inf = ''
        adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
        drivers_info = self.obj_machine_info.get_driver_info(SystemDriverType.GFX)
        for driver in range(drivers_info.Count):
            if drivers_info.DriverInfo[driver].DeviceID == adapter_info.deviceID:
                logging.info("uninstalling gfx driver for Device ID:{}"
                             .format(drivers_info.DriverInfo[driver].DeviceID))
                driver_inf = drivers_info.DriverInfo[driver].DriverInf
                driver_inf = driver_inf.split('INF\\')[1]
                logging.info("driver_inf:{}".format(driver_inf))
                if driver_inf != "display.inf":
                    uninstall_status = subprocess.call(
                        ["C:\Windows\System32\pnputil.exe", "/delete-driver", driver_inf, "/uninstall", "/force"])
                    logging.info("uninstall status: {}".format(uninstall_status))
                    verification_manager.configure_skip_driver_check(True)

        return True

    ##
    # @brief Function to uninstall all graphics drivers
    # @return boolean value true
    def uninstall_all_graphics_driver(self):
        driver_inf = ''
        drivers_info = self.obj_machine_info.get_driver_info(SystemDriverType.GFX)
        for driver in range(drivers_info.Count):
            logging.info("uninstalling gfx driver for Device ID:{}"
                         .format(drivers_info.DriverInfo[driver].DeviceID))
            driver_inf = drivers_info.DriverInfo[driver].DriverInf
            driver_inf = driver_inf.split('INF\\')[1]
            logging.info("driver_inf:{}".format(driver_inf))
            if driver_inf != "display.inf":
                driver_inf = drivers_info.DriverInfo[driver].DriverInf
                uninstall_status = subprocess.call(
                    ["C:\Windows\System32\pnputil.exe", "/delete-driver", driver_inf, "/uninstall", "/force"])
                logging.info("uninstall status: {}".format(uninstall_status))
                verification_manager.configure_skip_driver_check(True)

        return True

    ##
    # @brief plug required display as given in command line parameter.
    # @return plugged_display_list - list of plug displays
    def plug_require_display(self):
        plugged_display_list = []
        for index in range(len(self.cmd_line_param)):
            adapter_dict = self.cmd_line_param[index]
            for key, value in adapter_dict.items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        if value['gfx_index'] is not None and value['is_lfp'] is False:
                            if display_utility.plug(port=value['connector_port'],
                                                    gfx_index=value['gfx_index'].lower()) is True:
                                logging.info("{} Display plug on adapter {}".
                                             format(value['connector_port'], value['gfx_index']))
                                plugged_display_list.append((value['connector_port'], value['gfx_index']))
                            else:
                                self.fail("failed to plug {} display on adapter {}"
                                          .format(value['connector_port'], value['gfx_index']))

        return plugged_display_list

    ##
    # @brief Set the display config as mentioned in config_type
    # @param[in] connected_display is a list of displays
    # @param[in] config_type mentions the configuration type of the display
    # @return boolean true
    def set_display_config(self, connected_display, config_type):
        config = []

        # Apply Configuration
        if len(connected_display) == 1:
            display1 = connected_display[0]

            config = (enum.SINGLE, [display1])

        elif len(connected_display) == 2:
            display1 = connected_display[0]
            display2 = connected_display[1]

            config = (config_type, [display2, display1])

        elif len(connected_display) == 3:
            display1 = connected_display[0]
            display2 = connected_display[1]
            display3 = connected_display[2]

            config = (config_type, [display3, display2, display1])
        elif len(connected_display) == 4:
            display1 = connected_display[0]
            display2 = connected_display[1]
            display3 = connected_display[2]
            display4 = connected_display[3]

            config = (config_type, [display3, display2, display1, display4])

        self.assertNotEquals(config, [], "Invalid config")

        self.assertEquals(self.config.set_display_configuration_ex(config[0], config[1],
                                                                   self.config.get_enumerated_display_info()),
                          True, "failed to apply display configuration")

        logging.info("PASS: Successfully applied Display configuration")
        return True

    ##
    # @brief Function to check driver version
    # @param[in] dvr_path - gives the driver path
    # @param[in] driver_type - tells the type of driver ("NON_UWD"/"UWD_DC"/"UWD_DCH"/"UWD_DCH_D"/"UWD_DCH_I")
    # @param[in] gfx_index - Graphics Index to which verify version
    # @return boolean value true or false
    def check_driver_version(self, dvr_path, driver_type, gfx_index):
        minor_version = ""
        version = []
        major_version = ""
        inf_path = ""
        inf_text_path = ""
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

        if driver_type == "NON_UWD":
            inf_path = os.path.join(dvr_path, r"Graphics\igdlh64.inf")
            inf_text_path = os.path.join(dvr_path, r"Graphics\igdlh64.txt")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"igdlh64.inf")
                inf_text_path = os.path.join(dvr_path, r"igdlh64.txt")
        elif driver_type == "UWD_DC":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dc.inf")
            inf_text_path = os.path.join(dvr_path, r"Graphics\iigd_dc.txt")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dc.inf")
                inf_text_path = os.path.join(dvr_path, r"iigd_dc.txt")
        elif driver_type == "UWD_DCH":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dch.inf")
            inf_text_path = os.path.join(dvr_path, r"Graphics\iigd_dch.txt")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch.inf")
                inf_text_path = os.path.join(dvr_path, r"iigd_dch.txt")
        elif driver_type == "UWD_DCH_D":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dch_d.inf")
            inf_text_path = os.path.join(dvr_path, r"Graphics\iigd_dch_d.txt")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch_d.inf")
                inf_text_path = os.path.join(dvr_path, r"iigd_dch_d.txt")
        elif driver_type == "UWD_DCH_I":
            inf_path = os.path.join(dvr_path, r"Graphics\iigd_dch_i.inf")
            inf_text_path = os.path.join(dvr_path, r"Graphics\iigd_dch_i.txt")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch_i.inf")
                inf_text_path = os.path.join(dvr_path, r"iigd_dch_i.txt")
            if not os.path.exists(inf_path):
                inf_path = os.path.join(dvr_path, r"iigd_dch.inf")
                inf_text_path = os.path.join(dvr_path, r"iigd_dch.txt")
        else:
            if not os.path.exists(inf_path):
                logging.info("inf file not found at specified location")
                return False

        shutil.copy2(inf_path,
                     inf_text_path)
        inf_file_open = open(inf_text_path, "r")

        for line in inf_file_open:
            inf_driver_line = line.replace("\x00", '')
            if "DriverVer=" in inf_driver_line:
                version = (inf_driver_line.split(".")[-1])

            if "PC_Release_Major" in inf_driver_line:
                major_version = (inf_driver_line.split(',')[-1]).split(';')[0]

            if "PC_Release_Minor" in inf_driver_line:
                minor_version = (inf_driver_line.split(',')[-1]).split(';')[0]
                break

        driver_major, major_type = registry_access.read(args=ss_reg_args, reg_name="PC_Release_Major")
        driver_minor, minor_type = registry_access.read(args=ss_reg_args, reg_name="PC_Release_Minor")
        driver_version, version_type = registry_access.read(args=ss_reg_args, reg_name="DriverVersion")

        if (int(version) == int(driver_version.split('.')[-1])) and (
                int(major_version) == driver_major) and (
                int(minor_version) == driver_minor):
            logging.info(
                "PASS: Graphics driver Version check successfull, Expected Driver Ver is: %s.%s.%s, "
                "Actual Driver Ver is: %s.%s.%s",
                major_version.strip(), minor_version.strip(), version.strip(), driver_major,
                driver_minor, driver_version.split('.')[-1])
            return True
        else:
            logging.error(
                "FAIL: Graphics driver Version check unsuccessfull, Expected Driver Ver is: %s.%s.%s, "
                "Actual Driver Ver is: %s.%s.%s",
                major_version.strip(), minor_version.strip(), version.strip(), driver_major, driver_minor,
                driver_version.split('.')[-1])
        return False

    ##
    # @brief tearDown Function for Install_Uninstall
    # @return None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        if self.is_teardown_required:
            for display in self.plugged_display:
                logging.info("Trying to unplug %s", display)
                self.assertEquals(display_utility.unplug(display), True, "Aborting the test as display unplug failed")
                logging.info("Successfully  unplugged %s", display)
        else:
            logging.debug("Unplug of displays not required")
