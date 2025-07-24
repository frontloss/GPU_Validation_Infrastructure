namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Diagnostics;

    internal class DriverVerifier : FunctionalBase, ISetNoArgs, IGet, IParse
    {
        private string _driverFile = "igdkmd{0}.sys";

        public bool SetNoArgs()
        {
            this.IdentifyDriverFile();
            Log.Verbose("Enabling driver verifier for {0}", this._driverFile);
            if (CommonExtensions.StartProcess("verifier.exe", string.Format("/flags 11 /driver {0}", this._driverFile)).HasExited)
            {
                PowerEvent powerEvent = new PowerEvent() { CurrentMethodIndex = base.CurrentMethodIndex };
                return powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 5 });
            }
            return false;
        }
        public object Get
        {
            get
            {
                this.IdentifyDriverFile();
                string result = string.Empty;
                Process process = CommonExtensions.StartProcess("verifier.exe", "/querysettings");
                while (!process.StandardOutput.EndOfStream)
                {
                    result = process.StandardOutput.ReadLine();
                    if (result.ToLower().Contains(this._driverFile))
                    {
                        Log.Verbose("Driver verifier enabled for {0}.", result);
                        return true;
                    }
                }
                Log.Alert("Driver verifier not enabled for {0}.", this._driverFile);
                return false;
            }
        }
        [ParseAttribute(InterfaceName = InterfaceType.ISetNoArgs, Comment = "Driver Verifier")]
        [ParseAttribute(InterfaceName = InterfaceType.IGet, Comment = "Driver verifier")]
        public void Parse(string[] args)
        {
            if (!args.Length.Equals(0) && args[0].ToLower().Contains("get"))
            {
                var result = this.Get;
            }
            else if (!args.Length.Equals(0) && args[0].ToLower().Contains("set"))
                this.SetNoArgs();
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Execute DriverVerifier get|set").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
        private void IdentifyDriverFile()
        {
            this._driverFile = string.Format("igdkmd{0}.sys", base.MachineInfo.OS.Architecture.ToLower().Replace("bit", string.Empty).Replace("-", string.Empty).Trim());
        }
    }
}