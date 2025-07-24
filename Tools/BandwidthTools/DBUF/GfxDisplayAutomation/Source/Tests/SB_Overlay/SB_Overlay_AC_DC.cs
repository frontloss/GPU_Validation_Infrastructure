namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Windows.Forms;

    public class SB_Overlay_AC_DC : SB_Overlay_S3
    {
        public SB_Overlay_AC_DC()
            : base()
        {
            _PowerEvent = this.PerformAC_DCSwitch;
        }

        private void PerformAC_DCSwitch()
        {
            Log.Message(true, "Enable AC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Offline)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in AC Mode");
                else
                    Log.Fail("Fail to set AC mode");
            }
            else
                Log.Success("System is Running in AC Mode");

            VerifyRegisters(base.CurrentConfig);

            Log.Message(true, "Enable DC Mode");
            powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");
        }    
    }
}