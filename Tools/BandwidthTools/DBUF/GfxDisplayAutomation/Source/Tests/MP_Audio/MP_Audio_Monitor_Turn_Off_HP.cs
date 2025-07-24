namespace Intel.VPG.Display.Automation
{
    using System.Threading;
    using System.Linq;

    class MP_Audio_Monitor_Turn_Off_HP : MP_Audio_Monitor_Turn_Off
    {
        [Test(Type = TestType.Method, Order = 4)]
        public void HotUnPlugDisplay()
        {
            if (base.CurrentConfig.PluggedDisplayList.Count == 0)
            {
                Log.Fail("There is No Display to plug");
            }
            foreach (DisplayType DT in base.CurrentConfig.PluggedDisplayList.Reverse<DisplayType>())
            {
                Log.Message("Hot unplugging {0} Display", DT);
                if (base.HotUnPlug(DT))
                {
                    Log.Success("Display {0} is Unplugged successfully", DT);
                    base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                }
                else
                    Log.Fail("Unable to hot plug display {0}", DT);
            }
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void HotPlugDisplayAgainAndValidateAudio()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("{0} is not enumerated..Plugging it", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Display {0} is plugged successfully", DT);
                    Log.Verbose("Verifying audio endpoint after monitor turn on");
                    base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                }
                else
                    Log.Fail("Unable to hot plug display {0}", DT);
            }
        }

    } 
}
