######################################################################################################
# @file         concurrency_utility.py
# @brief        Contains all the helper functions and the utilities used by Concurrency Tests
#               Functions present in this wrapper :
#               1.verify_psr()
#               2.verify_pipe_scaler()
# @author       Smitha B, Vimalesh D
######################################################################################################
import logging
import time
import DisplayRegs
from DisplayRegs.DisplayArgs import TranscoderType, PipeType
from DisplayRegs.DisplayOffsets import ScalerOffsetsValues, PsrOffsetValues, DpstOffsetValues
from Tests.Color.Common import color_mmio_interface
from Libs.Core.logger import gdhm

mmio_interface = color_mmio_interface.ColorMmioInterface()


def verify_pipe_scaler(gfx_index: str, platform: str, plane: str, pipe: str):

    regs = DisplayRegs.get_interface(platform, gfx_index)
    ps_ctl_offsets = regs.get_scaler_offsets(plane,pipe)
    ps1_offsets_value = mmio_interface.read(gfx_index,ps_ctl_offsets.scaler_offset_1)
    ps2_offsets_value = mmio_interface.read(gfx_index, ps_ctl_offsets.scaler_offset_2)
    ps_1_status = regs.get_scaler_info(plane,pipe,ScalerOffsetsValues(scaler_offset_1=ps1_offsets_value))
    ps_2_status = regs.get_scaler_info(plane,pipe,ScalerOffsetsValues(scaler_offset_2=ps2_offsets_value))
    if ps_1_status.scaler_1_enable:
        if ps_1_status.scaler_1_binding == 0:
            logging.info("Scaler Expected: Enable and Actual: Enable")
            return True
        else:
            gdhm.report_driver_bug_os("[{0}] Scaler Binding Expected: Enable and Actual: {1} for Adapter: {2}"
                                        .format(platform, ps_1_status.scaler_1_binding, gfx_index))
    elif ps_2_status.scaler_2_enable:
        if ps_2_status.scaler_2_binding == 0:
            logging.info("Scaler Expected: Enable and Actual: Enable")
            return True
        else:
            gdhm.report_driver_bug_os("[{0}] Scaler Binding Expected: Enable and Actual: {1} for Adapter: {2}"
                                        .format(platform, ps_1_status.scaler_2_binding, gfx_index))
    logging.debug("Scaler 1 Enable status:{0}".format(ps_1_status.scaler_1_enable))
    logging.debug("Scaler 2 Enable status:{0}".format(ps_1_status.scaler_2_enable))
    logging.debug("Scaler 1 Bind with plane:{0}".format(ps_1_status.scaler_1_binding))
    logging.debug("Scaler 2 Bind with plane:{0}".format(ps_1_status.scaler_2_binding))
    logging.error("Scaler Expected: Enable and Actual: Disabled")
    return False


# @brief verify_psr
# @param[in]   gfx_index - str
# @param[in]   platform - str
# @param[in]   port - str
# @param[in]   transcoder - TranscoderType
# @param[in]   is_psr2 - bool
# @return      is_psr_enabled - bool
# @brief
# @param[in] -  gfx_index
# @param[in] -  delay - default is 0;
def verify_psr(gfx_index: str, platform: str, port: str, pipe: str, transcoder: TranscoderType, is_psr2, expected_status:bool) -> bool:
    regs = DisplayRegs.get_interface(platform, gfx_index)
    psr_offset = regs.get_psr_offsets(TranscoderType(transcoder))
    psr_ctl_offset = psr_offset.Psr2CtrlReg if is_psr2 else psr_offset.SrdCtlReg
    psr_ctl_value = mmio_interface.read(gfx_index, psr_ctl_offset)

    if is_psr2:
        psr_info = regs.get_psr_info(TranscoderType(transcoder), PsrOffsetValues(Psr2CtrlReg=psr_ctl_value))
        if psr_info.Psr2Enable is expected_status:
            logging.info("PASS: PSR2 on Adapter {0} on Port {1} and Pipe {2}, Expected : {4}; Actual : {3}".format(gfx_index, port, pipe,
                                                                                                                   psr_info.Psr2Enable, expected_status))
            return True
    else:
        psr_info = regs.get_psr_info(TranscoderType(transcoder), PsrOffsetValues(SrdCtlReg=psr_ctl_value))
        if psr_info.SrdEnable is expected_status:
            logging.info("PASS: PSR1  on Adapter {0} on Port {1} and Pipe {2} Expected : {4}; Actual : {3}".format(gfx_index, port, pipe,
                                                                                                                   psr_info.SrdEnable, expected_status))
            return True
    logging.error("PSR Status not matches with Expected: {0}".format(expected_status))
    return False


def verify_dpst(gfx_index: str, platform: str, port: str, pipe: str):
    regs = DisplayRegs.get_interface(platform, gfx_index)
    dpst_offsets = regs.get_dpst_offsets(getattr(PipeType, f'PIPE_{pipe}'))
    dpst_offsets_value = mmio_interface.read(gfx_index,dpst_offsets.DpstControl)

    status = False
    dpst_histogram_status = regs.get_dpst_info(getattr(PipeType, f'PIPE_{pipe}'),DpstOffsetValues(DpstControl=dpst_offsets_value))

    if dpst_histogram_status.IEHistogramEnable == 1:
        logging.info("IEHistogram expected:Enable and actual:Enable")
        for i in range(0,3):
            dpst_guard_value = mmio_interface.read(gfx_index, dpst_offsets.DpstGuard)

            dpst_guard_status = regs.get_dpst_info(getattr(PipeType, f'PIPE_{pipe}'), DpstOffsetValues(DpstGuard=dpst_guard_value))
            if dpst_guard_status.HistogramEventStatus:
                logging.info("DPST HistogramInterruptEnable expected:Enable and actual:Enable")
                status = True
                return status
            else:
                logging.error("Trial - {0}: Ignoring if event status is not set".format(i))
    else:
        logging.info("IEHistogram expected:Enable and actual:Disable")
        logging.error("dpst_histogram_status disabled")
        gdhm.report_driver_bug_os("[{0}] IEHistogram for Adapter: {1} Pipe: {2} Expected:Enable and Actual:Disable".format(platform,gfx_index,pipe))

    return status
