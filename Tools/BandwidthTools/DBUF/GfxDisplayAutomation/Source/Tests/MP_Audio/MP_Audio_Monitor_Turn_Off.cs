namespace Intel.VPG.Display.Automation
{
    using System.Threading;

    class MP_Audio_Monitor_Turn_Off : MP_Audio_Base
    {
        MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
        [Test(Type = TestType.Method, Order = 1)]
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

        [Test(Type = TestType.Method, Order = 2)]
        public void GetAudioEndpoint()
        {
            Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void GotoMonitorTurnOff()
        {
            monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
            monitorOnOffParam.waitingTime = 60;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
            Log.Success("Successfully able to turn OFF and ON monitor");
            Log.Verbose("Verifying audio endpoint after monitor turn OFF and ON");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }
    }
}
