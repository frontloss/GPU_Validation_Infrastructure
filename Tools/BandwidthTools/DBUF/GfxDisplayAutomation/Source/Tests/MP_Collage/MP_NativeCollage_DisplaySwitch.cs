namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class MP_NativeCollage_DisplaySwitch : MP_NativeCollage_BAT
    {
        List<DisplayConfig> _switchPatternList = new List<DisplayConfig>();
        public MP_NativeCollage_DisplaySwitch()
            : base()
        {
            base._performAction = this.PerformAction;
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal,
                DisplayConfigType.Vertical
            };
        }

        private void PerformAction()
        {
            if (_switchPatternList.Count == 0)
            {
                if (base.CurrentConfig.DisplayList.Count == 2)
                    GetSwitchPatternForDualDisplayMode();
                else if (base.CurrentConfig.DisplayList.Count == 3)
                    GetSwitchPatternForTriDisplayMode();
            }
            Log.Message(true, "Switch to different config and verify collage status");

            _switchPatternList.ForEach(dC =>
            {
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC))
                {
                    Log.Success("Config set successfully to {0}", dC.GetCurrentConfigStr());
                    Log.Message(true, "Verifying {0} configuration is set using API", displayConfig.ConfigType);
                    DisplayConfig currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    List<DisplayType> currentConfigDisplayList = base.GetDisplayList(currentDisplayConfig);
                    List<DisplayType> collageConfigDisplayList = base.GetDisplayList(displayConfig);
                    if (Enumerable.SequenceEqual(currentConfigDisplayList.OrderBy(DT => DT), collageConfigDisplayList.OrderBy(DT => DT)))
                        Log.Success("displays are same after switch to different config {0}", dC.GetCurrentConfigStr());
                    else
                        Log.Fail("Display list is different after switch to different config expected {0} current is {1}", base.GetDisplayListString(collageConfigDisplayList), base.GetDisplayListString(currentConfigDisplayList));
                }
                else
                {
                    Log.Fail("Config not applied to {0}", dC.GetCurrentConfigStr());
                }
            });

        }

        private void GetSwitchPatternForDualDisplayMode()
        {
            DisplayConfig cfg = null;
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            _switchPatternList.Add(cfg);
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            _switchPatternList.Add(cfg);
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            _switchPatternList.Add(cfg);
        }

        private void GetSwitchPatternForTriDisplayMode()
        {
            DisplayConfig cfg = null;
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            _switchPatternList.Add(cfg);
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            _switchPatternList.Add(cfg);
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            _switchPatternList.Add(cfg);
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            _switchPatternList.Add(cfg);
            cfg = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            _switchPatternList.Add(cfg);
        }
    }
}
