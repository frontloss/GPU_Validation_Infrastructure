namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;

    class SB_DisplayCStates_ConfigSwitch : SB_DisplayCStates_BasicFeature
    {
        private Dictionary<int, Action<List<DisplayConfigWrapper>>> _switchPatternList = null;


        [Test(Type = TestType.Method, Order = 3)]
        public void DisplaySwitch()
        {
            Log.Message(true, "Switch to different config and verify DisplayCstate Achieved");
            List<DisplayConfigWrapper> switchPatternList = new List<DisplayConfigWrapper>();

            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);
            switchPatternList.ForEach(dC =>
            {
                AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC.DispConfig);
                base.Method();
            });

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

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay }, true);
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay }, true);
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay }, true);
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay }, true);
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
    }
}