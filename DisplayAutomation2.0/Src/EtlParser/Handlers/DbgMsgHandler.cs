/**
* @file		DbgMsgHandler.cs
* @brief	Debug Message Handler
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
    public class DbgMsgData : CommonData
    {
        private string _message;
        private string _function;
        private uint _line;

        public string Message { get => _message; private set => _message = value; }
        public string Function { get => _function; private set => _function = value; }
        public uint Line { get => _line; private set => _line = value; }
        public DbgMsgData(DebugPrint_t data) : base(data)
        {
            this.Message = data.Message;
            this.Function = data.Function;
            this.Line = data.Line;
        }
    }
    class DbgMsgHandler
    {
        public Queue<DbgMsgData> dbgMsgDataQueue = new Queue<DbgMsgData>();
        public void Enqueue(DebugPrint_t data)
        {
            this.dbgMsgDataQueue.Enqueue(new DbgMsgData(data));
        }

        public void DumpJson()
        {
            String dbgMsgDataOutputFile = Environment.CurrentDirectory + "\\" + "dbgMsgData.json";
            // First delete the existing file
            System.IO.File.Delete(dbgMsgDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(dbgMsgDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this.dbgMsgDataQueue);
            }
        }
    }
}
