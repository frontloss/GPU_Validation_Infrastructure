/**
* @file		FunctionHandler.cs
* @brief	Handlels function entry and exit events
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
    public class FunctionData : CommonData
    {
        public string Name;
        public uint Stage;
        public uint ErrorCode;
        public FunctionData(FunctionTrack_t data) : base(data)
        {
            this.Name = data.Function;
            this.Stage = (uint)data.Stage;
            this.ErrorCode = (uint)data.ErrorCode;
        }
    }

    class FunctionHandler
    {
        public Queue<FunctionData> functionDataQueue = new Queue<FunctionData>();
        public void Enqueue(FunctionTrack_t data)
        {
            this.functionDataQueue.Enqueue(new FunctionData(data));
        }
        public void DumpJson()
        {
            String functionDataOutputFile = Environment.CurrentDirectory + "\\" + "functionData.json";
            // First delete the existing file
            System.IO.File.Delete(functionDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(functionDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
