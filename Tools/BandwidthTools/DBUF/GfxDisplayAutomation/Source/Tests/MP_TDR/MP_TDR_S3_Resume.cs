namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class MP_TDR_S3_Resume : MP_TDR_Base
    {
        PowerStates powerState;
        
        public MP_TDR_S3_Resume()
            : base()
        {
            this.powerState = PowerStates.S3;
        }
        public MP_TDR_S3_Resume(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.RunTDRNVerify(true);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "4. Put the system into {0} state & resume", this.powerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            base.EventResult(this.powerState, base.InvokePowerEvent(powerParams, this.powerState));
        }
    }
}