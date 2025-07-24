namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Xml;
    using System.Management;
    using System.Collections.Generic;

    public class WinSystemInformation : FunctionalBase, IGet
    {
        private Dictionary<WinApiQuery, string> _winApiQueryMappings = new Dictionary<WinApiQuery, string>();

        internal enum WinApiQuery
        {
            OperatingSystem,
            BIOSVersion,
            PhysicalMemory
        }

        public WinSystemInformation()
            : base()
        {
            this._winApiQueryMappings.Add(WinApiQuery.OperatingSystem, "SELECT * FROM Win32_OperatingSystem");
            this._winApiQueryMappings.Add(WinApiQuery.BIOSVersion, "SELECT * FROM Win32_BIOS");
            this._winApiQueryMappings.Add(WinApiQuery.PhysicalMemory, "SELECT * FROM Win32_ComputerSystem");

        }
        public object Get
        {
            get
            {
                MachineInfo machineInfo = new MachineInfo();
                machineInfo.PhysicalMemory = Math.Round(Convert.ToDouble(this.GetWin32Value("TotalPhysicalMemory", this._winApiQueryMappings[WinApiQuery.PhysicalMemory])) / (1024 * 1024 * 1024), 2).ToString() + "GB";
                machineInfo.Name = Environment.MachineName;
                machineInfo.BIOSVersion = this.GetWin32Value("SMBIOSBIOSVersion", this._winApiQueryMappings[WinApiQuery.BIOSVersion]);

                machineInfo.OS = new OSInfo();
                machineInfo.OS.Architecture = this.GetWin32Value("OSArchitecture", this._winApiQueryMappings[WinApiQuery.OperatingSystem]);
                machineInfo.OS.Build = this.GetWin32Value("Version", this._winApiQueryMappings[WinApiQuery.OperatingSystem]);
                string servicePack = string.Concat(" ", this.GetWin32Value("CSDVersion", this._winApiQueryMappings[WinApiQuery.OperatingSystem]));
                machineInfo.OS.Description = string.Concat(this.GetWin32Value("Caption", this._winApiQueryMappings[WinApiQuery.OperatingSystem]), servicePack.TrimEnd());

                DriverFunction driverFunction = base.CreateInstance<DriverFunction>(new DriverFunction());
                machineInfo.Driver = driverFunction.Get as DriverInfo;
                
                Log.Message("The device id is {0}", machineInfo.Driver.DeviceID);

                if (!string.IsNullOrEmpty(machineInfo.Driver.DeviceID))
                {
                    XmlDocument xDoc = new XmlDocument();
                    xDoc.Load(@"Mapper\PlatformDeviceIDs.map");
                    XmlNodeList platformNode = xDoc.SelectNodes("/Platforms/Platform");
                    string formFactor = string.Empty;
                    foreach (XmlNode node in platformNode)
                    {
                        foreach (XmlNode childNode in node.ChildNodes)
                        {
                            if (childNode.Attributes["ID"].Value.Trim() == machineInfo.Driver.DeviceID)
                            {
                                machineInfo.PlatformDetails = new PlatformDetails();
                                machineInfo.PlatformDetails.Platform = (Platform)Enum.Parse(typeof(Platform), (node.Attributes["ID"].Value.Trim().ToString()), true);
                                formFactor = childNode.Attributes["formfactor"] == null ? string.Empty : childNode.Attributes["formfactor"].Value.Trim();
                                if (Enum.IsDefined(typeof(FormFactor), formFactor))
                                    machineInfo.PlatformDetails.FormFactor = (FormFactor)Enum.Parse(typeof(FormFactor), formFactor, true);
                                else
                                    machineInfo.PlatformDetails.FormFactor = FormFactor.Unknown;
                                break;
                            }
                        }
                    }
                }
                if (!CommonExtensions.HasRebootFile())
                {
                    Log.Verbose("************ TEST MACHINE INFORMATION ************");
                    Log.Verbose("MachineName:: {0}", machineInfo.Name);
                    Log.Verbose("BIOSVersion:: {0}", machineInfo.BIOSVersion);
                    if (string.IsNullOrEmpty(machineInfo.PlatformDetails.Platform.ToString()))
                        Log.Abort("Platform information not found! Check Mapper\\PlatformDeviceIDs.map for entry.");
                    Log.Verbose("Platform:: {0} is Low Power:: {1}", machineInfo.PlatformDetails.Platform, machineInfo.PlatformDetails.IsLowpower);
                    Log.Verbose("Platform formfactor:: {0}", machineInfo.PlatformDetails.FormFactor.ToString());
                    Log.Verbose("OS.Architecture:: {0}", machineInfo.OS.Architecture);
                    Log.Verbose("OS.Build:: {0}", machineInfo.OS.Build);
                    Log.Verbose("OS.Description:: {0}", machineInfo.OS.Description);
                    Log.Verbose("OS.Type:: {0}", machineInfo.OS.Type);
                }
                machineInfo.Driver.PrintAllDetails();
                return machineInfo;
            }
        }

        private string GetWin32Value(string argColumn, string argQuery)
        {
            string outputString = string.Empty;
            ObjectQuery mgmtQuery = new ObjectQuery(argQuery);
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(mgmtQuery);
            ManagementObjectCollection queryCollection = searcher.Get();
            if (queryCollection.Count != 0)//workaround kept after discussing with vijayan regarding BIOS version not populated for CHV.
            {
                Object value = new Object();
                foreach (ManagementObject obj in queryCollection)
                    value = obj[argColumn];
                searcher.Dispose();
                queryCollection.Dispose();
                outputString = (null == value) ? string.Empty : value.ToString();
            }
            else
                Log.Alert("queryCollection for query {0} is zero", argColumn);

            return outputString;
        }
    }
}