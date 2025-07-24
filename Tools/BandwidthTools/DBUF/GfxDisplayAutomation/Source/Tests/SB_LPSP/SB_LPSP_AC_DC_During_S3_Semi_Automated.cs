namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Windows.Forms;
    using System.Collections.Generic;

    class SB_LPSP_AC_DC_During_S3_Semi_Automated : SB_LPSP_Base 
    {
        protected PowerStates _PowerState = PowerStates.S3;
            
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                //Step - 1
                _CurrentModeType.Key();

                //Step - 2
                Log.Message(true,"Semi Automated Event");
                String message = "Switch AC Mode after System go to " + _PowerState;
                PromptMessage(message);

                //Step - 3
                Log.Message(true, "Power Event {0}", _PowerState);
                GotoPowerState();

                //Step - 4
                Log.Message(true, "Check Power State");
                String abortMessage = "System is Running in DC Mode";
                String successMessage = "System is Running in AC Mode";
                CheckPowerState(PowerLineStatus.Offline, abortMessage, successMessage);

                //Step - 5
                Log.Message(true,"Verify LPSP Register");
                _CurrentModeType.Value();

                //Step - 6
                Log.Message(true, "Semi Automated Event");
                message = "Switch DC Mode after System go to " + _PowerState;
                PromptMessage(message);

                //Step - 7
                Log.Message(true, "Power Event {0}", _PowerState);
                GotoPowerState();

                //Step - 8
                Log.Message(true, "Check Power State");
                abortMessage = "System is Running in AC Mode";
                successMessage = "System is Running in DC Mode";
                CheckPowerState(PowerLineStatus.Online, abortMessage, successMessage);

                //Step - 9
                Log.Message(true, "Verify LPSP Register");
                _CurrentModeType.Value();
            }
        }

        protected void PromptMessage(String pMessage)
        {
            if (!AccessInterface.SetFeature<bool, String>(Features.PromptMessage, Action.SetMethod, pMessage))
                Log.Abort("User rejected Semi Automated Request");
        }

        protected void GotoPowerState()
        {
            Log.Message("Putting the system into {0} state & resume", _PowerState);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;
            base.InvokePowerEvent(powerParams, _PowerState);
            Log.Success("Put the system into {0} state & resumed", _PowerState);
        }

        protected void CheckPowerState(PowerLineStatus pPowerState, String pAbortMessage, String pSuccessMessage)
        {
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == pPowerState)
                Log.Abort(pAbortMessage);

            Log.Success(pSuccessMessage);
        }

    }
}