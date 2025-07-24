namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class MP_AudioSingleSource : MP_Audio_Base
    {
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
        public void RebootSystem()
        {
            Log.Message(true, "Reboot the system and repeat the step 2 to 3.");
            base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);   
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void GetSetAudioEndpoint()
        {
            SetConfigMethod();
            GetAudioEndpoint();
        }
    }
}
