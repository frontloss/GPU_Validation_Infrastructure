namespace Intel.VPG.Display.Automation
{
    class MP_NativeCollage_PowerEvents : MP_NativeCollage_BAT
    {
        PowerParams _powerParams = null;
        public MP_NativeCollage_PowerEvents()
        {
            base._performAction = this.PerformAction;
        }
        private void PerformAction()
        {
            Log.Message(true, "Put the system to {0} and resume", PowerStates.S3);
            this._powerParams = new PowerParams() { Delay = 30, };
            base.InvokePowerEvent(this._powerParams, PowerStates.S3);
            //Log.Message(true, "Verify that the system comes back in the same configuration after {0}", PowerStates.S3);
            //base.VerifyCollagePersistence(setConfigString,1);
            if (base.CheckCollageThruResolution(displayConfig.ConfigType, currentMode, base.CurrentConfig.DisplayList.Count))
                Log.Success("{0} is verified to be successfully set using Resolutions after resuming from S3", displayConfig.ConfigType);
            else
                Log.Sporadic("{0} is not verified using Resolutions after resuming from S3", displayConfig.ConfigType);
            Log.Message(true, "Put the system to {0} and resume", PowerStates.S4);
            this._powerParams = new PowerParams() { Delay = 30, };
            base.InvokePowerEvent(this._powerParams, PowerStates.S4);
            //Log.Message(true, "Verify that the system comes back in the same configuration after {0}", PowerStates.S4);
            //base.VerifyCollagePersistence(setConfigString,1);
            if (base.CheckCollageThruResolution(displayConfig.ConfigType, currentMode, base.CurrentConfig.DisplayList.Count))
                Log.Success("{0} is verified to be successfully set using Resolutions after resuming from S4", displayConfig.ConfigType);
            else
                Log.Sporadic("{0} is not verified using Resolutions after resuming from S4", displayConfig.ConfigType);
        }
    }
}