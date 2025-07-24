namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;

    public class MP_DisplaySwitch_OSPage : TestBase
    {
        private Dictionary<int, Action<List<DisplayConfig>>> _switchPatternList = null;
        //private bool _isCUIOpen = false;

        protected System.Action _additionalActionHandler = null;

        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {
            if (base.CurrentConfig.CustomDisplayList.Count == 1)
                Log.Abort("DisplaySwitch_OSPage test requires atleast 2 displays connected!");

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
                    Log.Success("Switch successful to : {0} and verified from OS page", dC.GetCurrentConfigStr());
                }
                else
                {
                    Log.Fail("Switch Unsucessful to : {0} when verified from OS page", dC.GetCurrentConfigStr());
                    this.EnumeratedDisplaysHandler();
                }
                Thread.Sleep(5000);
                if (VerifyCuiDispConfig(dC))
                    Log.Success("Switch successful to : {0} and verified from CUI page", dC.GetCurrentConfigStr());
                else
                {
                    Log.Fail("Switch Unsucessful to : {0} when verified from CUI page", dC.GetCurrentConfigStr());
                    this.EnumeratedDisplaysHandler();
                }
            });
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (null != this._additionalActionHandler)
                this._additionalActionHandler();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            if (null != this._additionalActionHandler)
            {
                Log.Verbose("Test Cleanup");
                base.ListEnumeratedDisplays();
            }
        }
        private void EnumeratedDisplaysHandler()
        {
            List<uint> winMonitorIDList = base.ListEnumeratedDisplays();
            List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
            if (!enumeratedWinMonIDList.Count.Equals(winMonitorIDList.Count) && !CommonExtensions.HasRetryThruRebootFile())
            {
                Log.Verbose("Currently enumerated display list [{0}] mismatch with windows monitor id list [{1}]! A reboot is required.", enumeratedWinMonIDList.Count, winMonitorIDList.Count);
                CommonExtensions.WriteRetryThruRebootInfo();
                base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
            }
            else
                TestStep2();

        }
        private int _retry = 0;
        private bool VerifyCuiDispConfig(DisplayConfig argDispConfig)
        {
            DisplayConfig argCUIConfig = null;
            argCUIConfig = AccessInterface.GetFeature<DisplayConfig>(Features.SDKConfig, Action.Get);

            if (argDispConfig.GetCurrentConfigStr().Equals(argCUIConfig.GetCurrentConfigStr()))
                return true;
            else
            {
                if (_retry.Equals(0))
                {
                    Log.Sporadic("Switch failed to {0} Current CUI Config {1}  ", argDispConfig.GetCurrentConfigStr(),argCUIConfig.GetCurrentConfigStr());
                    _retry++;
                    return this.VerifyCuiDispConfig(argDispConfig);
                }
                else
                    return false;
            }
        }
        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");
            DisplayConfig displayconfig = null;

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayconfig);
        } // End GetSwitchPatternForDualDisplayMode
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");
            DisplayConfig displayconfig = null;

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayconfig);

            displayconfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayconfig);
        } // End GetSwitchPatternForTriDisplayMode 
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
    } // End MP_DisplaySwitch_OSPage class
}