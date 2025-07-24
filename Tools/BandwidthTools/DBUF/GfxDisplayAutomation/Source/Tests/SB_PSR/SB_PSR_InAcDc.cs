namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.Threading;
    using System.Windows.Forms;

    class SB_PSR_InAcDc : SB_PSR_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Check that system is in DC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");


            Log.Message(true, "Check PSR in DC Mode");
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed in DC Mode");
            else
                Log.Fail(true, "PSR Check Failed in DC Mode");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Enable AC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Offline)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in AC Mode");
                else
                    Log.Fail("Fail to set AC mode");
            }
            else
                Log.Success("System is Running in AC Mode");

            Log.Message(true, "FYI: PSR should work in AC Mode in CS supported (enabled) systems and PSR should not work in AC Mode in Non-CS system");
            if(DisplayExtensions.VerifyCSSystem(this.ApplicationManager.MachineInfo))
            {
                // CS supported system, PSR should work in AC Mode in CS supported system.
                Log.Message(true, "This system supports CS and checking PSR in CS supported system");

                PsrTestInput psrTestInput = new PsrTestInput();
                psrTestInput.captureIntervalInSec = iTestRunDuration;
                psrTestInput.currentConfig = base.CurrentConfig;
                psrTestInput.psrEventType = PsrEventType.Default;
                PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

                if (PrintPsrStatusResult(psrStatus, true))
                    Log.Success("PSR Check Passed in AC Mode");
                else
                    Log.Fail(true, "PSR Check Failed in AC Mode");
            }
            else
            {
                // Non-CS system, PSR should not work in AC Mode in Non-CS system.
                Log.Message(true, "This system doesn\'t support CS and checking PSR in Non-CS system");

                // Check PSR is disabled

            }
            
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Enable DC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");


            Log.Message(true, "Check PSR");
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed");
            else
                Log.Fail(true, "PSR Check Failed");
        }
    }
}
