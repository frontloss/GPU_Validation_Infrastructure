namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using System.Management;
    using System.Runtime.InteropServices;

    class DriverFunction : FunctionalBase, IGetMethod, IParse, IGet
    {
        private string _command = string.Empty;
        private string _vendorId = string.Empty;
        public DriverFunction()
            : base()
        {
            this._command = "status =display PCI\\VEN_8086*";
            this._vendorId = "8086";
        }
        public object GetMethod(object argMessage)
        {
            DriverAdapterType argAdapterType = (DriverAdapterType)argMessage;
            if (argAdapterType == DriverAdapterType.ATI)
            {
                this._command = "status =display PCI\\VEN_1002*";
                this._vendorId = "1002";
            }
            string result = string.Empty;
            DriverInfo driverInfo = this.Get as DriverInfo;
            return driverInfo;
        }
        public object Get
        {
            get
            {
                string result = string.Empty;
                List<DriverInfo> listDriverInfo = new List<DriverInfo>();
                this.LoadDriverInfo(listDriverInfo);
                return listDriverInfo.Find(driver => driver.VendorID == this._vendorId);
            }
        }
        [ParseAttribute(InterfaceName = InterfaceType.ISetNoArgs, Comment = "Gets the driver information")]
        public void Parse(string[] args)
        {
            if (args.Length.Equals(1) && args[0].ToLower().Contains("get"))
            {
                DriverInfo driverInfo = this.Get as DriverInfo;
                driverInfo.PrintBasicDetails();
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Execute DriverFunction get").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
        private void LoadDriverInfo(List<DriverInfo> argDriverInfo)
        {
            ManagementScope scope = new ManagementScope("\\\\.\\ROOT\\CIMV2");
            ObjectQuery query = new ObjectQuery("SELECT * FROM Win32_VideoController");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);
            ManagementObjectCollection queryCollection = searcher.Get();
            foreach (ManagementObject m in queryCollection)
            {
                DriverInfo driverInfo = new DriverInfo();
                driverInfo.VendorID = m["PNPDeviceID"].ToString().Substring(m["PNPDeviceID"].ToString().IndexOf('_') + 1, 4);
                string deviceID = m["PNPDeviceID"].ToString().Substring(m["PNPDeviceID"].ToString().IndexOf('&') + 1);
                driverInfo.DeviceID = deviceID.Substring(deviceID.IndexOf('_') + 1, 4);
                driverInfo.Name = m["Description"].ToString();
                driverInfo.OEMFile = m["InfFilename"].ToString();
                driverInfo.Version = m["DriverVersion"].ToString();
                driverInfo.DriverDescription = m["Description"].ToString();
                driverInfo.Status = GetStatus(Convert.ToUInt16(m["ConfigManagerErrorCode"]));
                driverInfo.DriverBaseLine = GetDriverBaseLine(base.AppManager.ApplicationSettings.ProdDriverPath);
                if (GetDeviceDriverKey() != string.Empty)
                    driverInfo.GfxDriverRegistryPath = @"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\" + GetDeviceDriverKey();
                if (driverInfo.Status == DriverState.UnKnown.ToString())
                    DevconHelper(driverInfo);
                LoadAudioDriverInfo(driverInfo);
                argDriverInfo.Add(driverInfo);
            }
        }
        private void LoadAudioDriverInfo(DriverInfo argDriverInfo)
        {
            bool enableBlock = false;
            ManagementScope scope = new ManagementScope("\\\\.\\ROOT\\CIMV2");
            ObjectQuery query = new ObjectQuery("SELECT * FROM Win32_SoundDevice");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);
            ManagementObjectCollection queryCollection = searcher.Get();
            foreach (ManagementObject m in queryCollection)
            {
                if (m["Name"].ToString().Trim().ToLower().Contains("intel"))
                    enableBlock = true;
                if (enableBlock)
                {
                    argDriverInfo.AudioDriverName = m["Name"].ToString();
                    argDriverInfo.AudioDriverStatus = m["Status"].ToString();
                }
            }
        }
        private string GetStatus(UInt16 returnCode)
        {
            string status = DriverState.UnKnown.ToString();
            if (returnCode == (UInt16)ConfigManagerErrorCode.Running)
                return ConfigManagerErrorCode.Running.ToString();
            else if (returnCode == (UInt16)ConfigManagerErrorCode.Disabled)
                return ConfigManagerErrorCode.Disabled.ToString();
            else if (returnCode == (UInt16)ConfigManagerErrorCode.Restart_Required)
                return ConfigManagerErrorCode.Restart_Required.ToString();
            else
                Log.Alert("Config manager error code value {0}", returnCode);
            return status;
        }

        private void DevconHelper(DriverInfo argDriverInfo)
        {
            string result = DriverState.UnKnown.ToString();
            argDriverInfo.Status = result;
            Process statusProcess = CommonExtensions.StartProcess("devcon.exe", this._command);
            Regex driverStatusKey = new Regex("Driver is");
            List<string> driverStates = new List<string>() { "disabled", "running", "stopped" };
            while (!statusProcess.StandardOutput.EndOfStream)
            {
                result = statusProcess.StandardOutput.ReadLine();
                if (driverStates.Any(st => result.ToLower().Contains(st)))
                    argDriverInfo.Status = result.Split(' ').Last().Replace(".", string.Empty);
            }
        }

        public string GetDriverBaseLine(string driverPath)
        {
            string driverBaseline = string.Empty;
            RegistryInf registryInf = base.CreateInstance<RegistryInf>(new RegistryInf());

            RegistryParams registryParams = new RegistryParams();
            registryParams.infChanges = InfChanges.ReadInf;
            registryParams.registryKey = Microsoft.Win32.Registry.LocalMachine;
            registryParams.path = @"SYSTEM\CurrentControlSet\Control\Class\" + GetDeviceDriverKey();
            
            registryParams.keyName = "PC_Release_Major";
            int major = (int)registryInf.GetMethod(registryParams);

            registryParams.keyName = "PC_Release_Minor";
            int minor = (int)registryInf.GetMethod(registryParams);
            if (major != -1 && minor != -1)
                driverBaseline = major.ToString() + "." + minor.ToString();

            return driverBaseline;
        }
        private string GetDeviceDriverKey()
        {
            string driverKey = string.Empty;
            const int SPDRP_DRIVER = 0x00000009;  // Driver (R/W)
            const int DIGCF_PRESENT = 0x00000002;

            Guid GUID_DEVINTERFACE_DISPLAY = new Guid(0x4D36E968, 0xE325, 0x11CE, 0xBF, 0xC1, 0x08, 0x00, 0x2B, 0xE1, 0x03, 0x18);
            DisplayInfoData displayInfoData = new DisplayInfoData();
            displayInfoData.Size = Marshal.SizeOf(displayInfoData);
            uint MemberIndex = 0;
            int lastError = 0;

            uint PropertyDataType = 0;
            StringBuilder PropertyBuffer = new StringBuilder(256);
            uint RequiredSize = 0;
            IntPtr DeviceInfoSet = new IntPtr();

            DeviceInfoSet = Interop.SetupDiGetClassDevs(ref GUID_DEVINTERFACE_DISPLAY, null, IntPtr.Zero, DIGCF_PRESENT);
            lastError = Marshal.GetLastWin32Error();

            for (; Interop.SetupDiEnumDeviceInfo(DeviceInfoSet, MemberIndex++, ref displayInfoData); )
            {
                Interop.SetupDiGetDeviceRegistryProperty(DeviceInfoSet, ref displayInfoData, SPDRP_DRIVER, ref PropertyDataType, PropertyBuffer, 1000, ref RequiredSize);
                lastError = Marshal.GetLastWin32Error();

                if (lastError == 0 && ValidateDeviceDriverKey(PropertyBuffer.ToString()))
                {
                    driverKey = PropertyBuffer.ToString();
                }
            }

            return driverKey;
        }

        private bool ValidateDeviceDriverKey(string key)
        {
            RegistryInf registryInf = base.CreateInstance<RegistryInf>(new RegistryInf());

            RegistryParams registryParams = new RegistryParams();
            registryParams.infChanges = InfChanges.ReadInf;
            registryParams.registryKey = Microsoft.Win32.Registry.LocalMachine;
            registryParams.path = @"SYSTEM\CurrentControlSet\Control\Class\" + key;

            registryParams.keyName = "PC_Release_Major";
            try
            {
                registryInf.GetMethod(registryParams);
                return true;
            }
            catch { return false; }
        }
    }
}