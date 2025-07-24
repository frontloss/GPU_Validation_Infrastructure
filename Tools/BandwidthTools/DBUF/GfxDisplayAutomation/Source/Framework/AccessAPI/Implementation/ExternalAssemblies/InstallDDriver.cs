namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Threading.Tasks;
    using System.Windows.Automation;

    internal class InstallDDriver : FunctionalBase, ISet
    {
        private CancellationTokenSource _ctsUnsignedPopup = null;
        private Task<Process> _processTask = null;

        public object Set
        {
            set
            {
                string driverPath = value.ToString();
                Log.Verbose("Install DDriver command issued. Driver path is {0}", driverPath);
                this._processTask = Task.Factory.StartNew<Process>(() => CommonExtensions.StartProcess("devcon.exe", String.Concat("install ", driverPath, " Root\\DDriver")));
                this.InstallDDriverProcessHandler();
            }
        }

        private void InstallDDriverProcessHandler()
        {
            Thread.Sleep(3000);
            Log.Verbose("Initiating InstallDDriverProcessHandler");
            this._ctsUnsignedPopup = new CancellationTokenSource();
            Log.Verbose("Initiating UnsignedPopupWarningHandler Task");
            Task unsignedPopupProcess = Task.Factory.StartNew(() => this.UnsignedPopupWarningHandler(), this._ctsUnsignedPopup.Token);
            Log.Verbose("Initiating HasDevconProcess Assertion Task");
            Task<bool> setupProcess = Task.Factory.StartNew<bool>(() => this.HasDevconProcess());
            setupProcess.Wait();
            this._processTask.Wait();
            if (setupProcess.Result)
            {
                Log.Verbose("Setup assertion task completed with status:: {0}. Devcon Process task status:: {1}", setupProcess.IsCompleted, this._processTask.IsCompleted);
                this._ctsUnsignedPopup.Cancel();
                Log.Verbose("Task status for UnsignedPopupWarningHandler [{0}]", unsignedPopupProcess.IsCompleted);
            }
        }
        private bool HasDevconProcess()
        {
            bool exists = false;
            while (!exists)
            {
                try
                {
                    exists = (
                        !Process.GetProcesses()
                        .Where(p => p.ProcessName.ToLower().StartsWith("devcon") && !p.HasExited &&
                            p.MainModule.FileVersionInfo.FileDescription.Replace(" ", string.Empty).ToLower().Contains("windowssetupapi"))
                        .Count().Equals(0)
                        );
                }
                catch (Exception ex)
                {
                    Log.Sporadic(false, "UnsignedPopupWarningHandler: HasDevconProcess:: {0}", ex.Message);
                    Log.Verbose("{0}", ex.StackTrace);
                    Thread.Sleep(60000);
                }
            }
            //Log.Verbose("UnInstall Assertion Task complete");
            return exists;
        }
        private void UnsignedPopupWarningHandler()
        {
            while (true)
            {
                Condition mainWindowHandle = new PropertyCondition(AutomationElement.NameProperty, "Windows Security");
                AutomationElement mainWindowElement = AutomationElement.RootElement.FindFirst(TreeScope.Children, mainWindowHandle);
                if (null != mainWindowElement)
                {
                    //Log.Verbose("UnsignedPopupWarningHandler:: Found Windows Security popup");
                    Condition installBtnHandle = new PropertyCondition(AutomationElement.NameProperty, "install this driver software anyway", PropertyConditionFlags.IgnoreCase);
                    AutomationElement installBtnElement = mainWindowElement.FindFirst(TreeScope.Descendants, installBtnHandle);
                    if (null != installBtnElement && installBtnElement.Current.ControlType.Equals(ControlType.Button))
                    {
                        //Log.Verbose("UnsignedPopupWarningHandler:: Found Install button");
                        InvokePattern pattern = installBtnElement.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                        //Log.Verbose("UnsignedPopupWarningHandler:: Clicking Install");
                        pattern.Invoke();
                    }
                }
                if (this._ctsUnsignedPopup.IsCancellationRequested)
                {
                    //Log.Verbose("Cancelling UnsignedPopupWarningHandler Task");
                    break;
                }
            }
            //Log.Verbose("UnsignedPopupWarningHandler Task complete");
        }
    }
}