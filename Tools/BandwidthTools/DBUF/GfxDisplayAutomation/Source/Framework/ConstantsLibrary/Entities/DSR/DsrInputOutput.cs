namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Drawing;

    public class DsrInput
    {
        public DisplayConfig currentConfig { get; set; }
        public int captureIntervalInSec { get; set; }
        public PsrEventType dsrEventType { get; set; }
    }

    public class DsrStat
    {
        public DsrWorkingState dsrWorkingState;
        public DsrCapturedData dsrCapturedData;
        public DsrStat()
        {
            dsrWorkingState = DsrWorkingState.DsrUninitialized;
            dsrCapturedData.currentEntryExitCount = 0;
            dsrCapturedData.requiredEntryExitCount = 0;
            dsrCapturedData.currentDsrMode = "NONE";
        }
    }

    public struct DsrCapturedData
    {
        public int requiredEntryExitCount { get; set; }
        public int currentEntryExitCount { get; set; }
        public string currentDsrMode { get; set; }
    }
}
