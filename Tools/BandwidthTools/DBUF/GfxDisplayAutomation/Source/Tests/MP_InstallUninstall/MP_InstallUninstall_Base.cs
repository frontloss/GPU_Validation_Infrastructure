namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    class MP_InstallUninstall_Base : TestBase
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
            Log.Message("{0}. {1} IGD", argStepNumbers.First(), argState);
            bool initState = AccessInterface.SetFeature<bool>(argFeature, Action.SetNoArgs);
            AccessInterface.SetFeature<bool>(Features.DriverFunction, Action.SetNoArgs);
            base.MachineInfo.Driver.PrintBasicDetails();
            if (initState)
            {
                Log.Message("{0}. Verify IGD got {1}.", argStepNumbers.Last(), argState);
                return base.MachineInfo.Driver.Status.ToLower().Equals(argState.ToString().ToLower());
            }
            return false;
        }
        protected void DisableNVerifyIGDWithDTCM(int argStepNumber)
        {
            Log.Message("{0}) Disable the IGD driver and verify IGD driver should be disabled and the system should run on VGA driver", argStepNumber);
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { argStepNumber, argStepNumber });

            DTCMHelper dtcmHelper = new DTCMHelper(base.ApplicationManager, DTCMAccess.Desktop);
            bool hasGraphicsPropertiesInDTCM = dtcmHelper.IsFeatureVisible(Features.DTCMFeature);
            if (!hasGraphicsPropertiesInDTCM)
                Log.Success("Driver running in VGA mode. {0}", base.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Abort("Driver disable failed! {0}", base.MachineInfo.Driver.GetDriverInfoStr());
        }
        protected void EnableNVerifyIGDBasic(int argStepNumber)
        {
            Log.Message("{0}) Enable the IGD driver and verify IGD driver should be enabled and the system should run on IGD driver.", argStepNumber);
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { argStepNumber, argStepNumber });
            if (CommonExtensions.IntelDriverStringList.Any(str => base.MachineInfo.Driver.Name.ToLower().Contains(str)) && base.MachineInfo.Driver.Status.ToLower().Contains("running"))
                Log.Success("{0}", base.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Fail("Driver enable failed! {0}", base.MachineInfo.Driver.GetDriverInfoStr());
        }
        protected bool InvokePowerEvent(PowerParams argPowerParams, PowerStates argState)
        {
            argPowerParams.PowerStates = argState;
            return AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, argPowerParams);
        }
        protected void EventResult(PowerStates argState, bool argResult)
        {
            if (argResult)
                Log.Success("{0} completed successfully", argState);
            else
                Log.Alert("{0} not successful!", argState);
        }
        protected void GetOSDriverVersionNStatus(List<string> argDriverNameStrList)
        {
            if (argDriverNameStrList.Any(str => base.MachineInfo.Driver.Name.ToLower().Contains(str)) && base.MachineInfo.Driver.Status.ToLower().Contains("running"))
                Log.Success("Driver switched to {0}", base.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Abort("Driver install failed. Current driver is {0}", base.MachineInfo.Driver.GetDriverInfoStr());
        }
        protected void GetOSDriverVersionNStatus(List<string> argDriverNameStrList, bool argNullDriverVersion)
        {
            if (argDriverNameStrList.Any(str => base.MachineInfo.Driver.Name.ToLower().Contains(str)) || (string.IsNullOrEmpty(base.MachineInfo.Driver.Name) && string.IsNullOrEmpty(base.MachineInfo.Driver.Version)))
                Log.Success("Driver switched to {0}", string.IsNullOrEmpty(base.MachineInfo.Driver.Version) ? "VGA mode" : base.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Abort("Driver install failed. Current driver is {0}", base.MachineInfo.Driver.GetDriverInfoStr());
        }
        protected bool CheckOSDriverVersionNStatus(List<string> argDriverNameStrList)
        {
            return (argDriverNameStrList.Any(str => base.MachineInfo.Driver.Name.ToLower().Contains(str)) || (string.IsNullOrEmpty(base.MachineInfo.Driver.Name) && string.IsNullOrEmpty(base.MachineInfo.Driver.Version)));
        }
        protected List<uint> ListEnumeratedDisplays()
        {
            Log.Verbose("Current enumerated displays");
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
        protected void UninstallThruUI()
        {
            File.Delete(CommonExtensions.UninstallFile);
            if (!this.CheckOSDriverVersionNStatus(CommonExtensions.StandardDriverStringList))
            {
                Log.Sporadic(false, "Driver uninstallation failed! Trying through UI method");
                base.MachineInfo.Driver.PrintBasicDetails();
                AccessInterface.SetFeature<bool>(Features.UnInstallDriver, Action.SetNoArgs, Source.AccessUI);
            }
        }
        protected void SetBCDEditOptions(string disableIntegrityChecks, string testSigning)
        {
            CommonExtensions.StartProcess("bcdedit", disableIntegrityChecks);
            CommonExtensions.StartProcess("bcdedit", testSigning);
            this.InvokePowerEvent(new PowerParams() { Delay = 10, PowerStates = PowerStates.S5 }, PowerStates.S5);
        }
        protected void CheckBCDEditOptions(string loadOptions, string testSigning)
        {
            string result = string.Empty;
            Process bcdedit = CommonExtensions.StartProcess("bcdedit");
            string normalisedLoadOptions = Regex.Replace(loadOptions, @"\s+", string.Empty);
            string normalisedTestSigning = Regex.Replace(testSigning, @"\s+", string.Empty);
            while (!bcdedit.StandardOutput.EndOfStream)
            {
                result = bcdedit.StandardOutput.ReadLine();
                string normalisedResult = Regex.Replace(result, @"\s+", string.Empty);
                if (string.Equals(normalisedResult, normalisedLoadOptions, StringComparison.OrdinalIgnoreCase))
                    Log.Success("{0} set", loadOptions);
                if (string.Equals(normalisedResult, normalisedTestSigning, StringComparison.OrdinalIgnoreCase))
                    Log.Success("{0} set", testSigning);
            }
        }
    }
}