namespace Intel.VPG.Display.Automation
{
    class MP_CI_Rotation_S3 : MP_CI_Rotation
    {
        private PowerStates _powerState = PowerStates.S3;

        public MP_CI_Rotation_S3()
            : base()
        {
            base._powerStateAction = () => base.EventResult(this._powerState, base.InvokePowerEvent(new PowerParams() { Delay = 30 }, this._powerState));
        }
        public MP_CI_Rotation_S3(PowerStates argPowerState)
            : this()
        {
            this._powerState = argPowerState;
        }
    }
}