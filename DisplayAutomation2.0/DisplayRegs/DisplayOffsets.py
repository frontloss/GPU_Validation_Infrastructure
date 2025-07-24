########################################################################################################################
# @file         DisplayOffsets.py
# @brief        Dataclasses for register offsets
#
# @author       Rohit Kumar
########################################################################################################################

from dataclasses import dataclass, field
from typing import List


########################################################################################################################
# Transcoder
########################################################################################################################


@dataclass
class PsrOffsets:
    SrdCtlReg: int = 0
    SrdStatusReg: int = 0
    PsrMaskReg: int = 0
    Psr2CtrlReg: int = 0
    Psr2StatusReg: int = 0
    Psr2ManTrkCtrlReg: int = 0
    Psr2ManTrkChickenReg: int = 0


@dataclass
class PsrOffsetValues(PsrOffsets):
    pass


@dataclass
class TimingOffsets:
    HTotal: int = 0
    HBlank: int = 0
    HSync: int = 0
    VTotal: int = 0
    VBlank: int = 0
    VSync: int = 0
    VSyncShift: int = 0
    DataM: int = 0
    DataN: int = 0
    LinkM: int = 0
    LinkN: int = 0


@dataclass
class TimingOffsetValues(TimingOffsets):
    pass


@dataclass
class VrrOffsets:
    VrrControl: int = 0
    VrrVmaxReg: int = 0
    VrrVminReg: int = 0
    VrrStatus: int = 0
    VrrPush: int = 0
    VrrFlipLine: int = 0
    VrrVTotal: int = 0
    PipeDmcScanlineUpper: int = 0
    VrrDcbVmaxReg: int = 0
    VrrDcbFlipLine: int = 0

@dataclass
class VrrOffsetValues(VrrOffsets):
    pass


@dataclass
class EmpOffsets:
    EmpControl: int = 0
    EmpHeader: int = 0
    EmpData: int = 0
    EmpAsSdpTl: int = 0


@dataclass
class EmpOffsetValues(EmpOffsets):
    pass


@dataclass
class TransDDiOffsets:
    FuncCtrlReg: int = 0


@dataclass
class TransDDiOffsetsValues(TransDDiOffsets):
    pass

@dataclass
class TransDDiCtl2Offsets:
    FuncCtrl2Reg: int = 0

@dataclass
class TransDDiCtl2OffsetsValues(TransDDiCtl2Offsets):
    pass

@dataclass
class PlaneColorCtlOffsets:
    PlaneColorCtl: int = 0


@dataclass
class PlaneColorCtlOffsetsValues(PlaneColorCtlOffsets):
    pass


@dataclass
class PlaneCtlOffsets:
    PlaneCtl: int = 0


@dataclass
class PlaneCtlOffsetsValues(PlaneCtlOffsets):
    pass


@dataclass
class PlanePixelNormalizerOffsets:
    PlanePixelNormalize: int = 0


@dataclass
class PlanePixelNormalizerOffsetsValues(PlanePixelNormalizerOffsets):
    pass


@dataclass
class ScalerOffsets:
    scaler_offset_1: int = 0
    scaler_offset_2: int = 0


@dataclass
class ScalerOffsetsValues(ScalerOffsets):
    pass


@dataclass
class PlaneGammaOffsets:
    ##
    # Gamma Index Registers
    PlanePreCSCGammaIndex: int = 0
    PlanePreCSCGammaIndexEnh: int = 0
    PlanePostCSCGammaIndex: int = 0

    ##
    # Gamma Data Registers
    PlanePreCSCGammaData: int = 0
    PlanePreCSCGammaDataEnh: int = 0
    PlanePostCSCGammaData: int = 0


@dataclass
class PlaneGammaOffsetValues(PlaneGammaOffsets):
    pass


@dataclass
class PipeFrameCtrOffsets:
    pipe_frm_cntr_offset: int = 0
    pipe_frm_cntr_incr: int = 0


@dataclass
class PipeFrameCtrOffsetValues(PipeFrameCtrOffsets):
    pass

@dataclass
class VideoDipCtlOffsets:
    VideoDipOffset: int=0

@dataclass
class VideoDipCtlOffsetsValues(VideoDipCtlOffsets):
    pass

@dataclass
class TransMsaMiscOffsets:
    MsaMiscOffset: int=0

@dataclass
class TransMsaMiscOffsetsValues(TransMsaMiscOffsets):
    pass



@dataclass
class CmtgOffsets:
    CmtgControlReg: int = 0
    CmtgHTotalReg: int = 0
    CmtgHBlankReg: int = 0
    CmtgHSyncReg: int = 0
    CmtgVTotalReg: int = 0
    CmtgVBlankReg: int = 0
    CmtgVSyncReg: int = 0
    CmtgLinkMReg: int = 0
    CmtgLinkNReg: int = 0
    DdiFunctionControlReg: int = 0
    CmtgContextLatency: int = 0


@dataclass
class CmtgOffsetValues(CmtgOffsets):
    pass


@dataclass
class Dc6vOffsets:
    GuardBand: int = 0
    RestoreProgrammingTime: int = 0
    LineTimeDc6v: int = 0


@dataclass
class Dc6vOffsetValues(Dc6vOffsets):
    pass


########################################################################################################################
# PIPE
########################################################################################################################
@dataclass
class DpstOffsets:
    DpstControl: int = 0
    DpstGuard: int = 0
    DpstBin: int = 0


@dataclass
class DpstOffsetValues(DpstOffsets):
    pass


@dataclass
class Hw3dLutOffsets:
    LutControl: int = 0
    LutData: int = 0
    LutIndex: int = 0


@dataclass
class Hw3dLutOffsetsValues(Hw3dLutOffsets):
    pass


@dataclass
class LaceOffsets:
    DplcControl: int = 0


@dataclass
class LaceOffsetsValues(LaceOffsets):
    pass


@dataclass
class ColorCtlOffsets:
    PipeMisc: int = 0
    PipeMisc2: int = 0
    CscMode: int = 0
    GammaMode: int = 0


@dataclass
class ColorCtlOffsetsValues(ColorCtlOffsets):
    pass


@dataclass
class AviInfoOffsets:
    QuantRange: int = 0
    videoDipCtl: int = 0


@dataclass
class AviInfoOffsetsValues(AviInfoOffsets):
    pass

@dataclass
class VscSdpDataOffsets:
    QuantRange: int = 0


@dataclass
class VscSdpDataOffsetsValues(VscSdpDataOffsets):
    pass

@dataclass
class PipeCscCoeffOffsets:
    PipeCscCoeff: List[int] = field(default_factory=list)
    PipeOutputCscCoeff: List[int] = field(default_factory=list)
    PipeCscCc2Coeff: List[int] = field(default_factory=list)


@dataclass
class PipeCscCoeffOffsetValues(PipeCscCoeffOffsets):
    pass


@dataclass
class PlaneCscCoeffOffsets:
    PlaneInputCscCoeff: List[int] = field(default_factory=list)
    PlaneCscCoeff: List[int] = field(default_factory=list)


@dataclass
class PlaneCscCoeffOffsetValues(PlaneCscCoeffOffsets):
    pass


@dataclass
class PlaneGammaOffsets:

    PlanePreCSCGammaIndex: int = 0
    PlanePreCSCGammaData: int = 0

    PlanePostCSCGammaIndex: int = 0
    PlanePostCSCGammaData: int = 0


@dataclass
class PlaneGammaOffsetValues(PlaneGammaOffsets):
    pass


@dataclass
class PlaneGammaEnhOffsets:
    PlanePreCSCGammaIndexEnh: int = 0
    PlanePreCSCGammaDataEnh: int = 0

    PlanePostCSCGammaIndexEnh: int = 0
    PlanePostCSCGammaDataEnh: int = 0


@dataclass
class PlaneGammaEnhOffsetValues(PlaneGammaEnhOffsets):
    pass


@dataclass
class PipeCscPrePostOffsets:
    PipeCscPreOff: List[int] = field(default_factory=list)
    PipeCscPostOff: List[int] = field(default_factory=list)
    # todo : Currently OutputCSCPreOff is not present in the autogen Gen*PipeRegs.py . Once  fixed will uncomment this
    # PipeOutputCscPreOff: List[int] = field(default_factory=list)
    PipeOutputCscPostOff: List[int] = field(default_factory=list)


@dataclass
class PipeCscPrePostOffsetValues(PipeCscPrePostOffsets):
    pass


@dataclass
class PlaneCscCoeffOffsets:
    PlaneCscCoeff: List[int] = field(default_factory=list)
    PlaneInputCscCoeff: List[int] = field(default_factory=list)


@dataclass
class PlaneCscCoeffOffsetValues(PlaneCscCoeffOffsets):
    pass

@dataclass
class PipeGammaOffsetsCC2:
    PalGCMaxData: int = 0
    PreCscCC2Index: int = 0
    PreCscCC2Data: int = 0
    PostCscCC2Index: int = 0
    PostCscCC2Data: int = 0

@dataclass
class PipeGammaOffsets:
    ##
    # Index Offsets
    PreCSCGammaIndex: int = 0
    PreCSCGammaData: int = 0

    PalPrecMultiSegmentIndex: int = 0
    PalPrecMultiSegmentData: int = 0

    PalPrecIndex: int = 0
    PalPrecData: int = 0

    PreCscCC2Index: int = 0
    PreCscCC2Data: int = 0

    PostCscCC2Index: int = 0
    PostCscCC2Data: int = 0

    PalGCMaxData: int = 0
    PalExtGCMaxData: int = 0
    PalExt2GCMaxData: int = 0

@dataclass
class PipeGammaCC2Offsets:
    ##
    # Index Offsets
    PreCscCC2Index: int = 0
    PreCscCC2Data: int = 0

    PostCscCC2Index: int = 0
    PostCscCC2Data: int = 0


@dataclass
class PipeGammaOffsetValues(PipeGammaOffsets):
    pass


@dataclass
class PlaneCscPrePostOffsets:
    PlaneCscPreOff: List[int] = field(default_factory=list)
    PlaneCscPostOff: List[int] = field(default_factory=list)
    PlaneInputCscPreOff: List[int] = field(default_factory=list)
    PlaneInputCscPostOff: List[int] = field(default_factory=list)


@dataclass
class PlaneCscPrePostOffsetValues(PlaneCscPrePostOffsets):
    pass


@dataclass
class MetadataOffsets:
    VideoDipDRMData: int = 0
    VideoDipGMPData: int = 0
    VscExtSdpCtl: int = 0
    VscExtSdpData: int = 0


@dataclass
class InterruptOffsets:
    InterruptISR: int = 0
    InterruptIMR: int = 0
    InterruptIIR: int = 0
    InterruptIER: int = 0


@dataclass
class InterruptOffsetValues(InterruptOffsets):
    pass


@dataclass
class DCStateOffsets:
    DcStateEnable: int = 0


@dataclass
class DCStateOffsetsValues(DCStateOffsets):
    pass


@dataclass
class ALPMOffsets:
    ALPMCTL: int = 0


@dataclass
class ALPMOffsetsValues(ALPMOffsets):
    pass


@dataclass
class VideoDataIslandPacketPPSOffsets:
    PPS0: int = 0
    PPS1: int = 0
    PPS2: int = 0
    PPS3: int = 0
    PPS4: int = 0
    PPS5: int = 0
    PPS6: int = 0
    PPS7: int = 0
    PPS8: int = 0
    PPS9: int = 0
    PPS10: int = 0
    PPS11: int = 0
    PPS12: int = 0
    PPS13: int = 0
    PPS14: int = 0
    PPS15: int = 0
    PPS16: int = 0
    PPS17: int = 0
    PPS18: int = 0
    PPS19: int = 0
    PPS20: int = 0
    PPS21: int = 0
    PPS22: int = 0
    PPS23: int = 0
    PPS24: int = 0
    PPS25: int = 0
    PPS26: int = 0
    PPS27: int = 0
    PPS28: int = 0
    PPS29: int = 0
    PPS30: int = 0
    PPS31: int = 0
    PPS32: int = 0


@dataclass
class VideoDataIslandPacketPPSValues(VideoDataIslandPacketPPSOffsets):
    pass


@dataclass
class AudDP2CtlOffsets:
    AudDP2CtlOffset: int = 0


@dataclass
class AudDP2CtlOffsetsValues(AudDP2CtlOffsets):
    pass
