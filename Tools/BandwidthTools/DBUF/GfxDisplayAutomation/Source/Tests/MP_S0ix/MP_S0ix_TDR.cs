namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.ConnectedStandby)]
    class MP_S0ix_TDR : MP_S0ixBase
    {
        #region Test
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
                Log.Message("Set the maximum display mode on all the active displays");
            }
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SendSysytemToS0ix()
        {
            this.CSCall();
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void RunTDRNVerify()
        {
            if (!GetListEnumeratedDisplays())
                Log.Fail("Display enumeration mismatch after comming from S0ix");
            else
                Log.Message("Connected displays are enumerated properly");

            Log.Message(true, "Running ForceTDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true, "TDR unsuccessful! A reboot may be required.");
                    CommonExtensions.WriteRetryThruRebootInfo();
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5}, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
            }
            else
                CommonExtensions.ClearRetryThruRebootFile();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void S0ix()
        {
            //base.DisableLAN();
            SendSysytemToS0ix();
        }

        #endregion
    }
}
