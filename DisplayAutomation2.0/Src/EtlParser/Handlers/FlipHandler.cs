/**
* @file		FlipHandler.cs
* @brief	Handles all the flip related events
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
using System.Net;
using Address = System.UInt64;
using DXGK_PLANE_SPECIFIC_INPUT_FLAGS = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver.DXGK_PLANE_SPECIFIC_INPUT_FLAGS;
using DXGK_SETVIDPNSOURCEADDRESS_INPUT_FLAGS = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver.DXGK_SETVIDPNSOURCEADDRESS_INPUT_FLAGS;
using DXGK_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver.DXGK_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS;
using PIPE_ID = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay.PIPE_ID;

namespace EtlParser.Handlers
{
    public class Mpo3FlipPlaneInfo : CommonData
    {
        public uint LayerIndex;
        public DXGK_PLANE_SPECIFIC_INPUT_FLAGS Flags;
        public long PresentId;
        public uint Reserved;
        public Mpo3FlipPlaneInfo(Mpo3FlipPlaneIn_t data) : base(data)
        {
            this.LayerIndex = data.LayerIndex;
            this.Flags = (DXGK_PLANE_SPECIFIC_INPUT_FLAGS)data.Flags;
            this.PresentId = data.PresentID;
            this.Reserved = data.Rsvd;
        }

        public Mpo3FlipPlaneInfo(t_Mpo3FlipPlaneIn data) : base(data)
        {
            this.LayerIndex = data.LayerIndex;
            this.Flags = data.Flags;
            this.PresentId = data.PresentID;
            this.Reserved = data.Rsvd;
        }
    }
    public class Mpo3FlipPlaneDetails : CommonData
    {
        public uint MaxImmFlipLine;
        public uint PlaneAttribFlag;
        public uint Blend;
        public uint ClrSpace;
        public uint Rotation;
        public uint StretchQuality;
        public uint SDRWhiteLevel;
        public long SrcLeft;
        public long SrcTop;
        public long SrcRight;
        public long SrcBottom;
        public long DestLeft;
        public long DestTop;
        public long DestRight;
        public long DestBottom;
        public long ClipLeft;
        public long ClipTop;
        public long ClipRight;
        public long ClipBottom;
        public long DirtyRectLeft;
        public long DirtyRectTop;
        public long DirtyRectRight;
        public long DirtyRectBottom;
        public Address hAllocation;

        public Mpo3FlipPlaneDetails(Mpo3FlipPlaneDetails_t data) : base(data)
        {
            this.MaxImmFlipLine = data.MaxImmFlipLine;
            this.PlaneAttribFlag = data.PlaneAttribFlag;
            this.Blend = data.Blend;
            this.ClrSpace = data.ClrSpace;
            this.Rotation = data.Rotation;
            this.StretchQuality = data.StretchQuality;
            this.SDRWhiteLevel = data.SDRWhiteLevel;
            this.SrcLeft = data.SrcLeft;
            this.SrcTop = data.SrcTop;
            this.SrcRight = data.SrcRight;
            this.SrcBottom = data.SrcBottom;
            this.DestLeft = data.DestLeft;
            this.DestTop = data.DestTop;
            this.DestRight = data.DestRight;
            this.DestBottom = data.DestBottom;
            this.ClipLeft = data.ClipLeft;
            this.ClipTop = data.ClipTop;
            this.ClipRight = data.ClipRight;
            this.ClipBottom = data.ClipBottom;
            this.DirtyRectLeft = data.DirtyRectLeft;
            this.DirtyRectTop = data.DirtyRectTop;
            this.DirtyRectRight = data.DirtyRectRight;
            this.DirtyRectBottom = data.DirtyRectBottom;
            this.hAllocation = data.hAllocation;
        }
    }
    public class FlipAllParam : CommonData
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
        public FlipAllParam(FlipAllParam_t data) : base(data)
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
    public class FlipAddress : CommonData
    {
        public PIPE_ID Pipe;
        public int PlaneID;
        public bool Async;
        public uint Address;
        public uint ScanLineCount;
        public uint FrameCount;
        public PLANE_IN_FLAGS FeatureFlags;
        public uint DisplayTime;
        public uint AddressUv;
        public PLANE_OUT_FLAGS OutFlags;
        public uint PresentationTimeStamp;

        public FlipAddress(FlipAddress_t data, bool IsAsync) : base(data)
        {
            this.Pipe = data.Pipe;
            this.PlaneID = data.PlaneID;
            this.Async = IsAsync;
            this.Address = data.Address;
            this.ScanLineCount = data.ScanLineCount;
            this.FrameCount = data.FrameCount;
            this.FeatureFlags = data.FeatureFlags;
            this.DisplayTime = data.DisplayTime;
            this.AddressUv = data.AddressUv;
            this.OutFlags = data.OutFlags;
            this.PresentationTimeStamp = data.PresentationTimeStamp;
        }
    }
    public class NotifyVSyncMpo2Info : CommonData
    {
        public DD_DXGK_INTERRUPT_TYPE Type;
        public uint TargetID;
        public DXGKCB_NOTIFY_INTERRUPT_DATA_FLAGS Flags;
        public uint DataCount;

        public NotifyVSyncMpo2Info(NotifyVSyncMpo2_Info_t data) : base(data)
        {
            this.Type = data.Type;
            this.TargetID = data.TargetID;
            this.Flags = data.Flags;
            this.DataCount = data.DataCount;
        }
    }
    public class NotifyVSyncMpo2Layer : CommonData
    {
        public uint LayerIndex;
        public long PresentID;
        public DXGKCB_NOTIFY_MPO_VSYNC_FLAGS Flags;

        public NotifyVSyncMpo2Layer(NotifyVSyncMpo2_Layer_t data) : base(data)
        {
            this.LayerIndex = data.LayerIndex;
            this.PresentID = data.PresentID;
            this.Flags = data.Flags;
        }
    }

    public class FlipData : CommonData
    {
        public uint SourceId;
        public uint PlaneCount;
        public uint Duration;
        public long TargetFlipTime;
        public double SoftwareOverhead;
        public double FlipDoneTime;
        public bool IsAllParam;
        public bool IsAddressOnly;
        public PIPE_ID Pipe;
        public DXGK_SETVIDPNSOURCEADDRESS_INPUT_FLAGS InputFlags;
        public DXGK_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS OutputFlags;
        public List<Mpo3FlipPlaneInfo> PlaneInfoList;
        public List<Mpo3FlipPlaneDetails> PlaneDetailsList;
        public List<FlipAllParam> FlipAllParamList;
        public List<FlipAddress> FlipAddressList;
        public List<NotifyVSyncMpo2Info> NotifyVSyncInfoList;
        public List<NotifyVSyncMpo2Layer> NotifyVSyncLayerList;
        public List<MmioData> MmioDataList;

        public FlipData(TraceEvent data) : base(data)
        {
            this.PlaneInfoList = new List<Mpo3FlipPlaneInfo>();
            this.PlaneDetailsList = new List<Mpo3FlipPlaneDetails>();
            this.FlipAllParamList = new List<FlipAllParam>();
            this.FlipAddressList = new List<FlipAddress>();
            this.NotifyVSyncInfoList = new List<NotifyVSyncMpo2Info>();
            this.NotifyVSyncLayerList = new List<NotifyVSyncMpo2Layer>();
            this.MmioDataList = new List<MmioData>();
            this.FlipDoneTime = -1;
        }
    }

    public class DictKey
    {
        public uint SourceId;
        public int ThreadId;

        public DictKey(uint SourceId, int ThreadId)
        {
            this.SourceId = SourceId;
            this.ThreadId = ThreadId;
        }
    }

    class FlipHandler
    {
        public static List<ulong> mmioTrackingOffsets = new List<ulong>() {
            0x70880, 0x70980, 0x70890, 0x708B0, 0x708D0, 0x708F0, 0x70920, 0x70940, 0x70960, 0x70990, 0x709B0, 0x709D0,
            0x709F0, 0x70A20, 0x70A40, 0x70A60, 0x7089C, 0x708BC, 0x708DC, 0x708FC, 0x7092C, 0x7094C, 0x7096C, 0x7099C,
            0x709BC, 0x709DC, 0x709FC, 0x70A2C, 0x70A4C, 0x70A6C, 0x70894, 0x708B4, 0x708D4, 0x708F4, 0x70924, 0x70944,
            0x70964, 0x70994, 0x709B4, 0x709D4, 0x709F4, 0x70A24, 0x70A44, 0x70A64, 0x70898, 0x708B8, 0x708D8, 0x708F8,
            0x70928, 0x70948, 0x70968, 0x70998, 0x709B8, 0x709D8, 0x709F8, 0x70A28, 0x70A48, 0x70A68, 0x70080, 0x71080,
            0x72080, 0x73080, 0x70180, 0x71180, 0x72180, 0x73180, 0x70280, 0x71280, 0x72280, 0x73280, 0x70380, 0x71380,
            0x72380, 0x73380, 0x70480, 0x71480, 0x72480, 0x73480, 0x70580, 0x71580, 0x72580, 0x73580, 0x70680, 0x71680,
            0x72680, 0x73680, 0x70780, 0x71780, 0x72780, 0x73780, 0x701C8, 0x711C8, 0x721C8, 0x702C8, 0x712C8, 0x722C8,
            0x703C8, 0x713C8, 0x723C8, 0x731C8, 0x732C8, 0x733C8, 0x60940, 0x61940, 0x60910, 0x61910, 0x70890, 0x71890,
            0x70998, 0x60900, 0x61900, 0x701C0, 0x711C0, 0x721C0, 0x731C0, 0x702C0, 0x712C0, 0x722C0, 0x732C0, 0x703C0,
            0x713C0, 0x723C0, 0x733C0, 0x704C0, 0x714C0, 0x724C0, 0x734C0, 0x705C0, 0x715C0, 0x725C0, 0x735C0, 0x706C0,
            0x716C0, 0x726C0, 0x736C0, 0x701C0, 0x717C0, 0x727C0, 0x737C0, 0x701B4, 0x711B4, 0x721B4, 0x731B4, 0x702B4,
            0x712B4, 0x722B4, 0x732B4, 0x703B4, 0x713B4, 0x723B4, 0x733B4, 0x704B4, 0x714B4, 0x724B4, 0x734B4, 0x705B4,
            0x715B4, 0x725B4, 0x735B4, 0x706B4, 0x716B4, 0x726B4, 0x736B4, 0x707B4, 0x717B4, 0x727B4, 0x737B4, 0x5F12C,
            0x5F13C, 0x5F52C, 0x5F53C, 0x5F92C, 0x5F93C, 0x5FD2C, 0x5FD3C, 0x85FA8, 0x8F080, 0x5F080, 0x5F480, 0x5F880,
            0x5FC80
        };
        public IDictionary<int, FlipData> flipTracking = new Dictionary<int, FlipData>();
        public IDictionary<(uint, long), FlipData> flipDoneTracking = new Dictionary<(uint, long), FlipData>();
        public Queue<FlipData> flipDataQueue = new Queue<FlipData>();

        public void StartFlip(Mpo3FlipIn_t data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData dummy))
            {
                this.flipTracking.Remove(data.ThreadID);
            }

            FlipData flipData = new FlipData(data)
            {
                SourceId = data.SourcceID,
                InputFlags = (DXGK_SETVIDPNSOURCEADDRESS_INPUT_FLAGS)data.Flags,
                PlaneCount = data.PlaneCount,
                Duration = data.Duration,
                TargetFlipTime = data.TargetFlipTime
            };
            flipTracking.Add(data.ThreadID, flipData);
        }

        public void StartFlip(t_Mpo3FlipIn data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData dummy))
            {
                this.flipTracking.Remove(data.ThreadID);
            }

            FlipData flipData = new FlipData(data)
            {
                SourceId = data.SourcceID,
                InputFlags = data.Flags,
                PlaneCount = data.PlaneCount,
                Duration = data.Duration,
                TargetFlipTime = data.TargetFlipTime
            };
            flipTracking.Add(data.ThreadID, flipData);
        }

        public void AddPlaneInfo(Mpo3FlipPlaneIn_t data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
            {
                flipData.PlaneInfoList.Add(new Mpo3FlipPlaneInfo(data));
                if(this.flipDoneTracking.TryGetValue((data.LayerIndex, data.PresentID), out FlipData dummy))
                {
                    this.flipDoneTracking.Remove((data.LayerIndex, data.PresentID));
                }
                this.flipDoneTracking.Add((data.LayerIndex, data.PresentID), flipData);
            }
        }

        public void AddPlaneInfo(t_Mpo3FlipPlaneIn data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
            {
                flipData.PlaneInfoList.Add(new Mpo3FlipPlaneInfo(data));
                if (this.flipDoneTracking.TryGetValue((data.LayerIndex, data.PresentID), out FlipData dummy))
                {
                    this.flipDoneTracking.Remove((data.LayerIndex, data.PresentID));
                }
                this.flipDoneTracking.Add((data.LayerIndex, data.PresentID), flipData);
            }
        }

        public void AddPlaneDetails(Mpo3FlipPlaneDetails_t data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
            {
                flipData.PlaneDetailsList.Add(new Mpo3FlipPlaneDetails(data));
            }
        }
        public void StopFlip(Mpo3FlipOut_t data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
            {
                flipData.OutputFlags = (DXGK_SETVIDPNSOURCEADDRESS_OUTPUT_FLAGS)data.Flags;
                flipData.SoftwareOverhead = data.TimeStampRelativeMSec - flipData.TimeStamp;

                this.flipDataQueue.Enqueue(flipData);
                this.flipTracking.Remove(data.ThreadID);
            }
        }
        public void StopFlip(t_Mpo3FlipOut data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
            {
                flipData.OutputFlags = data.Flags;
                flipData.SoftwareOverhead = data.TimeStampRelativeMSec - flipData.TimeStamp;

                this.flipDataQueue.Enqueue(flipData);
                this.flipTracking.Remove(data.ThreadID);
            }
        }
        public void AddFlipDetails(FlipAllParam_t data)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
            {
                flipData.IsAllParam = true;
                flipData.IsAddressOnly = false;
                flipData.Pipe = data.Pipe;
                flipData.FlipAllParamList.Add(new FlipAllParam(data));
            }
        }
        public void AddFlipDetails(FlipAddress_t data, bool IsAsync)
        {
            if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
            {
                flipData.IsAllParam = false;
                flipData.IsAddressOnly = true;
                flipData.Pipe = data.Pipe;
                flipData.FlipAddressList.Add(new FlipAddress(data, IsAsync));
            }
        }
        public void AddNotifyVSyncInfo(NotifyVSyncMpo2_Info_t data)
        {

        }
        public void AddNotifyVSyncLayer(NotifyVSyncMpo2_Layer_t data)
        {
            if (this.flipDoneTracking.TryGetValue((data.LayerIndex, data.PresentID), out FlipData flipData))
            {
                if(flipData.FlipDoneTime == -1)
                {
                    flipData.FlipDoneTime = data.TimeStampRelativeMSec - flipData.TimeStamp;
                }
                flipData.NotifyVSyncLayerList.Add(new NotifyVSyncMpo2Layer(data));
                if(this.flipDoneTracking.ContainsKey((data.LayerIndex, data.PresentID-1)))
                {
                    this.flipDoneTracking.Remove((data.LayerIndex, data.PresentID - 1));
                }
            }
        }
        public void AddMmioData(t_MMIO_ReadWrite data, bool IsWrite)
        {
            if(FlipHandler.mmioTrackingOffsets.Contains(data.Offset))
            {
                if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
                {
                    flipData.MmioDataList.Add(new MmioData(data, IsWrite));
                }
            }
        }

        public void AddDsbMmioData(Dsb_Prepare_t data, uint offset, uint value)
        {
            if (FlipHandler.mmioTrackingOffsets.Contains(offset))
            {
                if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
                {
                    flipData.MmioDataList.Add(new MmioData(data, offset, value));
                }
            }
        }

        public void AddDsbMmioData(t_DSBInfo data, uint offset, uint value)
        {
            if (FlipHandler.mmioTrackingOffsets.Contains(offset))
            {
                if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
                {
                    flipData.MmioDataList.Add(new MmioData(data, offset, value));
                }
            }
        }

        public void AddMmioWriteData(t_MMIOAccessData data)
        {
            if (FlipHandler.mmioTrackingOffsets.Contains(data.Offset))
            {
                if (this.flipTracking.TryGetValue(data.ThreadID, out FlipData flipData))
                {
                    flipData.MmioDataList.Add(new MmioData(data));
                }
            }
        }

        public void DumpJson()
        {
            String dbgMsgDataOutputFile = Environment.CurrentDirectory + "\\" + "flipData.json";
            // First delete the existing file
            System.IO.File.Delete(dbgMsgDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(dbgMsgDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this.flipDataQueue);
            }
        }
    }
}
