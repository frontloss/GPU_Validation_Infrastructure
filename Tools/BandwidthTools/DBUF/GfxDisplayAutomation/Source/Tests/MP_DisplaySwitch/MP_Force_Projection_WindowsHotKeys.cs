namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    class WinPParams
    {
        private int _tabCount = 1;

        internal CharmBarOptions CharmOptions { get; set; }
        internal DisplayUnifiedConfig UnifiedConfigType { get; set; }
        internal int TabCount
        {
            get { return this._tabCount; }
            set { this._tabCount = value; }
        }
        internal bool AdditionalTab { get; set; }
    }

    internal enum CharmBarOptions
    {
        PCScreenOnly,
        Duplicate,
        Extend,
        SecondScreenOnly
    }
    class MP_Force_Projection_WindowsHotKeys : TestBase
    {
        private List<WinPParams> _myDictionary = null;
        private uint _flagRetry = 0;
        private DisplayType _displayType = DisplayType.None;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Check if the no of displays connected is more than two and EDP is connected ");
            Log.Message("Check if the number of displays is more than 1");
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("This test requires atleast two displays connected...");

            Log.Message("Verify EDP/MIPI is connected ");
            this._displayType = base.CurrentConfig.DisplayList.FirstOrDefault(dT => (dT == DisplayType.EDP || dT == DisplayType.MIPI));
            if (this._displayType != DisplayType.None)
                Log.Success("{0} is connected..test continues", this._displayType);
            else
                Log.Abort("EDP/MIPI is not connected..Aborting the test");
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (base.MachineInfo.OS.Type == OSType.WINBLUE)
                ApplyPreConfigWinTh();

            Log.Message(true, "Set the Configuration to SD {0}", this._displayType);
            DisplayConfig displayConfig = new DisplayConfig();
            displayConfig.ConfigType = DisplayConfigType.SD;
            displayConfig.PrimaryDisplay = this._displayType;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Config (SD {0}) applied successfully", this._displayType);
            else
                Log.Abort("Config (SD {0}) not applied!", this._displayType);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            this._myDictionary = new List<WinPParams>()
            {
                new WinPParams() { CharmOptions = CharmBarOptions.Duplicate, UnifiedConfigType = DisplayUnifiedConfig.Clone },
                new WinPParams() { CharmOptions = CharmBarOptions.Extend, UnifiedConfigType = DisplayUnifiedConfig.Extended },
                new WinPParams() { CharmOptions = CharmBarOptions.PCScreenOnly, UnifiedConfigType = DisplayUnifiedConfig.Single, TabCount = base.MachineInfo.OS.IsGreaterThan(OSType.WINTHRESHOLD)? 3 : 2 },
                new WinPParams() { CharmOptions = CharmBarOptions.SecondScreenOnly, UnifiedConfigType = DisplayUnifiedConfig.Single, TabCount = 3, AdditionalTab = base.MachineInfo.PlatformDetails.Platform.ToString().Equals(Platform.VLV.ToString()) }
            };

            DisplayConfig currentConfig = null;

            this._myDictionary.ForEach(winP =>
            {
                Log.Message(true, "Applying {0} through Win + P", winP.CharmOptions);
                AccessInterface.SetFeature<int>(Features.LaunchCharmWindow, Action.Set, winP.TabCount);
                if (winP.AdditionalTab)
                    AccessInterface.SetFeature<bool>(Features.LaunchCharmWindow, Action.SetNoArgs);
                Log.Message("Checking if the config changes correctly for {0}", winP.CharmOptions);
                currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                if (VerifyConfigApplied(currentConfig, winP))
                    Log.Success("The config has been sucessfully applied");
                else
                    Log.Fail(false, "Error in applying config...");
            });
        }
        private bool VerifyConfigApplied(DisplayConfig currentConfig, WinPParams argWinPParams)
        {
            //CharmBarOptions charmbar = (CharmBarOptions)Enum.Parse(typeof(CharmBarOptions), dT);
            //DisplayUnifiedConfig unifiedConfigFromDict = _myDictionary[charmbar];
            Log.Message("Unified config from dictionary = {0} ", argWinPParams.UnifiedConfigType);
            DisplayUnifiedConfig unifiedConfigFromOS = DisplayExtensions.GetUnifiedConfig(currentConfig.ConfigType);
            Log.Message("Unified config from OS Page = {0} ", unifiedConfigFromOS);
            if (unifiedConfigFromOS != argWinPParams.UnifiedConfigType && argWinPParams.CharmOptions != CharmBarOptions.SecondScreenOnly)
            {
                Log.Sporadic(false, "Config from the Win+P is {0} whereas the config from OS Page is {1}. Trying again.", argWinPParams.UnifiedConfigType, unifiedConfigFromOS);
                return (Retry(currentConfig, argWinPParams));
            }
            else
            {
                _flagRetry = 0;
                if (argWinPParams.CharmOptions == CharmBarOptions.SecondScreenOnly)
                {
                    if (currentConfig.CustomDisplayList.Contains(this._displayType))
                    {
                        Log.Fail(false, "CharmBar shows {0} and the current config is {1}", argWinPParams.CharmOptions, currentConfig.GetCurrentConfigStr());
                        return false;
                    }
                    Log.Success("CharmBar shows {0} and the current config is {1}", argWinPParams.CharmOptions, currentConfig.GetCurrentConfigStr());

                }
                else if (argWinPParams.UnifiedConfigType == DisplayUnifiedConfig.Single)
                    return (CheckDisplayForSingle(currentConfig, argWinPParams.CharmOptions));
                else
                {
                    Log.Success("CharmBar {0} matches with OS config type {1}", argWinPParams.CharmOptions, unifiedConfigFromOS);
                    DisplayInfo currentDisplayInfo = null;
                    List<DisplayModeList> displayModeList_OSPage = new List<DisplayModeList>();
                    List<DisplayMode> testModes = null;
                    displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, currentConfig.CustomDisplayList);

                    if (!displayModeList_OSPage.Count.Equals(0))
                    {
                        displayModeList_OSPage.ForEach(dML =>
                        {
                            currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                            testModes = this.TestModes(dML.supportedModes);
                            testModes.ForEach(dM => this.ApplyAndVerify(dM, currentDisplayInfo));
                        });
                    }
                    else
                        Log.Fail(false, "No modes returned!");
                }
            }
            return true;
        }

        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            return testModes;
        }

        private bool ApplyAndVerify(DisplayMode argDispMode, DisplayInfo argDisplayInfo)
        {
            Log.Message(true, "Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
            {
                Log.Fail("Fail to apply Mode");
                return false;
            }
            else
                Log.Success("Mode applied successfully");

            DisplayMode currentDisplayMode_OSPage = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, argDisplayInfo);
            if (GetModeStr(argDispMode).Equals(GetModeStr(currentDisplayMode_OSPage)))
                Log.Success("OSPage and CUI are in sync {0}", GetModeStr(argDispMode));
            else
            {
                Log.Fail("Applied Mode {0}. Current OS Page Mode : {1}", GetModeStr(argDispMode), GetModeStr(currentDisplayMode_OSPage));
                return false;
            }
            return true;
        }
        private string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
        }
        private bool Retry(DisplayConfig currentConfig, WinPParams argWinPParams)
        {
            _flagRetry++;
            if (_flagRetry > 3)
            {
                Log.Fail(false, "Failed in resetting config more than thrice. Os page shows {0}, Charm Window shows {1}", DisplayExtensions.GetUnifiedConfig(currentConfig.ConfigType), argWinPParams.CharmOptions);
                _flagRetry = 0;
                return false;
            }
            else
            {
                AccessInterface.SetFeature<int>(Features.LaunchCharmWindow, Action.Set, argWinPParams.TabCount);
                if (argWinPParams.AdditionalTab)
                    AccessInterface.SetFeature<bool>(Features.LaunchCharmWindow, Action.SetNoArgs);
                DisplayConfig currentRetryConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                return (VerifyConfigApplied(currentRetryConfig, argWinPParams));
            }
        }
        private bool CheckDisplayForSingle(DisplayConfig currentConfig, CharmBarOptions charmBar)
        {
            if ((charmBar == CharmBarOptions.PCScreenOnly) && (currentConfig.PrimaryDisplay != this._displayType))
            {
                Log.Fail(false, "CharmBar shows {0} and the DisplayType is {1}", charmBar, currentConfig.PrimaryDisplay);
                return false;
            }
            if ((charmBar == CharmBarOptions.SecondScreenOnly) && (currentConfig.PrimaryDisplay == this._displayType))
            {
                Log.Fail(false, "CharmBar shows {0} and the DisplayType is {1}", charmBar, currentConfig.PrimaryDisplay);
                return false;
            }
            Log.Success("CharmBar shows {0} and the DisplayType is {1}", charmBar, currentConfig.PrimaryDisplay);
            return true;
        }

        private void ApplyPreConfigWinTh()
        {
            DisplayConfig _displayConfig = new DisplayConfig();
            _displayConfig.PrimaryDisplay = this.CurrentConfig.CustomDisplayList[0];
            _displayConfig.SecondaryDisplay = this.CurrentConfig.CustomDisplayList[1];
            if (this.CurrentConfig.ConfigTypeCount == 3)
            {
                Log.Message("Set the initial configuration as TDC ");
                _displayConfig.ConfigType = DisplayConfigType.TDC;
                _displayConfig.TertiaryDisplay = this.CurrentConfig.CustomDisplayList[2];
            }
            else
            {
                Log.Message("Set the initial configuration as DDC ");
                _displayConfig.ConfigType = DisplayConfigType.DDC;
            }

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, _displayConfig))
                Log.Success("Config {0} applied successfully", _displayConfig);
            else
                Log.Alert("Problem while applying {0} ", _displayConfig);
        }
    }
}
