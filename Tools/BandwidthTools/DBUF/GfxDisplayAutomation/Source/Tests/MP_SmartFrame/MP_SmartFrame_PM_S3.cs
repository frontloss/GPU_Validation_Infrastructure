namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class MP_SmartFrame_PM_S3 : MP_SmartFrame_Base
    {
        internal PowerStates powerState;
        public MP_SmartFrame_PM_S3()
            : base()
        {
            powerState = PowerStates.S3;
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set config SD {0} via OS", base.GetInternalDisplay());
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.SD;
            config.PrimaryDisplay = base.GetInternalDisplay();
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, config))
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
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Put the system into {0} state & resume", this.powerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            base.EventResult(this.powerState, base.InvokePowerEvent(powerParams, this.powerState));
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
            Log.Message(true, "Put the system into {0} state & resume", this.powerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            base.EventResult(this.powerState, base.InvokePowerEvent(powerParams, this.powerState));
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Swtich to SF mode. SF Should be enabled");
            base.EnableRegistryForSF();
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
    }
}
