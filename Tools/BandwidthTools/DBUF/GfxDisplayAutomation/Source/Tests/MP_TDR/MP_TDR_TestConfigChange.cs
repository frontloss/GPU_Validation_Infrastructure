namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;

    [Test(Type = TestType.HasReboot)]
    class MP_TDR_TestConfigChange : MP_TDR_Base
    {
        DisplayConfig displayWrapper = null;
        private Dictionary<int, Action<List<DisplayConfig>>> _switchPatternList = null;
        
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.RunTDRNVerify(true);
        }

        [Test(Type = TestType.Method, Order = 2)]        
        public void TestStep2()
        {
            Log.Message(true, "Set all possible display configurations with displays planned in grid");            
            
            List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            if (base.CurrentConfig.CustomDisplayList.Count == 1)
            {
                Log.Abort("Please specify minimum 2 display in command line to run the test");
            }
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);
            
            switchPatternList.ForEach(dC =>
            {
                if(AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC))
                {
                    Log.Success("Config set successfully to {0}", dC.GetCurrentConfigStr());
                    DisplayConfig CUISDK_currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.SDKConfig, Action.Get, Source.AccessAPI);
                    DisplayConfig API_currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    if (CUISDK_currentDisplayConfig.GetCurrentConfigStr().Equals(API_currentDisplayConfig.GetCurrentConfigStr()))
                    {
                        Log.Success("Current display config set in CUI is same as API");
                    }
                    else
                    {
                        Log.Fail("Current display config set in CUI is not same as API");
                    }
                }
                else
                {
                    Log.Fail("Set Config failed");
                }
            });            
        }        
        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);
        }
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);
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
    }
}