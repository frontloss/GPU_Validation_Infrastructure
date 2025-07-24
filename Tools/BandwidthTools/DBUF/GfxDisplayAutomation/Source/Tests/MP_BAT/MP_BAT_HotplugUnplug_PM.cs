namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_BAT_HotplugUnplug_PM : MP_BAT_HotPlug_Unplug
    {
        private PowerParams _powerParams = null;

        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            base.TestStep1();
            Invoke(PowerStates.S3);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            base.TestStep2();
            Invoke(PowerStates.S4);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.TestStep3();
            Invoke(PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.TestStep4();
            Invoke(PowerStates.S3);
        }
        private void Invoke(PowerStates State)
        {
            this._powerParams = new PowerParams() { Delay = 30 };
            _powerParams.PowerStates = State;
            _powerParams.Delay = 30;
            //  AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, _powerParams);
            base.EventResult(_powerParams.PowerStates, base.InvokePowerEvent(_powerParams, _powerParams.PowerStates));
        }
    }
}