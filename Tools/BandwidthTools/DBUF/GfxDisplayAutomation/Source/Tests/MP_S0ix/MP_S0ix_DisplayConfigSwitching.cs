namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;

    [Test(Type = TestType.ConnectedStandby)]
    class MP_S0ix_DisplayConfigSwitching : MP_S0ixBase
    {
        #region Test
        private Dictionary<int, Action<List<DisplayConfigWrapper>>> _switchPatternList = null;
        string setConfigStr = string.Empty;
        string currentConfigStr = string.Empty;
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
        private List<DisplayConfigWrapper> switchPatternList = null;

        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            Log.Message(true, "Preparing display config switching list");
            if (base.CurrentConfig.DisplayList.Count < 2)
            {
                Log.Fail("To run the test minimum two maximum three display config required");
                Log.Abort("Exiting...");
            }
            switchPatternList = new List<DisplayConfigWrapper>();
            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            this.SwitchPatternList[dispFetchKey](switchPatternList);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void DisplayConfigSwitching()
        {
            Log.Message("Set SD to any of the display (Display1) connected active in maximum resolution");
            if (!AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, switchPatternList.First().DispConfig))
            {
                Log.Abort("Config not applied!");
            }
            SendSysytemToS0ix();
            switchPatternList.Remove(switchPatternList.First());
            Log.Message(true, "Verify Display switching using OS page for all the connected displays as mentioned below");
            switchPatternList.ForEach(dC =>
            {
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC.DispConfig))
                {
                    DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                    setConfigStr = this.GetConfigString(dC.DispConfig);
                    currentConfigStr = this.GetConfigString(currentConfig);
                    if (setConfigStr.Equals(currentConfigStr))
                        Log.Success("Switch successful to {0}", currentConfigStr);
                    else
                        Log.Fail("Switch failed to {0}. Current config is {1}", setConfigStr, currentConfigStr);
                }
                else
                {
                    this.ListEnumeratedDisplays();
                    Log.Fail("Config not applied!");
                }
            });
        }

        private void SendSysytemToS0ix()
        {
            this.CSCall();
            if (!GetListEnumeratedDisplays())
                Log.Fail("Display enumeration mismatch after comming from S0ix");
            else
                Log.Message("Connected displays are enumerated properly");
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
        }
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfigWrapper> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");
            DisplayConfigWrapper displayWrapper = null;
            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(displayWrapper);
            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(displayWrapper);
            displayWrapper = new DisplayConfigWrapper(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(displayWrapper);
            
        } // End GetSwitchPatternForTriDisplayMode 
        private string GetConfigString(DisplayConfig argConfig)
        {
            StringBuilder sb = new StringBuilder(argConfig.ConfigType.ToString()).Append(" ");
            sb.Append(argConfig.PrimaryDisplay.ToString()).Append(" ");
            if (argConfig.SecondaryDisplay != DisplayType.None)
                sb.Append(argConfig.SecondaryDisplay.ToString()).Append(" ");
            if (argConfig.TertiaryDisplay != DisplayType.None)
                sb.Append(argConfig.TertiaryDisplay.ToString()).Append(" ");
            return sb.ToString();
        }
        #endregion
    }
}
