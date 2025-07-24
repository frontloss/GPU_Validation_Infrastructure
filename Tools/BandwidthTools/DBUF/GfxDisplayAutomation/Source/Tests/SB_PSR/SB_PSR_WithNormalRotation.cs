namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Threading;
    using System.Linq;

    class SB_PSR_WithNormalRotation : SB_PSR_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            uint[] rotAngles = new uint[] {90, 180, 270, 0, 270, 180, 90, 0};

            foreach (var angle in rotAngles)
            {
                Log.Message(true, "Checking PSR in the rotation angle {0}", angle);

                // Finding Native Mode (get all modes and last mode is th native)
                List<DisplayMode> displayModes = GetModesForTest(DisplayType.EDP);
                DisplayMode nativMode = displayModes.Last();
                nativMode.Angle = angle;
                if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, nativMode))
                {
                    Log.Success("Mode with rotation angle {0} is applied on eDP, checking PSR", angle);
                    Thread.Sleep(2000);

                    PsrTestInput psrTestInput = new PsrTestInput();
                    psrTestInput.captureIntervalInSec = iTestRunDuration;
                    psrTestInput.currentConfig = base.CurrentConfig;
                    psrTestInput.psrEventType = PsrEventType.Default;
                    PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

                    if (PrintPsrStatusResult(psrStatus, true))
                        Log.Success("PSR Check Passed in the rotation angle {0}", angle);
                    else
                        Log.Fail(true, "PSR Check Failed in the rotation angle {0}", angle);
                }
                else
                    Log.Verbose("Failed to apply mode with the rotation angle {0} on eDP, Skipping PSR check", angle);
                
            }

        }
    }
}
