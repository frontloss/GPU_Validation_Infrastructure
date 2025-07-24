namespace Intel.VPG.Display.Automation
{
    class MP_AudioMultiSource_S3 : MP_AudioSingleSource_S3
    {
        public MP_AudioMultiSource_S3()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }
    }
}
