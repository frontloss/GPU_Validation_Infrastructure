namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;
    using System.Windows.Automation;
    using System.Windows;
    using System.IO;

    class SB_MODES_Change_Configuration_From_ConfigType : SB_MODES_Base
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();
        private Dictionary<DisplayConfigType, List<DisplayConfig>> _myDictionary = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Create a dictionary");
            DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig sdConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig tdcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig tedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            this._myDictionary = new Dictionary<DisplayConfigType, List<DisplayConfig>>();
            if (base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount() == 2)
            {
                this._myDictionary.Add(DisplayConfigType.DDC, new List<DisplayConfig> { ddcConfig, sdConfig, edConfig });
                this._myDictionary.Add(DisplayConfigType.SD, new List<DisplayConfig> { sdConfig, ddcConfig, edConfig });
                this._myDictionary.Add(DisplayConfigType.ED, new List<DisplayConfig> { edConfig, ddcConfig, sdConfig });
            }
            else
            {
                this._myDictionary.Add(DisplayConfigType.DDC, new List<DisplayConfig> { ddcConfig, sdConfig, edConfig, tdcConfig, tedConfig });
                this._myDictionary.Add(DisplayConfigType.SD, new List<DisplayConfig> { sdConfig, ddcConfig, edConfig, tdcConfig, tedConfig });
                this._myDictionary.Add(DisplayConfigType.ED, new List<DisplayConfig> { edConfig, ddcConfig, sdConfig, tdcConfig, tedConfig });
                this._myDictionary.Add(DisplayConfigType.TDC, new List<DisplayConfig> { tdcConfig, sdConfig, edConfig, ddcConfig, tedConfig });
                this._myDictionary.Add(DisplayConfigType.TED, new List<DisplayConfig> { tedConfig, ddcConfig, sdConfig, tdcConfig, edConfig });
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            List<DisplayConfig> configList = _myDictionary[base.CurrentConfig.ConfigType];
            Log.Message(true, "Apply {0} on {1},{2},{3}", configList[0].ConfigType, configList[0].PrimaryDisplay, configList[0].SecondaryDisplay, configList[0].TertiaryDisplay);
            SetConfig(configList[0]);
            ApplyNativeResolutionAndVerify(configList[0]);
            foreach (DisplayConfig currentDispConfig in configList.Skip(1))
            {
                if ((base.CurrentConfig.DisplayList.Count < 3) && ((currentDispConfig.ConfigType == DisplayConfigType.TED) || (currentDispConfig.ConfigType == DisplayConfigType.TDC)))
                    continue;
                Log.Message(true, "Switching configuration, Applying {0} on {1},{2},{3}", currentDispConfig.ConfigType, currentDispConfig.PrimaryDisplay, currentDispConfig.SecondaryDisplay, currentDispConfig.TertiaryDisplay);
                ApplyConfigCUI(currentDispConfig);
                Log.Message(true, "Switch back to original configuration");
                ApplyConfigCUI(configList[0]);
                CheckNativeResolutionPersistant(configList[0]);
            }
        }
        private void ApplyNativeResolutionAndVerify(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Apply Native Resolution");
            Log.Message("Get the list of all the modes for the config passed");
            _commonDisplayModeList = base.GetAllModes(argDisplayConfig.CustomDisplayList);
            List<DisplayMode> modeList = new List<DisplayMode>();
            _commonDisplayModeList.ForEach(dML =>
            {
                modeList.Add(dML.supportedModes.ToList().Last());
            });
            modeList.ForEach(dM =>
            {
                base.ApplyModeOS(dM, dM.display);
                base.VerifyModeOS(dM, dM.display);
            });
        }
        private void CheckNativeResolutionPersistant(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Check Native Resolution is still applied");
            Log.Message("Get the list of all the modes for the config passed");
            _commonDisplayModeList = base.GetAllModes(argDisplayConfig.CustomDisplayList);
            List<DisplayMode> modeList = new List<DisplayMode>();
            _commonDisplayModeList.ForEach(dML =>
            {
                modeList.Add(dML.supportedModes.ToList().Last());
            });
            modeList.ForEach(dM =>
            {
                base.VerifyModeOS(dM, dM.display);
            });
        }
        private void SetConfig(DisplayConfig argDispConfig)
        {
            Log.Message(true, "Set current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
    }
}


