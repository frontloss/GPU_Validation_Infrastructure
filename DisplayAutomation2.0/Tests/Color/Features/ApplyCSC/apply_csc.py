import logging

from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Tests.Color import color_common_utility
from Tests.Color.Common import csc_utility, color_mmio_interface, color_escapes
from Tests.Color.Verification import feature_basic_verify, gen_verify_pipe
from Libs.Core.logger import gdhm
from Libs.Feature.presi.presi_crc import start_plane_processing
from Libs.Core import system_utility
from Tests.Planes.Common import planes_helper


def verify_gamma_ctrl_prog_linear_mode(gfx_index, platform, pipe, color_conv_blk="cc1"):
    sys_util = system_utility.SystemUtility()
    exec_env = sys_util.get_execution_environment_type()
    if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_index):
        start_plane_processing()

    mmio_interface = color_mmio_interface.ColorMmioInterface()
    pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)

    ##
    # verify ocsc oceff and pre/post offsets
    color_ctl_offsets = pipe_verification.regs.get_color_ctrl_offsets(pipe)
    csc_mode_data = mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
    gamma_mode_data = mmio_interface.read(gfx_index,color_ctl_offsets.GammaMode)
    csc_mode_value = pipe_verification.regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(CscMode=csc_mode_data))
    color_ctl_value = pipe_verification.regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(GammaMode=gamma_mode_data))
    ##
    # In case of Linear CSC, need to check DeGamma and Gamma Enable bits
    if color_conv_blk == "CC1":
        if csc_mode_value.PipeCscEnable:
            logging.info("PASS: Pipe CSC CC1: Expected = ENABLE and Actual = ENABLE")
            if color_ctl_value.PreCscGammaEnable:
                logging.info("PASS: Pipe Pre CSC CC1 Gamma : Expected = ENABLE Actual = ENABLE")
            else:
                logging.error("FAIL: Pipe Pre CSC CC1 Gamma : Expected = ENABLE Actual = DISABLE")
                gdhm.report_driver_bug_os("Pipe Pre CSC CC1 Gamma Verification failed for Adapter: {0} Pipe: {1} : "
                                            "Expected = ENABLE Actual = DISABLE".format(gfx_index, pipe))
                return False
        else:
            logging.error("FAIL: Pipe CSC CC1 : Expected = ENABLE Actual = DISABLE")
            gdhm.report_driver_bug_os("Pipe CSC CC1 Verification failed for Adapter: {0} Pipe: {1} : "
                                        "Expected = ENABLE Actual = DISABLE".format(gfx_index,pipe))
            return False
    else:
        if csc_mode_value.PipeCscCC2Enable:
            logging.info("PASS: Pipe CSC CC2 : Expected = ENABLE and Actual = ENABLE")
            if color_ctl_value.PreCscCc2GammaEnable:
                logging.info("PASS: Pipe Pre CSC CC2 Gamma : Expected = ENABLE Actual = ENABLE")
            else:
                logging.error("FAIL: Pipe Pre CSC CC2 Gamma : Expected = ENABLE Actual = DISABLE")
                gdhm.report_driver_bug_os("Pipe Pre CSC CC2 Gamma Verification failed for Adapter: {0} Pipe: {1} : "
                                            "Expected = ENABLE Actual = DISABLE".format(gfx_index,pipe))
                return False
        else:
            logging.error("FAIL: Pipe CSC CC2 : Expected = ENABLE Actual = DISABLE")
            gdhm.report_driver_bug_os("Pipe CSC CC2 Verification failed for Adapter: {0} Pipe: {1} : "
                                        "Expected = ENABLE Actual = DISABLE".format(gfx_index,pipe))
            return False
