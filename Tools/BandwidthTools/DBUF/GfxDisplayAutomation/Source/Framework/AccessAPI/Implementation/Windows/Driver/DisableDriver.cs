namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Threading;
    using System.Diagnostics;
    using System.Collections.Generic;

    internal class DisableDriver : FunctionalBase, IParse, ISetMethod
    {
        private string _command = string.Empty;
        private bool intelDriver;
        private int _delay = 5000;
        private bool LANSDisabledStatus = false;

        public DisableDriver()
            : base()
        {
            this._command = "disable =";
        }
        public DisableDriver(string argCommand, int argDelay)
        {
            this._command = argCommand;
            this._delay = argDelay;
        }
        public bool SetMethod(object argMessage)
        {
            EnableDisableLAN();
            DriverAdapterType adapterType = (DriverAdapterType)argMessage;
            if (adapterType == DriverAdapterType.Intel)
            {
                this._command = String.Concat(_command, "display PCI\\VEN_8086*");
                intelDriver = true;
            }
            else if (adapterType == DriverAdapterType.Audio)
                this._command = String.Concat(_command, "media");
            else
                this._command = String.Concat(_command, "display PCI\\VEN_1002*");
            Process process = CommonExtensions.StartProcess("devcon.exe", this._command);
            Thread.Sleep(this._delay);
            if (process.HasExited)
            {
                while (!process.StandardOutput.EndOfStream)
                {
                    string result = process.StandardOutput.ReadLine();
                    if (result.ToLower().Contains(string.Format("{0}d", this.Status)))
                    {
                        if(_command.ToLower().Contains("enable") && intelDriver)
                        {
                            EnableULT();
                            DisplayEnumeration enumDisplay = base.CreateInstance<DisplayEnumeration>(new DisplayEnumeration());
                            List<DisplayInfo> enumeratedDisplay = enumDisplay.GetAll as List<DisplayInfo>;
                        }
                        Log.Verbose("Driver Successfully {0}d...", this.Status);
                        if (!(this._command.Contains("1002")))
                            UpdateBase();
                        return true;
                    }
                }
            }
            Log.Alert("Driver Not Successfully {0}d!!! Time taken for process to exit {1} minute(s)", this.Status, Math.Round(DateTime.Now.Subtract(process.StartTime).TotalMinutes));
            process.Close();
            EnableDisableLAN();
            return true;
        }
        [ParseAttribute(InterfaceName = InterfaceType.ISetNoArgs, Comment = "Disables/Enables the driver")]
        public void Parse(string[] args)
        {
            if (!args.Length.Equals(0) && args[0].ToLower().Contains("set"))
                this.SetMethod(DriverAdapterType.Intel);
            else
                this.HelpText();
        }

        private void UpdateBase()
        {
            DriverFunction driverFunc = base.CreateInstance<DriverFunction>(new DriverFunction());
            MachineInfo machineInfo = new MachineInfo();
            base.AppManager.MachineInfo.Driver = driverFunc.Get as DriverInfo;
        }

        private void EnableULT()
        {

            if (base.AppManager.ApplicationSettings.UseDivaFramework || base.AppManager.ApplicationSettings.UseULTFramework || base.AppManager.ApplicationSettings.UseSHEFramework)   //SHE
            {
                Log.Message("Enabling ULT again");
                SimulatedHotPlugDisplay simDisplay = base.CreateInstance<SimulatedHotPlugDisplay>(new SimulatedHotPlugDisplay());
                HotPlugUnplug argSimulationFramework = new HotPlugUnplug(FunctionName.SimulationFramework, true);
                simDisplay.SetMethod(argSimulationFramework);

                HotPlugUnplug argSimulationFeature = new HotPlugUnplug(FunctionName.SimulationFeature, true);
                simDisplay.SetMethod(argSimulationFeature);
            }
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(string.Format("..\\>Execute {0}Driver set", this.Status)).Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
        private string Status
        {
            get { return this._command.Split(' ')[0]; }
        }

        /* This is applicable for CS test, which Disable LAN before test start
           while we are disabling GFX driver it may cause BSOD, and if we dont
           enable LAN again all consicutive test will not execute */
        private void EnableDisableLAN()
        {
            NetParam netParam;
            netParam = new NetParam();
            netParam.adapter = Adapter.LAN;

            if (NetworkExtensions.GetLANUPStatus() == false)
            {
                netParam.netWorkState = NetworkState.Enable;
                LANSDisabledStatus = true;
                Log.Message("Enabling LAN connection again...");
                NetworkExtensions.SetNetworkConnection(netParam);
            }
            else if(LANSDisabledStatus)
            {
                LANSDisabledStatus = false;
                netParam.netWorkState = NetworkState.Disable;
                Log.Message("Disabling LAN connection again...");
                NetworkExtensions.SetNetworkConnection(netParam);
            }
        }
    }
}