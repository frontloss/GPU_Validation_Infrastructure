using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace Intel.VPG.Display.Automation
{
    class MP_SwitchableGraphics_PSR_Entry_Exit_Basic : MP_SwitchableGraphics_Base
    {
        [Test(Type = TestType.PreCondition, Order = 1)]
        public virtual void TestStep1()
        {
            Log.Message(true, "Checking/ Setting Preconditions for test");
            iTestRunDuration = 12;
            displayPassedInCommandline = base.CurrentConfig.DisplayList;
            base.verifyEDPConnected();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            Log.Message("Set SD eDP config via OS call");
            ApplySDConfigNativeModeOnEdp();

            Log.Message("Enable DC Mode");
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

            // Disable balloon notification (Enable at the end)
        }

        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            Log.Message(true, "Initial PSR Check...");

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
            PrintPSRStatusResult(psrStatus);
        }
    
    }
}
