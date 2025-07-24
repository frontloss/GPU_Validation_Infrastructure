namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_Multi_Source_HP : MP_Audio_Base
    {
        List<DisplayType> displayList = new List<DisplayType>();
        public MP_Audio_Multi_Source_HP()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void HotPlugNValidateEndpoint()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message(true, "Trying to plug display {0}", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Successfully able to hotplug display {0}", DT);
                }
                else
                    Log.Fail("Unable to hot plug display {0}", DT);
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SetAudioSource()
        {
            Log.Message(true, "Set audio source to {0} and verify audio endpoint", _audioInputSource);
            base.SetAudioSource();
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }
    }
}
