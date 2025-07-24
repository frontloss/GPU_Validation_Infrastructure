namespace AudioEndpointVerification
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;
    using System.Linq;
    using System.Management;
    using System.Text;
    using System.Threading.Tasks;
    using System.Windows.Forms;
    using System.Xml;
    using System.Xml.Linq;


    public static class CommonExtension
    {
        public static string PlatformID { get; set; }

        public static DriverInfo driverInfo { get; set; }

        public static void Init()
        {
            DriverInfo driverObj = new DriverInfo();
            driverObj.AudioDriver = new AudioDriverInfo();
            driverObj.GfxDriver = new GfxDriverInfo();
            driverInfo = driverObj;
        }
        public static void CopyAssembly()
        {
            if (IntPtr.Size.Equals(8))
            {
                //Console.WriteLine("Copying 64 bit assemblies to root");
                StartProcess("xcopy", ".\\x64 . /R /Y");
            }
            else
            {
                //Console.WriteLine("Copying 32 bit assemblies to root");
                StartProcess("xcopy", ".\\x86 . /R /Y");
            }
        }

        public static Process StartProcess(string argFileName)
        {
            return StartProcess(argFileName, string.Empty);
        }
        public static Process StartProcess(string argFileName, string arguments)
        {
            return StartProcess(argFileName, arguments, 90);
        }
        public static Process StartProcess(string argFileName, string arguments, int argDelay)
        {
            return StartProcess(argFileName, arguments, argDelay, string.Empty);
        }
        public static Process StartProcess(string argFileName, string arguments, int argDelay, string argWorkingDir)
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.RedirectStandardOutput = true;
            processStartInfo.RedirectStandardInput = true;
            processStartInfo.UseShellExecute = false;
            processStartInfo.CreateNoWindow = true;
            processStartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processStartInfo.WorkingDirectory = argWorkingDir;
            processStartInfo.FileName = argFileName;
            if (!string.IsNullOrEmpty(arguments))
                processStartInfo.Arguments = arguments;
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();
            if (!argDelay.Equals(0))
                process.WaitForExit(argDelay * 1000);
            return process;
        }
        public static void RegisterDll(string argDLLName)
        {
            if (!argDLLName.Contains(".dll"))
                argDLLName += ".dll";

            string dllFilePath = string.Concat(@"""", Directory.GetCurrentDirectory(), "\\", argDLLName, @"""");
            StartProcess("regsvr32", string.Concat(@"/s ", dllFilePath), 1);
        }

        public static List<AudioDispInfo> GetAudioDisplayInfo()
        {
            DisplayEnumeration enumerate = new DisplayEnumeration();
            List<AudioDispInfo> audioDataList = new List<AudioDispInfo>();
            List<EnumeratedDisplayDetails> displayEnumirationList = new List<EnumeratedDisplayDetails>();
            List<DisplayInfo> enumList = enumerate.GetAll;
            foreach (DisplayInfo display in enumList)
            {
                AudioDispInfo temp = new AudioDispInfo();
                temp.AudioCapable = display.isAudioCapable.Equals(true) ? "Yes" : "No";
                temp.CompleteDisplayName = display.CompleteDisplayName;
                temp.DisplayType = display.DisplayType;
                temp.Port = display.Port;
                audioDataList.Add(temp);
            }
            if (enumList != null)
            {
                audioDataList.Remove(audioDataList.Where(DT => DT.DisplayType == DisplayType.EDP).First());
            }
            return audioDataList;
        }


        public static string GetplatformID()
        {
            string platformDeviceID = string.Empty;
            ManagementScope scope = new ManagementScope("\\\\.\\ROOT\\CIMV2");
            ObjectQuery query = new ObjectQuery("SELECT * FROM Win32_VideoController");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);
            ManagementObjectCollection queryCollection = searcher.Get();
            foreach (ManagementObject m in queryCollection)
            {
                string deviceID = m["PNPDeviceID"].ToString().Substring(m["PNPDeviceID"].ToString().IndexOf('&') + 1);
                string providerName = m["Name"].ToString();
                if (providerName.ToLower().Contains("intel"))
                {
                    platformDeviceID = deviceID.Substring(deviceID.IndexOf('_') + 1, 4);
                }
            }
            XDocument xDoc = XDocument.Load(@"Mapper\PlatformDeviceIDs.map");
            if (!string.IsNullOrEmpty(platformDeviceID))
            {
                PlatformID = (from c in xDoc.Elements("Platforms").Descendants("Platform").Descendants("DeviceID")
                              where c.Value.Contains(platformDeviceID)
                              select (string)c.Parent.FirstAttribute.Value).FirstOrDefault();
            }
            if (string.IsNullOrEmpty(PlatformID))
            {
                MessageBox.Show("Platform device {0} id not found in mapper file !!", platformDeviceID);
                System.Windows.Forms.Application.Exit();
            }
            return PlatformID;
        }

        public static string GetBIOSVersion()
        {
            return GetWin32Value("SMBIOSBIOSVersion", "SELECT * FROM Win32_BIOS");
        }

        private static string GetWin32Value(string argColumn, string argQuery)
        {
            ObjectQuery mgmtQuery = new ObjectQuery(argQuery);
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(mgmtQuery);
            ManagementObjectCollection queryCollection = searcher.Get();
            Object value = new Object();
            foreach (ManagementObject obj in queryCollection)
                value = obj[argColumn];
            searcher.Dispose();
            queryCollection.Dispose();
            return (null == value) ? string.Empty : value.ToString();
        }
        public static void GetGFXDriverVersion()
        {
            ManagementScope scope = new ManagementScope("\\\\.\\ROOT\\CIMV2");
            ObjectQuery query = new ObjectQuery("SELECT * FROM Win32_VideoController");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);
            ManagementObjectCollection queryCollection = searcher.Get();
            foreach (ManagementObject m in queryCollection)
            {
                CommonExtension.driverInfo.GfxDriver.Version = m["DriverVersion"].ToString();
                CommonExtension.driverInfo.GfxDriver.Status = GetStatus(Convert.ToUInt16(m["ConfigManagerErrorCode"]));
            }
        }

        public static bool DriverStatus(bool enableLogging = false)
        {
            bool status = true;
            GetGFXDriverVersion();

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
                    CommonExtension.driverInfo.AudioDriver.Status = m["Status"].ToString();
                    CommonExtension.driverInfo.AudioDriver.Version = GetAudioDriverVersion();
                    break;
                }
            }
            if (enableLogging)
            {
                if (CommonExtension.driverInfo.GfxDriver.Status.ToLower() != DriverState.Running.ToString().ToLower())
                {
                    CommonExtension.ErrorMessage("Gfx Driver is not Enable!", ErrorCode.Error);
                    status = status & false;
                }
                if (CommonExtension.driverInfo.AudioDriver.Status.ToLower().Trim() != "ok")
                {
                    CommonExtension.ErrorMessage("Audio Driver is not Enable!", ErrorCode.Error);
                    status = status & false;
                }
            }
            return status;
        }

        public static void ErrorMessage(string text, ErrorCode code, bool ExitApplication = false)
        {
            MessageBox.Show(text, code.ToString());
            if (ExitApplication)
                Environment.Exit(0);
        }

        private static string GetStatus(UInt16 returnCode)
        {
            if (returnCode == (UInt16)ConfigManagerErrorCode.Running)
                return ConfigManagerErrorCode.Running.ToString();
            else if (returnCode == (UInt16)ConfigManagerErrorCode.Disabled)
                return ConfigManagerErrorCode.Disabled.ToString();
            else if (returnCode == (UInt16)ConfigManagerErrorCode.Restart_Required)
                return ConfigManagerErrorCode.Restart_Required.ToString();
            else
                return ConfigManagerErrorCode.Unknown.ToString();
        }

        public static string GetAudioDriverVersion()
        {
            bool enableBlock = false;
            string ver = string.Empty;
            Process audDriver_process = CommonExtension.StartProcess("devcon.exe", " drivernodes =media", 4);
            while (!audDriver_process.StandardOutput.EndOfStream)
            {
                string line = audDriver_process.StandardOutput.ReadLine().ToLower().Trim();
                if (line.ToLower().Contains("manufacturer name is intel"))
                    enableBlock = true;
                if (enableBlock && line.ToLower().Contains("driver version is"))
                {
                    string[] arr = line.ToLower().Split(' ');
                    ver = arr.Last();
                    break;
                }
            }
            return ver;
        }
        public static string GetSupportedAudioEndpoint()
        {
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\AudioEndpointData.map");
            XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/NumAudioEndPoint");
            foreach (XmlNode eventNode in eventBenchmarkRoot.ChildNodes)
            {
                if (GetplatformID().Contains(Convert.ToString(eventNode.Attributes["id"].Value)))
                {
                    return Convert.ToString(eventNode.Attributes["MaxSupportedEndpoints"].Value);
                }
            }
            return "0";
        }
    }
}
