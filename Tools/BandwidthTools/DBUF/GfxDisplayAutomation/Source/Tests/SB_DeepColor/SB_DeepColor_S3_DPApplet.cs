namespace Intel.VPG.Display.Automation
{
    using System;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_S3_DPApplet : SB_Deepcolor_DisplayConfig_DPApplet
    {
        protected PowerStates powerState;

        public SB_DeepColor_S3_DPApplet()
            : base()
        {
            this.powerState = PowerStates.S3;
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
        }
        public SB_DeepColor_S3_DPApplet(PowerStates argPowerState)
            : this()
        {
            this.powerState = argPowerState;
        }

        private void ActionAfterEnable()
        {
            GotoPowerState();
            base.TestStep2();
        }
        private void ActionAfterDisable()
        {
            GotoPowerState();
            base.TestStep5();
        }

        private void GotoPowerState()
        {
            Log.Message("Putting the system into {0} state & resume", this.powerState);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 15;
            base.InvokePowerEvent(powerParams, this.powerState);
            Log.Success("Put the system into {0} state & resumed", this.powerState);
        }
    }
}