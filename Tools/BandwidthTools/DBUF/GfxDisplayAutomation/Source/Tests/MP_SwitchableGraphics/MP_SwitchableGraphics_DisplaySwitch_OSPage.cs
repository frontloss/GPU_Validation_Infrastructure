namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;

    class MP_SwitchableGraphics_DisplaySwitch_OSPage : MP_SwitchableGraphics_Base
    {
        private Dictionary<int, Action<List<DisplayConfigWrapper>>> _switchPatternList = null;
        private bool _isCUIOpen = false;

        protected System.Action _additionalActionHandler = null;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (base.CurrentConfig.CustomDisplayList.Count == 1)
                Log.Abort("DisplaySwitch_OSPage test requires atleast 2 displays connected!");

            DisplayConfig currentCUIConfig = null;
            DisplayConfig currentOSPageConfig = null;
            List<DisplayConfigWrapper> switchPatternList = new List<DisplayConfigWrapper>();

            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);

            switchPatternList.ForEach(dC =>
            {
                if (dC.UseCUI)
                {
                    this.OpenCUI();
                    AccessInterface.SetFeature<DisplayConfig>(Features.Config, Action.Set, Source.AccessUI, dC.DispConfig);
                    if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                        AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);

                    currentCUIConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessUI);
                    if (!dC.DispConfig.GetCurrentConfigStr().Equals(currentCUIConfig.GetCurrentConfigStr()))
                    {
                        Log.Sporadic("Config not set through CUI! Expected {0}, but was {1}", dC.DispConfig.GetCurrentConfigStr(), currentCUIConfig.GetCurrentConfigStr());

                        AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
                        this._isCUIOpen = false;
                        this.OpenCUI();

                        Log.Verbose("Reapplying config through CUI {0}", dC.DispConfig.GetCurrentConfigStr());
                        AccessInterface.SetFeature<DisplayConfig>(Features.Config, Action.Set, Source.AccessUI, dC.DispConfig);
                        if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                            AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);
                    }
                }
                else
                    AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC.DispConfig);
                Thread.Sleep(5000);
                if (VerifyCuiOsDispConfig(dC.DispConfig, out currentCUIConfig, out currentOSPageConfig))
                    Log.Success("Switch successful to : {0}", dC.DispConfig.GetCurrentConfigStr());
                else
                {
                    Log.Fail("Switch failed to {0}. Current OS Config {1} . Current CUI Config {2}  ", dC.DispConfig.GetCurrentConfigStr(), currentOSPageConfig.GetCurrentConfigStr(), currentCUIConfig.GetCurrentConfigStr());
                    this.EnumeratedDisplaysHandler();
                }

            });
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            if (null != this._additionalActionHandler)
                this._additionalActionHandler();
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
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
            if (!enumeratedWinMonIDList.Count.Equals(winMonitorIDList.Count))
            {
                Log.Verbose("Currently enumerated display list [{0}] mismatch with windows monitor id list [{1}]! A reboot is required.", enumeratedWinMonIDList.Count, winMonitorIDList.Count);
                base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5, rebootReason = RebootReason.DriverModify }, PowerStates.S5);
            }
        }
        private void OpenCUI()
        {
            if (!this._isCUIOpen)
            {
                if (AccessInterface.SetFeature<bool>(Features.LaunchCUI, Action.SetNoArgs))
                {
                    Log.Success("CUI Launched Successfully");
                    AccessInterface.Navigate(Features.Config);
                    this._isCUIOpen = true;
                }
                else
                    Log.Abort("Error in launching CUI");
            }
        }
        private int _retry = 0;
        private bool VerifyCuiOsDispConfig(DisplayConfig argDispConfig, out DisplayConfig argCUIConfig, out DisplayConfig argOSPageConfig)
        {
            this.OpenCUI();
            argCUIConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessUI);
            argOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);

            if (argDispConfig.GetCurrentConfigStr().Equals(argCUIConfig.GetCurrentConfigStr()) && argDispConfig.GetCurrentConfigStr().Equals(argOSPageConfig.GetCurrentConfigStr()))
                return true;
            else
            {
                if (_retry.Equals(0))
                {
                    Log.Sporadic("Switch failed to {0}. Current OS Config {1} . Current CUI Config {2}  ", argDispConfig.GetCurrentConfigStr(), argOSPageConfig.GetCurrentConfigStr(), argCUIConfig.GetCurrentConfigStr());
                    _retry++;
                    this._isCUIOpen = false;
                    AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
                    return this.VerifyCuiOsDispConfig(argDispConfig, out argCUIConfig, out argOSPageConfig);
                }
                else
                    return false;
            }
        }
        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfigWrapper> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");
            DisplayConfigWrapper displayWrapper = null;

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);
        } // End GetSwitchPatternForDualDisplayMode
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfigWrapper> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");
            DisplayConfigWrapper displayWrapper = null;

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay }, true);
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay }, true);
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay }, true);
            argList.Add(displayWrapper);
        } // End GetSwitchPatternForTriDisplayMode 
        private Dictionary<int, Action<List<DisplayConfigWrapper>>> SwitchPatternList
        {
            get
            {
                if (null == this._switchPatternList)
                {
                    this._switchPatternList = new Dictionary<int, Action<List<DisplayConfigWrapper>>>();
                    this._switchPatternList.Add(2, this.GetSwitchPatternForDualDisplayMode);
                    this._switchPatternList.Add(3, this.GetSwitchPatternForTriDisplayMode);
                }
                return this._switchPatternList;
            }
        }
    } // End MP_DisplaySwitch_OSPage class
}