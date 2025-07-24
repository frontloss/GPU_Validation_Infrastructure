namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.WiDi)]
    class MP_WIDI_S3 : MP_WIDIBase
    {
        protected PowerStates _powerStateOption;
        public MP_WIDI_S3()
        {
            _powerStateOption = PowerStates.S3;
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Switching display config using windows API");
            this.SetNValidateConfig(this.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SwitchToPowerEvent()
        {
            Log.Message(true, "Go to {0} on the active display and wait for 30-secs.", _powerStateOption.ToString());
            PowerParams powerParam = new PowerParams() { Delay = 30, PowerStates = _powerStateOption };
            if (AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, powerParam))
                Log.Success("{0} completed successfully", powerParam.PowerStates);
            else
                Log.Fail("{0} power state event failed !! ", powerParam.PowerStates);
            SetConfigMethod();
        }
    }
}
