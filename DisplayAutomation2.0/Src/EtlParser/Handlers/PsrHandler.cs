/**
* @file     PsrHandler.cs
* @brief    Handles all PSR related events
*
* @author   creddyy
*/

using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.IO;

namespace EtlParser.Handlers
{
 
    public class PsrEvents:CommonData
    {
        public PIPE_ID PipeId;
        public PSR_EVENT_TYPE Operation;
        public int Field1;
        public int Field2;
        public PsrEvents(PsrPrClientEvent_t data) : base(data)
        {
            this.PipeId = data.PipeId;
            this.Operation = data.Operation;
            this.Field1 = data.Field1;
            this.Field2 = data.Field2;
        }
    }

    public class DisplayPcPsrPrProcess : CommonData
    {
        public PIPE_ID PipeId;
        public DISPLAY_PC_EVENT_NOTIFICATION_OPERATION Operation;
        public uint Field1;
        public uint Field2;

        public DisplayPcPsrPrProcess(PsrPrEvents_t data) : base(data)
        {
            this.PipeId = data.PipeId;
            this.Operation = data.Operation;
            this.Field1 = data.Field1;
            this.Field2 = data.Field2;
        }
    }
    class PsrHandler
    {
        public Queue<PsrEvents> PsrDpstEventQueue = new Queue<PsrEvents>();
        public Queue<DisplayPcPsrPrProcess> DisplayPcPsrPrProcessQueue = new Queue<DisplayPcPsrPrProcess>();

        public void Enqueue(PsrPrClientEvent_t data)
        {
            this.PsrDpstEventQueue.Enqueue(new PsrEvents(data));
        }
        public void Enqueue(PsrPrEvents_t data)
        {
            this.DisplayPcPsrPrProcessQueue.Enqueue(new DisplayPcPsrPrProcess(data));
        }

        public void DumpJson()
        {
            String psrDataOutputFile = Environment.CurrentDirectory + "\\" + "psrData.json";
            // First delete the existing file
            System.IO.File.Delete(psrDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(psrDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
