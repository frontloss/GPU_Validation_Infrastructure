namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Threading;

    class SB_PSR_InAllResolutions : SB_PSR_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            List<DisplayMode>  eDpAllModes = GetModesForTest(DisplayType.EDP);

            foreach (DisplayMode dispMode in eDpAllModes)
            {
                Log.Message(true, "Checking PSR in the mode {0}", dispMode.GetCurrentModeStr(false));

                bool modeRet = base.ApplyModeOS(dispMode, DisplayType.EDP);

                Thread.Sleep(3000); // 3sec Breather
                //base.VerifyModeOS(dm, dm.display);

                if(modeRet)
                {
                    PsrTestInput psrTestInput = new PsrTestInput();
                    psrTestInput.captureIntervalInSec = iTestRunDuration;
                    psrTestInput.currentConfig = base.CurrentConfig;
                    psrTestInput.psrEventType = PsrEventType.Default;
                    PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

                    if (PrintPsrStatusResult(psrStatus, true))
                        Log.Success("PSR Check Passed in the mode {0}", dispMode.GetCurrentModeStr(false));
                    else
                        Log.Fail(true, "PSR Check Failed in the mode {0}", dispMode.GetCurrentModeStr(false));
                }
                else
                {
                    Log.Verbose("Mode set failed... Skipping PSR Check for {0}", dispMode.GetCurrentModeStr(false));
                }
            }

        }

    }
}
