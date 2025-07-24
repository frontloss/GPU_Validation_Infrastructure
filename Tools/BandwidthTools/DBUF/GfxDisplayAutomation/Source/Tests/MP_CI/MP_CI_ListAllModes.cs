namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_CI_ListAllModes : MP_CI_Mode
    {        
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            List<DisplayMode> modeList = null;
            allModeList.ForEach(dML =>
            {
                modeList = GetMinMaxInterModes(dML.supportedModes.ToList());
                modeList.ForEach(dM =>
                {
                    ApplyNVerifyModeOS(dM, dML.display);
                    VerifyModeOSPageNCUI(dM);
                });
            });
        }               
        private void VerifyModeOSPageNCUI(DisplayMode argMode)
        {
            Log.Message("Verify if the mode in OS Page and CUI match after disabling and enabling driver");
            Log.Verbose("Get mode from OS page");
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argMode.display).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            Log.Verbose("Get mode from CUI page");
            if (AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
            {
                AccessInterface.Navigate(Features.DisplaySettings);
                AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, argMode.display);
                string currCUIResolution = AccessInterface.GetFeature<string>(Features.Modes, Action.Get, Source.AccessUI);
                string currCUIRefreshRate = AccessInterface.GetFeature<string>(Features.RefreshRate, Action.Get, Source.AccessUI);
                string modeStr = string.Concat(currCUIResolution.Split('x').First().Trim(), "x", currCUIResolution.Split('x').Last().Trim(), "x", currCUIRefreshRate, "x", argMode.Bpp);
                if (GetModeStr(actualMode).Equals(modeStr))
                    Log.Success("OSPage and CUI are in sync");
                else
                    Log.Fail("Current OS Page Mode : {0} . Current CUI Mode : {1}  ", GetModeStr(actualMode), modeStr);
                AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            }
            else
                Log.Fail("CUI couldnt launch!");
        }
        private string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
        }

    }
}