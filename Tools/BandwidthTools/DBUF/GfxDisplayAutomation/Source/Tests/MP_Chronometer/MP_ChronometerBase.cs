namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.Text;
    using System.IO;
    using System.Text.RegularExpressions;
    using System.Threading;
    using System.Xml.Serialization;
    using System.Windows.Forms;
    using System.Xml;

    public class MP_ChronometerBase : TestBase
    {
        protected PowerParams _powerParams = null;
        protected bool IsResumeTimeTest = false;
        public List<DisplayType> pluggingDisplayList = new List<DisplayType>();
        public List<DisplayType> externalDisplayList = new List<DisplayType>();
        public Dictionary<int, DisplayType> displaySequence = new Dictionary<int, DisplayType>();
       
        protected bool GetListEnumeratedDisplays()
        {
            List<uint> winMonitorIdList = base.ListEnumeratedDisplays();
            List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
            return enumeratedWinMonIDList.Count.Equals(winMonitorIdList.Count);
        }
        protected void PrintEnumeratedDisplay(List<DisplayInfo> enumeratedDisplays)
        {
            Log.Verbose("************** List Of Enumerated Display supported by System ***************");
            foreach (DisplayInfo eachEnumDisplay in enumeratedDisplays)
            {
                Log.Verbose("Enumerated {0}: {1} - Windows monitor ID: {2}, CUI SDK ID {3}", eachEnumDisplay.DisplayType, eachEnumDisplay.CompleteDisplayName, eachEnumDisplay.WindowsMonitorID, eachEnumDisplay.CUIMonitorID);
                Log.Verbose("Port information for display {0}: System port is {1} and DVMU port is {2}", eachEnumDisplay.DisplayType, eachEnumDisplay.Port, eachEnumDisplay.DvmuPort);
                Log.Verbose("Optmal Resolution is {0}x{1}x{2}{3}Hz", eachEnumDisplay.DisplayMode.HzRes, eachEnumDisplay.DisplayMode.VtRes, eachEnumDisplay.DisplayMode.RR, eachEnumDisplay.DisplayMode.InterlacedFlag.Equals(0) ? "p" : "i");
                Log.Verbose("Color support: XvYcc {0}, YcBcr {1}", eachEnumDisplay.ColorInfo.IsXvYcc, eachEnumDisplay.ColorInfo.IsYcBcr);
                Log.Verbose("------------------------------------------------------------------------------");
                Log.Verbose("");
            }
            Log.Verbose("*************** List Of Enumerated Display End ***************");
        }
    }
}
