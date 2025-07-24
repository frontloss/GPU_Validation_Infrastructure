namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Threading;

    class SB_DSR_Basic : SB_DSR_Base
    {
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Initial DSR Check...");

            // Initializing base current config to SD MIPI for DSR
            base.CurrentConfig.ConfigType = DisplayConfigType.SD;
            base.CurrentConfig.PrimaryDisplay = DisplayType.MIPI;
            base.CurrentConfig.SecondaryDisplay = DisplayType.None;
            base.CurrentConfig.TertiaryDisplay = DisplayType.None;

            DsrInput dsrInput = new DsrInput();
            dsrInput.captureIntervalInSec = iTestRunDuration;
            dsrInput.currentConfig = base.CurrentConfig;
            dsrInput.dsrEventType = PsrEventType.Default;
            DsrStat dsrStat = AccessInterface.GetFeature<DsrStat, DsrInput>(Features.DSR, Action.GetMethod, Source.AccessAPI, dsrInput);

            PrintDSRStatResult(dsrStat);
        }

    }
}
