####################################################################################################
# @file     display_scalar.py
# @brief    Python wrapper exposes interfaces for Display Scalar Verification
# @details  display_scalar.py provides interface's to Verify Display Scalar programming
#           for HDMI, DP.
#           User-Input : DisplayScalar() instance - display_port to be verifed for scalar programming
#           DisplayScalar information mentioned below: \n
# @note     Supported display interfaces are DP, HDMI\n
# @author   Aafiya Kaleem
##################################################################################################

import logging
import os
import math

from Libs.Core import system_utility as sys_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_engine.de_base.display_pipe import PIPEEXCESS
from registers.mmioregister import MMIORegister

DISP_NUM_PIXELS_PER_CLK = 2


##
# @brief DisplayScalar Base Class. Has functions for Scalar verification
class DisplayScalar(display_base.DisplayBase):
    xsize = 0
    ysize = 0
    xpos = 0
    ypos = 0
    scalar_flag = 0

    ##
    # @brief Initializes Display Scalar Object
    # @param[in] display_port display to create the object for
    # @param[in] scaling_mode CI/MDS/MAR/CAR
    # @param[in] gfx_index graphics adapter
    def __init__(self, display_port, scaling_mode, gfx_index='gfx_0'):
        self.display_port = display_port
        self.scaling_mode = scaling_mode
        display_base.DisplayBase.__init__(self, display_port, gfx_index=gfx_index)


##
# @brief Verify if Pipe Scalar is enabled for display, verify scalar plane size and position.
# @param[in] scalarObj scalar object
# @param[in] down_scale_percent_x amount of x-downscale to do; 100: No Scaling, 1: Max Scaling(11 percent)
# @param[in] down_scale_percent_y amount of y-downscale to do; 100: No Scaling, 1: Max Scaling(11 percent)
# @return Return true if MMIO programming is correct, else return false
def VerifyScalar(scalarObj, down_scale_percent_x = 0, down_scale_percent_y = 0):
    scalar_flag = 0
    pipe = scalarObj.pipe.split("PIPE_")
    PLATFORM = scalarObj.platform

    scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_%s" % (pipe[1]), PLATFORM)
    logging.debug("PS_CTRL_1_" + pipe[1] + "--> Offset : "
                  + format(scalar1_reg.offset, '08X') + " Value :" + format(scalar1_reg.asUint, '08X'))

    scalar2_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_%s" % (pipe[1]), PLATFORM)
    logging.debug("PS_CTRL_2_" + pipe[1] + "--> Offset : "
                  + format(scalar2_reg.offset, '08X') + " Value :" + format(scalar2_reg.asUint, '08X'))

    if ((scalar1_reg.enable_scaler) and (scalar1_reg.scaler_binding == 0)):  # Pipe scalar enabled
        logging.info("INFO : %s - Scalar1 is enabled on Pipe%s" % (scalarObj.display_port, pipe[1]))
        scalar_flag = 1
    elif (scalar2_reg.enable_scaler) and (scalar2_reg.scaler_binding == 0):
        logging.info("INFO : %s - Scalar2 is enabled on Pipe%s" % (scalarObj.display_port, pipe[1]))
        scalar_flag = 2
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][SCALAR]:Pipe Scalar not enabled on Pipe{} - for Port{}".format(
                 pipe[1], scalarObj.display_port),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("ERROR : Pipe Scalar is not enabled.")
        return False

    status = get_scalar_size_position(scalarObj, down_scale_percent_x, down_scale_percent_y)
    if status is False:
        return status

    return VerifyScalarSizePosition(scalarObj, scalar_flag)


##
# @brief Verify display Scalar Plane size and position registers (PS_WIN_SZ_REGISTER, PS_WIN_POS_REGISTER).
# @param[in] scalarObj Scalar Object used for verification
# @param[in] scalar_flag (to specify if scalar 1 or scalar 2 is enabled)
# @return bool Return true if MMIO programming is correct, else return false
def VerifyScalarSizePosition(scalarObj, scalar_flag):
    pipe = scalarObj.pipe.split("PIPE_")
    PLATFORM = scalarObj.platform

    scalar_size = MMIORegister.read("PS_WIN_SZ_REGISTER", "PS_WIN_SZ_%s_%s" % (scalar_flag, pipe[1]), PLATFORM)
    logging.debug("PS_WIN_SZ_%s_%s" % (scalar_flag, pipe[1]) + "--> Offset : "
                  + format(scalar_size.offset, '08X') + " Value :" + format(scalar_size.asUint, '08X'))

    if (scalar_size.xsize == scalarObj.xsize) and (scalar_size.ysize == scalarObj.ysize):
        logging.info("PASS : HeightxWidth for PS_WIN_SZ_%s_%s Expected : %sx%s Actual : %sx%s"
                     % (scalar_flag, pipe[1], scalarObj.xsize, scalarObj.ysize, scalar_size.xsize, scalar_size.ysize))

        scalar_pos = MMIORegister.read("PS_WIN_POS_REGISTER", "PS_WIN_POS_%s_%s" % (scalar_flag, pipe[1]), PLATFORM)
        logging.debug("PS_WIN_POS_%s_%s" % (scalar_flag, pipe[1]) + "--> Offset : "
                      + format(scalar_pos.offset, '08X') + " Value :" + format(scalar_pos.asUint, '08X'))
        if (scalar_pos.xpos == scalarObj.xpos) and (scalar_pos.ypos == scalarObj.ypos):
            logging.info("PASS : X,Y-Position for PS_WIN_POS_%s_%s Expected : %sx%s Actual : %sx%s"
                         % (scalar_flag, pipe[1], scalarObj.xpos, scalarObj.ypos, scalar_pos.xpos, scalar_pos.ypos))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][SCALAR]:PS_WIN_POS_{}_{} X,Y position Mis-Matched! Expected: {} x "
                      "{} Actual: {} x {}".format(scalar_flag, pipe[1], scalarObj.xpos, scalarObj.ypos,
                                                  scalar_pos.xpos, scalar_pos.ypos),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL : X,Y-Position for PS_WIN_POS_%s_%s Expected : %sx%s Actual : %sx%s"
                          % (scalar_flag, pipe[1], scalarObj.xpos, scalarObj.ypos, scalar_pos.xpos, scalar_pos.ypos))
            return False
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][SCALAR]:PS_WIN_SZ_{}_{} Height x Width Mis-Matched! Expected: {} x {} "
                  "Actual: {} x {}".format(scalar_flag, pipe[1], scalarObj.xsize, scalarObj.ysize, scalar_size.xsize,
                                           scalar_size.ysize),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("FAIL : HeightxWidth for PS_WIN_SZ_%s_%s Expected : %sx%s Actual : %sx%s"
                      % (scalar_flag, pipe[1], scalarObj.xsize, scalarObj.ysize, scalar_size.xsize, scalar_size.ysize))

    return False


##
# @brief Calculate scalar plane size and position based on scalar mode (CI,FS,MAR)
# @param[in] scalarObj DisplayScalar() instance to specify display_port and scalar mode
# @param[in] down_scale_percent_x amount of x-downscale to do; 100: No Scaling, 1: Max Scaling(11 percent)
# @param[in] down_scale_percent_y amount of y-downscale to do; 100: No Scaling, 1: Max Scaling(11 percent)
# @return Fill scalarObj (xsize, ysize, xpos, ypos)
def get_scalar_size_position(scalarObj, down_scale_percent_x = 0, down_scale_percent_y = 0):
    BIT0 = (1 << 0)
    config = display_config.DisplayConfiguration()
    PLATFORM = scalarObj.platform

    source_mode = config.get_current_mode(scalarObj.targetId)
    src_hactive = source_mode.HzRes
    src_vactive = source_mode.VtRes

    target_mode = config.get_display_timings(scalarObj.targetId)
    tgt_hactive = target_mode.hActive
    tgt_vactive = target_mode.vActive

    logging.info("INFO : Source Mode (HactivexVactive) : %sx%s Target Mode (HactivexVactive) : %sx%s Scaling Mode : %s"
                 % (src_hactive, src_vactive, tgt_hactive, tgt_vactive, scalarObj.scaling_mode))

    if scalarObj.scaling_mode in ["FS", "Stretch"]:
        scalarObj.xsize = tgt_hactive
        scalarObj.ysize = tgt_vactive
        scalarObj.xpos = scalarObj.ypos = 0
    elif scalarObj.scaling_mode == "CI":
        scalarObj.xsize = src_hactive
        scalarObj.ysize = src_vactive
        scalarObj.xpos = ((tgt_hactive // 2) - (src_hactive // 2))
        scalarObj.ypos = ((tgt_vactive // 2) - (src_vactive // 2))
    elif scalarObj.scaling_mode == "MAR":
        utility = sys_utility.SystemUtility()
        if utility.is_ddrw():
            # Yangra
            precisionFactor = 1000000
            precisionFactorby2 = precisionFactor // 2
            stretchFactor = min(((tgt_hactive * precisionFactor) // src_hactive),
                                ((tgt_vactive * precisionFactor) // src_vactive))
            # round div (((x) + (y)/2) / (y))
            scalarObj.xsize = ((src_hactive * stretchFactor) + precisionFactorby2) // precisionFactor
            scalarObj.ysize = ((src_vactive * stretchFactor) + precisionFactorby2) // precisionFactor
            scalarObj.xpos = (tgt_hactive - scalarObj.xsize) // 2
            scalarObj.ypos = (tgt_vactive - scalarObj.ysize) // 2
        else:
            src_aspectratio = float(src_hactive) / float(src_vactive)
            tgt_aspectratio = float(tgt_hactive) / float(tgt_vactive)
            if (tgt_aspectratio < src_aspectratio):
                scalarObj.xsize = tgt_hactive
                scalarObj.ysize = (float(scalarObj.xsize) / src_aspectratio) + 1
                scalarObj.ysize = int(scalarObj.ysize) & (~(BIT0))
            elif (tgt_aspectratio > src_aspectratio):
                scalarObj.ysize = tgt_vactive
                scalarObj.xsize = (float(scalarObj.ysize) * src_aspectratio) + 1
                scalarObj.xsize = int(scalarObj.xsize) & (~(BIT0))
                scalarObj.xpos = (tgt_hactive - scalarObj.xsize) // 2
                scalarObj.ypos = (tgt_vactive - scalarObj.ysize) // 2
    elif (scalarObj.scaling_mode == 'CAR'):
        down_scale_amount_x = (down_scale_percent_x / 100) * 11
        down_scale_amount_y = (down_scale_percent_y / 100) * 11
        scalarObj.xsize = round(src_hactive - (src_hactive * (down_scale_amount_x/100)))
        scalarObj.ysize = round(src_vactive - (src_vactive * (down_scale_amount_y/100)))
        scalarObj.xpos = (tgt_hactive - scalarObj.xsize) // 2
        scalarObj.ypos = (tgt_vactive - scalarObj.ysize) // 2
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][SCALAR]:Unsupported Scalar Mode- {} passed".format(
                scalarObj.scaling_mode),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("Scalar Mode is not supported")
        return False

    is_pipe_joiner_required, no_of_pipe_required = DisplayClock.is_pipe_joiner_required(scalarObj.display_and_adapter_info.adapterInfo.gfxIndex, scalarObj.display_port)
    if is_pipe_joiner_required:
        logging.info("Pipe Joiner is Enabled on Port".format(scalarObj.display_port))
        # source size programmed by driver includes post excess pixels dExcess
        # https://gfxspecs.intel.com/Predator/Home/Index/49247
        scaling_factor_target = src_hactive/tgt_hactive
        destination_excess = ((src_hactive + PIPEEXCESS) / scaling_factor_target) - tgt_hactive

        # https://gfxspecs.intel.com/Predator/Home/Index/49247
        # Window size position calculation for ultra joiner case.
        # In case of ultra joine, when a scaled image spans more than two Pipes, then there will be more than one seams to join.
        # For the tiles that have seams on both sides, PIPE_MISC3 with 2 * Sexcess or 2 * Dexcess
        # PS_WIN_SIZE with D + (2 * Dexcess)
        if no_of_pipe_required == 4:
            if scalarObj.pipe_suffix in ["B", "C"]:
                destination_excess = 2 * destination_excess

        if destination_excess % DISP_NUM_PIXELS_PER_CLK != 0:
            destination_excess = destination_excess - (destination_excess % DISP_NUM_PIXELS_PER_CLK) + DISP_NUM_PIXELS_PER_CLK
        # In case of pipe joiner, each pipe will take source size as equal parts of no of pipes used and do the scaling to that value
        scalarObj.xsize = (tgt_hactive / no_of_pipe_required) + destination_excess

    # Scalar size and position has to be an even number for YUV420 format, if computed size is odd then reduce to 1 as
    # increasing can cause the size to become more than pipe size which is wrong.
    # Keeping the logic common for all color formats and putting changes only for GEN11 to keep in sync with driver
    # TODO:Need to implement for legacy platfroms
    if sys_utility.SystemUtility().is_ddrw():
        scalarObj.xsize = (scalarObj.xsize - 1) if (scalarObj.xsize % 2 != 0) else scalarObj.xsize
        scalarObj.ysize = (scalarObj.ysize - 1) if (scalarObj.ysize % 2 != 0) else scalarObj.ysize
        scalarObj.xpos = (scalarObj.xpos - 1) if (scalarObj.xpos % 2 != 0) else scalarObj.xpos
        scalarObj.ypos = (scalarObj.ypos - 1) if (scalarObj.ypos % 2 != 0) else scalarObj.ypos


##
# @brief Verify display Scalar programming for the passed display_port and scalar mode.
# @param[in] scalarList DisplayScalar() instance to specify display_port and scalar mode
# @param[in] downscale_percent_x amount of x-downscale to do; 100: No Scaling, 1: Max Scaling(11 percent)
# @param[in] downscale_percent_y amount of y-downscale to do; 100: No Scaling, 1: Max Scaling(11 percent)
# @return bool Return true if MMIO programming is correct, else return false
def VerifyScalarProgramming(scalarList, downscale_percent_x = 0, downscale_percent_y = 0):
    status = False
    logging.info("**************SCALAR VERIFICATION START**************")
    for scalarObj in scalarList:
        if scalarObj.pipe is None:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][SCALAR]:ERROR : {} port is NOT Connected to any Pipe".format(
                    scalarObj.display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "ERROR : " + scalarObj.display_port + " is not connected to any Pipe. Check if it is connected")
            return False

        status = VerifyScalar(scalarObj, downscale_percent_x, downscale_percent_y)
        if status is False:
            return status
    logging.info("**************SCALAR VERIFICATION END**************")
    return status


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

    scalarList = []
    scalarList.append(DisplayScalar("DP_B", "Center"))
    result = VerifyScalarProgramming(scalarList)
    if result is False:
        # GDHM handled in VerifyScalarProgramming(scalarList)
        logging.error("FAIL : VerifyScalarProgramming")
    else:
        logging.info("PASS : VerifyScalarProgramming")
