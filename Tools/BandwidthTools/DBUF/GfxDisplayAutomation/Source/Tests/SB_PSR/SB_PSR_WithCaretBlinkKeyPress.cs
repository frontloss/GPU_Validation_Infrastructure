namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Threading;
    using System.Windows.Forms;

    class SB_PSR_WithCaretBlinkKeyPress : SB_PSR_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            // set caret blink time
            Log.Message(true, "Checking PSR with command prompt launched with default caret blink time");

            Process pCmd = new Process();
            pCmd.StartInfo.CreateNoWindow = false;
            pCmd.StartInfo.FileName = "cmd.exe";
            pCmd.Start();

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Nothing;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (!pCmd.HasExited)
                pCmd.Kill();

            psrStatus.psrCapturedData.requiredEntryExitCount = 12;
            if (psrStatus.psrCapturedData.currentEntryExitCount >= psrStatus.psrCapturedData.requiredEntryExitCount)
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledAndWorkingProperly;
            else if ((psrStatus.psrCapturedData.currentEntryExitCount < psrStatus.psrCapturedData.requiredEntryExitCount) &&
                (psrStatus.psrCapturedData.currentEntryExitCount != 0))
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledButLessEntryExitCount;
            else if (psrStatus.psrCapturedData.currentEntryExitCount == 0)
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledButNotWorking;

            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed for caret blink");
            else
                Log.Fail(true, "PSR Check Failed for caret blink");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Checking PSR with key press"); 

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.KeyPress;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
               
            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed with key press");
            else
                Log.Fail(true, "PSR Check Failed with key press");
        }

    }
}
