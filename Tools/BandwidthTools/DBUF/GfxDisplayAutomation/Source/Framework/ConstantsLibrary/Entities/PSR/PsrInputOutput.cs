namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    public class PsrTestInput
    {
        public int captureIntervalInSec { get; set; }
        public DisplayConfig currentConfig { get; set; }
        public PsrEventType psrEventType { get; set; }
    }

    public class PsrStatus
    {
        public PsrWorkingState psrWorkingState;
        public PsrCapturedData psrCapturedData;
        public PsrStatus()
        {
            psrWorkingState = PsrWorkingState.PsrUninitialized;
            psrCapturedData.currentEntryExitCount = 0;
            psrCapturedData.requiredEntryExitCount = 0;
            psrCapturedData.currentResidencyTime = 0;
            psrCapturedData.requiredResidencyTime = 0;
        }
    }

    public struct PsrCapturedData
    {
        public int requiredEntryExitCount { get; set; }
        public int currentEntryExitCount { get; set; }
        public int requiredResidencyTime { get; set; }
        public int currentResidencyTime { get; set; }
    }

    
}
