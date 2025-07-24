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

    internal class UnInstallDriver : FunctionalBase, ISetMethod, IParse
    {
        private string oemFilePath = @"C:\Windows\Inf\";
        private bool needReboot = false;
        private bool success = false;
        private Task<Process> _processTask = null;
        public void Parse(string[] args)
        {
            if (args.Length.Equals(1) && args[0].ToLower().Contains("set"))
                this.SetMethod(null);
            else
                this.HelpText();
        }

        public bool SetMethod(object argMessage)
        {
            Log.Verbose("UnInstall command issued");
            InstallUnInstallParams param = argMessage as InstallUnInstallParams;
            if (Directory.Exists(base.AppSettings.ProdDriverPath))
            {
                string[] driverBaselineFiles = Directory.GetFiles(base.AppSettings.ProdDriverPath);
                if (Path.GetFileNameWithoutExtension(driverBaselineFiles.First()).StartsWith("1"))
                    File.Delete(driverBaselineFiles.First());
            }
            if (param.AdapterType == DriverAdapterType.ATI)
            {
                return UnInstallSwitchableGraphicsDriver(param);
            }
            else
            {
                return DriverUnInstallHandle(oemFilePath + base.MachineInfo.Driver.OEMFile, param.OverrideMethodIndex, base.CurrentMethodIndex);
            }
        }
        private bool DriverUnInstallHandle(string infPath, int argOverrideIndex, int argCurrentMethodIndex)
        {
            Log.Message("UnInstalling Driver through inf file");
            if (!(File.Exists(infPath)))
            {
                Log.Message("inf does not exist at {0}", infPath);
                string[] oemFiles = Directory.GetFiles(Directory.GetCurrentDirectory()).ToArray().Select(f => Path.GetFileName(f)).ToArray();
                string[] driverOemFile = oemFiles.Where(dI => dI.StartsWith(base.MachineInfo.Driver.OEMFile.ToString().Split('.').First())).ToArray();
                if (driverOemFile.Length != 0)
                {
                    foreach (string oemFile in driverOemFile)
                    {
                        if (File.Exists(string.Concat(Directory.GetCurrentDirectory(), "\\", oemFile)))
                            File.Move(string.Concat(Directory.GetCurrentDirectory(), "\\", oemFile), string.Concat(oemFilePath, "\\", oemFile));
                    }
                }
            }
            Process DPInstProcess = CommonExtensions.StartProcess("dpinst.exe", " /u \"" + infPath + "\" /d /q", 0);
            DPInstProcess.WaitForExit();
            int exitCode = DPInstProcess.ExitCode;
            int rebootCode = exitCode >> 24;
            if (rebootCode == 64)
                needReboot = true;
            int numDriverPackageSuccessCode = exitCode & 255;
            if (numDriverPackageSuccessCode == 0)
                success = true;
            Thread.Sleep(10000);
            AutomationElement restartElement = UIABaseHandler.SelectElementNameControlType("Restart Later", ControlType.Button);
            if (restartElement != null)
                needReboot = true;
            if (success)
            {
                Log.Verbose("Driver UnInstalled..");
                DriverFunction driverFunc = base.CreateInstance<DriverFunction>(new DriverFunction());
                MachineInfo machineInfo = new MachineInfo();
                base.AppManager.MachineInfo.Driver = driverFunc.Get as DriverInfo;
                DriverInfo info = driverFunc.Get as DriverInfo;
                Log.Verbose("Driver Information: drivername {0} and version {1}", info.Name, info.Version);
             //   UIABaseHandler.Invoke(UIABaseHandler.SelectElementNameControlType("Restart Later", ControlType.Button));
                if (needReboot)
                {
                    Log.Verbose("Reboot required to disable driver functionality");
                    Log.Success("Successfully UnInstall driver package.");
                    PowerEvent powerEvent = new PowerEvent() { CurrentMethodIndex = argCurrentMethodIndex };
                    powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 10, rebootReason = RebootReason.DriverModify });
                }
                Thread.Sleep(30000);
                return true;
            }
            else
                Log.Verbose("Driver UnInstallation failed with error code {0}", exitCode);
            return false;
        }
        private bool UnInstallSwitchableGraphicsDriver(InstallUnInstallParams argSgInstallParams)
        {
            string driverPath = argSgInstallParams.ProdPath;
            if (string.IsNullOrEmpty(driverPath))
                driverPath = this.GetDriverPath;
            if (driverPath.EndsWith(@"\"))
                driverPath = driverPath.Remove(driverPath.Length - 1);
            if (!Directory.Exists(driverPath) || Directory.GetFiles(driverPath, "Setup.exe").Count().Equals(0))
                Log.Abort("Setup file(s) in {0} path not found!", driverPath);
            this._processTask = Task.Factory.StartNew<Process>(() => CommonExtensions.StartProcess(string.Format(@"{0}\Setup.exe", driverPath), " -uninstall"));
            return this.UnInstallSGProcessHandler();
        }
        private bool UnInstallSGProcessHandler()
        {
            Log.Verbose("Initiating UnInstall SG Assertion Task");
            Task<bool> uninstallProcess = Task.Factory.StartNew<bool>(() => this.HasATISetupProcess());
            uninstallProcess.Wait();
            this._processTask.Wait();
            Log.Verbose("UnInstall process assertion completed with status {0}.UnInstall command result::{1}", _processTask.Status.ToString(), this._processTask.Result.HasExited.ToString());
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
        private string GetDriverPath
        {
            get { return base.AppSettings.SwitchableGraphicsDriverPath; }
        }
        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(@"..\>Execute UnInstallDriver set").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
    }
}