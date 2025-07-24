namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.IO;
    using System.Windows.Forms;

    public delegate void DSRCaptureDelegate();

    public class SB_DSR_Base : TestBase
    {
        protected int iTestRunDuration = 30;

        protected List<DisplayMode> GetModesForTest(DisplayType pDisplayType)
        {
            List<DisplayType> displays = new List<DisplayType>();
            displays.Add(pDisplayType);
            List<DisplayModeList> displayModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, displays);
            List<DisplayMode> dispModes = displayModeList.Where(dML => dML.display == pDisplayType).Select(dML => dML.supportedModes).FirstOrDefault();
            return dispModes;
        }

        protected void ApplyNativeModeOnMipi()
        {
            Log.Message("Applying native mode on MIPI");

            // Finding Native Mode (get all modes and last mode is th native)
            List<DisplayMode> displayModes = GetModesForTest(DisplayType.MIPI);

            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayModes.Last()))
                Log.Success("Native mode is applied on MIPI");
            else
                Log.Fail("Failed to apply native mode on MIPI");
        }

        protected void ApplySDConfigNativeModeOnMipi()
        {
            Log.Message("Applying SD config, Native mode on MIPI");

            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.ConfigType = DisplayConfigType.SD;
            displayConfig.PrimaryDisplay = DisplayType.MIPI;
            displayConfig.SecondaryDisplay = DisplayType.None;
            displayConfig.TertiaryDisplay = DisplayType.None;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Successfully applied the config: {0}", displayConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to apply the config: {0}", displayConfig.GetCurrentConfigStr());

            ApplyNativeModeOnMipi();
        }

        protected bool RunTDR()
        {
            Log.Message("Running TDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true, "TDR unsuccessful! A reboot may be required.");
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
            }
            else
            {
                CommonExtensions.ClearRetryThruRebootFile();
                return true;
            }
            return false;
        }

        protected bool PrintDSRStatResult(DsrStat dsrStat)
        {
            bool bRetVal = true;

            Log.Verbose(string.Format("Mode = {0}", dsrStat.dsrCapturedData.currentDsrMode));
            if(dsrStat.dsrWorkingState == DsrWorkingState.DsrEnabledAndWorkingProperly)
            {
                Log.Success("DSR Passed (DSR Entry Exit Count = " + (dsrStat.dsrCapturedData.currentEntryExitCount.ToString()) + " )");
            }
            else if (dsrStat.dsrWorkingState == DsrWorkingState.DsrEnabledButLessEntryExitCount)
            {
                Log.Success("DSR Passed with less count (DSR Entry Exit Count = " + (dsrStat.dsrCapturedData.currentEntryExitCount.ToString()) + " )");
            }
            else
            {
                Log.Fail("DSR Failed (DSR Entry Exit Count = " + (dsrStat.dsrCapturedData.currentEntryExitCount.ToString()) + " )");
                bRetVal = false;
            }

            return bRetVal;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Checking/ Setting Preconditions for test");

            iTestRunDuration = 12;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message("Set SD MIPI config");
            ApplySDConfigNativeModeOnMipi();

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
        }
    }
}
