namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_Without_Video_HP_Single_Source : MP_Audio_Base
    {
        internal SetAudioParam audioInputParam = new SetAudioParam();
        MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();

        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void HotPlugExternalDisplay()
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
        public void SetDisplayConfig()
        {
            if (base.CurrentConfig.EnumeratedDisplays.Count == base.CurrentConfig.DisplayList.Count)
            {
                Log.Message(true, "Set Current config via OS call");
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                    Log.Success("Config applied successfully");
                else
                {
                    Log.Abort("Config not applied!");
                }
            }
            else
                Log.Abort("Required display is not enumerated");
        }

        [Test(Type = TestType.Method, Order = 4)]
        public virtual void SetAudioTopologyNAudioWTVideo()
        {
            audioInputParam.audioTopology = AudioInputSource.Single;
            audioInputParam.audioWTVideo = AudioWTVideo.Enable;
            base.EnableDisableAudioWTVideo(audioInputParam);
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void GetAudioEndpoint()
        {
            Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void VerifyAudioEndpoint()
        {
            if (DisplayExtensions.pluggedDisplayList.Count != 0)
            {
                Log.Message(true, "Turning off monitor for 60 sec and hot unplug display {0}", DisplayExtensions.pluggedDisplayList.First());
                base.HotUnPlug(DisplayExtensions.pluggedDisplayList.First(), true);
                monitorOnOffParam.onOffParam = MonitorOnOff.Off;
                AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
                Log.Success("Successfully able to turn off monitor");

                Thread.Sleep(60000);
                GetAudioEndpoint();

                monitorOnOffParam.onOffParam = MonitorOnOff.On;
                Log.Verbose("Wake monitor from turn off using keyboard event");
                AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
                Log.Success("Successfully able to turn on monitor");

                GetAudioEndpoint();

                if (base.EnumeratedDisplays.Select(DT => DT.DisplayType == DisplayExtensions.pluggedDisplayList.First()).FirstOrDefault())
                {
                    Log.Fail("Unable to hot unplug display {0} in LP state", base.CurrentConfig.PluggableDisplayList.First());
                }
                else
                    Log.Success("Successfully hot unplug display {0} in LP state", base.CurrentConfig.PluggableDisplayList.First());
            }
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void HotPlugUnPlugExternalDisplay()
        {
            DisplayType DT = DisplayType.None;
            Log.Message(true, "Hotplug and UnPlug external display and verify audio endpoint");
            monitorOnOffParam.onOffParam = MonitorOnOff.Off;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
            Log.Success("Successfully able to turn off monitor");
            int currentDisplay = base.CurrentConfig.EnumeratedDisplays.Count;
            if(DisplayExtensions.pluggedDisplayList.Count > 1)
            {
                if (base.HotPlug(DisplayExtensions.pluggedDisplayList.First()))
                {
                    Log.Success("Successfully able to hotplug display {0}", DT);
                    Thread.Sleep(5000);
                    if (base.HotUnPlug(DisplayExtensions.pluggedDisplayList.Last()))
                    {
                        Log.Success("Successfully able to hot unplug display {0}", DT);
                    }
                    else
                        Log.Fail("Unable to hot unplug display {0}", DT);
                }
                Log.Fail("Unable to hotplug display {0}", DT);
            }
            int dispCount = base.CurrentConfig.EnumeratedDisplays.Count;
            if (currentDisplay == dispCount)
            {
                Log.Fail("Unable to hot Unplug display {0} in low power", DisplayExtensions.pluggedDisplayList.Last());
            }
            monitorOnOffParam.onOffParam = MonitorOnOff.On;
            Log.Verbose("Wake monitor from turn off using keyboard event");
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
            Log.Success("Successfully able to turn on monitor");

            GetAudioEndpoint();
            Log.Verbose("Default audio endpoint device {0}", base.GetDefaultEndPoint().FriendlyName);
        }
    }
}
