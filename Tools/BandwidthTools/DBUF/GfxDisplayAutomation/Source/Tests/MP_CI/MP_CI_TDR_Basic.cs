namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_CI_TDR_Basic : TestBase
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestPreCondition()
        {
            Log.Message(true, "Connect the displays planned in the grid");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                List<uint> winMonitorIDList = base.ListEnumeratedDisplays();
                List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
                if (!enumeratedWinMonIDList.Count.Equals(winMonitorIDList.Count) && !CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Verbose("Currently enumerated displays mismatch! A reboot is required.");
                    CommonExtensions.WriteRetryThruRebootInfo();
                    base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            RunTDRNVerify(true);
        }
        protected void RunTDRNVerify(bool argIsLogMessageParent)
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