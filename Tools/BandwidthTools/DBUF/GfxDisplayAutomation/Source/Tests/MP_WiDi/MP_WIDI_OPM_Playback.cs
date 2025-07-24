namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_OPM_Playback : MP_WIDIBase
    {
        DisplayConfig config = new DisplayConfig();
        private List<DisplayModeList> allModeList = new List<DisplayModeList>();

        [Test(Type = TestType.Method, Order = 1)]
        public void InstallMEDrv()
        {
            if (VerifyMEDriver() == false)
                InstallMEDriver(); 
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            if (!base.CurrentConfig.CustomDisplayList.Any(D => D.Equals(DisplayType.WIDI)))
            {
                Log.Abort("Command line dose not contains WIDI display, Hence Aborting test execution");
            }
            base.GetExternalDisplay();
            Log.Verbose("External display count is {0}", base.externalDisplayList.Count);
            config.ConfigType = base.CurrentConfig.ConfigType;
            config.PrimaryDisplay = DisplayType.WIDI;
            if (base.CurrentConfig.DisplayList.Count == 2)
                config.SecondaryDisplay = base.pDisplayList.First();
            else if (base.CurrentConfig.DisplayList.Count == 3)
            {
                config.SecondaryDisplay = base.pDisplayList.First();
                config.TertiaryDisplay = base.pDisplayList.Last();
            }

            Log.Message(true, "Set display Config using Windows API");
            this.SetNValidateConfig(config);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void GetAllModesForActiceDisplay()
        {
            List<DisplayType> DT = new List<DisplayType>();
            DT.Add(DisplayType.WIDI);
            Log.Verbose("Getting all suppored modes for all active display");
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, DT);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SetModesForActiveDisplay()
        {
            DisplayInfo currentDisplayInfo = null;
            List<DisplayMode> testModes = null;
            if (!allModeList.Count.Equals(0))
            {

                allModeList.ForEach(dML =>
                {
                    currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                    testModes = this.TestModes(dML.supportedModes);
                    testModes.ForEach(dM => ApplyAndVerify(dM, currentDisplayInfo));
                    RunOPMTester(config);
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
    }
}
