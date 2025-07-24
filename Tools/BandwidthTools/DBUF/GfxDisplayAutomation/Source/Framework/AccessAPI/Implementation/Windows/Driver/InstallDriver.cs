namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Diagnostics;
    using System.Threading.Tasks;
    using System.Windows.Automation;
    using System.Collections.Generic;

    internal class InstallDriver : FunctionalBase, ISet, IParse, ISetMethod
    {
        private CancellationTokenSource _ctsSetupPopup = null;
        private Task<Process> _processTask = null;
        private string _typeContext = string.Empty;
        private bool needReboot = false;
        private bool success = false;

        public InstallDriver()
            : base()
        {
            this._typeContext = "Install";
        }
        public InstallDriver(string argContext)
            : this()
        {
            this._typeContext = argContext;
        }
        public void Parse(string[] args)
        {
            if (!args.Length.Equals(0) && args[0].ToLower().Contains("set"))
            {
                if (args.Length > 1)
                    this.Set = args[1];
                else
                    this.Set = this.GetDriverPath;
            }
            else
                this.HelpText();
        }
        public object Set
        {
            set { this.SetMethod(new InstallUnInstallParams() { ProdPath = value.ToString() }); }
        }
        public bool SetMethod(object argMessage)
        {
            InstallUnInstallParams param = argMessage as InstallUnInstallParams;
            string driverPath = param.ProdPath;
            if (Directory.Exists(base.AppSettings.ProdDriverPath))
            {
                string[] driverBaselineFiles = Directory.GetFiles(Directory.GetCurrentDirectory());
                if (Path.GetFileNameWithoutExtension(driverBaselineFiles.First()).StartsWith("15."))
                    File.Delete(driverBaselineFiles.First());
            }

            string oemFilePath = @"C:\Windows\Inf\";
            string[] oemFiles = Directory.GetFiles(Directory.GetCurrentDirectory()).ToArray().Select(f => Path.GetFileName(f)).ToArray();
            string[] driverOemFile = oemFiles.Where(dI => dI.StartsWith("oem")).ToArray();
            if (driverOemFile.Length != 0)
            {
                foreach (string oemFile in driverOemFile)
                {
                    if (File.Exists(string.Concat(Directory.GetCurrentDirectory(), "\\", oemFile)))
                        File.Copy(string.Concat(Directory.GetCurrentDirectory(), "\\", oemFile), string.Concat(oemFilePath, "\\", oemFile), true);
                }
            }
            if (string.IsNullOrEmpty(driverPath))
                driverPath = this.GetDriverPath;
            if (driverPath.EndsWith(@"\"))
                driverPath = driverPath.Remove(driverPath.Length - 1);
            if (param.AdapterType == DriverAdapterType.ATI)
            {
                this._processTask = Task.Factory.StartNew<Process>(() => CommonExtensions.StartProcess(string.Format(@"{0}\Setup.exe", driverPath), " -install"));
                return this.InstallSGProcessHandler();
            }
            else
            {
                string infFilePath = CommonExtensions.IdentifyDriverFile(driverPath);
                if (base.MachineInfo.Driver.Version == DisplayExtensions.GetDriverVesion(infFilePath).Trim().Split(',').Last() && 
                    !base.AppManager.ListTestTypeAttribute.Contains(TestType.HasINFModify))
                {
                    Log.Verbose("Same Driver already installed, returning from Driver installation");
                    return true;
                }
                Log.Verbose("{0} command issued. Driver path is {1}", this._typeContext, driverPath);
                return DriverInstallerHandle(Path.GetDirectoryName(infFilePath), param.OverrideMethodIndex, base.CurrentMethodIndex);
            }
        }

        private bool DriverInstallerHandle(string infPath, int argOverrideIndex, int argCurrentMethodIndex)
        {
            Log.Message("Installing driver through inf {0}", infPath);
            Process DPInstProcess = CommonExtensions.StartProcess("dpinst.exe", " /i /q /f /path \"" + infPath + "\" /se", 0);
            DPInstProcess.WaitForExit();
            int exitCode = DPInstProcess.ExitCode;
            int rebootCode = exitCode >> 24;
            if (rebootCode == 64)
                needReboot = true;
            int numDriverPackageSuccessCode = exitCode & 255;
            if (numDriverPackageSuccessCode != 0)
                success = true;
            if (success)
            {
                Log.Verbose("Driver Installed..");
                Log.Verbose("Reboot required to enable driver functionality");
                PowerEvent powerEvent = new PowerEvent() { CurrentMethodIndex = argCurrentMethodIndex };
                powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 10, rebootReason = RebootReason.DriverModify });
                return true;
            }
            else
                Log.Verbose("Driver Installation failed with error code {0}", exitCode);
            return false;
        }
        //This function not required as the sytem gets reboot after installing.
        //private void EnableULT()
        //{
        //    if (base.AppManager.ApplicationSettings.UseDivaFramework || base.AppManager.ApplicationSettings.UseULTFramework || base.AppManager.ApplicationSettings.UseSHEFramework)   //SHE
        //    {
        //        Log.Message("Enabling ULT again");
        //        SimulatedHotPlugDisplay simDisplay = base.CreateInstance<SimulatedHotPlugDisplay>(new SimulatedHotPlugDisplay());
        //        HotPlugUnplug argSimulationFramework = new HotPlugUnplug(FunctionName.SimulationFramework, true);
        //        simDisplay.SetMethod(argSimulationFramework);

        //        HotPlugUnplug argSimulationFeature = new HotPlugUnplug(FunctionName.SimulationFeature, true);
        //        simDisplay.SetMethod(argSimulationFeature);
        //    }
        //}
        private bool InstallSGProcessHandler()
        {
            Log.Verbose("Initiating Install SG Assertion Task");
            this._ctsSetupPopup = new CancellationTokenSource();
            Log.Verbose("Initiating SetupPopupHandler Task");
            Task popupProcess = Task.Factory.StartNew(() => this.SetupPopupHandlerSG(), this._ctsSetupPopup.Token);
            Task<bool> uninstallProcess = Task.Factory.StartNew<bool>(() => this.HasATISetupProcess());
            uninstallProcess.Wait();
            this._processTask.Wait();
            while (!(this._processTask.Result.HasExited))
                this._processTask.Wait();
            Log.Verbose("Install process assertion completed with status {0}.Install command result::{1}", _processTask.Status.ToString(), this._processTask.Result.HasExited.ToString());
            Thread.Sleep(20000);
            PowerEvent powerEvent = new PowerEvent() { CurrentMethodIndex = base.CurrentMethodIndex };
            return powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 10 });
        }
        private bool HasATISetupProcess()
        {
            bool exists = false;
            while (exists)
            {
                try
                {
                    exists = (
                        !Process.GetProcesses()
                        .Where(p => p.ProcessName.ToLower().StartsWith("atisetup") && !p.HasExited).Count().Equals(0)
                        );
                }
                catch (Exception ex)
                {
                    Log.Sporadic(false, "HasATISetupProcess:: {0}", ex.Message);
                    Log.Verbose("{0}", ex.StackTrace);
                    Thread.Sleep(60000);
                }
            }
            return exists;
        }
        private void SetupPopupHandlerSG()
        {
            while (true)
            {
                Condition mainWindowHandle = new PropertyCondition(AutomationElement.NameProperty, "Windows Security", PropertyConditionFlags.IgnoreCase);
                AutomationElement mainWindowElement = AutomationElement.RootElement.FindFirst(TreeScope.Children, mainWindowHandle);
                if (null != mainWindowElement)
                {
                    Condition installBtnHandle = new PropertyCondition(AutomationElement.NameProperty, "Install");
                    AutomationElement installBtnElement = mainWindowElement.FindFirst(TreeScope.Descendants, installBtnHandle);
                    this.ClickInstallButton(installBtnElement);
                }
                if (this._ctsSetupPopup.IsCancellationRequested)
                    break;
            }
        }
        private void ClickInstallButton(AutomationElement argBtnElement)
        {
            if (null != argBtnElement && argBtnElement.Current.ControlType.Equals(ControlType.Button))
            {
                InvokePattern pattern = argBtnElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                pattern.Invoke();
            }
        }
        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(string.Format(@"..\>Execute {0}Driver set [driverPath --> {1}]", this._typeContext, this.GetDriverPath)).Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
        private string GetDriverPath
        {
            get { return this._typeContext.Equals("Install") ? base.AppSettings.ProdDriverPath : base.AppSettings.CustomDriverPath; }
        }
    }
}