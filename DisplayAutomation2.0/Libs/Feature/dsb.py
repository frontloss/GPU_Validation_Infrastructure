########################################################################################################################
# \file
# \addtogroup PyLibs_DSB
# \brief Python wrapper which exposes API's related to Display State Buffer (DSB)
# \remarks
# \ref dsb.py exposes API's which provide information to test writers
# related triggering and verifying dsb. It also defines the enums and structures used by DSB
# below: \n
# <ul>
# <li> @ref verify_dsb      \n \copybrief verify_dsb \n
# </li>
# </ul>
# \author   Amit Sau
########################################################################################################################
import ctypes
import logging
import os
from enum import IntEnum

from Libs.Core.core_base import singleton
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.logger import gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context

MAX_SUPPORTED_PIPE = 4


##
# DSB Selector
class SimDrvDsbSelector(IntEnum):
    NONE = -1
    PIPE = 0
    LACE = 1
    HDR = 2
    MAX = 3


##
# DSB Trigger mode
class SimDrvDsbTriggerMode(IntEnum):
    NONE = 0
    SYNC = 1
    ASYNC = 2
    OVERRIDE = 3
    APEND = 4
    MAX = 5


##
# DSB sync type
class SimDrvDsbSyncType(IntEnum):
    WAIT_FOR_NONE = 0
    WAIT_FOR_VBLANK = 1
    WAIT_FOR_U_SEC = 2
    WAIT_FOR_SCANLINES = 3
    WAIT_FOR_SCANLINE_IN_RANGE = 4
    WAIT_FOR_SCANLINE_OUT_OF_RANGE = 5
    WAIT_FOR_POLL_REG = 6


##
# DSB Error Code
class SimDrvDsbErrorCode(IntEnum):
    SUCCESS = 0
    FAILED = 1
    MEMORY_ALLOCATION_FAILED = 2
    INVALID_MEMORY_ACCESS = 3
    INVALID_PIPE = 4
    TRIGGER_FAILED = 5
    VERIFICATION_FAILED = 6
    VALSIM_INIT_FAILED = 7
    VALSIM_IOCTL_FAILED = 8
    ERROR_UNDEFINED = 9
    ERROR_CODE_MAX = 10


##
# Structure definition for DSB offset data pair
class SIMDRV_DSB_OFFSET_DATA_PAIR(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('Offset', ctypes.c_ulong),
                ('Data', ctypes.c_ulong)]


##
# Structure definition for DSB write with contiguous polling
class SIMDRV_DSB_POLL_ARGS(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('PollOffset', ctypes.c_ulong),
                ('PollValue', ctypes.c_ulong),
                ('PollMask', ctypes.c_ulong)]


##
# Structure definition for DSB Pipe Args
class SIMDRV_DSB_PIPE_ARGS(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('PipeIndex', ctypes.c_ulong),
                ('IndexRegister', ctypes.c_ulong),
                ('IndexRegStartOffset', ctypes.c_ulong),
                ('pOffsetDataPair', ctypes.POINTER(SIMDRV_DSB_OFFSET_DATA_PAIR)),
                ('DataCount', ctypes.c_ulong),
                ('ScanlineCountOffset', ctypes.c_ulong),
                ('FrameCountOffset', ctypes.c_ulong),
                ('DeltaFrameCount', ctypes.c_ulong)]


##
# Structure definition for DSB buffer args
class SIMDRV_DSB_BUFFER_ARGS(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('DsbPipeArgs', SIMDRV_DSB_PIPE_ARGS),
                ('DsbSelectionType', ctypes.c_int),
                ('DsbTriggerMode', ctypes.c_int),
                ('DsbSyncType', ctypes.c_int),
                ('DsbSyncData', ctypes.c_ulong),
                ('DsbPollArgs', SIMDRV_DSB_POLL_ARGS),
                ('IsAutoIncrement', ctypes.c_bool),
                ('InterruptOnCompletion', ctypes.c_bool),
                ('Delay', ctypes.c_ulong),
                ('Status', ctypes.c_int)]


##
# Structure definition for DSB buffer args
class SIMDRV_DSB_BUFFER(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('DsbBufferArgs', SIMDRV_DSB_BUFFER_ARGS * MAX_SUPPORTED_PIPE),
                ('NumDsbBuffer', ctypes.c_ulong)]


pipe_index_mapping = {0: 'PIPE_A', 1: 'PIPE_B', 2: 'PIPE_C', 3: 'PIPE_D'}

dsb_ctrl_reg = {
    'PIPE_A': [0x70B08, 0x70C08, 0x70D08],
    'PIPE_B': [0x71B08, 0x71C08, 0x71D08],
    'PIPE_C': [0x72B08, 0x72C08, 0x72D08],
    'PIPE_D': [0x73B08, 0x73C08, 0x73D08]
}


##
# SystemUtility Class
@singleton
class DisplayStateBuffer(object):
    def __init__(self):
        # Load Gfx Val Sim library.
        self.gfxValSim = ctypes.cdll.LoadLibrary(os.path.join(test_context.TestContext.bin_store(), 'GfxValSim.dll'))
        self.driver_interface_ = driver_interface.DriverInterface()

    ##
    # @brief API to Trigger batch MMIO write through DSB
    # @param[in] dsb_buffer_args object of the type SIMDRV_DSB_BUFFER_ARGS
    # @param[in] gfx index
    # @return - BOOL.
    def trigger_dsb(self, dsb_buffer, gfx_index='gfx_0'):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        prototype = ctypes.PYFUNCTYPE(ctypes.c_int, ctypes.POINTER(GfxAdapterInfo), ctypes.c_uint,
                                      ctypes.POINTER(SIMDRV_DSB_BUFFER))
        func = prototype(('GfxValSimTriggerDSB', self.gfxValSim))

        for index in range(0, dsb_buffer.NumDsbBuffer):
            buffer = dsb_buffer.DsbBufferArgs[index]

            logging.info("DSB trigger args are as follows:")
            logging.info('[DSB_ARGS] Pipe index = %s & buffer length = %s'
                         % (buffer.DsbPipeArgs.PipeIndex, buffer.DsbPipeArgs.DataCount))
            logging.debug('[DSB_ARGS] Index register: %s & start Offset %s'
                          % (hex(buffer.DsbPipeArgs.IndexRegister).upper(),
                             hex(buffer.DsbPipeArgs.IndexRegStartOffset).upper()))
            logging.info('[DSB_ARGS] Selector = %s, Trigger Mode = %s, Sync Type %s'
                         % (SimDrvDsbSelector(buffer.DsbSelectionType).name,
                            SimDrvDsbTriggerMode(buffer.DsbTriggerMode).name,
                            SimDrvDsbSyncType(buffer.DsbSyncType).name))
            logging.info('[DSB_ARGS] Interrupt on completion = %s & auto increment = %s'
                         % (buffer.InterruptOnCompletion, buffer.IsAutoIncrement))
            logging.info('[DSB_ARGS] Buffer start offset & value pair [%s : %s]'
                         % (hex(buffer.DsbPipeArgs.pOffsetDataPair[0].Offset).upper(),
                            hex(buffer.DsbPipeArgs.pOffsetDataPair[0].Data).upper()))
            logging.info('[DSB_ARGS] Buffer end offset & value pair [%s : %s]'
                         % (hex(buffer.DsbPipeArgs.pOffsetDataPair[buffer.DsbPipeArgs.DataCount - 1].Offset).upper(),
                            hex(buffer.DsbPipeArgs.pOffsetDataPair[buffer.DsbPipeArgs.DataCount - 1].Data).upper()))

        # Trigger DSB
        status = func(ctypes.byref(adapter_info), ctypes.sizeof(GfxAdapterInfo), ctypes.byref(dsb_buffer))
        if status != SimDrvDsbErrorCode.SUCCESS:
            failing_pipes_list = list()
            for index in range(0, dsb_buffer.NumDsbBuffer):
                dsb_buffer_data = dsb_buffer.DsbBufferArgs[index]
                logging.error('Trigger DSB status on %s - %s ' %
                              (pipe_index_mapping[dsb_buffer_data.DsbPipeArgs.PipeIndex],
                               SimDrvDsbErrorCode(dsb_buffer_data.Status).name))
                if dsb_buffer_data.Status != SimDrvDsbErrorCode.SUCCESS:
                    failing_pipes_list.append(pipe_index_mapping[dsb_buffer_data.DsbPipeArgs.PipeIndex])
            gdhm.report_bug(
                title="[DSB] Test failed to trigger DSB on {}".format(','.join(failing_pipes_list)),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2)
            return False
        else:
            logging.info('Trigger DSB status - %s' % SimDrvDsbErrorCode(status).name)
            return True

    ##
    # @brief API to verify batch MMIO update through DSB
    # @param[in] dsb_buffer_args object of the type SIMDRV_DSB_BUFFER_ARGS
    # @return - BOOL.
    def verify_dsb(self, dsb_buffer_args, mode, pipe):
        logging.info('Verifying all %s %s DATA_REG programmed through DSB' % (pipe, mode))
        if dsb_buffer_args.IsAutoIncrement is True:
            return self.__verify_buffer_auto_inc(dsb_buffer_args, mode, pipe)
        else:
            return self.__verify_buffer_non_auto_inc(dsb_buffer_args)

    ##
    # @brief API to verify batch MMIO update through DSB with auto inc mode
    # @param[in] dsb_buffer_args object of the type SIMDRV_DSB_BUFFER_ARGS
    # @return - BOOL.
    def __verify_buffer_auto_inc(self, dsb_buffer_args, mode, pipe):
        status = False
        mismatch_elements = []

        # Set start index of Auto increment register
        self.driver_interface_.mmio_write(dsb_buffer_args.DsbPipeArgs.IndexRegister,
                                  dsb_buffer_args.DsbPipeArgs.IndexRegStartOffset, 'gfx_0')
        reg_value = self.driver_interface_.mmio_read(dsb_buffer_args.DsbPipeArgs.IndexRegister, 'gfx_0')

        # enable auto increment
        if mode == '3D_LUT':
            auto_mode_value = (reg_value | 0x2000)
            logging.info('Enable auto increment %s %s INDEX_REG %s Bit13:1' % (pipe, mode, hex(reg_value).upper()))
        elif mode == 'GAMMA':
            logging.info('Enable auto increment %s %s INDEX_REG %s Bit15:1' % (pipe, mode, hex(reg_value).upper()))
            auto_mode_value = (reg_value | 0x8000)
        else:
            logging.error('Invalid mode !! Expected 3D_LUT or GAMMA register')
            gdhm.report_bug(
                title="[DSB] Invalid mode provided for triggering DSB. Expected 3D_LUT or GAMMA.",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3)
            return status

        self.driver_interface_.mmio_write(dsb_buffer_args.DsbPipeArgs.IndexRegister, auto_mode_value, 'gfx_0')

        # verify all dsb buffer through MMIO read.
        offset = dsb_buffer_args.DsbPipeArgs.pOffsetDataPair[0].Offset
        for data_index in range(dsb_buffer_args.DsbPipeArgs.DataCount):
            expected_value = dsb_buffer_args.DsbPipeArgs.pOffsetDataPair[data_index].Data
            reg_value = self.driver_interface_.mmio_read(offset, 'gfx_0')
            if expected_value != reg_value:
                mismatch_elements.append(hex(expected_value))

        if len(mismatch_elements) == 0:
            logging.info('[PASS] All %s %s DATA_REG %s programmed through DSB' % (pipe, mode, hex(offset).upper()))
            status = True
        else:
            size = 15  # In log file every line should have max 15 element
            splitted_list = [mismatch_elements[i:i + size] for i in range(0, len(mismatch_elements), size)]
            logging.error('[FAIL] All %s %s DATA_REG %s not programmed through DSB' % (pipe, mode, hex(offset).upper()))
            gdhm.report_bug(
                title="[DSB] All {} {} DATA_REG {} not programmed through DSB".format(pipe, mode, hex(offset).upper()),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2)
            logging.debug('Non-programmed data through DSB are as follows:')
            for data_list in splitted_list:
                logging.debug('%s' % data_list)

        # disable auto increment
        if mode == '3D_LUT':
            auto_mode_value = (reg_value & (~0x2000))
            logging.info('Disable auto increment %s %s INDEX_REG %s Bit13:0' % (pipe, mode, hex(reg_value).upper()))
        elif mode == 'GAMMA':
            auto_mode_value = (reg_value & (~0x8000))
            logging.info('Disable auto increment %s %s INDEX_REG %s Bit15:0' % (pipe, mode, hex(reg_value).upper()))
        self.driver_interface_.mmio_write(dsb_buffer_args.DsbPipeArgs.IndexRegister, auto_mode_value, 'gfx_0')
        return status

    ##
    # @brief API to verify batch MMIO update through DSB with non auto increment mode
    # @param[in] dsb_buffer_args object of the type SIMDRV_DSB_BUFFER_ARGS
    # @return - BOOL.
    def __verify_buffer_non_auto_inc(self, dsb_buffer_args):
        last_index = dsb_buffer_args.DsbPipeArgs.DataCount - 1
        offset = dsb_buffer_args.DsbPipeArgs.pOffsetDataPair[last_index].Offset
        expected_value = dsb_buffer_args.DsbPipeArgs.pOffsetDataPair[last_index].Data
        reg_value = self.driver_interface_.mmio_read(offset, 'gfx_0')
        if expected_value == reg_value:
            logging.info('[PASS] Expected offset value pair = [%s : %s] Actual offset value pair = [%s : %s]'
                         % (hex(offset).upper(), hex(expected_value).upper(),
                            hex(offset).upper(), hex(reg_value).upper()))
            return True
        else:
            logging.error('[FAIL] Expected offset value pair = [%s : %s] Actual offset value pair = [%s : %s]'
                          % (hex(offset).upper(), hex(expected_value).upper(),
                             hex(offset).upper(), hex(reg_value).upper()))
            gdhm.report_bug(
                title="[DSB] Mismatch in DSB data offset-value pair. Expected = [{}:{}] Actual = [{}:{}]"
                    .format(hex(offset).upper(), hex(expected_value).upper(), hex(offset).upper(),
                            hex(reg_value).upper()),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2)
            return False
