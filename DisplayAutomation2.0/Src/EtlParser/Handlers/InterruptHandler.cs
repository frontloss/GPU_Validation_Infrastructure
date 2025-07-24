/**
* @file		InterruptHandler.cs
* @brief	Handles all the Interrupt related events
*
* @author	Rohit Kumar
*/

using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.IO;
using PIPE_ID = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay.PIPE_ID;

namespace EtlParser.Handlers
{
    public class ControlInterrupt1Data : CommonData
    {
        public DXGK_INTERRUPT_TYPE InterruptType;
        public bool Enable;
        public ControlInterrupt1Data(t_DxgkDdiControlInterruptEntry data) : base(data)
        {
            this.InterruptType = data.InterruptType;
            this.Enable = data.Enable;
        }
    }
    public class ControlInterrupt2Data : CommonData
    {
        public DXGK_INTERRUPT_TYPE InterruptType;
        public DXGK_INTERRUPT_STATE InterruptState;
        public DXGK_CRTC_VSYNC_STATE CrtVsyncState;
        public ControlInterrupt2Data(t_DxgkDdiControlInterrupt2Entry data) : base(data)
        {
            this.InterruptType = data.InterruptType;
            this.InterruptState = data.InterruptState;
            this.CrtVsyncState = data.CrtVsyncState;
        }
    }
    public class ControlInterrupt3Data : CommonData
    {
        public DXGK_INTERRUPT_TYPE InterruptType;
        public DXGK_INTERRUPT_STATE InterruptState;
        public DXGK_CRTC_VSYNC_STATE CrtVsyncState;
        public uint SourceId;
        public ControlInterrupt3Data(t_DxgkDdiControlInterrupt3Info data) : base(data)
        {
            this.InterruptType = data.InterruptType;
            this.InterruptState = data.InterruptState;
            this.CrtVsyncState = data.CrtVsyncState;
            this.SourceId = data.SourceId;
        }
    }
    public class ScanlineInterruptData : CommonData
    {
        public PIPE_ID PipeId;
        public ScanlineInterruptData(Pipe_t data) : base(data)
        {
            this.PipeId = data.PipeId;
        }
    }

    class InterruptHandler
    {
        public Queue<ControlInterrupt1Data> controlInterrupt1DataQueue = new Queue<ControlInterrupt1Data>();
        public Queue<ControlInterrupt2Data> controlInterrupt2DataQueue = new Queue<ControlInterrupt2Data>();
        public Queue<ControlInterrupt3Data> controlInterrupt3DataQueue = new Queue<ControlInterrupt3Data>();
        public Queue<ScanlineInterruptData> scanlineInterruptDataQueue = new Queue<ScanlineInterruptData>();

        public void Enqueue(t_DxgkDdiControlInterruptEntry data)
        {
            this.controlInterrupt1DataQueue.Enqueue(new ControlInterrupt1Data(data));
        }
        public void Enqueue(t_DxgkDdiControlInterrupt2Entry data)
        {
            this.controlInterrupt2DataQueue.Enqueue(new ControlInterrupt2Data(data));
        }
        public void Enqueue(t_DxgkDdiControlInterrupt3Info data)
        {
            this.controlInterrupt3DataQueue.Enqueue(new ControlInterrupt3Data(data));
        }
        public void Enqueue(Pipe_t data)
        {
            this.scanlineInterruptDataQueue.Enqueue(new ScanlineInterruptData(data));
        }

        public void DumpJson()
        {
            String vbiDataOutputFile = Environment.CurrentDirectory + "\\" + "interruptData.json";
            // First delete the existing file
            System.IO.File.Delete(vbiDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(vbiDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
