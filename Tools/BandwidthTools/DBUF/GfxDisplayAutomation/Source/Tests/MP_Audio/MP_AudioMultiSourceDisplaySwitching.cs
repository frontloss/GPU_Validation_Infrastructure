namespace Intel.VPG.Display.Automation
{
    class MP_AudioMultiSourceDisplaySwitching : MP_AudioSingleSourceDisplaySwitching
    {
        public MP_AudioMultiSourceDisplaySwitching()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }
    }
}
