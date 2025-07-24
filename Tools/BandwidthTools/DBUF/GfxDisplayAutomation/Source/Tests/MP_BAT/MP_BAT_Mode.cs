namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    class MP_BAT_Mode : TestBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "2) Set config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }

            Log.Message(true, "2) Apply Mode");
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            
            DisplayInfo currentDisplayInfo = null;
            List<DisplayMode> testModes = null;
            if (!allModeList.Count.Equals(0))
            {
                allModeList.ForEach(dML =>
                {
                    currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                    testModes = this.TestModes(dML.supportedModes);
                    testModes.ForEach(dM => ApplyAndVerify(dM, currentDisplayInfo));
                });
            }
            else
                Log.Fail(false, "No modes returned!");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.DisableNVerifyIGDWithDTCM(7);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.EnableNVerifyIGDBasic(8);
        }

        private bool ApplyAndVerify(DisplayMode argDispMode, DisplayInfo argDisplayInfo)
        {
            Log.Message(true, "Setting Mode : {0} for {1}", argDispMode.GetCurrentModeStr(true), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
            {
                Log.Fail("Fail to apply Mode");
                return false;
            }
            else
                Log.Success("Mode applied successfully");

            // Get Current DisplayMode
            DisplayMode currentDisplayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, argDisplayInfo);

            if (currentDisplayMode.GetCurrentModeStr(true).Equals(argDispMode.GetCurrentModeStr(true)))
                Log.Success("OSPage and CUI are in sync", argDispMode.display);
            else
            {
                Log.Fail("Applied Mode {0} . Current OS Page Mode : {1}  ", argDispMode.GetCurrentModeStr(true), currentDisplayMode.GetCurrentModeStr(true));
                return false;
            }
            return true;
        }
        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            return testModes;
        }
        /*private void SetModeViaAccessUI(string argSelectedMode)
        {
            AccessInterface.SetFeature(Features.Modes, Action.Set, Source.AccessUI, argSelectedMode);
            if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);
        }
        private void SetModeViaAccessApi(string argSelectedMode)
        {
            DisplayMode mode = new DisplayMode()
            {
                 HzRes = Convert.ToUInt32(argSelectedMode.Split('x').First().Trim()),
                 VtRes = Convert.ToUInt32(argSelectedMode.Split('x').Last().Trim()),
                 Bpp = 32,
                 RR = 60,
                 InterlacedFlag = 0
            };
            AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, mode);
        }*/
    }
}