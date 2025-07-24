namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_SmartFrame_Basic : MP_SmartFrame_Base
    {
        private Dictionary<int, Action<List<DisplayConfig>>> _switchPatternList = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            if (base.CurrentConfig.EnumeratedDisplays.Count != base.CurrentConfig.DisplayList.Count)
            {
                foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
                {
                    Log.Verbose("Display {0} is not enumerated after enable Gfx Driver (WA)", DT);
                    Log.Message("Plugging display {0}", DT);
                    base.HotPlug(DT);
                }
            }
            if (base.CurrentConfig.EnumeratedDisplays.Count == 1)
                Log.Abort("Display Switch requires atleast 2 displays connected!");

            List<DisplayConfig> switchPatternList = new List<DisplayConfig>();

            int dispFetchKey = base.CurrentConfig.EnumeratedDisplays.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);

            switchPatternList.ForEach(dC =>
            {
                AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC);
                if (dC.CustomDisplayList.Contains(base.GetInternalDisplay()))
                {
                    base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
                }
            });
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
        }
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
        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");
            DisplayConfig displayConfig = null;

            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.EnumeratedDisplays[0].DisplayType };
            argList.Add(displayConfig);

            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.EnumeratedDisplays[0].DisplayType, SecondaryDisplay = base.CurrentConfig.EnumeratedDisplays[1].DisplayType };
            argList.Add(displayConfig);

            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.EnumeratedDisplays[1].DisplayType, SecondaryDisplay = base.CurrentConfig.EnumeratedDisplays[0].DisplayType };
            argList.Add(displayConfig);

            argList.Add(base.CurrentConfig);

        } // End GetSwitchPatternForDualDisplayMode
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");
            DisplayConfig displayConfig = null;

            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.EnumeratedDisplays[0].DisplayType };
            argList.Add(displayConfig);

            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.EnumeratedDisplays[0].DisplayType, SecondaryDisplay = base.CurrentConfig.EnumeratedDisplays[1].DisplayType, TertiaryDisplay = base.CurrentConfig.EnumeratedDisplays[2].DisplayType };
            argList.Add(displayConfig);

            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.EnumeratedDisplays[2].DisplayType, SecondaryDisplay = base.CurrentConfig.EnumeratedDisplays[1].DisplayType, TertiaryDisplay = base.CurrentConfig.EnumeratedDisplays[0].DisplayType };
            argList.Add(displayConfig);

            displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.EnumeratedDisplays[0].DisplayType, SecondaryDisplay = base.CurrentConfig.EnumeratedDisplays[1].DisplayType };
            argList.Add(displayConfig);

            argList.Add(base.CurrentConfig);
        } // End GetSwitchPatternForTriDisplayMode 
    }
}