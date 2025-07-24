namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.WiDi)]
    [Test(Type = TestType.HasReboot)]
    class MP_WIDI_TDR_Simulation : MP_WIDIBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            this.SetNValidateConfig(this.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void RunTDRNVerify()
        {
            if (!base.IsWiDiConnected())
                base.WiDiReConnect(true);
            if(CommonExtensions._rebootAnalysysInfo.rebootReason == RebootReason.TDRUnsuccessful)
                this.SetNValidateConfig(this.CurrentConfig);
            Log.Message(true, "Running ForceTDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true,"TDR unsuccessful! A reboot may be required.");
                    CommonExtensions.WriteRetryThruRebootInfo();
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5, rebootReason = RebootReason.TDRUnsuccessful}, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
            }
            else
                CommonExtensions.ClearRetryThruRebootFile();
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SetConfigMethodAgain()
        {
            Log.Message("Check current system config");
            DisplayConfig configAfterTRD = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            Log.Verbose(configAfterTRD.GetCurrentConfigStr());
            if (configAfterTRD.ConfigType == this.CurrentConfig.ConfigType &&
                configAfterTRD.PrimaryDisplay == this.CurrentConfig.PrimaryDisplay &&
                configAfterTRD.SecondaryDisplay == this.CurrentConfig.SecondaryDisplay &&
                configAfterTRD.TertiaryDisplay == this.CurrentConfig.TertiaryDisplay)
                Log.Success("Display config same as expected");
            else
                Log.Fail("Display config not same as expected current config: {0} Expected config: {1} ", configAfterTRD.GetCurrentConfigStr(), this.CurrentConfig.GetCurrentConfigStr());
        }
    }
}
