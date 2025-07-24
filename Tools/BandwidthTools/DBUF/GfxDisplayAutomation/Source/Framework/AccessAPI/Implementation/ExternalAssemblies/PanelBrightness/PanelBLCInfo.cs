using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public class PanelBLCInfo : FunctionalBase, IGetMethod
    {
        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        private delegate void PanelConfigureTextLogger(bool ConfigureParam);

        private string LogFilePath = @"C:\PanelBLCLogger.txt";
        private string DriverLogFile;
        private string DriverPackagePath;
        private string UtilDLLPath;
        private IntPtr pProcAddress;
        public object GetMethod(object argMessage)
        {
            if (!File.Exists(LogFilePath))
            {
                Log.Abort("Panel Brightness control Log File not present in {0}", LogFilePath);
            }
            DriverLogFile = CommonExtensions._cmdLineArgs.First() + "_PanelDriverLog.dat";

            DriverPackagePath = (string)argMessage;
            UtilDLLPath = DriverPackagePath + "\\PanelBLCUtility.dll";
            StubDriverInterop.Register(StubDriverServiceType.PanelStubDriver, UtilDLLPath);
            pProcAddress = StubDriverInterop.GetAddress(StubDriverServiceType.PanelStubDriver, "PanelConfigureTextLogger");
            PanelConfigureTextLogger cfgTextLogger = (PanelConfigureTextLogger)Marshal.GetDelegateForFunctionPointer(
                                                                                    pProcAddress,
                                                                                    typeof(PanelConfigureTextLogger));


            cfgTextLogger(false);
            Thread.Sleep(3000);

            string[] lines = File.ReadAllLines(LogFilePath);
            List<PanelBLCData> PanelBLCDataCollection = new List<PanelBLCData>();
            Log.Message(true, "Panel Brightness Control Log Start");
            foreach (string line in lines)
            {
                PanelBLCData panelBLC = new PanelBLCData();
                File.AppendAllText(DriverLogFile, line +Environment.NewLine);
                if (line.Contains("PanelBLCNotifyEvent"))
                {
                    panelBLC.PanelNotifyEvent = ParsePanelNotifyEvent(line);
                }
                if (line.Contains("AUXAccessStatus"))
                {
                    panelBLC.PanelAuxAccess = ParsePanelAuxAccess(line);
                }
                if (line.Contains("PanelBLCSetBrightness"))
                {
                    panelBLC.PanelSetBrightness = ParsePanelSetBrightness(line);
                }
                if (line.Contains("PanelBLCGetBrightness"))
                {
                    panelBLC.PanelGetBrightness = ParsePanelGetBrightness(line);
                }
                if (line.Contains("PanelBLCGetBrightnessCaps"))
                {
                    panelBLC.PanelBrightnessCaps = ParsePanelGetBrightnessCaps(line);
                }
                if (line.Contains("DriverLoad"))
                {
                    panelBLC.PathEnableStatus = ParsePanelPathEnableStatus(line);
                }
                PanelBLCDataCollection.Add(panelBLC);
            }
            Log.Message(false, "Panel Brightness Control Log End");
            File.Delete(LogFilePath);

            cfgTextLogger(true);
            Thread.Sleep(3000);

            return PanelBLCDataCollection;
        }

        private NotifyEvent ParsePanelNotifyEvent(string argData)
        {
            NotifyEvent panelNotifyEvent = new NotifyEvent();
            Match match;
            string Event;
            string RegexNotifyEvent = @"IGD_([A-Z0-9_]+)\s+.*IGD_EVENT_TYPE_([A-Z_]+)\s+Time\s+Stamp\s+{\s*(\d+)\s*}";
            MatchCollection NotifyEventCollection = Regex.Matches(argData, RegexNotifyEvent);

            if (NotifyEventCollection.Count != 0)
            {
                match = NotifyEventCollection[0];
                if (match.Groups[1].Length != 0)
                {
                    Event = "IGD_" + match.Groups[1].Value.Trim();
                    panelNotifyEvent.EventName = (PanelBLCEventName)Enum.Parse(typeof(PanelBLCEventName), Event, true);
                }
                if (match.Groups[2].Length != 0)
                {
                    Event = "IGD_EVENT_TYPE_" + match.Groups[2].Value.Trim();
                    panelNotifyEvent.EventType = (PanelBLCEventType)Enum.Parse(typeof(PanelBLCEventType), Event, true);
                }
                if (match.Groups[3].Length != 0)
                {
                    Int64 timeStamp = Convert.ToInt64(match.Groups[3].Value.Trim());
                    panelNotifyEvent.TimeStamp = timeStamp;
                }
            }
            return panelNotifyEvent;
        }

        private AuxAccessStatus ParsePanelAuxAccess(string argData)
        {
            AuxAccessStatus PanelAuxAccess = new AuxAccessStatus();
            Match match;
            string Status;
            string RegexAuxAccess = @"IGD_([A-Z_]+)";
            MatchCollection AuxAccessEventCollection = Regex.Matches(argData, RegexAuxAccess);

            if (AuxAccessEventCollection.Count != 0)
            {
                match = AuxAccessEventCollection[0];
                if (match.Groups[1].Length != 0)
                {
                    Status = "IGD_" + match.Groups[1].Value.Trim();
                    PanelAuxAccess.AuxStatus = (PanelBLCIGDStatus)Enum.Parse(typeof(PanelBLCIGDStatus), Status, true);
                }
            }
            return PanelAuxAccess;
        }

        private SetBrighthness ParsePanelSetBrightness(string argData)
        {
            SetBrighthness PanelSetBrightness = new SetBrighthness();
            Match match;
            string RegexSetBrightness = @"(\d+).*Time\s+Stamp\s+{\s*(\d+)\s*}";
            MatchCollection SetBrightnessCollection = Regex.Matches(argData, RegexSetBrightness);
            if (SetBrightnessCollection.Count != 0)
            {
                match = SetBrightnessCollection[0];
                if (match.Groups[1].Length != 0)
                {
                    PanelSetBrightness.BrightnessValue = Convert.ToInt32(match.Groups[1].Value.Trim());
                }
                if (match.Groups[2].Length != 0)
                {
                    PanelSetBrightness.TimeStamp = Convert.ToInt64(match.Groups[2].Value.Trim());
                }
            }
            return PanelSetBrightness;
        }

        private PanelBlcPathEnableStatus ParsePanelPathEnableStatus(string argData)
        {
            PanelBlcPathEnableStatus PathEnableStatus = new PanelBlcPathEnableStatus();
            if (argData.Contains("IGD_RUNNING"))
                PathEnableStatus.Status = true;
            return PathEnableStatus;
        }

        private GetBrighthness ParsePanelGetBrightness(string argData)
        {
            GetBrighthness PanelGetBrightness = new GetBrighthness();
            Match match;
            string RegexGetBrightness = @"(\d+).*Time\s+Stamp\s+{\s*(\d+)\s*}";
            MatchCollection GetBrightnessCollection = Regex.Matches(argData, RegexGetBrightness);

            if (GetBrightnessCollection.Count != 0)
            {
                match = GetBrightnessCollection[0];
                if (match.Groups[1].Length != 0)
                {
                    PanelGetBrightness.BrightnessValue = Convert.ToInt32(match.Groups[1].Value.Trim());
                }
                if (match.Groups[2].Length != 0)
                {
                    PanelGetBrightness.TimeStamp = Convert.ToInt64(match.Groups[2].Value.Trim());
                }
            }
            return PanelGetBrightness;
        }

        private GetBrighthnessCaps ParsePanelGetBrightnessCaps(string argData)
        {
            GetBrighthnessCaps PanelBrightnessCaps = new GetBrighthnessCaps();
            Match match;
            string RegexGetBrightnessCaps = @"(\d+).*Time\s+Stamp\s+{\s*(\d+)\s*}";
            MatchCollection GetBrightnessCapsCollection = Regex.Matches(argData, RegexGetBrightnessCaps);

            if (GetBrightnessCapsCollection.Count != 0)
            {
                match = GetBrightnessCapsCollection[0];
                if (match.Groups[1].Length != 0)
                {
                    PanelBrightnessCaps.BrightnessCaps = Convert.ToInt32(match.Groups[1].Value.Trim());
                }
                if (match.Groups[2].Length != 0)
                {
                    PanelBrightnessCaps.TimeStamp = Convert.ToInt64(match.Groups[2].Value.Trim());
                }
            }
            return PanelBrightnessCaps;
        }
    }
}
