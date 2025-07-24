using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_MBO_Entry_After_TDR : SB_MBO_Basic
    {
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.ApplySDEDP();
            base.SwitchToDCMode();
            this.PlayVideo();
            this.RunTDRNVerify(true);
            Thread.Sleep(2000);
            base.VerifyMBOEnable();
            base.StopVideo();
            base.CleanUpHotplugFramework();
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
