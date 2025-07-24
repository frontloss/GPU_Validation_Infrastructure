using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_SwitchableGraphics_PSR_DIsplaySwitch : MP_SwitchableGraphics_PSR_Entry_Exit_Basic
    {

        List<DisplayType> externalDisplays = new List<DisplayType>();
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Checking displays requirement for this test");
            externalDisplays = base.displayPassedInCommandline;
            externalDisplays.Remove(DisplayType.EDP); // Just to have ony external display
            externalDisplays.ForEach(disp =>
            {
                Log.Message("Extrenal_Display(s): {0}", disp.ToString());
            });

            // this test needs more than 1 display. Check this first.
            if (externalDisplays.Count < 1)
                Log.Abort("SB_PSR_WithDisplaySwitch needs atleast 2 displays to execute");

            Log.Success("Continuing with the test as displays requirement is met");
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.ConfigType = DisplayConfigType.SD;
            displayConfig.PrimaryDisplay = externalDisplays[0];
            displayConfig.SecondaryDisplay = DisplayType.None;
            displayConfig.TertiaryDisplay = DisplayType.None;

            Log.Message(true, "Checking PSR disable with {0}", displayConfig.GetCurrentConfigStr());
            base.ApplyConfigOS(displayConfig);

            Thread.Sleep(2000);

            // Check PSR
            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = displayConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
            if (psrStatus.psrWorkingState < PsrWorkingState.PsrEnabledButNotWorking)
            {
                Log.Success("PSR is disabled in SD {0}", externalDisplays[0].ToString());
            }
            else
            {
                Log.Fail("PSR is enabled in SD {0}", externalDisplays[0].ToString());
            }
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Set SD eDP config via OS call and Check PSR");
            ApplySDConfigNativeModeOnEdp();

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = currentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPSRStatusResult(psrStatus))
                Log.Success("PSR Check Passed");
            else
                Log.Fail("PSR Check Failed");
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            if (externalDisplays.Count > 1)
            {
                DisplayConfig displayConfig = new DisplayConfig();
                displayConfig.ConfigType = DisplayConfigType.SD;
                displayConfig.PrimaryDisplay = externalDisplays[1];
                displayConfig.SecondaryDisplay = DisplayType.None;
                displayConfig.TertiaryDisplay = DisplayType.None;

                Log.Message(true, "Checking PSR disable in {0}", displayConfig.GetCurrentConfigStr());
                base.ApplyConfigOS(displayConfig);

                Thread.Sleep(2000);

                // Check PSR
                PsrTestInput psrTestInput = new PsrTestInput();
                psrTestInput.captureIntervalInSec = iTestRunDuration;
                psrTestInput.currentConfig = displayConfig;
                psrTestInput.psrEventType = PsrEventType.Default;
                PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
                if (psrStatus.psrWorkingState < PsrWorkingState.PsrEnabledButNotWorking)
                {
                    Log.Success("PSR is disabled in {0}", displayConfig.GetCurrentConfigStr());
                }
                else
                {
                    Log.Fail("PSR is enabled in {0}", displayConfig.GetCurrentConfigStr());
                }
            }
            else
            {
            }
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Skipping this as config specified has only one extrenal display");

            if (externalDisplays.Count > 1)
            {
                Log.Message(true, "Set SD eDP config via OS call and Check PSR");
                ApplySDConfigNativeModeOnEdp();

                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                PsrTestInput psrTestInput = new PsrTestInput();
                psrTestInput.captureIntervalInSec = iTestRunDuration;
                psrTestInput.currentConfig = currentConfig;
                psrTestInput.psrEventType = PsrEventType.Default;
                PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

                if (PrintPSRStatusResult(psrStatus))
                    Log.Success("PSR Check Passed");
                else
                    Log.Fail("PSR Check Failed");
            }
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.ConfigType = DisplayConfigType.DDC;
            displayConfig.PrimaryDisplay = externalDisplays[0];
            displayConfig.SecondaryDisplay = DisplayType.EDP;
            displayConfig.TertiaryDisplay = DisplayType.None;

            Log.Message(true, "Checking PSR disable in {0}", displayConfig.GetCurrentConfigStr());
            base.ApplyConfigOS(displayConfig);

            Thread.Sleep(2000);

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = displayConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
            if (psrStatus.psrWorkingState < PsrWorkingState.PsrEnabledButNotWorking)
            {
                Log.Success("PSR is disabled in {0}", displayConfig.GetCurrentConfigStr());
            }
            else
            {
                Log.Fail("PSR is enabled in {0}", displayConfig.GetCurrentConfigStr());
            }
        }
        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            Log.Message(true, "Set SD eDP config via OS call and Check PSR");
            ApplySDConfigNativeModeOnEdp();

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = currentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPSRStatusResult(psrStatus))
                Log.Success("PSR Check Passed");
            else
                Log.Fail("PSR Check Failed");
        }
        [Test(Type = TestType.Method, Order = 11)]
        public void TestStep11()
        {
            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.ConfigType = DisplayConfigType.ED;
            displayConfig.PrimaryDisplay = DisplayType.EDP;
            displayConfig.SecondaryDisplay = externalDisplays[0];
            displayConfig.TertiaryDisplay = DisplayType.None;

            Log.Message(true, "Checking PSR disable in {0}", displayConfig.GetCurrentConfigStr());
            base.ApplyConfigOS(displayConfig);

            Thread.Sleep(2000);

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = displayConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
            if (psrStatus.psrWorkingState < PsrWorkingState.PsrEnabledButNotWorking)
            {
                Log.Success("PSR is disabled in {0}", displayConfig.GetCurrentConfigStr());
            }
            else
            {
                Log.Fail("PSR is enabled in {0}", displayConfig.GetCurrentConfigStr());
            }
        }
        [Test(Type = TestType.Method, Order = 12)]
        public void TestStep12()
        {
            Log.Message(true, "Set SD eDP config via OS call and Check PSR");
            ApplySDConfigNativeModeOnEdp();

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            PsrTestInput psrTestInput = new PsrTestInput();
            psrTestInput.captureIntervalInSec = iTestRunDuration;
            psrTestInput.currentConfig = currentConfig;
            psrTestInput.psrEventType = PsrEventType.Default;
            PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

            if (PrintPSRStatusResult(psrStatus))
                Log.Success("PSR Check Passed");
            else
                Log.Fail("PSR Check Failed");
        }
        [Test(Type = TestType.Method, Order = 13)]
        public void TestStep13()
        {
            if (externalDisplays.Count > 1)
            {
                DisplayConfig displayConfig = new DisplayConfig();
                displayConfig.ConfigType = DisplayConfigType.TDC;
                displayConfig.PrimaryDisplay = DisplayType.EDP;
                displayConfig.SecondaryDisplay = externalDisplays[0];
                displayConfig.TertiaryDisplay = externalDisplays[1];

                Log.Message(true, "Checking PSR disabe in {0}", displayConfig.GetCurrentConfigStr());
                base.ApplyConfigOS(displayConfig);

                Thread.Sleep(2000);

                PsrTestInput psrTestInput = new PsrTestInput();
                psrTestInput.captureIntervalInSec = iTestRunDuration;
                psrTestInput.currentConfig = displayConfig;
                psrTestInput.psrEventType = PsrEventType.Default;
                PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
                if (psrStatus.psrWorkingState < PsrWorkingState.PsrEnabledButNotWorking)
                {
                    Log.Success("PSR is disabled in {0}", displayConfig.GetCurrentConfigStr());
                }
                else
                {
                    Log.Fail("PSR is enabled in {0}", displayConfig.GetCurrentConfigStr());
                }
            }
            else
            {
                Log.Message(true, "Skipping this as config specified has only one external display");
            }
        }
        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
        {
            if (externalDisplays.Count > 1)
            {
                Log.Message(true, "Set SD eDP config via OS call and Check PSR");
                ApplySDConfigNativeModeOnEdp();

                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                PsrTestInput psrTestInput = new PsrTestInput();
                psrTestInput.captureIntervalInSec = iTestRunDuration;
                psrTestInput.currentConfig = currentConfig;
                psrTestInput.psrEventType = PsrEventType.Default;
                PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

                if (PrintPSRStatusResult(psrStatus))
                    Log.Success("PSR Check Passed");
                else
                    Log.Fail("PSR Check Failed");
            }
        }
        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            if (externalDisplays.Count > 1)
            {
                DisplayConfig displayConfig = new DisplayConfig();
                displayConfig.ConfigType = DisplayConfigType.TED;
                displayConfig.PrimaryDisplay = DisplayType.EDP;
                displayConfig.SecondaryDisplay = externalDisplays[0];
                displayConfig.TertiaryDisplay = externalDisplays[1];

                Log.Message(true, "Checking PSR disable in {0}", displayConfig.GetCurrentConfigStr());
                base.ApplyConfigOS(displayConfig);

                Thread.Sleep(2000);

                PsrTestInput psrTestInput = new PsrTestInput();
                psrTestInput.captureIntervalInSec = iTestRunDuration;
                psrTestInput.currentConfig = displayConfig;
                psrTestInput.psrEventType = PsrEventType.Default;
                PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);
                if (psrStatus.psrWorkingState < PsrWorkingState.PsrEnabledButNotWorking)
                {
                    Log.Success("PSR is disabled in {0}", displayConfig.GetCurrentConfigStr());
                }
                else
                {
                    Log.Fail("PSR is enabled in {0}", displayConfig.GetCurrentConfigStr());
                }
            }
            else
            {
                Log.Message(true, "Skipping this as config specified has only one external display");
            }
        }
        [Test(Type = TestType.Method, Order = 16)]
        public void TestStep16()
        {
            if (externalDisplays.Count > 1)
            {
                Log.Message(true, "Set SD eDP config via OS call and Check PSR");
                ApplySDConfigNativeModeOnEdp();

                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                PsrTestInput psrTestInput = new PsrTestInput();
                psrTestInput.captureIntervalInSec = iTestRunDuration;
                psrTestInput.currentConfig = currentConfig;
                psrTestInput.psrEventType = PsrEventType.Default;
                PsrStatus psrStatus = AccessInterface.GetFeature<PsrStatus, PsrTestInput>(Features.PSR1, Action.GetMethod, Source.AccessAPI, psrTestInput);

                if (PrintPSRStatusResult(psrStatus))
                    Log.Success("PSR Check Passed");
                else
                    Log.Fail("PSR Check Failed");
            }
        }
    
    }
}
