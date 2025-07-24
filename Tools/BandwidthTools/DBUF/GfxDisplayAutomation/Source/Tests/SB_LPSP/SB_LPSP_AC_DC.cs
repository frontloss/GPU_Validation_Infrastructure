namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Windows.Forms;

    class SB_LPSP_AC_DC : SB_LPSP_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (!(CurrentConfig.ConfigType == DisplayConfigType.SD && CurrentConfig.PrimaryDisplay == DisplayType.EDP))
                Log.Abort("This Test is applicable only for SD-EDP.");

            base.TestStep0();
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                // Step - 1                
                _CurrentModeType.Key();

                // Step - 2
                Log.Message(true,"Enable AC Mode");
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

                // Step - 3
                Log.Message(true,"Verfiy LPSP Register");
                _CurrentModeType.Value();

                // Step - 4
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

                // Step - 5
                Log.Message(true, "Verfiy LPSP Register");
                _CurrentModeType.Value();
            }
        }
    }
}