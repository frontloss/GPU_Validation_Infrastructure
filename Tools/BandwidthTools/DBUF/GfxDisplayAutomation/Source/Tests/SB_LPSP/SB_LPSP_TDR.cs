namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class SB_LPSP_TDR : SB_LPSP_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (!(CurrentConfig.ConfigType == DisplayConfigType.SD && CurrentConfig.PrimaryDisplay == DisplayType.EDP))
                Log.Abort("This Test is applicable only for SD-EDP.");

            base.TestStep0();
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                //Step - 1
                _CurrentModeType.Key();

                // Step - 2
               RunTDRNVerify(true);

                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                if (base.CurrentConfig.GetCurrentConfigStr().Equals(currentConfig.GetCurrentConfigStr()))
                    Log.Success("Config {0} retained", base.CurrentConfig.GetCurrentConfigStr());
                else
                    Log.Fail("Expcted: {0} , Current: {1}",base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());

                // Step - 3
                Log.Message(true, "Verfiy LPSP Register");
                _CurrentModeType.Value();
            }
        }

        private void RunTDRNVerify(bool argIsLogMessageParent)
        {
            Log.Message(argIsLogMessageParent, "Run ForceTDR.exe as given in note, 'To Run TDR Application'");
            if (this.RunTDR())
                Log.Success("TDR Successful");
            else
                Log.Fail(false, "TDR Unsuccessful!");
        }

        private bool RunTDR()
        {
            Log.Verbose("Running TDR");
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
            {
                CommonExtensions.ClearRetryThruRebootFile();
                return true;
            }
            return false;
        }
    }
}