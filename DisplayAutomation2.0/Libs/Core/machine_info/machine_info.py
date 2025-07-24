########################################################################################################################
# @file     machine_info.py
# @brief    Exposes APIs to provide System related Information
# @author   Beeresh, Raghupathy
########################################################################################################################
import ctypes
import logging
import os
import platform
import re
import subprocess
import xml.etree.ElementTree as Et
from enum import Enum
from typing import Dict, Any

from Libs.Core.core_base import singleton
from Libs.Core.logger import gdhm
from Libs.Core.test_env import state_machine_manager, test_context

MAX_SUPPORTED_ADAPTERS = 10
MAX_DEVICE_ID_LEN = 200
PLATFORM_INFO_DICT = {}

GEN_09_PLATFORMS = ['SKL', 'KBL', 'CFL']
GEN_10_PLATFORMS = ['GLK', 'CNL', 'APL']
GEN_11_PLATFORMS = ['ICLLP', 'EHL', 'JSL']
GEN_11p5_PLATFORMS = ['LKF1']
GEN_12_PLATFORMS = ['TGL', 'RKL', 'DG1', 'ADLS']
GEN_13_PLATFORMS = ['DG2', 'ADLP']
GEN_14_PLATFORMS = ['DG3', 'MTL', 'ELG']
GEN_15_PLATFORMS = ['LNL']
GEN_16_PLATFORMS = ['PTL']
GEN_17_PLATFORMS = ['CLS', 'NVL']
PRE_GEN_11_PLATFORMS = GEN_09_PLATFORMS + GEN_10_PLATFORMS
PRE_GEN_11_P_5_PLATFORMS = PRE_GEN_11_PLATFORMS + GEN_11_PLATFORMS
PRE_GEN_12_PLATFORMS = GEN_09_PLATFORMS + GEN_10_PLATFORMS + GEN_11_PLATFORMS + GEN_11p5_PLATFORMS
PRE_GEN_13_PLATFORMS = PRE_GEN_12_PLATFORMS + GEN_12_PLATFORMS
PRE_GEN_14_PLATFORMS = PRE_GEN_13_PLATFORMS + GEN_13_PLATFORMS
PRE_GEN_15_PLATFORMS = PRE_GEN_14_PLATFORMS + GEN_14_PLATFORMS
PRE_GEN_16_PLATFORMS = PRE_GEN_15_PLATFORMS + GEN_15_PLATFORMS
PRE_GEN_17_PLATFORMS = PRE_GEN_16_PLATFORMS + GEN_16_PLATFORMS


##
# @brief        Method to check if graphics driver(s) is/are running
# @return       status - True if graphics driver(s) is/are running or skipped verification, False otherwise
def check_gfx_drivers_running() -> bool:
    status = True
    # Skip gfx driver check
    if state_machine_manager.StateMachine().skip_gfx_driver_check is True:
        return False

    gfx_driver_info = SystemInfo().get_driver_info(SystemDriverType.GFX)
    # If not Gfx Drivers are detected
    if len(gfx_driver_info.DriverInfo) == 0:
        status = False
    else:
        # Check for Intel Gfx Drivers
        for driver in gfx_driver_info.DriverInfo:
            # Skip if it's not Intel Gfx Adapter
            if "intel" not in driver.DriverDescription.lower() or driver.Status != 'Running':
                logging.warning(f"Graphics Driver {driver.DriverDescription} is in state {driver.Status}")
                status = False

    if status is not True:
        logging.error("Gfx driver(s) is/are not running!")
    return status


##
# @brief        Method to check if valsim is running
# @return       status - True if valsim is running or skipped verification, False otherwise
def check_gfxvalsim_running():
    status = False
    # Skip valsim driver check
    if not (state_machine_manager.StateMachine().simulation_type) or state_machine_manager.StateMachine().simulation_type == 'NONE' :
        return True

    valsim_driver_info = SystemInfo().get_driver_info(SystemDriverType.VALSIM)
    # If more than one instance of ValSim  Drivers are detected
    if len(valsim_driver_info.DriverInfo) > 1:
        gdhm.report_bug(
            f"[GfxValSim] Debug : Multiple GfxValSim Driver instances installed",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )

    for driver in valsim_driver_info.DriverInfo:
        if driver.Status == 'Running':
            status = True

    if status is not True:
         logging.error("GfxValsim is not running")
    return status


##
# @brief        Driver Info Class
class DriverInfo:

    ##
    # @brief    Constructor
    def __init__(self):
        self.DriverInf = 'None'
        self.DriverDescription = 'None'
        self.DriverVersion = 'None'
        self.Status = 'Unknown'
        self.BusDeviceID = 'None'
        self.VendorID = 'None'
        self.DeviceID = 'None'
        self.DeviceInstanceID = 'None'
        self.GfxIndex = 'None'
        self.IsActive = False


##
# @brief        EnumeratedDrivers class
class EnumeratedDrivers:

    ##
    # @brief    Constructor
    def __init__(self):
        self.DriverInfo = list()  # Connected display driver info list
        self.Count = 0  # No of connected display drivers

    ##
    # @brief    Overridden str method
    # @return       None
    def __str__(self):
        return f"DriverInfo count {self.Count}: {self.DriverInfo}"


##
# @brief        GfxDisplayHardwareInfo Structure
class GfxDisplayHardwareInfo(ctypes.Structure):
    _fields_ = [
        ('NumberOfDisplayAdapter', ctypes.c_uint),
        ('DisplayAdapterName', ctypes.c_wchar_p),  # Platform Name
        ('VendorID', ctypes.c_wchar * 6),  # GFX Adapter Vendor ID
        ('DeviceID', ctypes.c_wchar * 6),  # GFX Adapter Device ID
        ('DeviceInstanceID', ctypes.c_wchar * MAX_DEVICE_ID_LEN),  # GFX Adapter Instance ID
        ('RevisionID', ctypes.c_wchar_p),  # GFX Adapter Revision ID
        ('SkuName', ctypes.c_wchar_p),
        ('SkuConfig', ctypes.c_wchar_p),
        ('gfxIndex', ctypes.c_wchar * 6)
    ]


##
# @brief        Structure Definition for OS Information
class OSInfo(ctypes.Structure):
    _fields_ = [
        ('OSName', ctypes.c_wchar_p),
        ('OSCaption', ctypes.c_wchar_p),
        ('OSArchitecture', ctypes.c_wchar_p),
        ('MajorVersion', ctypes.c_wchar_p),
        ('MinorVersion', ctypes.c_wchar_p),
        ('BuildNumber', ctypes.c_wchar_p),
        ('BuildRevisionNumber', ctypes.c_wchar_p)

    ]


##
# @brief        Structure Definition to Get System Information.
class SystemInformation(ctypes.Structure):
    _fields_ = [
        ('ComputerName', ctypes.c_wchar_p),
        ('CpuInfo', ctypes.c_wchar_p),
        ('BIOSVersion', ctypes.c_wchar_p),
        ('BIOSManufacturer', ctypes.c_wchar_p),
        ('OSInfo', OSInfo)
    ]


##
# @brief        Structure Definition for Platform Information
class PlatformInfo(ctypes.Structure):
    _fields_ = [
        ('DeviceID', ctypes.c_wchar * 6),  # GFX Adapter Device ID
        ('PlatformName', ctypes.c_wchar_p),  # Platform Name
        ('SkuName', ctypes.c_wchar_p),  # SKU Name
        ('SkuConfig', ctypes.c_wchar_p)  # SKU Configuration
    ]


##
# @brief        Structure Definition for Audio Controller Information
class DisplayAudioDeviceInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('controller_busDeviceID', ctypes.c_wchar * MAX_DEVICE_ID_LEN),
        ('controller_vendorID', ctypes.c_wchar * 6),
        ('controller_deviceID', ctypes.c_wchar * 6),
        ('controller_deviceInstanceID', ctypes.c_wchar * MAX_DEVICE_ID_LEN),
        ('gfxIndex', ctypes.c_wchar * 6),
        ('isActive', ctypes.c_bool)
    ]

    ##
    # @brief        Overridden str function
    # @return       None
    def __str__(self):
        return ("Controller_DeviceID: " + self.controller_busDeviceID + " Controller_DeviceID: " +
                self.controller_deviceID + " Controller_GfxIndex: " + self.gfxIndex)


##
# @brief        Structure Definition for Audio Controller Information
class DisplayAudioDevices(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('numAudioController', ctypes.c_uint),
        ('displayAudioInfo', DisplayAudioDeviceInfo * MAX_SUPPORTED_ADAPTERS),
        ('status', ctypes.c_uint)
    ]

    ##
    # @brief        get_controller_details - Fetches audio controller adapter details
    # @param[in]    gfx_index - graphics adapter index
    # @return       Audio controller adapter details
    def get_controller_details(self, gfx_index):
        for i in range(self.numAudioController):
            if self.displayAudioInfo[i].gfxIndex == gfx_index:
                return self.displayAudioInfo[i]

    ##
    # @brief    Overridden str method
    # @return       None
    def __str__(self):
        output_str = ""
        for index in range(self.numAudioController):
            output_str += "Controller ({0}/{1}) ".format(index + 1, self.numAudioController)
            output_str += "[Controller_DeviceID: " + self.displayAudioInfo[index].controller_busDeviceID
            output_str += " Controller_DeviceID: " + self.displayAudioInfo[index].controller_deviceID
            output_str += " Controller_GfxIndex: " + self.displayAudioInfo[index].gfxIndex + "]\n"
        return output_str


##
# @brief        RAM Bank Class
class RamBank(object):
    Capacity = ""
    BankLabel = ""

    ##
    # @brief    Overridden str method
    # @return   str - String representation of RAM details
    def __str__(self):
        module_fields = {key: value for key, value in self.__dict__.items() if not (key.startswith('__'))}
        return str(module_fields)


##
# @brief        This function is used  to format the input string and saving as a dictionary
# @param[in]    input_str - Input String to be parsed
# @return       output_list - List of formatted dictionary
def parse_info(input_str):
    output_list = []
    output_dict = dict()

    for line in input_str.splitlines():
        if ":" in line:
            row = line.split(":", 1)
            if len(row) == 2:
                key = row[0].strip()
                value = row[1].strip()

                if key in output_dict.keys():
                    output_list.append(output_dict)
                    output_dict = dict()

                output_dict[key] = value
    if len(output_dict.keys()):
        output_list.append(output_dict)
    return output_list


##
# @brief        Helper function to read dictionary value from key if key is present
# @param[in]    obj - input dictionary
# @param[in]    key - search key element from dictionary
# @param[in]    default_val - dumps this data into return variable if key is not present in given dictionary
# @return       value - Returns value from given key if present, else returns default_val
def get_dict_value(obj: Dict[str, str], key: str, default_val: str) -> Any:
    value = default_val
    if isinstance(obj, dict) and key in obj.keys():
        value = obj[key]
    return value


##
# @brief        SystemDriverType class
class SystemDriverType(Enum):
    VALSIM = "SYSTEM"
    GFX = "DISPLAY"
    AUDIO = "MEDIA"


##
# @brief        SystemInfo Class
@singleton
class SystemInfo(object):
    sys_info = SystemInformation()
    audio_device_info = DisplayAudioDevices()

    ##
    # @brief        SystemInfo Constructor
    def __init__(self):
        self.os_info = None
        self.gfx_display_hardware_info_list = None
        self.driver_info = None

    ##
    # @brief        Overridden str method
    # @return       info - String representation of SystemInfo class
    def __str__(self):
        info = "Machine Name : %s \n" % self.sys_info.ComputerName
        info += "CPU and Stepping  : %s \n" % self.sys_info.CpuInfo
        info += "OS   : %s, [Build %s] \n" % (self.os_info.OSName, self.os_info.BuildNumber)
        info += "BIOS : %s, %s \n" % (self.sys_info.BIOSManufacturer, self.sys_info.BIOSVersion)
        return info

    ##
    # @brief        This function is used  to format and print machine information in display_logger.py API
    # @return       formatted_line - List of formatted lines
    def __format_print_machine_info(self):
        formatted_line = []
        fmt_line = "{0:^25}: {1}".format("Machine Name", self.sys_info.ComputerName)
        formatted_line.append(fmt_line)

        fmt_line = "{0:^25}: {1}".format("CPU and Stepping", self.sys_info.CpuInfo)
        formatted_line.append(fmt_line)

        fmt_line = "{0:^25}: {1}, [Build {2}]".format("OS", self.os_info.OSName, self.os_info.BuildNumber)
        formatted_line.append(fmt_line)

        fmt_line = "{0:^25}: {1}, {2}".format("BIOS", self.sys_info.BIOSManufacturer, self.sys_info.BIOSVersion)
        formatted_line.append(fmt_line)

        return formatted_line

    ##
    # @brief        This function is used to Get OS Information
    # @return       os_info - OS Info Object
    def get_os_info(self):
        if self.os_info is not None:
            return self.os_info

        self.os_info = OSInfo()
        output = subprocess.check_output(
            ['powershell.exe', "Get-WmiObject", "Win32_OperatingSystem | Format-List *"], universal_newlines=True)
        parse_os_info = parse_info(output)[0]
        self.os_info.OSCaption = parse_os_info['Caption'] if 'Caption' in parse_os_info.keys() else None
        self.os_info.OSArchitecture = parse_os_info[
            'OSArchitecture'] if 'OSArchitecture' in parse_os_info.keys() else None

        output = os.popen('ver.exe').read().replace('\n', '')
        self.os_info.OSName = output
        result = re.findall(r"\b\d+\.\d+\.\d+\.\d+\b", output)[0].split(".")
        if result and len(result) >= 4:
            self.os_info.MajorVersion = result[0]
            self.os_info.MinorVersion = result[1]
            self.os_info.BuildNumber = result[2]
            self.os_info.BuildRevisionNumber = result[3]
        return self.os_info

    def __get_bios_info(self):
        bios_info_out = subprocess.run(['powershell.exe', "Get-WmiObject", "Win32_bios"], universal_newlines=True,
                                       capture_output=True)
        if bios_info_out.returncode != 0:
            self.sys_info.BIOSVersion = "NA"
            self.sys_info.BIOSManufacturer = "NA"
            return

        parsed_bios_data = parse_info(bios_info_out.stdout)
        bios_info = parsed_bios_data[0] if parsed_bios_data is not None and len(parsed_bios_data) > 0 else None
        smbios_version = get_dict_value(bios_info, "SMBIOSBIOSVersion", "NA")
        bios_version = get_dict_value(bios_info, "Version", "NA")
        self.sys_info.BIOSVersion = (smbios_version + " [" + bios_version + "]")
        self.sys_info.BIOSManufacturer = get_dict_value(bios_info, "Manufacturer", "NA")

    ##
    # @brief        Get System Information
    # @return       str - Printable Machine info
    def _get_system_info(self):
        self.get_os_info()

        self.sys_info.ComputerName = platform.node()
        self.sys_info.CpuInfo = platform.processor()
        self.__get_bios_info()

        return self.__format_print_machine_info()

    ##
    # @brief        Get Graphics Display Hardware Information
    # @return       gfx_display_hardware_info_list - List of GFX DisplayHarwareInfo Structure to support 'N' Adapter's
    def get_gfx_display_hardwareinfo(self):
        if self.gfx_display_hardware_info_list is not None:
            return self.gfx_display_hardware_info_list

        self.gfx_display_hardware_info_list = []
        from Libs.Core.display_config.display_config import DisplayConfiguration
        display_config = DisplayConfiguration()
        gfx_adapter_details = display_config.get_all_gfx_adapter_details()

        for adapter_count in range(gfx_adapter_details.numDisplayAdapter):
            display_hardware_info = GfxDisplayHardwareInfo()
            platform_info = self.get_platform_details(gfx_adapter_details.adapterInfo[adapter_count].deviceID)
            display_hardware_info.NumberOfDisplayAdapter = gfx_adapter_details.numDisplayAdapter
            display_hardware_info.DisplayAdapterName = platform_info.PlatformName
            display_hardware_info.SkuName = platform_info.SkuName
            display_hardware_info.SkuConfig = platform_info.SkuConfig
            display_hardware_info.VendorID = gfx_adapter_details.adapterInfo[adapter_count].vendorID
            display_hardware_info.DeviceID = gfx_adapter_details.adapterInfo[adapter_count].deviceID
            display_hardware_info.DeviceInstanceID = gfx_adapter_details.adapterInfo[adapter_count].deviceInstanceID
            display_hardware_info.gfxIndex = gfx_adapter_details.adapterInfo[adapter_count].gfxIndex
            # display_hardware_info.RevisionID = gfx_adapter_details.adapterInfo[adapter_count].revisionID
            self.gfx_display_hardware_info_list.append(display_hardware_info)
        return self.gfx_display_hardware_info_list

    ##
    # @brief        function to parse and get platform details based on device ID
    # @param[in]    platform_device_id - Device ID
    # @return       platform_info - Platform info Object
    def get_platform_details(self, platform_device_id):
        platform_device_id = str(platform_device_id).upper()
        global PLATFORM_INFO_DICT
        if len(PLATFORM_INFO_DICT):
            for key, value in PLATFORM_INFO_DICT.items():
                if key == platform_device_id:
                    return value
        platform_info = PlatformInfo()
        platform_found = False
        script_path = os.path.dirname(os.path.realpath(__file__))
        map_input_file = os.path.join(script_path, "platform_ids.xml")
        try:
            xml_root = Et.parse(map_input_file).getroot()
            product_family = xml_root.findall('Product_Family')
            for product_family_list in product_family:
                family_name = product_family_list.attrib['FamilyName']
                device_id_list = product_family_list.findall('Device_ID_list')
                for device_id in device_id_list:
                    device_tag = device_id.findall('Device_ID')
                    for device_tag_item in device_tag:
                        dev2_id = device_tag_item.attrib['Dev2_ID']
                        if platform_device_id == dev2_id.upper():
                            platform_found = True
                            platform_info.DeviceID = platform_device_id
                            platform_info.PlatformName = family_name
                            platform_info.SkuName = device_tag_item.attrib['SKU_Name']
                            platform_info.SkuConfig = device_tag_item.attrib['Config']
                            PLATFORM_INFO_DICT[platform_device_id] = platform_info
                            return platform_info
            if platform_found is False:
                logging.error("FAIL: Platform Id {0} not found in XML".format(platform_device_id))
                platform_info.DeviceID = platform_device_id
                platform_info.PlatformName = 'Platform_None'.encode('utf-8')
                platform_info.SkuName = None
                platform_info.SkuConfig = None
                PLATFORM_INFO_DICT[platform_device_id] = platform_info
                return platform_info
        except Exception as ex:
            logging.error("FAIL:{0} Parsing FAILED".format(map_input_file))

    ##
    # @brief        API to Get Driver Information
    # @param[in]    driver_type - SystemDriverType enum
    # @return       driver_info - EnumeratedDrivers object
    def get_driver_info(self, driver_type: SystemDriverType) -> EnumeratedDrivers:
        driver_info = None
        driver_path, driver_name = self.__get_driver_class_list(driver_type.value)
        if driver_path is not None:
            if driver_type == SystemDriverType.VALSIM:
                driver_count = len(driver_path)
                valsim_driver_path = []
                valsim_driver_name = []
                for count in range(driver_count):
                    if 'Gfx Val Simulation Driver' in driver_name[count]:
                        valsim_found = True
                        valsim_driver_path.append(driver_path[count])
                        valsim_driver_name.append(driver_name[count])
                driver_path, driver_name = valsim_driver_path, valsim_driver_name
            driver_info = self.__get_driver_details(driver_path)
            if driver_type == SystemDriverType.GFX:
                for i in range(driver_info.Count):
                    self.__bus_device_id_split(driver_info.DriverInfo[i])
        return driver_info

    ##
    # @brief        Retrieves device driver_path and driver_name
    # @param[in]    device - name (Ex: Display for Gfx Adapter, Media for Audio and System for system devices)
    # @return       (driver_path, driver_name) - (Driver file path, Driver file name)
    def __get_driver_class_list(self, device):
        cmd = f"pnputil /enum-devices /class {device} | Where-Object {{ $_ -match 'Instance ID|Device Description|Status' }}"
        list_driver_class = subprocess.run(["powershell", "-Command", cmd],
                                           capture_output=True)
        if list_driver_class.returncode != 0:
            list_driver_stderr = list_driver_class.stderr.decode().replace('\r\n', ' | ')
            logging.error(f"Error while fetching list of drivers: {list_driver_stderr}")
            return None, None

        list_driver_stdout = list_driver_class.stdout.decode('utf-8','ignore')
        if not (list_driver_stdout):
            return None, None
        list_driver_stdout = list_driver_stdout.split('\r\n')
        driver_path = []
        driver_name = []

        for i in range(len(list_driver_stdout)):
            if list_driver_stdout[i].startswith('Instance ID:'):
                instance_id = list_driver_stdout[i].split(':')[-1].strip()
            elif list_driver_stdout[i].startswith('Device Description:'):
                device_desc = list_driver_stdout[i].split(':')[-1].strip()
            elif list_driver_stdout[i].startswith('Status:'):
                status = list_driver_stdout[i].split(':')[-1].strip()
                if status in ['Started', 'Stopped', 'Disabled']:
                    driver_path.append(instance_id)
                    driver_name.append(device_desc)
        if len(driver_path) == 0:
            return None, None
        return driver_path, driver_name

    ##
    # @brief        Retrieves driver's running status, DriverVersion, driver_path, DriverDescription, Etc..,
    # @param[in]    driver_path - Device Instance path (Device Instance path , Ex : ROOT\\SYSTEM\\0002)
    # @return       enum_drivers -  Object of type EnumeratedDrivers
    def __get_driver_details(self, driver_path):
        enum_drivers = EnumeratedDrivers()
        enum_drivers.Count = len(driver_path)
        for count in range(enum_drivers.Count):
            driver_info = DriverInfo()
            try:
                query_driver = driver_path[count].replace('\\\\', '\\')
                cmd_get_driver_info = f"pnputil /enum-devices /instanceid '{query_driver}'"
                driver_info_output = subprocess.run(["powershell", "-Command", cmd_get_driver_info],
                                                    capture_output=True)
                if driver_info_output.returncode != 0:
                    driver_info_stderr = driver_info_output.stderr.decode('utf-8', 'ignore').replace('\r\n', ' | ')
                    logging.error(f"Error fetching driver details {driver_info_stderr}")

                driver_info_stdout = driver_info_output.stdout.decode('utf-8', 'ignore').split("\r\n")
                driver_class = driver_info_stdout[5].split(":")[-1].strip()

                cmd_get_driver_version = f"pnputil /enum-drivers /class '{driver_class}'"
                driver_version_output = subprocess.run(["powershell", "-Command", cmd_get_driver_version],
                                                       capture_output=True)
                if driver_version_output.returncode != 0:
                    driver_version_stderr = driver_version_output.stderr.decode('utf-8', 'ignore').replace('\r\n',
                                                                                                           ' | ')
                    logging.error(f"Error fetching driver version {driver_version_stderr}")

                driver_version_stdout = driver_version_output.stdout.decode('utf-8', 'ignore').split("\r\n")
                driver_info.BusDeviceID = driver_info_stdout[2].split(":")[-1].strip()
                driver_info.DriverDescription = driver_info_stdout[3].split(":")[-1].strip()
                if driver_info_stdout[7].split(":")[-1].strip() == "Started":
                    driver_info.Status = "Running"
                else:
                    driver_info.Status = "Offline"
                inf = driver_info_stdout[8].split(":")[-1].strip()
                driver_info.DriverInf = os.path.join(r"C:\Windows\INF", inf)
                index_driver_version = driver_version_stdout.index(next(
                    driver_instance for driver_instance in driver_version_stdout if
                    inf in driver_instance))
                driver_info.DriverVersion = driver_version_stdout[index_driver_version + 5].split(":")[-1].split(" ")[1]

            except (WindowsError, StopIteration) as e:
                logging.error(f"Error while parsing the commandline - {e}")
            except Exception as exception:
                logging.error(exception)
            enum_drivers.DriverInfo.append(driver_info)
        return enum_drivers

    ##
    # @brief        Split the Gfx Display Device Instance Path and save into DriverInfo Structure
    # @param[in]    driver_info - DriverInfo Structure.
    # @return       None
    @staticmethod
    def __bus_device_id_split(driver_info):
        match_token = re.match(
            r'(?P<bus_id>[\w]+\\([\w&])*VEN_+(?P<vendor>[\w]+)&DEV_(?P<device>[\w]+)&([\w&]+))\\('
            r'?P<device_instance>.+)', driver_info.BusDeviceID)
        driver_info.BusDeviceID = match_token.group('bus_id')
        driver_info.VendorID = match_token.group('vendor')
        driver_info.DeviceID = match_token.group('device')
        driver_info.DeviceInstanceID = match_token.group('device_instance')
        driver_info.IsActive = False if driver_info.Status != "Running" else True

    ##
    # @brief        get_audio_adapter_info - This function gets the audio controller type
    # @param[in]    presi - if pre-si (True/False)
    # @return        audio_device_info - object of DisplayAudioDevices
    def get_audio_adapter_info(self, presi=False):
        self.audio_device_info.status = False
        gfx_parent_info_dict = {}
        get_parent_cmd = "powershell \"Get-PnpDeviceProperty -InstanceId '{0}' -KeyName 'DEVPKEY_Device_Parent' | Format-List -Property Data\""

        from Libs.Core.display_config.display_config import DisplayConfiguration
        gfx_adapter_info = DisplayConfiguration().get_all_gfx_adapter_details()

        cmd = "pnputil /enum-devices /class system | Where-Object {$_ -match 'Instance ID|Device Description|Status'}"
        ven_8086_devices = subprocess.run(["powershell", "-Command", cmd], capture_output=True)

        if ven_8086_devices.returncode != 0:
            ven_8086_devices_stderr = ven_8086_devices.stderr.decode('utf-8', 'ignore').replace('\r\n', ' | ')
            logging.error("\tUnable to get the audio controller type: %s", ven_8086_devices_stderr)
            return
        ven_8086_devices_stdout = ven_8086_devices.stdout.decode('utf-8', 'ignore')
        if not (ven_8086_devices_stdout):
            logging.error("\tUnable to get the audio controller type")
            return
        # Find Parent information for all display adapters
        for index in range(gfx_adapter_info.numDisplayAdapter):
            gfx_instance_id = "{0}\\{1}".format(gfx_adapter_info.adapterInfo[index].busDeviceID,
                                                gfx_adapter_info.adapterInfo[index].deviceInstanceID)
            gfx_output = subprocess.check_output(get_parent_cmd.format(gfx_instance_id), universal_newlines=True)
            gfx_parent_id = gfx_output.strip().split(':')[1].strip()
            device_id = gfx_adapter_info.adapterInfo[index].deviceID

            # @todo: Temporary fix to fetch parent of audio controller in ARL-S.
            if self.get_sku_name('gfx_0') == "ARL" and device_id == "7D67":
                gfx_parent_id = "ACPI\\PNP0A08\\2"
            else:
                if gfx_parent_id.startswith("PCI"):
                    gfx_parent_id_result = subprocess.run(get_parent_cmd.format(gfx_parent_id), capture_output=True,
                                                          text=True, check=False )
                    if gfx_parent_id_result.returncode > 0:
                        logging.error(f"\tReturn code is {gfx_parent_id_result.returncode} for Command:{' '.join(get_parent_cmd.format(gfx_parent_id))} Error:{gfx_parent_id_result.stderr}")
                    gfx_parent_id= gfx_parent_id_result.stdout

                    if gfx_parent_id.startswith("PCI"):
                        gfx_parent_id = gfx_output.strip().split(':')[1].strip()
                        gfx_parent_id = gfx_parent_id.split("&SUBSYS")[0]
            gfx_parent_info_dict[gfx_adapter_info.adapterInfo[index].gfxIndex] = gfx_parent_id

        controller_index = 0
        ven_8086_devices_stdout = ven_8086_devices_stdout.split('\r\n')

        for i in range(len(ven_8086_devices_stdout)):
            ms_controller = re.search(r'High Definition Audio Controller', ven_8086_devices_stdout[i], re.I)
            intel_controller = re.search(r'Smart Sound Technology', ven_8086_devices_stdout[i], re.I)
            if ms_controller or intel_controller:
                audio_instance_id = ven_8086_devices_stdout[i - 1].split(":")[-1].strip()
                status = ven_8086_devices_stdout[i + 1].split(":")[-1].strip()
                if status == "Disconnected":
                    continue
                if audio_instance_id.startswith("PCI"):
                    output = subprocess.check_output(get_parent_cmd.format(audio_instance_id),
                                                     universal_newlines=True)
                    audio_parent_id = output.strip().split(':')[1].strip()
                    if audio_parent_id.startswith("PCI"):
                        audio_parent_id_result = subprocess.run(get_parent_cmd.format(audio_parent_id), capture_output=True,
                                                              text=True, check=False)
                        if (audio_parent_id_result.returncode > 0):
                            logging.error(f"\tReturn code is {audio_parent_id_result.returncode} for Command:{' '.join(get_parent_cmd.format(audio_parent_id))} Error:{audio_parent_id_result.stderr}")
                        audio_parent_id = audio_parent_id_result.stdout

                        if audio_parent_id.startswith("PCI"):
                            audio_parent_parent_id = output.strip().split(':')[1].strip()
                            audio_parent_parent_id = audio_parent_id.split("&SUBSYS")[0]
                    audio_device_id = re.findall(r"&DEV_(\S+)&SUB", audio_instance_id, re.IGNORECASE)[0]
                    audio_vendor_id = re.findall(r"VEN_(\S+)&DEV", audio_instance_id, re.IGNORECASE)[0]
                    audio_dev_ins = audio_instance_id.split('\\')[-1]
                    audio_bus_id = audio_instance_id.split("\\" + audio_dev_ins)[0]

                    gfx_index_match = [key for key in gfx_parent_info_dict if
                                       gfx_parent_info_dict[key] == audio_parent_id]
                    # TODO: Need to check for 2 DG cards connected
                    if len(gfx_index_match) != 1:
                        logging.error(f"Unable to find parent ID for {audio_device_id}")
                        continue

                    self.audio_device_info.displayAudioInfo[
                        controller_index].controller_busDeviceID = audio_bus_id
                    self.audio_device_info.displayAudioInfo[
                        controller_index].controller_vendorID = audio_vendor_id
                    self.audio_device_info.displayAudioInfo[
                        controller_index].controller_deviceID = audio_device_id
                    self.audio_device_info.displayAudioInfo[
                        controller_index].controller_deviceInstanceID = audio_dev_ins
                    self.audio_device_info.displayAudioInfo[controller_index].gfxIndex = gfx_index_match[0]

                    controller_index += 1

        self.audio_device_info.numAudioController = controller_index

        # Verify Audio Controller is loaded for all Adapters
        if self.audio_device_info.numAudioController == gfx_adapter_info.numDisplayAdapter:
            self.audio_device_info.status = True
        else:
            if presi is False:
                logging.error("Audio Controller Count Expected: {0} Actual: {1}".format(
                    gfx_adapter_info.numDisplayAdapter, self.audio_device_info.numAudioController))
                self.audio_device_info.status = False
        return self.audio_device_info

    ##
    # @brief        Helper function to get the platform SKU Name.
    # @param[in]    gfx_index: str
    #                   Graphics Adapter index for which SKU Name is required. E.g. "gfx_0"
    # @return       sku_name: str
    #                   Name of the SKU in caps. For E.g. "ACMP"
    @staticmethod
    def get_sku_name(gfx_index: str) -> str:
        sku_name = "None"

        disp_hw_info = SystemInfo().get_gfx_display_hardwareinfo()
        if len(disp_hw_info) <= int(gfx_index[-1]):
            logging.error(f'{gfx_index} not available in enumerated adapters')
            return sku_name
        sku_name = disp_hw_info[int(gfx_index[-1])].SkuName

        return sku_name

    ##
    # @brief        Get CPU brand information
    # @details      Takes input of Cpuid.exe custom exe present in SharedBinary folder for fetching CPU details
    # @return       str - Returns CPU brand string for graphics adapter
    @staticmethod
    def get_cpu_brand_string() -> str:
        cpu_id_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "Applications", "Cpuid.exe")
        output = subprocess.run([cpu_id_path], capture_output=True)
        stdout = output.stdout.decode().replace("\n", " ")
        stderr = output.stderr.decode().replace("\n", " ")
        logging.debug(f"Output = {stdout}, Error = {stderr}")
        if output.returncode != 0:
            return stdout if stdout is not None or stdout != "" else stderr
        return stdout
