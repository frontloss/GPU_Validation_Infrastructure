namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Threading;

    class SB_PSR_Basic : SB_PSR_Base
    {
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            Log.Message(true, "Initial PSR Check...");

            // Initializing base current config to SD EDP for PSR
            base.CurrentConfig.ConfigType = DisplayConfigType.SD;
            base.CurrentConfig.PrimaryDisplay = DisplayType.EDP;
            base.CurrentConfig.SecondaryDisplay = DisplayType.None;
            base.CurrentConfig.TertiaryDisplay = DisplayType.None;

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = base.CurrentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            PrintPsrStatusResult(psrStatus, true);
        }

    }
}
