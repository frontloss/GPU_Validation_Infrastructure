/**
* @file     DpstHandler.cs
* @brief    Handles all DPST related events
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
    public class DpstPhasing : CommonData
    {
        public uint PipeId;
        public string DpstPhaseAdjustInfo;
        public string BlcUserAdjustInfo;
        public DpstPhasing(PhaseCoordinatorContextData_t data) : base(data)
        {
            this.PipeId = data.PipeId;
            this.DpstPhaseAdjustInfo = BitConverter.ToString(data.DpstPhaseAdjustInfo);
            this.BlcUserAdjustInfo = BitConverter.ToString(data.BlcUserAdjustInfo);
        }

    }

    public class DpstProgramStart : CommonData
    {
        public uint PipeId;
        public uint Adjust;
        public uint Feature;
        public uint Immediate;
        public DpstProgramStart(PhaseCoordinatorProgramAdjustData_t data) : base(data)
        {
            this.PipeId = data.PipeId;
            this.Adjust = data.Adjust;
            this.Feature = data.Feature;
            this.Immediate = data.Immediate;
        }
    }


    class DpstHandler
    {
        public Queue<DpstPhasing> dpstPhaseInDataQueue = new Queue<DpstPhasing>();
        public Queue<DpstProgramStart> dpstDataQueue = new Queue<DpstProgramStart>();

        public void Enqueue(PhaseCoordinatorContextData_t data)
        {
            this.dpstPhaseInDataQueue.Enqueue(new DpstPhasing(data));
        }

        public void Enqueue(PhaseCoordinatorProgramAdjustData_t data)
        {
            this.dpstDataQueue.Enqueue(new DpstProgramStart(data));
        }

        public void DumpJson()
        {
            String dpstDataOutputFile = Environment.CurrentDirectory + "\\" + "dpstData.json";
            // First delete the existing file
            System.IO.File.Delete(dpstDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(dpstDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
