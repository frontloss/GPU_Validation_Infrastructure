########################################################################################################################
# @file         virtual_display_helper.py
# @brief        The script consists of helper functions for Virtual Display Tests
# @author       Pai, Vinayak1
########################################################################################################################
import datetime
import logging
import math
import os
import subprocess
from concurrent import futures
from enum import IntEnum, StrEnum

from Libs.Core import etl_parser, registry_access
from Libs.Core import test_header, reboot_helper, system_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import QdcFlag, DisplayConfigVideoOutputTechnology
from Libs.Core.logger import display_logger, etl_tracer, gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Feature.app import App3D, AppMedia

# Path to exe's and folders
BIN_FOLDER = test_context.TestContext.bin_store()
ICLICK_EXE = os.path.join(BIN_FOLDER, "GfxValSimDriver", "iClick.exe")

# Path to applications and media
MEDIA_FILE = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos/24.000.mp4")
FLIPAT_APP = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR\\FlipAt\\FlipAt.exe")
CLASSICD3D_APP = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\ClassicD3D\\ClassicD3D.exe")
D3D12FULLSCREEN_APP = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\\D3D12FullScreen\\D3D12Fullscreen.exe")
SAMPLE_APPS_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER,
                                r"ControlApi\Release\SampleApp\dump64\Edid_Mgmt_Sample_app.exe")

# GDHM header
GDHM_IDD = "[Virtual Display IDD]"
GDHM_VIRTUAL_ATS = "[Virtual Display ATS]"

MAX_VIRTUAL_DISPLAY_COUNT = 4


##
# @brief        This class contains values for TestSigning actions
class TestSigning:
    ENABLE = "ON"
    DISABLE = "OFF"


##
# @brief        This class contains values for IddDriver actions
class IddDriver:
    INSTALL = "INSTALL"
    UNINSTALL = "UNINSTALL"


##
# @brief        This class contains values for iclick application actions
class IClick:
    ENABLE = "/arm"
    DISABLE = "/disarm"


##
# @brief        This class contains values for status
class Status(IntEnum):
    DISABLE = 0
    ENABLE = 1


##
# @brief        This class contains values for Regkeys used
class RegKeys(StrEnum):
    FORCE_VIRTUAL_DISPLAY = "ForceVirtualDisplay"
    MULTI_VIRTUAL_DISPLAY = "MultiVirtualDisplay"
    EDID_MGMT_ENABLE = "EdidMgmtEnable"


##
# @brief        Helper function to start ETL capture
# @param[in]    file_name : ETL file name
# @return       status    : True if ETL started otherwise False
def start_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = file_name + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return False
    return True


##
# @brief        Helper function to stop ETL capture
# @param[in]    file_name     : ETL file name
# @return       etl_file_path : Path of ETL file captured
def stop_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = file_name + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start GfxTrace after playback")
    return etl_file_path


##
# @brief        Helper function to create an object for specified app
# @param[in]    app_type : Type of app MEDIA/3D
# @return       object of the specified app type
def create_app_instance(app_type=None):
    if app_type == "MEDIA":
        return AppMedia(MEDIA_FILE)
    if app_type == "FLIPAT":
        return App3D('FlipAt', FLIPAT_APP)
    if app_type == "D3D12FULLSCREEN":
        return App3D("D3D12Fullscreen", D3D12FULLSCREEN_APP)
    if app_type == "CLASSICD3D":
        return App3D('ClassicD3D', CLASSICD3D_APP)
    else:
        raise Exception(f"{app_type} app is not defined")


##
# @brief        Helper Function to play app
# @param[in]    app        : Name of the app(MEDIA/FLIPAT/D3D12FULLSCREEN/CLASSICD3D)
# @param[in]    fullscreen : True for fullscreen else False
# @return       app_instance
def play_app(app, fullscreen=True):
    app_instance = create_app_instance(app)
    app_instance.open_app(fullscreen, minimize=True)
    return app_instance


##
# @brief        Helper function to run command line queries
# @param[in]    cmd_line : commandline
# @return       completed_process : details having stdout, stderror
def run_powershell_cmd(cmd_line):
    process_list = subprocess.run(["powershell", "-Command", cmd_line], capture_output=True)
    return process_list


############################
# Helper Functions for IDD #
############################

##
# @brief        Helper function to disable msft display adapter driver
# @return       None
def disable_msft_display_driver():
    adapter_id = None
    adapter_name = None
    # Commandline to get list of all the display adapters (Pnputil listclass Display)
    get_all_display_driver = f"pnputil /enum-devices /connected /class Display"
    process_list = run_powershell_cmd(get_all_display_driver)
    if process_list.returncode != 0:
        logging.error(f"ERROR MESSAGE: {process_list.stderr}")
        return False
    else:
        display_driver_list = process_list.stdout.decode("utf-8", "ignore").split("\r\n")
        for i in range(len(display_driver_list)):
            if display_driver_list[i].strip().startswith("Device Description") and 'Microsoft' in display_driver_list[
                i]:
                adapter_name = display_driver_list[i].split(":")[-1].strip()
                adapter_id = display_driver_list[i - 1].split(":")[-1].strip()
                break
        if adapter_id is None:
            logging.info("Microsoft Display Adapter not Present")
            return True
        # Commandline to disable all the instances of a particular adapter
        disable_microsoft_driver = f"pnputil /disable-device '{adapter_id}'"
        process_list = run_powershell_cmd(disable_microsoft_driver)
        if process_list.returncode != 0:
            logging.error(f"ERROR MESSAGE: {process_list.stderr}")
            return False
        logging.info(f"PASS: {adapter_name} disabled Successfully")
        return True


##
# @brief        Helper function to enable testsigning
# @param[in]    operation : Command to be executed [on/off]
# @return       status    : True if testsigning is enabled else False
def enable_disable_testsigning(operation):
    process_list = run_powershell_cmd(f"bcdedit /set testsigning {operation}")
    if process_list.returncode != 0:
        logging.error(f"FAIL: {process_list.stderr}")
        return False
    logging.info(f"PASS: TestSigning is {'enabled' if operation == TestSigning.ENABLE else 'disabled'}")
    return True


##
# @brief        Helper function to install/uninstall IDD
# @param[in]    operation          : Operation to be performed [INSTALL/UNINSTALL]
# @param[in]    monitor_resolution : Monitor resolution [1080p/1440p/2160p]
# @return       status             : True if driver installation/uninstallation is successful, else False
def install_uninstall_idd_driver(operation, monitor_resolution):
    inf_name = get_inf_name(monitor_resolution)

    # Commands to install and uninstall IDDs
    ENABLE_IDD_DRIVER = (f"pnputil /add-driver {test_context.SHARED_BINARY_FOLDER}\IddSampleDriver\{inf_name} "
                         f"root\iddsampledriver /install")
    DISABLE_IDD_DRIVER = (f"pnputil /delete-driver {test_context.SHARED_BINARY_FOLDER}\IddSampleDriver\{inf_name} "
                          f"root\iddsampledriver /uninstall")

    if operation == IddDriver.INSTALL:
        iclick(IClick.ENABLE)
        process_list = run_powershell_cmd(ENABLE_IDD_DRIVER)
        iclick(IClick.DISABLE)
    elif operation == IddDriver.UNINSTALL:
        process_list = run_powershell_cmd(DISABLE_IDD_DRIVER)
    else:
        logging.info(f"FAIL: {operation} not defined.Only INSTALL and UNINSTALL operations are supported")
        return False
    if process_list.returncode != 0:
        logging.error(f"FAIL: {process_list.stderr}")
        return False
    logging.info(f"PASS: IDD Driver {'installed' if operation == IddDriver.INSTALL else 'uninstalled'} successfully")
    return True


##
# @brief        Helper function to check whether idd display found
# @param[in]    monitor_resolution : Resolution of the monitor
# @return       status             : True if IDD display present, else False
def verify_idd_display_enumeration(monitor_resolution):
    config = DisplayConfiguration()
    status = True
    idd_count = 0

    ret_status, path_info_arr, mode_info_arr, topology_id = config.query_display_config_os(
        QdcFlag.QDC_ALL_PATHS | QdcFlag.QDC_VIRTUAL_MODE_AWARE)

    if ret_status is False:
        logging.error("FAIL: QDC call Failed")
        return False
    logging.info("PASS: QDC call Successful")

    logging.info("Step: Check whether display is IDD and resolution matches with the monitor or not")
    for (each_path, each_mode) in zip(path_info_arr, mode_info_arr):
        logging.debug(f"Enumerated Display value : {each_path.targetInfo.outputTechnology}")
        # After MSFT adapter is disabled, the system will enumerate a display which has output technology
        # enumerated to DISPLAYCONFIG_OUTPUT_TECHNOLOGY_FORCE_UINT32, so updating status as True in this case.
        if (each_path.targetInfo.outputTechnology !=
                DisplayConfigVideoOutputTechnology.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_FORCE_UINT32):
            if (each_path.targetInfo.outputTechnology ==
                    DisplayConfigVideoOutputTechnology.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INDIRECT_WIRED or \
                    each_path.targetInfo.outputTechnology ==
                    DisplayConfigVideoOutputTechnology.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INDIRECT_VIRTUAL):
                resolution = get_resolution(monitor_resolution)
                logging.info(f"Width: {each_mode.targetMode.targetVideoSignalInfo.activeSize.cx}, "
                             f"Height: {each_mode.targetMode.targetVideoSignalInfo.activeSize.cy}")
                if each_mode.targetMode.targetVideoSignalInfo.activeSize.cx == resolution['width'] and \
                        each_mode.targetMode.targetVideoSignalInfo.activeSize.cy == resolution['height']:
                    idd_count += 1
                    status = True

                else:
                    status = False
            else:
                status = False
    if status is False:
        logging.error("FAIL: IDD Display not Found")
        return False
    logging.info(f"PASS: {idd_count} IDD Display Found")
    return True


##
# @brief        Helper function to take care of popup during driver installation
# @param[in]    action : Command to be executed [arm/disarm]
# @return       None
def iclick(action):
    # /arm     : start waiting for pop-up windows and serve them if appear
    # /disarm  : stop waiting for pop - up windows
    # if not disarmed, then iclick will wait for 10 minutes and disarms automatically
    cmd = ICLICK_EXE + ' ' + action
    subprocess.Popen(cmd)
    logging.info(f"PASS: iClick {action}ed")


##
# @brief        Helper function to fetch name of the inf file for a monitor resolution
# @param[in]    monitor_resolution : Resolution of the monitor
# @return       inf_file_name      : Name of the inf file for a monitor resolution
def get_inf_name(monitor_resolution):
    return {
        '1080P': 'IddSampleDriver_1080.inf',
        '1440P': 'IddSampleDriver_1440.inf',
        '2160P': 'IddSampleDriver_2160.inf'
    }[monitor_resolution]


##
# @brief        Helper function to fetch the height and width for a monitor resolution
# @param[in]    monitor_resolution : Resolution of the monitor
# @return       {width, height}    : Dictionary containing width and height of a particular monitor resolution
def get_resolution(monitor_resolution):
    return {
        '1080P': {'width': 1920, 'height': 1080},
        '1440P': {'width': 2560, 'height': 1440},
        '2160P': {'width': 3840, 'height': 2160}
    }[monitor_resolution]


####################################################
# Helper Functions for Virtual Display Tests (ATS) #
####################################################

##
# @brief        Helper function to get enable and disable timings
# @param[in]    interrupt_data : List that contains details about the interrupt
# @return       vbi_timings    : List having enable and disable VBI timestamp
def get_enable_disable_timings(interrupt_data):
    vbi_enable_timings = []
    vbi_disable_timings = []
    for each_interrupt in range(1, len(interrupt_data) - 1):
        if interrupt_data[each_interrupt].CrtVsyncState == etl_parser.CrtcVsyncState.ENABLE and \
                interrupt_data[each_interrupt - 1].CrtVsyncState == etl_parser.CrtcVsyncState.DISABLE_NO_PHASE:
            vbi_enable_timings.append(interrupt_data[each_interrupt].TimeStamp)
        if interrupt_data[each_interrupt].CrtVsyncState == etl_parser.CrtcVsyncState.DISABLE_NO_PHASE and \
                interrupt_data[each_interrupt - 2].CrtVsyncState == etl_parser.CrtcVsyncState.ENABLE:
            vbi_disable_timings.append(interrupt_data[each_interrupt].TimeStamp)
    return vbi_enable_timings, vbi_disable_timings


##
# @brief        Helper function to calculate vsync interval
# @param[in]    media_playback_etl : Name of the ETL file to be verified
# @return       status             : True if verification is passed else False
def calculate_vsync_interval(media_playback_etl):
    status = True
    # Video etl parsing
    if etl_parser.generate_report(media_playback_etl) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                   etl_parser.InterruptType.CRTC_VSYNC)

    if interrupt_data is None:
        logging.error("FAIL: No VBI enable data present in ETL file")
        return False
    ##
    # Vsync interval verification
    flip_data = etl_parser.get_flip_data()
    if flip_data is None:
        logging.error("No Flip data found")
        return False

    vbi_enable_timings, vbi_disable_timings = get_enable_disable_timings(interrupt_data)

    for each_enable_timing, each_disable_timing in zip(vbi_enable_timings, vbi_disable_timings):
        time_stamp = []
        if each_enable_timing < each_disable_timing:
            for flip in flip_data:
                if len(flip.NotifyVSyncLayerList) != 0:
                    for notifyVsync in flip.NotifyVSyncLayerList:
                        if each_enable_timing < notifyVsync.TimeStamp < each_disable_timing:
                            time_stamp.append(notifyVsync.TimeStamp)
        else:
            continue
        ##
        # Taking average of flips and checking the Vsync interval should be ~16 or ~18
        time_avg = 0
        if len(time_stamp) > 0:
            for i in range(len(time_stamp) - 1):
                logging.debug(f"Length of Timestamp: {len(time_stamp)}")
                logging.debug(f"TimeStamp found between {each_enable_timing} and {each_disable_timing}")
                logging.debug(f"{time_stamp[i + 1]} - {time_stamp[i]} = {time_stamp[i + 1] - time_stamp[i]}")
                time_diff = time_stamp[i + 1] - time_stamp[i]
                time_avg = time_avg + time_diff
            avg = time_avg / (len(time_stamp) - 1)
            logging.debug(f"Average Vsync internal for {len(time_stamp)} flips {avg}ms for media playback")
            if 16 <= math.floor(avg) <= 18:
                logging.info(f"Vsync interval is {avg}ms for media playback")
                status &= True
            else:
                logging.error(f"Vsync interval Expected: 16ms-18ms Actual: {avg}ms for media playback")
                gdhm.report_driver_bug_os(
                    f"{GDHM_VIRTUAL_ATS} Vsync interval Expected: 16ms-18ms Actual: {avg}ms for media playback")
                status &= False

    return status


##
# @brief            API to verify virtual display
# @param[in]        etl_file           : Name of the ETL file to be verified
# @param[in]        display_resolution : Display resolution passed in command line
# @return           status             : True if verification is passed else False
def verify_virtual_display(etl_file, display_resolution):
    if etl_parser.generate_report(etl_file) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN)
    if ddi_output is None:
        logging.warning("No DDI_SETTIMINGSFROMVIDPN event found in ETLs (Driver Issue)")
        gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        return False

    ddi_data = ddi_output[-1]

    ##
    # Get all SetTiming events that happened during last DDI_SETTIMINGSFROMVIDPN call
    set_timing_output = etl_parser.get_event_data(
        etl_parser.Events.SET_TIMING, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)

    if set_timing_output is None:
        logging.error("No SetTiming event found in ETLs (Driver Issue)")
        gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} No SetTiming event found in ETLs")
        return False

    set_timing_data = set_timing_output[-1]
    logging.debug(f"Set_Timing_Data - {set_timing_data}")

    if set_timing_data.Port == "VIRTUAL" and set_timing_data.Enable is True:
        if display_resolution == "2K":
            if set_timing_data.HActive == 2560 and set_timing_data.VActive == 1440:
                logging.info("2k Custom Virtual Display is enumerated")
                return True
            else:
                logging.error("2k Custom Virtual Display is not enumerated")
                gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} 2k Custom Virtual Display is not enumerated."
                                          f"Expected: HActive= 2560 and VActive = 1440, "
                                          f"Actual: HActive= {set_timing_data.HActive} and VActive= "
                                          f"{set_timing_data.VActive}")
                return False
        elif display_resolution == "4K":
            if set_timing_data.HActive == 3840 and set_timing_data.VActive == 2160:
                logging.info("4k Custom Virtual Display is enumerated")
                return True
            else:
                logging.error("4k Custom Virtual Display is not enumerated")
                gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} 4k Custom Virtual Display is not enumerated."
                                          f"Expected: HActive= 3840 and VActive = 2160, "
                                          f"Actual: HActive= {set_timing_data.HActive} and VActive= "
                                          f"{set_timing_data.VActive}")
                return False
        elif display_resolution == "DEFAULT":
            if set_timing_data.HActive == 1920 and set_timing_data.VActive == 1080:
                logging.info("19*10 Virtual Display is enumerated")
                return True
            else:
                logging.error("19*10 Virtual Display is not enumerated")
                gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} Virtual Display is not enumerated."
                                          f"Expected: HActive= 1920 and VActive = 1080, "
                                          f"Actual: HActive= {set_timing_data.HActive} and VActive= "
                                          f"{set_timing_data.VActive}")
                return False
        else:
            logging.error(f"{display_resolution} display is not supported Expected: 4k/2k/19x10")
            gdhm.report_test_bug_os(f"{display_resolution} display is not supported Expected: 4k/2k/19x10")
            return False
    else:
        logging.error(f"Virtual Display is not enumerated on {set_timing_data.Port} port")
        gdhm.report_driver_bug_os(
            f"{GDHM_VIRTUAL_ATS} Virtual Display is not enumerated on {set_timing_data.Port} port")
        return False


##
# @brief            API to verify no virtual display
# @param[in]        etl_file           : Name of the ETL file to be verified
# @return           status             : True if verification is passed else False
def verify_no_virtual_display(etl_file):
    if etl_parser.generate_report(etl_file) is False:
        logging.error("Failed to generate EtlParser report")
        return False
    set_timing_output = etl_parser.get_event_data(etl_parser.Events.SET_TIMING, event_filter='')

    if set_timing_output is None:
        logging.error("No SetTiming event found in ETLs (Driver Issue)")
        gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} No SetTiming event found in ETLs")
        return False

    set_timing_data = set_timing_output[-1]
    logging.debug(f"Set_Timing_Data - {set_timing_data}")

    if set_timing_data.Port == "VIRTUAL" and set_timing_data.Enable is False:
        logging.info(f"Virtual Display is not enumerated on {set_timing_data.Port} port")
        return True


##
# @brief            API to verify multi virtual display
# @param[in]        etl_file           : Name of the ETL file to be verified
# @return           status             : True if verification is passed else False
def verify_multi_virtual_display(etl_file):
    virtual_display_count = 0
    edid_mgmt_display_count = 0
    if etl_parser.generate_report(etl_file) is False:
        logging.error("Failed to generate EtlParser report")
        return False

    ddi_output = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN)
    if ddi_output is None:
        logging.warning("No DDI_SETTIMINGSFROMVIDPN event found in ETLs (Driver Issue)")
        gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} No DDI_SETTIMINGSFROMVIDPN event found in ETLs")
        return False

    ddi_data = ddi_output[-1]

    ##
    # Get all SetTiming events that happened during last DDI_SETTIMINGSFROMVIDPN call
    set_timing_output = etl_parser.get_event_data(
        etl_parser.Events.SET_TIMING, start_time=ddi_data.StartTime, end_time=ddi_data.EndTime)

    if set_timing_output is None:
        logging.error("No SetTiming event found in ETLs (Driver Issue)")
        gdhm.report_driver_bug_os(f"{GDHM_VIRTUAL_ATS} No SetTiming event found in ETLs")
        return False

    for set_timing in set_timing_output:
        if set_timing.Port == "VIRTUAL" and set_timing.Enable is True and set_timing.HActive == 1920 and set_timing.VActive == 1080:
            virtual_display_count += 1
            logging.info("19*10 Virtual Display is enumerated")
        if set_timing.Port == "VIRTUAL" and set_timing.Enable is True and set_timing.HActive == 1920 and set_timing.VActive == 1200:
            edid_mgmt_display_count += 1
            logging.info("19*12 Virtual Display is enumerated [Plugged using LOCK EDID API]")

    if 1 != virtual_display_count:
        logging.error("Number of virtual displays enumerated. Expected: 1, Actual: {display_count}")
        gdhm.report_driver_bug_os(
            f"{GDHM_VIRTUAL_ATS} Number of virtual displays enumerated. Expected: 1, Actual: {virtual_display_count}")
        return False
    if 3 != edid_mgmt_display_count:
        logging.error("Number of edid mgmt displays enumerated. Expected: 3, Actual: {display_count}")
        gdhm.report_driver_bug_os(
            f"{GDHM_VIRTUAL_ATS} Number of edid mgmt displays enumerated. Expected: 3, Actual: {edid_mgmt_display_count}")
        return False

    if MAX_VIRTUAL_DISPLAY_COUNT == virtual_display_count + edid_mgmt_display_count:
        logging.info("Multi Display KVM is successfully enumerated")
        return True
    logging.error("Number of virtual displays enumerated. Expected: 4, Actual: {display_count}")
    gdhm.report_driver_bug_os(
        f"{GDHM_VIRTUAL_ATS} Number of virtual displays enumerated. Expected: 4, Actual: {virtual_display_count + edid_mgmt_display_count}")
    return False


##
# @brief            API to enable disable regkey
# @param[in]        status : Status of the regkey
# @param[in]        delete : Need to delete
# @return           None
def enable_disable_regkey(status=None, delete=False):
    if delete:
        for regkey in RegKeys:
            ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
            registry_access.delete(ss_reg_args, reg_name=regkey)
            logging.info(f"{regkey} deleted")
    else:
        for regkey in RegKeys:
            ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
            registry_access.write(args=ss_reg_args, reg_name=regkey,
                                  reg_type=registry_access.RegDataType.DWORD, reg_value=status)
            logging.info(f"{regkey} is {'Enabled' if status else 'Disabled'}")


#############################################################
# Test Header for Virtual Display test and IDD tests on ATS #
#############################################################

##
# @brief        Initialize test header data
# @param[in]    cmdline_args : Command Line Arguments
# @return       None
def initialize(cmdline_args):
    if reboot_helper.is_reboot_scenario() is True:
        return

    preamble = "\n"
    preamble += test_header.formatted_line_separator()
    preamble += test_header.format_line("TEST ENVIRONMENT DETAILS")
    preamble += test_header.formatted_line_separator()
    now = datetime.datetime.now()

    preamble += test_header.format_line("Execution Start: %s" % now.strftime("%d %B %Y %H:%M:%S %p"))
    if cmdline_args:
        working_path = "Working Path: %s" % os.path.dirname(os.path.abspath(cmdline_args[0]))
        preamble += test_header.format_line(working_path)
        cmd_param_str = " ".join(cmdline_args)
        preamble += test_header.format_line("Command Line Parameters: %s" % cmd_param_str)
    else:
        preamble += test_header.format_line("Command Line Parameters: NO ARGUMENTS")
        preamble += test_header.formatted_line_separator()

    if os.path.isfile(test_header.QUICK_BUILD_VERSION):
        with open(test_header.QUICK_BUILD_VERSION) as f:
            preamble += test_header.format_line("Display Automation Binary Version : %s" % f.readline().strip())

    preamble += test_header.formatted_line_separator()
    execution_env = 'Pre-Si' \
        if system_utility.SystemUtility().get_execution_environment_type() == 'SIMENV_FULSIM' \
        else 'Post-Si'
    preamble += test_header.format_line("{0:^25}: {1}".format("Environment", execution_env))

    obj_machine_info = machine_info.SystemInfo()

    tasks = [
        ('system_info', obj_machine_info._get_system_info, None),
        ('misc_info', test_header.__get_system_info, None),
        ('config_data', test_header.__get_config_data, None),
        ('display_driver_info', obj_machine_info.get_driver_info, machine_info.SystemDriverType.GFX),
        ('audio_driver_info', obj_machine_info.get_driver_info, machine_info.SystemDriverType.AUDIO),
        ('valsim_driver_info', obj_machine_info.get_driver_info, machine_info.SystemDriverType.VALSIM),
    ]

    with futures.ThreadPoolExecutor(max_workers=8) as executor:
        for output in executor.map(test_header.__preamble_runner, tasks):
            if output[0] == 'system_info':
                for info in output[1]:
                    preamble += test_header.format_line(info)
            if output[0] == 'misc_info':
                misc_sys_info = output[1]
                if misc_sys_info is None or len(misc_sys_info.gopVersion) == 0:
                    preamble += test_header.format_line("{0:^25}: {1}".format("GOP/VBIOS Version", None))
                else:
                    preamble += test_header.format_line("{0:^25}: {1}".format("GOP/VBIOS Version",
                                                                              misc_sys_info.get_gop_version()))
            if output[0] == 'config_data':
                preamble += test_header.format_line("{0:^25}: {1}".format("Display Config & Mode", output[1]))

            if output[0] == 'display_driver_info':
                driver_info = output[1]

                preamble += test_header.format_line("{0:^25}: {1}".format("No. of Display Adapters", driver_info.Count))
                preamble += test_header.formatted_line_separator(width=test_header.DEFAULT_LINE_WIDTH)
                header = "{0:18} {1:<16} {2:<9} {3}".format("Service", "Version", "State", "Details & Description")
                preamble += test_header.format_line(header)
                preamble += test_header.formatted_line_separator(separator="-", width=test_header.DEFAULT_LINE_WIDTH)
                preamble += test_header.__print_adapter_information(driver_info)

            if output[0] == 'audio_driver_info':
                preamble += test_header.__print_device_info(output[1], 'Audio')

            if output[0] == 'valsim_driver_info':
                preamble += test_header.__print_device_info(output[1], 'GfxValSimDriver')

    preamble += test_header.formatted_line_separator(width=test_header.DEFAULT_LINE_WIDTH)

    preamble += "\n\n"
    preamble += test_header.formatted_line_separator()
    preamble += test_header.format_line("TEST SCRIPT EXECUTION START")
    preamble += test_header.formatted_line_separator()

    # print platform details on command prompt
    print(preamble)

    file_handle, log_file_path = display_logger._get_file_handle()
    # Python logging FileHandle class will have attribute named baseFilename which stores log file name
    with open(file_handle.baseFilename, 'w') as log_file:
        log_file.write(preamble)
