namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_DisplaySwitch_Base : TestBase
    {
        protected void AssertDriverState(Features argFeature, DriverState argState, int[] argStepNumbers)
        {
            if (this.ChangeDriverState(argFeature, argState, argStepNumbers))
                Log.Success("IGD {0}", argState);
            else
                Log.Abort("IGD not {0}!", argState);
        }
        protected bool ChangeDriverState(Features argFeature, DriverState argState, int[] argStepNumbers)
        {
            Log.Message(true, "{0}. {1} IGD", argStepNumbers.First(), argState);
            bool initState = AccessInterface.SetFeature<bool>(argFeature, Action.SetNoArgs);
            AccessInterface.SetFeature<bool>(Features.DriverFunction, Action.SetNoArgs);
            base.MachineInfo.Driver.PrintBasicDetails();
            if (initState)
            {
                Log.Message(true, "{0}. Verify IGD got {1}.", argStepNumbers.Last(), argState);
                return base.MachineInfo.Driver.Status.ToLower().Equals(argState.ToString().ToLower());
            }
            return false;
        }
        protected void EnableNVerifyIGDBasic(int argStepNumber)
        {
            Log.Message(true, "{0}) Enable the IGD driver and verify IGD driver should be enabled and the system should run on IGD driver.", argStepNumber);
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { argStepNumber, argStepNumber });
            if (CommonExtensions.IntelDriverStringList.Any(str => base.MachineInfo.Driver.Name.ToLower().Contains(str))
                && base.MachineInfo.Driver.Status.ToLower().Contains("running"))
                Log.Success("{0}", base.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Fail("Driver enable failed! {0}", base.MachineInfo.Driver.GetDriverInfoStr());
        }
        protected List<uint> ListEnumeratedDisplays()
        {
            Log.Verbose("Current enumerated displays in test context");
            Log.Verbose("*****************");
            base.CurrentConfig.EnumeratedDisplays.ForEach(dI => Log.Verbose("{0}", dI.DisplayType));
            Log.Verbose("*****************");
            List<uint> winMonitorIDs = AccessInterface.GetFeature<List<uint>>(Features.WindowsMonitorID, Action.GetAll);
            DisplayInfo displayInfo = null;
            winMonitorIDs.ForEach(iD =>
            {
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.WindowsMonitorID.Equals(iD)).FirstOrDefault();
                if (null != displayInfo)
                    Log.Verbose("{0} - {1}", displayInfo.DisplayType, displayInfo.CompleteDisplayName);
            });
            return winMonitorIDs;
        }
        protected bool InvokePowerEvent(PowerParams argPowerParams, PowerStates argState)
        {
            argPowerParams.PowerStates = argState;
            return AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, argPowerParams);
        }
     }
}