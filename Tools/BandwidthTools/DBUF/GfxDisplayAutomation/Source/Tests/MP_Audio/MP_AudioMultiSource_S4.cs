
namespace Intel.VPG.Display.Automation
{
    class MP_AudioMultiSource_S4 : MP_AudioSingleSource_S4
    {
        public MP_AudioMultiSource_S4()
        {
            powerParams.PowerStates = PowerStates.S4;
            _audioInputSource = AudioInputSource.Multiple;
        }
    }
}
