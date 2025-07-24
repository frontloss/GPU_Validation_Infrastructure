namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class SB_Overlay_S3 : SB_Overlay_Basic
    {
        protected PowerStates _PowerState ;
        protected System.Action _PowerEvent = null;
        public SB_Overlay_S3()
            : base()
        {
            _PowerState = PowerStates.S3;
            _PowerEvent = PowerEvent;
            _actionAfterVerify = ActionAfterVerify;
        }

        private void ActionAfterVerify()
        {
            _PowerEvent();
            VerifyRegisters(base.CurrentConfig);
        }
        protected void PowerEvent()
        {
            Log.Verbose("Putting the system into {0} state & resume ", _PowerState);   
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;
            base.InvokePowerEvent(powerParams,_PowerState);
            Log.Success("Put the system into {0} state & resumed ", _PowerState);   
        }
    }
}