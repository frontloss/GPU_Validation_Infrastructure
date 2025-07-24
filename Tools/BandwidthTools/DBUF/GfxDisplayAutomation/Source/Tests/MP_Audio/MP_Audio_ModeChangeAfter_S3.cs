namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class MP_Audio_ModeChangeAfter_S3 : MP_Audio_S3
    {
        public MP_Audio_ModeChangeAfter_S3()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void SetDisplayMode()
        {
            DisplayInfo currentDisplayInfo = null;
            List<DisplayMode> testModes = null;
            Log.Verbose("Getting all suppored modes for all active display");
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);

            if (!allModeList.Count.Equals(0))
            {
                allModeList.ForEach(dML =>
                {
                    if (dML.display != DisplayType.EDP)
                    {
                        currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                        testModes = this.TestModeslist(dML.supportedModes);
                        Log.Message(true, "Setting min max mid & Interlaced modes for display : {0}", testModes.First().display);
                        testModes.ForEach(dM => ApplyAndVerify(dM));
                    }
                });
            }
            else
                Log.Fail(false, "No modes returned!");
        }

    }
}
