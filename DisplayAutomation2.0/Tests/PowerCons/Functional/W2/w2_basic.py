#######################################################################################################################
# @file         w2_basic.py
# @brief        This file contains unit tests to validate Set Contect Latency (Window2/W2) feature.
# @details      Flow of the unit test is as follows
#               * Simulate required panels (As specified in the command line)
#               * Apply different available native modes across all the connected panels
#               * Calculate available VBlank, line time and min required VBlank to drive the resolution
#               * Verify W2 Size programming
#               * Verify FlipQ in VBlank programming (Yet to be implemented)
#               * Verify PSR2 restrictions and PSR2 enable 
#               * Verify DC6v enable/disable
#
# @author       Gowtham K L
#######################################################################################################################

import importlib
import logging
import unittest

from Libs.Core.logger import gdhm
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.machine_info import machine_info
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules import dut
from Tests.PowerCons.Functional.PSR import psr
from registers.mmioregister import MMIORegister
from Libs.Core.test_env.test_environment import TestEnvironment


##
# @brief        Exposed Class to write W2 tests. Any new W2 test can inherit this class to use common setUp and
#               tearDown functions. W2Basic also includes some functions that can be used across all W2 tests.
class W2Basic(unittest.TestCase):
    cmd_line_param = None
    display_config_ = display_config.DisplayConfiguration()
    VBLANK_REQUIREMENT_PPS_SDP_IN_LINES = 7
    VBLANK_REQUIREMENT_GMP_SDP_IN_LINES = 8
    VBLANK_REQUIREMENT_VSC_EXT_SDP_IN_LINES = 10
    W2_VBLANK_SIZE_THRESHOLD_IN_US  = 5000

    ##
    # @brief        This class method is the entry point for W2 test cases. Helps to initialize some of the
    #               parameters required for W2 test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        dut.prepare(pruned_mode_list=False)

    ##
    # @brief        This API contains the test to be run
    # @return       None
    def runTest(self):
        modes = []
        flipq_in_vblank = False
        # @todo :- Move all the MMIO verification to ETL based as a part of https://jira.devtools.intel.com/browse/VSDI-38109
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.vrr_caps.is_vrr_supported:
                    logging.info(f"Skipping W2 verification on Pipe-{panel.pipe} as it is not VRR supported")
                    continue
                all_supported_modes = self.display_config_.get_all_supported_modes([panel.target_id])
                for _, modes in all_supported_modes.items():
                    for mode in modes:
                        is_psr_enabled = False
                        # Verify W2 only for Sink Target modes and ignore other scaling modes
                        if mode.scaling != enum.MDS:
                            logging.debug(f"Mode {mode} is not a Sink Target Mode. Skipping the W2 check in this mode")
                            continue

                        # Apply required modes
                        logging.info(f"W2 verification with mode : {mode} on Pipe-{panel.pipe} ".center(common.MAX_LINE_WIDTH, "="))
                        if self.display_config_.set_display_mode([mode]) is False:
                            self.fail(f"Failed to apply mode : {mode}")
                        
                        # Calculate available VBlank, line time and min required VBlank to drive the resolution
                        min_req_vblank, available_vblank, line_time_in_us = self.calculate_resolution_requirements(adapter, panel, mode)
                        logging.info(f"Total VBlank of the mode :- {round(available_vblank, 3)}us. Minimum Required VBlank for resolution :- {round(min_req_vblank, 3)}us")

                        # Verify Set Context Latency(W2) Programming
                        scl_verification_status = self.verify_set_context_latency(adapter, panel, mode, available_vblank, min_req_vblank, line_time_in_us)
                        if scl_verification_status is None:
                            continue
                        if scl_verification_status is False:
                            self.fail("Set Context Latency verification failed")
                        logging.info(f"PASS : Set Context Latency verification on {panel.port}")


    ##
    # @brief        This method is the exit point for W2 test cases. This resets the environment changes done
    #               for the execution of W2 tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        dut.reset()


    ##
    # @brief        This API calculates resolution requirement parameters
    # @param[in]    adapter     Adapter         object
    # @param[in]    panel       Panel           object
    # @param[in]    mode        Current mode    object
    # @return       Calculates and returns the following 
    #               min_required_vblank - Minimum VBlank required to drive the resolution
    #               vblank_time_in_us   - Total available VBlank of the current mode 
    #               line_time_in_us     - Line time of the current mode
    def calculate_resolution_requirements(self, adapter, panel, mode):
        platform = adapter.name.lower()
        plane_wm_reg = MMIORegister.read("PLANE_WM_REGISTER", "PLANE_WM_1_"  + panel.pipe, adapter.name)
        psr2_ctl = MMIORegister.read('PSR2_CTL_REGISTER', 'PSR2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
        vid_dip_ctl = MMIORegister.read("VIDEO_DIP_CTL_REGISTER", "VIDEO_DIP_CTL_" + panel.transcoder, adapter.name)
        vsc_ext_sdp_ctl = MMIORegister.read("VSC_EXT_SDP_CTL_REGISTER", "VSC_EXT_SDP_CTL_0_" + panel.transcoder, adapter.name)
        pr_ctl = MMIORegister.get_instance('TRANS_DP2_CTL_REGISTER', 'TRANS_DP2_CTL_' + panel.transcoder, adapter.name)
        alpm_ctl = MMIORegister.read('ALPM_CTL_REGISTER', 'ALPM_CTL_' + panel.transcoder, adapter.name,
                                     gfx_index=adapter.gfx_index)
        if adapter.name in machine_info.PRE_GEN_16_PLATFORMS:
            v_total = MMIORegister.read(
                "TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + panel.transcoder, adapter.name,
                gfx_index=adapter.gfx_index)
        else:
            v_total = MMIORegister.read(
                'TRANS_VRR_VMAX_REGISTER', 'TRANS_VRR_VMAX_' + panel.transcoder, adapter.name,
                gfx_index=adapter.gfx_index)
            v_active = MMIORegister.read(
                "TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + panel.transcoder, adapter.name,
                gfx_index=adapter.gfx_index)
        h_total = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + panel.transcoder,
                                    adapter.name, gfx_index=adapter.gfx_index)

        # VTOTAL and HTOTAL Register values will always be one line lesser than the actual lines
        line_time_in_ns = round(((h_total.horizontal_total + 1) / float(mode.pixelClock_Hz / (1000 * 1000))) * 1000, 3)
        line_time_in_us = round(line_time_in_ns * 0.001, 3)
        if adapter.name in machine_info.PRE_GEN_16_PLATFORMS:
            vertical_total = v_total.vertical_total
            vertical_active = v_total.vertical_active
        else:
            vertical_total = v_total.vrr_vmax
            vertical_active = v_active.vertical_active

        logging.info(f"VTotal of the mode :- {vertical_total}")
        logging.info(f"HTotal of the mode :- {h_total.horizontal_total}")
        logging.info(f"Line Time of the mode :- {line_time_in_us}us")

        vblank_time_in_us = ((vertical_total + 1) - (vertical_active + 1)) * line_time_in_us

        # Frame Start delay and Watermark-0 prefil time are mandatory requirements for any resolution
        frame_start_delay_in_us = line_time_in_us * 1
        watermark_0_prefill_time = line_time_in_ns * plane_wm_reg.lines

        # DSC prefil-time, Pipe Scaler Prefil time, PSR2 VBlank time and SDP VBlank time will vary with panels
        if adapter.name in common.PRE_GEN_15_PLATFORMS:
            psr2_vblank_time = psr2_ctl.psr2_enable * psr2_ctl.block_count_number * line_time_in_us
        else:
            psr2_vblank_time = psr2_ctl.psr2_enable * line_time_in_us

        # PR ALPM vblank time
        pr_alpm_vblank_time = 0
        if adapter.name not in common.PRE_GEN_15_PLATFORMS:
            pr_alpm_vblank_time = pr_ctl.pr_enable * alpm_ctl.aux_less_wake_time * line_time_in_us

        first_scaler_time = 0
        second_scaler_time = 0
        s1_hor_downscale = 1.0
        s1_ver_downscale = 1.0
        s2_hor_downscale = 1.0
        s2_ver_downscale = 1.0
        dsc_pre_fill_time = 0
        downscaling_factor = 1

        pipe_misc_reg = MMIORegister.read("PIPE_MISC_REGISTER", "PIPE_MISC_" + panel.pipe, adapter.name)

        if pipe_misc_reg.yuv420_enable == 1:
            downscaling_factor = 2

        # Calculation logic for Pipe Scaler and DSC
        # As the driver programming for W2 happens during modeset, it always considers all scalers to be enabled
        # As we would not apply any scaling in native mode, horizontal and vertical downscale amounts can always be considered as 1

        # Time for first scaler in pipeline  = first scaler enable * 4 * line time
        first_scaler_time = 4 * line_time_in_ns

        # Pipe scaler pre-fill time = Time for second scaler in pipeline = second scaler enable * 4 * line time *
        # first scaler vertical downscale amount * first scaler horizontal downscale amount
        second_scaler_time = 4 * line_time_in_ns * s1_hor_downscale * s1_ver_downscale
    
        # Time for first scaler in pipeline + Time for second scaler in pipeline
        pipe_scaler_prefill_time = first_scaler_time + second_scaler_time

        dsc_ctl_reg_module = importlib.import_module(f"registers.{platform}.PIPE_DSS_CTL2_REGISTER")
        dsc_ctl_reg = MMIORegister.read('PIPE_DSS_CTL2_REGISTER', "PIPE_DSS_CTL2_P" + panel.pipe, adapter.name)

        # DSC pre-fill time = DSC enable * 1.5 * line time * first scaler vertical downscale amount * first scaler horizontal downscale amount *
        # second scaler vertical downscale amount * second scaler horizontal downscale amount
        if panel.vdsc_caps.is_vdsc_supported and dsc_ctl_reg.left_branch_vdsc_enable == dsc_ctl_reg_module.__getattribute__('left_branch_vdsc_enable_ENABLE'):
            dsc_pre_fill_time = 1.5 * line_time_in_ns * s1_ver_downscale * s1_hor_downscale * s2_ver_downscale * s2_hor_downscale * downscaling_factor

        dsc_pre_fill_time = dsc_pre_fill_time * 0.001
        pipe_scaler_prefill_time = pipe_scaler_prefill_time * 0.001
        watermark_0_prefill_time = watermark_0_prefill_time * 0.001

        # SDP vblank time = MAX(PPS enable * 7, GMP = GMP enable * 8, VSC_EXT enable * 10) * line time
        sdp_vblank_time = max((vid_dip_ctl.vdip_enable_pps * self.VBLANK_REQUIREMENT_PPS_SDP_IN_LINES),
                              (vid_dip_ctl.vdip_enable_gmp * self.VBLANK_REQUIREMENT_GMP_SDP_IN_LINES),
                              (vsc_ext_sdp_ctl.vsc_extension_sdp_metadata_enable * self.VBLANK_REQUIREMENT_VSC_EXT_SDP_IN_LINES)) * line_time_in_us

        # Calculate Minimum Required VBlank to drive the resolution based on the above parameters
        min_required_vblank = max(frame_start_delay_in_us + watermark_0_prefill_time + pipe_scaler_prefill_time + dsc_pre_fill_time, psr2_vblank_time, pr_alpm_vblank_time, sdp_vblank_time)

        return min_required_vblank, vblank_time_in_us, line_time_in_us
    

    ##
    # @brief        This API verifies Set Context Latency programming
    # @param[in]    adapter             Adapter         object
    # @param[in]    panel               Panel           object
    # @param[in]    mode                Current mode    object
    # @param[in]    available_vblank    Available VBlank of current mode
    # @param[in]    min_req_vblank      Minimum required vblank of current mode
    # @param[in]    line_time_in_us     Line time of the current mode in us
    # @return       True                SCL verification successful
    #               False               SCL verification failed
    #               None                SCL verification is not possible
    def verify_set_context_latency(self, adapter, panel, mode, available_vblank, min_req_vblank, line_time_in_us):
        set_context_latency_reg = MMIORegister.read('TRANS_SET_CONTEXT_LATENCY_REGISTER', 'TRANS_SET_CONTEXT_LATENCY_' + panel.transcoder, 
                                                                    adapter.name, gfx_index=adapter.gfx_index)
        # Verification logic :-
        # If available VBlank of the panel < 5000us, W2 should be programmed to 1 line time
        # If available VBlank of the panel >= 5000us, W2 should be - Total available VBlank - Minimumj required VBlank(Considering different requirements)
        expected_w2_size_in_lines = 0
        unused_vblank_size = available_vblank - min_req_vblank
        logging.info(f"Unused VBlank Size :- {round(unused_vblank_size, 3)}")

        # Check Delayed VBlank support - Delayed VBlank shouldnt be disabled
        is_delayed_vblank_supported = psr.is_delayed_vblank_supported(adapter, panel)
        if not is_delayed_vblank_supported:
            logging.info(f"Pipe-{panel.pipe} does not support delayed VBlank. W2 is not possible on this Pipe")
            return None

        # Verify W2 programming
        actual_w2_size_in_lines = set_context_latency_reg.context_latency
        actual_w2_size_in_us = round(actual_w2_size_in_lines * line_time_in_us, 3)

        if available_vblank < self.W2_VBLANK_SIZE_THRESHOLD_IN_US:
            expected_w2_size_in_lines = 1
        else:
            expected_w2_size_in_lines = unused_vblank_size / line_time_in_us

        if actual_w2_size_in_lines != expected_w2_size_in_lines:
            gdhm.report_driver_bug_pc(f"[PowerCons][W2] W2 was incorrectly programmed. W2 size - {actual_w2_size_in_us}us [{actual_w2_size_in_lines} lines")
            logging.error(f"FAIL : W2 was incorrectly programmed. W2 size - {actual_w2_size_in_us}us [{actual_w2_size_in_lines} lines")
            return False
        logging.info(f"PASS : W2 has been programmed as expected. W2 size - {actual_w2_size_in_us}us [{actual_w2_size_in_lines} lines]")
        return True

    

if __name__ == '__main__':
    TestEnvironment.initialize()
    suite = unittest.TestLoader().loadTestsFromTestCase(W2Basic)
    result = unittest.TextTestRunner().run(suite)
    TestEnvironment.cleanup(result)
