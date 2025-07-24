namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    class MP_CI_DisplaySwitch_OS : TestBase
    {
        private Dictionary<int, Action<List<DisplayConfig>>> _switchPatternList = null;
        private int _dispFetchKey = 0;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            this._dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (this._dispFetchKey > dispByPlatform)
                this._dispFetchKey = dispByPlatform;

            if (base.CurrentConfig.CustomDisplayList.Count < 2)
                Log.Abort("CI_DisplaySwitch_OS test requires atleast 2 displays connected!");

            this._switchPatternList = new Dictionary<int, Action<List<DisplayConfig>>>();
            this._switchPatternList.Add(2, this.GetSwitchPatternForDualMode);
            this._switchPatternList.Add(3, this.GetSwitchPatternForTriMode);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayConfig currentConfig = null;
            Log.Message(true, "Set display switch configurations through OS");
            List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
            this._switchPatternList[this._dispFetchKey](switchPatternList);
            switchPatternList.ForEach(dC =>
            {
                AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC);
                currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                if (dC.GetCurrentConfigStr().Equals(currentConfig.GetCurrentConfigStr()))
                {
                    Log.Success("Switch successful to {0}", currentConfig.GetCurrentConfigStr());
                    Log.Message(true, "Disable the driver");
                    base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });
                    Log.Message(true, "Enable the driver");
                    base.EnableNVerifyIGDBasic(1);
                }
                else
                    Log.Fail("Switch failed to {0}. Current config is {1}", dC.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
            });
        }

        private void GetSwitchPatternForSingleMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for Single Mode");
            List<DisplayType> displayList = base.CurrentConfig.CustomDisplayList;
            if (null == displayList || displayList.Count.Equals(0))
            {
                displayList = base.CurrentConfig.EnumeratedDisplays.Select(dI => dI.DisplayType).ToList();
                Log.Verbose("No displays passed via command line. Considering enumerated displays #{0}", displayList.Count);
            }
            displayList.ForEach(dT => argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = dT }));
        }
        private void GetSwitchPatternForDualMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for Dual Mode");
            List<DisplayType> displayList = base.CurrentConfig.CustomDisplayList;
            foreach (DisplayType primaryDisplay in displayList)
            {
                foreach (DisplayType secondaryDisplay in displayList)
                {
                    if (primaryDisplay != secondaryDisplay)
                        argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = primaryDisplay, SecondaryDisplay = secondaryDisplay });
                }
            }
        }
        private void GetSwitchPatternForTriMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for Tri Mode");
            List<DisplayType> displayList = base.CurrentConfig.CustomDisplayList;
            foreach (DisplayType primaryDisplay in displayList)
            {
                foreach (DisplayType secondaryDisplay in displayList)
                {
                    if (primaryDisplay != secondaryDisplay)
                    {
                        foreach (DisplayType thirdDisplay in displayList)
                        {
                            if (secondaryDisplay != thirdDisplay && primaryDisplay != thirdDisplay)
                                argList.Add(new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = primaryDisplay, SecondaryDisplay = secondaryDisplay, TertiaryDisplay = thirdDisplay });
                        }
                    }
                }
            }
        }
    }
}