namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;
    using System.Windows.Automation;
    using System.Windows;
    using System.IO;

    class SB_MODES_Display_Switch_Within_Config : SB_MODES_Base
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            //if (!base.CurrentConfig.DisplayList.Count.Equals(3))
            //    Log.Abort("This test requires atleast 3 displays connected!");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            switch (base.CurrentConfig.ConfigTypeCount)
            {
                case 1: DisplaySwitchWithinSingleDisplayConfig(base.CurrentConfig); break;
                case 2: DisplaySwitchWithinDualDisplayConfig(base.CurrentConfig); break;
                case 3: DisplaySwitchWithinTriDisplayConfig(base.CurrentConfig); break;
                default: break;
            }
        }
        private void DisplaySwitchWithinSingleDisplayConfig(DisplayConfig currentConfig)
        {
            Log.Message(true, "Display  switch within SD ");
            Log.Message("Apply SD {0}", currentConfig.PrimaryDisplay);
            DisplayConfig initalConfig = new DisplayConfig()
            {
                ConfigType = currentConfig.ConfigType,
                PrimaryDisplay = currentConfig.PrimaryDisplay
            };
            SetConfig(initalConfig);
            ApplyNativeResolutionAndVerify(initalConfig);
            foreach (DisplayType currentDispType in base.CurrentConfig.DisplayList.Skip(1))
            {
                Log.Message(true, "Apply SD {0}", currentDispType);
                DisplayConfig config = new DisplayConfig()
                {
                    ConfigType = base.CurrentConfig.ConfigType,
                    PrimaryDisplay = currentDispType
                };
                ApplyConfigCUI(config);
                Log.Message(true, "Switch back to original configuration");
                ApplyConfigCUI(initalConfig);
                CheckNativeResolutionPersistant(initalConfig);
            }
        }
        private void DisplaySwitchWithinDualDisplayConfig(DisplayConfig currentConfig)
        {
            Log.Message(true, "Display  switch within Dual Display Config ");
            Log.Message("Apply {0} on {1}, {2}", currentConfig.ConfigType, currentConfig.PrimaryDisplay, currentConfig.SecondaryDisplay);
            DisplayConfig initialConfig = new DisplayConfig()
            {
                ConfigType = currentConfig.ConfigType,
                PrimaryDisplay = currentConfig.PrimaryDisplay,
                SecondaryDisplay = currentConfig.SecondaryDisplay
            };
            SetConfig(initialConfig);
            ApplyNativeResolutionAndVerify(initialConfig);
            Log.Message(true, "Apply {0}  {1}, {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.TertiaryDisplay);
            DisplayConfig config = new DisplayConfig()
            {
                ConfigType = currentConfig.ConfigType,
                PrimaryDisplay = currentConfig.PrimaryDisplay,
                SecondaryDisplay = currentConfig.TertiaryDisplay
            };
            ApplyConfigCUI(config);
            Log.Message(true, "Switch back to original configuration");
            ApplyConfigCUI(initialConfig);
            CheckNativeResolutionPersistant(initialConfig);
        }
        private void DisplaySwitchWithinTriDisplayConfig(DisplayConfig currentConfig)
        {
            Log.Message(true, "Display  switch within Tri Display Config ");
            Log.Message("Apply {0} {1},{2},{3}", currentConfig.ConfigType, currentConfig.PrimaryDisplay, currentConfig.SecondaryDisplay, currentConfig.TertiaryDisplay);
            DisplayConfig initialConfig = new DisplayConfig()
            {
                ConfigType = currentConfig.ConfigType,
                PrimaryDisplay = currentConfig.PrimaryDisplay,
                SecondaryDisplay = currentConfig.SecondaryDisplay,
                TertiaryDisplay = currentConfig.TertiaryDisplay,
            };
            SetConfig(initialConfig);
            ApplyNativeResolutionAndVerify(initialConfig);
            Log.Message(true, "Apply {0}  {1}, {2}, {3}", base.CurrentConfig.ConfigType, base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.TertiaryDisplay, base.CurrentConfig.SecondaryDisplay);
            DisplayConfig config = new DisplayConfig()
            {
                ConfigType = currentConfig.ConfigType,
                PrimaryDisplay = currentConfig.PrimaryDisplay,
                SecondaryDisplay = currentConfig.TertiaryDisplay,
                TertiaryDisplay = currentConfig.SecondaryDisplay
            };
            ApplyConfigCUI(config);
            Log.Message(true, "Switch back to original configuration");
            ApplyConfigCUI(initialConfig);
            CheckNativeResolutionPersistant(initialConfig);
        }
        private void ApplyNativeResolutionAndVerify(DisplayConfig displayConfig)
        {
            Log.Message(true, "Apply Native Resolution");
            Log.Message("Get the list of all the modes for the config passed");
            _commonDisplayModeList = base.GetAllModes(displayConfig.CustomDisplayList);
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
        private void CheckNativeResolutionPersistant(DisplayConfig displayConfig)
        {
            Log.Message(true, "Check Native Resolution is still applied");
            Log.Message("Get the list of all the modes for the config passed");
            _commonDisplayModeList = base.GetAllModes(displayConfig.CustomDisplayList);
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

