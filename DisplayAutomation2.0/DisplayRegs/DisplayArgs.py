########################################################################################################################
# @file         DisplayArgs.py
# @brief        Contains common structures used in DisplayRegsInterface as well as tests
#
# @author       Rohit Kumar
########################################################################################################################

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from Libs.Core.sw_sim import driver_interface


########################################################################################################################
# Common Enum classes
# This classes will be used to identify the register set based on trancoder or pipe etc.
########################################################################################################################
class TranscoderType(Enum):
    TRANSCODER_EDP = 0
    TRANSCODER_A = 1
    TRANSCODER_B = 2
    TRANSCODER_C = 3
    TRANSCODER_D = 4
    TRANSCODER_DSI0 = 5
    TRANSCODER_DSI1 = 6
    TRANSCODER_CMTG = 7
    TRANSCODER_NULL = 8


class PipeType(Enum):
    PIPE_A = 0
    PIPE_B = 1
    PIPE_C = 2
    PIPE_D = 3
    PIPE_NULL = 4


class PlaneType(Enum):
    PLANE_1 = 1
    PLANE_2 = 2
    PLANE_3 = 3
    PLANE_4 = 4
    PLANE_5 = 5
    PLANE_6 = 6
    PLANE_7 = 7


########################################################################################################################
# Transcoder Data
########################################################################################################################
@dataclass
class VrrInfo:
    VrrVmin: int = 0
    VrrVmax: int = 0
    VrrFlipLine: int = 0
    VrrEnable: bool = False
    FlipLineEnable: bool = False
    VrrEnableLive: bool = False
    PushEnable: bool = False
    SendPush: bool = False
    VrrGuardband: int = 0
    PipeDmcScanlineUpper: int = 0
    VrrDcbVmax: int = 0
    VrrDcbFlipLine: int = 0


@dataclass
class EmpInfo:
    EmpType: int = 0
    Hb0Spare: int = 0
    DsType: int = 0
    NumOfPackets: int = 0
    End: int = 0
    EmpData: int = 0
    EmpAsSdpTl: int = 0



@dataclass
class PsrInfo:
    SrdEnable: bool = False
    Psr2Enable: bool = False
    Psr2DeepSleep: bool = False
    SFPartialFrameEnable: bool = False
    Psr2ManualTrackingEnable: bool = False
    SelectiveFetchPlaneEnable: bool = False
    IdleFrames: int = 0
    Psr2StateIdle: bool = False


@dataclass
class TimingsInfo:
    HTotal: int = 0
    HActive: int = 0
    VTotal: int = 0
    VActive: int = 0
    LinkM: int = 0
    VBlankStart: int = 0
    VSyncStart: int = 0


@dataclass
class TransDdiInfo:
    BitsPerColor: int = 0
    DdiModeSelect: int = 0


@dataclass
class TransDdiCtl2Info:
    PortSyncModeMasterSelect: int = 0
    PortSyncModeEnable: int = 0


########################################################################################################################
# Pipe Data
########################################################################################################################
@dataclass
class DpstInfo:
    IEHistogramEnable: bool = False
    HistogramInterruptEnable: bool = False
    HistogramEventStatus: bool = False


@dataclass
class Hw3dlutInfo:
    Lut3DEnable: int = 0
    NewLutReady: int = 0
    Lut3Ddata: int = 0


@dataclass
class ColorCtlInfo:
    PipeOutputColorSpaceSelect: int = 0
    HdrMode: int = 0
    DitheringBpc: int = 0
    DitheringEnable: int = 0
    DitheringType: int = 0
    Yuv420Mode: int = 0
    Yuv420Enable: int = 0
    Yuv422Mode: int = 0
    PipeOutputCscEnable: int = 0
    PipeCscEnable: int = 0
    PipeCscCC2Enable: int = 0
    GammaMode: int = 0
    PreCscGammaEnable: int = 0
    PreCscCc2GammaEnable: int = 0
    PostCscGammaEnable: int = 0
    PostCscCc2GammaEnable: int = 0


@dataclass
class PlaneColorCtlInfo:
    PlaneGammaMode: int = 0
    PlaneGammaDisable: int = 0
    PlanePreCscGammaEnable: int = 0
    PlaneInputCscEnable: int = 0
    PlaneCscEnable: int = 0
    YuvRangeCorrectionOutput: int = 0
    YuvRangeCorrectionDisable: int = 1
    RemoveYuvOffset: int = 0


@dataclass
class PlaneCtlInfo:
    SourcePixelFormat: int = 0


@dataclass
class PlanePixelNormalizeInfo:
    NormalizerEnable: int = 0
    NormalizationFactor: int = 0


@dataclass
class LaceInfo:
    FunctionEnable: int = 0
    IeEnable: int = 0
    FastAccessModeEnable: int = 0


@dataclass
class PipeCscCoeffInfo:
    PipeCscCoeffValues: List[int] = field(default_factory=list)


@dataclass
class PlaneCscCoeffInfo:
    PlaneCscCoeffValues: List[int] = field(default_factory=list)


@dataclass
class GammaDataInfo:
    LutData: List[int] = field(default_factory=list)


@dataclass
class GammaIndexInfo:
    GammaIndexValue: int = 0


@dataclass
class GammaModeInfo:
    PlanePreCscGammaEnable: int = 0
    PlaneGammaMode: int = 0
    PlaneGammaDisable: int = 0
    PreCscGammaEnable: int = 0
    PipeGammaEnable: int = 0
    GammaMode: int = 0


@dataclass
class AviInfo:
    QuantRange: int = 0
    vdipctlavi: int = 0
    vdipctlvsc: int = 0

@dataclass
class VscSdpData:
    QuantRange: int = 0

@dataclass
class PipeCscPrePostOffInfo:
    PipeCscPrePostOffsetValues: List[int] = field(default_factory=list)


@dataclass
class PlaneCscPrePostOffInfo:
    PlaneCscPrePostOffsetValues: List[int] = field(default_factory=list)


@dataclass
class PipeFrameCtrInfo:
    pipe_frm_cntr_offset: int = 0
    pipe_frm_cntr_incr: int = 0

@dataclass
class VideoDipCtlInfo:
    video_dip_ctl_off: int = 0
    video_dip_ctl_off_vsc: int = 0

@dataclass
class MsaMiscInfo:
    Msa_misc_ctl_off: int = 0

@dataclass
class CmtgInfo:
    CmtgEnable: bool = False
    DdiFnCtrlCmtgSlave: bool = False
    CmtgHTotal: int = 0
    CmtgHActive: int = 0
    CmtgHBlankStart: int = 0
    CmtgHBlankEnd: int = 0
    CmtgHSyncStart: int = 0
    CmtgHSyncEnd: int = 0
    CmtgVTotal: int = 0
    CmtgVActive: int = 0
    CmtgVBlankStart: int = 0
    CmtgVBlankEnd: int = 0
    CmtgVSyncStart: int = 0
    CmtgVSyncEnd: int = 0
    CmtgLinkM: int = 0
    CmtgLinkN: int = 0
    CmtgContextLatency: int = 0


@dataclass
class Dc6vInfo:
    LowerGuardBand: int = 0
    UpperGuardBand: int = 0
    RestoreProgrammingTime: int = 0
    LineTimeDc6v: int = 0


@dataclass
class ScalerInfo:
    scaler_1_enable: int = 0
    scaler_2_enable: int = 0
    scaler_1_binding: int = 0
    scaler_2_binding: int = 0


@dataclass
class InterruptInfo:
    InterruptISR_CmtgDelayedVblank: int = 0
    InterruptISR_CmtgVblank: int = 0
    InterruptISR_CmtgVsync: int = 0
    InterruptIMR_CmtgDelayedVblank: int = 0
    InterruptIMR_CmtgVblank: int = 0
    InterruptIMR_CmtgVsync: int = 0
    InterruptIIR_CmtgDelayedVblank: int = 0
    InterruptIIR_CmtgVblank: int = 0
    InterruptIIR_CmtgVsync: int = 0
    InterruptIER_CmtgDelayedVblank: int = 0
    InterruptIER_CmtgVblank: int = 0
    InterruptIER_CmtgVsync: int = 0


@dataclass
class DcStateInfo:
    DC9Enabled: int = 0
    DC6Enabled: int = 0
    DC5Enabled: int = 0
    DC6vEnabled: int = 0
    DC3CoEnabled: int = 0
    PhyClkreqPg1Latch: int = 0
    PhyPg1Latch: int = 0

@dataclass
class ALPMInfo:
    ExtendedFastWakeEnable: int = 0
    LinkOffBetweenFramesEnable: int = 0
    AlpmAuxLessEnable: int = 0
    AlpmEnable: int = 0


########################################################################################################################
# Common Functions
########################################################################################################################
def read_register(offset: int, gfx_index: str) -> int:
    return driver_interface.DriverInterface().mmio_read(offset, gfx_index)


def write_register(offset: int, value: int, gfx_index: str) -> bool:
    return driver_interface.DriverInterface().mmio_write(offset, value, gfx_index)
