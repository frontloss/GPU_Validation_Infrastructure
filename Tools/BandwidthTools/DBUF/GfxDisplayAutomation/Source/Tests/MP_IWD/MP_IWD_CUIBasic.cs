namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.WiDi)]
    class MP_IWD_CUIBasic : MP_IWDBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void LaunchCUI()
        {
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Abort("Unable to launch CUI!");
            if (base.CurrentConfig.CustomDisplayList.Count == 3)
                GetThreeDisplaySwitchingPattern(this.switchPatternList);
            else
                this.GetTwoDisplaySwitchPattern(this.switchPatternList);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            try
            {
                Log.Message(true, "Setting display config using CUI");
                this.switchPatternList.ForEach(dC =>
                {
                    if (SetNValidateConfigCUI(dC))
                    {
                        Log.Success("Switch successful to {0}", dC.GetCurrentConfigStr());
                        if (!this.GetAllModesForActiceDisplay().Count.Equals(0))
                        {
                            DisplayInfo currentDisplayInfo = null;
                            List<DisplayMode> testModes = null;
                            commonDisplayModeList.ForEach(dML =>
                            {
                                currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                                testModes = this.TestModes(dML.supportedModes);
                                testModes.ForEach(dM => ApplyAndVerify(dM, currentDisplayInfo));
                            });
                        }
                        else
                            Log.Fail("Error in getting modelist");
                    }
                    else
                        Log.Fail("Failed to switch display config");

                });
            }
            catch
            {
                base.CheckWiDiStatus();
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void ValidateDisplayType()
        {
            try
            {
                Log.Message(true, "Open Information center from option menu");
                AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
                if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                    Log.Abort("Unable to launch CUI!");
                AccessInterface.Navigate(Features.SystemInfo);
                Log.Verbose("successfully opened information center");

                if (string.IsNullOrEmpty(base.CurrentConfig.EnumeratedDisplays.Where(DT => DT.DisplayType == DisplayType.WIDI).Select(CDN => CDN.CompleteDisplayName).FirstOrDefault()))
                {
                    Log.Fail("Unable to find display name");
                }
                else
                {
                    Log.Message("From select report type selecting display {0} and check connectortype, device type", DisplayType.WIDI.ToString());
                    AccessInterface.SetFeature(Features.SelectDisplayInfo, Action.Set, DisplayType.WIDI);
                    ConnectorType cinfo = AccessInterface.GetFeature<ConnectorType>(Features.SelectDisplayInfo, Action.Get);
                    if (base.CurrentConfig.EnumeratedDisplays.Where(MI => MI.DisplayType == DisplayType.WIDI).Select(CT => CT.ConnectorType).FirstOrDefault().connectorType ==
                        cinfo.connectorType && (base.CurrentConfig.EnumeratedDisplays.Where(MI => MI.DisplayType == DisplayType.WIDI).Select(CT => CT.ConnectorType).FirstOrDefault().deviceType ==
                        cinfo.deviceType))
                    {
                        Log.Verbose("CUI Information page in sync ConnectorType: {0} and DeviceType: {1} ", cinfo.connectorType, cinfo.deviceType);
                    }
                    else
                        Log.Fail("CUI Information page not in Sync ConnectorType: {0} and DeviceType: {1} ", cinfo.connectorType, cinfo.deviceType);
                }
            }
            catch
            {
                base.CheckWiDiStatus();
            }

            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }

        private bool SetNValidateConfigCUI(DisplayConfig argConfig)
        {
            AccessInterface.Navigate(Features.Config);
            AccessInterface.SetFeature(Features.Config, Action.Set, Source.AccessUI, argConfig);
            if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);
            DisplayConfig currConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessUI);
            return (currConfig.GetCurrentConfigStr().Equals(argConfig.GetCurrentConfigStr()));
        }

    }
}
