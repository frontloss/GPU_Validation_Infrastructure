namespace Intel.VPG.Display.Automation
{
    class MP_Audio_Without_Video_MultiSource : MP_Audio_Without_Video_SingleSource
    {
        SetAudioParam audioInputParam = new SetAudioParam();
        MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();

        [Test(Type = TestType.Method, Order = 1)]
        public override void SetAudioTopologyNAudioWTVideo()
        {
            audioInputParam.audioTopology = AudioInputSource.Multiple;
            audioInputParam.audioWTVideo = AudioWTVideo.Enable;
            base.EnableDisableAudioWTVideo(audioInputParam);
        }
    }
}
