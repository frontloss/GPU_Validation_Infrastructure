namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Threading;

    class SB_PSR_WithCursorEvents : SB_PSR_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Checking PSR with cusror move");
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.CursorMove;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if(PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed with cursor move");
            else
                Log.Fail("PSR Check Failed with cursor move");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Checking PSR with cusror change");
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.CursorChange;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed with cursor change");
            else
                Log.Fail("PSR Check Failed with cursor change");
        }
    }
}
