namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    class MP_AudioLPSPBasic : MP_Audio_Base
    {
        List<DisplayModeList> allModeList = new List<DisplayModeList>();
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
        public void VerifyLPSP()
        {
            base.LPSPRegisterVerify(base.GetLPSPEnableStatus());
            Log.Message("Fetching Audio endpoint data");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
            Log.Verbose("Default audio endpoint device {0}", base.GetDefaultEndPoint().FriendlyName);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void VerifyLPSPNonNativeMode()
        {
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            List<DisplayMode> testModes = null;
            if (!allModeList.Count.Equals(0))
                {
                    allModeList.ForEach(dML =>
                    {
                        testModes = this.TestModes(dML.supportedModes);
                        Log.Message(true, "Setting min mid modes for display : {0}", testModes.First().display);
                        testModes.ForEach(dM => ApplyAndVerify(dM));
                        VerifyLPSP();
                    });
                }
                else
                    Log.Fail("No modes returned!");
        }
        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            return testModes;
        }

        private bool ApplyAndVerify(DisplayMode argDispMode)
        {
            Log.Message(true, "Setting Mode : {0} for {1}", base.GetModeStrX(argDispMode), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
            {
                Log.Fail("Fail to apply Mode");
                return false;
            }
            else
            {
                Log.Success("Mode applied successfully");
                return true;
            }
        }

        
    }
}
