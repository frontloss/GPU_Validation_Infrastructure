namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class MP_ConnectedStandbyModeSet : MP_ConnectedStandbyBase
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        #region Test
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
                Log.Message("Set the maximum display mode on all the active displays");
            }
            else
            {
                this.CleanUP();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void GetAllModesForActiceDisplay()
        {
            Log.Verbose("Getting all suppored modes for all active display");
            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            List<DisplayMode> commonModes = null;
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                commonModes = displayModeList_OSPage.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                displayModeList_OSPage.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                if (commonModes.Count() > 0)
                    _commonDisplayModeList.Add(new DisplayModeList() { display = base.CurrentConfig.PrimaryDisplay, supportedModes = commonModes });
            }
            else
                _commonDisplayModeList = displayModeList_OSPage;
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SetModesForActiveDisplay()
        {
            DisplayInfo currentDisplayInfo = null;
            List<DisplayMode> testModes = null;
            if (!_commonDisplayModeList.Count.Equals(0))
            {
                _commonDisplayModeList.ForEach(dML =>
                {
                    currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                    testModes = this.TestModes(dML.supportedModes);
                    testModes.ForEach(dM => ApplyAndVerify(dM, currentDisplayInfo));
                });
            }
            else
                Log.Fail(false, "No modes returned!");
        }

        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            return testModes;
        }

        private void ApplyAndVerify(DisplayMode argDispMode, DisplayInfo argDisplayInfo)
        {
            this.S0ixCall();
            Log.Message("Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
                Log.Fail("Fail to apply Mode");
            else
                Log.Success("Mode applied successfully");
        }
        private string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
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