/**
* @file		VbiHandler.cs
* @brief	Handles all the VBI related events
*
* @author	Rohit Kumar
*/

using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.IO;

namespace EtlParser.Handlers
{
    public class VbiData : CommonData
    {
        private PIPE_ID _pipe;
        private uint _crcCtl;
        private uint _crcResult;

        public PIPE_ID Pipe { get => _pipe; private set => _pipe = value; }
        public uint CrcCtl { get => _crcCtl; private set => _crcCtl = value; }
        public uint CrcResult { get => _crcResult; private set => _crcResult = value; }
        public VbiData(PipeVBI_t data) : base(data)
        {
            this.Pipe = data.Pipe;
            this.CrcCtl = data.CRC_CTL;
            this.CrcResult = data.CRC_Result;
        }

    }
    class VbiHandler
    {
        public Queue<VbiData> vbiDataQueue = new Queue<VbiData>();
        public void Enqueue(PipeVBI_t data)
        {
            this.vbiDataQueue.Enqueue(new VbiData(data));
        }

        public void DumpJson()
        {
            String vbiDataOutputFile = Environment.CurrentDirectory + "\\" + "vbiData.json";
            // First delete the existing file
            System.IO.File.Delete(vbiDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(vbiDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this.vbiDataQueue);
            }
        }
    }
}
