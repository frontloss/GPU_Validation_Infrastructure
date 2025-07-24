namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;
    using System.Threading;

    [Test(Type = TestType.HasReboot)]
    class MP_SwitchableGraphics_TDR_TestConfigChange : MP_SwitchableGraphics_Base
    {
        DisplayConfig displayWrapper = null;
        private Dictionary<int, Action<List<DisplayConfig>>> _switchPatternList = null;

        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Connect the displays planned in the grid");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                List<uint> winMonitorIDList = base.ListEnumeratedDisplays();
                List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
                if (!enumeratedWinMonIDList.Count.Equals(winMonitorIDList.Count) && !CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Verbose("Currently enumerated displays mismatch! A reboot is required.");
                    base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5, rebootReason = RebootReason.DriverModify }, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayConfig cuiDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.SDKConfig, Action.Get);
            if (cuiDisplayConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
            {
                Log.Success("All Displays are enumerated in CUI");
            }
            else
            {
                Log.Fail("All Displays are not enumerated in CUI, current config is {0}", cuiDisplayConfig.ToString());
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            RunTDRNVerify(true, 2);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            this.TestStep1();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Set all possible display configurations with displays planned in grid");
            DisplayConfig currentCUIConfig = null;
            List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);
            switchPatternList.ForEach(dC =>
            {
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC))
                {
                    currentCUIConfig = AccessInterface.GetFeature<DisplayConfig>(Features.SDKConfig, Action.Get);
                    if (dC.GetCurrentConfigStr().Equals(currentCUIConfig.GetCurrentConfigStr()))
                        Log.Success("The driver is able to Config {0} successfully. Verified through CUI and OS", dC.GetCurrentConfigStr());
                    else
                        Log.Fail("Failure in applying Config , expected  {0}, CUI shows {1}", dC.GetCurrentConfigStr(), currentCUIConfig.GetCurrentConfigStr());
                }
            });
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            TestStep1();
        }
        private void RunTDRNVerify(bool argIsLogMessageParent, int argOverrideIdx)
        {
            Log.Message(argIsLogMessageParent, "Run ForceTDR.exe as given in note, 'To Run TDR Application'");
            if (this.RunTDR(argOverrideIdx))
                Log.Success("TDR Successful");
            else
                Log.Fail(false, "TDR Unsuccessful!");
        }
        private bool RunTDR(int argOverrideIdx)
        {
            Log.Verbose("Running TDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true, "TDR unsuccessful! A reboot may be required.");
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5, rebootReason = RebootReason.DriverModify }, PowerStates.S5);
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
        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);
        }
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);
        }
        private Dictionary<int, Action<List<DisplayConfig>>> SwitchPatternList
        {
            get
            {
                if (null == this._switchPatternList)
                {
                    this._switchPatternList = new Dictionary<int, Action<List<DisplayConfig>>>();
                    this._switchPatternList.Add(2, this.GetSwitchPatternForDualDisplayMode);
                    this._switchPatternList.Add(3, this.GetSwitchPatternForTriDisplayMode);
                }
                return this._switchPatternList;
            }
        }
    }
}