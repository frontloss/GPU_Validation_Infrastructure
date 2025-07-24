#################################################################################################
# @file         feature_basic_verify.py
# @brief        This scripts comprises of basic enable/disable verify function per subfeature which can be used by
#               Color test scripts / other features for concurrency validation"
#               To perform register verification for functions as of below
#               1. verify_hw3dlut_feature()
#               2. verify_transcoder_bpc()
#               3. verify_dithering_feature()
#               4. verify_hdr_feature()
#               5. verify_lace_feature()
#               6. verify_ycbcr_feature()
#               7. hdr_status()
# @author       Vimalesh D
#################################################################################################
import logging
import time
import DisplayRegs
from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues, TransDDiOffsetsValues, Hw3dLutOffsetsValues, \
    LaceOffsetsValues
from Tests.Color.Common import common_utility, color_enums, color_mmio_interface
from Tests.Planes.Common import planes_helper
from Libs.Feature.presi.presi_crc import start_plane_processing
from Libs.Core import system_utility

##
# Dictionary map for register bit and function parameter  0 or 1 to map Enable or Disable
BIT_MAP_DICT = {1: "ENABLE", 0: "DISABLE"}

color_mmiointerface = color_mmio_interface.ColorMmioInterface()


##
# @brief         Verify the register programming for  3DLUT feature
# @param[in]     gfx_index - gfx adapter index
# @param[in]     platform - Name of the platform
# @param[in]     pipe - current pipe
# @param[in]     enable - Boolean value to be either True or False
# @return        status - True on Success, False otherwise
def verify_hw3dlut_feature(gfx_index: str, platform: str, pipe: str, enable: bool) -> bool:
    status = False
    regs = DisplayRegs.get_interface(platform, gfx_index)
    lut_3d_ctl_off = regs.get_3dlut_offsets(pipe)
    data = color_mmiointerface.read(gfx_index, lut_3d_ctl_off.LutControl)
    lut_3d_ctl_value = regs.get_hw3dlut_info(pipe, Hw3dLutOffsetsValues(LutControl=data))
    ##
    # 3D LUT ENABLE/DISABLE STATUS
    if lut_3d_ctl_value.Lut3DEnable == int(enable):
        logging.info("PASS : HW 3DLUT on Adapter {0} pipe {1} Expected: {2} and Actual : {3}".format
                     (gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[lut_3d_ctl_value.Lut3DEnable]))
        status = True
    else:
        title = " HW 3DLUT on Adapter {0} Pipe {1} Expected: {2} and Actual : {3}".format \
            (gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[lut_3d_ctl_value.Lut3DEnable])
        status = False
        logging.error("FAIL :" + title)
        common_utility.gdhm_report_app_color(title=title)
        return status
    ##
    # NEW LUT READY STATUS
    if lut_3d_ctl_value.Lut3DEnable:
        if lut_3d_ctl_value.NewLutReady == 0:
            logging.info("PASS : New LUT ready reset - HW has loaded the LUT buffer")
            status = True
        if lut_3d_ctl_value.NewLutReady == 1:
            ##
            # HW will take <15 ms to reset the ready bit
            time.sleep(1)
            data = color_mmiointerface.read(gfx_index, lut_3d_ctl_off.LutControl)
            lut_3d_ctl_value = regs.get_hw3dlut_info(pipe, Hw3dLutOffsetsValues(LutControl=data))

            if lut_3d_ctl_value.NewLutReady != 1:
                logging.info("PASS : New LUT ready reset - HW has loaded the LUT buffer")
                status = True
            else:
                title = "New LUT ready not reset - HW is yet to load the LUT buffer"
                logging.error("FAIL :" + title)
                common_utility.gdhm_report_app_color(title=title)
                status = False
    else:
        if lut_3d_ctl_value.NewLutReady != 0:
            title = "New LUT ready set, HW_3DLUT was Disabled"
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
            return False

    return status


##
# @brief         Verify the register programming for transcoder bpc
# @param[in]     gfx_index - gfx adapter index
# @param[in]     platform - Name of the platform
# @param[in]     transcoder - current transcoder
# @param[in]     expected_bpc -  6,8,10,12
# @return        status - True on Success, False otherwise
def verify_transcoder_bpc(gfx_index: str, platform: str, transcoder: str, expected_bpc: int) -> bool:
    bpc_dict = {0: "BPC8", 1: "BPC10", 2: "BPC6", 3: "BPC12"}
    expected_bpc_str = "BPC" + str(expected_bpc)
    regs = DisplayRegs.get_interface(platform, gfx_index)
    transcoder = DisplayRegs.DisplayRegsInterface.TranscoderType(transcoder).name
    trans_ddi_func_offset = regs.get_trans_ddi_offsets(transcoder)
    data = color_mmiointerface.read(gfx_index, trans_ddi_func_offset.FuncCtrlReg)
    trans_ddi_value = regs.get_trans_ddi_info(transcoder, TransDDiOffsetsValues(FuncCtrlReg=data))

    ##
    # Compare transcode BPC and Expected BPC
    if bpc_dict[trans_ddi_value.BitsPerColor] == expected_bpc_str:
        logging.info("PASS: Transcoder BPC on Adapter {0} Transcoder {1} Expected: {2} and Actual : {3}".format(
            gfx_index, transcoder, expected_bpc_str, bpc_dict[trans_ddi_value.BitsPerColor]))
        status = True
    else:
        title = "Transcoder BPC on Adapter {0} Transcoder {1} Expected: {2} and Actual : {3}".format(
            gfx_index, transcoder, expected_bpc_str, bpc_dict[trans_ddi_value.BitsPerColor])
        logging.error("FAIL :" + title)
        common_utility.gdhm_report_app_color(title=title)
        status = False

    return status


##
# @brief         Verify the register programming for dithering feature
# @param[in]     gfx_index - gfx adapter index
# @param[in]     platform - Name of the platform
# @param[in]     pipe - current pipe
# @param[in]     transcoder - current transcoder
# @param[in]     enable - Boolean value to be either True or False
# @return        status - True on Success, False otherwise
def verify_dithering_feature(gfx_index: str, platform: str, pipe: str, transcoder: str, enable: bool) -> bool:
    bpc_dict = {0: "BPC8", 1: "BPC10", 2: "BPC6", 3: "BPC12"}
    dithering_type_dict = {0: "SPATIAL", 1: "ST1", 2: "ST2", 3: "TEMPORAL"}
    status = False
    regs = DisplayRegs.get_interface(platform, gfx_index)
    transcoder = DisplayRegs.DisplayRegsInterface.TranscoderType(transcoder).name
    trans_ddi_func_offset = regs.get_trans_ddi_offsets(transcoder)
    data = color_mmiointerface.read(gfx_index, trans_ddi_func_offset.FuncCtrlReg)
    trans_ddi_value = regs.get_trans_ddi_info(transcoder, TransDDiOffsetsValues(FuncCtrlReg=data))

    color_ctl_offsets = regs.get_color_ctrl_offsets(pipe)
    pipe_misc_data = color_mmiointerface.read(gfx_index, color_ctl_offsets.PipeMisc)
    color_ctl_values = regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(PipeMisc=pipe_misc_data))
    ##
    # Verify Dithering status
    if color_ctl_values.DitheringEnable == int(enable):
        logging.info("PASS: Dithering on Adapter {0} Pipe {1} Expected {2} and Actual : {3}".format(
            gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[color_ctl_values.DitheringEnable]))
        status = True
    else:
        title = "Dithering on Adapter {0} Pipe {1} Expected {2} and Actual : {3}".format(
            gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[color_ctl_values.DitheringEnable])
        logging.error("FAIL :" + title)
        common_utility.gdhm_report_app_color(title=title)
        return status

    ##
    # Compare trans ddi and pipe misc BPC
    if color_ctl_values.DitheringEnable:
        if color_ctl_values.DitheringType == 0:
            logging.info("PASS : Dithering Type Expected: {0} Actual: {1}".format(
                dithering_type_dict[0], dithering_type_dict[color_ctl_values.DitheringType]))
        else:
            title = "Dithering Type Expected: {0} Actual: {1}".format(
                dithering_type_dict[0], dithering_type_dict[color_ctl_values.DitheringType])
            logging.info("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
            status = False
            return status

        if trans_ddi_value.BitsPerColor == color_ctl_values.DitheringBpc:
            logging.info("PASS:  Dithering BPC {0} and Transcoder BPC: {1}".format(
                bpc_dict[trans_ddi_value.BitsPerColor], bpc_dict[color_ctl_values.DitheringBpc]))
        else:
            title = "Dithering BPC : {0} and Transcoder BPC: {1}".format(
                bpc_dict[trans_ddi_value.BitsPerColor], bpc_dict[color_ctl_values.DitheringBpc])
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
            status = False
    return status


##
# @brief         Check the register programming for  hdr feature
# @param[in]     gfx_index - gfx adapter index
# @param[in]     platform - Name of the platform
# @param[in]     pipe - current pipe
# @return        pipe_misc_obj.HdrMode - 0 or 1
def hdr_status(gfx_index: str, platform: str, pipe: str) -> bool:
    sys_util = system_utility.SystemUtility()
    exec_env = sys_util.get_execution_environment_type()
    if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_index):
        start_plane_processing()
    regs = DisplayRegs.get_interface(platform, gfx_index)
    color_ctl_offsets = regs.get_color_ctrl_offsets(pipe)
    pipe_misc_data = color_mmiointerface.read(gfx_index, color_ctl_offsets.PipeMisc)
    pipe_misc_obj = regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(PipeMisc=pipe_misc_data))
    logging.debug(
        "HDR status on Adapter {0} Pipe {1} : {2}".format(gfx_index, pipe, BIT_MAP_DICT[pipe_misc_obj.HdrMode]))
    return True if pipe_misc_obj.HdrMode else False


##
# @brief         Verify the register programming for  hdr feature
# @param[in]     gfx_index - gfx adapter index
# @param[in]     platform - Name of the platform
# @param[in]     pipe - current pipe
# @param[in]     enable - Boolean value to be either True or False
# @return        status - True on Success, False otherwise
def verify_hdr_feature(gfx_index: str, platform: str, pipe: str, enable: bool) -> bool:
    status = False
    is_hdr_supported = hdr_status(gfx_index, platform, pipe)
    ##
    # Verify HDR Mode
    if is_hdr_supported == int(enable):
        logging.info("PASS: HDR Mode on Adapter {0} Pipe {1} Expected = {2} and Actual = {3}".format(
            gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[is_hdr_supported]))
        status = True
    else:
        title = "HDR Mode on Adapter {0} Pipe {1} Expected= {2} and Actual = {3}".format(
            gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[is_hdr_supported])
        logging.error("FAIL :" + title)
        common_utility.gdhm_report_app_color(title=title)

    return status


##
# @brief         Verify the register programming lace or fast lace feature
# @param[in]     gfx_index - gfx adapter index
# @param[in]     platform - Name of the platform
# @param[in]     pipe - current pipe
# @param[in]     enable - Boolean value to be either True or False
# @param[in]     version - LACE, FASTLACE
# @return        status - True on Success, False otherwise
def verify_lace_feature(gfx_index: str, platform: str, pipe: str, enable: bool, version: str) -> bool:
    status = False
    regs = DisplayRegs.get_interface(platform, gfx_index)
    dplc_offset = regs.get_lace_offsets(pipe)
    dplc_data = color_mmiointerface.read(gfx_index, dplc_offset.DplcControl)
    dplc_value = regs.get_lace_info(pipe, LaceOffsetsValues(DplcControl=dplc_data))
    #
    # LACE status
    if dplc_value.FunctionEnable == int(enable):
        logging.info(
            "PASS : LACE Function enable status on Adapter {0} Pipe {1} : Expected= {2} and Actual = {3}".format(
                gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[dplc_value.FunctionEnable]))
        status = True
    else:
        title = "LACE Function enable status on Adapter {0} Pipe {1} : Expected= {2} and Actual = {3}".format(
            gfx_index, pipe, BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[dplc_value.FunctionEnable])
        logging.error("FAIL :" + title)
        common_utility.gdhm_report_app_color(title=title)
        return status

    # As per spec IE Enable field is ignored if the function is disabled.
    if enable:
        # LACE IE Enable
        if dplc_value.IeEnable == int(enable):
            logging.info("PASS : LACE IE Enable status : Expected={0} and Actual ={1}".format(
                         BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[dplc_value.IeEnable]))
        else:
            title = "LACE IE Enable status : Expected= {0} and Actual ={1}".format(BIT_MAP_DICT[int(enable)],BIT_MAP_DICT[dplc_value.IeEnable])
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
            status = False
            return status

        if version == "FAST_LACE":
            if dplc_value.FastAccessModeEnable:
                logging.info('PASS : LACE Fast Access mode status: Expected = ENABLE, Actual = ENABLE')
                status = True
            else:
                title = 'LACE Fast Access mode status: Expected = ENABLE, Actual = DISABLE'
                logging.error("FAIL :" + title)
                common_utility.gdhm_report_app_color(title=title)
                status = False
    return status


##
# @brief         Verify the register programming for  ycbcr feature
# @param[in]     gfx_index - gfx adapter index
# @param[in]     platform - Name of the platform
# @param[in]     pipe - current pipe
# @param[in]     enable - Boolean value to be either True or False
# @param[in]     sampling - enum type of YUV420,YUV422,YUV444
# @return        status - True on Success, False otherwise
def verify_ycbcr_feature(gfx_index: str, platform: str, pipe: str, enable: bool,
                         sampling=color_enums.YuvSampling.YUV444) -> bool:
    status = False
    pipe_colorspace_dict = {0: "RGB", 1: "YUV"}
    regs = DisplayRegs.get_interface(platform, gfx_index)
    color_ctl_offsets = regs.get_color_ctrl_offsets(pipe)
    pipe_misc_data = color_mmiointerface.read(gfx_index, color_ctl_offsets.PipeMisc)
    pipe_misc2_data = color_mmiointerface.read(gfx_index, color_ctl_offsets.PipeMisc2)
    csc_mode_data = color_mmiointerface.read(gfx_index, color_ctl_offsets.CscMode)
    color_ctl_value = regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(PipeMisc=pipe_misc_data,
                                                                         PipeMisc2=pipe_misc2_data,
                                                                         CscMode=csc_mode_data))

    if enable:
        # Colorspace verification
        if pipe_colorspace_dict[color_ctl_value.PipeOutputColorSpaceSelect] == "YUV":
            logging.info(" PASS : Pipe output colorspace on Adapter {0} Pipe {1}  Expected:{2} Actual: {3}".format
                         (gfx_index, pipe, "YUV", pipe_colorspace_dict[color_ctl_value.PipeOutputColorSpaceSelect]))
            status = True
        else:
            title = " Pipe output colorspace on Adapter {0} Pipe {1}  Expected:{2} Actual: {3}".format(
                gfx_index, pipe, "YUV", pipe_colorspace_dict[color_ctl_value.PipeOutputColorSpaceSelect])
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
            return status
        # OCSC enable verification
        if color_ctl_value.PipeOutputCscEnable == int(enable):
            logging.info("PASS : Pipe OutputCsc Expected:{0}; Actual:{1}".format
                         (BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[color_ctl_value.PipeOutputCscEnable]))
        else:
            title = "Pipe OutputCsc Expected:{0}; Actual:{1}".format(
                BIT_MAP_DICT[int(enable)], BIT_MAP_DICT[color_ctl_value.PipeOutputCscEnable])
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
            status = False
            return status
        # Sampling verification
        if sampling == color_enums.YuvSampling.YUV444:
            if not color_ctl_value.Yuv420Enable:
                logging.info("PASS : YUV420 : Expected - DISABLED; Actual - DISABLED")
            else:
                status = False
                title = "YUV420: Expected - DISABLED; Actual - ENABLED"
                logging.error("FAIL :" + title)
                common_utility.gdhm_report_app_color(title=title)
                return status
        elif sampling == color_enums.YuvSampling.YUV422:
            if color_ctl_value.Yuv422Mode:
                logging.info("PASS : YUV422 : Expected - ENABLED; Actual - ENABLED")
            else:
                title = "YUV422: Expected - ENABLED; Actual - DISABLED"
                logging.error("FAIL :" + title)
                common_utility.gdhm_report_app_color(title=title)
                status = False
                return status

            if not color_ctl_value.Yuv420Enable:
                logging.info("PASS : YUV420 mode : Expected - DISABLED; Actual - DISABLED")
            else:
                status = False
                title = "YUV420 mode: Expected - DISABLED; Actual - ENABLED"
                logging.error("FAIL :" + title)
                common_utility.gdhm_report_app_color(title=title)
                return status
        elif sampling == color_enums.YuvSampling.YUV420:
            if color_ctl_value.Yuv420Enable:
                logging.info("PASS : YUV420 mode : Expected - ENABLED ; Actual - ENABLED")
            else:
                title = " YUV420 mode: Expected - ENABLED; Actual - DISABLED"
                logging.error("FAIL :" + title)
                common_utility.gdhm_report_app_color(title=title)
                status = False
                return status

    else:
        if pipe_colorspace_dict[color_ctl_value.PipeOutputColorSpaceSelect] == "RGB":
            logging.info("PASS : Pipe output colorspace on Adapter {0} Pipe {1} Expected:{2} Actual: {3}".format(
                gfx_index, pipe, "RGB", pipe_colorspace_dict[color_ctl_value.PipeOutputColorSpaceSelect]))
            status = True
        else:
            title = "SPipe output colorspace on Adapter {0} Pipe {1} Expected:{2} Actual: {3}".format(
                gfx_index, pipe, "RGB", pipe_colorspace_dict[color_ctl_value.PipeOutputColorSpaceSelect])
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
            status = False

    return status

