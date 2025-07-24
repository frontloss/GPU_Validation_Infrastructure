namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    class MP_AudioSingleSource_S3 : MP_Audio_Base
    {
        protected PowerParams powerParams;
        public MP_AudioSingleSource_S3()
        {
            powerParams = new PowerParams() { Delay = 45, };
            powerParams.PowerStates = PowerStates.S3;
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void SetAudioSource()
        {
            base.SetAudioSource();
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
        public void GotopowerState()
        {
            Log.Message(true, "Going {0} state and Resume the system from {1} after {2} seconds", powerParams.PowerStates, powerParams.PowerStates, powerParams.Delay);
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
            GetAudioEndpoint();
        }
    }
}
