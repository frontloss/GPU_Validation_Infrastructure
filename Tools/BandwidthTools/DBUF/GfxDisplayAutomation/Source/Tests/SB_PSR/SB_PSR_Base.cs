namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.IO;
    using System.Windows.Forms;

    public delegate void PSRCaptureDelegate();

    public class SB_PSR_Base : TestBase
    {
        protected int iTestRunDuration = 30;
        protected bool bIsDMCEnabled = true;

        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }

        protected bool VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            bool status = true;
            // Verifying config via OS
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
            {
                Log.Success("Config {0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
            }
            else
            {
                status = false;
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
            }
            return status;
        }

        protected bool ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
            {
                Log.Message("Successfully applied the mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
                return true;
            }
            else
            {
                Log.Fail("Failed to apply the mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
                return false;
            }
        }

        protected void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            // Verify the mode through OS
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
            {
                Log.Success("Mode chosen {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }

        protected void EnableDisableCursor(bool enable)
        {
            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.ShowCursor);
            if (enable == false)
                driverParams.FunctionName = SetUpDesktopArgs.SetUpDesktopOperation.HideCursor;

            if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
                Log.Fail("Failed to {0} Cursor", enable ? "enable" : "disable");
        }

        protected List<DisplayMode> GetModesForTest(DisplayType pDisplayType)
        {
            List<DisplayType> displays = new List<DisplayType>();
            displays.Add(pDisplayType);
            List<DisplayModeList> displayModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, displays);
            List<DisplayMode> dispModes = displayModeList.Where(dML => dML.display == pDisplayType).Select(dML => dML.supportedModes).FirstOrDefault();
            return dispModes;
        }

        protected void ApplyNativeModeOnEdp()
        {
            Log.Message("Applying native mode on eDP");

            // Finding Native Mode (get all modes and last mode is th native)
            List<DisplayMode> displayModes = GetModesForTest(DisplayType.EDP);

            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayModes.Last()))
                Log.Success("Native mode is applied on eDP");
            else
                Log.Fail("Failed to apply native mode on eDP");
        }

        protected void ApplySDConfigNativeModeOnEdp()
        {
            Log.Message("Applying SD config, Native mode on eDP");

            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.ConfigType = DisplayConfigType.SD;
            displayConfig.PrimaryDisplay = DisplayType.EDP;
            displayConfig.SecondaryDisplay = DisplayType.None;
            displayConfig.TertiaryDisplay = DisplayType.None;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Successfully applied the config: {0}", displayConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to apply the config: {0}", displayConfig.GetCurrentConfigStr());

            ApplyNativeModeOnEdp();
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

        protected bool PrintPsrStatusResult(PsrStatus psrStatus, bool bIsLegacyPSR)
        {
            bool bRetVal = true;
            string strPsrVersion = "PSR";
            string strPsrCountString = "PSR Active Count";
            string strPsrPerfString = "PSR Perf Count";
            if(!bIsLegacyPSR)
            {
                strPsrVersion = "PSR2";
                strPsrCountString = "PSR2 Deep Sleep Count";
                strPsrPerfString = "PSR2 Perf Count";
            }
            if(psrStatus.psrWorkingState == PsrWorkingState.PsrEnabledAndWorkingProperly)
            {
                Log.Success("{0} Passed ({1} = {2})", strPsrVersion, strPsrCountString, (psrStatus.psrCapturedData.currentEntryExitCount.ToString()));
            }
            else if (psrStatus.psrWorkingState == PsrWorkingState.PsrEnabledButLessEntryExitCount)
            {
                Log.Success("{0} Passed with less count ({1} = {2})", strPsrVersion, strPsrCountString, (psrStatus.psrCapturedData.currentEntryExitCount.ToString()));
            }
            else
            {
                Log.Fail("{0} Failed ({1} = {2}", strPsrVersion, strPsrCountString, (psrStatus.psrCapturedData.currentEntryExitCount.ToString()));
                bRetVal = false;
            }

            Platform platform = base.MachineInfo.PlatformDetails.Platform;
            if (platform != Platform.VLV && platform != Platform.CHV)
            {
                if(bIsDMCEnabled && !(platform == Platform.HSW))
                {
                    Log.Message(strPsrVersion + " residency check is skipped as DMC (c9) is enabled (Counter doesn\'t work)");
                }
                else
                {
                    if(psrStatus.psrCapturedData.currentResidencyTime >= psrStatus.psrCapturedData.requiredResidencyTime) // residency value comes les due to HW optimization
                    {
                        Log.Success("{0} residency check passed ({1} = {2}ms)", strPsrVersion, strPsrPerfString, psrStatus.psrCapturedData.currentResidencyTime);
                    }
                    else
                    {
                        Log.Fail("{0} residency check failed ({1} = {2}ms)", strPsrVersion, strPsrPerfString, psrStatus.psrCapturedData.currentResidencyTime);
                        bRetVal = false;
                    }
                }
            }
            return bRetVal;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            Log.Message(true, "Checking/ Setting Preconditions for test");
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.EDP))
                Log.Abort("PSR test should be run with eDP");

            iTestRunDuration = 17;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            Log.Message("Set SD eDP config");
            ApplySDConfigNativeModeOnEdp();

            Log.Message("Enable DC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Abort("Fail to set DC Mode ==> Aborting the test");
            }
            else
                Log.Success("System is Running in DC Mode");

            // Disable balloon notification (Enable at the end)
        }
    }
}
