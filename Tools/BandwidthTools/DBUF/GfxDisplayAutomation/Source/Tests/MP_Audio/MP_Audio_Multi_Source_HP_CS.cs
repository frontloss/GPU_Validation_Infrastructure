namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_Multi_Source_HP_CS : MP_Audio_Single_Source_HP_CS
    {
        public MP_Audio_Multi_Source_HP_CS()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }
    }
}
