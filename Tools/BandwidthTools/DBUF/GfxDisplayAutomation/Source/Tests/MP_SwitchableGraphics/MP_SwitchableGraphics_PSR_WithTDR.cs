using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class MP_SwitchableGraphics_PSR_WithTDR : MP_SwitchableGraphics_PSR_Entry_Exit_Basic
    {
         [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Running Force TDR with the system in PSR");

            Thread.Sleep(5000); // Make sure its in PSR before generating the TDR. (add code to check in PSR)
            if(RunTDR())
            {
                Log.Success("TDR successfully");
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

            if (PrintPSRStatusResult(psrStatus))
                Log.Success("PSR Check Passed after TDR");
            else
                Log.Fail(true, "PSR Check Failed after TDR");
        }
    
    }
}
