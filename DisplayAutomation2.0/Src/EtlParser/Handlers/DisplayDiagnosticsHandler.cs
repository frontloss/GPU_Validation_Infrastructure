/**
* @file		DisplayDiagnosticsHandler.cs
* @brief	Handles all the display diagnostics events
*
* @source   GfxInstrumentationAnalyzer\DisplayAnalysis\Trackers
*/

using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.IO;

namespace EtlParser.Handlers
{
    public class DiagnosticData
    {
        DIAG_TYPE _DiagDataType;
        DD_DIAGNOSTIC_SOURCE _Source;
        public uint Param1;
        public uint Param2;
        public uint Param3;
        public uint Param4;
        DateTime _TimeStamp;
        double _TimeStampRelativeMSec;
        int _ThreadID;

        public DiagnosticData(DiagnosticData_t DiagEventData)
        {
            _Source = (DD_DIAGNOSTIC_SOURCE)DiagEventData.Source;
            _DiagDataType = (DIAG_TYPE)((UInt32)DiagEventData.Source >> 28);
            Param1 = (uint)DiagEventData.Param1;
            Param2 = DiagEventData.Param2;
            Param3 = DiagEventData.Param3;
            Param4 = DiagEventData.Param4;
            _TimeStamp = DiagEventData.TimeStamp;
            _TimeStampRelativeMSec = DiagEventData.TimeStampRelativeMSec;
            _ThreadID = DiagEventData.ThreadID;
            // Backward compatiility
            if (Source == DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DDI_ENTRY ||
                Source == DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DDI_EXIT)
            {
                // Check if the DDI is less than the minimum.
                if (Ddi < DD_DIAG_SOURCE_DDI.DDI_START_DEVICE)
                {
                    // Add the offset to make it compatible with the new definition
                    Param1 += (uint)DD_DIAG_SOURCE_DDI.DDI_START_DEVICE;
                }
            }
        }

        public DateTime TimeStamp { get => _TimeStamp; }
        public double TimeStampRelativeMSec { get => _TimeStampRelativeMSec; }
        public int ThreadID { get => _ThreadID; }
        public ANALYZE_LEVEL Level
        {
            get
            {
                switch (_DiagDataType)
                {
                    case DIAG_TYPE.CATASTROPHE:
                        return ANALYZE_LEVEL.CRITICAL;
                    case DIAG_TYPE.ERROR:
                        return ANALYZE_LEVEL.ERROR;
                    case DIAG_TYPE.WARNING:
                        return ANALYZE_LEVEL.WARNING;
                    case DIAG_TYPE.INFO:
                        return ANALYZE_LEVEL.INFO;
                    default:
                        return ANALYZE_LEVEL.VERBOSE;
                }
            }
        }
        public DD_DIAGNOSTIC_SOURCE Source { get => _Source; }
        public Boolean IsDdiFailure
        {
            get
            {
                if (_Source != DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DDI_EXIT)
                {
                    return false;
                }
                // special case handling for fucntions which return boolean
                switch (Ddi)
                {
                    case DD_DIAG_SOURCE_DDI.DDI_DISPATCH_IO_REQUEST:
                        return (Param2 == 0);
                    default:
                        return (Param2 < 0);
                }

            }
        }
        public DD_DIAG_SOURCE_DDI Ddi { get { return (DD_DIAG_SOURCE_DDI)Param1; } }
    }

    public class DisplayDiagnosticsHandler
    {
        public DdiHandler ddiHandler = new DdiHandler();
        public void DiagnosticDataProcessor(DiagnosticData_t DiagData)
        {
            switch ((DD_DIAGNOSTIC_SOURCE)DiagData.Source)
            {
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DDI_ENTRY:
                    this.ddiHandler.DdiEntry(DiagData.ThreadID, (DD_DIAG_SOURCE_DDI)DiagData.Param1, DiagData.TimeStampRelativeMSec, DiagData.Param2);
                    break;
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DDI_EXIT:
                    this.ddiHandler.DdiExit(DiagData.ThreadID, (DD_DIAG_SOURCE_DDI)DiagData.Param1, DiagData.TimeStampRelativeMSec, DiagData.Param2);
                    break;
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DELAY_STALL_CPU:
                    // StallCpu(DiagData.ThreadID, DiagData.Param1);
                    break;
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DELAY_EXECUTION_THREAD:
                    // SleepThread(DiagData.ThreadID, DiagData.Param1);
                    break;
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_WI_ENTRY:
                    this.ddiHandler.DdiEntry(DiagData.ThreadID, (DD_DIAG_SOURCE_DDI)0x1000, DiagData.TimeStampRelativeMSec, DiagData.Param2);
                    break;
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_WI_EXIT:
                    this.ddiHandler.DdiExit(DiagData.ThreadID, (DD_DIAG_SOURCE_DDI)0x1000, DiagData.TimeStampRelativeMSec, DiagData.Param2);
                    break;
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DPC_ENTRY:
                    this.ddiHandler.DdiEntry(DiagData.ThreadID, (DD_DIAG_SOURCE_DDI)0x1001, DiagData.TimeStampRelativeMSec, DiagData.Param2);
                    break;
                case DD_DIAGNOSTIC_SOURCE.DD_DIAG_INF_DPC_EXIT:
                    this.ddiHandler.DdiExit(DiagData.ThreadID, (DD_DIAG_SOURCE_DDI)0x1001, DiagData.TimeStampRelativeMSec, DiagData.Param2);
                    break;
                default:
                    break;

            }
        }        
        public void DumpJson()
        {
            String ddiDataOutputFile = Environment.CurrentDirectory + "\\" + "displayDiagnosticsData.json";
            // First delete the existing file
            System.IO.File.Delete(ddiDataOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(ddiDataOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
