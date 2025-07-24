import logging
import time

import DisplayRegs
from DisplayRegs import DisplayArgs
from DisplayRegs.DisplayOffsets import Hw3dLutOffsetsValues, PipeFrameCtrOffsetValues
from Libs.Core import etl_parser
from Tests.Color.Common.color_constants import POST_GEN14_PLATFORMS
from Tests.Color.Common import color_properties
from Tests.Color.Common import color_mmio_interface, common_utility
from Tests.Color.Common.common_utility import get_bit_value, perform_plane_processing, get_psr_caps
from Tests.Color.Verification import feature_basic_verify, gen_verify_pipe
from Tests.PowerCons.Functional.DCSTATES.dc_state import get_etl_trace
from registers.mmioregister import MMIORegister

mmio_interface = color_mmio_interface.ColorMmioInterface()


def verify(gfx_index: str, platform: str, port:str, pipe: str, transcoder:str, target_id: int, input_file, is_lfp,enable: bool, via_igcl = False):
    feature_caps = color_properties.FeatureCaps()
    feature_caps = get_psr_caps(target_id, feature_caps)

    # Ignoring the HW_3DLUT verification for PSR capable panels, till the IGCL PSR bug fixed HSD-18032331787.
    if feature_caps.PSRSupport is False:
        ##
        # verify_hw3dlut_feature
        if platform in POST_GEN14_PLATFORMS:
            logging.info("Skip: Platform :{0} PSR/DC state Disable for 3DLUT verification".format(platform))
        else:
            if is_lfp:  # For external display - feature caps for psr return true sporadically. so added check
                if common_utility.toggle_psr_and_verify(gfx_index, platform, target_id, port, pipe, transcoder,
                                                        enable=False) is False:
                    logging.error("Switch to PSR enable and verify scenario failed on gfx_index{0} and Target ID:{1}".format(gfx_index,
                                                                                                                         target_id))
                    return False
        pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)
    
        if feature_basic_verify.verify_hw3dlut_feature(gfx_index, platform, pipe, enable):
            if enable:
                if via_igcl:
                  ref_lut = get_ref_lut_value_igcl(input_file)
                else:
                  ref_lut = get_ref_lut_value(input_file)
                if not pipe_verification.verify_hw3dlut(gfx_index, platform, port, pipe, transcoder, target_id, ref_lut):
                    return False
        else:
            return False
    
        if platform in POST_GEN14_PLATFORMS:
            logging.info("Skip: Platform :{0} PSR/DC state Disable for 3DLUT verification".format(platform))
        else:
            if is_lfp:  # For external display - feature caps for psr return true sporadically. so added check
                if common_utility.toggle_psr_and_verify(gfx_index, platform, target_id, port, pipe, transcoder, enable=True) is False:
                    logging.error("Switch to PSR enable and verify scenario failed on gfx_index{0} and Target ID:{1}".format(gfx_index,
                                                                                                                         target_id))
                    return False
    return True

def setup_for_verify(exec_env, gfx_index, platform, current_pipe):
    pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)
    # exec_env (For Ex: ExecutionEnv.POST_SI)
    if 'ExecutionEnv.PRE_SI_SIM' in str(exec_env):
        perform_plane_processing(gfx_index)
        # Keep buffer, simulation it takes considerable time for ready bit reset.
        time.sleep(20)
    elif 'ExecutionEnv.PRE_SI_EMU' in str(exec_env):
        wait_for_frame_cntr_incr(gfx_index, current_pipe, pipe_verification)
        # Keep buffer, emulation it takes considerable time for ready bit reset.
        time.sleep(300)

def wait_for_frame_cntr_incr(gfx_index, pipe, pipe_verification):
    pipe_frame_cntr_val_incr = 0
    pipe_frame_ctr_off = pipe_verification.regs.get_pipe_frame_ctr_offsets(pipe)
    data = mmio_interface.read(gfx_index, pipe_frame_ctr_off.pipe_frm_cntr_offset)
    pipe_frm_cntr_offset_value = pipe_verification.regs.get_pipe_frame_ctr_info(pipe, PipeFrameCtrOffsetValues(pipe_frm_cntr_offset=data))
    while pipe_frame_cntr_val_incr - pipe_frm_cntr_offset_value.pipe_frm_cntr_offset < 2:
        data_1 = mmio_interface.read(gfx_index, pipe_frame_ctr_off.pipe_frm_cntr_incr)
        pipe_frm_cntr_offset_incr_value = pipe_verification.regs.get_pipe_frame_ctr_info(pipe, PipeFrameCtrOffsetValues(pipe_frm_cntr_incr=data_1))
        pipe_frame_cntr_val_incr = pipe_frm_cntr_offset_incr_value.pipe_frm_cntr_incr


def get_ref_lut_value(input_file):
    red_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                0x300, 0x340, 0x380, 0x3C0, 0x3FC]
    green_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                  0x300, 0x340, 0x380, 0x3C0, 0x3FC]
    blue_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                 0x300, 0x340, 0x380, 0x3C0, 0x3FC]
    ref_lut = []
    count = 0
    if "CUSTOMLUT_NO_R.BIN" in input_file:
        for i in range(0, 17):
            red_data[i] = 0
    elif "CUSTOMLUT_NO_G.BIN" in input_file:
        for i in range(0, 17):
            green_data[i] = 0
    elif "CUSTOMLUT_NO_B.BIN" in input_file:
        for i in range(0, 17):
            blue_data[i] = 0
    for i in range(0, 17):
        for j in range(0, 17):
            for k in range(0, 17):
                ref_lut.append(red_data[i])
                ref_lut.append(green_data[j])
                ref_lut.append(blue_data[k])
                count = count + 3
    return ref_lut


def get_ref_lut_value_igcl(input_file):
    red_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                0x300, 0x340, 0x380, 0x3C0, 0x3FF]
    green_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                  0x300, 0x340, 0x380, 0x3C0, 0x3FF]
    blue_data = [0x0, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0,
                 0x300, 0x340, 0x380, 0x3C0, 0x3FF]
    ref_lut = []
    count = 0
    if "CUSTOMLUT_NO_R.BIN" in input_file:
        for i in range(0, 17):
            red_data[i] = 0
    elif "CUSTOMLUT_NO_G.BIN" in input_file:
        for i in range(0, 17):
            green_data[i] = 0
    elif "CUSTOMLUT_NO_B.BIN" in input_file:
        for i in range(0, 17):
            blue_data[i] = 0
    for i in range(0, 17):
        for j in range(0, 17):
            for k in range(0, 17):
                ref_lut.append(red_data[i])
                ref_lut.append(green_data[j])
                ref_lut.append(blue_data[k])
                count = count + 3
    return ref_lut
