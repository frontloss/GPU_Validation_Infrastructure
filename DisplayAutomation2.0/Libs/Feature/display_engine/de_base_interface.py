########################################################################################################################################################
# @file         de_base_interface.py
# @brief        Python Wrapper that exposes the interface for Display Pipeline Validation
# @remarks      Checks for the platform and calls the correct implementation
# @author       akaleem
#########################################################################################################################################################


import logging
from typing import Tuple, List

from Libs.Core import system_utility as sys_utility
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.logger import gdhm
from Libs.Feature.display_engine.de_base.display_scalar import DisplayScalar
from Libs.Feature.presi.presi_crc import start_plane_processing
from Tests.Planes.Common import planes_helper
from registers.mmioregister import MMIORegister


reg_read = MMIORegister()
system_utility = sys_utility.SystemUtility()
platform = None
gfx_display_hwinfo = SystemInfo().get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for adapter_count in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[adapter_count].DisplayAdapterName).upper()
    break

if platform in ["SKL", "KBL", "CFL", "GLK", "CNL", "ICLLP", "JSL", "ICLHP", "LKF1", "TGL", "RYF", "DG1", 'RKL', 'DG2',
                'ADLP', 'ADLS', 'MTL', 'ELG', 'LNL', 'PTL', 'NVL', 'CLS']:
    from Libs.Feature.display_engine.de_base.display_base import *
    from Libs.Feature.display_engine.de_base.display_plane import *
    from Libs.Feature.display_engine.de_base.display_pipe import *
    from Libs.Feature.display_engine.de_base.display_transcoder import *
    from Libs.Feature.display_engine.de_base.display_ddi import *
    from Libs.Feature.display_engine.de_base.display_dip_control import *
    from Libs.Feature.display_engine.de_base.display_phy_buffer import *
else:
    gdhm.report_bug(
        title="[Interfaces][Display_Engine][Display_Base_Interface]: DE programming verification is not supported on {}"
              " platform".format(platform),
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Test.DISPLAY_INTERFACES,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )
    logging.error("display_base :: Platform Not Supported: %s" % platform)


##
# @brief Based on the platform, calls the correct implementation
# @param[in] display_port display to verify
# @return bool pipe and ddi mapped to display_port
def get_pipe_ddi_attached_to_port(display_port):
    mapped_pipe_ddi = DisplayBase(display_port)
    return mapped_pipe_ddi.pipe, mapped_pipe_ddi.ddi


##
# @brief        Static Method that helps to get values required to pass to DE Verification.
# @param[in]    gfx_index: str
#                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
# @param[in]    display_port: str
#                   Port Name in Which the Display is Plugged.
# @param[in]    bpc: int
#                   Represents number of bits per component.
# @param[in]    color_format_info: str
#                   Represents color space.
# @param[in]    scaling_type: str
#                   Scaling mode MAR/CI/FS
# @return Returns the list of adjacent planes, pipes and DisplayTranscoder, DisplayDIPControl scalar objects.
def get_display_context(gfx_index: str, display_port: str, bpc: int, color_format_info: str, scaling_type="Default"
                        ) -> Tuple[List[DisplayPipe], List[DisplayPlane], List[DisplayTranscoder],
                                   List[DisplayDIPControl], List[DisplayScalar]]:
    scalar_list = []
    pipe_list = []
    plane_list = []
    scalar_list.append(DisplayScalar(display_port, scaling_type, gfx_index=gfx_index))
    pipe_list.append(DisplayPipe(display_port, color_format_info, gfx_index=gfx_index))
    plane_list.append(DisplayPlane(display_port, gfx_index=gfx_index))
    trans_obj = DisplayTranscoder(display_port, pipe_color_space=color_format_info, bpc=bpc, gfx_index=gfx_index)
    dp_ctl_obj = DisplayDIPControl(display_port, bpc, gfx_index)
    is_pipe_joiner_req, num_pipes = DisplayClock.is_pipe_joiner_required(gfx_index, display_port)
    for i in range(1, num_pipes):
        pipe_obj = DisplayPipe(display_port, color_format_info, gfx_index=gfx_index)
        adj_pipe = chr(ord(pipe_obj.pipe[-1]) + i)
        pipe_obj.pipe = "PIPE_" + adj_pipe
        pipe_obj.pipe_suffix = adj_pipe
        pipe_list.append(pipe_obj)

        plane_obj = DisplayPlane(display_port, gfx_index=gfx_index)
        plane_obj.pipe = pipe_obj.pipe
        plane_obj.pipe_suffix = adj_pipe
        plane_list.append(plane_obj)

        scalar_obj = DisplayScalar(display_port, scaling_type, gfx_index=gfx_index)
        scalar_obj.pipe = pipe_obj.pipe
        scalar_obj.pipe_suffix = adj_pipe
        scalar_list.append(scalar_obj)

    return pipe_list, plane_list, [trans_obj], [dp_ctl_obj], scalar_list

##
# @brief Checks for the platform and calls the correct implementation for plane verification
# @param[in] portList ports to verify
# @param[in] planeList planes to verify
# @param[in] gfx_index graphics adapter
# @return bool plane verification pass/fail
def verify_plane_programming(portList, planeList=None, gfx_index='gfx_0'):
    if planeList is None:
        planeList = []
        for display in portList:
            planeList.append(DisplayPlane(display, gfx_index=gfx_index))

    exec_env = system_utility.get_execution_environment_type()
    if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_index):
        start_plane_processing()
    if exec_env == 'SIMENV_PIPE2D' and planes_helper.get_flipq_status(gfx_index):
        for display in portList:
            display_base_obj = DisplayBase(display, platform, gfx_index=gfx_index)
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(display, gfx_index)
            current_pipe = chr(int(current_pipe) + 65)
            frame_cnt = importlib.import_module("registers.%s.PIPE_FRMCNT_REGISTER" % platform)

            frame_cnt_reg = 'PIPE_FRMCNT_' + current_pipe
            frame_cnt_val = reg_read.read('PIPE_FRMCNT_REGISTER', frame_cnt_reg, platform, 0x0)
            current_frame_cnt_val = frame_cnt_val.__getattribute__("pipe_frame_counter")
            logging.info(f"Frame counter value {current_frame_cnt_val}")
            count = 0
            while True:
                time.sleep(600)
                count = count + 1
                frame_cnt_val = reg_read.read('PIPE_FRMCNT_REGISTER', frame_cnt_reg, platform, 0x0)
                updated_frame_cnt_val = frame_cnt_val.__getattribute__("pipe_frame_counter")
                if updated_frame_cnt_val > current_frame_cnt_val:
                    logging.info(
                        f"Frame cnt val current_frame_cnt_val {current_frame_cnt_val} updated_frame_cnt_val {updated_frame_cnt_val}")
                    break
                elif count > 5:
                    logging.info("Count exceeded")
                    break

    return VerifyPlaneProgramming(planeList, gfx_index)


##
# @brief Checks for the platform and calls the correct implementation for pipe verification
# @param[in] portList ports list
# @param[in] pipeList pipes list
# @param[in] gfx_index graphics adapter
# @return bool pipe verification pass/fail
def verify_pipe_programming(portList, pipeList=None, gfx_index='gfx_0'):
    if pipeList is None:
        pipeList = []
        for display in portList:
            pipeList.append(DisplayPipe(display, "RGB", gfx_index=gfx_index))
    return VerifyPipeProgramming(pipeList, gfx_index)


##
# @brief Checks for the platform and calls the correct implementation for transcoder verification
# @param[in] portList ports list
# @param[in] transcoderList transcoder list
# @param[in] gfx_index graphics adapter
# @return bool transcoder verification pass/fail
def verify_transcoder_programming(portList, transcoderList=None, gfx_index='gfx_0'):
    if transcoderList is None:
        transcoderList = []
        for display in portList:
            transcoderList.append(DisplayTranscoder(display, gfx_index=gfx_index))
    return VerifyTranscoderProgramming(transcoderList, gfx_index)


##
# @brief Checks for the platform and calls the correct implementation for ddi verification
# @param[in] portList ports list
# @param[in] ddiList ddi list
# @param[in] gfx_index graphics adapter
# @return bool ddi verification pass/fail
def verify_ddi_programming(portList, ddiList=None, gfx_index='gfx_0'):
    if ddiList is None:
        ddiList = []
        for display in portList:
            ddiList.append(DisplayDDI(display, gfx_index=gfx_index))
    return VerifyDDIProgramming(ddiList, gfx_index)


##
# @brief Checks for the platform and calls the correct implementation for dip ctrl verification
# @param[in] portList ports list
# @param[in] dipList ddi list
# @param[in] gfx_index graphics adapter
# @return bool dip ctrl verification pass/fail
def verify_videoDIPCtrl_programming(portList, dipList=None, gfx_index='gfx_0'):
    if dipList is None:
        dipList = []
        for display in portList:
            dipList.append(DisplayDIPControl(display, gfx_index=gfx_index))
    return VerifyDisplayDIPControl(dipList, gfx_index)


##
# @brief Checks for the platform and calls the correct implementation for phy buffer programming verification
# @param[in] portList ports list
# @param[in] phyList phy list
# @param[in] gfx_index graphics adapter
# @return bool ddi verification pass/fail
def verify_phy_buffer_programming(portList, phyList=None, gfx_index='gfx_0'):
    if phyList is None:
        phyList = []
        for display in portList:
            phyList.append(DisplayPhyBuffer(display, gfx_index=gfx_index))
    return VerifyPhyBufferProgramming(phyList, gfx_index=gfx_index)


##
# @brief Checks for the platform and calls the correct implementation for dip avi data  verification
# @param[in] portList ports list
# @param[in] dipList ddi list
# @param[in] gfx_index graphics adapter
# @return bool dip avi data bytes verification pass/fail
def verify_videodipavi_infoframe(portList, dipList=None, gfx_index='gfx_0'):
    if dipList is None:
        dipList = []
        for display in portList:
            dipList.append(DisplayDIPControl(display, gfx_index=gfx_index))
    return VerifyDisplayDIPAVIdata(dipList, gfx_index)


