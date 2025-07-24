namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_DisplaySwap_10BitScanout : SB_DeepColor_DisplaySwap_DPApplet
    {
        public SB_DeepColor_DisplaySwap_10BitScanout()
            :base()
        {
            this._AppType = DeepColorAppType.N10BitScanOut;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            _allDisplayCombinations.ForEach(dc =>
            {
                AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dc);
                EnableDeepColor(_AppType);

                foreach (DisplayType display in dc.DisplayList)
                {
                    DisplayInfo dispInfo = base.CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                    PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                    CheckDeepColorconditions(dispInfo, pipePlane, _AppType, true, dc,DisplayHierarchy.Display_1);
                }

                CloseApp(_AppType);
            });
        }

        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            
        }

        private void SingleDisplayCombination()
        {
            _allDisplayCombinations.Add(base.CurrentConfig);
        }

        private void TwoDisplaysCombinations()
        {
            DisplayConfig dispSwitch1 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch2 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig dispSwitch3 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };

            _allDisplayCombinations = new List<DisplayConfig>() { dispSwitch1, dispSwitch2, dispSwitch3 };
        }

        private void ThreeDisplaysCombinations()
        {
            DisplayConfig dispSwitch1 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig dispSwitch2 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig dispSwitch3 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch4 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };

            _allDisplayCombinations = new List<DisplayConfig>() { dispSwitch1, dispSwitch2, dispSwitch3, dispSwitch4 };

        }
    }
}
