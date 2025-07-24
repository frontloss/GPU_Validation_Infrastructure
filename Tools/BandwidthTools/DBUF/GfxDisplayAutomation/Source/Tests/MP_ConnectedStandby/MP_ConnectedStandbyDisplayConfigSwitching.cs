namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;

    class MP_ConnectedStandbyDisplayConfigSwitching : MP_ConnectedStandbyBase
    {
        #region Test
        List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
        string setConfigStr = string.Empty;
        string currentConfigStr = string.Empty;

        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            Log.Message(true, "Preparing display config switching list");
            if (base.CurrentConfig.DisplayList.Count < 2 ||
                base.CurrentConfig.DisplayList.Count > 3)
            {
                Log.Fail("To run the test minimum two maximum three display config required");
                this.CleanUP();
                Log.Abort("Exiting...");
            }
            this.GetTwoDisplaySwitchPattern(switchPatternList);
            if (base.CurrentConfig.DisplayList.Count == 3)
                GetThreeDisplaySwitchingPattern(switchPatternList);
        }

        private void SendSysytemToS0ix()
        {
            this.S0ixCall();
            if (!GetListEnumeratedDisplays())
                Log.Fail("Display enumeration mismatch after comming from S0ix");
            else
                Log.Message("Connected displays are enumerated properly");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void DisplayConfigSwitching()
        {
            Log.Message(true, "Set display Config using Windows API");
            switchPatternList.ForEach(dC =>
            {
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC))
                {
                    DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                    setConfigStr = this.GetConfigString(dC);
                    currentConfigStr = this.GetConfigString(currentConfig);
                    if (setConfigStr.Equals(currentConfigStr))
                        Log.Success("Switch successful to {0}", currentConfigStr);
                    else
                        Log.Fail("Switch failed to {0}. Current config is {1}", setConfigStr, currentConfigStr);
                }
                else
                {
                    this.ListEnumeratedDisplays();
                    this.CleanUP();
                    Log.Abort("Config not applied!");
                }
                SendSysytemToS0ix();
            });
        }

        private void GetTwoDisplaySwitchPattern(List<DisplayConfig> argList)
        {
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
        }

        private void GetThreeDisplaySwitchingPattern(List<DisplayConfig> argList)
        {
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
        }

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

        #region PostCondition
        [Test(Type = TestType.PostCondition, Order = 4)]
        public void TestPostCondition()
        {
            this.CleanUP();
        }
        #endregion
    }
}
