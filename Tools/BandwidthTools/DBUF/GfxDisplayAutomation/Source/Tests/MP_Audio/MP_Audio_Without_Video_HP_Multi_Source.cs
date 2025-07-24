namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_Without_Video_HP_Multi_Source : MP_Audio_Without_Video_HP_Single_Source
    {
        [Test(Type = TestType.Method, Order = 4)]
        public override void SetAudioTopologyNAudioWTVideo()
        {
            audioInputParam.audioTopology = AudioInputSource.Multiple;
            audioInputParam.audioWTVideo = AudioWTVideo.Enable;
            base.EnableDisableAudioWTVideo(audioInputParam);
        }
    }
}
