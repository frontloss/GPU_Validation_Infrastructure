/**
* @file		DpcdHandler.cs
* @brief	Handles all the Aux transaction related events
*
* @author	Rohit Kumar
*/

using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDisplayExternal;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.IO;
using GFX_DISPLAY_EXTERNAL = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDisplayExternal;
using GFX_DISPLAY_DRIVER = Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;

namespace EtlParser.Handlers
{
    public class DpcdData : CommonData
    {
        public bool IsWrite;
        public DD_DP_AUX_CHANNEL_TYPE Channel;
        public uint Address;
        public int Size;
        public DDSTATUS Status;
        public string Data;

        public DpcdData(GFX_DISPLAY_DRIVER.Aux_t data, Boolean IsWrite) : base(data)
        {
            this.IsWrite = IsWrite;
            this.Channel = data.Channel;
            this.Address = (uint)data.Address;
            this.Size = data.Size;
            this.Status = data.Status;
            this.Data = BitConverter.ToString(data.Data);
        }

        public DpcdData(GFX_DISPLAY_EXTERNAL.Aux_t data, Boolean IsWrite) : base(data)
        {
            this.IsWrite = IsWrite;
            this.Channel = (DD_DP_AUX_CHANNEL_TYPE)data.Channel;
            this.Address = (uint)data.Address;
            this.Size = data.Size;
            this.Status = (DDSTATUS)data.Status;
            this.Data = BitConverter.ToString(data.Data);
        }
    }
    class DpcdHandler
    {
        public Queue<DpcdData> dpcdDataQueue = new Queue<DpcdData>();
        public void Enqueue(GFX_DISPLAY_DRIVER.Aux_t data, Boolean IsWrite)
        {
            this.dpcdDataQueue.Enqueue(new DpcdData(data, IsWrite));
        }
        public void Enqueue(GFX_DISPLAY_EXTERNAL.Aux_t data, Boolean IsWrite)
        {
            this.dpcdDataQueue.Enqueue(new DpcdData(data, IsWrite));
        }
        public void DumpJson()
        {
            String dpcdDataOutputFile = Environment.CurrentDirectory + "\\" + "dpcdData.json";
            // First delete the existing file
            System.IO.File.Delete(dpcdDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(dpcdDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
