namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    internal class CommonRoutines
    {
        private IApplicationManager _appManager = null;

        internal CommonRoutines(IApplicationManager argAppManager)
        {
            this._appManager = argAppManager;
        }

        internal void AssertDriverState(Features argFeature, DriverState argState, int[] argStepNumbers)
        {
            if (this.ChangeDriverState(argFeature, argState, argStepNumbers))
                Log.Success("IGD {0}", argState);
            else
                Log.Abort("IGD not {0}!", argState);
        }
        internal bool ChangeDriverState(Features argFeature, DriverState argState, int[] argStepNumbers)
        {
            Log.Message(true, "{0}. {1} IGD", argStepNumbers.First(), argState);
            bool initState = AccessInterface.SetFeature<bool, DriverAdapterType>(argFeature, Action.SetMethod, DriverAdapterType.Intel);
            //AccessInterface.SetFeature<bool>(Features.DriverFunction, Action.SetNoArgs);
            this.MachineInfo.Driver.PrintBasicDetails();
            if (initState)
            {
                Log.Message(true, "{0}. Verify IGD got {1}.", argStepNumbers.Last(), argState);
                return this.MachineInfo.Driver.Status.ToLower().Equals(argState.ToString().ToLower());
            }
            return false;
        }
        internal void DisableNVerifyIGDWithDTCM(int argStepNumber)
        {
            Log.Message(true, "{0}) Disable the IGD driver and verify IGD driver should be disabled and the system should run on VGA driver", argStepNumber);
            this.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { argStepNumber, argStepNumber });
            AccessInterface.SetFeature<string>(Features.DTCMShowDesktop, Action.Set, "");
            if (!(AccessInterface.GetFeature<bool, string>(Features.DTCMFeature, Action.GetMethod, Source.WindowsAutomationUI, "Graphics_Properties")))
                Log.Success("Driver running in VGA mode. {0}", this.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Fail("Driver disable failed! {0}", this.MachineInfo.Driver.GetDriverInfoStr());
        }
        internal void EnableNVerifyIGDBasic(int argStepNumber)
        {
            Log.Message(true, "{0}) Enable the IGD driver and verify IGD driver should be enabled and the system should run on IGD driver.", argStepNumber);
            this.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { argStepNumber, argStepNumber });
            if (CommonExtensions.IntelDriverStringList.Any(str => this.MachineInfo.Driver.Name.ToLower().Contains(str))
                && this.MachineInfo.Driver.Status.ToLower().Contains("running"))
                Log.Success("{0}", this.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Fail("Driver enable failed! {0}", this.MachineInfo.Driver.GetDriverInfoStr());
        }
        internal bool InvokePowerEvent(PowerParams argPowerParams, PowerStates argState)
        {
            argPowerParams.PowerStates = argState;
            return AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, argPowerParams);
        }
        internal void EventResult(PowerStates argState, bool argResult)
        {
            if (argResult)
                Log.Success("{0} completed successfully", argState);
            else
                Log.Fail("{0} not successful!", argState);
        }
        internal void GetOSDriverVersionNStatus(List<string> argDriverNameStrList)
        {
            if (argDriverNameStrList.Any(str => this.MachineInfo.Driver.Name.ToLower().Contains(str)) && this.MachineInfo.Driver.Status.ToLower().Contains("running"))
                Log.Success("Driver switched to {0}", this.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Abort("Driver install failed. Current driver is {0}", this.MachineInfo.Driver.GetDriverInfoStr());
        }
        internal void GetOSDriverVersionNStatus(List<string> argDriverNameStrList, string argDriverVersion)
        {
            if (argDriverNameStrList.Any(str => this.MachineInfo.Driver.Name.ToLower().Contains(str)) && this.MachineInfo.Driver.Status.ToLower().Contains("running") && this.MachineInfo.Driver.Version.Equals(argDriverVersion))
                Log.Success("Driver switched to {0}", this.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Abort("Driver install failed. Current driver is {0}", this.MachineInfo.Driver.GetDriverInfoStr());
        }
        internal void GetOSDriverVersionNStatus(List<string> argDriverNameStrList, bool argNullDriverVersion)
        {
            if (argDriverNameStrList.Any(str => this.MachineInfo.Driver.Name.ToLower().Contains(str)) || (string.IsNullOrEmpty(this.MachineInfo.Driver.Name) && string.IsNullOrEmpty(this.MachineInfo.Driver.Version)))
                Log.Success("Driver switched to {0}", string.IsNullOrEmpty(this.MachineInfo.Driver.Version) ? "VGA mode" : this.MachineInfo.Driver.GetDriverInfoStr());
            else
                Log.Abort("Driver install failed. Current driver is {0}", this.MachineInfo.Driver.GetDriverInfoStr());
        }
        internal bool CheckOSDriverVersionNStatus(List<string> argDriverNameStrList)
        {
            return (argDriverNameStrList.Any(str => this.MachineInfo.Driver.Name.ToLower().Contains(str)) || (string.IsNullOrEmpty(this.MachineInfo.Driver.Name) && string.IsNullOrEmpty(this.MachineInfo.Driver.Version)));
        }
        internal List<uint> ListEnumeratedDisplays()
        {
            Log.Verbose("Current enumerated displays in test context #{0}", this.EnumeratedDisplays.Count);
            Log.Verbose("*****************");
            this.EnumeratedDisplays.ForEach(dI => Log.Verbose("{0}", dI.DisplayType));
            Log.Verbose("*****************");
            List<uint> winMonitorIDs = AccessInterface.GetFeature<List<uint>>(Features.WindowsMonitorID, Action.GetAll);
            DisplayInfo displayInfo = null;
            Log.Verbose("Current enumerated displays in system context #{0}", winMonitorIDs.Count);
            Log.Verbose("*****************");
            winMonitorIDs.ForEach(iD =>
            {
                displayInfo = this.EnumeratedDisplays.Where(dI => dI.WindowsMonitorID.Equals(iD)).FirstOrDefault();
                if (null != displayInfo)
                    Log.Verbose("{0} - {1}", displayInfo.DisplayType, displayInfo.CompleteDisplayName);
            });
            Log.Verbose("*****************");
            return winMonitorIDs;
        }
        internal void UninstallThruUI()
        {
            //File.Delete(CommonExtensions.UninstallFile);
            if (AccessInterface.SetFeature<bool>(Features.UnInstallDriver, Action.SetNoArgs, Source.WindowsAutomationUI))
                _appManager.MachineInfo.Driver = AccessInterface.GetFeature<DriverInfo>(Features.DriverFunction, Action.Get);
        }

        internal bool InstallThruUI(string driverPath)
        {
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = driverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, Source.WindowsAutomationUI, param))
            {
                _appManager.MachineInfo.Driver = AccessInterface.GetFeature<DriverInfo>(Features.DriverFunction, Action.Get);
                return true;
            }
            return false;
        }

        internal void SetBCDEditOptions(string disableIntegrityChecks, string testSigning)
        {
            CommonExtensions.StartProcess("bcdedit", disableIntegrityChecks);
            CommonExtensions.StartProcess("bcdedit", testSigning);
            this.InvokePowerEvent(new PowerParams() { Delay = 10, PowerStates = PowerStates.S5 }, PowerStates.S5);
        }
        internal void CheckBCDEditOptions(string loadOptions, string testSigning)
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

        private IAccessInterface AccessInterface
        {
            get { return this._appManager.AccessInterface; }
        }
        private MachineInfo MachineInfo
        {
            get { return this._appManager.MachineInfo; }
        }
        private List<DisplayInfo> EnumeratedDisplays
        {
            get { return this._appManager.ParamInfo.Get<List<DisplayInfo>>(ArgumentType.Enumeration); }
        }
    }
}