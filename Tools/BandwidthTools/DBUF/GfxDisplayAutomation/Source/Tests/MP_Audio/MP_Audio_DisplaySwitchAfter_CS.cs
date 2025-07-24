namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    class MP_Audio_DisplaySwitchAfter_CS : MP_Audio_Single_Source_CS
    {
        [Test(Type = TestType.Method, Order = 6)]
        public void DisplaySwitch()
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
