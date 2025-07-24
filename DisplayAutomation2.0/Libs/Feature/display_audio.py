################################################################################################################################
# @file            display_audio.py
# @brief           Python wrapper exposes interfaces to CodecAudio DLL and contains common functions
#                  used for audio endpoint and audio playback verification
# @details         Contains all functions which is used to verify audio driver, controller, power states of
#                  codec/controller, sgpc status and also checks if a panel is audio capable
# @author          Sridharan V, Rohit Kumar, Ravichandran M
################################################################################################################################

import ctypes
import logging
import os
import re
import subprocess
import time
import json
from enum import IntEnum

import DisplayRegs
from DisplayRegs.DisplayOffsets import TransDDiOffsetsValues
from Libs.Core import display_utility, driver_escape, registry_access
from Libs.Core import enum as custom_enum
from Libs.Core import system_utility as sys_utility
from Libs.Core.core_base import singleton
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature.display_engine.de_base import display_base
from Libs.Core.display_config import adapter_info_struct as adapter_struct
from Libs.Core.Verifier.common_verification_args import VerifierCfg
from DisplayRegs.DisplayOffsets import AudDP2CtlOffsets
from DisplayRegs import DisplayArgs, DisplayRegsService

AUDIO_PIN = 0x650c0
PWR_CONTROL = 0x45404

BIT_MASK_AUDIO_PIN = 0x00000005  # For Mainline Driver
BIT_MASK_AUDIO_PIN_DDRW = 0x00000005  # For Yangra Driver
BIT_MASK_POWER_WELL_2 = 0x40000000  # Gen 9 and Gen 10 use power well 2
BIT_MASK_POWER_WELL_3 = 0x00000010  # ICL onwards power well 3 is used
MAX_NUM_ENDPOINTS_GEN_9 = 3  # Gen 10 also has maximum 3 audio endpoints
MAX_NUM_ENDPOINTS_GEN_11 = 4  # ICLHP and TGL support maximum 4 endpoints
MAX_NUM_AUDIO_END_POINTS = 10
MAX_ENDPOINT_NAME_LENGTH = 128

HARDWARE_ID_INTEL_AUDIO = "INTELAUDIO*FUNC_01&VEN_8086*"
HARDWARE_ID_HD_AUDIO = "HDAUDIO*FUNC_01&VEN_8086*"

DEVCON_EXE_PATH = test_context.TestContext.devcon_path()
CERT_INSTALL_PATH = os.path.join(test_context.COMMON_BIN_FOLDER, "CertificateInstall.exe")

# @brief Default path for graphics driver files
DRIVER_PATH = "C:\Driver\Gfxinstaller"

# @brief Audio driver install or uninstall operation timeout value in seconds
AUDIO_DRIVER_INSTALL_UNINSTALL_TIMEOUT = 30

MAX_CHANNELS = 8
MAX_GFX_ADAPTER = 5
MAX_DEVICE_ID_LEN = 200

SGPC_MAPPING = {
    'RKL': True,
    'ADLS': True,
    'DG2': False,
    'ADLP': False,
    'MTL': True,
    'LNL': True,
    'ELG': False
}


##
# @brief Structure Definition for Audio Format and Used for Audio Property Page Verification Test Cases.
class AudioFormat(ctypes.Structure):
    _fields_ = [('pFormatName', ctypes.c_char_p),
                ('SampleRate', ctypes.c_uint),
                ('BitDepth', ctypes.c_uint)]


##
# @brief Structure Definition for Audio Endpoints Information
class AudioEndpointsInformation(ctypes.Structure):
    _fields_ = [('Size', ctypes.c_uint),
                ('NumFormats', ctypes.c_uint),
                ('MaxNumberOfChannels', ctypes.c_uint),
                ('AudFormat', AudioFormat * 315)]


##
# @brief Structure Definition for Codec Configuration
class CodecConfig(ctypes.Structure):
    _fields_ = [('size', ctypes.c_int),
                ('outputDevice', ctypes.c_wchar_p),
                ('numberOfChannels', ctypes.c_int),
                ('toneDuration', ctypes.c_int),
                ('sampleRate', ctypes.c_int),
                ('bitDepth', ctypes.c_int),
                ('amplitude', ctypes.c_double),
                ('audioFormat', ctypes.c_wchar_p),
                ('toneFrequency', (ctypes.c_int * 8))
                ]


##
# @brief Structure Definition for Codec PlayAndVerify Output
class ErrorInfo(ctypes.Structure):
    _fields_ = [('size', ctypes.c_int),
                ('api', ctypes.c_wchar_p),
                ('error', ctypes.c_wchar_p)
                ]


##
# @brief Structure Definition for Codec PlayAndVerify Output
class AudioEndpointNameInfo(ctypes.Structure):
    _fields_ = [('formfactor', ctypes.c_uint),
                ('endpoint_name', ctypes.c_wchar * MAX_ENDPOINT_NAME_LENGTH)
                ]


##
# @brief Structure Definition for Codec PlayAndVerify Output
class AudioEndpointName(ctypes.Structure):
    _fields_ = [('count', ctypes.c_int),
                ('endpoint_info', MAX_NUM_AUDIO_END_POINTS * AudioEndpointNameInfo)
                ]

##
# @brief Enum for Audio Codec Driver Type
class AudioCodecDriverType(IntEnum):
    NONE = 0
    INTEL = 1
    MS = 2
    ACX = 3


##
# @brief Enum for Audio Controller Type
class AudioControllerType(IntEnum):
    NONE = 0
    INTEL = 1
    MS = 2


##
# @brief Enum for Audio Codec/Controller Power State
class AudioPowerState(IntEnum):
    UNSPECIFIED = 0
    D0 = 1
    D1 = 2
    D2 = 3
    D3 = 4


##
# @brief Enum for Audio Codec/Controller Power State
class AudioEndpointFormFactor(IntEnum):
    REMOTE_NETWORK_DEVICE = 0
    SPEAKERS = 1
    LINE_LEVEL = 2
    HEADPHONES = 3
    MICROPHONES = 4
    HEADSET = 5
    HANDSET = 6
    UNKNOWN_DIGITAL_PASS_THROUGH = 7
    SPDIF = 8
    DIGITAL_AUDIO_DISPLAY_DEVICE = 9
    UNKNOWN_FORM_FACTOR = 10


@singleton
##
# @class DisplayAudio
# @brief Display Audio support
class DisplayAudio(object):
    power_well_bit = 30
    is_log_enabled = True
    supported_sample_rates = [32000, 44100, 48000, 88200, 96000, 176400, 192000]
    supported_channels = [2, 4, 6, 8]
    supported_bit_depths = [16, 20, 24, 32]
    supported_audio_formats = ["LPCM"]
    non_acx_platforms = ['CFL', 'KBL', 'SKL', 'GLK', 'ICLLP', 'EHL', 'LKF1']
    system_utility = sys_utility.SystemUtility()
    driver_interface_ = driver_interface.DriverInterface()
    controller_adapter = None
    audio_codec_name = None
    audio_controller_name = None
    codec_id = None

    ##
    # @brief This function will load the CodecAudio.dll
    def __init__(self):
        # Load DisplayAudio C library
        self.displayAudioCodecDll = ctypes.cdll.LoadLibrary(os.path.join(test_context.TestContext.bin_store(),
                                                                         'DisplayAudioCodec.dll'))
        self.audio_device_id_json = os.path.join(test_context.ROOT_FOLDER, 'Libs', 'Feature',
                                                 'Audio_Codec_Controller_IDs.json')
        self.display_config = DisplayConfiguration()
        self.platform = None
        self.current_display_config = None

        # Controller will not get loaded in case of pre-si due to PCH, hence skipping the call
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        # Added only for presi check in VP/PSS platforms as Audio controller will not be enumerated in generic presi platforms
        for gfx_index in adapter_dict.keys():
            platform = SystemInfo().get_platform_details(adapter_dict[gfx_index].deviceID).PlatformName
        if self.system_utility.get_execution_environment_type() in ["SIMENV_FULSIM"]:
            if platform in ['MTL']:
                self.controller_adapter = SystemInfo().get_audio_adapter_info(presi=True)
        else:
            if self.system_utility.get_execution_environment_type() not in ["SIMENV_FULSIM"]:
                self.controller_adapter = SystemInfo().get_audio_adapter_info()

        prototype = ctypes.PYFUNCTYPE(ctypes.c_long)
        func = prototype(('CreateEnumerator', self.displayAudioCodecDll))
        result = func()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_long)
        func = prototype(('CreateAndRegisterNotificationClient', self.displayAudioCodecDll))
        result = func()

    ##
    # @brief This function will unload the CodecAudio.dll
    def __del__(self):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_long)
        func = prototype(('DestroyEnumerator', self.displayAudioCodecDll))
        result = func()

    ##
    # @brief        Get the audio device ID from JSON file
    # @param[in]    platform - Platform Name
    # @return       Dictionary with Controller and Codec ID list
    def get_audio_device_id_from_json(self, platform):
        ret_dict = {"controller": [], "codec": []}
        with open(self.audio_device_id_json) as js_handle:
            json_data = json.load(js_handle)

        if (json_data is not None) and (platform in json_data.keys()):
            return json_data[platform]
        else:
            return ret_dict

    ##
    # @brief        Get the installed audio codec driver
    # @param[in]    gfx_index - Graphics adapter index
    # @return       AudioCodecDriverType (INTEL or MS or No Audio Codec)
    def get_audio_driver(self, gfx_index='gfx_0'):
        audio_codec_driver = AudioCodecDriverType.NONE
        # If environment is Pre-Silicon, No Audio Codec driver will be loaded
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        platform_information = SystemInfo().get_platform_details(adapter_dict[gfx_index].deviceID)
        # Added only for presi check in VP/PSS platforms as Audio controller will not be enumerated in generic presi platforms
        if platform_information.PlatformName not in ['MTL']:
            if self.system_utility.get_execution_environment_type() in ["SIMENV_FULSIM"]:
                return audio_codec_driver
        # Codec device ID will differ for JSL and EHL. Since based on SKU name update the platform name as EHL.
        if platform_information.PlatformName == "JSL" and platform_information.SkuName == "EHL":
            platform_name = 'EHL'
        else:
            platform_name = platform_information.PlatformName
        device_id_dict = self.get_audio_device_id_from_json(platform_name)
        logging.debug("CodecID retrieved from JSON for {0} = {1}".format(platform_name, device_id_dict['codec']))
        # Adding Hard sleep time since test is failing sporadically due to codec is taking ~3 extra sec to load
        time.sleep(5)
        for self.codec_id in device_id_dict['codec']:
            intel_audio_codec_id = "{0}&DEV_{1}*".format(HARDWARE_ID_INTEL_AUDIO[:-1], self.codec_id)
            hd_audio_codec_id = "{0}&DEV_{1}*".format(HARDWARE_ID_HD_AUDIO[:-1], self.codec_id)

            try:
                # Get the audio codec driver status
                driver_status_output = subprocess.check_output([DEVCON_EXE_PATH, "status", "=media",
                                                                intel_audio_codec_id], universal_newlines=True)

                if re.search(r'No matching devices found.', driver_status_output, re.I):
                    driver_status_output = subprocess.check_output([DEVCON_EXE_PATH, "status", "=media",
                                                                    hd_audio_codec_id], universal_newlines=True)
            except Exception as e:
                logging.warning(e)
                raise e

            if re.search(r'No matching devices found.', driver_status_output, re.I):
                logging.debug("No Audio Codec loaded with CodecDevice ID {0}".format(self.codec_id))
                continue
            else:
                # Check the output string for Intel/MS audio driver
                intel_driver_status = re.search(r'Intel', driver_status_output, re.I)
                ms_driver_status = re.search(r'High Definition Audio', driver_status_output, re.I)
                acx_driver_status = re.search(r'HD Audio Driver', driver_status_output, re.I)
                if acx_driver_status:
                    audio_codec_driver = AudioCodecDriverType.ACX
                elif ms_driver_status:
                    audio_codec_driver = AudioCodecDriverType.MS
                elif intel_driver_status:
                    audio_codec_driver = AudioCodecDriverType.INTEL
                else:
                    audio_codec_driver = AudioCodecDriverType.NONE
                    logging.debug("DevCon output for codec query: {0}".format(driver_status_output))
                hardware_id_1 = '*{0}*'.format(self.codec_id)
                codec_device_status = subprocess.check_output([DEVCON_EXE_PATH, "status", hardware_id_1],
                                                              universal_newlines=True)
                for name in codec_device_status.splitlines():
                    for i in name.split('\n'):
                        if ':' not in i:
                            continue
                        key, self.audio_codec_name = i.strip().split(':', 1)
                logging.debug("Audio Codec loaded with CodecDeviceID {0} = {0}".format(
                    self.codec_id, AudioCodecDriverType(audio_codec_driver).name))
                break

        return audio_codec_driver

    ##
    # @brief        Get the audio endpoints
    # @return       Number of audio endpoints
    def get_audio_endpoints(self):
        count = 0
        audio_endpoint_name = AudioEndpointName()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_long, ctypes.POINTER(AudioEndpointName))
        func = prototype(('GetAudioEndpointNames', self.displayAudioCodecDll))
        result = func(ctypes.byref(audio_endpoint_name))
        if result == 0:
            for i in range(audio_endpoint_name.count):
                if audio_endpoint_name.endpoint_info[i].formfactor == AudioEndpointFormFactor.DIGITAL_AUDIO_DISPLAY_DEVICE:
                    count += 1
        return count

    ##
    # @brief        Get the audio codec power state
    # @param[in]    present_audio_codec - INTEL or MS or ACX
    # @return       status - Audio Codec Power State (D0 or D3)
    def get_audio_codec_power_state(self, present_audio_codec=None):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_int)
        func = prototype(('GetAudioCodecPowerState', self.displayAudioCodecDll))
        status = func(present_audio_codec)
        return status

    ##
    # @brief        Get the audio controller power state
    # @param[in]    present_controller - INTEL or MS
    # @return       status - Audio controller power state (D0 or D3)
    def get_audio_controller_power_state(self, present_controller=None):
        present_controller = present_controller.strip()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_int)
        func = prototype(('GetAudioControllerPowerState', self.displayAudioCodecDll))
        status = func(present_controller)
        return status

    ##
    # @brief        To check if panel is audio capable
    # @param[in]    display_and_adapter_info - Target_id/display_and_adapter_info of the panel to be checked
    # @return       audio_support - Bool, True if panel is audio capable;False otherwise
    def is_audio_capable(self, display_and_adapter_info):
        audio_support = False
        audio_mask = 0x40
        edid_flag, display_edid, _ = driver_escape.get_edid_data(display_and_adapter_info)

        if not edid_flag:
            if type(display_and_adapter_info) is DisplayAndAdapterInfo:
                target_id = display_and_adapter_info.TargetID
            else:
                target_id = display_and_adapter_info

            gdhm.report_test_bug_audio(
                title="[Audio] Failed to get EDID data for target_id : {0}".format(target_id))
            logging.error(f"Failed to get EDID data for target_id : {target_id}")
            assert edid_flag, "Failed to get EDID data for TargetID: {0}".format(target_id)

        # EDID data 126 byte represents Extention block availability and EDID data 128 byte represnets CEA block and
        # 131 byte - 6th bit represents audio capability
        no_of_extension_blocks = display_edid[126]  # Refer's to Extension block count in BaseBlock
        if no_of_extension_blocks >= 1:
            for extension_block_index in range(1, no_of_extension_blocks + 1):
                cea_header = display_edid[(extension_block_index) * 128]
                if (cea_header == 0x02) and (
                        (display_edid[((extension_block_index) * 128) + 3] & audio_mask) == audio_mask):
                    audio_support = True
                    break
        return audio_support

    ##
    # @brief    Common interface for audio verification
    # @return   status - Bool, True if audio verification is successful; False otherwise
    def audio_verification(self):
        active_audio_displays = 0
        status = False

        # Get the audio endpoint list from OS
        no_of_endpoints_ospage = self.get_audio_endpoints()

        # Get the number of active audio displays
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if enumerated_displays.Count != 0:
            get_config = self.display_config.get_current_display_configuration()
            current_topology_str = get_config.to_string(enumerated_displays).split(' ')
            displays_str = current_topology_str[0]
        else:
            current_topology_str = ["NONE"]
            displays_str = "NONE"

        for display_index in range(enumerated_displays.Count):
            if enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                if displays_str == current_topology_str[0]:
                    displays_str += ' ' + str(
                        cfg_enum.CONNECTOR_PORT_TYPE(
                            enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
                else:
                    displays_str += '+' + str(
                        cfg_enum.CONNECTOR_PORT_TYPE(
                            enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))

                display_and_adapter_info = enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo
                if self.is_audio_capable(display_and_adapter_info):
                    active_audio_displays += 1
                    displays_str += '(Audio Capable)'
                else:
                    displays_str += '(Non Audio)'

        if active_audio_displays == no_of_endpoints_ospage:
            logging.info("\tPASS: Expected Audio Endpoints for {2}= {0} Actual= {1}".format(
                active_audio_displays, no_of_endpoints_ospage, displays_str))
            status = True
        elif self.is_log_enabled is True:
            logging.error("\tFAIL: Expected Audio Endpoints for {2}= {0} Actual= {1}".format(
                active_audio_displays, no_of_endpoints_ospage, displays_str))

        return status, active_audio_displays

    ##
    # @brief        Powerwell verification for Audio
    # @param[in]    power_well_enabled
    # @param[in]    gfx_index - Gfx Adapter index
    # @return       Bool, True is status is success; False, otherwise
    def verify_power_well(self, power_well_enabled=True, gfx_index="gfx_0"):
        pg_bit = BIT_MASK_POWER_WELL_2
        status = False
        platform = None

        gfx_display_hwinfo = SystemInfo().get_gfx_display_hardwareinfo()
        for i in range(len(gfx_display_hwinfo)):
            if gfx_display_hwinfo[i].gfxIndex == gfx_index:
                platform = gfx_display_hwinfo[i].DisplayAdapterName
                break

        # Set PG2 bit mask
        if platform in ['ICLHP', 'ICLLP', 'LKF1', 'TGL']:
            pg_bit = BIT_MASK_POWER_WELL_3
            self.power_well_bit = 4

        # Get the audio MMIO
        reg_pg = self.driver_interface_.mmio_read(PWR_CONTROL, gfx_index)
        logging.debug("\tPWR_WELL_CTL register 0x45404 value is        :   %s" % hex(reg_pg))
        enumerated_displays = self.display_config.get_enumerated_display_info()
        self.current_display_config = self.display_config.get_current_display_configuration_ex(enumerated_displays)
        if power_well_enabled is False:
            if reg_pg & pg_bit == 0:
                logging.info("\tPASS: PWR_WELL_CTL expected to be DISABLED({0}:0) and Actual: {0}:0".format(
                    self.power_well_bit))
                status = True
            else:
                gdhm.report_test_bug_audio(
                    title="[Audio] PWR_WELL_CTL expected to be DISABLED({0}:0) and Actual: {0}:1".format(
                        self.power_well_bit))
                logging.error("\tFAIL: PWR_WELL_CTL expected to be DISABLED({0}:0) and Actual: {0}:1".format(
                    self.power_well_bit))
        else:
            check_pg_bit = (reg_pg & pg_bit)
            if check_pg_bit == pg_bit:
                logging.info("\tPASS: PWR_WELL_CTL expected to be ENABLED({0}:1) and Actual: {0}:1".format(
                    self.power_well_bit))
                status = True
            else:
                gdhm.report_test_bug_audio(
                    title="[Audio] PWR_WELL_CTL expected to be ENABLED({0}:1) and Actual: {0}:0".format(
                        self.power_well_bit))
                logging.error("\tFAIL: PWR_WELL_CTL expected to be ENABLED({0}:1) and Actual: {0}:0".format(
                    self.power_well_bit))
        return status

    ##
    # @brief        Function to install audio driver
    # @param[in]    dvr_path - Intel Graphics Driver path
    # @return       Status - True if installation successful; False otherwise
    def install_audio_driver(self, dvr_path=DRIVER_PATH):
        status = False
        platform_name = None
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for index in adapter_dict.keys():
            platform_information = SystemInfo().get_platform_details(adapter_dict[index].deviceID)
            # Codec device ID will differ for JSL and EHL. Since based on SKU name update the platform name as EHL.
            if platform_information.PlatformName == "JSL" and platform_information.SkuName == "EHL":
                platform_name = 'EHL'
            else:
                platform_name = platform_information.PlatformName
        # Checks if the folder is present
        driver_path = os.path.join(dvr_path, r"Graphics\DisplayAudio")
        is_path_present = os.path.exists(driver_path)

        # Installs ACX Codec. ACX Supported platforms: TGL,DG1,DG2,RKL,ADLS,ADLP
        if platform_name not in self.non_acx_platforms:
            if is_path_present is False:
                logging.info("Release internal package is loaded")
                inf_path = "MSHdaDac.inf"
                cat_path = "AcxDAC.cat"
            else:
                logging.info("Installer-release package is loaded")
                inf_path = "Graphics\\" + "\\MSHdaDac.inf"
                cat_path = "Graphics\\" + "\\AcxDAC.cat"
        # Installs Intel codec
        else:
            # Variable to hold the name of audio directory
            audio_directory_name = None

            # Set the directory name corresponding to platform
            if platform_name in ['SKL', 'APL']:
                audio_directory_name = "10.26"
            if platform_name in ['KBL', 'CFL', 'GLK', 'WHL', 'CML']:
                audio_directory_name = "10.27"
            if platform_name in ['ICLLP', 'JSL']:
                audio_directory_name = "11.1"
            if platform_name in ['LKF1', 'EHL']:
                audio_directory_name = "11.2"

            if audio_directory_name is None:
                gdhm.report_test_bug_audio(
                    title="[Audio] Display Audio folder is not present for installing the Audio Codec Driver")
                logging.error("\tDisplay Audio folder is not present for installing the Audio Codec Driver")
                return status

            if is_path_present is False:
                logging.info("Release internal package is loaded")
                inf_path = "DisplayAudio\\" + audio_directory_name + "\\IntcDAud.inf"
                cat_path = "DisplayAudio\\" + audio_directory_name + "\\IntcDAud.cat"
            else:
                logging.info("Installer-release package is loaded")
                inf_path = "Graphics\\DisplayAudio\\" + audio_directory_name + "\\IntcDAud.inf"
                cat_path = "Graphics\\DisplayAudio\\" + audio_directory_name + "\\IntcDAud.cat"

        cert_path = os.path.join(dvr_path, cat_path)
        cert_install_process = subprocess.call([CERT_INSTALL_PATH, cert_path])
        if cert_install_process != 0:
            logging.error("\tCertificate installation failed")
        else:
            for gfx_index in adapter_dict.keys():
                inf_path = os.path.join(dvr_path, inf_path)
                install_status = subprocess.call(
                    ["C:\Windows\System32\pnputil.exe", "/add-driver", inf_path, "/install"])
                if install_status != 0:
                    logging.error("\tPnPUtil call failed")

                for sec in range(AUDIO_DRIVER_INSTALL_UNINSTALL_TIMEOUT):
                    codec = self.get_audio_driver(gfx_index)
                    audio_codec = 'ACX' if codec == AudioCodecDriverType.ACX else 'Intel'
                    status = True
                    break
            logging.info(f"{audio_codec} audio driver installed successfully for {gfx_index} (~{sec} seconds)")

        return status

    ##
    # @brief    Function to uninstall audio drivers
    # @return   Status - True if uninstalled; false otherwise
    def uninstall_audio_driver(self):
        status = False
        # Get audio driver info
        audio_driver_info = self.get_audio_driver_info()
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        # get_audio_driver_info failed, return False
        if audio_driver_info['OEM_File'] is None or audio_driver_info['status'] is False:
            logging.error("\tUnable to get driver info")
        else:
            # Uninstall the audio driver
            uninstall_status = subprocess.call(
                ["C:\Windows\System32\pnputil.exe", "/delete-driver", audio_driver_info['OEM_File'], "/uninstall",
                 "/force"])
            if uninstall_status != 0:
                logging.error("\tPnPUtil call failed")

            for gfx_index in adapter_dict.keys():
                for sec in range(AUDIO_DRIVER_INSTALL_UNINSTALL_TIMEOUT):
                    present_audio_codec_driver = self.get_audio_driver(gfx_index)
                    if present_audio_codec_driver != AudioCodecDriverType.INTEL or \
                            present_audio_codec_driver != AudioCodecDriverType.ACX:
                        status = True
                        logging.info(f"Audio driver uninstalled successfully for {gfx_index} (~{sec} seconds)")
                        break
                    time.sleep(1)

        return status

    ##
    # @brief    Get Audio Driver Info
    # @return   Audio Codec Driver Inf Name
    def get_audio_driver_info(self):
        audio_driver_info = {'status': False, 'OEM_File': None}
        query_result = ""
        # Query to get audio driver information
        cmd = "powershell \"([wmisearcher]\\\"SELECT * FROM Win32_PnPSignedDriver " \
              "where DeviceClass='Media' " \
              "and HardWareID LIKE 'INTELAUDIO%FUNC_01%VEN_8086%' " \
              "or HardWareID LIKE 'HDAUDIO%FUNC_01%VEN_8086%'\\\").Get()\""

        # Execute the command and get the query result
        try:
            # In SGPC case, unable to get Audio driver info in Clone mode, Restarting WMI service is helping to fix the issue,
            os.system('powershell.exe net stop winmgmt /y')
            os.system('powershell.exe net start winmgmt /y')
            query_result = subprocess.check_output(cmd, universal_newlines=True)
            time.sleep(5)
        except Exception as e:
            logging.error("\tUnable to get the driver info")

        # If query failed to produce any result, mark driver as not found and return the status
        if len(query_result) > 1:
            driver_info_entries = query_result.split("\n")
            if len(driver_info_entries) < 1:
                logging.debug("Invalid audio driver info")

            # Populate the audio_driver_info object with query result
            if driver_info_entries:
                for entry in driver_info_entries:
                    entry_data = entry.strip().split(": ")
                    if len(entry_data) > 1:
                        if entry_data[0].strip() == 'InfName':
                            audio_driver_info['status'] = True
                            audio_driver_info['OEM_File'] = entry_data[1].strip()

        return audio_driver_info

    ##
    # @brief        get property page details
    # @param[in]    display_name target
    # @return       playback_device_info of type AudioEndpointsInformation
    def get_property_page_details(self, display_name):
        playback_device_info = AudioEndpointsInformation()
        playback_device_info.Size = ctypes.sizeof(AudioEndpointsInformation)
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_char_p, ctypes.POINTER(AudioEndpointsInformation))
        func = prototype(('GetAudioEndpointNames', self.displayAudioCodecDll))
        status = func(display_name, ctypes.byref(playback_device_info))
        if status is not True:
            logging.error("\tFailed to get data from property page")
            return None
        return playback_device_info

    ##
    # @brief        Disabling Intel/ACX Audio codec driver
    # @param[in]    gfx_index - Gfx Adapter index
    # @return       Status - True if audio codec driver is disabled successfully; False otherwise
    def disable_audio_driver(self, gfx_index="gfx_0"):
        status = False
        codec = self.get_audio_driver(gfx_index)
        # Disables the hardware id of INTELAUDIO incase of Intel Bus and Intel/ACX audio codec
        cmd = "Disable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{ $_.InstanceId -like 'INTELAUDIO*FUNC_01*VEN_8086*'}).InstanceId -Confirm:$false"
        subprocess.run(["powershell", "-Command", cmd])
        time.sleep(5)

        status_cmd = f"pnputil /enum-devices /connected | Select-String -Pattern 'INTELAUDIO.*FUNC_01.*VEN_8086.*' -Context 0,7"
        disable_status = subprocess.run(["powershell", "-Command", status_cmd], capture_output=True)
        if disable_status.returncode != 0:
            disable_status_stderr = disable_status.stderr.decode("utf-8", "ignore").replace("\r\n", " | ")
            logging.error(
                f"Error fetching status of Intel Bus and Intel/ACX audio codec drivers- {disable_status_stderr}")

        time.sleep(5)
        status_index = disable_status.stdout.find(b"Status")
        result = re.search(r'Disabled', disable_status.stdout[status_index:].decode("unicode_escape"), re.I)
        if result:
            status = True
        else:
            # Disables the hardware id of HDAUDIO incase of MSFT Bus and Intel/ACX audio codec
            logging.debug("Trying to disable audio driver with HDAUDIO")
            cmd = "Disable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{ $_.InstanceId -like 'HDAUDIO*FUNC_01&VEN_8086*'}).InstanceId -Confirm:$false"
            subprocess.run(["powershell", "-Command", cmd])
            time.sleep(5)

            status_cmd = f"pnputil /enum-devices /connected | Select-String -Pattern 'HDAUDIO.*FUNC_01&VEN_8086.*' -Context 0,7"
            disable_status = subprocess.run(["powershell", "-Command", status_cmd], capture_output=True)
            if disable_status.returncode != 0:
                disable_status_stderr = disable_status.stderr.decode("utf-8", "ignore").replace("\r\n", " | ")
                logging.error(
                    f"Error fetching status of MSFT Bus and Intel/ACX audio codec drivers- {disable_status_stderr}")

            time.sleep(5)
            status_index = disable_status.stdout.find(b"Status")
            result = re.search(r'Disabled', disable_status.stdout[status_index:].decode("unicode_escape"), re.I)
            if result:
                status = True

        audio_codec = "Intel" if codec == AudioCodecDriverType.INTEL else "ACX"
        if status:
            logging.info("\t{0} audio codec driver disabled successfully".format(audio_codec))
        else:
            gdhm.report_test_bug_audio(
                title="[Audio] Failed to disable {0} audio codec driver".format(audio_codec))
            logging.error("\tFailed to disable {0} audio codec driver".format(audio_codec))
        return status

    ##
    # @brief        Enabling Intel/ACX Audio Codec driver
    # @param[in]    gfx_index - Index of Gfx Adapter
    # @return       Status - True if audio codec driver is enabled successfully; False otherwise
    def enable_audio_driver(self, gfx_index="gfx_0"):
        status = False
        codec = self.get_audio_driver(gfx_index)
        # Enables the hardware id of INTEL AUDIO in case of Intel Bus and Intel/ACX audio codec
        cmd = "Enable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{ $_.InstanceId -like 'INTELAUDIO*FUNC_01*VEN_8086*'}).InstanceId -Confirm:$false"
        sub_cmd = "Enable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{ $_.InstanceId -like 'INTELAUDIO*SUBFUNC_01*VEN_8086*'}).InstanceId -Confirm:$false"
        subprocess.run(["powershell", "-Command", cmd])
        subprocess.run(["powershell", "-Command", sub_cmd])
        time.sleep(5)

        status_cmd = f"pnputil /enum-devices /connected | Select-String -Pattern 'INTELAUDIO.*FUNC_01.*VEN_8086.*' -Context 0,7"
        enable_status = subprocess.run(["powershell", "-Command", status_cmd], capture_output=True)
        if enable_status.returncode != 0:
            enable_status_stderr = enable_status.stderr.decode("utf-8", "ignore").replace("\r\n", " | ")
            logging.error(
                f"Error fetching status of Intel Bus and Intel/ACX audio codec drivers- {enable_status_stderr}")

        time.sleep(5)
        status_index = enable_status.stdout.find(b"Status")
        result = re.search(r'Started', enable_status.stdout[status_index:].decode("unicode_escape"), re.I)
        if result:
            status = True
        else:
            # Enables the hardware id of HDAUDIO incase of MSFT Bus and Intel/ACX audio codec
            logging.debug("Trying to enable audio driver with HDAUDIO")
            cmd = "Enable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{ $_.InstanceId -like 'HDAUDIO*FUNC_01&VEN_8086*'}).InstanceId -Confirm:$false"

            if codec == AudioCodecDriverType.ACX:
                # Enables the endpoint entry of ACX audio codec driver
                sub_cmd = "Enable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{ $_.InstanceId -like 'HDAUDIO*SUBFUNC_01&VEN_8086*'}).InstanceId -Confirm:$false"
                subprocess.run(["powershell", "-Command", cmd])
                subprocess.run(["powershell", "-Command", sub_cmd])
            subprocess.run(["powershell", "-Command", cmd])

            time.sleep(5)
            status_cmd = f"pnputil /enum-devices /connected | Select-String -Pattern 'HDAUDIO.*FUNC_01&VEN_8086.*' -Context 0,7"
            enable_status = subprocess.run(["powershell", "-Command", status_cmd], capture_output=True)
            if enable_status.returncode != 0:
                enable_status_stderr = enable_status.stderr.decode("utf-8", "ignore").replace("\r\n", " | ")
                logging.error(
                    f"Error fetching status of MSFT Bus and Intel/ACX audio codec drivers- {enable_status_stderr}")

            time.sleep(5)
            status_index = enable_status.stdout.find(b"Status")
            result = re.search(r'Started', enable_status.stdout[status_index:].decode("unicode_escape"), re.I)
            if result:
                status = True
        audio_codec = "Intel" if codec == AudioCodecDriverType.INTEL else "ACX"
        if status:
            logging.info("\t{0} audio codec driver enabled successfully".format(audio_codec))
        else:
            gdhm.report_test_bug_audio(
                title="[Audio] Failed to enable {0} audio codec driver".format(audio_codec))
            logging.error("\tFailed to enable {0} audio codec driver".format(audio_codec))
        return status

    ##
    # @brief        Enable or Disable Audio controller
    # @param[in]    action - parameter to specify enable/disable
    # @param[in]    gfx_index - Index of Gfx Adapter
    # @return       status - True if audio controller driver is enabled/disabled successfully; False otherwise
    def disable_enable_audio_controller(self, action, gfx_index="gfx_0"):
        status = False

        if action.lower() not in ['disable', 'enable']:
            logging.error("Invalid Action Parameter ({0}) parsed".format(action))
            return status
        else:
            action = action.lower()

        for index in range(self.controller_adapter.numAudioController):
            if self.controller_adapter.displayAudioInfo[index].gfxIndex == gfx_index:
                device_id = self.controller_adapter.displayAudioInfo[index].controller_deviceID
                hardware_id = 'PCI\\VEN_8086&DEV_{0}*'.format(device_id)

                if action == "disable":
                    cmd = f"Disable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{{ $_.InstanceId -like '{hardware_id}'}}).InstanceId -Confirm:$false"
                else:
                    cmd = f"Enable-PnpDevice -InstanceId(Get-PnpDevice | Where-Object{{ $_.InstanceId -like '{hardware_id}'}}).InstanceId -Confirm:$false"

                # Enable/Disable the Audio Controller
                driver_status_output = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
                device_status = subprocess.run([DEVCON_EXE_PATH, "rescan"], universal_newlines=True)

                # Check if enable/disable operation is successful or not
                if device_status.returncode == 0:
                    logging.debug("{0} Audio controller for {1} success".format(action.upper(), gfx_index.upper()))
                    status = True
                else:
                    gdhm.report_test_bug_audio(
                        title="[Audio] {0} Audio controller for {1} failed".format(action.upper(), gfx_index.upper()))
                    logging.error("\t{0} Audio controller for {1} failed".format(action.upper(), gfx_index.upper()))
                break

        return status

    ##
    # @brief        Get Audio Driver version
    # @param[in]    gfx_index - Gfx Adapter index
    # @param[in]    codec_driver - Codec which requires version
    # @return       driver_version - Audio driver version
    def get_audio_driver_version(self, codec_driver, gfx_index="gfx_0"):
        driver_version = None
        intel_audio_codec_id = None
        if codec_driver == AudioCodecDriverType.INTEL:
            adapter_dict = test_context.TestContext.get_gfx_adapter_details()
            platform_name = SystemInfo().get_platform_details(adapter_dict[gfx_index].deviceID).PlatformName
            device_id_dict = self.get_audio_device_id_from_json(platform_name)

            for codec_id in device_id_dict['codec']:
                intel_audio_codec_id = "{0}&DEV_{1}".format(HARDWARE_ID_INTEL_AUDIO[:-1].replace('*', '.*'), codec_id)

                # Get the driver nodes data from pnputil
                cmd = f"pnputil /enum-devices /connected | Select-String -Pattern '{intel_audio_codec_id}' -Context 0,7"
                codec_status = subprocess.run(["powershell", "-Command", cmd], capture_output=True)

                if codec_status.returncode != 0:
                    codec_status_stderr = codec_status.stderr.decode('utf-8', 'ignore').replace("\r\n", " | ")
                    logging.error(f"Error fetching Intel audio codec status-{codec_status_stderr}")
                    return driver_version

                codec_status_stdout = codec_status.stdout
                if len(codec_status_stdout) == 0:
                    logging.error(f"Audio driver not found")
                    return driver_version

                codec_inf_index = codec_status_stdout.find(b'Driver Name:')
                codec_inf = codec_status_stdout[codec_inf_index:].decode('unicode_escape').split("\r\n")[0].split(":")[1].strip()

                inf_cmd = f"pnputil /enum-drivers | Select-String -Pattern '{codec_inf}' -Context 0,5"
                driver_nodes_output = subprocess.run(["powershell", "-Command", inf_cmd], capture_output=True)
                if driver_nodes_output.returncode != 0:
                    driver_nodes_output_stderr = driver_nodes_output.stderr.decode('utf-8', 'ignore').replace("\r\n", " | ")
                    logging.error(f"Error fetching driver version - {driver_nodes_output_stderr}")
                    return driver_version

                driver_nodes_output_stdout = driver_nodes_output.stdout
                if len(driver_nodes_output_stdout) == 0:
                    logging.error(f"Driver version detail is not present")
                    return driver_version

                version_index = driver_nodes_output_stdout.find(b'Driver Version:')
                version_info = driver_nodes_output_stdout[version_index:].decode('unicode_escape').split("\r\n")[0].split(":")[1]
                driver_version = version_info.strip().split(" ")[-1]

        return driver_version

    ##
    # @brief        Check if any external display is present
    # @param[in]    gfx_index - Gfx Adapter index
    # @return       True if any external panel is connected, False otherwise
    def is_external_display_present(self, gfx_index="gfx_0"):
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[index]
            display_adapter_index = display.DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if (display_adapter_index != gfx_index) or (display.IsActive is False):
                continue
            vbt_panel_type = display_utility.get_vbt_panel_type(
                cfg_enum.CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name, gfx_index)
            if vbt_panel_type not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                return True
        return False

    ##
    # @brief        Verification of SGPC status
    # @param[in]    gfx_index - Gfx Adapter index
    # @return       Status - True, if SGPC is enabled, False otherwise
    def is_sgpc_enabled(self, gfx_index='gfx_0'):
        status = False
        platform_name = None

        # Verify OS Build version since SGPC is not supported on OS builds older than 19H1(18282)
        os_information = SystemInfo().get_os_info()
        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        for index in adapter_dict.keys():
            dut_info = SystemInfo().get_platform_details(adapter_dict[index].deviceID)
            if dut_info.PlatformName == "JSL" and dut_info.SkuName == "EHL":
                platform_name = "EHL"
            else:
                platform_name = dut_info.PlatformName
        if int(os_information.BuildNumber) <= 18282 and platform_name not in ['EHL']:
            ver_str = f"{os_information.MajorVersion}.{os_information.MinorVersion}.{os_information.BuildNumber}"
            logging.debug("SGPC is not supported in this OS (Version {0})".format(ver_str))
            return status

        if self.system_utility.get_execution_environment_type() in ["SIMENV_FULSIM"]:
            # In Pre-Si FulSim platform, audio controller will not be loaded because of PCH
            # In this case, registry read will fail for GfxSharedCodecAddress
            # Using static platform mapping for such cases
            adapter_dict = test_context.TestContext.get_gfx_adapter_details()
            platform_name = SystemInfo().get_platform_details(adapter_dict[gfx_index].deviceID).PlatformName
            if platform_name in SGPC_MAPPING.keys():
                status = SGPC_MAPPING[platform_name]
            return status

        # Get Audio Driver SGPC status, SGPC enabled = 'GfxSharedCodecAddress' with value 0x02
        ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index,
                                                             feature=registry_access.Feature.AUDIO,
                                                             guid=registry_access.GUID_DEVCLASS_SYSTEM)
        aud_bus_sgpc_reg_value, reg_type = registry_access.read(args=ss_reg_args, reg_name='GfxSharedCodecAddress',
                                                                sub_key="Settings")

        if aud_bus_sgpc_reg_value == 2:
            status = True
        logging.info("GfxSharedCodecAddress registry value: {0} SGPC Status: {1}".format(aud_bus_sgpc_reg_value,
                                                                                         status))

        return status

    ##
    # @brief        This function gets the audio controller type
    # @param[in]    gfx_index - Gfx Adapter index
    # @return       audio_controller - controller type (enum)
    def get_audio_controller(self, gfx_index='gfx_0'):
        audio_controller = AudioControllerType.NONE
        bus_version = None
        device_id = None
        for index in range(self.controller_adapter.numAudioController):
            if self.controller_adapter.displayAudioInfo[index].gfxIndex == gfx_index:
                device_id = self.controller_adapter.displayAudioInfo[index].controller_deviceID

                hardware_id = f'PCI.*VEN_8086&DEV_{device_id}.*'
                cmd = f"pnputil /enum-devices /connected | Select-String -Pattern '{hardware_id}' -Context 0,7"
                device_status = subprocess.run(["powershell", "-Command", cmd], capture_output=True)

                if device_status.returncode != 0:
                    device_status_stderr = device_status.stderr.decode('utf-8', 'ignore').replace("\r\n", " | ")
                    logging.error(f"Error fetching device status status-{device_status_stderr}")

                device_status_stdout = device_status.stdout
                device_description = device_status_stdout.find(b'Device Description:')

                if device_description == -1:
                    logging.error("No Audio Controller is loaded")
                    break
                else:
                    self.audio_controller_name = device_status_stdout[device_description:].decode('unicode_escape').split("\r\n")[0].split(":")[1].strip()
                    logging.debug(f"Audio_controller_name - {self.audio_controller_name}")
                ms_controller = re.search(r'High Definition Audio Controller', self.audio_controller_name, re.I)
                intel_controller = re.search(r'Intel', self.audio_controller_name, re.I)
                controller_status = re.search(r'Started', device_status_stdout[device_description:].decode('unicode_escape'), re.I)
                if ms_controller is not None:
                    if controller_status is not None:
                        audio_controller = AudioControllerType.MS
                        logging.debug("MS Audio Controller with {0} device ID loaded".format(device_id))
                    else:
                        logging.error("MS Audio Controller with {0} device ID is in yellow bang".format(device_id))
                    break
                elif intel_controller is not None:
                    if controller_status is not None:
                        audio_controller = AudioControllerType.INTEL
                        device_inf_index = device_status_stdout.find(b'Driver Name:')
                        device_inf = device_status_stdout[device_inf_index:].decode('unicode_escape').split("\r\n")[0].split(":")[1].strip()
                        inf_cmd = f"pnputil /enum-drivers | Select-String -Pattern '{device_inf}' -Context 0,5"
                        device_version = subprocess.run(["powershell", "-Command", inf_cmd],capture_output=True)

                        if device_version.returncode != 0:
                            device_version_stderr = device_version.stderr.decode('utf-8', 'ignore').replace("\r\n", " | ")
                            logging.error(f"Error fetching device version - {device_version_stderr}")

                        device_version_stdout = device_version.stdout.decode('utf-8', 'ignore').split('\r\n')
                        if len(device_version_stdout) == 1:
                            logging.error("Driver version detail is not present")
                        else:
                            bus_version = device_version_stdout[6].split(":")[-1].strip().split(" ")[-1]
                            logging.debug("Intel Audio Controller with {0} device ID loaded [{1}]"
                                          .format(device_id, bus_version))
                    else:
                        logging.error("Intel Audio Controller with {0} device ID is in yellow bang [{1}]"
                                      .format(device_id, bus_version))
                    break
                else:
                    logging.error("No Audio Controller is loaded")
                    break

        return audio_controller, device_id, bus_version

    ##
    # @brief        This function gets the oed status in case of Intel Bus
    # @return       oed_status - True if OED is loaded, false if YB/Not loaded
    def get_oed_status(self):
        oed_status = False
        bus_version = None
        hardware_id = "INTELAUDIO.*DSP_CTLR_.*"
        status_cmd = f"pnputil /enum-devices /connected | Select-String -Pattern '{hardware_id}' -Context 0,7"
        device_status = subprocess.run(["powershell", "-Command", status_cmd], capture_output=True)
        if device_status.returncode != 0:
            device_status_stderr = device_status.stderr.decode('utf-8', 'ignore').replace("\r\n", " | ")
            logging.error(f"Error fetching Intel OED Controller status - {device_status_stderr}")
            return oed_status, bus_version

        device_status_stdout = device_status.stdout
        device_status_index = device_status_stdout.find(b'Status:')
        oed_status = re.search('Started', device_status_stdout[device_status_index:].decode('unicode_escape'), re.I)

        if oed_status is not None:
            oed_status = True
        else:
            oed_status = False
            gdhm.report_test_bug_audio(
                title="[Audio] Intel OED Controller is not loaded or Yellow bang observed ")
            logging.error("Intel OED Controller is not loaded or Yellow bang observed")
            return oed_status, bus_version

        inf_index = device_status_stdout.find(b'Driver Name:')
        device_inf = device_status_stdout[inf_index:].decode("unicode_escape").split(":")[-1].replace("\r\n",
                                                                                                      "").strip()

        version_cmd = f"pnputil /enum-drivers | Select-String -Pattern '{device_inf}' -Context 0,7"
        device_version = subprocess.run(["powershell", "-Command", version_cmd], capture_output=True)
        if device_version.returncode != 0:
            device_version_stderr = device_version.stderr.decode('utf-8', 'ignore').replace("\r\n", " | ")
            logging.error(f"Error fetching Intel OED Controller version - {device_version_stderr}")
            return oed_status, bus_version

        device_version_stdout = device_version.stdout
        version_index = device_version_stdout.find(b'Driver Version:')
        bus_version = device_version_stdout[version_index:].decode("unicode_escape").split(" ")[7].replace("\r\n",
                                                                                                           "").strip()
        bus_version = "Driver version  is " + bus_version
        if oed_status:
            logging.debug("Intel OED Controller with [{0}] is loaded".format(bus_version))
        return oed_status, bus_version

    ##
    # @brief        This function dumps all the Audio specific MMIO's in case of failure
    # @return       None
    def mmio_dumps(self):
        endpoint_mmio = {'AUD_PIN_ELD_CP_VLD': [0x650C0], 'AUD_EDID_DATA': [0x65050, 0x65150, 0x65250, 0x65350]}
        codec_mmio = {'PWR_WELL_CTL1': [0x45400], 'PWR_WELL_CTL2': [0x45404], 'AUDIO_PIN_BUF_CTL': [0x48414],
                      'CDCLK_CTL': [0x46000], 'CDCLK_PLL_ENABLE': [0x46070], 'AUD_VID_DID': [0x65020],
                      'AUD_RID': [0x65024], 'AUD_CHICKENBIT_REG': [0x65F10], 'AUD_CHICKENBIT_REG_2': [0x65F0C],
                      'AUD_PWRST': [0x6504C], 'AUD_FREQ_CNTRL': [0x65900]}
        playback_mmio = {'AUD_PIPE_CONV_CFG': [0x6507C], 'AUD_OUT_CHAN_MAP': [0x65088],
                         'AUD_HDMI_FIFO_STATUS': [0x650D4], 'AUD_PIPE_CONN_SEL_CTRL': [0x650AC],
                         'AUD_DP_DIP_STATUS': [0x65F20], 'AUD_HDA_DMA_REG': [0x65E00],
                         'AUD_MISC_CTRL': [0x65010, 0x65110, 0x65210, 0x65310],
                         'AUD_CONFIG': [0x65000, 0x65100, 0x65200, 0x65300],
                         'AUD_CONFIG_2': [0x65004, 0x65104, 0x65204, 0x65304],
                         'AUD_M_CTS_ENABLE': [0x65028, 0x65128, 0x65228, 0x65328],
                         'AUD_EDID_DATA': [0x65050, 0x65150, 0x65250, 0x65350],
                         'AUD_INFOFR': [0x65054, 0x65154, 0x65254, 0x65354],
                         'AUD_DIP_ELD_CTRL_ST': [0x650B4, 0x651B4, 0x652B4, 0x653B4],
                         'AUD_STR_DESC': [0x65084, 0x65184, 0x65284, 0x65384],
                         'AUD_DIG_CNVT': [0x65080, 0x65180, 0x65280, 0x65380],
                         'AUD_PIN_PIPE_CONN_ENTRY_LNGTH': [0x650A8, 0x651A8, 0x652A8, 0x653A8],
                         'AUD_VRR_COUNTER': [0x650B8, 0x651B8, 0x652B8, 0x653B8],
                         'AUD_HDA_LPIBx_REG': [0x65E04, 0x65E08, 0x65E0C, 0x65E14]}

        adapter_dict = test_context.TestContext.get_gfx_adapter_details()
        # {:30} is the number of spaces to be aligned.
        logging.info('{:*^80}'.format('Audio HardwareState MMIO DUMP'))
        for gfx_index in adapter_dict.keys():
            dut_info = SystemInfo().get_platform_details(adapter_dict[gfx_index].deviceID)
            if dut_info.PlatformName == "JSL" and dut_info.SkuName == "EHL":
                platform = "EHL"
            else:
                platform = dut_info.PlatformName

            logging.info('{:*^50}'.format(f'AUDIO ENDPOINT MMIO DUMP for {platform}'))
            for key, value in endpoint_mmio.items():
                for offset in value:
                    reg_value = self.driver_interface_.mmio_read(offset, gfx_index)
                    logging.info("{:<30s}{:>14s}{:>15s}".format(key, hex(offset), hex(reg_value)))

            logging.info('{:*^50}'.format(f'AUDIO CODEC MMIO DUMP for {platform}'))
            for key, value in codec_mmio.items():
                for offset in value:
                    reg_value = self.driver_interface_.mmio_read(offset, gfx_index)
                    logging.info("{:<30s}{:>14s}{:>15s}".format(key, hex(offset), hex(reg_value)))

            if VerifierCfg.audio_playback_verification is True:
                logging.info('{:*^50}'.format(f'AUDIO PLAYBACK MMIO DUMP for {platform}'))
                for key, value in playback_mmio.items():
                    for offset in value:
                        reg_value = self.driver_interface_.mmio_read(offset, gfx_index)
                        logging.info("{:<30s}{:>14s}{:>15s}".format(key, hex(offset), hex(reg_value)))

        logging.info('{:*^80}'.format('End of Audio HardwareState Dumps'))

    ##
    # @brief        This function will verify audio playback for provided display with provided audio sample details
    # @param[in]    port - Port Name (ex: HDMI_B)
    # @param[in]    display_info - Member of DisplayInfo Structure
    # @param[in]    channel - Audio Channel Info
    # @param[in]    bit_depth - Audio BitDepth Info
    # @param[in]    sample_rate - Audio SampleRate Info
    # @param[in]    gfx_index - Gfx Adapter Index
    # @param[in]    end_point_name - Endpoint name to be verified
    # @return       True if Playback_verification passed else False
    def audio_playback_verification(self, port=None, display_info=None, channel=2, bit_depth=16, sample_rate=48000,
                                    gfx_index='gfx_0', end_point_name=None):

        adapter_info = None
        wav_file_name = None
        # Verify Bit_depth & Sample_rate is valid
        if (bit_depth not in self.supported_bit_depths) or (sample_rate not in self.supported_sample_rates):
            logging.error(f"Invalid Parameter: BitDepth:{bit_depth} SampleRate:{sample_rate}")
            return False

        # Verify Playback Audio File
        if channel == 2:
            wav_file_name = f"Sine_Stereo_{sample_rate}Hz_{bit_depth}bits_20s.wav"
        elif channel == 4:
            wav_file_name = f"Sine_Quadrophonic_{sample_rate}Hz_{bit_depth}bits_20s.wav"
        elif channel == 6:
            wav_file_name = f"Sine_FivePointOneSurround_{sample_rate}Hz_{bit_depth}bits_20s.wav"
        elif channel == 8:
            wav_file_name = f"Sine_SevenPointOneSurround_{sample_rate}Hz_{bit_depth}bits_20s.wav"
        else:
            logging.error(f"Channel {channel} is invalid")
            return False

        audio_file = os.path.join(test_context.TestContext.test_store(), "AudioSamples", f"{channel}ch",
                                  f"{bit_depth}bit", wav_file_name)
        if os.path.exists(audio_file) is False:
            logging.error(f"Audio file is not available. Path: {audio_file}")
            return False

        # Get Audio Endpoint Device Name and Display Encoder type (Either DP or HDMI)
        # Todo: Leverage this information from OS interface instead of Monitor FriendlyName
        if display_info is not None:
            port = str(cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name)
            adapter_info = display_info.DisplayAndAdapterInfo.adapterInfo
            if end_point_name is None:
                end_point_name = display_info.FriendlyDeviceName

        elif port is not None:
            enumerated_displays = self.display_config.get_enumerated_display_info()

            for i in range(enumerated_displays.Count):
                enm_port = str(
                    cfg_enum.CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType))
                index = enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                if (index == gfx_index) and (port == enm_port):
                    if end_point_name is None:
                        end_point_name = enumerated_displays.ConnectedDisplays[index].FriendlyDeviceName

                    adapter_info = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo.adapterInfo
                    break

            if (end_point_name is None) or (adapter_info is None):
                logging.error(f"Unable to find AudioEndpoint Device name for Display: {port}")
                return False
        else:
            logging.error("Invalid Parameter. Either port or display_info parameter to be parsed")
            return False

        # Audio Endpoint port type
        if 'dp' in port.lower():
            encoder_type = 'dp'
        elif 'hdmi' in port.lower():
            encoder_type = 'hdmi'
        else:
            gdhm.report_test_bug_audio(
                title="[Audio] Unable to find Port type for Port: {0}".format(port))
            logging.error("Unable to find Port type for Port: {0}".format(port))
            return False

        # Typecasting Python str to c_char pointer
        audio_file_pointer = ctypes.c_char_p(audio_file.encode('utf-8'))
        encoder_type_pointer = ctypes.c_char_p(encoder_type.encode('utf-8'))
        device_name_pointer = ctypes.c_char_p(end_point_name.encode('utf-8'))

        prototype = ctypes.PYFUNCTYPE(ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                                      ctypes.POINTER(GfxAdapterInfo))
        func = prototype(('PlayAudioAndVerify', self.displayAudioCodecDll))
        result = func(audio_file_pointer, device_name_pointer, encoder_type_pointer, ctypes.byref(adapter_info))

        if result == 0:
            return True
        else:
            gdhm.report_driver_bug_audio(title="[Audio] Audio Playback Verification Failed")
            return False

    ##
    # @brief        This function will verify audio playback for provided display with provided audio sample details
    # @param[in]    current_endpoint_dict
    # @param[in]    only_unique_endpoint
    # @return       endpoint_list - list of audio endpoints loaded
    def get_audio_endpoint_name(self, current_endpoint_dict=None, only_unique_endpoint=True):

        if current_endpoint_dict is None:
            current_endpoint_dict = {}
        # Adding sleep time since endpoint enumeration will take ~2-3 seconds
        time.sleep(5)
        audio_endpoint_name = AudioEndpointName()
        endpoint_name_list = []

        prototype = ctypes.PYFUNCTYPE(ctypes.c_long, ctypes.POINTER(AudioEndpointName))
        func = prototype(('GetAudioEndpointNames', self.displayAudioCodecDll))
        result = func(ctypes.byref(audio_endpoint_name))

        if result == 0:
            for i in range(audio_endpoint_name.count):
                if audio_endpoint_name.endpoint_info[
                    i].formfactor == AudioEndpointFormFactor.DIGITAL_AUDIO_DISPLAY_DEVICE:
                    endpoint_name_list.append(audio_endpoint_name.endpoint_info[i].endpoint_name)
        else:
            gdhm.report_test_bug_audio(
                title="[Audio] Unable to get Audio EndPoint Name from dll")
            logging.error(f"Unable to get Audio EndPoint Name from dll")
            return endpoint_name_list

        if only_unique_endpoint is True:
            unique_endpoint_list = list(set(endpoint_name_list) - set(current_endpoint_dict.values()))
            return unique_endpoint_list
        else:
            return endpoint_name_list


    ##
    # @brief        This function will return value of sdp_splitting_enable bit from mmio
    # @param[in]    gfx_index graphics adapter
    # @param[in]    platform to get reg values
    # @param[in]    display dp_a/dp_b etc
    # @return       value of sdp splitting bit
    def get_sdp_splitting_status(self, gfx_index, platform, display):
        offset = None
        display_base_obj = display_base.DisplayBase(display, gfx_index=gfx_index)
        pipe, ddi, transcoder = display_base_obj.GetPipeDDIAttachedToPort(display, True, gfx_index)
        if pipe == 'pipe_a':
            offset = 0x650BC
        if pipe == 'pipe_b':
            offset = 0x651BC
        if pipe == 'pipe_c':
            offset = 0x652BC
        if pipe == 'pipe_d':
            offset = 0x653BC
        reg_value = self.driver_interface_.mmio_read(offset, gfx_index)
        sdp_splitting = (reg_value & 0x80000000) >> 31
        return sdp_splitting