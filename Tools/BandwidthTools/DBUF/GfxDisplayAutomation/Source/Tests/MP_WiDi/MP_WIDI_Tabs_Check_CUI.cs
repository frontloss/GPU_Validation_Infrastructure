namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Threading;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_Tabs_Check_CUI : MP_WIDIBase
    {
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void CheckWiDiDisplay()
        {
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.WIDI))
                Log.Abort("Test Requires WIDI  display to run the test.");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void ValidateCUI()
        {
            Validate3DNVideo(Features.ThreeDBasicSettingFeatures);
            Validate3DNVideo(Features.VideoBasicSettingFeatures);
            ValidateInformationCenter();
        }

        private void Validate3DNVideo(Features feature)
        {
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Abort("Unable to launch CUI!");
            AccessInterface.Navigate(feature);
            Log.Success("Successfully open CUI {0} ", feature.ToString());
            Thread.Sleep(3000);
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }

        private void ValidateInformationCenter()
        {
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
                Log.Abort("Unable to launch CUI!");
            AccessInterface.Navigate(Features.SystemInfo);
            Log.Success("successfully opened information center page");
            if (!IsWiDiConnected())
            {
                if (!WiDiReConnect())
                    CheckWiDiStatus();
            }
            if (string.IsNullOrEmpty(base.CurrentConfig.EnumeratedDisplays.Where(DT => DT.DisplayType == DisplayType.WIDI).Select(CDN => CDN.CompleteDisplayName).FirstOrDefault()))
                Log.Fail("Unable to find display name");
            else
            {
                AccessInterface.SetFeature(Features.SelectDisplayInfo, Action.Set, DisplayType.WIDI);
                ConnectorType cinfo = AccessInterface.GetFeature<ConnectorType>(Features.SelectDisplayInfo, Action.Get);
                if (base.CurrentConfig.EnumeratedDisplays.Where(MI => MI.DisplayType == DisplayType.WIDI).Select(CT => CT.ConnectorType).FirstOrDefault().connectorType ==
                    cinfo.connectorType && (base.CurrentConfig.EnumeratedDisplays.Where(MI => MI.DisplayType == DisplayType.WIDI).Select(CT => CT.ConnectorType).FirstOrDefault().deviceType ==
                    cinfo.deviceType))
                {
                    Log.Success("CUI Information page in sync ConnectorType: {0} and DeviceType: {1} ", cinfo.connectorType, cinfo.deviceType);
                }
                else
                    Log.Fail("CUI Information page not in Sync ConnectorType: {0} and DeviceType: {1} ", cinfo.connectorType, cinfo.deviceType);
            }
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
    }
}

