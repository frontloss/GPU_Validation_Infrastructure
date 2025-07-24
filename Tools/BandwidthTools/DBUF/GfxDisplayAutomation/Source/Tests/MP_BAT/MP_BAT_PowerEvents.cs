namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class MP_BAT_PowerEvents: TestBase
    {
        protected PowerParams _powerParams = null;

        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Connect all the displays planned in the grid.");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "2. Reboot the machine.");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Verbose("Current driver is {0} - {1} - {2}", base.MachineInfo.Driver.Name, base.MachineInfo.Driver.Version, base.MachineInfo.Driver.Status);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            this._powerParams = new PowerParams() { Delay = 30 };
            Log.Message(true, "3. Goto sleep and resume.");
            base.EventResult(PowerStates.S3, base.InvokePowerEvent(this._powerParams, PowerStates.S3));
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message(true, "4. Goto hibernation and resume.");
            base.EventResult(PowerStates.S4, base.InvokePowerEvent(this._powerParams, PowerStates.S4));
        }
    }
}