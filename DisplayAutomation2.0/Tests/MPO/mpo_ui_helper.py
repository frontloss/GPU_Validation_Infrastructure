########################################################################################################################
# @file         mpo_ui_helper.py
# @brief        The script implements common helper functions given below that will be used by MPO test scripts:
#               * To Play media, launch D3D12Fullscreen and Maps application.
#               * Get the pixel format value based on command line argument.
#               * Get the pixel format string for logging.
#               * Get plane status string for logging.
#               * Get pipe details.
#               * Verify plane programming, plane status.
#               * Verify plane programming for MST and SST.
#               * Get the display configuration.
#               * Get display type from the connector port.
#               * Base classes and associated functions for different app types
# @author       Shetty, Anjali N, Gopikrishnan R
########################################################################################################################
import importlib
import logging
import os
import time
from collections import OrderedDict

import win32api
import win32con
import win32gui

from Libs.Core import enum, window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Feature.app import AppMedia, App3D
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.mmioregister import MMIORegister

media_test = False


##
# @brief            Decorator to retry verification in case of plane verification failures
# @param[in]        func
# @return		    status, bool, True or False
def retry_mpo_verification(func):
    global media_test

    def check_if_error(*args, **kwargs):
        content_type = args[-2]
        test_instance = args[-1]

        if content_type == 'D3D12':
            status = func(*args, **kwargs)
            logging.info(f'Verification Status: {status}')
            # 1st time failure check
            if status:
                return True
            # Checking if D3D12 app is active
            else:
                if test_instance.mpo_helper.app3d.hwnd is not None:
                    test_instance.mpo_helper.app3d.maximise()
                    time.sleep(5)
                    status = func(*args, **kwargs)
                    logging.info(f'Verification Status: {status}')
                    # 2nd time failure check
                    if status:
                        return True
                    else:
                        raise Exception("Plane Verification Failure")
                else:
                    # Retrying to open app
                    test_instance.mpo_helper.play_3d_app(False)
                    logging.info(f'App Handle after reopening: {test_instance.mpo_helper.app3d.hwnd}')
                    time.sleep(5)
                    if test_instance.mpo_helper.app3d.hwnd is not None:
                        test_instance.mpo_helper.app3d.maximise()
                        time.sleep(5)
                        status = func(*args, **kwargs)
                        logging.info(f'Verification Status: {status}')
                        # 2nd time failure check
                        if status:
                            return True
                        else:
                            raise Exception("Plane Verification Failure")
                    else:
                        logging.error("D3D12 app is not active")
                        raise Exception("Plane Verification Failure")
        else:
            app_media = AppMedia(os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_1920_1080_avc.mp4"))
            status = func(*args, **kwargs)
            logging.info(f'Verification Status: {status}')
            # 1st time failure check
            if status:
                return True
            else:
                status = app_media.check_app_status_and_controls()
                # 2nd time failure check
                if status:
                    logging.info(f'Retry plane verification')
                    status = func(*args, **kwargs)
                    # 2nd time failure check
                    if status:
                        return True
                    else:
                        raise Exception("Plane verification Failure")

                else:
                    logging.error("Media app is not active")
                    raise Exception("Plane verification failed as Media App is not active")

    return check_if_error


##
# @brief    Contains helper functions that will be used by MPO test scripts
class MPOUIHelper(object):
    platform = []
    os_info = None
    machine_info = SystemInfo()
    config = DisplayConfiguration()
    app3d = None
    stepCounter = 0

    ##
    # @brief            Helper function to get platform and OS details
    # @return		    void
    def get_platform_os(self):
        ##
        # Get the machine info
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        for i in range(len(gfx_display_hwinfo)):
            self.platform.append(str(gfx_display_hwinfo[i].DisplayAdapterName).lower())
        self.os_info = self.machine_info.get_os_info()

    ##
    # @brief            Helper function to get the step value for logging
    # @return           Step count
    def getStepInfo(self):
        self.stepCounter = self.stepCounter + 1
        return "STEP-%d: " % self.stepCounter

    ##
    # @brief            Helper function to play media
    # @param[in]        media_file  : Path to the media file
    # @param[in]	    bfullscreen : Mode in which 3D application to be launched.
    # @return		    void
    def play_media(self, media_file, bfullscreen):
        global media_test
        media_test = True
        self.app_media = AppMedia(media_file)
        self.app_media.open_app(bfullscreen, minimize=True)
        media_window_handle = self.app_media.instance

        if media_window_handle is None:
            gdhm.report_bug(
                title="[MPO] Media Application didn't open",
                problem_classification=gdhm.ProblemClassification.APP_CRASH,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return media_window_handle

    ##
    # @brief            Helper function to launch D3D12Fullscreen application.
    # @param[in]	    bfullscreen : Mode in which 3D application to be launched.
    # @return		    void
    def play_3d_app(self, bfullscreen):
        self.app3d = App3D("D3D12FULLSCREEN", os.path.join(
            os.getcwd()[:2] + r'/SHAREDBINARY/920697932/MPO/D3D12FullScreen/D3D12Fullscreen.exe'),
                           os.path.join(test_context.SHARED_BINARY_FOLDER))
        self.app3d.open_app(bfullscreen, minimize=True)
        mode = "full screen mode " if bfullscreen else "windowed mode"
        logging.info("Launched 3D App successfully in %s" % mode)

    ##
    # @brief            helper function to get the pixel format value based on command line argument
    # @param[in]	    pixel_format : Pixel format of the plane
    # @return		    Value of pixel format
    def get_pixel_format_value(self, pixel_format):
        return {
            'YUV422_8BPC': 0,
            'YUV422_10BPC': 1,
            'YUV420_8BPC': 2,
            'YUV422_12BPC': 3,
            'RGB2101010': 4,
            'YUV422_16BPC': 5,
            'YUV420_10BPC': 6,
            'YUV444_10BPC': 7,
            'RGB8888': 8,
            'YUV444_12BPC': 9,
            'YUV420_12BPC': 10,
            'YUV444_16BPC': 11,
            'RGB16_FLOAT': 12,
            'YUV420_16BPC': 14,
            'YUV444_8BPC': 16,
            'RGB16_UINT': 18,
            'RGB2101010_XRBIAS': 20,
            'INDEXED_8BIT': 24,
            'RGB565': 28
        }[pixel_format]

    ##
    # @brief            helper function to get the pixel format string for logging
    # @param[in]	    pixel_format : Pixel format of the plane
    # @return		    Pixel format string for the given pixel format
    def get_pixel_format_string(self, pixel_format):
        return {
            0: 'YUV422_8BPC',
            1: 'YUV422_10BPC',
            2: 'YUV420_8BPC',
            3: 'YUV422_12BPC',
            4: 'RGB2101010',
            5: 'YUV422_16BPC',
            6: 'YUV420_10BPC',
            7: 'YUV444_10BPC',
            8: 'RGB8888',
            9: 'YUV444_12BPC',
            10: 'YUV420_12BPC',
            11: 'YUV444_16BPC',
            12: 'RGB16_FLOAT',
            14: 'YUV420_16BPC',
            16: 'YUV444_8BPC',
            18: 'RGB16_UINT',
            20: 'RGB2101010_XRBIAS',
            24: 'INDEXED_8BIT',
            28: 'RGB565'
        }[pixel_format]

    ##
    # @brief            Helper function to get the pixel format string for logging for legacy platforms
    # @param[in]	    pixel_format : Pixel format of the plane
    # @return		    Pixel format string for the given pixel format
    def get_pixel_format_string_legacy(self, pixel_format):
        return {
            0: 'YUV422_8BPC',
            1: 'YUV420_8BPC',
            2: 'RGB2101010',
            4: 'RGB8888',
            6: 'RGB16_FLOAT',
            8: 'YUV444_8BPC',
            10: 'RGB2101010_XRBIAS',
            12: 'INDEXED_8BIT',
            14: 'RGB565'
        }[pixel_format]

    ##
    # @brief            helper function to get plane status string for logging
    # @param[in]	    plane_status : Plane status value
    # @return		    Plane status string
    def get_plane_status_string(self, plane_status):
        return {
            0: 'Plane disabled',
            1: "Plane enabled"
        }[plane_status]

    ##
    # @brief            Helper function to get pipe details for master
    # @param[in]        value : Master select transcoder value
    # @return           Pipe details
    def get_pipe_details(self, value):
        return {
            1: 'A',
            2: 'B',
            3: 'C',
            4: 'D'
        }[value]

    ##
    # @brief        helper function to verify plane programming
    # @param[in]    display               : Display for which planes need to be verified
    # @param[in]    plane_ctl_reg         : Plane to be verified
    # @param[in]	expected_pixel_format : Expected pixel format value
    # @param[in]    gfx_adapter_index     : Adapter details
    # @param[in]    test_instance:        : Instance of the current test under execution
    # @param[in]    content_type          : Type of content
    # @return		Plane verification status
    @retry_mpo_verification
    def verify_planes(self, display, plane_ctl_reg, expected_pixel_format, gfx_adapter_index='gfx_0', content_type=None, test_instance=None):
        reg_read = MMIORegister()

        index = gfx_adapter_index.split('_')
        gfx_index = int(index[1])

        ##
        # Import PLANE_CTL_REGISTER module.
        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % self.platform[gfx_index])
        ##
        # Get current pipe value
        display_base_obj = DisplayBase(display, self.platform[gfx_index], gfx_index=gfx_adapter_index)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display, gfx_adapter_index)
        current_pipe = chr(int(current_pipe) + 65)

        ##
        # Plane to be verified
        plane_ctl_reg = plane_ctl_reg + '_' + current_pipe

        ##
        # Read PLANE_CTL_REGISTER values.
        plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform[gfx_index], 0x0,
                                        gfx_adapter_index)

        ##
        # Programmed value of plane enable bit.
        plane_enable = plane_ctl_value.__getattribute__("plane_enable")

        ##
        # Verify if plane is enabled.
        if plane_enable:
            logging.info("PASS: {} Plane enable status - Expected: Plane enabled Actual: {}"
                         .format(plane_ctl_reg, self.get_plane_status_string(plane_enable)))

            ##
            # Programmed value of source pixel format.
            programmed_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")

            if (type(expected_pixel_format) == str):
                pixel_format = getattr(plane_ctl, expected_pixel_format)
                if programmed_pixel_format == pixel_format:
                    if self.platform in ['skl', 'kbl', 'cfl', 'cml', 'whl', 'aml', 'glk']:
                        logging.info("PASS: {} Pixel Format - Expected: {} Actual: {}"
                                     .format(plane_ctl_reg, expected_pixel_format.replace('source_pixel_format_', ''),
                                             self.get_pixel_format_string_legacy(programmed_pixel_format)))
                    else:
                        logging.info("PASS: {} Pixel Format - Expected: {} Actual: {}"
                                     .format(plane_ctl_reg, expected_pixel_format.replace('source_pixel_format_', ''),
                                             self.get_pixel_format_string(programmed_pixel_format)))
                else:
                    if self.platform in ['skl', 'kbl', 'cfl', 'cml', 'whl', 'aml', 'glk']:
                        logging.error("FAIL: {}Pixel Format - Expected: {} Actual: {}"
                                      .format(plane_ctl_reg, expected_pixel_format.replace('source_pixel_format_', ''),
                                              self.get_pixel_format_string_legacy(programmed_pixel_format)))
                    else:
                        logging.error("FAIL: {}Pixel Format - Expected: {} Actual: {}"
                                      .format(plane_ctl_reg, expected_pixel_format.replace('source_pixel_format_', ''),
                                              self.get_pixel_format_string(programmed_pixel_format)))
                    return False
            else:
                if programmed_pixel_format == expected_pixel_format:
                    logging.info("PASS: {} Pixel Format - Expected: {} Actual: {}"
                                 .format(plane_ctl_reg, self.get_pixel_format_string(expected_pixel_format),
                                         self.get_pixel_format_string(programmed_pixel_format)))

                else:
                    logging.error("FAIL: {} Pixel Format - Expected: {} Actual: {}"
                                  .format(plane_ctl_reg, self.get_pixel_format_string(expected_pixel_format),
                                          self.get_pixel_format_string(programmed_pixel_format)))
                    return False

        else:
            logging.error("FAIL: {} Plane enable status - Expected: Plane enabled Actual {}"
                          .format(plane_ctl_reg, self.get_plane_status_string(plane_enable)))
            return False

        return True

    ##
    # @brief        Helper function to verify plane status
    # @param[in]    display           : Display for which planes need to be verified
    # @param[in]    plane_ctl_reg     : Plane to be verified
    # @param[in]    gfx_adapter_index : Adapter details
    # @return       Plane status
    @retry_mpo_verification
    def verify_plane_status(self, display, plane_ctl_reg, gfx_adapter_index='gfx_0'):
        reg_read = MMIORegister()

        index = gfx_adapter_index.split('_')
        gfx_index = int(index[1])

        ##
        # Import PLANE_CTL_REGISTER module.
        plane_ctl = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % self.platform[gfx_index])
        ##
        # Get current pipe value
        display_base_obj = DisplayBase(display, self.platform[gfx_index], gfx_index=gfx_adapter_index)
        current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display, gfx_adapter_index)
        current_pipe = chr(int(current_pipe) + 65)

        ##
        # Plane to be verified
        plane_ctl_reg = plane_ctl_reg + '_' + current_pipe

        ##
        # Read PLANE_CTL_REGISTER values.
        plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_reg, self.platform[gfx_index], 0x0)

        ##
        # Programmed value of plane enable bit.
        plane_enable = plane_ctl_value.__getattribute__("plane_enable")

        ##
        # Verify if plane is enabled.
        if plane_enable:
            logging.info("PASS: {} Plane enable status - Expected: Plane enabled Actual: {}"
                         .format(plane_ctl_reg, self.get_plane_status_string(plane_enable)))
        else:
            logging.error("FAIL: {} Plane enable status - Expected: Plane enabled Actual {}"
                          .format(plane_ctl_reg, self.get_plane_status_string(plane_enable)))
            return False
        return True

    ##
    # @brief        Helper function to verify plane programming for MST
    # @param[in]	expected_pixel_format : Expected pixel format value
    # @param[in]    plane_ctl_reg         : Plane to be verified
    # @param[in]    gfx_adapter_index     : Adapter index
    # @return		Plane verification status
    @retry_mpo_verification
    def verify_planes_mst(self, expected_pixel_format, plane_ctl_reg, gfx_adapter_index='gfx_0'):
        reg_read = MMIORegister()

        index = gfx_adapter_index.split('_')
        gfx_index = int(index[1])

        ##
        # Pipe list
        pipe_list = ['A', 'B', 'C', 'D']

        verify_list = []

        dp_mst = 0b011

        for pipe in pipe_list:

            trans_ddi_reg = 'TRANS_DDI_FUNC_CTL_' + pipe
            trans_ddi2_reg = 'TRANS_DDI_FUNC_CTL2_' + pipe
            ##
            # Read TRANS_DDI_FUNC_CTL_REGISTER values.
            trans_ddi_ctl_value = reg_read.read('TRANS_DDI_FUNC_CTL_REGISTER', trans_ddi_reg, self.platform[gfx_index],
                                                0x0)

            ##
            # Read TRANS_DDI_FUNC_CTL2_REGISTER values.
            trans_ddi_ctl2_value = reg_read.read('TRANS_DDI_FUNC_CTL2_REGISTER', trans_ddi2_reg,
                                                 self.platform[gfx_index], 0x0)

            ##
            # Programmed value of plane enable bit.
            trans_enable = trans_ddi_ctl_value.__getattribute__("trans_ddi_function_enable")

            ##
            # Programmed value of port sync mode.
            port_sync_enable = trans_ddi_ctl2_value.__getattribute__("port_sync_mode_enable")

            ##
            # Port sync master
            master_select = trans_ddi_ctl2_value.__getattribute__("port_sync_mode_master_select")

            if trans_enable and dp_mst == trans_ddi_ctl_value.__getattribute__("trans_ddi_mode_select"):
                if port_sync_enable:
                    verify_list.append(pipe)
                if master_select:
                    verify_list.append(self.get_pipe_details(master_select))

        if verify_list:
            for pipe in verify_list:
                ##
                # Plane to be verified
                plane_ctl_register = plane_ctl_reg + '_' + pipe

                ##
                # Read PLANE_CTL_REGISTER values.
                plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_register, self.platform[gfx_index], 0x0)

                ##
                # Programmed value of plane enable bit.
                plane_enable = plane_ctl_value.__getattribute__("plane_enable")

                ##
                # Verify if plane is enabled
                if plane_enable:
                    logging.info("PASS: {} Plane enable status - Expected: Plane enabled Actual: {}"
                                 .format(plane_ctl_register, self.get_plane_status_string(plane_enable)))

                    ##
                    # Programmed value of source pixel format.
                    programmed_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")

                    if programmed_pixel_format == expected_pixel_format:
                        logging.info("PASS: {} Pixel Format - Expected: {} Actual: {}"
                                     .format(plane_ctl_register, self.get_pixel_format_string(expected_pixel_format),
                                             self.get_pixel_format_string(programmed_pixel_format)))

                    else:
                        logging.error("FAIL: {} Pixel Format - Expected: {} Actual: {}"
                                      .format(plane_ctl_register, self.get_pixel_format_string(expected_pixel_format),
                                              self.get_pixel_format_string(programmed_pixel_format)))
                        return False

                else:
                    logging.error("FAIL: {} Plane enable status - Expected: Plane enabled Actual {}"
                                  .format(plane_ctl_register, self.get_plane_status_string(plane_enable)))
                    return False

            return True
        else:
            logging.error("Pipes are not enabled")
            return False

    ##
    # @brief        Helper function to verify plane programming for SST
    # @param[in]	expected_pixel_format : Expected pixel format value
    # @param[in]    plane_ctl_reg         : Plane to be verified
    # @param[in]    gfx_adapter_index     : Adapter index
    # @return		Plane verification status
    @retry_mpo_verification
    def verify_planes_sst(self, expected_pixel_format, plane_ctl_reg, gfx_adapter_index='gfx_0'):
        reg_read = MMIORegister()

        index = gfx_adapter_index.split('_')
        gfx_index = int(index[1])

        ##
        # Pipe list
        pipe_list = ['A', 'B', 'C', 'D']

        verify_list = []

        dp_sst = 0b010

        for pipe in pipe_list:

            trans_ddi_reg = 'TRANS_DDI_FUNC_CTL_' + pipe
            trans_ddi2_reg = 'TRANS_DDI_FUNC_CTL2_' + pipe
            ##
            # Read TRANS_DDI_FUNC_CTL_REGISTER values.
            trans_ddi_ctl_value = reg_read.read('TRANS_DDI_FUNC_CTL_REGISTER', trans_ddi_reg, self.platform[gfx_index],
                                                0x0)

            ##
            # Read TRANS_DDI_FUNC_CTL2_REGISTER values.
            trans_ddi_ctl2_value = reg_read.read('TRANS_DDI_FUNC_CTL2_REGISTER', trans_ddi2_reg,
                                                 self.platform[gfx_index], 0x0)

            ##
            # Programmed value of plane enable bit.
            trans_enable = trans_ddi_ctl_value.__getattribute__("trans_ddi_function_enable")

            ##
            # Programmed value of port sync mode.
            port_sync_enable = trans_ddi_ctl2_value.__getattribute__("port_sync_mode_enable")

            ##
            # Port sync master
            master_select = trans_ddi_ctl2_value.__getattribute__("port_sync_mode_master_select")

            if trans_enable and dp_sst == trans_ddi_ctl_value.__getattribute__("trans_ddi_mode_select"):
                if port_sync_enable:
                    verify_list.append(pipe)
                if master_select:
                    verify_list.append(self.get_pipe_details(master_select))

        if verify_list:
            for pipe in verify_list:
                ##
                # Plane to be verified
                plane_ctl_register = plane_ctl_reg + '_' + pipe

                ##
                # Read PLANE_CTL_REGISTER values.
                plane_ctl_value = reg_read.read('PLANE_CTL_REGISTER', plane_ctl_register, self.platform[gfx_index], 0x0)

                ##
                # Programmed value of plane enable bit.
                plane_enable = plane_ctl_value.__getattribute__("plane_enable")

                ##
                # Verify if plane is enabled
                if plane_enable:
                    logging.info("PASS: {} Plane enable status - Expected: Plane enabled Actual: {}"
                                 .format(plane_ctl_register, self.get_plane_status_string(plane_enable)))

                    ##
                    # Programmed value of source pixel format.
                    programmed_pixel_format = plane_ctl_value.__getattribute__("source_pixel_format")

                    if programmed_pixel_format == expected_pixel_format:
                        logging.info("PASS: {} Pixel Format - Expected: {} Actual: {}"
                                     .format(plane_ctl_register, self.get_pixel_format_string(expected_pixel_format),
                                             self.get_pixel_format_string(programmed_pixel_format)))

                    else:
                        logging.error("FAIL: {} Pixel Format - Expected: {} Actual: {}"
                                      .format(plane_ctl_register, self.get_pixel_format_string(expected_pixel_format),
                                              self.get_pixel_format_string(programmed_pixel_format)))
                        return False

                else:
                    logging.error("FAIL: {} Plane enable status - Expected: Plane enabled Actual {}"
                                  .format(plane_ctl_register, self.get_plane_status_string(plane_enable)))
                    return False

            return True
        else:
            logging.error("Pipes are not enabled")
            return False

    ##
    # @brief            Helper function to get the display configuration
    # @param[in]        connected_port_list : List of connected port
    # @param[in]        enumerated_displays : Enumerated displays
    # @param[in]        gfx_adapter_index   : gfx adapter
    # @return           Port config
    def get_display_configuration(self, connected_port_list, enumerated_displays, gfx_adapter_index='gfx_0'):
        port_config_str = ""
        for each_port in connected_port_list:
            target_id = self.config.get_target_id(each_port, enumerated_displays, gfx_adapter_index)
            mode = self.config.get_current_mode(target_id)
            port_config_str = port_config_str + "\n" + mode.to_string(enumerated_displays)
        return port_config_str

    ##
    # @brief            Launch Maps application
    # @param[in]	    bfullscreen Mode in which Maps application has to be launched
    # @return		    void
    def play_maps(self, bfullscreen):
        mode = " fullscreen" if bfullscreen else " windowed"
        logging.info(self.getStepInfo() + "Launching Maps application")
        win32api.ShellExecute(None, "open", "bingmaps:", None, None, win32con.SW_MAXIMIZE)
        time.sleep(5)
        maps_handle = window_helper.get_window('Maps', True)
        maps_handle.set_foreground()
        display_config = DisplayConfiguration()
        mode = display_config.get_current_mode(
            display_config.get_all_display_configuration().displayPathInfo[0].targetId)
        window_size_hor = 1920 if mode.HzRes > 1920 else mode.HzRes
        window_size_ver = 1080 if mode.VtRes > 1080 else mode.VtRes
        maps_handle.set_position(0, 0, window_size_hor, window_size_ver)
        time.sleep(5)
        if (bfullscreen):
            maps_handle.maximize()
            time.sleep(2)
        if maps_handle is not None:
            return maps_handle
        else:
            gdhm.report_bug(
                title="[MPO]Application Maps didn't open",
                problem_classification=gdhm.ProblemClassification.APP_CRASH,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            raise Exception("Application Maps didn't open")

    ##
    # @brief            Helper function to get the pixel format value based on command line argument
    # @param[in]	    pixel_format : The pixel format
    # @return		    pixel_format
    def get_pixel_format(self, pixel_format):
        return {'YUV_422_PACKED_8_BPC': 'source_pixel_format_YUV_422_PACKED_8_BPC',
                'NV12_YUV_420': 'source_pixel_format_NV12_YUV_420',
                'RGB_2101010': 'source_pixel_format_RGB_2101010',
                'P010_YUV_420_10_BIT': 'source_pixel_format_P010_YUV_420_10_BIT',
                'RGB_8888': 'source_pixel_format_RGB_8888',
                'P012_YUV_420_12_BIT': 'source_pixel_format_P012_YUV_420_12_BIT',
                'RGB_16161616_FLOAT': 'source_pixel_format_RGB_16161616_FLOAT',
                'P016_YUV_420_16_BIT': 'source_pixel_format_P016_YUV_420_16_BIT',
                'YUV_444_PACKED_8_BPC': 'source_pixel_format_YUV_444_PACKED_8_BPC',
                'RGB_64_BIT_16161616_FLOAT': 'source_pixel_format_RGB_64_BIT_16161616_FLOAT',
                'RGB_2101010_XR_BIAS': 'source_pixel_format_RGB_2101010_XR_BIAS',
                'INDEXED_8_BIT': 'source_pixel_format_INDEXED_8_BIT',
                'RGB_565': 'source_pixel_format_RGB_565'
                }[pixel_format]

    ##
    # @brief            Helper function to get display type from the connector port
    # @param[in]	    connector_port_type : The type of connector port
    # @return		    connector_port_type
    def get_display(self, connector_port_type):
        return {'DP_B': enum.DP_1,
                'DP_C': enum.DP_2,
                'DP_D': enum.DP_3,
                'HDMI_B': enum.HDMI_1,
                'HDMI_C': enum.HDMI_2
                }[connector_port_type]

    ##
    # @brief            Helper function to get the string from a list
    # @param[in]        test_string : The list that needs to be converted in string
    # @return           final string
    def list_to_str(self, test_string):
        final_string = ''
        for each_char in test_string:
            if each_char != '[' and each_char != ']':
                final_string = final_string + each_char
        return final_string

    ##
    # @brief            Helper function to remove the nested lists
    # @param[in]        lists : The list where nesting needs to be removed
    # @return           flatlist
    def remove_nested_list(self, lists):
        flatList = []
        for element in lists:
            if type(element) == list:
                for each_elem in element:
                    flatList.append(each_elem)
            else:
                flatList.append(element)
        return flatList

    ##
    # @brief            Helper function to get display topology
    # @param[in]	    topology : Gives details of topology
    # @return		    topology
    def get_topology(self, topology):
        return {1: 'SINGLE',
                2: 'CLONE',
                3: 'EXTENDED'
                }[topology]

    ##
    # @brief            Helper function to report GDHM  for verification failure
    # @param[in]        app_name     : String gives info about on what verification is done (3d_App/media/Desktop)
    # @param[in]        topology     : String gives details of topology (Extended/Single/Clone)
    # @param[in]        isfullscreen : Boolean which tells fullscreen or windowed
    # @return           None
    def report_to_gdhm_verifcation_failure(self, app_name, topology, isfullscreen=None):
        topology = self.get_topology(topology)
        mode = "fullscreen "
        if isfullscreen == False:
            mode = "windowed"
        gdhm.report_bug(
            title=f"[MPO][Plane formats]Plane verification failed for {app_name} in {mode} mode with config{topology}",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )

    ##
    # @brief            Helper function to get failure statements
    # @param[in]        verify_on    : String gives info about on what verification is done (3d_App/media/Desktop)
    # @param[in]        topology     : String gives details of topology (Extended/Single/Clone)
    # @param[in]        isfullscreen : Boolean which tells fullscreen or windowed
    # @return           fail_statement
    def fail_statement(self, verify_on, topology, isfullscreen=None):
        topology = self.get_topology(topology)
        mode = "fullscreen "
        if isfullscreen == False:
            mode = "windowed"
        fail_statement = f"Plane verification failed for {verify_on} in {mode} mode in {topology} config"
        return fail_statement

    ##
    # @brief            Helper function to get the list of target_ids for displays connected
    # @param[in]        include_inactive : Flag to indicate whether active/all display to be included
    # @return           target_id_list   : List of all target ids
    def get_target_id_list(self, include_inactive=False):
        target_id_list = []
        ##
        # fetch the display configuration of all the displays connected
        if include_inactive:
            display_info = self.config.get_all_display_configuration()
        else:
            display_info = self.config.get_current_display_configuration()
        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)
        return target_id_list

    ##
    # @brief            Helper function to create a dictionary of target ID with adapter and panel details
    # @return           adapter_tid_dict : A dictionary having key values as targetid:(gfx_index,panel)
    def get_tid_adapter_dict(self):
        self.target_id_list = self.get_target_id_list()

        enumerated_displays = self.config.get_enumerated_display_info()
        config, connector_port, display_and_adapter_info_list = self.config.get_current_display_configuration_ex(
            enumerated_displays)

        adapter_tid_dict = OrderedDict(zip(self.target_id_list, (
            zip(connector_port, [i.adapterInfo.gfxIndex for i in display_and_adapter_info_list]))))

        return adapter_tid_dict

    ##
    # @brief            Helper Function to set display configuration
    # @param[in]        topology                      : Topology of displays to be plugged in
    # @param[in]        display_and_adapter_info_list : Display and adapter info list
    # @return           adapter_tid_dict
    def set_display_config(self, topology, display_and_adapter_info_list):
        status = self.config.set_display_configuration_ex(topology, display_and_adapter_info_list)
        if status:
            logging.info("Successfully applied display configuration {}".format(
                DisplayConfigTopology(topology).name, display_and_adapter_info_list))
        else:
            self.fail("Failed to display configuration {}".format(
                DisplayConfigTopology(topology).name, display_and_adapter_info_list))
        return status

    ##
    # @brief            Helper function to apply_native_mode
    # @param[in]        display_and_adapterInfo : Display and adapter info
    # @return           mode                    : Native mode
    def apply_native_mode(self, display_and_adapterInfo):
        mode = None
        native_mode = self.config.get_native_mode(display_and_adapterInfo.TargetID)
        if native_mode is None:
            logging.error(f"Failed to get native mode for {display_and_adapterInfo.TargetID}")
            return mode
        mode = self.config.get_current_mode(display_and_adapterInfo)
        hzres = native_mode.hActive
        vtres = native_mode.vActive
        rr = native_mode.refreshRate
        mode.HzRes, mode.VtRes, mode.refreshRate = hzres, vtres, rr
        self.config.set_display_mode([mode])
        logging.info("Successfully applied native display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
            mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))
        return mode
