namespace Intel.VPG.Display.Automation
{
    class MP_AudioMultiSourceDisplayModeset : MP_AudioSingleSourceDisplayModeset
    {
        public MP_AudioMultiSourceDisplayModeset()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }
    }
}
