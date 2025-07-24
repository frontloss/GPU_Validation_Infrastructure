########################################################################################################################
# @file         dsb_verification.py
# @brief
# <b> Test Name: DsbVerification </b> <br>
# @ref          dsb_verification.py
# <ul>
# <li> <b> Description: </b> <br>
# Verify batch MMIO update through DSB on single/multiple pipe(s) in different scenarios
# (selection type/trigger mode/sync type etc.) based on the dsb_test_config.xml.
# </li>
# <li> <b> H/W Planning Config : </b> <br>
# <ul>
# <li> DSB supported HW platform (i.e GEN12 platform)
# </li>
# </ul>
# </li>
# <li> <b> Execution Command : </b> <br>
# <ul>
# <li> dsb_verification.py -test -config <SINGLE/CLONE/EXTENDED> -test "<test_config name from XML>" </li>
# </ul>
# </li>
# <li> <b> Test Failure Case(s) : </b> <br>
# <ul>
# <li> Failed to trigger and verify MMIO write using DSB.
# </li>
# <li> Pipe under-run during test execution
# </li>
# </ul>
# </li>
# </ul>
# @author       Amit Sau, Suraj Gaikwad
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Libs.Feature import dsb as dsb_feature
from Tests.DSB.dsb_base import DsbBase, dsb_pipe_dict, dsb_mmio_range

##
# @brief        DsbVerification
class DsbVerification(DsbBase):
    dsb_buffer = dsb_feature.SIMDRV_DSB_BUFFER()

    ##
    # @brief        Test run
    # @return       None
    def runTest(self):
        if self.cmd_line_param['SINGLE_TRIGGER'] != 'NONE':
            # save index register
            for pipe in self.display_port_pipe_mapping.keys():
                self.configure_index_register(pipe, is_save=True)

            self.trigger_dsb_on_all_pipe()

            # restore index register
            for pipe in self.display_port_pipe_mapping.keys():
                self.configure_index_register(pipe, is_save=False)

        else:
            for pipe in self.display_port_pipe_mapping.keys():
                self.configure_index_register(pipe, is_save=True)
                self.trigger_dsb(pipe)
                self.configure_index_register(pipe, is_save=False)

        # Verify Under-run
        self.verify_underrun()

    ##
    # @brief        trigger dsb buffer on all pipe together
    # @return       None
    def trigger_dsb_on_all_pipe(self):
        num_dsb_buffer = 0
        for pipe in self.display_port_pipe_mapping.keys():
            dsb_buffer_args = self.get_dsb_buffer(pipe)
            self.dsb_buffer.DsbBufferArgs[num_dsb_buffer] = dsb_buffer_args

            # enable auto increment
            if self.dsb_buffer.DsbBufferArgs[num_dsb_buffer].IsAutoIncrement is True:
                self.enable_auto_increment(pipe)
            num_dsb_buffer += 1
            self.dsb_buffer.NumDsbBuffer = num_dsb_buffer

        # trigger dsb
        self.dsb.trigger_dsb(self.dsb_buffer)

        # Verify all MMIO update operation through DSB
        time.sleep(1)
        for pipe in self.display_port_pipe_mapping.keys():
            pipe_info = dsb_pipe_dict[pipe]
            for dsb_index in range(0, self.dsb_buffer.NumDsbBuffer):
                dsb_buffer_args = self.dsb_buffer.DsbBufferArgs[dsb_index]
                if dsb_buffer_args.DsbPipeArgs.PipeIndex == pipe_info['PIPE_INDEX']:
                    self.get_dsb_status(pipe)
                    if self.dsb.verify_dsb(self.dsb_buffer.DsbBufferArgs[dsb_index], pipe_info['MODE'], pipe) is False:
                        self.fail_count += 1

    ##
    # @brief        trigger DSB buffer on single pipe
    # @param[in]    pipe - DSB Trigger pipe
    # @return       None
    def trigger_dsb(self, pipe):
        test_config = self.dsb_test_config[pipe]

        dsb_buffer_pipe_args = self.get_dsb_buffer(pipe)
        if 'contiguous_dsb_trigger' in test_config.keys():
            self.dsb_buffer = self.get_dsb_buffer_contiguous_trigger(dsb_buffer_pipe_args, pipe)
        else:
            self.dsb_buffer.DsbBufferArgs[0] = dsb_buffer_pipe_args
            self.dsb_buffer.NumDsbBuffer = 1

        # enable auto increment
        for dsb_index in range(0, self.dsb_buffer.NumDsbBuffer):
            if self.dsb_buffer.DsbBufferArgs[dsb_index].IsAutoIncrement is True:
                self.enable_auto_increment(pipe)

        # trigger dsb
        self.dsb.trigger_dsb(self.dsb_buffer)

        # verify dsb
        time.sleep(1)
        pipe_info = dsb_pipe_dict[pipe]
        for dsb_index in range(0, self.dsb_buffer.NumDsbBuffer):
            self.get_dsb_status(pipe)
            if self.dsb.verify_dsb(self.dsb_buffer.DsbBufferArgs[dsb_index], pipe_info['MODE'], pipe) is False:
                self.fail_count += 1

    ##
    # @brief        enable auto increment
    # @param[in]    pipe - Auto increment Enable Pipe
    # @return       None
    def enable_auto_increment(self, pipe):
        pipe_info = dsb_pipe_dict[pipe]
        index_register = pipe_info['INDEX_REG_OFFSET']
        reg_value = self.driver_interface_.mmio_read(index_register, 'gfx_0')
        if pipe_info['MODE'] == '3D_LUT':
            auto_mode_value = (reg_value | 0x2000)
            logging.info('Enable auto increment %s %s INDEX_REG %s Bit13:1' %
                         (pipe, pipe_info['MODE'], hex(reg_value).upper()))
        elif pipe_info['MODE'] == 'GAMMA':
            logging.info('Enable auto increment %s %s INDEX_REG %s Bit15:1' %
                         (pipe, pipe_info['MODE'], hex(reg_value).upper()))
            auto_mode_value = (reg_value | 0x8000)
        else:
            gdhm.report_bug(
                title="[DSB] Invalid mode provided for triggering DSB. Expected 3D_LUT or GAMMA",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3)
            self.fail('Invalid mode !! Expected 3D_LUT or GAMMA register')
        self.driver_interface_.mmio_write(index_register, auto_mode_value, 'gfx_0')

    ##
    # @brief        get dsb buffer
    # @param[in]    pipe - Get DSB Buffer Pipe
    # @return       dsb_buffer_args - DSB Buffer Array
    def get_dsb_buffer(self, pipe):
        dsb_buffer_args = dsb_feature.SIMDRV_DSB_BUFFER_ARGS()
        dsb_pipe_args = dsb_feature.SIMDRV_DSB_PIPE_ARGS()
        poll_args = dsb_feature.SIMDRV_DSB_POLL_ARGS()
        sync_data = 0

        # get current resolution
        target_id = self.display_config.get_target_id(self.display_port_pipe_mapping[pipe], self.enumerated_displays)
        current_mode = self.display_config.get_current_mode(target_id)

        test_config = self.dsb_test_config[pipe]

        mmio_range = dsb_mmio_range[dsb_feature.SimDrvDsbSelector(test_config['dsb_selector']).name]

        # get mmio range for dsb sync type
        sync_type = dsb_feature.SimDrvDsbSyncType(test_config['dsb_sync_type'])

        if sync_type == dsb_feature.SimDrvDsbSyncType.WAIT_FOR_SCANLINES:
            scanline = current_mode.VtRes // 2
            mmio_range = scanline if scanline < mmio_range else mmio_range
            sync_data = mmio_range

        elif sync_type == dsb_feature.SimDrvDsbSyncType.WAIT_FOR_POLL_REG:
            scanline = current_mode.VtRes // 2
            mmio_range = scanline if scanline < mmio_range else mmio_range
            poll_args.PollOffset = dsb_pipe_dict[pipe]['PIPE_SCANLINE_OFFSET']
            poll_args.PollValue = mmio_range
            sync_data = poll_args.PollValue

        elif sync_type == dsb_feature.SimDrvDsbSyncType.WAIT_FOR_U_SEC:
            mmio_range = dsb_mmio_range[dsb_feature.SimDrvDsbSelector(test_config['dsb_selector']).name]
            sync_data = test_config['wait_time']

        else:
            mmio_range = dsb_mmio_range[dsb_feature.SimDrvDsbSelector(test_config['dsb_selector']).name]

        dsb_offset_data_pair = (dsb_feature.SIMDRV_DSB_OFFSET_DATA_PAIR * mmio_range)()

        # Create DSB buffer data pair
        for data_pair in range(mmio_range):
            dsb_offset_data_pair[data_pair].Offset = dsb_pipe_dict[pipe]['DATA_REG_OFFSET']
            dsb_offset_data_pair[data_pair].Data = data_pair

        # Fill the DSB buffer pipe args
        dsb_pipe_args.PipeIndex = dsb_pipe_dict[pipe]['PIPE_INDEX']
        dsb_pipe_args.IndexRegister = dsb_pipe_dict[pipe]['INDEX_REG_OFFSET']
        dsb_pipe_args.IndexRegStartOffset = 0
        dsb_pipe_args.pOffsetDataPair = dsb_offset_data_pair
        dsb_pipe_args.DataCount = mmio_range
        dsb_pipe_args.ScanlineCountOffset = dsb_pipe_dict[pipe]['PIPE_SCANLINE_OFFSET']
        dsb_pipe_args.FrameCountOffset = dsb_pipe_dict[pipe]['PIPE_FRMCNT_OFFSET']
        dsb_pipe_args.DeltaFrameCount = test_config['delta_frame_count']

        # Fill the DSB buffer args
        dsb_buffer_args.DsbPipeArgs = dsb_pipe_args
        dsb_buffer_args.DsbSelectionType = test_config['dsb_selector']
        dsb_buffer_args.DsbTriggerMode = test_config['dsb_trigger_mode']
        dsb_buffer_args.DsbSyncType = test_config['dsb_sync_type']
        dsb_buffer_args.DsbSyncData = sync_data
        dsb_buffer_args.DsbPollArgs = poll_args
        dsb_buffer_args.IsAutoIncrement = test_config['auto_increment']
        dsb_buffer_args.InterruptOnCompletion = test_config['interrupt_on_completion']
        dsb_buffer_args.Delay = test_config['delay_in_verification']
        dsb_buffer_args.Status = dsb_feature.SimDrvDsbErrorCode.ERROR_UNDEFINED

        return dsb_buffer_args

    ##
    # @brief        get dsb buffer for contiguous trigger
    # @param[in]    dsb_buffer_args - DSB Buffer Array
    # @param[in]    pipe - Auto increment Pipe Enable
    # @return       dsb_buffer - DSB Buffer Value
    def get_dsb_buffer_contiguous_trigger(self, dsb_buffer_args, pipe):
        dsb_buffer = dsb_feature.SIMDRV_DSB_BUFFER()
        test_config = self.dsb_test_config[pipe]
        index_reg_start_offset = 0
        dsb_buffer_index = 0
        no_of_trigger = test_config['no_of_trigger']
        no_of_element = 0
        remaining_element = dsb_buffer_args.DsbPipeArgs.DataCount

        dsb_buffer.NumDsbBuffer = no_of_trigger
        temp = dsb_buffer_args

        while no_of_trigger > 0:
            temp.DsbPipeArgs.IndexRegStartOffset = index_reg_start_offset
            no_of_element = remaining_element // no_of_trigger
            remaining_element = remaining_element - no_of_element
            dsb_offset_data_pair = (dsb_feature.SIMDRV_DSB_OFFSET_DATA_PAIR * no_of_element)()

            for data_pair in range(no_of_element):
                dsb_offset_data_pair[data_pair].Offset = dsb_pipe_dict[pipe]['DATA_REG_OFFSET']
                dsb_offset_data_pair[data_pair].Data = index_reg_start_offset
                index_reg_start_offset += 1

            temp.DsbPipeArgs.DataCount = no_of_element
            temp.DsbSelectionType = dsb_buffer_index  # change DSB selector type enum value to 0,1,2 ..
            dsb_buffer.DsbBufferArgs[dsb_buffer_index] = temp
            dsb_buffer.DsbBufferArgs[dsb_buffer_index].DsbPipeArgs.pOffsetDataPair = dsb_offset_data_pair
            dsb_buffer_index += 1
            no_of_trigger -= 1
        return dsb_buffer

    ##
    # @brief        dump all dsb control register status
    # @param[in]    pipe - Get DSB Status Pipe
    # @return       None
    def get_dsb_status(self, pipe):
        dsb_ctrl_registers = dsb_feature.dsb_ctrl_reg[pipe]
        logging.debug('%s DSB CTRL register status are as follows' % pipe)
        index = 0
        for ctrl_reg in dsb_ctrl_registers:
            value = self.driver_interface_.mmio_read(ctrl_reg, 'gfx_0')
            logging.debug('DSB_CTRL_%s_%s %s = %s' % (index, pipe[5:], hex(ctrl_reg).upper(), hex(value).upper()))
            index += 1


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
