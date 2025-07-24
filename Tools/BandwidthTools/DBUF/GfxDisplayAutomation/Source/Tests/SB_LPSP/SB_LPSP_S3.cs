namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class SB_LPSP_S3 : SB_LPSP_Base
    {
        protected PowerStates _PowerState ;
        protected System.Action _PowerEvent = null ;

        public SB_LPSP_S3()
        {
            _PowerEvent = this.PowerEvent;
            _PowerState = PowerStates.S3;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                //Step - 1
                _CurrentModeType.Key();

                // Step - 2
                Log.Message(true, "Power Event {0}" , _PowerState);
                _PowerEvent();

                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                if (base.CurrentConfig.GetCurrentConfigStr().Equals(currentConfig.GetCurrentConfigStr()))
                    Log.Success("Config {0} retained", base.CurrentConfig.GetCurrentConfigStr());
                else
                    Log.Fail("Expcted: {0} , Current: {1}",base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
                // Step - 3
                Log.Message(true, "Verfiy LPSP Register");
                _CurrentModeType.Value();
            }
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