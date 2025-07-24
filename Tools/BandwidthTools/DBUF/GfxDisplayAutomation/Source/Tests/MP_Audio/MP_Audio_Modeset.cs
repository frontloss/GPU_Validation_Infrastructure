namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;

    class MP_Audio_Modeset : MP_Audio_Base
    {
        private List<DisplayModeList> allModeList = new List<DisplayModeList>();
        [Test(Type = TestType.Method, Order = 1)]
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

        [Test(Type = TestType.Method, Order = 2)]
        public void GetAllModesForActiceDisplay()
        {
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
            Log.Verbose("Getting all suppored modes for all active display");
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
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
            bool SeqCheck = false;
            SeqCheck = base.IsPDBpresent();

            if (true == SeqCheck)
                base.StartLog();
            
            Log.Message(true, "Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);

            //Log.Message("Setting Mode : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);
            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
                Log.Fail("Fail to apply Mode");
            else
            {
                //Log.Success("Mode applied successfully");
                Log.Success("Successful Modeset : {0} for {1}", GetModeStr(argDispMode), argDispMode.display);

                //Log.Message(true, "Check Audio Endpoint and AUD_PIN_ELD_CP_VLD Registers");
    
                base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                if (true == SeqCheck)
                {
                    base.StopLog();

                    if (PWR_Status.No_PWR_Change != base.VerifyPWRSequence())
                        Log.Fail("PWR Sequence should not occur in Modeset");
                    else
                        Log.Success("PWR Sequence Passed");
                    base.AUDseq_Modeset();
                }
            }
        }

        private string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
        }
    }
}
