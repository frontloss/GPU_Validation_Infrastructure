using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_modes_DisplaySwap_TDR : SB_modes_DisplaySwap_Basic
    {
        protected override void VerifyMode(List<DisplayModeList> argDispModeList)
        {
            this.RunTDR(1);
            base.VerifyMode(argDispModeList);
        }
        private bool RunTDR(int argOverrideIdx)
        {
            Log.Verbose("Running TDR");
            if (!AccessInterface.SetFeature<bool>(Features.ForceTDR, Action.SetNoArgs))
            {
                if (!CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(true, "TDR unsuccessful! A reboot may be required.");
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

