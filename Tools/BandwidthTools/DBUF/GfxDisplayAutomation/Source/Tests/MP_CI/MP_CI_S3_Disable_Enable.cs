namespace Intel.VPG.Display.Automation
{
    class MP_CI_S3_Disable_Enable : TestBase
    {
        PowerStates powerState;

        public MP_CI_S3_Disable_Enable()
            : base()
        {
            this.powerState = PowerStates.S3;
        }
        public MP_CI_S3_Disable_Enable(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            Log.Message(true, "Goto {0} and resume.", this.powerState);
            base.EventResult(this.powerState, base.InvokePowerEvent(powerParams, this.powerState));
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Disable the driver from Device manager.");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Enable the driver from Device manager.");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });
        }
    }
}
