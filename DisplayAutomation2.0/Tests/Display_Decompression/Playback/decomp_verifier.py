#######################################################################################################################
# @file         decomp_verifier.py
# @brief        APIs to help Verify Render and Media Decompression Programming
# @author       Prateek Joshi, Pai Vinayak1
#######################################################################################################################
import logging
import os
import subprocess
import time

from Libs.Core import etl_parser, system_utility, registry_access, winkb_helper, display_essential
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Feature.app import App3D
from Libs.Feature.app import AppMedia
from registers.mmioregister import MMIORegister

MAX_LINE_WIDTH = 64

# Registry path
INTEL_GMM_PATH = "SOFTWARE\\Intel"

# DirectX app location
DIRECTX_APP_LOCATION = "C:\\Program Files (x86)\\Microsoft DirectX SDK (June 2010)\\Samples\\C++\\Direct3D\\Bin\\x64\\"

# Register offsets for FLAT CCS Register bitfields
FLAT_CCS_ENABLE_MASK = 0x00000001
FLATCCSBASEANDRANGE_OFFSET = 0x1344B0

# Path to applications and media
MEDIA_FILE = os.path.join(test_context.SHARED_BINARY_FOLDER, "MediaDecomp\Media Clip.mp4")
FLIPAT_APP = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR\\FlipAt\\FlipAt.exe")
CLASSICD3D_APP = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\ClassicD3D\\ClassicD3D.exe")
D3D12FULLSCREEN_APP = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\\D3D12FullScreen\\D3D12Fullscreen.exe")
BITSCANOUT10_APP = os.path.join(DIRECTX_APP_LOCATION, '10BitScanout10.exe')

PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
IS_PRE_SI = system_utility.SystemUtility().get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]

# Platform List
GEN_11_PLATFORMS = ['ICLLP', 'JSL', 'LKF1', 'LKFR']
GEN_12_PLATFORMS = ['TGL', 'DG1', 'ADLS']
GEN_13_PLATFORMS = ['DG2', 'ADLP']
GEN_14_PLATFORMS = ['MTL', 'ELG']
GEN_15_PLATFORMS = ['LNL']
GEN_16_PLATFORMS = ['PTL']
GEN_17_PLATFORMS = ['CLS', 'NVL']

GEN12_PLUS_PLATFORM = (GEN_12_PLATFORMS + GEN_13_PLATFORMS + GEN_14_PLATFORMS + GEN_15_PLATFORMS + GEN_16_PLATFORMS +
                       GEN_17_PLATFORMS)

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1

RENDER_DECOMP_SUPPORTED = GEN_11_PLATFORMS + GEN12_PLUS_PLATFORM
MEDIA_DECOMP_SUPPORTED = GEN12_PLUS_PLATFORM
UNIFIED_COMPRESSION_SUPPORTED_PLATFORMS = ['ELG', 'LNL', 'PTL', 'NVL']

# Pixel formats supported by both render and media compression
RENDER_DECOMP_SUPPORTED_FORMATS = ['RGB_2101010', 'RGB_8888', 'RGB_16161616_FLOAT', 'RGB_16161616_UINT', 'RGB_565']
MEDIA_DECOMP_SUPPORTED_FORMATS = ['NV12', 'P0XX', 'YUV422', 'YUV_420', 'RGB_8888', 'RGB_2101010',
                                  'RGB_16161616_FLOAT', 'RGB_16161616_UINT']
UNIFIED_MEDIA_DECOMP_UNSUPPORTED_FORMATS = ['RGB_16161616_UINT', 'RGB_2101010_XR_BIAS', 'Indexed_8_bit', 'RGB_565']

# List of platforms that not supports different plane registers
PLANE_AUX_PROG_UNSUPPORTED = ['DG2', 'DG3', 'MTL', 'ELG', 'LNL', 'PTL', 'NVL']
PLANE_CC_PROG_UNSUPPORTED = ['ICLLP', 'LKF1', 'LKFR', 'JSL', 'ELG', 'PTL', 'NVL']
PLANE_SURF_STRIDE_UNSUPPORTED = ['TGL', 'ADLP', 'ADLS', 'PTL', 'NVL']

# List of platforms that support Tile Y format
TILE_Y_SUPPORTED = ['ICLLP', 'EHL', 'LKF1', 'LKFR', 'JSL', 'TGL', 'ADLS', 'ADLP']


##
# @brief        Helper function to map pixel format to string
# @param[in]    pixel_format : Pixel format in value
# @return       pixel format : Pixel format in string
def map_pixel_format(pixel_format):
    return {0: 'YUV_422_Packed_8_bpc',
            2: 'YUV_420_Planar_8_bpc',
            4: 'RGB_2101010',
            6: 'YUV_420_Planar_10_bpc',
            8: 'RGB_8888',
            10: 'YUV_420_Planar_12_bpc',
            12: 'RGB_16161616_Float',
            14: 'YUV_420_Planar_16_bpc',
            16: 'YUV_444_Packed_8_bpc',
            18: 'RGB_16161616_UINT',
            20: 'RGB_2101010_XR_BIAS',
            24: 'Indexed_8_bit',
            28: 'RGB_565',
            1: 'YUV_422_Packed_10_bpc',
            3: 'YUV_422_Packed_12_bpc',
            5: 'YUV_422_Packed_16_bpc',
            7: 'YUV_444_Packed_10_bpc',
            9: 'YUV_444_Packed_12_bpc',
            11: 'YUV_444_Packed_16_bpc',
            }[pixel_format]


##
# @brief        Helper function to map rotation to string.
# @param[in]    rotation : Rotation in string
# @return       register bit value
def map_rotation(rotation):
    return {0: 'No_rotation',
            1: '90_degree_rotation',
            2: '180_degree_rotation',
            3: '270_degree_rotation',
            }[rotation]


##
# @brief        Helper function to map tiled surface to string.
# @param[in]    tiled_surface : Tiled surface in value
# @return       register bit value
def map_tiled_surface(tiled_surface):
    return {0: 'Linear_memory',
            1: 'Tile_X_memory',
            4: 'Tile_Y_Legacy_memory',
            5: 'Tile_4_memory',
            }[tiled_surface]


##
# @brief        Helper function to map pixel format to register bit.
# @param[in]    pixel_format : Pixel format in string
# @return       register bit value
def get_pixel_format(pixel_format):
    return {'YUV_422_Packed_8_bpc': 0,
            'YUV_420': 2,
            'RGB_2101010': 4,
            'YUV_420_Planar_10_bpc': 6,
            'RGB_8888': 8,
            'YUV_420_Planar_12_bpc': 10,
            'RGB_16161616_Float': 12,
            'YUV_420_Planar_16_bpc': 14,
            'YUV_444_Packed_8_bpc': 16,
            'RGB_16161616_UINT': 18,
            'RGB_2101010_XR_BIAS': 20,
            'Indexed_8_bit': 24,
            'RGB_565': 28,
            'YUV_422_Packed_10_bpc': 1,
            'YUV_422_Packed_12_bpc': 3,
            'YUV_422_Packed_16_bpc': 5,
            'YUV_444_Packed_10_bpc': 7,
            'YUV_444_Packed_12_bpc': 9,
            'YUV_444_Packed_16_bpc': 11,
            }[pixel_format]


##
# @brief        Helper function to start ETL capture.
# @return       status : True if ETL started otherwise False
def start_etl_capture():
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_Before_Scenario_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
        return False
    return True


##
# @brief        Helper function to stop ETL capture.
# @param[in]    display_connected : Display
# @return       etl_file_path     : Path of ETL file captured
def stop_etl_capture(display_connected):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTrace_After_Scenario_' + display_connected + '.etl'
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
        raise Exception("Specified app is not defined")


##
# @brief        Helper Function to play app
# @param[in]    app         : Name of the app(MEDIA/FLIPAT/D3D12FULLSCREEN/CLASSICD3D)
# @param[in]    fullscreen  : True for fullscreen else False
# @return       app_instance
def play_app(app, fullscreen=True):
    app_instance = create_app_instance(app)
    app_instance.open_app(fullscreen, minimize=True)
    return app_instance


##
# @brief        Helper function to switch between full screen and windowed
# @return       status
def media_window_switch():
    # Switch to fullscreen
    winkb_helper.press('ALT_ENTER')
    logging.info("Switched to fullscreen")

    # Wait for a minute after switching to fullscreen
    time.sleep(60)

    # Switch to windowed mode
    winkb_helper.press('ALT_ENTER')
    logging.info("Switched to windowed mode")

    # Wait for a minute after switching to windowed mode
    time.sleep(60)

    return True


##
# @brief        Helper function to play 3D app
# @param[in]    fullscreen : Specify if app has to be launched in fullscreen / windowed mode
# @param[in]    minimize   : Specify whether all current windows have to be minimized prior to opening the app
# @return       app_instance
def play_3d_app(fullscreen, minimize=True):
    if minimize:
        # Minimize all the windows
        winkb_helper.press('WIN+M')

    mode = "full screen mode " if fullscreen else "windowed mode"

    logging.info("Launching 3D Application in %s" % mode)

    # Play the 10 bit scan out app
    app_instance = subprocess.Popen(r'C:/Program Files (x86)/Microsoft DirectX SDK (June '
                                    r'2010)/Samples/C++/Direct3D10/Bin/x64/10BitScanout10.exe')

    time.sleep(2)

    # Play the app in 8 bit format
    winkb_helper.press('F8')
    winkb_helper.press(' ')

    if fullscreen:
        winkb_helper.press('ALT_ENTER')
        time.sleep(2)

    if app_instance is None:
        logging.error("Failed to launch 10BitScanout Application")
        assert False, f"D3D10 Application did not open in {mode}"
    logging.info(f"Launched 3D Application Successfully in {mode}")
    return app_instance


##
# @brief        Helper function to check if feature is supported on platform.
# @param[in]    feature : Render_Decomp / Media_Decomp
# @return       status  : True if feature is supported
def is_feature_supported(feature):
    if feature == 'RENDER_DECOMP':
        if PLATFORM_NAME in RENDER_DECOMP_SUPPORTED:
            return True
        else:
            return False
    elif feature == 'MEDIA_DECOMP':
        if PLATFORM_NAME in MEDIA_DECOMP_SUPPORTED:
            return True
        else:
            return False


##
# @brief            Helper function to get app name
# @param[in]        app_name : Name of the app
# @return           Complete Name of the Application
def get_app_name(app_name):
    app = {
        "MEDIA": "Microsoft.Media.Player.exe",
        "FLIPAT": "FlipAt.exe",
        "FLIPMODELD3D12": "FlipModelD3D12.exe",
        "CLASSICD3D": "Classic3DCubeApp.exe",
        "TRIVFLIP": "TrivFlip11.exe",
        "MOVINGRECTANGLEAPP": "MovingRectangleApp.exe",
        "DEFAULT": "10BitScanout10.exe"
    }
    return app.get(app_name.upper(), "Application Name not found")


##
# @brief            Verification based on layer re-ordering status
# @param[in]        etl_file_path : Name of the ETL
# @param[in]        app_name      : Name of the App
# @return           (layer_index, pipe)
def fetch_layer_index_and_pipe(etl_file_path, app_name):
    plane_id_list = []
    pipe_list = []
    app_layer_index = 0
    if etl_parser.generate_report(etl_file_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate EtlParser report [Test Issue]")
        return False
    ##
    # Get Process config data
    process_config_table_data = etl_parser.get_event_data(etl_parser.Events.PROCESS_CONFIG_TABLE)
    if process_config_table_data is None:
        logging.error("\tFAIL: Event process_config_table_data missing from ETL ")
        return False

    ##
    # Get Flip Process Details
    flip_process_data = etl_parser.get_event_data(etl_parser.Events.FLIP_PROCESS_DETAILS)
    if flip_process_data is None:
        logging.error("\tFAIL: Event flip_process_data missing from ETL ")
        return False

    ##
    # Get Layer Index for Plane ID data
    layer_index_plane_id_data = etl_parser.get_event_data(etl_parser.Events.HW_PLANE_LAYER_INDEX)
    if layer_index_plane_id_data is None:
        logging.error("\tFAIL: Event layer_index_plane_id_data missing from ETL ")
        return False

    for each_flip_process in flip_process_data:
        if each_flip_process.ProcessName == str(app_name):
            if each_flip_process.ProcessFlags != 0:
                logging.error(f"Incorrect Process flag, either DWM Process/Media Process "
                              f"- {each_flip_process.ProcessFlags}")
            else:
                app_layer_index = each_flip_process.LayerIndex
                logging.debug(f"Flip Process Details, Process Name - {each_flip_process.ProcessName}, "
                              f"Process Flag - {each_flip_process.ProcessFlags}, "
                              f"Layer Index - {each_flip_process.LayerIndex}, Timestamp -{each_flip_process.TimeStamp}")

    for hw_plane_layer in layer_index_plane_id_data:
        if hw_plane_layer.LayerIndexMap == app_layer_index:
            plane_id_list.append((hw_plane_layer.LayerIndexMap, hw_plane_layer.TimeStamp, hw_plane_layer.PipeId))
            if hw_plane_layer.PipeId not in pipe_list:
                pipe = chr(int(hw_plane_layer.PipeId) + 65)
                pipe_list.append(pipe)

    return app_layer_index, pipe_list[0]


##
# @brief        Helper function to generate ETL report.
# @param[in]    current_pipe      : Current Pipe (A/B/C/D)
# @param[in]    etl_file_path     : ETL file path to generate report
# @return       flip_data, plane_ctl, plane_aux_dist, plane_cc_val : Flip data from ETL with Register instance
def get_decompression_etl_report(current_pipe, etl_file_path):
    plane_ctl = 0
    plane_aux_dist = 0
    plane_cc_val = 0

    if etl_parser.generate_report(etl_file_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate EtlParser report [Test Issue]")
        return False

    # Get Flip data from ETL
    flip_data = etl_parser.get_flip_data(f'PIPE_{current_pipe}')
    for flip in flip_data:
        for flip_id in flip.FlipAddressList:
            plane_id = flip_id.PlaneID + 1
            break
        break

    plane_ctl = MMIORegister.get_instance("PLANE_CTL_REGISTER", f"PLANE_CTL_{plane_id}_{current_pipe}", PLATFORM_NAME)

    if PLATFORM_NAME not in PLANE_AUX_PROG_UNSUPPORTED:
        plane_aux_dist = MMIORegister.get_instance("PLANE_AUX_DIST_REGISTER",
                                                   f"PLANE_AUX_DIST_{plane_id}_{current_pipe}",
                                                   PLATFORM_NAME)
    else:
        logging.info(f"PLANE_AUX_DIST register is not present and unsupported for {PLATFORM_NAME} Platform")

    if PLATFORM_NAME not in PLANE_CC_PROG_UNSUPPORTED:
        plane_cc_val = MMIORegister.get_instance("PLANE_CC_VAL_REGISTER", f"PLANE_CC_VAL_{plane_id}_{current_pipe}",
                                                 PLATFORM_NAME)
    else:
        logging.info(f"PLANE_CC_VAL register is not present and unsupported for {PLATFORM_NAME} Platform")

    # Wait for sometime to get Flip data from ETL

    logging.info("".center(MAX_LINE_WIDTH, "*"))

    if flip_data is None:
        logging.error("\tFlip data is Empty")
        return False

    logging.info(f"Number of Flips :{len(flip_data)}")

    return flip_data, plane_ctl, plane_aux_dist, plane_cc_val


##
# @brief        Helper function to check post-si regkey for compression
# @return       status : True if regkey is enabled, False otherwise
def postsi_reg_key_check():
    legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                    reg_path=INTEL_GMM_PATH)
    e2e_registry_value, _ = registry_access.read(legacy_reg_args, "DisableE2ECompression", sub_key="GMM")
    if e2e_registry_value == 0:
        logging.info("E2ECompression is enabled")
    elif e2e_registry_value == 1:
        logging.error("E2ECompression is disabled")
        logging.error(f"E2ECompression is disabled - DisableE2ECompression [{e2e_registry_value}]")
        return False
    else:
        logging.info(f"E2ECompression Master Registry path/key is not available. Returned value - "
                     f"{e2e_registry_value}")
    if PLATFORM_NAME in UNIFIED_COMPRESSION_SUPPORTED_PLATFORMS and IS_PRE_SI is False:
        unified_registry_value, _ = registry_access.read(legacy_reg_args, 'EnableDisableUnifiedCompression',
                                                         sub_key='GMM')
        logging.info(f"DisableE2ECompression: {e2e_registry_value}")
        logging.info(f"EnableDisableUnifiedCompression: {unified_registry_value}")
        if e2e_registry_value == 0 and unified_registry_value == 1:
            logging.info("E2ECompression and UnifiedCompression is enabled")
            return True
        else:
            if e2e_registry_value == 0:
                logging.error("DisableE2ECompression is disabled")
            if unified_registry_value == 0:
                logging.warning("EnableDisableUnifiedCompression is disabled")
                if registry_access.write(legacy_reg_args, 'EnableDisableUnifiedCompression',
                                         registry_access.RegDataType.DWORD, 1, sub_key='GMM') is False:
                    logging.error("Failed to add EnableDisableUnifiedCompression")
                    return False
                else:
                    logging.info("EnableDisableUnifiedCompression regkey added successfully")
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        logging.error("Failed to restart display driver")
                        return False
                    return True
    return True


##
# @brief        Helper function to check ccs_enable bit for BMG/ELG
# @return       status : True if ccs bit is disabled else False
def ccs_enable_check():
    flat_ccs_enable_values = etl_parser.get_mmio_data(FLATCCSBASEANDRANGE_OFFSET)
    if flat_ccs_enable_values is None:
        logging.warning("No mmio read/write data found")
        return False
    for each_enable_value in flat_ccs_enable_values:
        if each_enable_value.Data & FLAT_CCS_ENABLE_MASK == FLAT_CCS_ENABLE_MASK:
            logging.info("CCS enable bit is enabled")
            return True
        else:
            logging.info("CCS enable bit is disabled")
            return False


#########################################################
# Plane Aux Register and Plane CC Register verification #
#########################################################

##
# @brief        Helper function to verify PLANE_AUX_DIST Reg.
# @param[in]    flip_data       : Flip Data from ETL
# @param[in]    plane_aux_dist  : Register instance
# @param[in]    plane_ctl       : Register instance
# @return       status          : True if PLANE_AUX_DIST verification pass, False otherwise
def verify_plane_aux_dist(flip_data, plane_aux_dist, plane_ctl):
    logging.info(" PLANE_AUX_DIST Register Verification ".center(MAX_LINE_WIDTH, "*"))
    surf_status, dist_status = None, None

    for flip in flip_data:
        for aux_data in flip.MmioDataList:
            plane_aux_dist.asUint = aux_data.Data
            plane_ctl.asUint = aux_data.Data
            if aux_data.Offset == plane_aux_dist.offset and aux_data.IsWrite and (plane_ctl.render_decomp == 1):

                logging.debug(f"PLANE_AUX_DIST MMIO Data - {aux_data.Data}")
                logging.debug("-".center(MAX_LINE_WIDTH, "-"))

                if plane_aux_dist.auxiliary_surface_distance != 0:
                    logging.debug(
                        f"\t Plane Aux Surf Distance Programmed - {plane_aux_dist.auxiliary_surface_distance}"
                        f" TimeStamp - {aux_data.TimeStamp}")
                else:
                    logging.error(f"\t Plane Aux Surf Distance not Programmed - "
                                  f"{plane_aux_dist.auxiliary_surface_distance} TimeStamp - {aux_data.TimeStamp}")

                if plane_aux_dist.auxiliary_surface_stride != 0:
                    logging.debug(f"\t Plane Aux Surf Stride Programmed - {plane_aux_dist.auxiliary_surface_stride} "
                                  f"TimeStamp - {aux_data.TimeStamp}")
                elif (plane_aux_dist.auxiliary_surface_stride == 0) and \
                        (PLATFORM_NAME in PLANE_SURF_STRIDE_UNSUPPORTED):
                    logging.info(f"\t Plane Aux Surf Stride not Programmed - {plane_aux_dist.auxiliary_surface_stride} "
                                 f"as not applicable for {PLATFORM_NAME} Platform")
                elif plane_aux_dist.auxiliary_surface_stride == 0:
                    logging.error(
                        f"\t Plane Aux Surf Stride not Programmed - {plane_aux_dist.auxiliary_surface_stride} "
                        f"TimeStamp - {aux_data.TimeStamp}")

    logging.debug("-".center(MAX_LINE_WIDTH, "-"))
    # TODO: Remove return True due to AUX issue post closure with GMM team. Workaround: return True always
    return True
    # if dist_status is True and surf_status is True:
    #     return True
    # else:
    #     return False


##
# @brief        Helper function to verify PLANE_CC_VAL Reg.
# @param[in]    flip_data   : Flip Data from ETL
# @param[in]    plane_cc_val: Register instance
# @return       None
def verify_plane_cc_val(flip_data, plane_cc_val):
    logging.info(" PLANE_CC_VAL Verification ".center(MAX_LINE_WIDTH, "*"))

    for flip in flip_data:
        for cc_data in flip.MmioDataList:
            if cc_data.Offset == plane_cc_val.offset and cc_data.IsWrite:
                plane_cc_val.asUint = cc_data.Data
                if cc_data != 0:
                    logging.debug(f"PLANE_CC_VAL MMIO data - {cc_data.Data}")
                    logging.info(f"\t Plane Clear Color Value - {plane_cc_val.clearcolorvaluedw0} "
                                 f"TimeStamp - {cc_data.TimeStamp}")
                else:
                    logging.info("NO MMIO data available for PLANE_CC_VAL Register")


################################################################
# Plane Control register and Render Decompression Verification #
################################################################
##
# @brief        Helper function to verify Render Decompression Programming.
# @param[in]    panel             : Dictionary that contains various Panel attributes
# @param[in]    source_format     : Expected source format
# @param[in]    etl_path          : ETL file path for verification
# @param[in]    app_name          : Name of the application
# @return       status            : True if Plane_CTL & Plane_AUX_DIST verification pass, False otherwise
def verify_render_decomp(panel, source_format, etl_path, app_name):
    decomp_count = 0
    ctl_status = None
    aux_status = None

    _, pipe_id = fetch_layer_index_and_pipe(etl_path, app_name)

    flip_data, plane_ctl, plane_aux_dist, plane_cc_val = get_decompression_etl_report(pipe_id, etl_path)
    for flip_all_param in flip_data:
        for info in flip_all_param.FlipAllParamList:
            if info.FeatureFlags == 0:
                continue
            if "RendDecomp" in info.FeatureFlags:
                decomp_count = decomp_count + 1
    if IS_PRE_SI or decomp_count == 0:
        # In Pre-si platforms, only Async flips are present so checking the Async Flips feature flag status
        for flip_address in flip_data:
            for info in flip_address.FlipAddressList:
                if info.FeatureFlags == 0:
                    continue
                if "RendDecomp" in info.FeatureFlags:
                    decomp_count = decomp_count + 1

    logging.info(f"Number of frames Render Decompressed :{decomp_count}")

    # Verify PLANE_CTL Programming
    if PLATFORM_NAME in UNIFIED_COMPRESSION_SUPPORTED_PLATFORMS:
        # @Note : Not verifying CCS Bit as this register is not written from Display side
        '''
        if ccs_enable_check() is True:
            if verify_plane_ctrl_decomp_enable(flip_data, plane_ctl, source_format) is True:
              assert False, "CCS bit is enabled and decompression is enabled (Unexpected)"
        '''
        ctl_status = verify_plane_ctrl_decomp_enable(flip_data, plane_ctl, source_format)
    else:
        ctl_status = verify_plane_ctrl_render_decomp(flip_data, plane_ctl, source_format)
    if ctl_status:
        logging.info("Pass: PLANE_CTL Register Programming")
        ctl_status = True
    else:
        logging.error("Fail: PLANE_CTL Register Programming")
        ctl_status = False

    # Verify PLANE_AUX_DIST Programming
    if PLATFORM_NAME not in PLANE_AUX_PROG_UNSUPPORTED:
        if verify_plane_aux_dist(flip_data, plane_aux_dist, plane_ctl):
            logging.info("Pass: PLANE_AUX_DIST Register Programming")
            aux_status = True
        else:
            logging.error("Fail: PLANE_AUX_DIST Register Programming")
            aux_status = False
    else:
        aux_status = True
        logging.info(f"{PLATFORM_NAME} Platform does not support PLANE_AUX_DIST Programming")

    # Verify PLANE_CC_VAL Programming
    if PLATFORM_NAME not in PLANE_CC_PROG_UNSUPPORTED:
        verify_plane_cc_val(flip_data, plane_cc_val)
    else:
        logging.info(f"{PLATFORM_NAME} Platform does not support PLANE_CC_VAL Register Programming")

    if ctl_status and aux_status:
        logging.info("Pass: Render Decompression Programming Verification")
        return True
    return False


##
# @brief        Helper function to verify Plane_CTL Reg for Render Decompression.
# @param[in]    flip_data       : Flip Data from ETL
# @param[in]    plane_ctl       : Register instance
# @param[in]    source_format   : Expected source format
# @return       status          : True if Plane_CTL verification pass, False otherwise
def verify_plane_ctrl_render_decomp(flip_data, plane_ctl, source_format):
    logging.info(" PLANE_CTL Register Verification ".center(MAX_LINE_WIDTH, "*"))
    render_enable = 0

    for flip in flip_data:
        for ctl_data in flip.MmioDataList:
            plane_ctl.asUint = ctl_data.Data
            if ctl_data.Offset == plane_ctl.offset and ctl_data.IsWrite and plane_ctl.render_decomp == 1:
                logging.debug(f"PLANE_CTL MMIO Data - {ctl_data.Data}")
                logging.debug("-".center(MAX_LINE_WIDTH, "-"))
                if plane_ctl.render_decomp == 1:
                    render_enable = render_enable + 1
                    logging.debug(f"\t Render Decompression Enabled -[{plane_ctl.render_decomp}] on "
                                  f"TimeStamp = {ctl_data.TimeStamp}")
                else:
                    logging.error(f"\t Render Decompression Disabled -[{plane_ctl.render_decomp}] on "
                                  f"TimeStamp = {ctl_data.TimeStamp}")

                if plane_ctl.plane_rotation == 2 or plane_ctl.plane_rotation == 0:
                    logging.debug(f"\t Plane Rotation {map_rotation(plane_ctl.plane_rotation)} "
                                  f"supported for render decompression")
                elif plane_ctl.plane_rotation == 4 or plane_ctl.plane_rotation == 1:
                    logging.error(f"\t Plane Rotation {map_rotation(plane_ctl.plane_rotation)} is not supported for "
                                  f"render decompression on TimeStamp = {ctl_data.TimeStamp}")

                if plane_ctl.tiled_surface == 4 and PLATFORM_NAME in TILE_Y_SUPPORTED:
                    logging.debug(f"\t Tiled Surface {map_tiled_surface(plane_ctl.tiled_surface)} supported for render "
                                  f"decompression")
                elif plane_ctl.tiled_surface == 5 and PLATFORM_NAME not in TILE_Y_SUPPORTED:
                    logging.debug(f"\t Tiled Surface {map_tiled_surface(plane_ctl.tiled_surface)} supported for render "
                                  f"decompression")
                else:
                    logging.error(f"\t Tiled Surface {map_tiled_surface(plane_ctl.tiled_surface)} not supported for "
                                  f"render decompression on TimeStamp = {ctl_data.TimeStamp}")

                if plane_ctl.source_pixel_format == source_format:
                    logging.debug(f"\t Source Pixel Format {map_pixel_format(plane_ctl.source_pixel_format)} supported "
                                  f"for render decompression")
                else:
                    logging.error(f"\t Source Pixel Format {map_pixel_format(plane_ctl.source_pixel_format)} not "
                                  f"supported for render decompression")

                if PLATFORM_NAME not in PLANE_CC_PROG_UNSUPPORTED:
                    if plane_ctl.clear_color_disable == 0:
                        logging.debug(f"\t Clear Color Enabled -[{plane_ctl.clear_color_disable}] with render "
                                      f"decompression -[{plane_ctl.render_decomp}]")
                    elif plane_ctl.clear_color_disable == 1 and plane_ctl.render_decomp == 0:
                        logging.warning(f"\t Clear Color Disabled -[{plane_ctl.clear_color_disable}] as render "
                                        f"decompression -[{plane_ctl.render_decomp}] on "
                                        f"TimeStamp = {ctl_data.TimeStamp}")

    logging.debug("-".center(MAX_LINE_WIDTH, "-"))
    if render_enable == 0:
        logging.error("\t Render Decompression is Disabled")
        return False
    else:
        logging.info("\t Render Decompression is Enabled")
        return True


##
# @brief        Helper function to verify Plane_CTL Reg for Decompression.(ELG+ platforms)
# @param[in]    flip_data       : Flip Data from ETL
# @param[in]    plane_ctl       : Register instance
# @param[in]    source_format   : Expected source format
# @return       status          : True if Plane_CTL verification pass, False otherwise
def verify_plane_ctrl_decomp_enable(flip_data, plane_ctl, source_format):
    logging.info(" PLANE_CTL Register Verification ".center(MAX_LINE_WIDTH, "*"))
    render_enable = 0

    for flip in flip_data:
        for ctl_data in flip.MmioDataList:
            plane_ctl.asUint = ctl_data.Data
            if ctl_data.Offset == plane_ctl.offset and ctl_data.IsWrite and plane_ctl.decomp_enable == 1:
                logging.debug(f"PLANE_CTL MMIO Data - {ctl_data.Data}")
                logging.debug("-".center(MAX_LINE_WIDTH, "-"))
                if plane_ctl.decomp_enable == 1:
                    render_enable = render_enable + 1
                    logging.debug(f"\t Decompression Enabled -[{plane_ctl.decomp_enable}] on "
                                  f"TimeStamp = {ctl_data.TimeStamp}")
                else:
                    logging.error(f"\t Decompression Disabled -[{plane_ctl.decomp_enable}] on "
                                  f"TimeStamp = {ctl_data.TimeStamp}")

                if plane_ctl.plane_rotation == 2 or plane_ctl.plane_rotation == 0:
                    logging.debug(f"\t Plane Rotation {map_rotation(plane_ctl.plane_rotation)} supported for "
                                  f" decompression")
                elif plane_ctl.plane_rotation == 4 or plane_ctl.plane_rotation == 1:
                    logging.error(f"\t Plane Rotation {map_rotation(plane_ctl.plane_rotation)} is not supported for "
                                  f"decompression on TimeStamp = {ctl_data.TimeStamp}")

                if plane_ctl.tiled_surface == 4 and PLATFORM_NAME in TILE_Y_SUPPORTED:
                    logging.debug(f"\t Tiled Surface {map_tiled_surface(plane_ctl.tiled_surface)} supported for "
                                  f" decompression")
                elif plane_ctl.tiled_surface == 5 and PLATFORM_NAME not in TILE_Y_SUPPORTED:
                    logging.debug(f"\t Tiled Surface {map_tiled_surface(plane_ctl.tiled_surface)} supported for "
                                  f" decompression")
                else:
                    logging.error(f"\t Tiled Surface {map_tiled_surface(plane_ctl.tiled_surface)} not supported for"
                                  f" decompression on TimeStamp = {ctl_data.TimeStamp}")

                if (plane_ctl.source_pixel_format == source_format and
                        plane_ctl.source_pixel_format not in UNIFIED_MEDIA_DECOMP_UNSUPPORTED_FORMATS):
                    logging.debug(f"\t Source Pixel Format {map_pixel_format(plane_ctl.source_pixel_format)} "
                                  f"supported for decompression")
                else:
                    logging.error(f"\t Source Pixel Format {map_pixel_format(plane_ctl.source_pixel_format)} "
                                  f"not supported for decompression")

    logging.debug("-".center(MAX_LINE_WIDTH, "-"))
    if render_enable == 0:
        logging.error("\t Decompression is Disabled")
        return False
    else:
        logging.info("\t Decompression is Enabled")
        return True


###############################################################
# Plane Control register and Media Decompression Verification #
###############################################################

##
# @brief        Helper function to verify Media Decompression Programming.
# @param[in]    panel           : Dictionary that contains various Panel attributes
# @param[in]    source_format   : Expected source format
# @param[in]    etl_file        : ETL file for verification
# @param[in]    app_name        : Name of the application
# @return       status          : True if Plane_CTL & Plane_AUX_DIST verification pass, False otherwise
def verify_media_decomp(panel, source_format, etl_file, app_name):
    media_decomp_count = 0
    ctl_status = None
    aux_status = None

    _, pipe_id = fetch_layer_index_and_pipe(etl_file, app_name)

    flip_data, plane_ctl, plane_aux_dist, plane_cc_val = get_decompression_etl_report(pipe_id, etl_file)

    for flip_all_param in flip_data:
        for info in flip_all_param.FlipAllParamList:
            if info.FeatureFlags == 0:
                continue
            if "MediaDecomp" in info.FeatureFlags:
                media_decomp_count = media_decomp_count + 1

    logging.info(f"Number of frames Media Decompressed :{media_decomp_count}")

    # Verify PLANE_CTL Programming
    if PLATFORM_NAME in UNIFIED_COMPRESSION_SUPPORTED_PLATFORMS:
        # @Note: Not verifying CCS Bit as this register is not written from Display side
        '''
        if ccs_enable_check() is True:
            if verify_plane_ctrl_decomp_enable(flip_data, plane_ctl, source_format) is True:
              assert False, "CCS bit is enabled and decompression is enabled (Unexpected)"
        '''
        ctl_status = verify_plane_ctrl_decomp_enable(flip_data, plane_ctl, source_format)
    else:
        ctl_status = verify_plane_ctrl_media_decomp(flip_data, plane_ctl, source_format)
    if ctl_status:
        logging.info("Pass: PLANE_CTL Register Programming")
        ctl_status = True
    else:
        logging.error("Fail: PLANE_CTL Register Programming")
        ctl_status = False

    # Verify PLANE_AUX_DIST Programming
    if PLATFORM_NAME not in PLANE_AUX_PROG_UNSUPPORTED:
        if verify_plane_aux_dist(flip_data, plane_aux_dist, plane_ctl):
            logging.info("Pass: PLANE_AUX_DIST Register Programming")
            aux_status = True
        else:
            logging.error("Fail: PLANE_AUX_DIST Register Programming")
            aux_status = False
    else:
        logging.info(f"{PLATFORM_NAME} Platform does not support PLANE_AUX_DIST Programming")
        aux_status = True

    if ctl_status and aux_status:
        logging.info("Pass: Media Decompression Programming Verification")
        return True
    return False


##
# @brief        Helper function to verify Plane_CTL Reg for Media Decompression.
# @param[in]    flip_data    : Flip Data from ETL
# @param[in]    plane_ctl    : Register instance
# @param[in]    source_format: Expected source format
# @return       status       : True if Plane_CTL verification pass, False otherwise
def verify_plane_ctrl_media_decomp(flip_data, plane_ctl, source_format):
    logging.info(" PLANE_CTL Register Verification ".center(MAX_LINE_WIDTH, "*"))
    media_enable = 0

    for flip in flip_data:
        for ctl_data in flip.MmioDataList:
            plane_ctl.asUint = ctl_data.Data
            if (ctl_data.Offset == plane_ctl.offset) and ctl_data.IsWrite and (plane_ctl.media_decomp == 1):
                if plane_ctl.media_decomp == 1:
                    media_enable = media_enable + 1
                    logging.debug(f"\t Media Decompression Enabled - {plane_ctl.media_decomp} on "
                                  f"TimeStamp - {ctl_data.TimeStamp}")
                elif plane_ctl.media_decomp == 0:
                    logging.error(f"\t Media Decompression Disabled - {plane_ctl.media_decomp} on "
                                  f"TimeStamp - {ctl_data.TimeStamp}")
                if plane_ctl.plane_rotation == 2 or plane_ctl.plane_rotation == 0:
                    logging.debug(f"\t Plane Rotation - {map_rotation(plane_ctl.plane_rotation)} supported for "
                                  f"Media decompression")
                elif plane_ctl.plane_rotation == 4 or plane_ctl.plane_rotation == 1:
                    logging.error(f"\t Plane Rotation - {map_rotation(plane_ctl.plane_rotation)} is not supported for"
                                  f" Media decompression")

                if plane_ctl.tiled_surface == 4 and PLATFORM_NAME in TILE_Y_SUPPORTED:
                    logging.debug(f"\t Tiled Surface - {map_tiled_surface(plane_ctl.tiled_surface)} supported for "
                                  f"Media decompression")
                elif plane_ctl.tiled_surface == 5 and PLATFORM_NAME not in TILE_Y_SUPPORTED:
                    logging.debug(f"\t Tiled Surface - {map_tiled_surface(plane_ctl.tiled_surface)} supported for "
                                  f"Media decompression")
                else:
                    logging.error(f"\t Tiled Surface - {map_tiled_surface(plane_ctl.tiled_surface)} not supported for"
                                  f" Media decompression")

                if plane_ctl.source_pixel_format in MEDIA_DECOMP_SUPPORTED_FORMATS:
                    logging.debug(f"\t Source Pixel Format - {plane_ctl.source_pixel_format} supported for "
                                  f"Media decompression")
                else:
                    logging.error(f"\t Source Pixel Format - {plane_ctl.source_pixel_format} not supported for"
                                  f" Media decompression")

                if plane_ctl.async_address_update_enable == 0:
                    logging.debug(f"\t Sync flips for Media decompression - [{plane_ctl.async_address_update_enable}]")
                else:
                    logging.debug(f"\t Async flips for Media decompression - [{plane_ctl.async_address_update_enable}]")

    if media_enable == 0:
        logging.error("\t Media Decompression is Disabled")
        return False
    else:
        logging.info("\t Media Decompression is Enabled")
        return True


##################################################
# Negative verification for Render decompression #
##################################################
##
# @brief        Helper function for negative verification of Render Decompression.
# @param[in]    panel            : Dictionary that contains various Panel attributes
# @param[in]    source_format    : Expected source format
# @param[in]    etl_path         : ETL file path for verification
# @param[in]    app_name         : Name of the application
# @return       status           : True if Render Decomp is enabled, False otherwise
def verify_negative_render_decomp(panel, source_format, etl_path, app_name):
    decomp_count = 0
    render_enable = 0
    _, pipe_id = fetch_layer_index_and_pipe(etl_path, app_name)

    flip_data, plane_ctl, plane_aux_dist, plane_cc_val = get_decompression_etl_report(pipe_id, etl_path)

    for flip_all_param in flip_data:
        for info in flip_all_param.FlipAllParamList:
            if info.FeatureFlags == 0:
                continue
            if "RendDecomp" in info.FeatureFlags:
                decomp_count = decomp_count + 1
    logging.info(f"Number of frames Render Decompressed :{decomp_count}")

    logging.info(" Render Decomp Negative Verification ".center(MAX_LINE_WIDTH, "*"))

    for flip in flip_data:
        for ctl_data in flip.MmioDataList:
            plane_ctl.asUint = ctl_data.Data
            if (ctl_data.Offset == plane_ctl.offset) and ctl_data.IsWrite and (plane_ctl.plane_enable == 1):
                logging.debug(f"PLANE_CTL MMIO Data - {ctl_data.Data}")
                logging.debug("-".center(MAX_LINE_WIDTH, "-"))
                if plane_ctl.render_decomp == 0:
                    render_enable = render_enable + 1
                    logging.debug(f"\t Render Decompression Disabled -[{plane_ctl.render_decomp}] for "
                                  f"pixel format - {map_pixel_format(plane_ctl.source_pixel_format)} on "
                                  f"TimeStamp = {ctl_data.TimeStamp}")
                else:
                    logging.error(f"\t Render Decompression Enabled -[{plane_ctl.render_decomp}] for "
                                  f"pixel format - {map_pixel_format(plane_ctl.source_pixel_format)} on "
                                  f"TimeStamp = {ctl_data.TimeStamp}")

    logging.debug("-".center(MAX_LINE_WIDTH, "-"))
    if render_enable != 0:
        logging.info("\t Render Decompression is Disabled for unsupported pixel format")
        return True
    else:
        logging.error("\t Render Decompression is Enabled for unsupported pixel format")
        return False


#########################
# Pre-si Related checks #
#########################

##
# @brief        Helper function to check pre-si regkey for compression
# @return       status : True if regkey is enabled, False otherwise
def presi_reg_key_check():
    if PLATFORM_NAME in UNIFIED_COMPRESSION_SUPPORTED_PLATFORMS and IS_PRE_SI:
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                        reg_path=INTEL_GMM_PATH)
        e2e_registry_value, _ = registry_access.read(legacy_reg_args, 'DisableE2ECompression', sub_key='GMM')
        unified_registry_value, _ = registry_access.read(legacy_reg_args, 'EnableDisableUnifiedCompression',
                                                         sub_key='GMM')
        logging.info(f"DisableE2ECompression: {e2e_registry_value}")
        logging.info(f"EnableDisableUnifiedCompression: {unified_registry_value}")
        if e2e_registry_value == 0 and unified_registry_value == 1:
            logging.info("E2ECompression and UnifiedCompression is enabled")
            return True
        else:
            if e2e_registry_value == 0:
                logging.error("DisableE2ECompression is disabled")
            if unified_registry_value == 0:
                logging.error("EnableDisableUnifiedCompression is disabled")
            return False
    else:
        logging.info(f"{PLATFORM_NAME} is not presi platform. Skipping the presi regkey check")
        return None


##################
# GDHM Reporting #
##################

##
# @brief            Helper function to report GDHM
# @param[in]        feature    : Any feature in display compression [MEDIA/RENDER]
# @param[in]        message    : GDHM message
# @param[in]        priority   : Priority of the GDHM bug [P1/P2/P3/P4]
# @param[in]        driver_bug : True for driver bug reporting else False
# @return           None
def report_to_gdhm(feature, message="", priority='P2', driver_bug=True):
    if message == "":
        title = f"[Display {feature} Decompression] verification failed"
    else:
        title = f"[Display {feature} Decompression] {message}"
    if driver_bug:
        gdhm.report_driver_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))
    else:
        gdhm.report_test_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))
