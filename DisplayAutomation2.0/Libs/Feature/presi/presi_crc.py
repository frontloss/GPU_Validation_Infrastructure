#####################################################################################################################################
# @file         presi_crc.py
# @brief        Interface for capturing CRC value in pre-silicon environment
# @author       Gopal Beeresh, Ami Golwala, Girish
########################################################################################################################

import logging
import os
import shutil
import time
import win32api

from Libs import env_settings
from Libs.Core import window_helper
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature.display_engine.de_base import display_base

from registers.mmioregister import MMIORegister

PORT_SUFFIX_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
PLANE_PIPE_SUFFIX_LIST = ['A', 'B', 'C', 'D']
FRM_CNT_WHEN_CRC_ENABLED = 0
NO_OF_FRM_CNT_WAIT = 5
DEBUG_CRC = False
pipe_plane_crc_source_select = dict([
    ('plane1', 0b000),
    ('plane2', 0b010),
    ('dmux', 0b100),
    ('plane3', 0b110),
    ('plane4', 0b111),
    ('plane5', 0b101),
    ('plane6', 0b011),
    ('plane7', 0b001)
])


##
# @brief        Helper function to Enable CRC capture through HW register programming
# @param[in]    enable_crc - Boolean flag to determine CRC capture state
# @param[in]    port_suffix - port value to capture CRC
# @param[in]    pipe_plane_suffix - pipe or plane value to capture CRC
# @param[in]    capture_plane_crc - Boolean flag to capture plane CRC
# @param[in]    plane_no - Plane no  to be crc
# @return       Boolean value
def control_crc(enable_crc, port_suffix, pipe_plane_suffix, capture_plane_crc=False, plane_no=1):
    driver_interface_ = driver_interface.DriverInterface()
    machine_info = SystemInfo()
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break

    silicon_type = env_settings.get('GENERAL', 'silicon_type')
    if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']) is False:
        logging.error("set silicon_type to SIMULATOR or EMULATOR in config.ini file")
        return False

    if pipe_plane_suffix not in PLANE_PIPE_SUFFIX_LIST:
        logging.error(
            "Plane/Pipe suffix %s not found in the current set %s" % (pipe_plane_suffix, PLANE_PIPE_SUFFIX_LIST))
        return False
    if port_suffix not in PORT_SUFFIX_LIST:
        logging.error("Port %s not found in the current set %s" % (port_suffix, PORT_SUFFIX_LIST))
        return False

    # Enable/Disable Port and Pipe or Plane CRC
    if enable_crc is True:
        logging.info("Enabling crc calculations -DDI_CRC_CTL and PIPE_CRC_CTL")
    else:
        logging.info("Disabling crc calculations -DDI_CRC_CTL and PIPE_CRC_CTL")

    ddi_crc_ctl_reg_offset_name = "DDI_CRC_CTL_%s" % port_suffix
    ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)
    logging.debug("Current - port_crc_reg.offset = %s, port_crc_reg.asUint = %s" % (ddi_crc_ctl_reg.offset,
                                                                                    ddi_crc_ctl_reg.asUint))

    pipe_crc_ctl_reg_offset_name = "PIPE_CRC_CTL_%s" % pipe_plane_suffix
    pipe_crc_ctl_reg = MMIORegister.get_instance("PIPE_CRC_CTL_REGISTER", pipe_crc_ctl_reg_offset_name, platform)
    logging.debug(
        "Current - pipe_plane_crc_reg.offset = %s, pipe_plane_crc_reg.asUint = %s" % (pipe_crc_ctl_reg.offset,
                                                                                      pipe_crc_ctl_reg.asUint))
    if enable_crc is True:
        window_helper.show_desktop_bg_only(True)
        # In Pre-si environment mainly in pipe2d it will 2 mins to minimize windows and hide task bar so added delay
        time.sleep(120)
        # Required to enable scrambler bit for EDP panel
        logging.debug("Required to enable scrambler bit for EDP panel")
        # scrambler_offset_name = "SCRAMBLER_DP_TP_DFT_%s" % port_suffix
        scrambler_offset_name = "SCRAMBLER_DP_TP_DFT_%s" % pipe_plane_suffix
        scrambler_reg = MMIORegister.get_instance("SCRAMBLER_DP_TP_DFT_REGISTER", scrambler_offset_name, platform)
        scrambler_offset = scrambler_reg.offset
        driver_interface_.mmio_write(scrambler_offset, 1, 'gfx_0')

        pipe_crc_ctl_reg.asUint = 0
        pipe_crc_ctl_reg.enable_crc = 1
        pipe_crc_ctl_reg.crc_change = 1
        # pipe_plane_crc_reg.crc_done = 1
        if capture_plane_crc:
            # Enable Plane CRC
            plane = "plane%s" % plane_no
            pipe_crc_ctl_reg.crc_source_select = pipe_plane_crc_source_select[plane]
        else:
            # Enable Pipe CRC
            pipe_crc_ctl_reg.crc_source_select = pipe_plane_crc_source_select['dmux']
        # Enable Port CRC
        ddi_crc_ctl_reg.asUint = 0
        ddi_crc_ctl_reg.enable_crc = 1
        ddi_crc_ctl_reg.crc_change = 1
        ddi_crc_ctl_reg.crc_done = 1
    else:
        window_helper.show_desktop_bg_only(False)
        # Disable Pipe/Plane CRC
        pipe_crc_ctl_reg.asUint = 0
        # Disable Port CRC
        ddi_crc_ctl_reg.asUint = 0

    logging.debug(
        "Setting -pipe_plane_crc_reg.offset = %s, pipe_plane_crc_reg.asUint = %s" % (pipe_crc_ctl_reg.offset,
                                                                                     pipe_crc_ctl_reg.asUint))
    driver_interface_.mmio_write(pipe_crc_ctl_reg.offset, pipe_crc_ctl_reg.asUint, 'gfx_0')

    logging.debug("Setting - port_crc_reg.offset = %s, port_crc_reg.asUint = %s" % (ddi_crc_ctl_reg.offset,
                                                                                    ddi_crc_ctl_reg.asUint))
    driver_interface_.mmio_write(ddi_crc_ctl_reg.offset, ddi_crc_ctl_reg.asUint, 'gfx_0')

    if silicon_type == "EMULATOR" and enable_crc:
        # Constant variable to store the warm up time required for CRC module in
        # pre-silicon environment to generate CRC
        CRC_MODULE_WARM_UP_IN_SECS = 50
        time.sleep(CRC_MODULE_WARM_UP_IN_SECS)
        trans_frmln_dbg_reg = MMIORegister.read("TRANS_FRMLN_DBG_REGISTER",
                                                "TRANS_FRMLN_DBG_%s" % (pipe_plane_suffix), platform)
        logging.debug(
            "FRAME_COUNT " + pipe_plane_suffix + "--> Offset : " + format(trans_frmln_dbg_reg.offset, '08X')
            + " Value :" + format(trans_frmln_dbg_reg.frame_counter_lsbs, '08X'))
        global FRM_CNT_WHEN_CRC_ENABLED
        FRM_CNT_WHEN_CRC_ENABLED = trans_frmln_dbg_reg.frame_counter_lsbs

        if DEBUG_CRC is True:
            ddi_crc_res_reg_offset_name = "DDI_CRC_RES_%s" % port_suffix
            ddi_crc_res_reg = MMIORegister.read("DDI_CRC_RES_REGISTER", ddi_crc_res_reg_offset_name,
                                                platform=platform)
    return True


##
# @brief        Helper function to Capture CRC through HW registers for all the connected displays
# @param[in]    port_suffix - port value to capture CRC
# @param[in]    pipe_plane_suffix - pipe or plane value to capture CRC
# @returns      result - Dictionary with port_crc and (pipe_crc or plane_crc)
#                        based on which one of pipe and plane crc done.
def read_crc(port_suffix, pipe_plane_suffix):
    import time
    result = dict()
    silicon_type = env_settings.get('GENERAL', 'silicon_type')
    if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']) is False:
        logging.error("set silicon_type to SIMULATOR or EMULATOR in config.ini file")
        return result
    driver_interface_ = driver_interface.DriverInterface()
    machine_info = SystemInfo()
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).upper()
        break
    ddi_crc_ctl_reg_offset_name = "DDI_CRC_CTL_%s" % port_suffix
    ddi_crc_res_reg_offset_name = "DDI_CRC_RES_%s" % port_suffix
    pipe_crc_ctl_reg_offset_name = "PIPE_CRC_CTL_%s" % pipe_plane_suffix
    pipe_cd_crc_res_reg_offset_name = "PIPE_CD_CRC_RES_%s" % pipe_plane_suffix
    if silicon_type == "SIMULATOR":
        # Triggering the plane processing
        start_plane_processing()
        ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)
        # wait_for_ddi_crc_done
        time_out = 30
        while ddi_crc_ctl_reg.crc_done == 0 and time_out:
            # Sleep for 30 secs
            time.sleep(30)
            ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)
            time_out -= 1

        ##
        # ddi_crc_ctl_reg.crc_done is a sticky bit, cleared by writing 1b to it.
        ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)
        if ddi_crc_ctl_reg.crc_done == 1:
            ddi_crc_ctl_reg.crc_done = 1
            driver_interface_.mmio_write(ddi_crc_ctl_reg.offset, ddi_crc_ctl_reg.asUint, 'gfx_0')

        ##
        # pipe_crc_ctl_reg.crc_done is a sticky bit, cleared by writing 1b to it.
        # pipe_crc_ctl_reg = MMIORegister.read("PIPE_CRC_CTL_REGISTER", pipe_crc_ctl_reg_offset_name, platform=platform)
        # if pipe_crc_ctl_reg.crc_done == 1:
        #     pipe_crc_ctl_reg.crc_done = 1
        #     mmio_write(pipe_crc_ctl_reg.offset, pipe_crc_ctl_reg.asUint)

        ##
        # CRC is calculated on all pixels and blanking. The lane carrying the clock is replaced with all 0s.
        # The first CRC done indication after CRC is first enabled is from a full frame
        # and will have the expected CRC result.
        # Subsequent CRC done indications will give a steady CRC result.
        # so Triggering the plane processing for the 2nd time to get the steady CRC result.
        start_plane_processing()
        ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)
        # wait_for_ddi_crc_done
        time_out = 30
        while ddi_crc_ctl_reg.crc_done == 0 and time_out:
            # Sleep for 30 secs
            time.sleep(30)
            ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)
            time_out -= 1
    else:
        # wait_for_ddi_crc_done(platform, port_suffix, time_out=60)
        ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)

        trans_frmln_dbg_reg = MMIORegister.read("TRANS_FRMLN_DBG_REGISTER", "TRANS_FRMLN_DBG_%s" % (pipe_plane_suffix),
                                                platform)
        logging.debug("FRAME_COUNT " + pipe_plane_suffix + "--> Offset : " + format(trans_frmln_dbg_reg.offset, '08X')
                      + " Value :" + format(trans_frmln_dbg_reg.frame_counter_lsbs, '08X'))

        if DEBUG_CRC is True:
            ddi_crc_res_reg = MMIORegister.read("DDI_CRC_RES_REGISTER", ddi_crc_res_reg_offset_name, platform=platform)

        time_out = 120
        global FRM_CNT_WHEN_CRC_ENABLED
        while (trans_frmln_dbg_reg.frame_counter_lsbs < (FRM_CNT_WHEN_CRC_ENABLED + NO_OF_FRM_CNT_WAIT)) and time_out:
            # Sleep for 1 minute
            time.sleep(30)
            time_out -= 1
            trans_frmln_dbg_reg = MMIORegister.read("TRANS_FRMLN_DBG_REGISTER",
                                                    "TRANS_FRMLN_DBG_%s" % (pipe_plane_suffix),
                                                    platform)
            logging.debug(
                "FRAME_COUNT " + pipe_plane_suffix + "--> Offset : " + format(trans_frmln_dbg_reg.offset, '08X')
                + " Value :" + format(trans_frmln_dbg_reg.frame_counter_lsbs, '08X'))

            if DEBUG_CRC is True:
                cur_ctl_reg_offset_name = 'CUR_CTL_%s' % pipe_plane_suffix
                cur_ctl_reg_instance = MMIORegister.read("CUR_CTL_REGISTER", cur_ctl_reg_offset_name, platform)
                aud_pin_eld_cp_vld_reg_instance = MMIORegister.read("AUD_PIN_ELD_CP_VLD_REGISTER",
                                                                    'AUD_PIN_ELD_CP_VLD', platform)

                ddi_crc_res_reg = MMIORegister.read("DDI_CRC_RES_REGISTER", ddi_crc_res_reg_offset_name,
                                                    platform=platform)
                pipe_cd_crc_res_reg = MMIORegister.read("PIPE_CD_CRC_RES_REGISTER", pipe_cd_crc_res_reg_offset_name,
                                                        platform=platform)

        if DEBUG_CRC is True:
            trans_frmln_dbg_reg = MMIORegister.read("TRANS_FRMLN_DBG_REGISTER",
                                                    "TRANS_FRMLN_DBG_%s" % (pipe_plane_suffix),
                                                    platform)
            logging.debug(
                "FRAME_COUNT " + pipe_plane_suffix + "--> Offset : " + format(trans_frmln_dbg_reg.offset, '08X')
                + " Value :" + format(trans_frmln_dbg_reg.frame_counter_lsbs, '08X'))

            cur_ctl_reg_offset_name = 'CUR_CTL_%s' % pipe_plane_suffix
            cur_ctl_reg_instance = MMIORegister.read("CUR_CTL_REGISTER", cur_ctl_reg_offset_name, platform)
            aud_pin_eld_cp_vld_reg_instance = MMIORegister.read("AUD_PIN_ELD_CP_VLD_REGISTER",
                                                                'AUD_PIN_ELD_CP_VLD', platform)

            ddi_crc_res_reg = MMIORegister.read("DDI_CRC_RES_REGISTER", ddi_crc_res_reg_offset_name, platform=platform)
            pipe_cd_crc_res_reg = MMIORegister.read("PIPE_CD_CRC_RES_REGISTER", pipe_cd_crc_res_reg_offset_name,
                                                    platform=platform)

    ddi_crc_ctl_reg = MMIORegister.read("DDI_CRC_CTL_REGISTER", ddi_crc_ctl_reg_offset_name, platform=platform)
    if ddi_crc_ctl_reg.crc_done == 0:
        logging.error("CRC is not Completed, ddi_crc_ctl_reg.crc_done = 0 ")
        return result
    pipe_crc_ctl_reg = MMIORegister.read("PIPE_CRC_CTL_REGISTER", pipe_crc_ctl_reg_offset_name, platform=platform)
    # if pipe_crc_ctl_reg.crc_done == 0:
    #     logging.error("PIPE CRC is not Completed, pipe_crc_ctl_reg.crc_done = 0 ")
    #     return result

    # Read PORT CRC values
    ddi_crc_res_reg = MMIORegister.read("DDI_CRC_RES_REGISTER", ddi_crc_res_reg_offset_name, platform=platform)
    port_crc_value = format(ddi_crc_res_reg.asUint, '#04x')
    result['port_crc'] = port_crc_value
    logging.debug("PORT CRC result %s with offset %s" % (format(ddi_crc_res_reg.asUint, "#04x"),
                                                         ddi_crc_res_reg.offset))

    # Read pipe / plane CRC values
    pipe_cd_crc_res_reg = MMIORegister.read("PIPE_CD_CRC_RES_REGISTER", pipe_cd_crc_res_reg_offset_name,
                                            platform=platform)
    pipe_plane_crc_value = format(pipe_cd_crc_res_reg.asUint, '#04x')

    if pipe_crc_ctl_reg.enable_crc == 0b1 and pipe_crc_ctl_reg.crc_source_select == pipe_plane_crc_source_select[
        'dmux']:
        result['pipe_crc'] = pipe_plane_crc_value
        logging.debug("PIPE CRC result %s with offset %s" % (format(pipe_cd_crc_res_reg.asUint, "#04x"),
                                                             pipe_cd_crc_res_reg.offset))
    else:
        key = list(pipe_plane_crc_source_select.keys())[
            list(pipe_plane_crc_source_select.values()).index(pipe_crc_ctl_reg.crc_source_select)]
        key = "%s_crc" % key
        result[key] = pipe_plane_crc_value
        logging.debug("PLANE CRC result %s with offset %s" % (format(pipe_cd_crc_res_reg.asUint, "#04x"),
                                                              pipe_cd_crc_res_reg.offset))
    logging.debug("CRC results : %s" % result)
    return result


##
# @brief        Helper function to Store CRC stored in file with key name
# @param[in]   crc_file_name - Absolute Path of crc_file_name where CRC to be stored.
# @param[in]   crc_key_name -  key name for port/pipe crc values
# @param[in]   port_crc -  port_crc value to store
# @param[in]   pipe_crc -  pipe_crc value to store
# @param[in]   plane_crc -  plane_crc value to store
# @return      bool - True/False
def store_crc_in_file(crc_file_name, crc_key_name, port_crc, pipe_crc="NO_DATA", plane_crc="NO_DATA"):
    logging.info("In Store crc : %s" % crc_file_name)

    # crc_key_name|PORT_CRC|PIPE_CRC|PLANE_CRC|
    crc_line_to_write = "%s|%s|%s|%s|\n" % (crc_key_name, port_crc, pipe_crc, plane_crc)
    if os.path.exists(crc_file_name):
        crc_file_fd = open(crc_file_name, 'r')
        crc_lines = crc_file_fd.readlines()
        crc_file_fd.close()
        crc_file_fd = open(crc_file_name, 'w')
        is_overwritten = False
        for crc_line in crc_lines:
            crc_data = crc_line.split('|')
            if crc_data[0] == crc_key_name:
                logging.debug("Crc Key Name :%s already Exsists, overwriting it" % crc_key_name)
                crc_file_fd.write(crc_line_to_write)
                is_overwritten = True
            else:
                crc_file_fd.write(crc_line)
        if is_overwritten is False:
            crc_file_fd.write(crc_line_to_write)
        crc_file_fd.close()
    else:
        crc_file_fd = open(crc_file_name, 'w+')
        crc_file_fd.write(crc_line_to_write)
        crc_file_fd.close()

    if os.path.exists(crc_file_name):
        logging.debug("SUCCESS: In File - %s CRC - %s is Stored" % (crc_file_name, crc_line_to_write))
    else:
        logging.error("FAILED: To store CRC - %s in File - %s" % (crc_line_to_write, crc_file_name))
        return False
    ##
    # Copy the CRC file to log_folder so the in GTA it will get uploaded as a log file
    shutil.copy(crc_file_name, test_context.TestContext.logs_folder())
    return True


##
# @brief        Helper function to Compare CRC stored in file
# @param[in]   crc_file_name - Absolute Path of crc_file_name where CRC is stored.
# @param[in]   crc_key_name -  key name of port/pipe crc value in a file
# @param[in]   port_crc -  port_crc value to compare
# @param[in]   pipe_crc -  pipe_crc value to compare
# @param[in]   plane_crc -  plane_crc value to compare
# @return      crc_status - bool value
def compare_crc_stored_in_file(crc_file_name, crc_key_name, port_crc, pipe_crc="NO_DATA", plane_crc="NO_DATA"):
    is_mode_name_exists = False
    crc_status = True
    if os.path.exists(crc_file_name):
        crc_file_fd = open(crc_file_name, 'r')
        crc_lines = crc_file_fd.readlines()
        crc_file_fd.close()
        for crc_line in crc_lines:
            crc_data = crc_line.split('|')
            stored_mode_name = crc_data[0]
            stored_port_crc = crc_data[1]
            stored_pipe_crc = crc_data[2]
            stored_plane_crc = crc_data[3]
            if stored_mode_name == crc_key_name:
                is_mode_name_exists = True
                if stored_port_crc == port_crc:
                    crc_status &= True
                    logging.info("PASS: %s : PORT_CRC MATCHES: EXPECTED = %s, ACTUAL = %s" %
                                 (crc_key_name, stored_port_crc, port_crc))
                else:
                    logging.error("FAIL: %s : PORT_CRC DOESN'T MATCHES: EXPECTED = %s, ACTUAL = %s" %
                                  (crc_key_name, stored_port_crc, port_crc))
                    crc_status &= False

                if pipe_crc != "NO_DATA":
                    if stored_pipe_crc == "NO_DATA":
                        crc_status &= False
                        logging.error("FAIL: FOR %s :, PIPE_CRC IS NOT STORED" % crc_key_name)
                    else:
                        if stored_pipe_crc == pipe_crc:
                            crc_status &= True
                            logging.info("PASS: %s : PIPE_CRC MATCHES: EXPECTED = %s, ACTUAL = %s" %
                                         (crc_key_name, stored_pipe_crc, pipe_crc))
                        else:
                            crc_status &= False
                            logging.error("FAIL: %s : PIPE_CRC DOESN'T MATCHES: EXPECTED = %s, ACTUAL = %s" %
                                          (crc_key_name, stored_pipe_crc, pipe_crc))

                if plane_crc != "NO_DATA":
                    if stored_plane_crc == "NO_DATA":
                        crc_status &= False
                        logging.error("FAIL: FOR %s : , PLANE_CRC IS NOT STORED" % crc_key_name)
                    else:
                        if stored_plane_crc == plane_crc:
                            crc_status &= True
                            logging.info("PASS: %s : PLANE_CRC MATCHES: EXPECTED = %s, ACTUAL = %s" %
                                         (crc_key_name, stored_plane_crc, plane_crc))
                        else:
                            crc_status &= False
                            logging.error("FAIL: %s : PLANE_CRC DOESN'T MATCHES: EXPECTED = %s, ACTUAL = %s" %
                                          (crc_key_name, stored_plane_crc, plane_crc))
                break
        if is_mode_name_exists is False:
            logging.error("FAIL: CRC Value NOT STORED For %s in file %s" % (crc_key_name, crc_file_name))
            crc_status &= False
    else:
        logging.error("FAIL: CRC File %s doesn't exist" % crc_file_name)
        crc_status &= False
    return crc_status


##
# @brief        Helper function to Set below pre requisites to capture crc
# @details      Disable cursor gamma as Fulsim does not support
#               Disable Audio
#               Set Cursor position to (100, 100)
# @param[in]    pipe_suffix - to disable cursor gamma based for a pipe
# @return       None
def set_pre_requisites_to_capture_crc(pipe_suffix):
    logging.info("Setting Pre Requisites to Capture CRC: Disable Gamma, Disable Audio, SetCursorPos to (100,100)")
    driver_interface_ = driver_interface.DriverInterface()
    machine_info = SystemInfo()
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).upper()
        break

    ##
    # Disable Cursor Gamma CUR_CTL ( 70080) based on Pipe Suffix - Bit no 26
    # As Fulsim does not support Cursor gamma
    logging.debug("disable Cursor Gamma CUR_CTL ( 70080) based on Pipe Suffix - Bit no 26")
    cur_ctl_reg_offset_name = 'CUR_CTL_%s' % pipe_suffix
    cur_ctl_reg_instance = MMIORegister.read("CUR_CTL_REGISTER", cur_ctl_reg_offset_name, platform)
    cur_ctl_reg_instance.gamma_enable = 0
    driver_interface_.mmio_write(cur_ctl_reg_instance.offset, cur_ctl_reg_instance.asUint, 'gfx_0')

    ##
    # Set 0x00000000 to AUD_PIN_ELD_CP_VLD(0x650C0)
    logging.debug("Set 0x00000000 to AUD_PIN_ELD_CP_VLD(0x650C0)")
    aud_pin_eld_cp_vld_reg_offset_name = 'AUD_PIN_ELD_CP_VLD'
    aud_pin_eld_cp_vld_reg_instance = MMIORegister.read("AUD_PIN_ELD_CP_VLD_REGISTER",
                                                        aud_pin_eld_cp_vld_reg_offset_name, platform)
    aud_pin_eld_cp_vld_reg_instance.asUint = 0
    driver_interface_.mmio_write(aud_pin_eld_cp_vld_reg_instance.offset, aud_pin_eld_cp_vld_reg_instance.asUint, 'gfx_0')

    ##
    # Set Cursor Position to (100, 100)
    logging.debug("Setting Cursor Position to (100, 100)")
    win32api.SetCursorPos((100, 100))
    time.sleep(60)


##
# @brief        API to Capture CRC through HW register programming  and Compare it stored value or store in a file
#               This API will capture Port and Pipe CRC only.
# @param[in]    display_port - Ex: HDMI_A/HDMI_B/DP_B/DP_C/... for which port and pipe crc to be captured
# @param[in]   crc_file_name - Absolute Path of crc_file_name where CRC to be stored or get crc to compare
# @param[in]   crc_key_name -  key name to store or compare port/pipe crc values in a file
# @return       True if port and pipe CRC compare matches or stored in a file else False
def verify_or_capture_presi_crc(display_port, crc_file_name, crc_key_name):
    logging.info("********* Entered COMPARE OR CAPTURE CRC*******")
    crc_status = True
    # Commence CRC verification only if below settings are set in config.ini file
    # crc_enable is TRUE
    # silicon_type is SIMULATOR or EMULATOR
    # crc_presi_operation is CAPTURE or COMPARE
    silicon_type = env_settings.get('GENERAL', 'silicon_type')
    crc_presi_operation = env_settings.get('CRC', 'crc_presi')
    logging.info("silicon_type = {0}; crc_operation = {1}".format(silicon_type, crc_presi_operation))
    if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']
            and crc_presi_operation is not None and crc_presi_operation in ['CAPTURE', 'COMPARE']):
        logging.info("*********COMPARE OR CAPTURE PRESI-CRC START *******")
        port_suffix = str(display_port).split('_')[1]
        pipe_suffix = None
        port2pipe_map = display_base.get_port_to_pipe()
        if display_port in port2pipe_map.keys():
            pipe_suffix = port2pipe_map[display_port][-1:]
        if pipe_suffix is None:
            logging.error("No pipe attached to %s" % display_port)
            crc_status = False

        if crc_status is True:
            # Set pre requisites to capture crc
            set_pre_requisites_to_capture_crc(pipe_suffix)

            # Enable CRC, read_crc and disable CRC
            port_pipe_crc_dict = None
            if control_crc(True, port_suffix, pipe_suffix, False):
                port_pipe_crc_dict = read_crc(port_suffix=port_suffix, pipe_plane_suffix=pipe_suffix)
                dump_crc_debug_registers()
                control_crc(False, port_suffix, pipe_suffix, False)

            if "port_crc" not in port_pipe_crc_dict.keys():
                logging.error("Port CRC is not captured for :%s" % display_port)
                crc_status = False
            if "pipe_crc" not in port_pipe_crc_dict.keys():
                logging.error("Port CRC is not captured for :%s" % display_port)
                crc_status = False

            # Compare CRC or Store CRC in file
            if crc_status is True:
                if crc_presi_operation in ['CAPTURE']:
                    store_crc_in_file(crc_file_name, crc_key_name, port_crc=port_pipe_crc_dict['port_crc'],
                                      pipe_crc=port_pipe_crc_dict['pipe_crc'], plane_crc="NO_DATA")
                else:
                    crc_status &= compare_crc_stored_in_file(crc_file_name, crc_key_name,
                                                             port_crc=port_pipe_crc_dict['port_crc'],
                                                             pipe_crc=port_pipe_crc_dict['pipe_crc'],
                                                             plane_crc="NO_DATA")
        logging.info("*********COMPARE OR CAPTURE PRESI-CRC END *******")
    else:
        logging.error(
            "To verify or capture pre-si CRC: In config.ini file set silicon_type to SIMULATOR/EMULATOR  and crc_presi to CAPTURE OR COMPARE")
        crc_status = False
    return crc_status


##
# @brief       Helper function to Trigger or initiate plane processing by MMIO write 0x1 to scratch pad register 0x4f080
#              In the HAS pre-silicon environment, Fulsim uses programming to 0x4F080 to generate events
#              Plane processing is required to process image and generate CRC in SIMULATOR(FULSIM)
# @return      None
def start_plane_processing():
    logging.debug("In start plane processing")
    driver_interface_ = driver_interface.DriverInterface()
    machine_info = SystemInfo()
    platform = None
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).upper()
        break
    swf_reg_offset_name = "SWF_32"
    swf_reg_instance = MMIORegister.read("SWF_REGISTER", swf_reg_offset_name, platform)
    swf_reg_instance.software_flags = 1
    driver_interface_.mmio_write(swf_reg_instance.offset, swf_reg_instance.asUint, 'gfx_0')
    logging.debug("End start plane processing")
    return


##
# @brief        Helper function to dump the debug register
# @details      This is temporary solution, long term solution is currently under-development
# @return       None
def dump_crc_debug_registers():
    driver_interface_ = driver_interface.DriverInterface()
    plane_registers = {"PLANE_STRIDE": 0x70188, "PLANE_POS": 0x7018c, "PLANE_SIZE": 0x70190, "PLANE_KEYVAL": 0x70194,
                       "PLANE_KEYMAX": 0x701a0, "PLANE_KEYMSK": 0x70198, "PLANE_AUX_OFFSET": 0x701c4,
                       "PLANE_OFFSET": 0x701a4,
                       "PLANE_WM": 0x70240, "PLANE_WM_TRANS": 0x70268, "PLANE_LEFT_SURF": 0x701b0,
                       "PLANE_AUX_DIST": 0x701c0,
                       "PLANE_CTL": 0x70180,
                       }
    logging.debug("****************** PLANE REGISTERS DUMP ******************")
    for reg_name, reg_offset in plane_registers.items():
        reg_val = driver_interface_.mmio_read(reg_offset, 'gfx_0')
        logging.debug("%s[%s] = %s" % (reg_name, reg_offset, reg_val))
    logging.debug("***************END OF PLANE REGISTERS DUMP ****************")

    pipe_registers = {
        "TRANS_HTOTAL_A": 0x60000, "TRANS_HTOTAL_B": 0x61000, "TRANS_HTOTAL_C": 0x62000, "TRANS_HTOTAL_EDP": 0x6f000,
        "TRANS_HTOTAL_WD0": 0x6e000, "TRANS_HTOTAL_WD1": 0x6e800,
        "TRANS_HBLANK_A": 0x60004, "TRANS_HBLANK_B": 0x61004, "TRANS_HBLANK_C": 0x62004, "TRANS_HBLANK_EDP": 0x6f004,
        "TRANS_HSYNC_A": 0x60008, "TRANS_HSYNC_B": 0x61008, "TRANS_HSYNC_C": 0x62008, "TRANS_HSYNC_EDP": 0x6f008,
        "TRANS_VTOTAL_A": 0x6000c, "TRANS_VTOTAL_B": 0x6100c, "TRANS_VTOTAL_C": 0x6200c, "TRANS_VTOTAL_EDP": 0x6f00c,
        "TRANS_VTOTAL_WD0": 0x6e00c, "TRANS_VTOTAL_WD1": 0x6e80c,
        "TRANS_VBLANK_A": 0x60010, "TRANS_VBLANK_B": 0x61010, "TRANS_VBLANK_C": 0x62010, "TRANS_VBLANK_EDP": 0x6f010,
        "TRANS_VSYNC_A": 0x60014, "TRANS_VSYNC_B": 0x61014, "TRANS_VSYNC_C": 0x62014, "TRANS_VSYNC_EDP": 0x6f014,
        "TRANS_MULT_A": 0x6002c, "TRANS_MULT_B": 0x6102c, "TRANS_MULT_C": 0x6202c,
        "TRANS_SPACE_A": 0x60024, "TRANS_SPACE_B": 0x61024, "TRANS_SPACE_C": 0x62024, "TRANS_SPACE_EDP": 0x6f024,
        "PIPE_SRCSZ_B": 0x6101c, "PIPE_SRCSZ_A": 0x6001c, "PIPE_SRCSZ_C": 0x6201c,
        "TRANS_VSYNCSHIFT_A": 0x60028, "TRANS_VSYNCSHIFT_B": 0x61028, "TRANS_VSYNCSHIFT_C": 0x62028,
        "TRANS_VSYNCSHIFT_EDP": 0x6f028
    }
    logging.debug("****************** PIPE REGISTERS DUMP ******************")
    for reg_name, reg_offset in pipe_registers.items():
        reg_val = driver_interface_.mmio_read(reg_offset, 'gfx_0')
        logging.debug("%s[%s] = %s" % (reg_name, reg_offset, reg_val))
    logging.debug("***************END OF PIPE REGISTERS DUMP ****************")
