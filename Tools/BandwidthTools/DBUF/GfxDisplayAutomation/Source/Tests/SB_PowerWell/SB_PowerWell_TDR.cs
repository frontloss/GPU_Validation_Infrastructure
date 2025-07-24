namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_PowerWell_TDR : SB_PowerWell_DisplayConfig
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            RunTDRNVerify(true);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            VerifyConfig(base.CurrentConfig);
            VerifyPowerWell();    
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
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
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