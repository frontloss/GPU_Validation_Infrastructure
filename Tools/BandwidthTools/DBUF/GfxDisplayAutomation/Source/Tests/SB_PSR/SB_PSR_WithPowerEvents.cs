namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Threading;
    using System.Windows.Forms;

    class SB_PSR_WithPowerEvents : SB_PSR_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Initiating CS/S3 and resuming back");

            if (DisplayExtensions.VerifyCSSystem(this.ApplicationManager.MachineInfo))
            {
                Log.Message("This system supports CS, initiating CS entry.");
                CSParam csData = new CSParam();
                AccessInterface.SetFeature<bool, CSParam>(Features.ConnectedStandby, Action.SetMethod, csData);
            }
            else
            {
                Log.Message(true, "This system doesn't support CS, initiating S3 entry.");
                base.EventResult(PowerStates.S3, base.InvokePowerEvent(new PowerParams() { Delay = 30, PowerStates = PowerStates.S3 }, PowerStates.S3));
                // this.InvokePowerEvent(new PowerParams() { Delay = 30, PowerStates = PowerStates.S3 }, PowerStates.S3);
            }

            // After CS/ S3 resume, it will come back to AC if switched to DC programatically
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode (Switched back to DC)");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Checking PSR after CS/ S3 resume");
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed after CS/S3 resume");
            else
                Log.Fail("PSR Check Failed after CS/S3 resume");
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Initiating S4 and resuming back");

            base.EventResult(PowerStates.S4, base.InvokePowerEvent(new PowerParams() { Delay = 30, PowerStates = PowerStates.S4 }, PowerStates.S4));
            //this.InvokePowerEvent(new PowerParams() { Delay = 30, PowerStates = PowerStates.S4 }, PowerStates.S4);

            // After S4 resume, it will come back to AC if switched to DC programatically
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode (Switched back to DC)");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Checking PSR after S4 resume");
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPsrStatusResult(psrStatus, true))
                Log.Success("PSR Check Passed after S4 resume");
            else
                Log.Fail(true, "PSR Check Failed after S4 resume");
        }
    }
}
