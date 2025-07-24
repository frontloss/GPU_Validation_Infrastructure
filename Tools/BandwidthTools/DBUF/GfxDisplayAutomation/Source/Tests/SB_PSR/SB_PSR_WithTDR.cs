namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Threading;

    class SB_PSR_WithTDR : SB_PSR_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Running Force TDR with the system in PSR");

            Thread.Sleep(5000); // Make sure its in PSR before generating the TDR. (add code to check in PSR)
            if(RunTDR())
            {
                Log.Success("TDR successful");
            }
            else
            {
                Log.Abort("TDR failed");
            }

            Thread.Sleep(3000);
            Log.Message(true, "Checking PSR after TDR");
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed after TDR");
            else
                Log.Fail(true, "PSR Check Failed after TDR");
        }
    }
}
