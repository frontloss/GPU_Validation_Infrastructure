######################################################################################
# @file         mulitchip_genlock_verify_report_status.py
# @brief        These tests verifies if VBlank TS for each target are closer to same.
# @details      Its run either with multiple displays on single DUT or displays across multiple DUTs.
# Sample cmdline for genlock on single system:
# multichip_genlock_verify_escape.py -dp_b -dp_c -master_dut true -master_display dp_c
#
# @author       Goutham N
######################################################################################

import logging
import sys
import unittest
from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import driver_escape
from Libs.Core.logger import gdhm
from Libs.Core.display_config import display_config_enums as cfg_enum
import Libs.Feature.display_engine.de_base.display_base as display_base
import Tests.Multichip_Genlock.multichip_genlock_base as multichip_genlock_base
from DisplayRegs import DisplayArgs


##
# @brief Class for Multichip Genlock test that verifies if vblank TS of all the displays in Genlock are close same via escape call
class MultichipGenlockVerifyReportStatusEscape(multichip_genlock_base.MultichipGenlockBase):
    ##
    # @brief Test to enable genlock and verify the registers and check if all the displays are in sync
    # @return None
    def runTest(self):
        # Ensure all genlock displays are active.
        adapter_list = ['gfx_0'] * len(self.display_list)
        self.set_and_validate_config(enum.EXTENDED if len(self.display_list) > 1 else enum.SINGLE,
                                     self.display_list, adapter_list)

        logging.info('-----------Before enabling genlock, register values are:-----------')
        self.print_verify_genlock_registers(self.display_list, verify_prog=False)

        # Fill genlock args. Apply SD config with LFP or a slave display; this is required to do SD config with
        # master display post enabling genlock.
        self.genlock_args = self.fill_genlock_args(self.display_list)
        if self.lfp_display is not None:
            self.set_and_validate_config(enum.SINGLE, [self.lfp_display], adapter_list)
        elif len(self.slave_disp_list) > 0:
            self.set_and_validate_config(enum.SINGLE, [self.slave_disp_list[0]], adapter_list)

        # Enable genlock
        enumerated_displays = self.disp_config.get_enumerated_display_info()
        target_id = self.disp_config.get_target_id(self.display_list[0], enumerated_displays)
        display_and_adapter_info = self.disp_config.get_display_and_adapter_info(target_id)
        if driver_escape.get_set_genlock(display_and_adapter_info, True, self.genlock_args):
            logging.info(f'Enable genlock successful on {display_and_adapter_info.adapterInfo.gfxIndex}')
        else:
            logging.error(f'Enable genlock failed on {display_and_adapter_info.adapterInfo.gfxIndex}')
            gdhm.report_test_bug_di(title='[Test Issue]: Enable genlock call failed')
            self.fail('Enable genlock call failed')

        # Do display switching so as to do modeset on all displays after genlock is enabled.
        # Post enabling genlock, first modeset should be of master.
        if self.master_display is not None:
            self.set_and_validate_config(enum.SINGLE, [self.master_display], adapter_list)
        self.set_and_validate_config(enum.EXTENDED if len(self.display_list) > 1 else enum.SINGLE,
                                     self.display_list, adapter_list)

        # Verify Genlock bits register programming
        logging.info('-----------After enabling genlock and doing modeset on all the genlock displays:-----------')
        if not self.print_verify_genlock_registers(self.display_list):
            gdhm.report_test_bug_di(title='[Test Issue]: Genlock register verification failed.')
            self.fail('Genlock register verification failed.')

        # Verify if vblank timestamp matches for each target
        # Display engine has TIMESTAMP_CTR register which is a free flowing timer in microseconds.
        # Every time VBLANK happens on a pipe, display engine samples current TIMESTAMP_CTR value into PIPE_FRMTMSTMP register.
        # Two things are verified here:
        # 1. VBlankTS for all the displays should be close to same
        # 2. Pipe time stamp should be same as current time stamp for each pipe
        # get_set_genlock_vblank_ts() returns when VBlank has occurred for each target.
        # https://docs.intel.com/documents/GfxSWAT/Display/MultiGPU_Display_Genlock_SAS/MultiGPU_Display_Genlock_SAS/MultiGPU_Display_Genlock_SAS.html#genlock-periodic-checking
        logging.info('-----------Verifying if VBlank timestamp matches for each target :-----------')
        # fill args for getting vblank timestamp for respective target ID
        self.genlock_args_for_vblank_ts = self.fill_genlock_args_for_fetching_vblank_ts(self.display_list)

        # Use first target's VBlank time stamp as reference for comparing
        status, vblank_ts_args = driver_escape.get_set_genlock_vblank_ts(display_and_adapter_info, self.genlock_args_for_vblank_ts)
        if not status:
            logging.error("[Test Issue]: Failed to invoke get_vblank_ts escape call")
            gdhm.report_test_bug_di(title='[Test Issue]: Failed to invoke get_vblank_ts escape call')
            self.fail()

        ref_vblank_ts = vblank_ts_args.VblankTS
        for display in range(len(self.display_list)):
            display_info = enumerated_displays.ConnectedDisplays[display]
            display_and_adapter_info = display_info.DisplayAndAdapterInfo
            display_port = cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name

            status, vblank_ts_args = driver_escape.get_set_genlock_vblank_ts(display_and_adapter_info, self.genlock_args_for_vblank_ts)
            if status is True:
                display_base_obj = display_base.DisplayBase(display_port)
                trans, pipe = display_base_obj.get_transcoder_and_pipe(display_port, self.default_gfx_index)

                current_vblank_ts = vblank_ts_args.VblankTS
                logging.info(f'VBlankTS for target ID {target_id} is {current_vblank_ts} μs')

                timestamp_ctr_value = DisplayArgs.read_register(self.TIMESTAMP_CTR_OFFSET, self.default_gfx_index)
                logging.info(f'Current time stamp value: {timestamp_ctr_value} μs')

                if pipe == 0:
                    pipe_frm_stmp_value = DisplayArgs.read_register(self.PipeFRMTMSTMP.PIPE_0.value,
                                                                     self.default_gfx_index)
                elif pipe == 1:
                    pipe_frm_stmp_value = DisplayArgs.read_register(self.PipeFRMTMSTMP.PIPE_1.value,
                                                                     self.default_gfx_index)
                elif pipe == 2:
                    pipe_frm_stmp_value = DisplayArgs.read_register(self.PipeFRMTMSTMP.PIPE_2.value,
                                                                     self.default_gfx_index)
                elif pipe == 3:
                    pipe_frm_stmp_value = DisplayArgs.read_register(self.PipeFRMTMSTMP.PIPE_3.value,
                                                                     self.default_gfx_index)
                else:
                    logging.error("Invalid Pipe!")
                    gdhm.report_test_bug_di(title='[Test Issue]: Invalid Pipe!')
                    self.fail()

                logging.info(f'Pipe Frame timestamp value for for pipe {pipe}: {pipe_frm_stmp_value} μs')

                # In document, Exact Delta is not mentioned, hence based on testing assuming it 999999 μs
                delta = 999999
                if abs(ref_vblank_ts-current_vblank_ts) > delta or abs(timestamp_ctr_value-pipe_frm_stmp_value) > delta:
                    logging.error('[Test Issue]: Displays are not in sync!')
                    gdhm.report_test_bug_di(title='[Test Issue]: Displays are not in sync!')
                    self.fail()
                else:
                    continue

            else:
                logging.error('[Test Issue]: Failed to invoke get_vblank_ts escape call')
                gdhm.report_test_bug_di(title='[Test Issue]: Failed to invoke get_vblank_ts escape call')
                self.fail()

        logging.info('[Pass]:VBlankTS verification is completed.')

        # Disable genlock
        self.disable_genlock_and_do_modeset_on_displays()

        logging.info('-----------After disabling genlock, register values are:-----------')
        self.print_verify_genlock_registers(self.display_list, verify_prog=False)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
