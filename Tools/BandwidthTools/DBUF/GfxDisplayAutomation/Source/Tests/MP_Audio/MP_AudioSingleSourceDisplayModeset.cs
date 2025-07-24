namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    class MP_AudioSingleSourceDisplayModeset : MP_Audio_Base
    {
        internal List<DisplayModeList> allModeList = new List<DisplayModeList>();

        [Test(Type = TestType.Method, Order = 1)]
        public void SetAudioSource()
        {
            base.SetAudioSource();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void GetAllSupportedModeList()
        {
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.CustomDisplayList);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public virtual void SetDisplayMode()
        {
            List<DisplayMode> testModes = null;
            if (!allModeList.Count.Equals(0))
            {
                allModeList.ForEach(dML =>
                {
                    if (dML.display != DisplayType.EDP)
                    {
                        testModes = this.TestModes(dML.supportedModes);
                        Log.Message(true, "Setting min max mid & Interlaced modes for display : {0}", testModes.First().display);
                        testModes.ForEach(dM => ApplyAndVerify(dM));
                    }
                });
            }
            else
                Log.Fail(false, "No modes returned!");
        }
        internal List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            List<DisplayMode> interlacedModeList = displayModeList.FindAll(DT => DT.InterlacedFlag.Equals(1));
            if (interlacedModeList.Count != 0)
                testModes.Add(interlacedModeList.First());
            testModes.Add(displayModeList.Last());
            return testModes;
        }

        internal bool ApplyAndVerify(DisplayMode argDispMode)
        {
            Log.Message("Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
            {
                Log.Fail("Fail to apply Mode");
                return false;
            }
            else
            {
                Log.Success("Mode applied successfully");
                Log.Message("Fetching Audio endpoint data");
                base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                Log.Verbose("Default audio endpoint device {0}", base.GetDefaultEndPoint().FriendlyName);
                return true;
            }
        }
        private string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
        }
    }
}
