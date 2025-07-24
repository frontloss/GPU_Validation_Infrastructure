namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;
    using System.Windows.Forms;

    class SB_DisplayCStates_AC_DC_Switch : SB_DisplayCStates_BasicFeature 
    {
        protected uint DMCVersion = 0;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void ACDCSwitch()
        {
            DMCVersion = GetRegisterValue("DMC_VERSION", PIPE.NONE, PLANE.NONE, PORT.NONE);
            Log.Message(true, "DMC Version for {0}", DMCVersion );

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
        }


        [Test(Type = TestType.Method, Order = 3)]
        public void DCMode()
        {
            Log.Message(true, "Enable DC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");
            base.Method();
        }
    } 
}