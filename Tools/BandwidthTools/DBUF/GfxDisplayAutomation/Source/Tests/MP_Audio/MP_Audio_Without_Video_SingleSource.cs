namespace Intel.VPG.Display.Automation
{
    using System.Threading;

    class MP_Audio_Without_Video_SingleSource : MP_Audio_Base
    {
        SetAudioParam audioInputParam = new SetAudioParam();
        MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void SetAudioTopologyNAudioWTVideo()
        {
            audioInputParam.audioTopology = AudioInputSource.Single;
            audioInputParam.audioWTVideo = AudioWTVideo.Enable;
            base.EnableDisableAudioWTVideo(audioInputParam);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void GetAudioEndpoint()
        {
            Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void VerifyAudioEndpoint()
        {
            Log.Message(true, "Verifying audio endpoint while monitor is turned off, Not playing audio to external display");
            monitorOnOffParam.onOffParam = MonitorOnOff.Off;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
            Log.Success("Successfully able to turn off monitor");
            Log.Verbose("Wait for 40 sec and resume the system");
            Thread.Sleep(40000);
            Log.Verbose("Verifying audio endpoint in monitor turn off state");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
            
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void WakeMonitor()
        {
            monitorOnOffParam.onOffParam = MonitorOnOff.On;
            Log.Verbose("Wake monitor from turn off using keyboard event");
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
            Log.Success("Successfully able to turn on monitor");
            Log.Verbose("Verifying audio endpoint after monitor turn on");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void DisableAudioWTVideo()
        {
            Log.Message(true, "disabling audio without video using CUI and verifying audio endpoint");
            audioInputParam.audioTopology = AudioInputSource.Single;
            audioInputParam.audioWTVideo = AudioWTVideo.Disable;
            base.EnableDisableAudioWTVideo(audioInputParam);

            Log.Message("Verifying audio endpoint while monitor is turned off, Not playing audio to external display");
            monitorOnOffParam.onOffParam = MonitorOnOff.Off;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
            Log.Success("Successfully able to turn off monitor");
            Log.Verbose("Wait for 45 sec and resume the system");
            Thread.Sleep(45000);
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
            WakeMonitor();
        }
    }
}
