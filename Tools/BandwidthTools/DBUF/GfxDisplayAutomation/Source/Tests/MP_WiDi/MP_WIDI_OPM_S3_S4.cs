namespace Intel.VPG.Display.Automation
{
    using System.Linq;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_OPM_S3_S4 : MP_WIDIBase
    {
        DisplayConfig config = new DisplayConfig();
        protected PowerParams powerParams;

        [Test(Type = TestType.Method, Order = 1)]
        public void InstallMEDrv()
        {
            if (VerifyMEDriver() == false)
                InstallMEDriver(); 
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            if (!base.CurrentConfig.CustomDisplayList.Any(D => D.Equals(DisplayType.WIDI)))
            {
                Log.Abort("Command line dose not contains WIDI display, Hence Aborting test execution");
            }
            base.GetExternalDisplay();
            config.ConfigType = base.CurrentConfig.ConfigType;
            config.PrimaryDisplay = DisplayType.WIDI;
            if (base.CurrentConfig.DisplayList.Count == 2)
                config.SecondaryDisplay = base.pDisplayList.First();
            else if (base.CurrentConfig.DisplayList.Count == 3)
            {
                config.SecondaryDisplay = base.pDisplayList.First();
                config.TertiaryDisplay = base.pDisplayList.Last();
            }

            Log.Message(true, "Set display Config using Windows API");
            this.SetNValidateConfig(config);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void RunOPMTesterNVerify()
        {
            base.RunOPMTester(config);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void SwitchToPowerEvent_S3()
        {
            powerParams = new PowerParams() { Delay = 60, };
            powerParams.PowerStates = PowerStates.S3;
            base.SwitchToPowerEvent(powerParams);
            this.SetNValidateConfig(config);
            base.RunOPMTester(config);
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void SwitchToPowerEvent_S4()
        {
            powerParams = new PowerParams() { Delay = 60, };
            powerParams.PowerStates = PowerStates.S4;
            base.SwitchToPowerEvent(powerParams);
            this.SetNValidateConfig(config);
            base.RunOPMTester(config);
        }
    }
}
