namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Threading;
    using System.Reflection;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Security;
    using System.Xml.Serialization;
    using System.Xml;
    using System.Text;

    public static class CommonExtensions
    {
        private static XDocument _featuresMap = null;
        private static XDocument _featuresMapAccessAPI = null;
        public static XDocument _navigationsMap = null;
        private static List<string> _intelDriverStringList = null;
        private static List<string> _standardDriverStringList = null;
        private static Dictionary<DumpCategory, string> _dumpPaths = null;
        private static IApplicationSettings _appSettings = null;
        public static string[] _cmdLineArgs = null;
        private static string _currentInstanceRef = DateTime.Now.ToString("yyyyMMddHHmmss");
        private static List<string> _recordLogMsgs = null;
        public static string _mpBSODAnalysisPath = null;
        public static RebootAnalysysInfo _rebootAnalysysInfo = null;
        public static RebootDataProvider _rebootReason = null;

        private static string _rebootAnalysysInfoBackupPath = null;
        private static string _mpBSODAnalysisBackupPath = null;

        public static bool _cloneDriverCopyStatus;

        public static void Init(IApplicationSettings argAppSettings, string[] args)
        {
            _appSettings = argAppSettings;
            _cmdLineArgs = args;
            _rebootAnalysysInfo = new RebootAnalysysInfo();
            _rebootReason = new RebootDataProvider();
            _featuresMapAccessAPI = XDocument.Load("Mapper\\AccessAPIFeaturesConfiguration.map");
            _featuresMap = argAppSettings.UIAutomationPath.Equals("WindowsAutomationUI") ? XDocument.Load("Mapper\\WindowsUIFeaturesConfiguration.map") : XDocument.Load("Mapper\\FeaturesConfiguration.map");
            _navigationsMap = argAppSettings.UIAutomationPath.Equals("WindowsAutomationUI") ? XDocument.Load("Mapper\\WindowsUINavigationConfiguration.map") : XDocument.Load("Mapper\\NavigationsConfiguration.map");
            _rebootAnalysysInfo.path = string.Format(@"RebootAnalysysInfo.xml");
            _rebootAnalysysInfoBackupPath = string.Format(@"RebootAnalysysInfo_backup.xml");
            _mpBSODAnalysisPath = string.Format(@"MPBSODAnalysisFlag.xml");
            _mpBSODAnalysisBackupPath = string.Format(@"MPBSODAnalysisFlag_backup.xml");

            _cloneDriverCopyStatus = false;

            if (File.Exists(_rebootAnalysysInfo.path))
                _rebootAnalysysInfo = DoDeSerialize();
            else
            {
                _rebootAnalysysInfo.identifier = string.Join("_", args);
                _rebootAnalysysInfo.currentMethodIdx = -100;
                _rebootAnalysysInfo.jobID = CurrentInstanceRefStr;
            }
            Thread.Sleep(1000);
            if (File.Exists(CommonExtensions._mpBSODAnalysisPath))
                _rebootReason = RebootLogDeSerialize();
            _intelDriverStringList = new List<string>() { "intel" };
            _standardDriverStringList = new List<string>() { "basic", "vga" };
            _dumpPaths = new Dictionary<DumpCategory, string>()
            {
                { DumpCategory.WatchDogdump, @"C:\Windows\LiveKernelReports\WATCHDOG" },
                { DumpCategory.Minidump, @"C:\Windows\Minidump" },
                { DumpCategory.Memorydump, @"C:\Windows"}
            };

            TestPostProcessing.Init();
        }
        public static void Init(string args)
        {
            if (args.Equals("15.36"))
            {
                Log.Verbose("Loading mapper for {0} baseline driver", args);
                _featuresMap = XDocument.Load("Mapper\\WindowsUIFeaturesConfiguration.map");
                _navigationsMap = XDocument.Load("Mapper\\WindowsUINavigationConfiguration.map");
            }
            else if (args.Equals("15.33"))
            {
                Log.Verbose("Loading mapper for {0} baseline driver", args);
                _featuresMap = XDocument.Load("Mapper\\15.33\\WindowsUIFeaturesConfiguration.map");
                _navigationsMap = XDocument.Load("Mapper\\15.33\\WindowsUINavigationConfiguration.map");
            }
            else
            {
                Log.Verbose("Loading mapper for {0} baseline driver", args);
                _featuresMap = XDocument.Load("Mapper\\15.40\\WindowsUIFeaturesConfiguration.map");
                _navigationsMap = XDocument.Load("Mapper\\15.40\\WindowsUINavigationConfiguration.map");
            }
        }
        public static List<string> IntelDriverStringList
        {
            get { return _intelDriverStringList; }
        }
        public static List<string> StandardDriverStringList
        {
            get { return _standardDriverStringList; }
        }
        public static Dictionary<DumpCategory, string> DumpPaths
        {
            get { return _dumpPaths; }
        }
        private static string CurrentInstanceRefStr
        {
            get
            {
                if (!File.Exists(_rebootAnalysysInfo.path))
                {
                    return _currentInstanceRef;
                }
                return
                    _rebootAnalysysInfo.jobID;
            }
        }
        public static object Activate(this Features argFeature, Source argAlternativeSource)
        {
            return Activate(argFeature, argAlternativeSource, argFeature.ToString());
        }
        public static object Activate(this Features argFeature, Source argAlternativeSource, object argContext)
        {
            return Activate(argFeature, argAlternativeSource, argFeature.ToString(), argContext);
        }
        public static object Activate(this Features argFeature, Source argAlternativeSource, string argTypeName)
        {
            return Activate(argFeature, argAlternativeSource, argTypeName, null);
        }
        public static object Activate(this Features argFeature, Source argAlternativeSource, string argTypeName, params object[] args)
        {
            Assembly assembly = null;
            Source source = argAlternativeSource;
            if (source == Source.Default)
                Enum.TryParse<Source>(argFeature.GetElementValue("source", source), out source);

            if (source == Source.WindowsAutomationUI)
                UIExtensions.setUIAEntity(argFeature);

            if (source == Source.CrcGenerator)
                assembly = assembly.Locate(string.Concat("Intel.Display.Automation.", source.ToString()));
            else
                assembly = assembly.Locate(string.Concat("Intel.VPG.Display.Automation.", source.ToString()));

            Type type = null;
            type = type.Locate(assembly, argTypeName);
            return Activator.CreateInstance(type, args);
        }
        public static Assembly Locate(this Assembly argContext, string argSource)
        {
            Features feature;
            if (Enum.TryParse<Features>(argSource, true, out feature))
                return null;
            if (!File.Exists(string.Concat(Directory.GetCurrentDirectory(), "\\", argSource, ".dll")))
                Log.Abort("Could not locate Assembly:: {0}!", argSource);
            argContext = Assembly.Load(argSource.ToString());
            if (null == argContext)
                Log.Abort("Could not locate Assembly:: {0}!", argSource);
            return argContext;
        }
        public static Type Locate(this Type argContext, Assembly argAssembly, string argInstance)
        {
            argContext = GetTypeInstance(argAssembly, argInstance);
            if (null == argContext)
                Log.Abort("Could not locate Type:: {0}!", argInstance);
            return argContext;
        }
        public static string GetElementValue(this Features argContext, string argMemberName, Source argSource)
        {
            if (argSource == Source.AccessAPI)
                return (from c in _featuresMapAccessAPI.Elements("Features").Descendants("feature")
                        where (string)c.Attribute("name") == argContext.ToString()
                        select (string)c.Attribute(argMemberName)).FirstOrDefault();
            else if (argSource == Source.Default)
            {
                string actionClass = (from c in _featuresMapAccessAPI.Elements("Features").Descendants("feature")
                                      where (string)c.Attribute("name") == argContext.ToString()
                                      select (string)c.Attribute(argMemberName)).FirstOrDefault();
                if (actionClass == null)
                    actionClass = (from c in _featuresMap.Elements("Features").Descendants("feature")
                                   where (string)c.Attribute("name") == argContext.ToString()
                                   select (string)c.Attribute(argMemberName)).FirstOrDefault();
                return actionClass;

            }
            return (from c in _featuresMap.Elements("Features").Descendants("feature")
                    where (string)c.Attribute("name") == argContext.ToString()
                    select (string)c.Attribute(argMemberName)).FirstOrDefault();
        }
        public static Dictionary<string, string> GetNavigationList(this Features argContext)
        {
            List<XElement> landscapeElements = new List<XElement>();
            Dictionary<string, string> navigationList = new Dictionary<string, string>();
            bool landscape = Orientation.Landscape();
            landscapeElements = (from c in _navigationsMap.Root.Descendants("Landscape") select c).ToList();
            if (landscapeElements.Count == 0)
            {
                var hierachy = (from c in _navigationsMap.Root.Descendants("feature")
                                where (string)c.Attribute("name") == argContext.ToString()
                                select c.Ancestors()).FirstOrDefault();
                if (null != hierachy)
                {
                    hierachy = hierachy.Reverse().Skip(1);
                    hierachy.ToList().ForEach(e => navigationList.Add(e.Name.LocalName, e.FirstAttribute.Value));
                }
            }
            else
            {
                foreach (XElement landscapeElement in landscapeElements)
                {
                    XAttribute subFeature = landscapeElement.Attribute("value");
                    if (String.Equals(subFeature.Value.ToString().ToLower(), landscape.ToString().ToLower()))
                    {
                        var hierachy = (from c in landscapeElement.Descendants("feature")
                                        where (string)c.Attribute("name") == argContext.ToString()
                                        select c.Ancestors()).FirstOrDefault();
                        if (null != hierachy)
                        {
                            hierachy = hierachy.Reverse().Skip(1);
                            hierachy.ToList().ForEach(e => navigationList.Add(e.Name.LocalName, e.FirstAttribute.Value));
                        }
                    }
                    if (navigationList.ContainsKey("Landscape")) navigationList.Remove("Landscape");
                }
            }
            return navigationList;
        }
        public static bool IsHelpCall(this string[] args)
        {
            return (args.Length > 0 && (args[0].Contains("?") || args[0].ToLower().Contains("help")));
        }
        public static Process StartProcess(string argFileName)
        {
            return StartProcess(argFileName, string.Empty);
        }
        public static Process StartProcess(string argFileName, string argUserName, string argPassword)
        {
            return StartProcess(argFileName, string.Empty, 0, string.Empty, argUserName, argPassword);
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
            return StartProcess(argFileName, arguments, argDelay, argWorkingDir, string.Empty, string.Empty);
        }
        public static Process StartProcess(string argFileName, string arguments, int argDelay, string argWorkingDir, string argUserName, string argPassword)
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.RedirectStandardOutput = true;
            processStartInfo.RedirectStandardInput = true;
            processStartInfo.UseShellExecute = false;
            processStartInfo.CreateNoWindow = false;
            processStartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processStartInfo.WorkingDirectory = argWorkingDir;
            processStartInfo.FileName = argFileName;
            if (!string.IsNullOrEmpty(arguments))
                processStartInfo.Arguments = arguments;
            if (!string.IsNullOrEmpty(argUserName) && !string.IsNullOrEmpty(argPassword))
            {
                processStartInfo.UserName = EncryptDecrypt(argUserName);
                processStartInfo.Password = GetPassword(EncryptDecrypt(argPassword));
            }
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();
            if (!argDelay.Equals(0))
                process.WaitForExit(argDelay * 1000);
            return process;
        }

        public static int ReadRebootInfo()
        {
            int methodInvocationIdx = 0;
            if (HasRebootFile())
            {
                methodInvocationIdx = CommonExtensions._rebootAnalysysInfo.currentMethodIdx;
                if (methodInvocationIdx == -100)
                    methodInvocationIdx = 0;
                else
                    methodInvocationIdx++;
                Log.Verbose("Setting 'methodInvocationIdx' to {0}", methodInvocationIdx);
            }
            ClearRebootFile();
            return methodInvocationIdx;
        }
        public static void ClearRebootFile()
        {
            if (File.Exists(CommonExtensions._rebootAnalysysInfo.path))
            {
                Log.Verbose("Deleting {0}", CommonExtensions._rebootAnalysysInfo.path);
                File.Delete(CommonExtensions._rebootAnalysysInfo.path);
            }
        }

        public static string IdentifyDriverFile(string GFXDriverPath)
        {
            string path = string.Empty;
            if (Directory.Exists(GFXDriverPath))
            {
                path = Directory.GetFiles(GFXDriverPath, IntPtr.Size.Equals(8) ? "igdlh64.inf" : "igdlh.inf", SearchOption.AllDirectories).First();
            }
            if (string.IsNullOrEmpty(path))
            {
                Log.Abort("Unable to find inf file in {0}", _appSettings.ProdDriverPath);
            }
            return path;
        }

        public static void WriteRetryThruRebootInfo()
        {
            _rebootAnalysysInfo.retryThroughReboot = true;
        }
        public static bool HasRetryThruRebootFile()
        {
            return _rebootAnalysysInfo.retryThroughReboot;
        }
        public static void ClearRetryThruRebootFile()
        {
            _rebootAnalysysInfo.retryThroughReboot = false;
        }
        public static bool HasDTMProcess()
        {
            return (Process.GetProcesses()
                .Where(p => p.ProcessName.ToLower().StartsWith("wlksvc") && p.MainModule.FileVersionInfo.FileDescription.Replace(" ", string.Empty).ToLower().Contains("wttsvc"))
                .Count() > 0);
        }
        public static bool IsPAVEEnvironment()
        {            
            return Directory.GetCurrentDirectory().ToLower().Contains("sharedbinary");
        }
        public static void ExitProcess(int argExitCode)
        {
            DeleteAllBackupFile();
            Log.GenerateHTMLReport();
            Console.ResetColor();
            Environment.ExitCode = argExitCode;
            Environment.Exit(argExitCode);
        }

        private static void DeleteAllBackupFile()
        {
            DirectoryInfo dir = new DirectoryInfo(Directory.GetCurrentDirectory());
            FileInfo[] backupFiles = dir.GetFiles("*.xml");
            File.Delete(_mpBSODAnalysisPath);
            foreach (FileInfo file in backupFiles)
            {
                if (file.Name.ToLower().Contains("backup"))
                    File.Delete(file.FullName);
            }
        }

        public static void RegisterDll(string argDLLName)
        {
            if (!argDLLName.Contains(".dll"))
                argDLLName += ".dll";

            string dllFilePath = string.Concat(@"""", Directory.GetCurrentDirectory(), "\\", argDLLName, @"""");
            Log.Verbose("Registering {0}", dllFilePath);
            StartProcess("regsvr32", string.Concat(@"/s ", dllFilePath), 1);
        }
        public static void KillProcess(string argProcessName)
        {
            Process.GetProcessesByName(argProcessName).Where(p => p.ProcessName.ToLower().Equals(argProcessName.ToLower())).ToList().ForEach(p =>
            {
                Log.Verbose("Killing process {0}", p.ProcessName);
                p.Kill();
            });
        }
        public static void PrintAllDetails(this DriverInfo argDriverInfo)
        {
            Log.Verbose("**************************************************");
            argDriverInfo.PrintBasicDetails();
            argDriverInfo.PrintControllerDetails();
            Log.Verbose("**************************************************");
        }
        public static void PrintBasicDetails(this DriverInfo argDriverInfo)
        {
            Log.Verbose("Driver.Name:: {0}", argDriverInfo.Name);
            Log.Verbose("Driver.Status:: {0}", argDriverInfo.Status);
            Log.Verbose("Driver.Version:: {0}", argDriverInfo.Version);
            Log.Verbose("Driver.Baseline:: {0}", argDriverInfo.DriverBaseLine);
            Log.Verbose("Driver.Description:: {0}", argDriverInfo.DriverDescription);
        }
        public static void FlushRecordedLogMsgs()
        {
            if (null != _recordLogMsgs)
            {
                _recordLogMsgs.ForEach(msg => Log.Verbose(msg));
                _recordLogMsgs.Clear();
            }
        }
        public static string GetCurrentDirectoryDrive()
        {
            string drive = Environment.GetEnvironmentVariable(_appSettings.DataPartitionRef);
            if (string.IsNullOrEmpty(drive))
                return Directory.GetParent(Directory.GetCurrentDirectory()).Root.Name;
            return string.Concat(drive, "\\");
        }

        private static void PrintControllerDetails(this DriverInfo argDriverInfo)
        {
            Log.Verbose("Driver.DeviceID:: {0}", argDriverInfo.DeviceID);
            Log.Verbose("Driver.VendorID:: {0}", argDriverInfo.VendorID);
            Log.Verbose("Driver.OEMFile:: {0}", argDriverInfo.OEMFile);
        }
        private static Type GetTypeInstance(Assembly argAssembly, string argInstanceName)
        {
            return (from type in argAssembly.GetTypes()
                    where type.Name.ToLower().Equals(argInstanceName.ToLower())
                    select type).SingleOrDefault();
        }
        public static bool HasRebootFile()
        {
            if (File.Exists(CommonExtensions._mpBSODAnalysisPath))
            {
                TimeSpan diff = DateTime.Now.Subtract(_rebootReason.dateTimeInfo);
                if (diff.Days < _appSettings.RebootFlgTimespanInDays)
                {
                    if (CommonExtensions._rebootAnalysysInfo.identifier.ToLower().Equals(string.Join("_", _cmdLineArgs).ToLower()))
                        return true;
                }
            }
            return false;
        }
        private static SecureString GetPassword(string argPassword)
        {
            SecureString securePassword = new SecureString();
            char[] password = Enumerable.Range(0, argPassword.Length).Select(i => Convert.ToChar(argPassword.Substring(i, 1))).ToArray();
            foreach (char pwd in password)
                securePassword.AppendChar(pwd);
            return securePassword;
        }
        public static string EncryptDecrypt(string textToEncrypt)
        {
            StringBuilder inSb = new StringBuilder(textToEncrypt);
            StringBuilder outSb = new StringBuilder(textToEncrypt.Length);
            char c;
            int key = 139;
            for (int i = 0; i < textToEncrypt.Length; i++)
            {
                c = inSb[i];
                c = (char)(c ^ key);
                outSb.Append(c);
            }
            return outSb.ToString();
        }
        private static RebootAnalysysInfo DoDeSerialize()
        {
            RebootAnalysysInfo rebootData = new RebootAnalysysInfo();
            XmlSerializer serializer = new XmlSerializer(typeof(RebootAnalysysInfo));
            FileStream fs = new FileStream(CommonExtensions._rebootAnalysysInfo.path, FileMode.Open);
            XmlReader reader = XmlReader.Create(fs);
            try
            {
                rebootData = (RebootAnalysysInfo)serializer.Deserialize(reader);
            }
            catch
            {
                if (_appSettings.AlternateLogFile)
                {
                    fs.Close();
                    File.Delete(CommonExtensions._rebootAnalysysInfo.path);
                    File.Move(CommonExtensions._rebootAnalysysInfoBackupPath, CommonExtensions._rebootAnalysysInfo.path);
                    fs = new FileStream(CommonExtensions._rebootAnalysysInfo.path, FileMode.Open);
                    reader = XmlReader.Create(fs);
                    rebootData = (RebootAnalysysInfo)serializer.Deserialize(reader);
                }
                Log.Abort("Unable to parse log file, file got corrupted");
            }
            fs.Close();
            return rebootData;
        }
        public static void DoSinchorize(int reboodMethodIdx = 0)
        {
            RebootAnalysysInfo rebootData = CommonExtensions._rebootAnalysysInfo;
            rebootData.dateTimeInfo = DateTime.Now;
            if (rebootData.currentMethodIdx == 0)
                rebootData.currentMethodIdx = reboodMethodIdx;
            else if (reboodMethodIdx != -1)
                rebootData.currentMethodIdx = reboodMethodIdx;
            rebootData.rebootJobID = rebootData.jobID;
            rebootData.rebootReason = rebootData.rebootReason;
            if (rebootData.retryThroughReboot)
                rebootData.currentMethodIdx = reboodMethodIdx - 1;

            rebootData.pluggedDisplayList = DisplayExtensions.pluggedDisplayList;

            XmlSerializer writer =
                new XmlSerializer(typeof(RebootAnalysysInfo));
            System.IO.StreamWriter file = new System.IO.StreamWriter(rebootData.path);
            writer.Serialize(file, rebootData);
            file.Close();
            if (_appSettings.AlternateLogFile)
            {
                File.Delete(CommonExtensions._rebootAnalysysInfoBackupPath);
                string arg = "/c copy /v /y " + rebootData.path + " " + CommonExtensions._rebootAnalysysInfoBackupPath;
                StartProcess("cmd.exe", arg).WaitForExit();
            }
        }
        public static RebootDataProvider RebootLogDeSerialize()
        {
            RebootDataProvider rebootData = new RebootDataProvider();
            XmlSerializer serializer = new
            XmlSerializer(typeof(RebootDataProvider));
            FileStream fs = new FileStream(CommonExtensions._mpBSODAnalysisPath, FileMode.Open);
            XmlReader reader = XmlReader.Create(fs);
            try
            {
                rebootData = (RebootDataProvider)serializer.Deserialize(reader);
            }
            catch
            {
                if (_appSettings.AlternateLogFile)
                {
                    fs.Close();
                    File.Delete(CommonExtensions._mpBSODAnalysisPath);
                    File.Move(CommonExtensions._mpBSODAnalysisBackupPath, CommonExtensions._mpBSODAnalysisPath);
                    fs = new FileStream(CommonExtensions._mpBSODAnalysisPath, FileMode.Open);
                    reader = XmlReader.Create(fs);
                    rebootData = (RebootDataProvider)serializer.Deserialize(reader);
                }
                Log.Abort("Unable to parse log file, file got corrupted");
            }
            fs.Close();
            return rebootData;
        }


        public static void RebootLogSerialize()
        {
            _rebootReason.jobID = CommonExtensions._rebootAnalysysInfo.jobID;
            _rebootReason.identifier = CommonExtensions._rebootAnalysysInfo.identifier;
            _rebootReason.dateTimeInfo = DateTime.Now;
            _rebootReason.osCreationTime = Directory.GetCreationTime(@"C:\Windows\System32");
            XmlSerializer writer = new XmlSerializer(typeof(RebootDataProvider));
            System.IO.StreamWriter file = new System.IO.StreamWriter(CommonExtensions._mpBSODAnalysisPath);
            writer.Serialize(file, _rebootReason);
            file.Close();

            if (_appSettings.AlternateLogFile)
            {
                File.Delete(CommonExtensions._mpBSODAnalysisBackupPath);
                string arg = "/c copy /v /y " + CommonExtensions._mpBSODAnalysisPath + " " + CommonExtensions._mpBSODAnalysisBackupPath;
                StartProcess("cmd.exe", arg).WaitForExit();
            }
        }
        public static void Exit(int argExitCode)
        {
            CommonExtensions.ClearRebootFile();
            CommonExtensions.ExitProcess(argExitCode);
        }

        public static bool DoesWindowsIdMatched(uint WindowsMonitorID1, uint WindowsMonitorID2)
        {
            if (WindowsMonitorID1 == WindowsMonitorID2 || (WindowsMonitorID1 & 0x00FFFFFF) == WindowsMonitorID2 || WindowsMonitorID1 == (WindowsMonitorID2 & 0x00FFFFFF))
                return true;
            else
                return false;
        }

        public static uint GetMaskedWindowsId(OSType OS, uint WindowsMonitorID)
        {
            uint tempWindowsID = WindowsMonitorID;
            if (OS == OSType.WINTHRESHOLD)
                tempWindowsID = WindowsMonitorID & 0x00FFFFFF;

            return tempWindowsID;
        }

        public static void PrintULTErrorCodes(uint returnValue)
        {
            foreach (uint item in Enum.GetValues(typeof(ULT_Return_Codes)))
            {
                if (item != (uint)ULT_Return_Codes.ULT_STATUS_SUCCESS)
                {
                    if ((item & returnValue) == item)
                    {
                        Log.Fail(String.Format("Failed with: {0}", Enum.GetName(typeof(ULT_Return_Codes), item)));
                    }
                }
            }
        }

        //public static void CloneDirectory(string source, string destination, string sourceDriverVersion)
        //{
        //    DRV_COPY_ARG copyStatus = ValidateGfxCopy(source, destination);
        //    string destinationDriverVersion = null;
        //    if (copyStatus == DRV_COPY_ARG.DEST_MISMATCH)
        //    {
        //        //copy driver to alternate path
        //        if (Directory.Exists(destination))
        //            Directory.Delete(destination, true);
        //        Directory.CreateDirectory(destination);
        //        Log.Verbose("Copying gfx driver from {0} to {1}", source, destination);
        //        CommonExtensions.CopyRecursive(source, destination);
        //        if (CommonExtensions.ValidateGfxCopy(source, destination) == DRV_COPY_ARG.DEST_MISMATCH)
        //        {
        //            Directory.Delete(destination, true);
        //            Directory.CreateDirectory(destination);
        //            CommonExtensions.CopyRecursive(source, destination);
        //            if (CommonExtensions.ValidateGfxCopy(source, destination) == DRV_COPY_ARG.DEST_MISMATCH)
        //                Log.Abort("Unable to copy GFX Driver to alternate path");
        //            else
        //                Log.Verbose("Successfully copy Gfx driver package");
        //        }
        //        else
        //            Log.Verbose("Successfully copy Gfx driver package");
        //    }
        //    else if (copyStatus == DRV_COPY_ARG.SOURCE_MISMATCH)
        //    {
        //        //Check whether the destination version is same as installed driver version
        //        destinationDriverVersion = File.ReadAllText(destination + _appSettings.DriverVersionFileName);
        //        if (!sourceDriverVersion.Equals(destinationDriverVersion))
        //            Log.Abort("Mismatch in the Driver Version of Source and Destination");

        //        //copy driver from alternate path to default path
        //        Log.Verbose("Copying gfx driver from {0} to {1}", destination, source);
        //        if (Directory.Exists(source))
        //            Directory.Delete(source, true);
        //        Directory.CreateDirectory(source);
        //        CommonExtensions.CopyRecursive(destination, source);
        //        if (CommonExtensions.ValidateGfxCopy(source, destination) == DRV_COPY_ARG.SOURCE_MISMATCH)
        //        {
        //            Directory.Delete(source, true);
        //            Directory.CreateDirectory(source);
        //            CommonExtensions.CopyRecursive(destination, source);
        //            if (CommonExtensions.ValidateGfxCopy(source, destination) == DRV_COPY_ARG.SOURCE_MISMATCH)
        //                Log.Abort("Unable to copy GFX Driver to alternate path");
        //            else
        //                Log.Verbose("Successfully copy Gfx driver package");
        //        }
        //        else                   
        //            Log.Verbose("Successfully copy Gfx driver package");                
        //    }
        //    else
        //    {
        //        Log.Verbose("Copy Status is match");
        //        destinationDriverVersion = File.ReadAllText(destination + _appSettings.DriverVersionFileName);
        //        if(sourceDriverVersion.Equals(destinationDriverVersion))
        //            Log.Verbose("Source and destination are in Sync");
        //        else
        //        {
        //            //even source and destination are in sync, there is differnce with destination driver version and installed driver version. So copy driver from source to destination
        //            if (Directory.Exists(destination))
        //                Directory.Delete(destination, true);
        //            Directory.CreateDirectory(destination);
        //            Log.Verbose("Copying gfx driver from {0} to {1}", source, destination);
        //            CommonExtensions.CopyRecursive(source, destination);
        //            if (CommonExtensions.ValidateGfxCopy(source, destination) == DRV_COPY_ARG.DEST_MISMATCH)
        //            {
        //                Directory.Delete(destination, true);
        //                Directory.CreateDirectory(destination);
        //                CommonExtensions.CopyRecursive(source, destination);
        //                if (CommonExtensions.ValidateGfxCopy(source, destination) == DRV_COPY_ARG.DEST_MISMATCH)
        //                    Log.Abort("Unable to copy GFX Driver to alternate path");
        //                else
        //                    Log.Verbose("Successfully copy Gfx driver package");
        //            }
        //            else
        //                Log.Verbose("Successfully copy Gfx driver package");
        //        }
        //    }
        //}

        public static void CopyRecursive(string argSource, string argDestination)
        {

            DirectoryInfo dir = new DirectoryInfo(argSource);
            DirectoryInfo[] dirs = dir.GetDirectories();
            if (!dir.Exists)
            {
                Log.Abort("Source directory does not exist or could not be found: " + argSource);
            }
            if (!Directory.Exists(argDestination))
                Directory.CreateDirectory(argDestination);
            FileInfo[] files = dir.GetFiles();
            foreach (FileInfo file in files)
            {
                string temppath = Path.Combine(argDestination, file.Name);
                file.CopyTo(temppath, false);
            }
            foreach (DirectoryInfo subdir in dirs)
            {
                string temppath = Path.Combine(argDestination, subdir.Name);
                CopyRecursive(subdir.FullName, temppath);
            }

        }

        public static DRV_COPY_ARG ValidateGfxCopy(string argOriginalPath, string argAlternatePath)
        {
            if (!Directory.Exists(argAlternatePath))
                return DRV_COPY_ARG.DEST_MISMATCH;
            if (!Directory.Exists(argOriginalPath))
                return DRV_COPY_ARG.SOURCE_MISMATCH;
            string[] sourceFiles = Directory.GetFiles(argOriginalPath, "*", SearchOption.AllDirectories);
            string[] destFiles = Directory.GetFiles(argAlternatePath, "*", SearchOption.AllDirectories);
            if (sourceFiles.Length < destFiles.Length)
                return DRV_COPY_ARG.SOURCE_MISMATCH;
            else if (destFiles.Length < sourceFiles.Length)
                return DRV_COPY_ARG.DEST_MISMATCH;
            else
                return DRV_COPY_ARG.MATCH;
        }

        public static bool VerifyWDTFStatus()
        {
            string cmd = @" QUERY HKLM\Software\Microsoft\WDTF";
            Process wdtfProcess = Process.Start("REG", cmd);
            wdtfProcess.WaitForExit();
            if (wdtfProcess.ExitCode == 0)
                return true;
            return false;
        }
    }
}
