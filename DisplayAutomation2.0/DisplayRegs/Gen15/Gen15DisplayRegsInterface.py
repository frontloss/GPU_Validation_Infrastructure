########################################################################################################################
# @file         Gen15DisplayRegsInterface.py
# @brief        Contains DisplayRegsService implementation for Gen15 platforms
#
# @author       Rohit Kumar
########################################################################################################################

from DisplayRegs.DisplayRegsInterface import *
from DisplayRegs.Gen15.Pipe.Gen15PipeRegs import *
from DisplayRegs.Gen15.Plane.Gen15PlaneRegs import *
from DisplayRegs.Gen15.Transcoder.Gen15TranscoderRegs import *
from DisplayRegs.Gen15.DisplayPowerHandler.Gen15DisplayPowerRegs import *
from DisplayRegs.Gen15.Interrupt.Gen15InterruptRegs import *


class Gen15DisplayRegsService(DisplayRegsService):

    ####################################################################################################################
    # Methods to get register offsets (required in ETL based verification)
    ####################################################################################################################

    ##
    # @brief        Exposed API to get Timing register offsets for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @return       TimingOffsets
    def get_timing_offsets(self, transcoder: TranscoderType) -> TimingOffsets:
        transcoder_name = transcoder.name.split('_')[1]
        return TimingOffsets(
            getattr(OFFSET_TRANS_HTOTAL, f'TRANS_HTOTAL_{transcoder_name}'),
            getattr(OFFSET_TRANS_HBLANK, f'TRANS_HBLANK_{transcoder_name}'),
            getattr(OFFSET_TRANS_HSYNC, f'TRANS_HSYNC_{transcoder_name}'),
            getattr(OFFSET_TRANS_VTOTAL, f'TRANS_VTOTAL_{transcoder_name}'),
            getattr(OFFSET_TRANS_VBLANK, f'TRANS_VBLANK_{transcoder_name}'),
            getattr(OFFSET_TRANS_VSYNC, f'TRANS_VSYNC_{transcoder_name}'),
            getattr(OFFSET_TRANS_VSYNCSHIFT, f'TRANS_VSYNCSHIFT_{transcoder_name}'),
            getattr(OFFSET_DATAM, f'TRANS_DATAM1_{transcoder_name}'),
            getattr(OFFSET_DATAN, f'TRANS_DATAN1_{transcoder_name}'),
            getattr(OFFSET_LINKM, f'TRANS_LINKM1_{transcoder_name}'),
            getattr(OFFSET_LINKN, f'TRANS_LINKN1_{transcoder_name}'),
        )

    ##
    # @brief        Exposed API to get VRR offsets for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @return       VrrOffsets
    def get_vrr_offsets(self, transcoder: TranscoderType) -> VrrOffsets:
        transcoder_name = transcoder.name.split('_')[1]
        return VrrOffsets(
            getattr(OFFSET_TRANS_VRR_CTL, f'TRANS_VRR_CTL_{transcoder_name}'),
            getattr(OFFSET_TRANS_VRR_VMAX, f'TRANS_VRR_VMAX_{transcoder_name}'),
            getattr(OFFSET_TRANS_VRR_VMIN, f'TRANS_VRR_VMIN_{transcoder_name}'),
            getattr(OFFSET_TRANS_VRR_STATUS, f'TRANS_VRR_STATUS_{transcoder_name}'),
            getattr(OFFSET_TRANS_PUSH, f'TRANS_PUSH_{transcoder_name}'),
            getattr(OFFSET_TRANS_VRR_FLIPLINE, f'TRANS_VRR_FLIPLINE_{transcoder_name}'),
            getattr(OFFSET_TRANS_VRR_VTOTAL_PREV, f'TRANS_VRR_VTOTAL_PREV_{transcoder_name}'),
            getattr(OFFSET_PIPE_DMC_SCANLINE_CMP_UPPER, f'PIPE_DMC_SCANLINE_CMP_UPPER_{transcoder_name}'),
            getattr(OFFSET_TRANS_VRR_VMAX_DCB, f'TRANS_VRR_VMAX_DCB_{transcoder_name}'),
            getattr(OFFSET_TRANS_VRR_FLIPLINE_DCB, f'TRANS_VRR_FLIPLINE_DCB_{transcoder_name}'),
        )

    ##
    # @brief        Exposed API to get Emp offsets for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @return       EmpOffsets
    def get_emp_offsets(self, transcoder: TranscoderType) -> EmpOffsets:
        transcoder_name = transcoder.name.split('_')[1]
        return EmpOffsets(
            getattr(OFFSET_HDMI_EMP_CTL, f'HDMI_EMP_CTL_{transcoder_name}'),
            getattr(OFFSET_HDMI_EMP_HEADER, f'HDMI_EMP_HEADER_{transcoder_name}'),
            getattr(OFFSET_HDMI_EMP_DATA, f'HDMI_EMP_DATA_{transcoder_name}'),
            getattr(OFFSET_EMP_AS_SDP_TL, f'EMP_AS_SDP_TL_{transcoder_name}')
        )

    ##
    # @brief        Exposed API to get DPST offsets for given pipe
    # @param[in]    pipe, PipeType
    # @return       DpstOffsets
    def get_dpst_offsets(self, pipe: PipeType) -> DpstOffsets:
        pipe_name = pipe.name.split('_')[1]
        return DpstOffsets(
            getattr(OFFSET_DPST_CTL, f'DPST_CTL_{pipe_name}'),
            getattr(OFFSET_DPST_GUARD, f'DPST_GUARD_{pipe_name}'),
            getattr(OFFSET_DPST_HIST_BIN, f'DPST_HIST_BIN_{pipe_name}')
        )

    ##
    # @brief        Exposed API to get PSR offsets for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @return       PsrOffsets
    def get_psr_offsets(self, transcoder: TranscoderType) -> PsrOffsets:
        transcoder_name = transcoder.name.split('_')[1]
        return PsrOffsets(
            getattr(OFFSET_SRD_CTL, f'SRD_CTL_{transcoder_name}'),
            getattr(OFFSET_SRD_STATUS, f'SRD_STATUS_{transcoder_name}'),
            getattr(OFFSET_PSR_MASK, f'PSR_MASK_{transcoder_name}'),
            getattr(OFFSET_PSR2_CTL, f'PSR2_CTL_{transcoder_name}'),
            getattr(OFFSET_PSR2_STATUS, f'PSR2_STATUS_{transcoder_name}'),
        )

    ##
    # @brief        Exposed API to get HW_3D_LUT offsets for given pipe
    # @param[in]    pipe, str -'A','B'
    # @return       Hw3dLutOffsets
    def get_3dlut_offsets(self, pipe: str) -> Hw3dLutOffsets:
        return Hw3dLutOffsets(
            getattr(OFFSET_LUT_3D_CTL, f'LUT_3D_CTL_{pipe}'),
            getattr(OFFSET_LUT_3D_DATA, f'LUT_3D_DATA_{pipe}'),
            getattr(OFFSET_LUT_3D_INDEX, f'LUT_3D_INDEX_{pipe}'),
        )

    ##
    # @brief        Exposed API to get lace offsets for given pipe
    # @param[in]    pipe, str -'A','B'
    # @return       LaceOffsets
    def get_lace_offsets(self, pipe: str) -> LaceOffsets:
        return LaceOffsets(
            getattr(OFFSET_DPLC_CTL, f'DPLC_CTL_{pipe}'),
        )

    ##
    # @brief        Exposed API to get color ctl offsets for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       ColorCtlOffsets
    def get_color_ctrl_offsets(self, pipe: str) -> ColorCtlOffsets:
        return ColorCtlOffsets(
            getattr(OFFSET_PIPE_MISC, f'PIPE_MISC_{pipe}'),
            getattr(OFFSET_PIPE_MISC2, f'PIPE_MISC2_{pipe}'),
            getattr(OFFSET_CSC_MODE, f'CSC_MODE_{pipe}'),
            getattr(OFFSET_GAMMA_MODE, f'GAMMA_MODE_{pipe}'),
        )

    ##
    # @brief        Exposed API to get Transcoder offsets for given pipe
    # @param[in]    transcoder, TranscoderType
    # @return       TransDDiOffsets
    def get_trans_ddi_offsets(self, transcoder: str) -> TransDDiOffsets:
        transcoder = transcoder.split('_')[1]
        return TransDDiOffsets(
            getattr(OFFSET_TRANS_DDI_FUNC_CTL, f'TRANS_DDI_FUNC_CTL_{transcoder}'),
        )

    ##
    # @brief        Exposed API to get Transcoder ctl2 offsets for given pipe
    # @param[in]    transcoder, TranscoderType
    # @return       TransDDiCtl2Offsets
    def get_trans_ddi_ctl2_offsets(self, transcoder: str) -> TransDDiCtl2Offsets:
        transcoder = transcoder.split('_')[1]
        return TransDDiCtl2Offsets(
            getattr(OFFSET_TRANS_DDI_FUNC_CTL2, f'TRANS_DDI_FUNC_CTL2_{transcoder}'),
        )

    ##
    # @brief        Exposed API to get pipe coeff offsets list for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       PipeCscCoeffOffsets
    def get_pipe_csc_coeff_offsets(self, pipe: str) -> PipeCscCoeffOffsets:
        pipe_csc_coeff_offsets = []
        if hasattr(OFFSET_CSC_CC2_COEFF, f'CSC_CC2_COEFF_{pipe}'):
            pipe_csc_coeff_attr_list = [getattr(OFFSET_CSC_COEFF, f'CSC_COEFF_{pipe}'),
                                        getattr(OFFSET_OUTPUT_CSC_COEFF, f'OUTPUT_CSC_COEFF_{pipe}'),
                                                getattr(OFFSET_CSC_CC2_COEFF, f'CSC_CC2_COEFF_{pipe}')
                                    ]

            for attr in pipe_csc_coeff_attr_list:
                coeff_offsets = []
                for i in range(0, 3):
                    offset = (attr + i * 8)
                    coeff_offsets.append(offset)
                    coeff_offsets.append(offset + 4)
                pipe_csc_coeff_offsets.append(coeff_offsets)
            return PipeCscCoeffOffsets(
                pipe_csc_coeff_offsets[0],
                pipe_csc_coeff_offsets[1],
                pipe_csc_coeff_offsets[2],
            )
        else:
            pipe_csc_coeff_attr_list = [getattr(OFFSET_CSC_COEFF, f'CSC_COEFF_{pipe}'),
                                        getattr(OFFSET_OUTPUT_CSC_COEFF, f'OUTPUT_CSC_COEFF_{pipe}')]

            for attr in pipe_csc_coeff_attr_list:
                coeff_offsets = []
                for i in range(0, 3):
                    offset = (attr + i * 8)
                    coeff_offsets.append(offset)
                    coeff_offsets.append(offset + 4)
                pipe_csc_coeff_offsets.append(coeff_offsets)
            return PipeCscCoeffOffsets(
                pipe_csc_coeff_offsets[0], pipe_csc_coeff_offsets[1], [0],
            )

    ##
    # @brief        Exposed API to get plane coeff offsets list for given pipe and plane
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @return       PlaneCscCoeffOffsets
    def get_plane_csc_coeff_offsets(self, pipe: str, plane: str) -> PlaneCscCoeffOffsets:
        plane_csc_coeff_offsets = []
        plane_csc_coeff_attr_list = [getattr(OFFSET_PLANE_CSC_COEFF, f'PLANE_CSC_COEFF_{plane}_{pipe}'),
                                     getattr(OFFSET_PLANE_INPUT_CSC_COEFF, f'PLANE_INPUT_CSC_COEFF_{plane}_{pipe}')]
        for attr in plane_csc_coeff_attr_list:
            coeff_offsets = []
            for i in range(0, 3):
                offset = (attr + i * 8)
                coeff_offsets.append(offset)
                coeff_offsets.append(offset + 4)
            plane_csc_coeff_offsets.append(coeff_offsets)
        return PlaneCscCoeffOffsets(
            plane_csc_coeff_offsets[0],
            plane_csc_coeff_offsets[1], )


    ##
    # @brief        Exposed API to get Plane Control Offsets for given plane, pipe
    # @param[in]    plane, str -'A'
    # @param[in]    pipe, str -'A'
    # @return       PlaneControlOffsets
    def get_plane_ctl_offsets(self, plane: str, pipe: str) -> PlaneCtlOffsets:
        return PlaneCtlOffsets(
            getattr(OFFSET_PLANE_CTL, f'PLANE_CTL_{plane}_{pipe}'))

    ##
    # @brief        Exposed API to get Plane Pixel Normalizer Offsets for given plane, pipe
    # @param[in]    plane, str -'A'
    # @param[in]    pipe, str -'A'
    # @return       PlanePixelNormalizerOffsets
    def get_plane_pixel_normalizer_offsets(self, plane: str, pipe: str) -> PlanePixelNormalizerOffsets:
        return PlanePixelNormalizerOffsets(
            getattr(OFFSET_PLANE_PIXEL_NORMALIZE, f'PLANE_PIXEL_NORMALIZE_{plane}_{pipe}'))

    # @brief        Exposed API to get Plane Pre and Post CSC Gamma Index and Data Info for given plane, pipe
    # @param[in]    plane, str -'A'
    # @param[in]    pipe, str -'A'
    # @return       PlaneGammaOffsets
    def get_plane_gamma_offsets(self, plane: str, pipe: str) -> PlaneGammaOffsets:
        return PlaneGammaOffsets(
            getattr(OFFSET_PLANE_PRE_CSC_GAMC_INDEX, f'PLANE_PRE_CSC_GAMC_INDEX_{plane}_{pipe}'),
            getattr(OFFSET_PLANE_PRE_CSC_GAMC_DATA, f'PLANE_PRE_CSC_GAMC_DATA_{plane}_{pipe}'),
            getattr(OFFSET_PLANE_POST_CSC_GAMC_INDEX, f'PLANE_POST_CSC_GAMC_INDEX_{plane}_{pipe}'),
            getattr(OFFSET_PLANE_POST_CSC_GAMC_DATA, f'PLANE_POST_CSC_GAMC_DATA_{plane}_{pipe}')
        )

    # @brief        Exposed API to get Plane Pre and Post CSC Gamma Index and Data Enh offsets for given plane, pipe
    # @param[in]    plane, str -'A'
    # @param[in]    pipe, str -'A'
    # @return       PlaneGammaOffsets
    def get_plane_gamma_enh_offsets(self, plane: str, pipe: str) -> PlaneGammaEnhOffsets:
        return PlaneGammaEnhOffsets(
            getattr(OFFSET_PLANE_PRE_CSC_GAMC_INDEX_ENH, f'PLANE_PRE_CSC_GAMC_INDEX_ENH_{plane}_{pipe}'),
            getattr(OFFSET_PLANE_PRE_CSC_GAMC_DATA_ENH, f'PLANE_PRE_CSC_GAMC_DATA_ENH_{plane}_{pipe}'),

            getattr(OFFSET_PLANE_POST_CSC_GAMC_INDEX_ENH, f'PLANE_POST_CSC_GAMC_INDEX_ENH_{plane}_{pipe}'),
            getattr(OFFSET_PLANE_POST_CSC_GAMC_DATA_ENH, f'PLANE_POST_CSC_GAMC_DATA_ENH_{plane}_{pipe}')
        )

    ##
    # @brief        Exposed API to get Pipe Gamma Info for given pipe
    # @param[in]    pipe, str -'A','B'
    # @return       PipeGammaOffsets
    def get_pipe_gamma_cc2_offsets(self, pipe: str) -> PipeGammaOffsetsCC2:
        pipe_str = pipe.split("CC2_")[1]
        return PipeGammaOffsetsCC2(
            getattr(OFFSET_PAL_GC_MAX, f'PAL_GC_MAX_{pipe}'),
            getattr(OFFSET_PRE_CSC_CC2_GAMC_INDEX, f'PRE_CSC_CC2_GAMC_INDEX_{pipe_str}'),
            getattr(OFFSET_PRE_CSC_CC2_GAMC_DATA,f'PRE_CSC_CC2_GAMC_DATA_{pipe_str}'),
            getattr(OFFSET_POST_CSC_CC2_INDEX, f'POST_CSC_CC2_INDEX_{pipe_str}'),
            getattr(OFFSET_POST_CSC_CC2_DATA, f'POST_CSC_CC2_DATA_{pipe_str}')
            )

    ##
    # @brief        Exposed API to get Pipe Gamma Info for given pipe
    # @param[in]    pipe, str -'A'
    # @return       PipeGammaOffsets
    def get_pipe_gamma_offsets(self, pipe: str) -> PipeGammaOffsets:
        return PipeGammaOffsets(
            getattr(OFFSET_PRE_CSC_GAMC_INDEX, f'PRE_CSC_GAMC_INDEX_{pipe}'),
            getattr(OFFSET_PRE_CSC_GAMC_DATA, f'PRE_CSC_GAMC_DATA_{pipe}'),
            0,0,

            getattr(OFFSET_PAL_PREC_INDEX, f'PAL_PREC_INDEX_{pipe}'),
            getattr(OFFSET_PAL_PREC_DATA, f'PAL_PREC_DATA_{pipe}'),

            0, 0, 0, 0,

            getattr(OFFSET_PAL_GC_MAX, f'PAL_GC_MAX_{pipe}'),
            getattr(OFFSET_PAL_EXT_GC_MAX, f'PAL_EXT_GC_MAX_{pipe}'),
            getattr(OFFSET_PAL_EXT2_GC_MAX, f'PAL_EXT2_GC_MAX_{pipe}')
        )

    ##
    # @brief        Exposed API to get avi info offsets list for given pipe and plane
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @return       AviInfoOffsets
    def get_avi_info_offsets(self, plane: str, pipe: str) -> AviInfoOffsets:
        return AviInfoOffsets(
            getattr(OFFSET_VIDEO_DIP_DATA, f'VIDEO_DIP_AVI_DATA_{plane}_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_CTL, f'VIDEO_DIP_CTL_{pipe}')
        )

    ##
    # @brief        Exposed API to get vsc sdp data info offsets list for given pipe and plane
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @return       vscsdpOffsets
    def get_vsc_sdp_offsets(self, plane: str, pipe: str) -> VscSdpDataOffsets:
        return VscSdpDataOffsets(
            getattr(OFFSET_VIDEO_DIP_DATA, f'VIDEO_DIP_VSC_DATA_{plane}_{pipe}')
        )

    ##
    # @brief        Exposed API to get VIDEO_DIP_CTL offsets for given pipe
    # @param[in]    plane, str -'A','B','C','D'
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       VideoDipCtlOffsets
    def get_video_dip_ctl_offset(self, pipe: str) -> VideoDipCtlOffsets:
        return VideoDipCtlOffsets(
            getattr(OFFSET_VIDEO_DIP_CTL, f'VIDEO_DIP_CTL_{pipe}')
        )

    ##
    # @brief        Exposed API to get pipe csc pre and post offsets list for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       PipeCscPrePostOffsets
    def get_pipe_csc_pre_post_offsets(self, pipe: str) -> PipeCscPrePostOffsets:
        pipe_csc_offsets = []
        pipe_csc_attr_list = [getattr(OFFSET_CSC_PREOFF, f'CSC_PREOFF_{pipe}'),
                              getattr(OFFSET_CSC_POSTOFF, f'CSC_POSTOFF_{pipe}'),
                              # @todo : Currently OutputCSCPreOff is not present in the autogen Gen*PipeRegs.py . Once  fixed will uncomment this
                              # getattr(OFFSET_OUTPUT_CSC_PREOFF, f'OUTPUT_CSC_PREOFF_{pipe}'),
                              getattr(OFFSET_OUTPUT_CSC_POSTOFF, f'OUTPUT_CSC_POSTOFF_{pipe}')]

        for attr in pipe_csc_attr_list:
            coeff_offsets = []
            for i in range(0, 3):
                coeff_offsets.append(attr)
                attr = attr + 4
            pipe_csc_offsets.append(coeff_offsets)
        return PipeCscPrePostOffsets(
            pipe_csc_offsets[0], pipe_csc_offsets[1], pipe_csc_offsets[2],
        )

    ##
    # @brief        Exposed API to get plane csc pre and post offsets list for given pipe and plane
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @return       PlaneCscPrePostOffsets
    def get_plane_csc_pre_post_offsets(self, plane: str, pipe: str) -> PlaneCscPrePostOffsets:
        plane_csc_offsets = []
        plane_csc_attr_list = [getattr(OFFSET_PLANE_CSC_PREOFF, f'PLANE_CSC_PREOFF_{plane}_{pipe}'),
                               getattr(OFFSET_PLANE_CSC_POSTOFF, f'PLANE_CSC_POSTOFF_{plane}_{pipe}'),
                               getattr(OFFSET_PLANE_INPUT_CSC_PREOFF, f'PLANE_INPUT_CSC_PREOFF_{plane}_{pipe}'),
                               getattr(OFFSET_PLANE_INPUT_CSC_POSTOFF, f'PLANE_INPUT_CSC_POSTOFF_{plane}_{pipe}')]

        for attr in plane_csc_attr_list:
            coeff_offsets = []
            for i in range(0, 3):
                coeff_offsets.append(attr)
                attr = attr + 4
            plane_csc_offsets.append(coeff_offsets)
        return PlaneCscPrePostOffsets(
            plane_csc_offsets[0], plane_csc_offsets[1], plane_csc_offsets[2], plane_csc_offsets[3],
        )

    ##
    # @brief        Exposed API to get Metadata offsets for given pipe
    # @param[in]    plane, str -'A','B','C','D'
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       MetadataOffsets
    def get_hdr_metadata_offsets(self, plane: str, pipe: str) -> MetadataOffsets:
        return MetadataOffsets(
            getattr(OFFSET_VIDEO_DIP_DRM_DATA, f'VIDEO_DIP_DRM_DATA_{plane}_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_DATA, f'VIDEO_DIP_GMP_DATA_{plane}_{pipe}'),
            getattr(OFFSET_VSC_EXT_SDP_CTL, f'VSC_EXT_SDP_CTL_{plane}_{pipe}'),
            getattr(OFFSET_VSC_EXT_SDP_DATA, f'VSC_EXT_SDP_DATA_{plane}_{pipe}')
        )

    # @brief        Exposed API to get Pipe frame ctr Info for given pipe
    # @param[in]    pipe, str -'A'
    # @return       PipeFrameCtrOffsets
    def get_pipe_frame_ctr_offsets(self, pipe: str) -> PipeFrameCtrOffsets:
        PipeFramectr = getattr(OFFSET_PIPE_FRMCNT, f'PIPE_FRMCNT_{pipe}')
        PipeFramectrIncr = PipeFramectr + (0x1000 * 1)
        return PipeFrameCtrOffsets(PipeFramectr, PipeFramectrIncr)

    # @brief        Exposed API to get Plane Color Control Offsets for given plane, pipe
    # @param[in]    plane, str -'A'
    # @param[in]    pipe, str -'A'
    # @return       PlaneColorControlOffsets
    def get_plane_color_ctl_offsets(self, plane: str, pipe: str) -> PlaneColorCtlOffsets:
        return PlaneColorCtlOffsets(
            getattr(OFFSET_PLANE_COLOR_CTL, f'PLANE_COLOR_CTL_{plane}_{pipe}'))

    # @brief        Exposed API to get DC6v Info
    # @param[in]    None
    # @return       Dc6vOffsets
    def get_dc6v_offsets(self) -> Dc6vOffsets:
        return Dc6vOffsets(
            getattr(OFFSET_SCANLINE_GB1, 'SCANLINE_GB1_A'),  # To be Enhanced by Feature Owner.
            getattr(OFFSET_DC6V_RESTORE_TIME, 'DC6V_RESTORE_TIME'),
            getattr(OFFSET_WM_LINETIME_DC6V, 'WM_LINETIME_DC6V'),
        )

    ##
    # @brief        Exposed API to get TRANS_MSA_MISC offsets for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       TransMsaMiscOffsets
    def get_trans_msa_misc_offset(self, pipe: str) -> TransMsaMiscOffsets:
        return TransMsaMiscOffsets(
            getattr(OFFSET_TRANS_MSA_MISC, f'TRANS_MSA_MISC_{pipe}')
        )

    ##
    # @brief        Exposed API to get CMTG related offsets in Gen15
    # @param[in]    transcoder, TranscoderType
    # @return       CmtgOffsets
    def get_cmtg_offsets(self, transcoder: TranscoderType) -> CmtgOffsets:
        transcoder_name = transcoder.name.split('_')[1]
        cmtg_map = {'A': 0, 'B': 1}
        return CmtgOffsets(
            getattr(OFFSET_TRANS_CMTG_CTL, f'TRANS_CMTG_CTL_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_TRANS_HTOTAL, f'TRANS_HTOTAL_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_TRANS_HBLANK, f'TRANS_HBLANK_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_TRANS_HSYNC, f'TRANS_HSYNC_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_TRANS_VTOTAL, f'TRANS_VTOTAL_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_TRANS_VBLANK, f'TRANS_VBLANK_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_TRANS_VSYNC, f'TRANS_VSYNC_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_LINKM, f'TRANS_LINKM1_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_LINKN, f'TRANS_LINKN1_CMTG{cmtg_map[transcoder_name]}'),
            getattr(OFFSET_TRANS_DDI_FUNC_CTL2, f'TRANS_DDI_FUNC_CTL2_{transcoder_name}')
        )

    ##
    # @brief        Exposed API to get CMTG interrupt related offsets in Gen13.1
    # @return       InterruptOffsets
    def get_interrupt_offsets(self) -> InterruptOffsets:
        return InterruptOffsets(
            getattr(OFFSET_DE_PORT_INTERRUPT_DEFINITION, 'DE_PORT_INTERRUPT_0'),
            getattr(OFFSET_DE_PORT_INTERRUPT_DEFINITION, 'DE_PORT_INTERRUPT_1'),
            getattr(OFFSET_DE_PORT_INTERRUPT_DEFINITION, 'DE_PORT_INTERRUPT_2'),
            getattr(OFFSET_DE_PORT_INTERRUPT_DEFINITION, 'DE_PORT_INTERRUPT_3'),
        )

    ##
    # @brief        Exposed API to get DC states offsets
    # @return       DCStateOffsets
    def get_dcstate_offsets(self) -> DCStateOffsets:
        return DCStateOffsets(
            getattr(OFFSET_DC_STATE_EN, f'DC_STATE_EN')
        )
    ##
    # @brief        Exposed API to get pipe scaler info offsets list for given pipe and plane
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @return       PipeScalerOffsets
    def get_scaler_offsets(self,plane:str,pipe:str) -> ScalerOffsets:
        return ScalerOffsets(
            getattr(OFFSET_PS_CTRL, f'PS_CTRL_{1}_{pipe}'),
            getattr(OFFSET_PS_CTRL, f'PS_CTRL_{2}_{pipe}')
        )

    ##
    # @brief        Exposed API to get ALMP offsets
    # @return       ALPMOffsets
    def get_ALPM_offsets(self, pipe:str) -> ALPMOffsets:
        return ALPMOffsets(
            getattr(OFFSET_ALPM_CTL, f'ALPM_CTL_{pipe}')
        )

    ##
    # @brief        Exposed API to get video data island packs picture parameter set offsets for given transcoder
    # @param[in]    pipe: str
    #                   E.g. 'A','B','C','D'
    # @return       VideoDataIslandPacketPPSOffsets
    def get_video_dip_pps_offsets(self, pipe: str) -> VideoDataIslandPacketPPSOffsets:
        return VideoDataIslandPacketPPSOffsets(
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_0_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_1_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_2_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_3_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_4_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_5_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_6_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_7_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_8_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_9_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_10_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_11_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_12_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_13_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_14_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_15_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_16_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_17_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_18_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_19_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_20_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_21_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_22_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_23_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_24_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_25_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_26_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_27_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_28_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_29_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_30_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_31_{pipe}'),
            getattr(OFFSET_VIDEO_DIP_PPS_DATA, f'VIDEO_DIP_PPS_DATA_32_{pipe}')
        )

    ####################################################################################################################
    # Methods to get register data
    ####################################################################################################################

    ##
    # @brief        Exposed API to get CMTG info
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data[optional], CmtgOffsetValues, to set value for any register
    # @return       CmtgInfo
    def get_cmtg_info(self, transcoder: TranscoderType, data: CmtgOffsetValues = None) -> CmtgInfo:
        regs = self.get_cmtg_offsets(transcoder)
        if data is not None:
            cmtg_ctl = REG_TRANS_CMTG_CTL(regs.CmtgControlReg, data.CmtgControlReg)
            h_total = REG_TRANS_HTOTAL(regs.CmtgHTotalReg, data.CmtgHTotalReg)
            h_blank = REG_TRANS_HBLANK(regs.CmtgHBlankReg, data.CmtgHBlankReg)
            h_sync = REG_TRANS_HSYNC(regs.CmtgHSyncReg, data.CmtgHSyncReg)
            v_total = REG_TRANS_VTOTAL(regs.CmtgVTotalReg, data.CmtgVTotalReg)
            v_blank = REG_TRANS_VBLANK(regs.CmtgVBlankReg, data.CmtgVBlankReg)
            v_sync = REG_TRANS_VSYNC(regs.CmtgVSyncReg, data.CmtgVSyncReg)
            link_m = REG_LINKM(regs.CmtgLinkMReg, data.CmtgLinkMReg)
            link_n = REG_LINKN(regs.CmtgLinkNReg, data.CmtgLinkNReg)
            ddi_func_ctl = REG_TRANS_DDI_FUNC_CTL2(regs.DdiFunctionControlReg, data.DdiFunctionControlReg)
            context_latency = REG_TRANS_SET_CONTEXT_LATENCY(regs.CmtgContextLatency, data.CmtgContextLatency)
        else:
            cmtg_ctl = REG_TRANS_CMTG_CTL(regs.CmtgControlReg, read_register(regs.CmtgControlReg, self.gfx_index))
            h_total = REG_TRANS_HTOTAL(regs.CmtgHTotalReg, read_register(regs.CmtgHTotalReg, self.gfx_index))
            h_blank = REG_TRANS_HBLANK(regs.CmtgHBlankReg, read_register(regs.CmtgHBlankReg, self.gfx_index))
            h_sync = REG_TRANS_HSYNC(regs.CmtgHSyncReg, read_register(regs.CmtgHSyncReg, self.gfx_index))
            v_total = REG_TRANS_VTOTAL(regs.CmtgVTotalReg, read_register(regs.CmtgVTotalReg, self.gfx_index))
            v_blank = REG_TRANS_VBLANK(regs.CmtgVBlankReg, read_register(regs.CmtgVBlankReg, self.gfx_index))
            v_sync = REG_TRANS_VSYNC(regs.CmtgVSyncReg, read_register(regs.CmtgVSyncReg, self.gfx_index))
            link_m = REG_LINKM(regs.CmtgLinkMReg, read_register(regs.CmtgLinkMReg, self.gfx_index))
            link_n = REG_LINKN(regs.CmtgLinkNReg, read_register(regs.CmtgLinkNReg, self.gfx_index))
            ddi_func_ctl = REG_TRANS_DDI_FUNC_CTL2(regs.DdiFunctionControlReg,
                                                   read_register(regs.DdiFunctionControlReg, self.gfx_index))
            context_latency = REG_TRANS_SET_CONTEXT_LATENCY(regs.CmtgContextLatency,
                                                            read_register(regs.CmtgContextLatency, self.gfx_index))

        return CmtgInfo(
            cmtg_ctl.CmtgEnable, ddi_func_ctl.CmtgSlaveMode, h_total.HorizontalTotal, h_total.HorizontalActive,
            h_blank.HorizontalBlankStart, h_blank.HorizontalBlankEnd, h_sync.HorizontalSyncStart,
            h_sync.HorizontalSyncEnd, v_total.VerticalTotal, v_total.VerticalActive, v_blank.VerticalBlankStart,
            v_blank.VerticalBlankEnd, v_sync.VerticalSyncStart, v_sync.VerticalSyncEnd, link_m.LinkMValue,
            link_n.LinkNValue, context_latency.ContextLatency
        )

    ##
    # @brief        Exposed API to get VRR info for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data[optional], VrrOffsetvalues, to set value for any register
    # @return       VrrInfo
    def get_vrr_info(self, transcoder: TranscoderType, data: VrrOffsetValues = None) -> VrrInfo:
        regs = self.get_vrr_offsets(transcoder)

        if data is not None:
            v_min = REG_TRANS_VRR_VMIN(regs.VrrVminReg, data.VrrVminReg)
            v_max = REG_TRANS_VRR_VMAX(regs.VrrVmaxReg, data.VrrVmaxReg)
            flip_line = REG_TRANS_VRR_FLIPLINE(regs.VrrFlipLine, data.VrrFlipLine)
            vrr_ctl = REG_TRANS_VRR_CTL(regs.VrrControl, data.VrrControl)
            vrr_status = REG_TRANS_VRR_STATUS(regs.VrrStatus, data.VrrStatus)
            vrr_push = REG_TRANS_PUSH(regs.VrrPush, data.VrrPush)
            scanline_upper = REG_PIPE_DMC_SCANLINE_CMP_UPPER(regs.PipeDmcScanlineUpper, data.PipeDmcScanlineUpper)
            dcb_vmax = REG_TRANS_VRR_VMAX_DCB(regs.VrrDcbVmaxReg, data.VrrDcbVmaxReg)
            dcb_flipline = REG_TRANS_VRR_FLIPLINE_DCB(regs.VrrDcbFlipLine, data.VrrDcbFlipLine)
        else:
            v_min = REG_TRANS_VRR_VMIN(regs.VrrVminReg, read_register(regs.VrrVminReg, self.gfx_index))
            v_max = REG_TRANS_VRR_VMAX(regs.VrrVmaxReg, read_register(regs.VrrVmaxReg, self.gfx_index))
            flip_line = REG_TRANS_VRR_FLIPLINE(regs.VrrFlipLine, read_register(regs.VrrFlipLine, self.gfx_index))
            vrr_ctl = REG_TRANS_VRR_CTL(regs.VrrControl, read_register(regs.VrrControl, self.gfx_index))
            vrr_status = REG_TRANS_VRR_STATUS(regs.VrrStatus, read_register(regs.VrrStatus, self.gfx_index))
            vrr_push = REG_TRANS_PUSH(regs.VrrPush, read_register(regs.VrrPush, self.gfx_index))
            scanline_upper = REG_PIPE_DMC_SCANLINE_CMP_UPPER(regs.PipeDmcScanlineUpper,
                                                             read_register(regs.PipeDmcScanlineUpper, self.gfx_index))
            dcb_vmax = REG_TRANS_VRR_VMAX_DCB(regs.VrrDcbVmaxReg, read_register(regs.VrrDcbVmaxReg, self.gfx_index))
            dcb_flipline = REG_TRANS_VRR_FLIPLINE_DCB(regs.VrrDcbFlipLine,
                                                      read_register(regs.VrrDcbFlipLine, self.gfx_index))

        return VrrInfo(
            v_min.VrrVmin, v_max.VrrVmax, flip_line.VrrFlipline,
            vrr_ctl.VrrEnable == 1, vrr_ctl.FlipLineEnable == 1,
            vrr_status.VrrEnableLive == 1, vrr_push.PushEnable == 1, vrr_push.SendPush == 1, vrr_ctl.VrrGuardband,
            scanline_upper.ScanLineUpper, dcb_vmax.VrrDcbVmax, dcb_flipline.VrrDcbFlipline
        )

    ##
    # @brief        Exposed API to get EMP info for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data[optional], EmpOffsetvalues, to set value for any register
    # @return       EmpInfo
    def get_emp_info(self, transcoder: TranscoderType, data: EmpOffsetValues = None) -> EmpInfo:
        regs = self.get_emp_offsets(transcoder)

        if data is not None:
            emp_ctl = REG_HDMI_EMP_CTL(regs.EmpControl, data.EmpControl)
            emp_header = REG_HDMI_EMP_HEADER(regs.EmpHeader, data.EmpHeader)
            emp_data = REG_HDMI_EMP_DATA(regs.EmpData, data.EmpData)
            emp_as_sdp_tl = REG_EMP_AS_SDP_TL(regs.EmpAsSdpTl, data.EmpAsSdpTl)
        else:
            emp_ctl = REG_HDMI_EMP_CTL(regs.EmpControl, read_register(regs.EmpControl, self.gfx_index))
            emp_header = REG_HDMI_EMP_HEADER(regs.EmpHeader, read_register(regs.EmpHeader, self.gfx_index))
            emp_data = REG_HDMI_EMP_DATA(regs.EmpData, read_register(regs.EmpData, self.gfx_index))
            emp_as_sdp_tl = REG_EMP_AS_SDP_TL(regs.EmpAsSdpTl, read_register(regs.EmpAsSdpTl, self.gfx_index))
        return EmpInfo(
            emp_ctl.ExtendedMetadataPacketType,
            emp_header.Hb0_Spare, emp_header.DataSetType, emp_header.NumberOfPackets, emp_header.End,
            emp_data.EmpData, emp_as_sdp_tl.DoubleBufferAndTransmissionLine
        )

    ##
    # @brief        Exposed API to get Timings info for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data[optional], TimingOffsetValues, to set value for any register
    # @return       TimingsInfo
    def get_timing_info(self, transcoder: TranscoderType, data: TimingOffsetValues = None) -> TimingsInfo:
        regs = self.get_timing_offsets(transcoder)
        if data is not None:
            h_total = REG_TRANS_HTOTAL(regs.HTotal, data.HTotal)
            v_total = REG_TRANS_VTOTAL(regs.VTotal, data.VTotal)
            link_m = REG_LINKM(regs.LinkM, data.LinkM)
            v_blank_start = REG_TRANS_VBLANK(regs.VBlank, data.VBlank)
            v_sync_start = REG_TRANS_VSYNC(regs.VSync, data.VSync)
        else:
            h_total = REG_TRANS_HTOTAL(regs.HTotal, read_register(regs.HTotal, self.gfx_index))
            v_total = REG_TRANS_VTOTAL(regs.VTotal, read_register(regs.VTotal, self.gfx_index))
            link_m = REG_LINKM(regs.LinkM, read_register(regs.LinkM, self.gfx_index))
            v_blank_start = REG_TRANS_VBLANK(regs.VBlank, read_register(regs.VBlank, self.gfx_index))
            v_sync_start = REG_TRANS_VSYNC(regs.VSync, read_register(regs.VSync, self.gfx_index))

        return TimingsInfo(h_total.HorizontalTotal, h_total.HorizontalActive, v_total.VerticalTotal,
                           v_total.VerticalActive, link_m.LinkMValue, v_blank_start.VerticalBlankStart,
                           v_sync_start.VerticalSyncStart)

    ##
    # @brief        Exposed API to get PSR info for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data[optional], PsrOffsetValues, to set value for any register
    # @return       PsrInfo
    def get_psr_info(self, transcoder: TranscoderType, data: PsrOffsetValues = None) -> PsrInfo:
        regs = self.get_psr_offsets(transcoder)

        if data is not None:
            srd_ctl = REG_SRD_CTL(regs.SrdCtlReg, data.SrdCtlReg)
            srd_status = REG_SRD_STATUS(regs.SrdStatusReg, data.SrdStatusReg)
            psr2_ctl = REG_PSR2_CTL(regs.Psr2CtrlReg, data.Psr2CtrlReg)
            psr2_status = REG_PSR2_STATUS(regs.Psr2StatusReg, data.Psr2StatusReg)
        else:
            srd_ctl = REG_SRD_CTL(regs.SrdCtlReg, read_register(regs.SrdCtlReg, self.gfx_index))
            srd_status = REG_SRD_STATUS(regs.SrdStatusReg, read_register(regs.SrdStatusReg, self.gfx_index))
            psr2_ctl = REG_PSR2_CTL(regs.Psr2CtrlReg, read_register(regs.Psr2CtrlReg, self.gfx_index))
            psr2_status = REG_PSR2_STATUS(regs.Psr2StatusReg, read_register(regs.Psr2StatusReg, self.gfx_index))

        return PsrInfo(
            srd_ctl.SrdEnable == 1, psr2_ctl.Psr2Enable == 1, psr2_status.Psr2State == 0x8, False, False, False,
            psr2_ctl.IdleFrames, psr2_status.Psr2State == 0x0
        )

    ##
    # @brief        Exposed API to get DPST info for given transcoder
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data[optional], DpstOffsetValues, to set value for any register
    # @return       DpstInfo
    def get_dpst_info(self, pipe: PipeType, data: DpstOffsetValues = None) -> DpstInfo:
        dpst_regs = self.get_dpst_offsets(pipe)

        if data is not None:
            dpst_ctl = REG_DPST_CTL(dpst_regs.DpstControl, data.DpstControl)
            dpst_guard = REG_DPST_GUARD(dpst_regs.DpstGuard, data.DpstGuard)
        else:
            dpst_ctl = REG_DPST_CTL(dpst_regs.DpstControl, read_register(dpst_regs.DpstControl, self.gfx_index))
            dpst_guard = REG_DPST_GUARD(dpst_regs.DpstGuard, read_register(dpst_regs.DpstGuard, self.gfx_index))

        return DpstInfo(dpst_ctl.IeHistogramEnable == 1, dpst_guard.HistogramEventStatus == 1,
                        dpst_guard.HistogramInterruptEnable == 1)

    ##
    # @brief        Exposed API to get Hw3DLut info for given pipe
    # @param[in]    pipe, str -'A'
    # @param[in]    data, Hw3dLutOffsetsValues, to set value for any register
    # @return       Hw3dlutInfo
    def get_hw3dlut_info(self, pipe: str, data: Hw3dLutOffsetsValues) -> Hw3dlutInfo:
        hw_3dlut_regs = self.get_3dlut_offsets(pipe)
        hwlut_ctl = REG_LUT_3D_CTL(hw_3dlut_regs.LutControl, data.LutControl)
        hwlut_data = REG_LUT_3D_DATA(hw_3dlut_regs.LutData, data.LutData)
        return Hw3dlutInfo(hwlut_ctl.Lut3DEnable, hwlut_ctl.NewLutReady, hwlut_data.Lut3DEntry)

    ##
    # @brief        Exposed API to get ColorCtl info for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    data, ColorCtlOffsetsValues, to set value for any register
    # @return       ColorCtlInfo
    def get_colorctl_info(self, pipe: str, data: ColorCtlOffsetsValues) -> ColorCtlInfo:
        color_ctl_regs = self.get_color_ctrl_offsets(pipe)
        pipe_misc_value = REG_PIPE_MISC(color_ctl_regs.PipeMisc, data.PipeMisc)
        pipe_misc2_value = REG_PIPE_MISC2(color_ctl_regs.PipeMisc2, data.PipeMisc2)
        csc_reg_value = REG_CSC_MODE(color_ctl_regs.CscMode, data.CscMode)
        gamma_mode_value = REG_GAMMA_MODE(color_ctl_regs.GammaMode, data.GammaMode)
        return ColorCtlInfo(pipe_misc_value.PipeOutputColorSpaceSelect,
                            pipe_misc_value.HdrMode, pipe_misc_value.PortOutputBpc, pipe_misc_value.DitheringEnable,
                            pipe_misc_value.DitheringType, pipe_misc_value.Yuv420Mode, pipe_misc_value.Yuv420Enable
                            , pipe_misc2_value.Yuv422Mode, csc_reg_value.PipeOutputCscEnable,
                            csc_reg_value.PipeCscEnable, csc_reg_value.PipeCscCC2Enable,
                            gamma_mode_value.GammaMode, gamma_mode_value.PreCscGammaEnable,
                            gamma_mode_value.PreCscCc2GammaEnable, gamma_mode_value.PostCscGammaEnable,
                            gamma_mode_value.PostCscCc2GammaEnable)

    ##
    # @brief        Exposed API to get Lace info for given pipe
    # @param[in]    pipe, str -'A'
    # @param[in]    data, LaceOffsetsValues, to set value for any register
    # @return       LaceInfo
    def get_lace_info(self, pipe: str, data: LaceOffsetsValues) -> LaceInfo:
        lace_regs = self.get_lace_offsets(pipe)
        lace_value = REG_DPLC_CTL(lace_regs.DplcControl, data.DplcControl)
        return LaceInfo(lace_value.FunctionEnable, lace_value.IeEnable, lace_value.FastAccessModeEnable)

    ##
    # @brief        Exposed API to get Transcoder Info for given Transcoder
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data, TransDDiOffsetsValues, to set value for any register
    # @return       TransDdiInfo
    def get_trans_ddi_info(self, transcoder: str, data: TransDDiOffsetsValues) -> TransDdiInfo:
        trans_ddi_regs = self.get_trans_ddi_offsets(transcoder)
        trans_ddi_value = REG_TRANS_DDI_FUNC_CTL(trans_ddi_regs.FuncCtrlReg, data.FuncCtrlReg)
        return TransDdiInfo(trans_ddi_value.BitsPerColor, trans_ddi_value.TransDdiModeSelect)

    ##
    # @brief        Exposed API to get Transcoder ctl2 Info for given Transcoder
    # @param[in]    transcoder, TranscoderType
    # @param[in]    data, TransDDiCtl2OffsetsValues, to set value for any register
    # @return       TransDdiCtl2Info
    def get_trans_ddi_ctl2_info(self, transcoder: str, data: TransDDiCtl2OffsetsValues) -> TransDdiCtl2Info:
        trans_ddi_regs = self.get_trans_ddi_ctl2_offsets(transcoder)
        trans_ddi_value = REG_TRANS_DDI_FUNC_CTL2(trans_ddi_regs.FuncCtrl2Reg, data.FuncCtrl2Reg)
        return TransDdiCtl2Info(trans_ddi_value.PortSyncModeMasterSelect, trans_ddi_value.PortSyncModeEnable)

    ##
    # @brief        Exposed API to get pipe csc coeff  for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    data, PipeCscCoeffOffsetValues, to set value for any register
    # @return       PipeCscCoeffInfo
    def get_pipe_csc_coeff_info(self, pipe: str, data: PipeCscCoeffOffsetValues) -> PipeCscCoeffInfo:
        reg_obj = []
        coeff_regs = self.get_pipe_csc_coeff_offsets(pipe)

        if all(value != '' for value in data.PipeCscCoeff):
            for index in range(0, len(data.PipeCscCoeff)):
                reg_obj.append(REG_CSC_COEFF(coeff_regs.PipeCscCoeff[index], [data.PipeCscCoeff[index]]))

        if all(value != '' for value in data.PipeOutputCscCoeff):
            for index in range(0, len(data.PipeOutputCscCoeff)):
                reg_obj.append(
                    REG_OUTPUT_CSC_COEFF(coeff_regs.PipeOutputCscCoeff[index], [data.PipeOutputCscCoeff[index]]))

        if all(value != '' for value in data.PipeCscCc2Coeff):
            for index in range(0, len(data.PipeCscCc2Coeff)):
                reg_obj.append(REG_CSC_CC2_COEFF(coeff_regs.PipeCscCc2Coeff[index], [data.PipeCscCc2Coeff[index]]))
        return PipeCscCoeffInfo(reg_obj)

    ##
    # @brief        Exposed API to get plane csc coeff  for given plane and pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @param[in]    data, PlaneCscCoeffOffsetValues, to set value for any register
    # @return       PlaneCscCoeffInfo
    def get_plane_csc_coeff_info(self, pipe: str, plane: str, data: PlaneCscCoeffOffsetValues) -> PlaneCscCoeffInfo:
        reg_obj = []

        coeff_regs = self.get_plane_csc_coeff_offsets(pipe, plane)
        if all(value == 0 for value in data.PlaneCscCoeff) is False:
            for index in range(0, len(data.PlaneCscCoeff)):
                reg_obj.append(REG_PLANE_CSC_COEFF(coeff_regs.PlaneCscCoeff[index], [data.PlaneCscCoeff[index]]))
        if all(value == 0 for value in data.PlaneInputCscCoeff) is False:
            for index in range(0, len(data.PlaneInputCscCoeff)):
                reg_obj.append(
                    REG_PLANE_INPUT_CSC_COEFF(coeff_regs.PlaneInputCscCoeff[index], [data.PlaneInputCscCoeff[index]]))
        return PlaneCscCoeffInfo(reg_obj)

    ##
    # @brief        Exposed API to get Plane ColorCtl info for given pipe and plane
    # @param[in]    plane, str -'A','B','C','D'
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       PlaneColorCtlInfo
    def get_plane_color_ctl_info(self, plane: str, pipe: str) -> PlaneColorCtlInfo:
        plane_color_ctl_regs = self.get_plane_color_ctl_offsets(plane, pipe)
        plane_color_ctl_value = read_register(plane_color_ctl_regs.PlaneColorCtl, self.gfx_index)
        plane_color_ctl = REG_PLANE_COLOR_CTL(plane_color_ctl_regs.PlaneColorCtl, plane_color_ctl_value)
        return PlaneColorCtlInfo(plane_color_ctl.PlaneGammaMode,
                                 plane_color_ctl.PlaneGammaDisable,
                                 plane_color_ctl.PlanePreCscGammaEnable,
                                 plane_color_ctl.PlaneInputCscEnable,
                                 plane_color_ctl.PlaneCscEnable,
                                 plane_color_ctl.YuvRangeCorrectionOutput,
                                 plane_color_ctl.YuvRangeCorrectionDisable,
                                 plane_color_ctl.RemoveYuvOffset
                                 )

    ##
    # @brief        Exposed API to get PlaneCtl info for given pipe and plane
    # @param[in]    plane, str -'A','B','C','D'
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       PlaneCtlInfo
    def get_plane_ctl_info(self, plane: str, pipe: str) -> PlaneCtlInfo:
        plane_ctl_regs = self.get_plane_ctl_offsets(plane, pipe)
        plane_ctl_value = read_register(plane_ctl_regs.PlaneCtl, self.gfx_index)
        plane_color_ctl = REG_PLANE_CTL(plane_ctl_regs.PlaneCtl, plane_ctl_value)
        return PlaneCtlInfo(plane_color_ctl.SourcePixelFormat)

    ##
    # @brief        Exposed API to get PlanePixelNormalizer info for given pipe and plane
    # @param[in]    plane, str -'A','B','C','D'
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       PlanePixelNormalizeInfo
    def get_plane_pixel_normalizer_info(self, plane: str, pipe: str) -> PlanePixelNormalizeInfo:
        plane_pixel_normalizer_regs = self.get_plane_pixel_normalizer_offsets(plane, pipe)
        plane_pixel_norm_value = read_register(plane_pixel_normalizer_regs.PlanePixelNormalize, self.gfx_index)
        plane_pixel_norm = REG_PLANE_PIXEL_NORMALIZE(plane_pixel_normalizer_regs.PlanePixelNormalize,
                                                     plane_pixel_norm_value)
        return PlanePixelNormalizeInfo(plane_pixel_norm.Enable, plane_pixel_norm.NormalizationFactor)

    # @brief        Exposed API to get Plane DeGamma Info for a given plane, pipe, gfx_index and lut_size
    # @param[in]    plane, str -'A','B','C','D' etc
    # @param[in]    pipe, str -'A','B','C','D' etc
    # @param[in]    lut_size, int - Size of the Degamma LUT to be fetched
    # @return       GammaDataInfo
    def get_plane_degamma_data_info(self, plane: str, pipe: str, lut_size: int) -> GammaDataInfo:
        lut_data = []
        if plane in (1, 2, 3):
            gamma_regs = self.get_plane_gamma_enh_offsets(plane, pipe)
            index_value = read_register(gamma_regs.PlanePreCSCGammaIndexEnh, self.gfx_index)
            gamma_value = REG_PLANE_PRE_CSC_GAMC_INDEX_ENH(gamma_regs.PlanePreCSCGammaIndexEnh, index_value)
            ##
            # Setting IndexAutoIncrement to 0 before reading the data registers
            gamma_value.IndexAutoIncrement = 0
            write_register(gamma_regs.PlanePreCSCGammaIndexEnh, gamma_value.value, self.gfx_index)
            for index in range(0, lut_size):
                gamma_value.IndexValue = index
                write_register(gamma_regs.PlanePreCSCGammaIndexEnh, gamma_value.value, self.gfx_index)
                data_value = read_register(gamma_regs.PlanePreCSCGammaDataEnh, self.gfx_index)
                data_reg1 = REG_PLANE_PRE_CSC_GAMC_DATA(gamma_regs.PlanePreCSCGammaDataEnh, data_value)
                lut_data.append(data_reg1.value)
        else:
            gamma_regs = self.get_plane_gamma_offsets(plane, pipe)
            index_value = read_register(gamma_regs.PlanePreCSCGammaIndex, self.gfx_index)
            gamma_value = REG_PLANE_PRE_CSC_GAMC_INDEX(gamma_regs.PlanePreCSCGammaIndex, index_value)
            ##
            # Setting IndexAutoIncrement to 0 before reading the data registers
            gamma_value.IndexAutoIncrement = 0
            write_register(gamma_regs.PlanePreCSCGammaIndex, gamma_value.value, self.gfx_index)
            for index in range(0, lut_size):
                gamma_value.IndexValue = index
                write_register(gamma_regs.PlanePreCSCGammaIndex, gamma_value.value, self.gfx_index)
                data_value = read_register(gamma_regs.PlanePreCSCGammaData, self.gfx_index)
                data_reg1 = REG_PLANE_PRE_CSC_GAMC_DATA(gamma_regs.PlanePreCSCGammaData, data_value)
                lut_data.append(data_reg1.value)

        return GammaDataInfo(lut_data)

    ##
    # @brief        Exposed API to get Pipe DeGamma Info for a given pipe, gfx_index and lut_size
    # @param[in]    pipe, str -'A','B','C','D' etc
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_pipe_degamma_data_info(self, pipe: str, lut_size: int) -> GammaDataInfo:
        return GammaDataInfo([])

    ##
    # @brief        Exposed API to get MutliSegment Pipe Gamma data for given pipe for all three channels
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_pipe_gamma_multi_segment_info(self, pipe: str, lut_size: int) -> GammaDataInfo:
        return GammaDataInfo([])

    ##
    # @brief        Exposed API to get Plane Gamma Info for a given plane, pipe, gfx_index and lut_size
    # @param[in]    plane, str -'A','B','C','D' etc
    # @param[in]    pipe, str -'A','B','C','D' etc
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_plane_gamma_data_info(self, plane: str, pipe: str, lut_size: int) -> GammaDataInfo:
        lut_data = []
        if plane in ('1', '2', '3'):
            gamma_regs = self.get_plane_gamma_enh_offsets(plane, pipe)
            index_value = read_register(gamma_regs.PlanePostCSCGammaIndexEnh, self.gfx_index)
            gamma_value = REG_PLANE_POST_CSC_GAMC_INDEX(gamma_regs.PlanePostCSCGammaIndexEnh, index_value)
            ##
            # Setting IndexAutoIncrement to 0 before reading the data registers
            gamma_value.IndexAutoIncrement = 0
            write_register(gamma_regs.PlanePostCSCGammaIndexEnh, gamma_value.value, self.gfx_index)
            for index in range(0, lut_size):
                gamma_value.IndexValue = index
                write_register(gamma_regs.PlanePostCSCGammaIndexEnh, gamma_value.value, self.gfx_index)
                data_value = read_register(gamma_regs.PlanePostCSCGammaDataEnh, self.gfx_index)
                data_reg1 = REG_PLANE_POST_CSC_GAMC_DATA(gamma_regs.PlanePostCSCGammaDataEnh, data_value)
                lut_data.append(data_reg1.value)
        else:
            gamma_regs = self.get_plane_gamma_offsets(plane, pipe)
            index_value = read_register(gamma_regs.PlanePostCSCGammaIndex, self.gfx_index)
            gamma_value = REG_PLANE_POST_CSC_GAMC_INDEX(gamma_regs.PlanePostCSCGammaIndex, index_value)
            ##
            # Setting IndexAutoIncrement to 0 before reading the data registers
            gamma_value.IndexAutoIncrement = 0
            write_register(gamma_regs.PlanePostCSCGammaIndex, gamma_value.value, self.gfx_index)
            for index in range(0, lut_size):
                gamma_value.IndexValue = index
                write_register(gamma_regs.PlanePostCSCGammaIndex, gamma_value.value, self.gfx_index)
                data_value = read_register(gamma_regs.PlanePostCSCGammaData, self.gfx_index)
                data_reg1 = REG_PLANE_POST_CSC_GAMC_DATA(gamma_regs.PlanePostCSCGammaData, data_value)
                lut_data.append(data_reg1.value)
        return GammaDataInfo(lut_data)

    ##
    # @brief        Exposed API to get Pipe DeGamma Info for a given pipe, gfx_index and lut_size
    # @param[in]    pipe, str -'A','B','C','D' etc
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_pipe_degamma_data_info_for_cc1(self, pipe: str, lut_size: int) -> GammaDataInfo:
        gamma_regs = self.get_pipe_gamma_offsets(pipe)

        index_value = read_register(gamma_regs.PreCSCGammaIndex, self.gfx_index)
        gamma_value = REG_PRE_CSC_GAMC_INDEX(gamma_regs.PreCSCGammaIndex, index_value)
        ##
        # Setting IndexAutoIncrement to 0 before reading the data registers
        gamma_value.IndexAutoIncrement = 0
        write_register(gamma_regs.PreCSCGammaIndex, gamma_value.value, self.gfx_index)

        lut_data = []
        for index in range(0, lut_size):
            gamma_value.IndexValue = index
            write_register(gamma_regs.PreCSCGammaIndex, gamma_value.value, self.gfx_index)
            data_value = read_register(gamma_regs.PreCSCGammaData, self.gfx_index)
            data_reg1 = REG_PRE_CSC_GAMC_DATA(gamma_regs.PreCSCGammaData, data_value)
            lut_data.append(data_reg1.value)

        return GammaDataInfo(lut_data)

    ##
    # @brief        Exposed API to get Pipe DeGamma Info for a given pipe, gfx_index and lut_size
    # @param[in]    pipe, str -'A','B','C','D' etc
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_pipe_degamma_data_info_for_cc2(self, pipe: str, lut_size: int) -> GammaDataInfo:
        gamma_regs = self.get_pipe_gamma_cc2_offsets(pipe)
        index_value = read_register(gamma_regs.PreCscCC2Index, self.gfx_index)
        gamma_value = REG_PRE_CSC_CC2_GAMC_INDEX(gamma_regs.PreCscCC2Index, index_value)
        ##
        # Setting IndexAutoIncrement to 0 before reading the data registers
        gamma_value.IndexAutoIncrement = 0
        write_register(gamma_regs.PreCscCC2Index, gamma_value.value, self.gfx_index)

        lut_data = []
        for index in range(0, lut_size):
            gamma_value.IndexValue = index
            write_register(gamma_regs.PreCscCC2Index, gamma_value.value, self.gfx_index)
            data_value = read_register(gamma_regs.PreCscCC2Data, self.gfx_index)
            data_reg1 = REG_PRE_CSC_CC2_GAMC_DATA(gamma_regs.PreCscCC2Data, data_value)
            lut_data.append(data_reg1.value)

        return GammaDataInfo(lut_data)

    ##
    # @brief        Exposed API to get PalPrecision Pipe Gamma data for given pipe for all three channels
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_pipe_pal_prec_data_info(self, pipe: str, lut_size: int) -> GammaDataInfo:
        return GammaDataInfo([])

    ##
    # @brief        Exposed API to get Pipe Gamma data for CC1 block for given pipe for all three channels
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_pipe_gamma_data_info_for_cc1(self, pipe: str, lut_size: int) -> GammaDataInfo:
        gamma_regs = self.get_pipe_gamma_offsets(pipe)

        index_value = read_register(gamma_regs.PalPrecIndex, self.gfx_index)
        gamma_value = REG_PAL_PREC_INDEX(gamma_regs.PalPrecIndex, index_value)
        ##
        # Setting IndexAutoIncrement to 0 before reading the data registers
        gamma_value.IndexAutoIncrement = 0
        write_register(gamma_regs.PalPrecIndex, gamma_value.value, self.gfx_index)

        lut_data = []
        for index in range(0, lut_size, 2):
            gamma_value.IndexValue = index
            write_register(gamma_regs.PalPrecIndex, gamma_value.value, self.gfx_index)
            data_value1 = read_register(gamma_regs.PalPrecData, self.gfx_index)

            gamma_value.IndexValue = index + 1
            write_register(gamma_regs.PalPrecIndex, gamma_value.value, self.gfx_index)
            data_value2 = read_register(gamma_regs.PalPrecData, self.gfx_index)

            data_reg1 = REG_PAL_PREC_DATA(gamma_regs.PalPrecData, data_value1)
            data_reg2 = REG_PAL_PREC_DATA(gamma_regs.PalPrecData, data_value2)
            lsb_blue = (data_reg1.BluePrecisionPaletteEntry & 0x3F0) >> 4
            msb_blue = data_reg2.BluePrecisionPaletteEntry & 0x3FF

            blue_value = (msb_blue << 6) | lsb_blue
            lut_data.append(blue_value)

            lsb_green = (data_reg1.GreenPrecisionPaletteEntry & 0x3F0) >> 4
            msb_green = data_reg2.GreenPrecisionPaletteEntry & 0x3FF
            green_value = (msb_green << 6) | lsb_green
            lut_data.append(green_value)

            lsb_red = (data_reg1.RedPrecisionPaletteEntry & 0x3F0) >> 4
            msb_red = data_reg2.RedPrecisionPaletteEntry & 0x3FF
            red_value = (msb_red << 6) | lsb_red
            lut_data.append(red_value)

        return GammaDataInfo(lut_data)

    ##
    # @brief        Exposed API to get trans msa misc info for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    data, Trans, to get value for any register
    # @return       MsaMiscInfo
    def get_trans_msa_misc_info(self, pipe: str, data: TransMsaMiscOffsetsValues) -> MsaMiscInfo:
        trans_msa_misc_regs: TransMsaMiscOffsets = self.get_trans_msa_misc_offset(pipe)
        msa_misc_data = REG_TRANS_MSA_MISC(trans_msa_misc_regs.MsaMiscOffset, data.MsaMiscOffset)
        return MsaMiscInfo(msa_misc_data.MsaMisc1)

    ##
    # @brief        Exposed API to get PalPrecision Pipe Gamma data for given pipe for all three channels
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    lut_size, int - Size of the gamma LUT to be fetched
    # @return       GammaDataInfo
    def get_pipe_gamma_data_info_for_cc2(self, pipe: str, lut_size: int) -> GammaDataInfo:
        gamma_regs = self.get_pipe_gamma_cc2_offsets(pipe)
        index_value = read_register(gamma_regs.PostCscCC2Index, self.gfx_index)
        gamma_value = REG_POST_CSC_CC2_INDEX(gamma_regs.PostCscCC2Index, index_value)
        ##
        # Setting IndexAutoIncrement to 0 before reading the data registers
        gamma_value.IndexAutoIncrement = 0
        write_register(gamma_regs.PostCscCC2Index, gamma_value.value, self.gfx_index)

        lut_data = []
        for index in range(0, lut_size, 2):
            gamma_value.IndexValue = index
            write_register(gamma_regs.PostCscCC2Index, gamma_value.value, self.gfx_index)
            data_value1 = read_register(gamma_regs.PostCscCC2Data, self.gfx_index)

            gamma_value.IndexValue = index + 1
            write_register(gamma_regs.PostCscCC2Index, gamma_value.value, self.gfx_index)
            data_value2 = read_register(gamma_regs.PostCscCC2Data, self.gfx_index)

            data_reg1 = REG_PAL_PREC_DATA(gamma_regs.PostCscCC2Data, data_value1)
            data_reg2 = REG_PAL_PREC_DATA(gamma_regs.PostCscCC2Data, data_value2)

            lsb_blue = (data_reg1.BluePrecisionPaletteEntry & 0x3F0) >> 4
            msb_blue = data_reg2.BluePrecisionPaletteEntry & 0x3FF
            blue_value = (msb_blue << 6) | lsb_blue
            lut_data.append(blue_value)

            lsb_green = (data_reg1.GreenPrecisionPaletteEntry & 0x3F0) >> 4
            msb_green = data_reg2.GreenPrecisionPaletteEntry & 0x3FF
            green_value = (msb_green << 6) | lsb_green
            lut_data.append(green_value)

            lsb_red = (data_reg1.RedPrecisionPaletteEntry & 0x3F0) >> 4
            msb_red = data_reg2.RedPrecisionPaletteEntry & 0x3FF
            red_value = (msb_red << 6) | lsb_red
            lut_data.append(red_value)

        return GammaDataInfo(lut_data)

    ##
    # @brief        Exposed API to get Extension Pipe Gamma data for given pipe for all three channels
    # @param[in]    pipe, str -'CC2_A','CC2_B'
    # @return       GammaDataInfo
    def get_pipe_gamma_ext_reg_cc2_info(self, pipe: str) -> GammaDataInfo:
        gamma_regs = self.get_pipe_gamma_cc2_offsets(pipe)
        ext_lut_data = []
        ##
        # PAL_GC_MAX
        pal_gc_max_base_offset = gamma_regs.PalGCMaxData
        for index in range(0, 3):
            pal_gc_max_data_value = read_register(pal_gc_max_base_offset, self.gfx_index)
            gamma_mode_value = REG_PAL_GC_MAX(pal_gc_max_base_offset, [pal_gc_max_data_value])
            ext_lut_data.append(gamma_mode_value.RedMaxGcPoint)
            pal_gc_max_base_offset += 4
        return GammaDataInfo(ext_lut_data)

    ##
    # @brief        Exposed API to get Extension Pipe Gamma data for given pipe for all three channels
    # @param[in]    pipe, str -'A','B','C','D'
    # @return       GammaDataInfo
    def get_pipe_gamma_ext_reg_info(self, pipe: str) -> GammaDataInfo:
        gamma_regs = self.get_pipe_gamma_offsets(pipe)
        ext_lut_data = []
        ##
        # PAL_GC_MAX
        pal_gc_max_base_offset = gamma_regs.PalGCMaxData
        for index in range(0, 3):
            pal_gc_max_data_value = read_register(pal_gc_max_base_offset, self.gfx_index)
            gamma_mode_value = REG_PAL_GC_MAX(pal_gc_max_base_offset, [pal_gc_max_data_value])
            ext_lut_data.append(gamma_mode_value.RedMaxGcPoint)
            pal_gc_max_base_offset += 4

        ##
        # PAL_GC_EXT_MAX
        pal_gc_ext_max_base_offset = gamma_regs.PalExtGCMaxData
        for index in range(0, 3):
            pal_gc_ext_max_data_value = read_register(pal_gc_ext_max_base_offset, self.gfx_index)
            gamma_mode_value = REG_PAL_EXT_GC_MAX(pal_gc_ext_max_base_offset, [pal_gc_ext_max_data_value])
            ext_lut_data.append(gamma_mode_value.RedExtMaxGcPoint)
            pal_gc_ext_max_base_offset += 4

        ##
        # PAL_GC_EXT2_MAX
        pal_gc_ext2_max_base_offset = gamma_regs.PalExt2GCMaxData
        for index in range(0, 3):
            pal_ext2_gc_max_data_value = read_register(pal_gc_ext2_max_base_offset, self.gfx_index)
            gamma_mode_value = REG_PAL_EXT2_GC_MAX(pal_gc_ext2_max_base_offset, [pal_ext2_gc_max_data_value])
            ext_lut_data.append(gamma_mode_value.RedExtMaxGcPoint)
            pal_gc_ext2_max_base_offset += 4

        return GammaDataInfo(ext_lut_data)

    ##
    # @brief        Exposed API to get avi info for given plane and pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @param[in]    data, AviInfoOffsetsValues, to set value for any register
    # @return       AviInfo
    def get_avi_info(self, plane: str, pipe: str, data: AviInfoOffsetsValues) -> AviInfo:
        avi_info_offsets = self.get_avi_info_offsets(plane, pipe)
        avi_dip_data = REG_VIDEO_DIP_DATA(avi_info_offsets.QuantRange, data.QuantRange)
        video_dip_ctl = REG_VIDEO_DIP_CTL(avi_info_offsets.videoDipCtl, data.videoDipCtl)
        return AviInfo(avi_dip_data.VideoDipData,video_dip_ctl.VdipEnableAvi, video_dip_ctl.VdipEnableVsc)

    ##
    # @brief        Exposed API to get avi info for given plane and pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @param[in]    data, VscSdpDataOffsetsValues, to set value for any register
    # @return       VscSdpData
    def get_vsc_sdp_data(self, plane: str, pipe: str, data: VscSdpDataOffsetsValues) -> VscSdpData:
        vsc_sdp_offsets = self.get_vsc_sdp_offsets(plane, pipe)
        vsc_sdp_data = REG_VIDEO_DIP_DATA(vsc_sdp_offsets.QuantRange, data.QuantRange)
        return VscSdpData(vsc_sdp_data.VideoDipData)

    ##
    # @brief        Exposed API to get pipe csc pre and post offset values for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    data, PipeCscPrePostOffsetValues, to set value for any register
    # @return       PipeCscPrePostOffInfo
    def get_pipe_csc_pre_post_offset_info(self, pipe: str, data: PipeCscPrePostOffsetValues) -> PipeCscPrePostOffInfo:
        reg_obj = []
        offset_regs = self.get_pipe_csc_pre_post_offsets(pipe)

        if all(value != '' for value in data.PipeCscPreOff):
            for index in range(0, len(data.PipeCscPreOff)):
                reg_obj.append(
                    REG_CSC_PREOFF(offset_regs.PipeCscPreOff[index], [data.PipeCscPreOff[index]]).PrecscHighOffset)

        if all(value != '' for value in data.PipeCscPostOff):
            for index in range(0, len(data.PipeCscPostOff)):
                reg_obj.append(
                    REG_CSC_POSTOFF(offset_regs.PipeCscPostOff[index], [data.PipeCscPostOff[index]]).PostcscHighOffset)

        # todo : Currently OutputCSCPreOff is not present in the autogen Gen*PipeRegs.py . Once  fixed will uncomment this
        # if all(value != '' for value in data.PipeOutputCscPreOff):
        #    for index in range(0, len(data.PipeOutputCscPreOff)):
        #        reg_obj.append(REG_OUTPUT_CSC_PREOFF(offset_regs.PipeOutputCscPreOff[index],
        #                                              data.PipeOutputCscPreOff[index]).PrecscHighOffset)

        if all(value != '' for value in data.PipeOutputCscPostOff):
            for index in range(0, len(data.PipeOutputCscPostOff)):
                reg_obj.append(REG_OUTPUT_CSC_POSTOFF(offset_regs.PipeOutputCscPostOff[index],
                                                      [data.PipeOutputCscPostOff[index]]).PostcscHighOffset)

        return PipeCscPrePostOffInfo(reg_obj)

    ##
    # @brief        Exposed API to get plane csc pre and post offset values for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @param[in]    data, PlaneCscPrePostOffsetValues, to set value for any register
    # @return       PlaneCscPrePostOffInfo
    def get_plane_csc_pre_post_offset_info(self, pipe: str, plane: str,
                                           data: PlaneCscPrePostOffsetValues) -> PlaneCscPrePostOffInfo:
        reg_obj = []
        offset_regs = self.get_plane_csc_pre_post_offsets(plane, pipe)

        if all(value != '' for value in data.PlaneCscPreOff):
            for index in range(0, len(data.PlaneCscPreOff)):
                reg_obj.append(
                    REG_PLANE_CSC_PREOFF(offset_regs.PlaneCscPreOff[index],
                                         [data.PlaneCscPreOff[index]]).PrecscHighOffset)

        if all(value != '' for value in data.PlaneCscPostOff):
            for index in range(0, len(data.PlaneCscPostOff)):
                reg_obj.append(
                    REG_PLANE_CSC_POSTOFF(offset_regs.PlaneCscPostOff[index],
                                          [data.PlaneCscPostOff[index]]).PostcscHighOffset)

        if all(value != '' for value in data.PlaneInputCscPreOff):
            for index in range(0, len(data.PlaneInputCscPreOff)):
                reg_obj.append(
                    REG_PLANE_INPUT_CSC_PREOFF(offset_regs.PlaneInputCscPreOff[index],
                                               [data.PlaneInputCscPreOff[index]]).PrecscHighOffset)

        if all(value != '' for value in data.PlaneInputCscPostOff):
            for index in range(0, len(data.PlaneInputCscPostOff)):
                reg_obj.append(REG_PLANE_INPUT_CSC_POSTOFF(offset_regs.PlaneInputCscPostOff[index],
                                                           [data.PlaneInputCscPostOff[index]]).PostcscHighOffset)

        return PlaneCscPrePostOffInfo(reg_obj)

    ##
    # @brief        Exposed API to get pipe frame counter info for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    data, PipeFrameCtrOffsetValues, to get value for any register
    # @return       PipeFrameCtrInfo
    def get_pipe_frame_ctr_info(self, pipe: str, data: PipeFrameCtrOffsetValues) -> PipeFrameCtrInfo:
        pipe_frame_ctr_regs: PipeFrameCtrOffsets = self.get_pipe_frame_ctr_offsets(pipe)
        pipe_frame_ctr = REG_PIPE_FRMCNT(pipe_frame_ctr_regs.pipe_frm_cntr_offset, data.pipe_frm_cntr_offset)
        pipe_frame_ctr_incr = REG_PIPE_FRMCNT(pipe_frame_ctr_regs.pipe_frm_cntr_incr, data.pipe_frm_cntr_incr)
        return PipeFrameCtrInfo(pipe_frame_ctr.PipeFrameCounter, pipe_frame_ctr_incr.PipeFrameCounter)

    ##
    # @brief        Exposed API to get pipe frame counter info for given pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    data, PipeFrameCtrOffsetValues, to get value for any register
    # @return       PipeFrameCtrInfo
    def get_video_dip_info(self, pipe: str, data: VideoDipCtlOffsetsValues) -> VideoDipCtlInfo:
        video_dip_regs: VideoDipCtlOffsets = self.get_video_dip_ctl_offset(pipe)
        video_dip_data = REG_VIDEO_DIP_CTL(video_dip_regs.VideoDipOffset, data.VideoDipOffset)
        return VideoDipCtlInfo(video_dip_data.VdipEnableVsc, video_dip_data.VscSelect)


    ##
    # @brief        Exposed API to get DC6v info
    # @param[in]    data[optional], Dc6vOffsetValues Type
    # @return       Dc6vInfo
    def get_dc6v_info(self, data: Dc6vOffsetValues = None) -> Dc6vInfo:
        regs = self.get_dc6v_offsets()
        if data is not None:
            scanline_gb = REG_SCANLINE_GB1(regs.GuardBand, [data.GuardBand])
            dc6v_line_time = REG_WM_LINETIME_DC6V(regs.LineTimeDc6v, data.LineTimeDc6v)
            restore_time = REG_DC6V_RESTORE_TIME(regs.RestoreProgrammingTime, data.RestoreProgrammingTime)
        else:
            scanline_gb = REG_SCANLINE_GB1(regs.GuardBand, [read_register(regs.GuardBand, self.gfx_index)])
            dc6v_line_time = REG_WM_LINETIME_DC6V(regs.LineTimeDc6v, read_register(regs.LineTimeDc6v, self.gfx_index))
            restore_time = REG_DC6V_RESTORE_TIME(regs.RestoreProgrammingTime,
                                                 read_register(regs.RestoreProgrammingTime, self.gfx_index))

        return Dc6vInfo(scanline_gb.Lowerboundguardband1, scanline_gb.Upperboundguardband1,
                        restore_time.RestoreProgrammingTime, dc6v_line_time.Linetime)

    # @brief        Exposed API to get avi info for given plane and pipe
    # @param[in]    pipe, str -'A','B','C','D'
    # @param[in]    plane, str - '1','2','3','4','5','6','7'
    # @param[in]    data, , to set value for any register
    # @return       PipeScalerInfo
    def get_scaler_info(self,plane:str,pipe:str,data: ScalerOffsetsValues) -> ScalerInfo:
        scaler_offsets = self.get_scaler_offsets(plane, pipe)
        scaler_data_1 = REG_PS_CTRL(scaler_offsets.scaler_offset_1,data.scaler_offset_1)
        scaler_data_2 = REG_PS_CTRL(scaler_offsets.scaler_offset_2,data.scaler_offset_2)
        return ScalerInfo(scaler_data_1.EnableScaler,scaler_data_2.EnableScaler,scaler_data_1.ScalerBinding,scaler_data_2.ScalerBinding)

    ##
    # @brief        Exposed API to get dcstate info
    # @param[in]    data[optional], DCStateOffsetsValues, to set value for any register
    # @return       DcStateInfo
    def get_dcstate_info(self, data: DCStateOffsetsValues = None) -> DcStateInfo:
        regs = self.get_dcstate_offsets()

        if data is not None:
            dc_state_en = REG_DC_STATE_EN(regs.DcStateEnable, data.DcStateEnable)
        else:
            dc_state_en = REG_DC_STATE_EN(regs.DcStateEnable, read_register(regs.DcStateEnable, self.gfx_index))

        return DcStateInfo(dc_state_en.Dc9Allow, dc_state_en.DynamicDcStateEnable == 2,
                           dc_state_en.DynamicDcStateEnable == 1, dc_state_en.DynamicDcStateEnable == 3,
                           dc_state_en.DisplayClockOffEnableEdp, 0, 0)

    ##
    # @brief        Exposed API to get interrupt info
    # @param[in]    data, , to set value for any register
    # @return       InterruptInfo
    def get_interrupt_info(self, data: InterruptOffsetValues = None) -> InterruptInfo:
        regs = self.get_interrupt_offsets()

        if data is not None:
            interrupt = REG_DE_PORT_INTERRUPT_DEFINITION(regs.InterruptIIR, data.InterruptIIR)
        else:
            interrupt = REG_DE_PORT_INTERRUPT_DEFINITION(regs.InterruptIIR, read_register(regs.InterruptIIR,
                                                                                          self.gfx_index))

        return InterruptInfo(0, 0, 0, 0, 0, 0, interrupt.Cmtg0DelayedVblank, interrupt.Cmtg0Vblank,
                             interrupt.Cmtg0Vsync, 0, 0, 0)

    ##
    # @brief        Exposed API to get ALPM info
    # @param[in]    data[optional], ALPMOffsetsValues, to set value for any register
    # @return       ALPMInfo
    def get_alpm_info(self,pipe:str, data: ALPMOffsetsValues = None) -> ALPMInfo:
        regs = self.get_ALPM_offsets(pipe)
        if data is not None:
            alpm_data = REG_ALPM_CTL(regs.ALPMCTL, data.ALPMCTL)
        else:
            alpm_data = REG_ALPM_CTL(regs.ALPMCTL, read_register(regs.ALPMCTL, self.gfx_index))

        return ALPMInfo(alpm_data.ExtendedFastWakeEnable,
                        alpm_data.LinkOffBetweenFramesEnable, alpm_data.AlpmAuxLessEnable, alpm_data.AlpmEnable)

    ##
    # @brief        Exposed API to get Audio Control offsets for given pipe
    # @param[in]    pipe, PipeType
    # @return       AudDP2CtlOffsets
    def get_audio_ctl_offsets(self, pipe: PipeType) -> AudDP2CtlOffsets:
        pass