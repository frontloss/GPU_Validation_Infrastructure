/**
* @file		CommonHandler.cs
* @brief	Common handler for all the custom events
*
* @author	Rohit Kumar
*/

using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.IO;
using DXGK_BACKLIGHT_OPTIMIZATION_LEVEL = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver.DXGK_BACKLIGHT_OPTIMIZATION_LEVEL;
using PIPE_ID = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay.PIPE_ID;


namespace EtlParser.Handlers
{
    public class CommonData
    {
        public double TimeStamp;
        public ANALYZE_LEVEL Level;
        public string TaskName;
        public TraceEventOpcode Opcode;
        public int ThreadId;

        public CommonData(TraceEvent data)
        {
            this.TimeStamp = data.TimeStampRelativeMSec;
            this.Level = (ANALYZE_LEVEL)data.Level;
            this.TaskName = data.TaskName;
            this.Opcode = data.Opcode;
            this.ThreadId = data.ThreadID;
        }
    }

    // *********************************************************************
    // Yangra Events
    // *********************************************************************

    public class EtlDetails
    {
        public double EndTime;
        public long SessionStartTime;
        public long SessionEndTime;
        public TimeSpan SessionDuration;
        public EtlDetails(ETWTraceEventSource source)
        {
            EndTime = source.SessionEndTimeRelativeMSec;
            SessionStartTime = source.SessionStartTime.Ticks;
            SessionEndTime = source.SessionEndTime.Ticks;
            SessionDuration = source.SessionDuration;
        }
    }

    public class SetTimingData : CommonData
    {
        public DD_PORT_TYPES Port;
        public PIPE_ID Pipe;
        public uint SinkIndex;
        public DD_VOT VOT;
        public bool Enable;
        public uint SrcX;
        public uint SrcY;
        public PIXEL_FMT PixelFmt;
        public uint HActive;
        public uint VActive;
        public uint HTotal;
        public uint VTotal;
        public uint RR;
        public ulong DotClock;
        public DD_SCALING Scaling;
        public bool FMS;
        public SetTimingData(ProtocolSetTimingData_t data) : base(data)
        {
            this.Port = data.Port;
            this.Pipe = data.Pipe;
            this.SinkIndex = data.SinkIndex;
            this.VOT = data.VOT;
            this.Enable = data.Enable;
            this.SrcX = data.SrcX;
            this.SrcY = data.ScrY;
            this.PixelFmt = data.PixelFmt;
            this.HActive = data.HActive;
            this.VActive = data.VActive;
            this.HTotal = data.HTotal;
            this.VTotal = data.VTotal;
            this.RR = data.RR;
            this.DotClock = (data.Version <= 2) ? data.DeprecatedDotClock : (ulong)data.DotClock;
            this.Scaling = data.Scaling;
            this.FMS = data.FMS;
        }
    }
    public class SetTimingOsStateData : CommonData
    {
        public uint SrcId;
        public uint TargetId;
        public DD_SET_TIMING_PATH_FLAGS PathStatus;
        public SetTimingOsStateData(OsSetTiming_t data) : base(data)
        {
            this.SrcId = data.SrcId;
            this.TargetId = data.TargetId;
            this.PathStatus = data.PathStatus;
        }
    }
    public class VrrEnableData : CommonData
    {
        public uint VrrMax;
        public uint VrrMin;
        public uint FrameStartToPipelineFullLineCount;
        public int VrrMaxShiftIncrement;
        public int VrrMaxShiftDecrement;
        public PIPE_ID PipeId;
        public uint VrrFlipLine;
        public VrrEnableData(VrrEnableParams_t data) : base(data)
        {
            this.VrrMax = data.VrrMax;
            this.VrrMin = data.VrrMin;
            this.FrameStartToPipelineFullLineCount = data.FramestartToPipelineFullLinecount;
            this.VrrMaxShiftIncrement = data.VrrMaxShiftIncrement;
            this.VrrMaxShiftDecrement = data.VrrMaxShiftDecrement;
            this.PipeId = data.PipeId;
            this.VrrFlipLine = data.VrrFlipLine;
        }
    }

    public class VrrDisableData : CommonData
    {
        public PIPE_ID PipeId;
        public VrrDisableData(VrrDisableParams_t data) : base(data)
        {
            this.PipeId = data.PipeId;
        }
    }

    public class VrrStatusData : CommonData
    {
        public uint TargetId;
        public bool Active;
        public uint VrrMax;
        public uint VrrMin;
        public uint VrrFlipLine;
        public VrrStatusData(VrrStatusParams_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.Active = data.Active;
            this.VrrMax = data.VrrMax;
            this.VrrMin = data.VrrMin;
            this.VrrFlipLine = data.VrrFlipLine;
        }
    }

    public class VrrUpdateData : CommonData
    {
        public PIPE_ID PipeId;
        public uint VrrMax;
        public uint VrrFlipLine;
        public VrrUpdateData(VrrUpdateParams_t data) : base(data)
        {
            this.PipeId = data.PipeId;
            this.VrrMax = data.VrrMax;
            this.VrrFlipLine = data.VrrFlipLine;
        }
    }

    public class VrrAdaptiveBalanceBalanceData : CommonData
    {
        public uint TargetId;
        public uint PreviousVtotal;
        public int Direction;
        public int Balance;

        public VrrAdaptiveBalanceBalanceData(VrrAdaptiveBalanceBalance_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.PreviousVtotal = data.PreviousVtotal;
            this.Direction = data.Direction;
            this.Balance = data.Balance;
        }
    }
    public class VrrAdaptiveBalanceApplyData : CommonData
    {
        public uint TargetId;
        public uint NumFrames;
        public uint CurrentFrameCount;
        public uint FlipLineValue;
        public uint Vmax;

        public VrrAdaptiveBalanceApplyData(VrrAdaptiveBalanceApply_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.NumFrames = data.NumFrames;
            this.CurrentFrameCount = data.CurrentFrameCount;
            this.FlipLineValue = data.FlipLineValue;
            this.Vmax = data.Vmax;
        }
    }
    public class VrrAdaptiveBalanceHwCounterMismatchData : CommonData
    {
        public uint TargetId;
        public DDSTATUS Status;
        public VrrAdaptiveBalanceHwCounterMismatchData(VrrAdaptiveBalanceHwCounterMismatch_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.Status = data.Status;
        }
    }
    public class SystemInfoTranscoderData : CommonData
    {
        public DD_PORT_TYPES Port;
        public PIPE_ID Pipe;
        public uint TargetID;
        public DD_VOT Vot;
        public bool Enable;
        public uint SrcX;
        public uint SrcY;
        public PIXEL_FMT PixelFmt;
        public uint HActive;
        public uint VActive;
        public uint HTotal;
        public uint VTotal;
        public uint RR;
        public long DotClock;
        public DD_SCALING Scaling;
        public bool FMS;
        public bool IsInterlaced;
        public bool IsS3DMode;
        public SystemInfoTranscoderData(CcdSetTimingData_t data) : base(data)
        {
            this.Port = data.Port;
            this.Pipe = data.Pipe;
            this.TargetID = data.TargetId;
            this.Vot = data.VOT;
            this.Enable = data.Enable;
            this.SrcX = data.SrcX;
            this.SrcY = data.ScrY;
            this.PixelFmt = data.PixelFmt;
            this.HActive = data.HActive;
            this.VActive = data.VActive;
            this.HTotal = data.HTotal;
            this.VTotal = data.VTotal;
            this.RR = data.RR;
            this.DotClock = data.DotClock;
            this.Scaling = data.Scaling;
            this.FMS = data.FMS;
            this.IsInterlaced = data.IsInterlaced;
            this.IsS3DMode = data.IsS3DMode;
        }
    }


    public class DisplayAssertData : CommonData
    {
        public string Function;
        public string Assert;
        public uint Line;
        public string File;
        public DisplayAssertData(Assert_t data) : base(data)
        {
            this.Function = data.Function;
            this.Assert = data.Assert;
            this.Line = data.Line;
            this.File = data.File;
        }
    }
    public class SelectiveFetchData : CommonData
    {
        public PIPE_ID PipeId;
        public int PlaneId;
        public uint SFScanX;
        public uint SFScanY;
        public uint SFPosX;
        public uint SFPosY;
        public SelectiveFetchData(SelectiveFetchInfo_t data) : base(data)
        {
            this.PipeId = data.PipeId;
            this.PlaneId = data.PlaneId;
            this.SFScanX = data.SFScanX;
            this.SFScanY = data.SFScanY;
            this.SFPosX = data.SFPosX;
            this.SFPosY = data.SFPosY;
        }
    }
    public class DcStateData : CommonData
    {
        public DD_DC_PWR_STATE DcStateRequested;
        public DISPLAY_DC_STATE_RESTRICTION DcStateRestriction;

        public DcStateData(DCStateRequest_t data) : base(data)
        {
            this.DcStateRequested = data.DcStateRequested;
            this.DcStateRestriction = data.DcStateRestriction;
        }
    }

    public class SpiData : CommonData
    {
        public DD_SPI_EVENTS SPIReasons;

        public DD_PORT_TYPES Port;

        public DP_SPI_REASON SPIIRQReasons;

        public SpiData(SPI_t data) : base(data)
        {
            this.SPIReasons = data.SPIReasons;
            this.Port = data.Port;
            this.SPIIRQReasons = data.SPIIRQReasons;
        }
    }

    public class PpsData : CommonData
    {
        public DD_PPS_SIGNAL PpsSignal;
        public OFF_ON PpsState;
        public DD_PORT_TYPES Port;

        public PpsData(Pps_t data) : base(data)
        {
            this.PpsSignal = data.Pps_Signal;
            this.PpsState = data.Pps_State;
            this.Port = data.Port;
        }
    }

    public class ColorSetAdjustedColorimetry : CommonData
    {
        public uint TargetId;
        public uint SdrWhiteLevel;
        public uint RedPointcx;
        public uint RedPointcy;
        public uint GreenPointcx;
        public uint GreenPointcy;
        public uint BluePointcx;
        public uint BluePointcy;
        public uint WhitePointcx;
        public uint WhitePointcy;
        public uint MinLuminance;
        public uint MaxLuminance;
        public uint MaxFullFrameLuminance;
        public uint FormatBitDepths;
        public uint StandardColorimetryFlags;

        public ColorSetAdjustedColorimetry(SetAdjustedColorimetry_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.SdrWhiteLevel = data.SdrWhiteLevel;
            this.RedPointcx = data.RedPointcx;
            this.RedPointcy = data.RedPointcy;
            this.GreenPointcx = data.GreenPointcx;
            this.GreenPointcy = data.GreenPointcy;
            this.BluePointcx = data.BluePointcx;
            this.BluePointcy = data.BluePointcy;
            this.WhitePointcx = data.WhitePointcx;
            this.WhitePointcy = data.WhitePointcy;
            this.MinLuminance = data.MinLuminance;
            this.MaxLuminance = data.MaxLuminance;
            this.MaxFullFrameLuminance = data.MaxFullFrameLuminance;
            this.FormatBitDepths = data.FormatBitDepths;
            this.StandardColorimetryFlags = data.StandardColorimetryFlags;
        }
    }

    public class DisplayCaps : CommonData
    {
        public bool HDRMetadataBlockFound;
        public int EOTFSupported;
        public int HdrStaticMetaDataType;
        public int DesiredMaxCLL;
        public int DesiredMaxFALL;
        public int DesiredMinCLL;
        public DD_PORT_TYPES Port;

        public DisplayCaps(HDRCaps_t data) : base(data)
        {
            this.HDRMetadataBlockFound = data.HDRMetadataBlockFound;
            this.EOTFSupported = data.EOTFSupported;
            this.HdrStaticMetaDataType = data.HdrStaticMetaDataType;
            this.DesiredMaxCLL = data.DesiredMaxCLL;
            this.DesiredMaxFALL = data.DesiredMaxFALL;
            this.DesiredMinCLL = data.DesiredMinCLL;
            this.Port = data.Port;
        }
    }

    public class DisplayBrightness3 : CommonData
    {
        public uint TargetId;
        public uint BrightnessMillinits;
        public uint TransitionTimeMs;
        public DisplayBrightness3(BlcDdi3Set_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.BrightnessMillinits = data.BrightnessMillinits;
            this.TransitionTimeMs = data.TransitionTimeMs;
        }
        public DisplayBrightness3(t_BlcDdi3Set data): base(data)
        {
            this.TargetId = data.TargetId;
            this.BrightnessMillinits = data.BrightnessMillinits;
            this.TransitionTimeMs = data.TransitionTimeMs;
        }
    }


    public class OSGivenOneDLUT : CommonData
    {
        public uint TargetId;
        public D3DDDI_GAMMA_TYPE GammaRampType;
        public uint GammaLUTSize;
        public uint[] GammaLUTData;
        public OSGivenOneDLUT(t_OsGiven1dLut data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.GammaRampType = data.GammaRampType;
            this.GammaLUTSize = data.GammaLUTSize;
            uint[] lutdata = new uint[data.GammaLUTSize];
            for (int i = 0; i < data.GammaLUTSize; i++)
                lutdata[i] = data.GammaLUTData(i);
            this.GammaLUTData = lutdata;
        }
    }

    public class OSOneDLUTParam : CommonData
    {
        public D3DDDI_GAMMA_TYPE Type;
        public int Operation;
        public uint Num_Samples6;
        public bool Enable;
        public int Config_Flag;
        public uint TargetID;
        public OSOneDLUTParam(t_OsOneDLUT_Param data) : base(data)
        {
            this.Type = data.Type;
            this.Operation = data.Operation;
            this.Num_Samples6 = data.Num_Samples;
            this.Enable = data.Enable;
            this.Config_Flag = data.Config_Flag;
            this.TargetID = data.TargetID;
        }
    }

    public class OSGivenCSC : CommonData
    {
        public uint TargetId;
        public D3DDDI_GAMMA_TYPE GammaRampType;
        public float ScalarMultiplier;
        public uint Matrix3x4Size;
        public double[] Matrix3x4Data;
        public OSGivenCSC(OSGivenCSC_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.GammaRampType = data.GammaRampType;
            this.ScalarMultiplier = data.ScalarMultiplier;
            this.Matrix3x4Size = data.Matrix3x4Size;
            double[] bytesAsDouble = Array.ConvertAll(data.Matrix3x4Data, c => (double)c);
            this.Matrix3x4Data = bytesAsDouble;
        }
    }

    public class DsbData : CommonData
    {
        public PIPE_ID PipeID;
        public DD_DSB_SELECTOR SelectedDsb;
        public uint DsbCtrlValue;
        public uint HeadPtr;
        public uint TailPtr;
        public uint BufferDataSize;
        public int[] BufferData;
        public DsbData(Dsb_Prepare_t data) : base(data)
        {
            this.PipeID = data.PipeID;
            this.SelectedDsb = (DD_DSB_SELECTOR)data.SelectedDsb;
            this.DsbCtrlValue = data.DsbCtrlValue;
            this.HeadPtr = data.HeadPtr;
            this.TailPtr = data.TailPtr;
            this.BufferDataSize = data.BufferDataSize;
            int[] bytesAsInts = Array.ConvertAll(data.BufferData, c => (int)c);
            this.BufferData = bytesAsInts;
        }
        public DsbData(t_DSBInfo data) : base(data)
        {
            this.PipeID = (PIPE_ID)data.PipeID;
            this.SelectedDsb =(DD_DSB_SELECTOR) data.SelectedDsb;
            this.HeadPtr = data.HeadPtr;
            this.TailPtr = data.TailPtr;
            byte[] dsbBufferData = new byte[data.BufferDwords * sizeof(uint)];
            for (int i = 0; i < data.BufferDwords * sizeof(uint); i++)
                Buffer.BlockCopy(BitConverter.GetBytes((int)data.BufferData[i]), 0, dsbBufferData, i, sizeof(byte));
            this.BufferDataSize = (uint)dsbBufferData.Length;
            int[] bytesAsInts = Array.ConvertAll(dsbBufferData, c => (int)c);
            this.BufferData = bytesAsInts;
        }
    }

    public class HDRMetadata : CommonData
    {
        public DD_MPO_HDR_METADATA_TYPE HDRType;
        public int EOTF;
        public int DisplayPrimariesX0;
        public int DisplayPrimariesX1;
        public int DisplayPrimariesX2;
        public int DisplayPrimariesY0;
        public int DisplayPrimariesY1;
        public int DisplayPrimariesY2;
        public int WhitePointX;
        public int WhitePointY;
        public uint MaxMasteringLuminance;
        public uint MinMasteringluminance;
        public uint MaxCLL;
        public uint MaxFALL;
        public uint TargetID;

        public HDRMetadata(HdrStaticMetadata_t data) : base(data)
        {
            this.HDRType = data.HDRType;
            this.EOTF = data.EOTF;
            this.DisplayPrimariesX0 = data.DisplayPrimariesX0;
            this.DisplayPrimariesX1 = data.DisplayPrimariesX1;
            this.DisplayPrimariesX2 = data.DisplayPrimariesX2;
            this.DisplayPrimariesY0 = data.DisplayPrimariesY0;
            this.DisplayPrimariesY1 = data.DisplayPrimariesY1;
            this.DisplayPrimariesY2 = data.DisplayPrimariesY2;
            this.WhitePointX = data.WhitePointX;
            this.WhitePointY = data.WhitePointY;
            this.MaxMasteringLuminance = data.MaxMasteringLuminance;
            this.MinMasteringluminance = data.MinMasteringluminance;
            this.MaxCLL = data.MaxCLL;
            this.MaxFALL = data.MaxFALL;
            this.TargetID = data.TargetId;
        }
    }

    public class GfxStartDeviceStopData : CommonData
    {
        public uint Status;
        public uint VideoPresentSources;
        public uint NumberOfChildren;
        public GfxStartDeviceStopData(t_DxgkDdiStartDeviceExit data) : base(data)
        {
            this.Status = data.Status;
            this.VideoPresentSources = data.VideoPresentSources;
            this.NumberOfChildren = data.NumberOfChildren;
        }
    }

    public class DFTFlipAddress : CommonData
    {
        public PIPE_ID Pipe;
        public int PlaneID;
        public bool Async;
        public uint Address;
        public uint ScanLineCount;
        public uint FrameCount;
        public uint DisplayTime;
        public uint AddressUv;
        public PLANE_OUT_FLAGS OutFlags;
        public uint PresentationTimeStamp;
        public DFTFlipAddress(FlipAddress_t data) : base(data)
        {
            this.Pipe = data.Pipe;
            this.PlaneID = data.PlaneID;
            this.Address = data.Address;
            if (data.OpcodeName == "Async")
                this.Async = true;
            this.ScanLineCount = data.ScanLineCount;
            this.FrameCount = data.FrameCount;
            this.DisplayTime = data.DisplayTime;
            this.AddressUv = data.AddressUv;
            this.OutFlags = data.OutFlags;
            this.PresentationTimeStamp = data.PresentationTimeStamp;
        }
    }

    public class FeatureStatus : CommonData
    {
        public DD_DIAG_FEATURE_STATE_INFO Feature;
        public bool Enable;
        public uint Param1;
        public uint Param2;
        public uint Param3;
        public uint Param4;
        public FeatureStatus(FeatureStatus_t data) : base(data)
        {
            this.Feature = data.Feature;
            this.Enable = data.Enable;
            this.Param1 = data.Param1;
            this.Param2 = data.Param2;
            this.Param3 = data.Param3;
            this.Param4 = data.Param4;
        }
    }

    public class CancelFlip : CommonData
    {
        public long EntryTimeStamp;
        public int SourceId;
        public int LayerIndex;
        public long PresentIdCancelRequested;
        public long PresentIdCancelled;
        public uint HwAddressBase;
        public uint HwAddressBaseCancelled;
        public CancelFlip(CancelFlip_t data) : base(data)
        {
            this.EntryTimeStamp = data.EntryTimeStamp;
            this.SourceId = data.SourceId;
            this.LayerIndex = data.LayerIndex;
            this.PresentIdCancelRequested = data.PresentIdCancelRequested;
            this.PresentIdCancelled = data.PresentIdCancelled;
            this.HwAddressBase = data.HwAddressBase;
            this.HwAddressBaseCancelled = data.HwAddressBaseCancelled;
        }
    }

    public class BlcDdi3Optimization : CommonData
    {
        public uint TargetId;
        public DXGK_BACKLIGHT_OPTIMIZATION_LEVEL OptimizationLevel;
        public uint IsNitsBased;
        public uint AggrLevel;

        public BlcDdi3Optimization(BlcDdi3Optimization_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.OptimizationLevel = (DXGK_BACKLIGHT_OPTIMIZATION_LEVEL)data.OptimizationLevel;
            this.IsNitsBased = data.IsNitsBased;
            this.AggrLevel = data.AggrLevel;
        }

        public BlcDdi3Optimization(t_BlcDdi3Optimization data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.OptimizationLevel = data.OptimizationLevel;
            this.IsNitsBased = data.IsNitsBased;
            this.AggrLevel = data.AggrLevel;
        }
    }

    public class DisplayPwrConsD0D3StateChange : CommonData
    {
        public uint IsD0;

        public DisplayPwrConsD0D3StateChange(DisplayPwrConsD0D3StateChangeData_t data) : base(data)
        {
            this.IsD0 = data.IsD0;
        }
    }
    public class TargetMode : CommonData
    {
        public uint TargetID;
        public uint H_Active;
        public uint V_Active;
        public uint H_Total;
        public uint V_Total;
        public uint RR;
        public uint DeprecatedDotClock;
        public bool IsInterlaced;
        public bool IsPreferred;
        public DD_MODE_TYPE Origin;
        public SAMPLING_MODE_BIT_MASK SamplingMode;
        public SUPPORTED_BPC_BIT_MASK BpcSupported;
        public long DotClock;

        public TargetMode(Target_Mode_t data) : base(data)
        {
            this.TargetID = data.TargetID;
            this.H_Active = data.H_Active;
            this.V_Active = data.V_Active;
            this.H_Total = data.H_Total;
            this.V_Total = data.V_Total;
            this.RR = data.RR;
            this.DeprecatedDotClock = data.DeprecatedDotClock;
            this.IsInterlaced = data.IsInterlaced;
            this.IsPreferred = data.IsPreferred;
            this.Origin = data.Origin;
            this.SamplingMode = data.SamplingMode;
            this.BpcSupported = data.BpcSupported;
            this.DotClock = data.DotClock;
        }

    }

    public class DpRxCaps : CommonData
    {
        public uint MaxLinkRate;
        public int MaxLanes;
        public bool FastLinkTraining;
        public uint TrainingPattern;

        public DpRxCaps(DPRxCaps_t data) : base(data)
        {
            this.MaxLinkRate = data.MaxLinkRate;
            this.MaxLanes = data.MaxLanes;
            this.FastLinkTraining = data.FastLinkTraining;
            this.TrainingPattern = data.TrainingPattern;
        }
    }

    public class SetInterruptTargetPresentId : CommonData
    {
        public long EntryTimeStamp;
        public int SourceId;
        public int LayerIndex;
        public long InterruptTargetPresentId;
        public SetInterruptTargetPresentId(SetInterruptTargetPresentId_t data) : base(data)
        {
            this.EntryTimeStamp = data.EntryTimeStamp;
            this.SourceId = data.SourceId;
            this.LayerIndex = data.LayerIndex;
            this.InterruptTargetPresentId = data.InterruptTargetPresentId;
        }
    }
    public class NotifyVSyncLogBufferPlaneExt : CommonData
    {
        public uint TargetID;
        public uint LayerIndex;
        public uint LogBufferIndex;
        public long PresentID;
        public long NotifyTimeStamp;

        public NotifyVSyncLogBufferPlaneExt(NotifyVsyncLogBuffer_Plane_Ext_t data) : base(data)
        {
            this.TargetID = data.TargetID;
            this.LayerIndex = data.LayerIndex;
            this.LogBufferIndex = data.LogBufferIndex;
            this.PresentID = data.PresentID;
            this.NotifyTimeStamp = data.TimeStamp;
        }
    }
    public class NotifyVSyncLogBufferPlane : CommonData
    {
        public uint TargetID;
        public uint LayerIndex;
        public uint FirstFreeIndex;
        public bool IsNotifyVsync;

        public NotifyVSyncLogBufferPlane(NotifyVsyncLogBuffer_Plane_t data) : base(data)
        {
            this.TargetID = data.TargetID;
            this.LayerIndex = data.LayerIndex;
            this.FirstFreeIndex = data.FirstFreeIndex;
            this.IsNotifyVsync = data.IsNotifyVsync;
        }
    }

    public class RrSwitchCapsFixedRxCapsData : CommonData
    {
        public DD_PORT_TYPES Port;
        public DD_VOT SinkType;
        public int SinkIndex;
        public bool ActiveCaps;
        public bool FixedRrSwitching;
        public bool FullRrRange;
        public uint MinRr;
        public uint MaxRr;
        public bool VbiMasking;
        public int VbiMaskingFactor;
        public int NumSupportedRr;
        public DD_RR_SWITCH_METHOD RrSwitchMethod;
        public DD_DPS_PANEL_TYPE DrrsPanelType;
        public bool VirtualRr;
        public uint VSyncMinRr1000;
        public RrSwitchCapsFixedRxCapsData(RrSwitchCapsFixed_t data) : base(data)
        {
            this.Port = data.Port;
            this.SinkType = data.SinkType;
            this.SinkIndex = data.SinkIndex;
            this.ActiveCaps = data.ActiveCaps;
            this.FixedRrSwitching = data.FixedRrSwitching;
            this.FullRrRange = data.FullRrRange;
            this.MinRr = data.MinRr;
            this.MaxRr = data.MaxRr;
            this.VbiMasking = data.VbiMasking;
            this.VbiMaskingFactor = data.VbiMaskingFactor;
            this.NumSupportedRr = data.NumSupportedRr;
            this.RrSwitchMethod = data.RrSwitchMethod;
            this.DrrsPanelType = data.DrrsPanelType;
            this.VirtualRr = data.VirtualRr;
            this.VSyncMinRr1000 = data.VSyncMinRr1000;
        }
    }

    public class FmsStatusInfo : CommonData
    {
        public uint TargetId;
        public DD_FMS_STATUS_REASONS Status;

        public FmsStatusInfo(FmsModesetStatus_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.Status = data.Status;
        }
    }

    public class HWFlipQMode : CommonData
    {
        public uint TargetId;
        public DD_HW_FLIPQ_MODE FlipQMode;

        public HWFlipQMode(FlipQMode_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.FlipQMode = data.FlipQMode;
        }
    }

    public class RrSwitchInfo : CommonData
    {
        public uint TargetId;
        public bool IsCurrent;
        public DD_REFRESH_RATE_MODE RrMode;
        public DD_RR_SWITCH_METHOD RrSwitchMethod;
        public uint FixedRr1000;
        public bool VbiMasking;
        public int VbiMaskingFactor;
        public uint VariableMinRr1000;
        public uint VariableMaxRr1000;

        public RrSwitchInfo(RrSwitchState_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.IsCurrent = data.IsCurrent;
            this.RrMode = data.RrMode;
            this.RrSwitchMethod = data.RrSwitchMethod;
            this.FixedRr1000 = data.FixedRr1000;
            this.VbiMasking = data.VbiMasking;
            this.VbiMaskingFactor = data.VbiMaskingFactor;
            this.VariableMinRr1000 = data.VariableMinRr1000;
            this.VariableMaxRr1000 = data.VariableMaxRr1000;
        }
    }

    public class RrSwitchProgram : CommonData
    {
        public DD_PORT_TYPES Port;
        public DD_VOT SinkType;
        public int SinkIndex;
        public DD_RR_SWITCH_METHOD RrSwitchMethod;
        public uint LinkM;
        public uint VTotal;
        public uint VSyncStart;
        public uint VSyncEnd;
        public bool VrrEnable;
        public uint VrrVmin;
        public uint VrrVmax;
        public uint VrrFlipLine;
        public uint FrameFillTime;
        public uint GuardBand;
        public bool DcbEnabled;
        public uint TempFlipLine;
        public int TempFlipLineFrames;
        public uint TempVmax;
        public int TempVmaxFrames;
        public bool CmrrEnable;
        public long CmrrM;
        public long CmrrN;

        public RrSwitchProgram(RrSwitchProgram_t data) : base(data)
        {
            this.Port = data.Port;
            this.SinkType = data.SinkType;
            this.SinkIndex = data.SinkIndex;
            this.RrSwitchMethod = data.RrSwitchMethod;
            this.LinkM = data.LinkM;
            this.VTotal = data.VTotal;
            this.VSyncStart = data.VSyncStart;
            this.VSyncEnd = data.VSyncEnd;
            this.VrrEnable = data.VrrEnable;
            this.VrrVmin = data.VrrVmin;
            this.VrrVmax = data.VrrVmax;
            this.VrrFlipLine = data.VrrFlipLine;
            this.FrameFillTime = data.FrameFillTime;
            this.GuardBand = data.GuardBand;
            this.DcbEnabled = data.DcbEnabled;
            this.TempFlipLine = data.TempFlipLine;
            this.TempFlipLineFrames = data.TempFlipLineFrames;
            this.TempVmax = data.TempVmax;
            this.TempVmaxFrames = data.TempVmaxFrames;
            this.CmrrEnable = data.CmrrEnable;
            this.CmrrM = data.CmrrM;
            this.CmrrN = data.CmrrN;
        }
    }

    public class ProcessConfigTable : CommonData
    {
        public string ProcessName;
        public uint ProcessId;
        public DD_GAMING_SYNC_MODE GamingSyncMode;
        public uint HeadIndex;
        public int RefCount;
        public bool FlipSubmissionDone;
        public int NumValidEntries;
        public DD_PROCESS_CONFIG_TABLE_ENTRY_ACTION Action;

        public ProcessConfigTable(ProcessConfigTableEntry_t data) : base(data)
        {
            this.ProcessName = data.ProcessName;
            this.ProcessId = data.ProcessId;
            this.GamingSyncMode = data.GamingSyncMode;
            this.HeadIndex = data.HeadIndex;
            this.RefCount = data.VRRBltEnabledProcessCount;
            this.FlipSubmissionDone = data.FlipSubmissionDone;
            this.NumValidEntries = data.NumValidEntries;
            this.Action = data.Action;

        }
    }

    public class FlipProcessDetails : CommonData
    {
        public string ProcessName;
        public uint ProcessId;
        public DD_PROCESS_FLAGS ProcessFlags;
        public uint LayerIndex;
        public UInt64 hAllocation;

        public FlipProcessDetails(FlipProcessDetails_t data) : base(data)
        {
            this.ProcessName = data.ProcessName;
            this.ProcessId = data.ProcessId;
            this.ProcessFlags = data.ProcessFlags;
            this.LayerIndex = data.LayerIndex;
            this.hAllocation = data.hAllocation;
        }
    }

    public class HwPlaneToLayerIndex : CommonData
    {
        public int HwPlaneIndexMap;
        public int LayerIndexMap;
        public int PipeId;

        public HwPlaneToLayerIndex(LayerToPlaneMap_t data) : base(data)
        {
            this.HwPlaneIndexMap = data.HwPlaneIndexMap;
            this.LayerIndexMap = data.LayerIndexMap;
            this.PipeId = data.PipeId;
        }
    }

    public class FeatureControl : CommonData
    {
        public uint Display;
        public uint PowerConservation;
        // Skipping Reserved1
        // Skipping Reserved2
        public uint SkuTableSize;
        public uint[] SkuData;
        public uint WaTableSize;
        public uint[] WaData;
        public uint OsFtrTableSize;
        public uint[] OsFtrTable;

        public FeatureControl(FeatureControl_t data) : base(data)
        {
            this.Display = data.Display;
            this.PowerConservation = data.PowerConservation;
            this.SkuTableSize = data.SkuTableSize;
            uint[] SkuDatabytesAsInts = Array.ConvertAll(data.OsFtrTable, c => (uint)c);
            this.SkuData = SkuDatabytesAsInts;
            this.WaTableSize = data.WaTableSize;
            uint[] WaDataTablebytesAsInts = Array.ConvertAll(data.OsFtrTable, c => (uint)c);
            this.WaData = WaDataTablebytesAsInts;
            uint[] OsFtrTablebytesAsInts = Array.ConvertAll(data.OsFtrTable, c => (uint)c);
            this.OsFtrTableSize = data.OsFtrTableSize;
            this.OsFtrTable = OsFtrTablebytesAsInts;
        }
    }

    public class DFTFlipAllParam : CommonData
    {
        public PIPE_ID Pipe;
        public int PlaneID;
        public int Enabled;
        public PIXEL_FMT PixelFmt;
        public uint SurfMemType;
        public uint ScanX;
        public uint ScanY;
        public uint Orientation;
        public uint PosX;
        public uint PosY;
        public uint Address;
        public int Rsvd;
        public PLANE_IN_FLAGS FeatureFlags;
        public uint ScanLineCount;
        public uint FrameCount;
        public uint AddressUv;
        public DFTFlipAllParam(FlipAllParam_t data) : base(data)
        {
            this.Pipe = data.Pipe;
            this.PlaneID = data.PlaneID;
            this.Enabled = data.Enabled;
            this.PixelFmt = data.PixelFmt;
            this.SurfMemType = data.SurfMemType;
            this.ScanX = data.ScanX;
            this.ScanY = data.ScanY;
            this.Orientation = data.Orientation;
            this.PosX = data.PosX;
            this.PosY = data.PosY;
            this.Address = data.Address;
            this.Rsvd = data.Rsvd;
            this.FeatureFlags = data.FeatureFlags;
            this.ScanLineCount = data.ScanLineCount;
            this.FrameCount = data.FrameCount;
            this.AddressUv = data.AddressUv;
        }
    }

    public class Scaler : CommonData
    {
        public uint Index;
        public int Plane;
        public uint Pipe;
        public bool EnableFlag;
        public uint PosX;
        public uint PosY;
        public uint ScaledX;
        public uint ScaledY;

        public Scaler(ScalerForFlip_t data) : base(data)
        {
            this.Index = data.Index;
            this.Plane = data.Plane;
            this.Pipe = data.Pipe;
            this.EnableFlag = data.EnableFlag;
            this.PosX = data.PosX;
            this.PosY = data.PosY;
            this.ScaledX = data.ScaledX;
            this.ScaledY = data.ScaledY;
        }
    }

    public class ScalerPlane : CommonData
    {
        public PIPE_ID Pipe;
        public bool EnableFlag;
        public DD_SCALING ScalingType;
        public uint PosX;
        public uint PosY;
        public uint ScaledX;
        public uint ScaledY;

        public ScalerPlane(ScalerEnableDisable_t data) : base(data)
        {
            this.Pipe = data.Pipe;
            this.EnableFlag = data.EnableFlag;
            this.ScalingType = data.ScalingType;
            this.PosX = data.PosX;
            this.PosY = data.PosY;
            this.ScaledX = data.ScaledX;
            this.ScaledY = data.ScaledY;
        }
    }

    // *********************************************************************
    // Legacy Events
    // *********************************************************************

    public class DpFastLinkTrainingData : CommonData
    {
        public PORT_TYPES Port;
        public uint LinkRate;
        public uint NumLanes;
        public bool MSTMode;
        public bool LinkTrained;
        public GMCH_DP_VOLTAGE_SWING_LEVEL SwingLevel;
        public GMCH_DP_PREEMPHASIS_LEVEL PreEmpLevel;
        public DP_LINK_TRAINING_STATUS Return;

        public DpFastLinkTrainingData(t_DP_LinkTraining_FastLinkTraining data) : base(data)
        {
            this.Port = data.Port;
            this.LinkRate = data.LinkRate;
            this.NumLanes = data.NumLanes;
            this.MSTMode = data.MSTMode;
            this.LinkTrained = data.LinkTrained;
            this.SwingLevel = data.SwingLevel;
            this.PreEmpLevel = data.PreEmpLevel;
            this.Return = data.Return;
        }
    }
    public class DpLinkTrainingData : CommonData
    {
        public PORT_TYPES Port;
        public uint LinkRate;
        public uint NumLanes;
        public bool MSTMode;
        public bool LinkTrained;
        public GMCH_DP_VOLTAGE_SWING_LEVEL SwingLevel;
        public GMCH_DP_PREEMPHASIS_LEVEL PreEmpLevel;
        public DP_LINK_TRAINING_STATUS Return;
        public double LinkTrainingTime;
        public DpLinkTrainingData(t_DP_LinkTraining_Stop data, double linkTrainingTime) : base(data)
        {
            this.Port = data.Port;
            this.LinkRate = data.LinkRate;
            this.NumLanes = data.NumLanes;
            this.MSTMode = data.MSTMode;
            this.LinkTrained = data.LinkTrained;
            this.SwingLevel = data.SwingLevel;
            this.PreEmpLevel = data.PreEmpLevel;
            this.Return = data.Return;
            this.LinkTrainingTime = linkTrainingTime;
        }
    }

    public class SetTimingColor : CommonData
    {
        public DD_COLOR_MODEL Model;
        public DD_COLOR_RANGE_TYPE RangeType;
        public DD_COLOR_ENCODING Encoding;
        public DD_COLOR_GAMUT Gamut;
        public int BPC;
        public DD_COLOR_YCBCR_SUBSAMPLING YCBCR_Subsampling;
        public PIPE_ID Pipe;
        public DD_CONTENT_TYPE ContentType;

        public SetTimingColor(ColorPixelDescPipe_t data) : base(data)
        {
            this.Model = data.Model;
            this.RangeType = data.RangeType;
            this.Encoding = data.Encoding;
            this.Gamut = data.Gamut;
            this.BPC = data.BPC;
            this.YCBCR_Subsampling = data.YCBCR_Subsampling;
            this.Pipe = data.Pipe;
            this.ContentType = data.ContentType;
        }
    }

    public class GfxCheckPresentDurationSupportData : CommonData
    {
        public uint SourceId;
        public uint DesiredPresentDuration;
        public uint ClosestSmallerDuration;
        public uint ClosestLargerDuration;
        public bool IsDataProvided;

        public GfxCheckPresentDurationSupportData(t_GfxCheckPresentDurationSupportInfo data) : base(data)
        {
            this.SourceId = data.SourceId;
            this.DesiredPresentDuration = data.DesiredPresentDuration;
            this.ClosestSmallerDuration = 0;
            this.ClosestLargerDuration = 0;
            this.IsDataProvided = false;
        }
    }

    public class InfoFrame : CommonData
    {
        public DD_PORT_TYPES Port;
        public PIPE_ID Pipe;
        public DD_PROTOCOL_TYPE Protocol;
        public DD_DIP_TYPE DipType;
        public uint DipSize;
        public String DipData;
        public bool Enable;

        public InfoFrame(AVI_InfoFrameData data) : base(data)
        {
            this.Port = data.Port;
            this.Pipe = data.Pipe;
            this.Protocol = data.Protocol;
            this.DipType = data.DipType;
            this.DipSize = data.DipSize;
            this.DipData = BitConverter.ToString(data.DipData);
            this.Enable = data.Enable;
        }

    }

    public class OsTargetMode : CommonData
    {
        public uint TargetId;
        public uint ModeId;
        public uint HActive;
        public uint VActive;
        public uint HTotal;
        public uint VTotal;
        public long DotClock;
        public bool IsInterlaced;
        public bool IsPreferred;
        public uint WireFormatPref;
        public bool IsVirtualRRSupported;
        public uint VSyncMinRR;

        public OsTargetMode(OsTargetMode_t data) : base(data)
        {
            this.TargetId = data.TargetId;
            this.ModeId = data.ModeId;
            this.HActive = data.HActive;
            this.VActive = data.VActive;
            this.HTotal = data.HTotal;
            this.VTotal = data.VTotal;
            this.DotClock = data.DotClock;
            this.IsInterlaced = data.IsInterlaced;
            this.IsPreferred = data.IsPreferred;
            this.WireFormatPref = data.WireFormatPref;
            this.IsVirtualRRSupported = data.IsVirtualRRSupported;
            this.VSyncMinRR = data.VSyncMinRR;
        }
    }

    public class CursorPosition : CommonData
    {
        public uint VidPnSourceId;
        public int X;
        public int Y;
        public uint PointerPositionFlag;

        public CursorPosition(t_DdiSetPointerPosition data) : base(data)
        {
            this.VidPnSourceId = data.VidPnSourceId;
            this.X = data.X;
            this.Y = data.Y;
            this.PointerPositionFlag = (uint)data.Flags;
        }
    }

    public class CursorShape : CommonData
    {
        public uint SourceId;
        public uint Width;
        public uint Height;
        public uint PointerPositionFlag;
        public int Pitch;
        public int XHot;
        public int YHot;

        public CursorShape(t_DxgkDdiSetPointerShapeEntry data) : base(data)
        {
            this.SourceId = data.SourceId;
            this.XHot = data.XHot;
            this.YHot = data.YHot;
            this.PointerPositionFlag = (uint)data.Flags;
            this.Width = data.Width;
            this.Height = data.Height;

        }
    }

    class CommonHandler
    {
        public Queue<String> messageQueue = new Queue<String>();
        public Queue<SetTimingData> setTimingDataQueue = new Queue<SetTimingData>();
        public Queue<SetTimingOsStateData> setTimingOsStateDataQueue = new Queue<SetTimingOsStateData>();
        public Queue<VrrEnableData> vrrEnableDataQueue = new Queue<VrrEnableData>();
        public Queue<VrrDisableData> vrrDisableDataQueue = new Queue<VrrDisableData>();
        public Queue<VrrAdaptiveBalanceBalanceData> vrrAdaptiveBalanceBalanceDataQueue = new Queue<VrrAdaptiveBalanceBalanceData>();
        public Queue<VrrAdaptiveBalanceApplyData> vrrAdaptiveBalanceApplyDataQueue = new Queue<VrrAdaptiveBalanceApplyData>();
        public Queue<VrrAdaptiveBalanceHwCounterMismatchData> vrrAdaptiveBalanceHwCounterMismatchDataQueue = new Queue<VrrAdaptiveBalanceHwCounterMismatchData>();
        public Queue<SystemInfoTranscoderData> SystemInfoTranscoderDataQueue = new Queue<SystemInfoTranscoderData>();
        public Queue<DpFastLinkTrainingData> dpFastLinkTrainingDataQueue = new Queue<DpFastLinkTrainingData>();
        public Queue<DpLinkTrainingData> dpLinkTrainingDataQueue = new Queue<DpLinkTrainingData>();
        public Queue<DisplayAssertData> displayAssertDataQueue = new Queue<DisplayAssertData>();
        public Queue<SelectiveFetchData> selectiveFetchDataQueue = new Queue<SelectiveFetchData>();
        public Queue<GfxCheckPresentDurationSupportData> gfxCheckPresentDurationSupportDataQueue = new Queue<GfxCheckPresentDurationSupportData>();
        public Queue<DcStateData> dcStateDataQueue = new Queue<DcStateData>();
        public Queue<PpsData> ppsDataQueue = new Queue<PpsData>();
        public Queue<SetTimingColor> setTimingColorQueue = new Queue<SetTimingColor>();
        public Queue<ColorSetAdjustedColorimetry> setAdjustedColorimetryInfoQueue = new Queue<ColorSetAdjustedColorimetry>();
        public Queue<DisplayCaps> hdrDisplayCapsQueue = new Queue<DisplayCaps>();
        public Queue<DisplayBrightness3> displayBrightness3Queue = new Queue<DisplayBrightness3>();
        public Queue<OSGivenOneDLUT> osGivenOneDLUTQueue = new Queue<OSGivenOneDLUT>();
        public Queue<OSOneDLUTParam> osOneDLUTParamQueue = new Queue<OSOneDLUTParam>();
        public Queue<OSGivenCSC> osGivenCSCQueue = new Queue<OSGivenCSC>();
        public Queue<HDRMetadata> defaultHdrMetadataQueue = new Queue<HDRMetadata>();
        public Queue<HDRMetadata> flipHdrMetadataQueue = new Queue<HDRMetadata>();
        public Queue<GfxStartDeviceStopData> gfxStartDeviceStopDataQueue = new Queue<GfxStartDeviceStopData>();
        public Queue<DsbData> dsbDataQueue = new Queue<DsbData>();
        public Queue<DFTFlipAddress> dftFlipAddressQueue = new Queue<DFTFlipAddress>();
        public Queue<VrrStatusData> VrrStatusDataQueue = new Queue<VrrStatusData>();
        public Queue<InfoFrame> SendInfoFrameQueue = new Queue<InfoFrame>();
        public Queue<OsTargetMode> OsTargetModeQueue = new Queue<OsTargetMode>();
        public Queue<FeatureStatus> featureStatusQueue = new Queue<FeatureStatus>();
        public Queue<SpiData> SpiDataQueue = new Queue<SpiData>();
        public Queue<CancelFlip> cancelFlipQueue = new Queue<CancelFlip>();
        public Queue<DisplayPwrConsD0D3StateChange> displayPwrConsD0D3StateChangeEventQueue = new Queue<DisplayPwrConsD0D3StateChange>();
        public Queue<BlcDdi3Optimization> blcDdi3OptimizationQueue = new Queue<BlcDdi3Optimization>();
        public Queue<TargetMode> TargetModeQueue = new Queue<TargetMode>();
        public Queue<DpRxCaps> dpRxCapsQueue = new Queue<DpRxCaps>();
        public Queue<SetInterruptTargetPresentId> setInterruptTargetPresentIdQueue = new Queue<SetInterruptTargetPresentId>();
        public Queue<NotifyVSyncLogBufferPlaneExt> notifyVSyncLogBufferPlaneExtQueue = new Queue<NotifyVSyncLogBufferPlaneExt>();
        public Queue<NotifyVSyncLogBufferPlane> notifyVSyncLogBufferPlaneQueue = new Queue<NotifyVSyncLogBufferPlane>();
        public Queue<EtlDetails> EtlDetailsQueue = new Queue<EtlDetails>();
        public Queue<RrSwitchCapsFixedRxCapsData> RrSwitchCapsFixedRxCapsDataQueue = new Queue<RrSwitchCapsFixedRxCapsData>();
        public Queue<HWFlipQMode> hwFlipQModeQueue = new Queue<HWFlipQMode>();
        public Queue<RrSwitchInfo> rrSwitchInfoQueue = new Queue<RrSwitchInfo>();
        public Queue<RrSwitchProgram> rrSwitchProgramQueue = new Queue<RrSwitchProgram>();
        public Queue<FmsStatusInfo> fmsStatusInfoQueue = new Queue<FmsStatusInfo>();
        public Queue<ProcessConfigTable> processConfigTableQueue = new Queue<ProcessConfigTable>();
        public Queue<FlipProcessDetails> flipProcessDetailsQueue = new Queue<FlipProcessDetails>();
        public Queue<HwPlaneToLayerIndex> hwPlaneToLayerIndexQueue = new Queue<HwPlaneToLayerIndex>();
        public Queue<FeatureControl> featureControlQueue = new Queue<FeatureControl>();
        public Queue<DFTFlipAllParam> dftFlipAllParamQueue = new Queue<DFTFlipAllParam>();
        public Queue<CursorPosition> CursorPosQueue = new Queue<CursorPosition>();
        public Queue<CursorShape> CursorShapeQueue = new Queue<CursorShape>();
        public Queue<Scaler> scalerQueue = new Queue<Scaler>();
        public Queue<ScalerPlane> scalerPlaneQueue = new Queue<ScalerPlane>();

        public GfxCheckPresentDurationSupportData previousCheckPresentDurationSupportData;

        public void Enqueue(String data)
        {
            this.messageQueue.Enqueue(data);
        }

        public void Enqueue(ProtocolSetTimingData_t data)
        {
            this.setTimingDataQueue.Enqueue(new SetTimingData(data));
        }

        public void Enqueue(OsSetTiming_t data)
        {
            this.setTimingOsStateDataQueue.Enqueue(new SetTimingOsStateData(data));
        }

        public void Enqueue(VrrEnableParams_t data)
        {
            this.vrrEnableDataQueue.Enqueue(new VrrEnableData(data));
        }

        public void Enqueue(VrrDisableParams_t data)
        {
            this.vrrDisableDataQueue.Enqueue(new VrrDisableData(data));
        }

        public void Enqueue(VrrAdaptiveBalanceBalance_t data)
        {
            this.vrrAdaptiveBalanceBalanceDataQueue.Enqueue(new VrrAdaptiveBalanceBalanceData(data));
        }

        public void Enqueue(t_DSBInfo data)
        {
            this.dsbDataQueue.Enqueue(new DsbData(data));
        }

        public void Enqueue(VrrAdaptiveBalanceApply_t data)
        {
            this.vrrAdaptiveBalanceApplyDataQueue.Enqueue(new VrrAdaptiveBalanceApplyData(data));
        }

        public void Enqueue(VrrAdaptiveBalanceHwCounterMismatch_t data)
        {
            this.vrrAdaptiveBalanceHwCounterMismatchDataQueue.Enqueue(new VrrAdaptiveBalanceHwCounterMismatchData(data));
        }

        public void Enqueue(CcdSetTimingData_t data)
        {
            // Console.WriteLine(data.ToString());
            this.SystemInfoTranscoderDataQueue.Enqueue(new SystemInfoTranscoderData(data));
        }

        public void Enqueue(t_DP_LinkTraining_FastLinkTraining data)
        {
            this.dpFastLinkTrainingDataQueue.Enqueue(new DpFastLinkTrainingData(data));
        }

        public void Enqueue(t_DP_LinkTraining_Stop data, double linkTrainingTime)
        {
            this.dpLinkTrainingDataQueue.Enqueue(new DpLinkTrainingData(data, linkTrainingTime));
        }

        public void Enqueue(Assert_t data)
        {
            this.displayAssertDataQueue.Enqueue(new DisplayAssertData(data));
        }

        public void Enqueue(SelectiveFetchInfo_t data)
        {
            this.selectiveFetchDataQueue.Enqueue(new SelectiveFetchData(data));
        }

        public void Enqueue(t_GfxCheckPresentDurationSupportInfo data)
        {
            this.previousCheckPresentDurationSupportData = new GfxCheckPresentDurationSupportData(data);
        }

        public void Enqueue(t_CheckPresentDurationSupportExit data)
        {
            if (this.previousCheckPresentDurationSupportData.IsDataProvided == false)
            {
                this.previousCheckPresentDurationSupportData.IsDataProvided = true;
                this.previousCheckPresentDurationSupportData.ClosestSmallerDuration = data.ClosestSmallerDuration;
                this.previousCheckPresentDurationSupportData.ClosestLargerDuration = data.ClosestLargerDuration;
                this.gfxCheckPresentDurationSupportDataQueue.Enqueue(this.previousCheckPresentDurationSupportData);
            }
        }

        public void Enqueue(DCStateRequest_t data)
        {
            this.dcStateDataQueue.Enqueue(new DcStateData(data));
        }

        public void Enqueue(Pps_t data)
        {
            this.ppsDataQueue.Enqueue(new PpsData(data));
        }

        public void Enqueue(ColorPixelDescPipe_t data)
        {
            this.setTimingColorQueue.Enqueue(new SetTimingColor(data));
        }

        public void Enqueue(SetAdjustedColorimetry_t data)
        {
            this.setAdjustedColorimetryInfoQueue.Enqueue(new ColorSetAdjustedColorimetry(data));
        }
        public void Enqueue(HDRCaps_t data)
        {
            this.hdrDisplayCapsQueue.Enqueue(new DisplayCaps(data));
        }

        public void Enqueue(BlcDdi3Set_t data)
        {
            this.displayBrightness3Queue.Enqueue(new DisplayBrightness3(data));
        }
        
        public void Enqueue(t_BlcDdi3Set data)
        {
            this.displayBrightness3Queue.Enqueue(new DisplayBrightness3(data));
        }

        public void Enqueue(t_OsGiven1dLut data)
        {
            this.osGivenOneDLUTQueue.Enqueue(new OSGivenOneDLUT(data));
        }

        public void Enqueue(t_OsOneDLUT_Param data)
        {
            this.osOneDLUTParamQueue.Enqueue(new OSOneDLUTParam(data));
        }

        public void Enqueue(OSGivenCSC_t data)
        {
            this.osGivenCSCQueue.Enqueue(new OSGivenCSC(data));
        }

        public void Enqueue(Dsb_Prepare_t data)
        {
            this.dsbDataQueue.Enqueue(new DsbData(data));
        }

        public void Enqueue(HdrStaticMetadata_t data)
        {
            if (String.Equals(data.OpcodeName, "Color"))
            {
                this.defaultHdrMetadataQueue.Enqueue(new HDRMetadata(data));
            }
            if (String.Equals(data.OpcodeName, "Plane"))
            {
                this.flipHdrMetadataQueue.Enqueue(new HDRMetadata(data));
            }
        }

        public void Enqueue(t_DxgkDdiStartDeviceExit data)
        {
            this.gfxStartDeviceStopDataQueue.Enqueue(new GfxStartDeviceStopData(data));
        }

        public void Enqueue(FlipAddress_t data)
        {
            this.dftFlipAddressQueue.Enqueue(new DFTFlipAddress(data));
        }

        public void Enqueue(VrrStatusParams_t data)
        {
            this.VrrStatusDataQueue.Enqueue(new VrrStatusData(data));
        }

        public void Enqueue(AVI_InfoFrameData data)
        {
            this.SendInfoFrameQueue.Enqueue(new InfoFrame(data));
        }

        public void Enqueue(OsTargetMode_t data)
        {
            this.OsTargetModeQueue.Enqueue(new OsTargetMode(data));
        }

        public void Enqueue(FeatureStatus_t data)
        {
            this.featureStatusQueue.Enqueue(new FeatureStatus(data));
        }
        public void Enqueue(SPI_t data)
        {
            this.SpiDataQueue.Enqueue(new SpiData(data));
        }

        public void Enqueue(CancelFlip_t data)
        {
            this.cancelFlipQueue.Enqueue(new CancelFlip(data));
        }

        public void Enqueue(DisplayPwrConsD0D3StateChangeData_t data)
        {
            this.displayPwrConsD0D3StateChangeEventQueue.Enqueue(new DisplayPwrConsD0D3StateChange(data));
        }
        public void Enqueue(Target_Mode_t data)
        {
            this.TargetModeQueue.Enqueue(new TargetMode(data));
        }

        public void Enqueue(BlcDdi3Optimization_t data)
        {
            this.blcDdi3OptimizationQueue.Enqueue(new BlcDdi3Optimization(data));
        }

        public void Enqueue(t_BlcDdi3Optimization data)
        {
            this.blcDdi3OptimizationQueue.Enqueue(new BlcDdi3Optimization(data));
        }

        public void Enqueue(DPRxCaps_t data)
        {
            this.dpRxCapsQueue.Enqueue(new DpRxCaps(data));
        }

        public void Enqueue(SetInterruptTargetPresentId_t data)
        {
            this.setInterruptTargetPresentIdQueue.Enqueue(new SetInterruptTargetPresentId(data));
        }

        public void Enqueue(NotifyVsyncLogBuffer_Plane_Ext_t data)
        {
            this.notifyVSyncLogBufferPlaneExtQueue.Enqueue(new NotifyVSyncLogBufferPlaneExt(data));
        }

        public void Enqueue(NotifyVsyncLogBuffer_Plane_t data)
        {
            this.notifyVSyncLogBufferPlaneQueue.Enqueue(new NotifyVSyncLogBufferPlane(data));
        }

        public void Enqueue(ETWTraceEventSource source)
        {
            this.EtlDetailsQueue.Enqueue(new EtlDetails(source));
        }

        public void Enqueue(RrSwitchCapsFixed_t data)
        {
            this.RrSwitchCapsFixedRxCapsDataQueue.Enqueue(new RrSwitchCapsFixedRxCapsData(data));
        }

        public void Enqueue(FlipQMode_t data)
        {
            this.hwFlipQModeQueue.Enqueue(new HWFlipQMode(data));
        }
        public void Enqueue(RrSwitchState_t data)
        {
            this.rrSwitchInfoQueue.Enqueue(new RrSwitchInfo(data));
        }

        public void Enqueue(RrSwitchProgram_t data)
        {
            this.rrSwitchProgramQueue.Enqueue(new RrSwitchProgram(data));
        }

        public void Enqueue(FmsModesetStatus_t data)
        {
            this.fmsStatusInfoQueue.Enqueue(new FmsStatusInfo(data));
        }

        public void Enqueue(ProcessConfigTableEntry_t data)
        {
            this.processConfigTableQueue.Enqueue(new ProcessConfigTable(data));
        }

        public void Enqueue(FlipProcessDetails_t data)
        {
            this.flipProcessDetailsQueue.Enqueue(new FlipProcessDetails(data));
        }

        public void Enqueue(LayerToPlaneMap_t data)
        {
            this.hwPlaneToLayerIndexQueue.Enqueue(new HwPlaneToLayerIndex(data));

        }

        public void Enqueue(FeatureControl_t data)
        {
            this.featureControlQueue.Enqueue(new FeatureControl(data));
        }

        public void Enqueue(FlipAllParam_t data)
        {
            this.dftFlipAllParamQueue.Enqueue(new DFTFlipAllParam(data));
        }

        public void Enqueue(t_DdiSetPointerPosition data)
        {
            this.CursorPosQueue.Enqueue(new CursorPosition(data));
        }

        public void Enqueue(t_DxgkDdiSetPointerShapeEntry data)
        {
            this.CursorShapeQueue.Enqueue(new CursorShape(data));
        }

        public void Enqueue(ScalerForFlip_t data)
        {
            this.scalerQueue.Enqueue(new Scaler(data));
        }

        public void Enqueue(ScalerEnableDisable_t data)
        {
            this.scalerPlaneQueue.Enqueue(new ScalerPlane(data));
        }

        public void DumpJson()
        {
            String commonDataOutputFile = Environment.CurrentDirectory + "\\" + "commonData.json";
            // First delete the existing file
            System.IO.File.Delete(commonDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(commonDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}