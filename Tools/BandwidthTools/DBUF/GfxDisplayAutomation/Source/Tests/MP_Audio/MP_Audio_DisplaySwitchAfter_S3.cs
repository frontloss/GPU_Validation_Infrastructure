namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    class MP_Audio_DisplaySwitchAfter_S3 : MP_Audio_S3
    {
        public MP_Audio_DisplaySwitchAfter_S3()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }
        [Test(Type = TestType.Method, Order = 4)]      
        public void DisplayConfigSwitch()
        {
            List<DisplayConfig> switchPatternList = null;
            if (base.CurrentConfig.CustomDisplayList.Count < 2)
                Log.Abort("DisplaySwitch_OSPage test requires atleast 2 displays connected!");

            switchPatternList = base.GetSwitchSequence();

            if (switchPatternList != null)
            {
                switchPatternList.ForEach(dC =>
                {
                    Log.Message(true, "Switching to display config {0}", dC.GetCurrentConfigStr());
                    if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dC))
                    {
                        Log.Success("Switch successful to : {0}", dC.GetCurrentConfigStr());
                        Log.Message("Fetching Audio endpoint data");
                        CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                        Log.Verbose("Default audio endpoint device {0}", GetDefaultEndPoint().FriendlyName);
                    }
                    else
                        Log.Fail("Switch failed to : {0}", dC.GetCurrentConfigStr());
                });
            }
            else
            {
                Log.Fail("Could not find any display switching sequence.");
            }
        }
    }
}