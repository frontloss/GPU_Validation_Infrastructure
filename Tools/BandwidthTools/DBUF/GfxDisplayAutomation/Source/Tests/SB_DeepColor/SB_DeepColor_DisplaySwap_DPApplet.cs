namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_DisplaySwap_DPApplet : SB_DeepColor_Base
    {
        protected DeepColorAppType _AppType;
        protected List<DisplayConfig> _allDisplayCombinations = new List<DisplayConfig>();
        protected Dictionary<DisplayConfigType, System.Action> _prepareDisplayCombination = new Dictionary<DisplayConfigType, System.Action>();

        public SB_DeepColor_DisplaySwap_DPApplet()
        {
            this._AppType = DeepColorAppType.DPApplet;

            _prepareDisplayCombination = new Dictionary<DisplayConfigType, System.Action>()
            { 
                {DisplayConfigType.SD,SingleDisplayCombination},
                {DisplayConfigType.ED,TwoDisplaysCombinations},
                {DisplayConfigType.DDC,TwoDisplaysCombinations},
                {DisplayConfigType.TDC,ThreeDisplaysCombinations},
                {DisplayConfigType.TED,ThreeDisplaysCombinations}
            };
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestPreCondition()
        {
            Log.Message("Test PreConditions start");
            HotPlugDeepColorPanels();

            _prepareDisplayCombination[base.CurrentConfig.ConfigType]();
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            EnableDeepColor(_AppType);
            _allDisplayCombinations.ForEach(dc =>
            {
                AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dc);

                foreach (DisplayType display in dc.DisplayList)
                {
                    DisplayInfo dispInfo = base.CurrentConfig.EnumeratedDisplays.Find(dp => dp.DisplayType == display);
                    PipePlaneParams pipePlane = GetPipePlane(dispInfo);
                    CheckDeepColorconditions(dispInfo, pipePlane, _AppType, true, CurrentConfig, DisplayHierarchy.Display_1);
                }
            });

            DisableDeepColor(_AppType);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            CloseApp(_AppType);
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
