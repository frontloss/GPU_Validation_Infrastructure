########################################################################################################################
# @file         DisplayRegsInterface.py
# @brief        Abstract class for DisplayRegs service implemented by each Gen separately.
#
# @author       Rohit Kumar
########################################################################################################################

import abc

from DisplayRegs.DisplayArgs import *
from DisplayRegs.DisplayOffsets import *


class DisplayRegsService(abc.ABC):

    def __init__(self, platform: str, gfx_index: str):
        self.platform: str = platform
        self.gfx_index: str = gfx_index

    ####################################################################################################################
    # Methods to get register offsets (required in ETL based verification)
    ####################################################################################################################

    @abc.abstractmethod
    def get_timing_offsets(self, transcoder: TranscoderType) -> TimingOffsets:
        pass

    @abc.abstractmethod
    def get_vrr_offsets(self, transcoder: TranscoderType) -> VrrOffsets:
        pass

    @abc.abstractmethod
    def get_emp_offsets(self, transcoder: TranscoderType) -> EmpOffsets:
        pass

    @abc.abstractmethod
    def get_trans_ddi_ctl2_offsets(self, transcoder: str) -> TransDDiCtl2Offsets:
        pass

    @abc.abstractmethod
    def get_dpst_offsets(self, pipe: PipeType) -> DpstOffsets:
        pass

    @abc.abstractmethod
    def get_psr_offsets(self, transcoder: TranscoderType) -> PsrOffsets:
        pass

    @abc.abstractmethod
    def get_3dlut_offsets(self, pipe: str) -> Hw3dLutOffsets:
        pass

    @abc.abstractmethod
    def get_lace_offsets(self, pipe: str) -> LaceOffsets:
        pass

    @abc.abstractmethod
    def get_color_ctrl_offsets(self, pipe: str) -> ColorCtlOffsets:
        pass

    @abc.abstractmethod
    def get_trans_ddi_offsets(self, transcoder: str) -> TransDDiOffsets:
        pass

    @abc.abstractmethod
    def get_pipe_csc_coeff_offsets(self, pipe: str) -> PipeCscCoeffOffsets:
        pass

    @abc.abstractmethod
    def get_plane_csc_coeff_offsets(self, pipe: str, plane: str) -> PlaneCscCoeffOffsets:
        pass

    @abc.abstractmethod
    def get_plane_color_ctl_offsets(self, plane: str, pipe: str) -> PlaneColorCtlOffsets:
        pass

    @abc.abstractmethod
    def get_plane_gamma_offsets(self, plane: str, pipe: str) -> PlaneGammaOffsets:
        pass

    @abc.abstractmethod
    def get_plane_gamma_enh_offsets(self, plane: str, pipe: str) -> PlaneGammaEnhOffsets:
        pass

    @abc.abstractmethod
    def get_plane_csc_pre_post_offsets(self, pipe: str, plane: str) -> PlaneCscPrePostOffsets:
        pass

    @abc.abstractmethod
    def get_avi_info_offsets(self, plane: str, pipe: str) -> AviInfoOffsets:
        pass

    @abc.abstractmethod
    def get_vsc_sdp_offsets(self, plane: str, pipe: str) -> VscSdpDataOffsets:
        pass

    @abc.abstractmethod
    def get_pipe_gamma_offsets(self, pipe: str) -> PipeGammaOffsets:
        pass

    @abc.abstractmethod
    def get_video_dip_ctl_offset(self, pipe: str) -> VideoDipCtlOffsets:
        pass

    @abc.abstractmethod
    def get_trans_msa_misc_offset(self, pipe: str) -> TransMsaMiscOffsets:
        pass

    @abc.abstractmethod
    def get_pipe_csc_pre_post_offsets(self, pipe: str) -> PipeCscPrePostOffsets:
        pass

    @abc.abstractmethod
    def get_hdr_metadata_offsets(self, plane: str, pipe: str) -> MetadataOffsets:
        pass

    @abc.abstractmethod
    def get_pipe_frame_ctr_offsets(self, pipe: str) -> PipeFrameCtrOffsets:
        pass

    @abc.abstractmethod
    def get_plane_pixel_normalizer_offsets(self, plane: str, pipe: str) -> PlanePixelNormalizerOffsets:
        pass

    @abc.abstractmethod
    def get_plane_ctl_offsets(self, plane: str, pipe: str) -> PlaneCtlOffsets:
        pass

    @abc.abstractmethod
    def get_cmtg_offsets(self, transcoder: TranscoderType) -> CmtgOffsets:
        pass

    @abc.abstractmethod
    def get_scaler_offsets(self, plane: str, pipe: str) -> ScalerOffsets:
        pass

    @abc.abstractmethod
    def get_interrupt_offsets(self) ->InterruptOffsets:
        pass

    @abc.abstractmethod
    def get_dcstate_offsets(self) -> DCStateOffsets:
        pass

    @abc.abstractmethod
    def get_ALPM_offsets(self, pipe:str) -> ALPMOffsets:
        pass
    
    @abc.abstractmethod
    def get_video_dip_pps_offsets(self, pipe: str) -> VideoDataIslandPacketPPSOffsets:
        pass

    @abc.abstractmethod
    def get_dc6v_offsets(self) -> Dc6vOffsets:
        pass

    ####################################################################################################################
    # Methods to get register data
    ####################################################################################################################

    @abc.abstractmethod
    def get_vrr_info(self, transcoder: TranscoderType, data: VrrOffsetValues = None) -> VrrInfo:
        pass

    @abc.abstractmethod
    def get_emp_info(self, transcoder: TranscoderType, data: EmpOffsetValues = None) -> EmpInfo:
        pass

    @abc.abstractmethod
    def get_trans_ddi_ctl2_info(self, transcoder: str, data: TransDDiCtl2OffsetsValues) -> TransDdiCtl2Info:
        pass

    @abc.abstractmethod
    def get_timing_info(self, transcoder: TranscoderType, data: TimingOffsetValues = None) -> TimingsInfo:
        pass

    @abc.abstractmethod
    def get_dpst_info(self, pipe: PipeType, data: DpstOffsetValues = None) -> DpstInfo:
        pass

    @abc.abstractmethod
    def get_psr_info(self, transcoder: TranscoderType, data: PsrOffsetValues = None) -> PsrInfo:
        pass

    @abc.abstractmethod
    def get_hw3dlut_info(self, pipe: str, data: Hw3dLutOffsetsValues) -> Hw3dlutInfo:
        pass

    @abc.abstractmethod
    def get_colorctl_info(self, pipe: str, data: ColorCtlOffsetsValues) -> ColorCtlInfo:
        pass

    @abc.abstractmethod
    def get_lace_info(self, pipe: str, data: LaceOffsetsValues) -> LaceInfo:
        pass

    @abc.abstractmethod
    def get_trans_ddi_info(self, transcoder: str, data: TransDDiOffsetsValues) -> TransDdiInfo:
        pass

    @abc.abstractmethod
    def get_pipe_csc_coeff_info(self, pipe: str, data: PipeCscCoeffOffsetValues) -> PipeCscCoeffInfo:
        pass

    @abc.abstractmethod
    def get_avi_info(self, plane: str, pipe: str, data: AviInfoOffsetsValues) -> AviInfo:
        pass

    @abc.abstractmethod
    def get_video_dip_info(self, pipe: str, data: VideoDipCtlOffsetsValues) -> VideoDipCtlInfo:
        pass

    @abc.abstractmethod
    def get_plane_csc_coeff_info(self, pipe: str, plane: str, data: PlaneCscCoeffOffsetValues) -> PlaneCscCoeffInfo:
        pass

    @abc.abstractmethod
    def get_plane_degamma_data_info(self, plane: str, pipe: str, lut_size: int) -> GammaDataInfo:
        pass

    @abc.abstractmethod
    def get_plane_gamma_data_info(self, plane: str, pipe: str, lut_size: int) -> GammaDataInfo:
        pass

    @abc.abstractmethod
    def get_pipe_gamma_multi_segment_info(self, pipe: str, lut_size: int) -> GammaDataInfo:
        pass

    @abc.abstractmethod
    def get_pipe_pal_prec_data_info(self, pipe: str, lut_size: int) -> GammaDataInfo:
        pass

    @abc.abstractmethod
    def get_pipe_gamma_ext_reg_info(self, pipe: str) -> GammaDataInfo:
        pass

    # @todo need to have function implementation in Gen*DisplayRegsInterface.py
    @abc.abstractmethod
    def get_pipe_degamma_data_info_for_cc1(self, pipe: str, lut_size: int) -> GammaDataInfo:
       pass

    @abc.abstractmethod
    def get_pipe_degamma_data_info_for_cc2(self, pipe: str, lut_size: int) -> GammaDataInfo:
       pass

    @abc.abstractmethod
    def get_pipe_gamma_data_info_for_cc1(self, pipe: str, lut_size: int) -> GammaDataInfo:
       pass

    @abc.abstractmethod
    def get_trans_msa_misc_info(self, pipe:str, data: TransMsaMiscOffsetsValues)->MsaMiscInfo:
        pass

    @abc.abstractmethod
    def get_pipe_gamma_data_info_for_cc2(self, pipe: str, lut_size: int) -> GammaDataInfo:
       pass

    # @abc.abstractmethod
    # def get_plane_csc_pre_post_offset_info(
    # self, pipe: str, plane: str, data: PlaneCscPrePostOffsetValues) -> PlaneCscPrePostOffInfo:
    #    pass

    # @abc.abstractmethod
    # def get_pipe_csc_pre_post_offset_info(self, pipe: str, data: PipeCscPrePostOffsetValues) -> PipeCscPrePostOffInfo:
    #    pass

    @abc.abstractmethod
    def get_pipe_frame_ctr_info(self, pipe: str, data: PipeFrameCtrOffsetValues) -> PipeFrameCtrInfo:
        pass

    @abc.abstractmethod
    def get_dc6v_info(self, data: Dc6vOffsetValues = None) -> Dc6vInfo:
        pass

    @abc.abstractmethod
    def get_plane_pixel_normalizer_info(self, plane: str, pipe: str) -> PlanePixelNormalizeInfo:
        pass

    @abc.abstractmethod
    def get_plane_ctl_info(self, plane: str, pipe: str) -> PlaneCtlInfo:
        pass

    @abc.abstractmethod
    def get_cmtg_info(self, transcoder: TranscoderType, data: CmtgOffsetValues = None) -> CmtgInfo:
        pass

    @abc.abstractmethod
    def get_scaler_info(self,plane:str,pipe:str,data: ScalerOffsetsValues) -> ScalerInfo:
        pass

    @abc.abstractmethod
    def get_interrupt_info(self, data: InterruptOffsetValues = None) -> InterruptInfo:
        pass

    @abc.abstractmethod
    def get_dcstate_info(self, data: DCStateOffsetsValues = None) -> DcStateInfo:
        pass

    @abc.abstractmethod
    def get_alpm_info(self, pipe: str, data: ALPMOffsetsValues = None) -> ALPMInfo:
        pass

    @abc.abstractmethod
    def get_audio_ctl_offsets(self, pipe: str) -> AudDP2CtlOffsets:
        pass
