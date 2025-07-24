namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;
    using System.Windows.Automation;

    class MP_ConnectedStandbyTDR : MP_ConnectedStandbyBase
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
                this.CleanUP();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SendSysytemToS0ix()
        {
            this.S0ixCall();
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void RunTDRNVerify()
        {
            Log.Message(true, "Running ForceTDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true, "TDR unsuccessful! A reboot may be required.");
                    this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5, OverrideMethodIndex = 1 }, PowerStates.S5);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
            }
            else
                CommonExtensions.ClearRetryThruRebootFile();
            SendSysytemToS0ix();
        }

        #endregion

        #region PostCondition
        [Test(Type = TestType.PostCondition, Order = 5)]
        public void TestPostCondition()
        {
            this.CleanUP();
        }
        #endregion
    }
}
