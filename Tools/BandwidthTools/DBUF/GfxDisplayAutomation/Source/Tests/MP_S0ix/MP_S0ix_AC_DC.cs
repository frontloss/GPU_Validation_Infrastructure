namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Threading;
    using System.Windows.Forms;

    [Test(Type = TestType.ConnectedStandby)]
    class MP_S0ix_AC_DC : MP_S0ixBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
                Log.Message("Set the maximum display mode on all the active displays");
            }
            else
            {
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void SwitchToPowerSource()
        {
            Log.Message("Switch between AC-DC for one time");
            ACDCSwitch(PowerLineStatus.Offline); 

            Log.Message(true, "Switch to AC Power Source");
            ACDCSwitch(PowerLineStatus.Online);
            this.CSCall();
            if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) == PowerLineStatus.Online)
                Log.Success("Power Source is same as expected, system is running in AC mode");
            else
                Log.Fail("Power Source has changed after resume from S0ix state");
            Thread.Sleep(3000);

            Log.Message(true, "Switch to DC Power Source");
            ACDCSwitch(PowerLineStatus.Online);
            this.CSCall();
            if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) == PowerLineStatus.Offline)
                Log.Success("Power Source is same as expected, system is running in DC mode");
            else
                Log.Fail("Power Source has changed after resume from S0ix state");
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void ManualSteps1()
        {
            PowerLineStatus currentPowerStatus = AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI);
            string powerOption = currentPowerStatus == PowerLineStatus.Online ? "AC" : "DC";
            Log.Message("Current power source is {0} ", powerOption);
            if (!AccessInterface.SetFeature<bool, String>(Features.PromptMessage, Action.SetMethod, "Please change power source while system is in S0ix state"))
            {
                Log.Abort("User rejected Semi Automated Request");
            }
            this.CSCall();
            if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) != currentPowerStatus)
            {
                currentPowerStatus = AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI);
                powerOption = currentPowerStatus == PowerLineStatus.Online ? "AC" : "DC";
                Log.Message("Current power source is {0} ", powerOption);
                Log.Success("Power source is {0} as expected", powerOption);
            }
            else
                Log.Fail("Power Source is same after resume from S0ix state");

        }
        [Test(Type = TestType.Method, Order = 4)]
        public void ManualSteps2()
        {
            ManualSteps1();
        }

        public void ACDCSwitch(PowerLineStatus powerSource)
        {
            string powerOption = powerSource == PowerLineStatus.Online ? "AC" : "DC";
            if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) != powerSource)
            {
                if (!AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Fail("Switch to {0} power option failed", powerOption);
                else
                    Log.Message("System is in {0} power mode", powerOption);
            }
            else
                Log.Message("System is in {0} power mode", powerOption);
        }

    }
}
