namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using System.Xml.Serialization;
    using XMLToExcel;
    using Microsoft.Win32;
    using System.Xml;
    using System.Text.RegularExpressions;

    class SystemResponsiveness : FunctionalBase, IParse, ISet
    {
        // Activate an application window.
        [DllImport("USER32.DLL")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        bool ButtonClickStatus = false;
        List<string> supportedCfg = new List<string>() { "standby (s3)", "hibernate", "hybrid sleep", "fast startup" };
        string dir = Directory.GetCurrentDirectory() + "\\ADKTimer.xml";
        string AppDataPath = string.Empty;
        string resultCSVFilePath = string.Empty;

        public void Parse(string[] args)
        {
            if (args.IsHelpCall())
                this.HelpText();
            else
            {
                RunTest();
            }
        }

        public object Set
        {
            set { RunTest(); }
        }

        private void RunTest()
        {
            try
            {
                DirectoryInfo parentDir = Directory.GetParent(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData));
                AppDataPath = parentDir.FullName + @"\Local\Microsoft\Axe\Results";
                Log.Message(true, "Checking ADK Test precondition");
                if (!ChecksystemConfig())
                {
                    Log.Alert("ADK test dose't meet system configuration S3/S4");
                    Log.Message("Enabling S4 into the test system");
                    Process sysCfg = CommonExtensions.StartProcess("powercfg.exe", "/hibernate on");
                    Thread.Sleep(3000);
                    if (!ChecksystemConfig())
                        Log.Abort("ADK test dose't meet system configuration S3/S4");
                }
                if (!ReadRegistry())
                {
                    RunADKTest();
                    if (ButtonClickStatus)
                        CreateRegistry();
                }
                GetResult();
            }
            catch (Exception ex)
            {
                DeleteRegistry();
                Log.Abort("Error: {0}", ex);
            }
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("ADK script should be located in C:\\Pre-Setups\\ADK");
            sb.Append("Execute.exe SystemResponsiveness");
        }

        private bool GetResult()
        {
            return CheckPowerShellStatus();
        }
        private bool ChecksystemConfig()
        {
            CommonExtensions.StartProcess("verifier.exe", string.Format("/reset"));
            Thread.Sleep(3000);
            List<string> testCfg = new List<string>();
            Process sysCfg = CommonExtensions.StartProcess("powercfg.exe", "/a");
            while (!sysCfg.StandardOutput.EndOfStream)
            {
                string line = sysCfg.StandardOutput.ReadLine();
                if (line == "The following sleep states are not available on this system:")
                    break;
                if (supportedCfg.Any(st => line.ToLower().Contains(st)))
                {
                    testCfg.Add(line.Trim().ToLower());
                }
            }
            Enumerable.SequenceEqual(supportedCfg.OrderBy(t => t), testCfg.OrderBy(t => t));
            if (supportedCfg.SequenceEqual(testCfg))
                return true;
            return false;
        }

        private void RunADKTest()
        {
            ADKSystemRequirement();
            Log.Message(true,"************************** ADK Test Starts **************************");
            if (Directory.Exists(base.AppSettings.ADKPath + @"\results"))
            {
                Log.Verbose("Clearing previous result file from {0}", base.AppSettings.ADKPath);
                Directory.Delete(base.AppSettings.ADKPath + @"\results", true);
            }
            if (Directory.Exists(AppDataPath))
            {
                Log.Verbose("Deleting AppData result file");
                Directory.Delete(AppDataPath, true);
            }
            string[] runjob = Directory.GetFiles(base.AppSettings.ADKPath, "*.cmd");
            if (runjob.Length != 0)
            {
                CommonExtensions.StartProcess(runjob[0], base.AppSettings.ADKProcessUserName, base.AppSettings.ADKProcessPassword);
                //Process.Start(runjob[0]);
                Thread.Sleep(5000);
                #region Run Job click

                for (int eachButton = 0; eachButton < ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children.Count; eachButton++)
                {
                    if (ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].Children[0].Children.Count == 0)
                    {
                        SearchButton("RUN", ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].FindChildren<Ranorex.Button>());
                    }
                    else
                    {
                        SearchButton("RUN", ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].Children[0].FindChildren<Ranorex.Button>());
                    }
                    if (ButtonClickStatus)
                        break;
                }
                #endregion
                if (ButtonClickStatus)
                {
                    ButtonClickStatus = false;
                    #region Start button click
                    Log.Verbose("Waiting for Start button click");
                    Ranorex.Delay.Seconds(20);
                    for (int eachButton = 0; eachButton < ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children.Count; eachButton++)
                    {
                        for (int eachSubButton = 0; eachSubButton < ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].Children.Count; eachSubButton++)
                        {
                            for (int l2 = 0; l2 < ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].Children[eachSubButton].Children.Count; l2++)
                            {
                                if (ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].Children[eachSubButton].Children[l2].Children.Count == 0)
                                {
                                    SearchButton("START", ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].Children[eachSubButton].FindChildren<Ranorex.Button>());
                                }
                                else
                                {
                                    SearchButton("START", ADKRepo.Instance.AssessmentLauncherNewJob4.Self.Children[eachButton].Children[eachSubButton].Children[l2].FindChildren<Ranorex.Button>());
                                }
                            }
                        }
                    }

                    #endregion
                }
                else
                {
                    Log.Alert("Run job button click Failed !!");
                }
            }
            else
            {
                Log.Abort("Runjob script not found at {0}", base.AppSettings.ADKPath);
                //Environment.Exit(0);
            }
        }

        private void SearchButton(string searchPattern, IList<Ranorex.Button> buttonList)
        {
            foreach (Ranorex.Button runButton in buttonList)
            {
                if (runButton.Text.ToUpper().Contains(searchPattern))
                {
                    runButton.Press();
                    ButtonClickStatus = true;
                    Log.Verbose("{0} job button click successfully", searchPattern);
                    break;
                }
            }
        }

        private void ADKSystemRequirement()
        {
            Log.Alert("To run the ADK test successfully system should meet the following requirement");
            Log.Verbose("ADK script should be located in C:\\Pre-Setups\\ADK");
            Log.Verbose("Automantio script will not take care of any system specific issue.");
            Log.Verbose("Also automation script not check for whether system meets the below requirement");
            Log.Verbose("System Details:");
            Log.Verbose("BIOS/GOP - based on the Start message will be configured.");
            Log.Verbose("Driver to be installed - Chipset, Graphics, LAN, ME (HECI) and Wifi  Drivers (for ULT need to install Serial IO, RST drivers).");
            Log.Verbose("OS Installation with all the updates.");
            Log.Verbose("Disabling Driver Verifier");
            Thread.Sleep(5000);
        }

        private bool CheckPowerShellStatus()
        {
            Log.Verbose("Wait for sometime to generate result file...");
            while (true)
            {
                // ############ check Powershell window came or not. ###########
                // ############ if there is no powershell window, wait for 4 hrs ######
                //IntPtr powerShellHandle = FindWindow("powerShellFrame", "powershell");
                Thread.Sleep(15000);
                DateTime startTime = DeSerialize();
                DateTime endtime = DateTime.Now;
                TimeSpan diff = endtime.Subtract(startTime);
                if (diff.Days > 0 || diff.Hours >= 6)
                    break;
                Process powerShellProcess = Process.GetProcesses().Where(p => p.ProcessName.ToLower().Contains("powershell")).FirstOrDefault();
                // Verify that powerShell is a running process. 
                if (powerShellProcess != null)
                {
                    PowerShellClickEvent(powerShellProcess);
                    break;
                }
            }
            DeleteRegistry();
            if (Directory.Exists(base.AppSettings.ADKPath + @"\results"))
                GetResultCSVFile(base.AppSettings.ADKPath + @"\results");
            else
            {
                ResultDataCreation(AppDataPath);
            }
            return true;
        }

        private void GetResultCSVFile(string argPath)
        {
            DirrectorySerch(argPath);
            if (resultCSVFilePath == string.Empty)
            {
                ResultDataCreation(base.AppSettings.ADKPath + @"\results");
            }
            PopulateResult(resultCSVFilePath);
        }

        private void PopulateResult(string resultFilePath)
        {
            Log.Message(true, "*********************** ADK PARSE DATA START ***********************");
            ADK_Parser parser = new ADK_Parser();
            base.CopyOver(parser);
            parser.MachineInfo = base.MachineInfo;
            parser.Init(resultFilePath);
            Log.Message("---------------------------------------------------------------------");
            Log.Message("*********************** ADK PARSE DATA END ***********************");

            ConvertDatatoExcel(parser);
        }

        private void DirrectorySerch(string path)
        {
            try
            {
                GetFile(path);
                if (resultCSVFilePath == string.Empty)
                {
                    foreach (string eachDir in Directory.GetDirectories(path.Replace("\"", string.Empty)))
                        DirrectorySerch(eachDir);
                }
            }
            catch (System.Exception excpt)
            {
                Log.Abort(excpt.Message);
            }

        }

        private void GetFile(string path)
        {
            foreach (string responsivenessFile in Directory.GetFiles(path))
            {
                string fileName = Path.GetFileName(responsivenessFile);
                Match match = Regex.Match(fileName, @"responsiveness_report_([0-9\-]+)\.csv$",
                    RegexOptions.IgnoreCase);
                if (match.Success)
                {
                    resultCSVFilePath = responsivenessFile;
                    break;
                }
            }
        }

        private void ResultDataCreation(string argPath)
        {
            Log.Alert("ADK result data not found normally");
            AppDataResultmanipulation(argPath);
            Process powerShellProcess = Process.GetProcesses().Where(p => p.ProcessName.ToLower().Contains("powershell")).FirstOrDefault();
            if (powerShellProcess != null)
                PowerShellClickEvent(powerShellProcess);
            KillProcess("powershell");
            GetResultCSVFile(argPath);
        }

        private void AppDataResultmanipulation(string argPath)
        {
            //string assessment4PowerShell = base.AppSettings.ADKPath + @"\Assessment4\RespTime";
            string workingDir = base.AppSettings.ADKPath + @"\Assessment4";
            string xmlFilePath = string.Empty;
            string[] dirPath = Directory.GetDirectories(argPath);
            var xmlDirPath = new DirectoryInfo(dirPath.First()).GetFiles("*xml", SearchOption.TopDirectoryOnly);
            var psFilePath = new DirectoryInfo(workingDir).GetFiles("*ps1", SearchOption.TopDirectoryOnly);
            foreach (FileInfo eachXML in xmlDirPath)
            {
                if (eachXML.Name.ToLower().StartsWith("jobresults"))
                    xmlFilePath = eachXML.FullName;
            }
            if (xmlFilePath != string.Empty)
            {
                Log.Verbose("XML file path {0}", xmlDirPath);
                StartProcess(workingDir);
                Process powerShellProcess = Process.GetProcesses().Where(p => p.ProcessName.ToLower().Contains("powershell")).FirstOrDefault();
                SetForegroundWindow(powerShellProcess.MainWindowHandle);
                SendKeys.SendWait("set-executionpolicy unrestricted");
                SendKeys.SendWait("{ENTER}");
                Thread.Sleep(2000);
                SendKeys.SendWait("y");
                SendKeys.SendWait("{ENTER}");
                Thread.Sleep(2000);
                SendKeys.SendWait(@".\"+ psFilePath.First().Name);
                SendKeys.SendWait("{ENTER}");
                Thread.Sleep(2000);
                SendKeys.SendWait(dirPath.First());
                SendKeys.SendWait("{ENTER}");
                SendKeys.SendWait(xmlFilePath);
                SendKeys.SendWait("{ENTER}");
                Log.Verbose("Waiting for log processing time");
                Thread.Sleep(200000);
            }
        }

        public Process StartProcess(string argWorkingDir)
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.UseShellExecute = true;
            processStartInfo.CreateNoWindow = false;
            processStartInfo.WindowStyle = ProcessWindowStyle.Normal;
            processStartInfo.WorkingDirectory = argWorkingDir;
            processStartInfo.FileName = "powershell.exe";
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();
            Thread.Sleep(3000);
            return process;
        }

        private void PowerShellClickEvent(Process powerShellProcess)
        {
            Log.Verbose("Press Enter to exit from power shell window.");
            SetForegroundWindow(powerShellProcess.MainWindowHandle);
            SendKeys.SendWait("{ENTER}");
            Log.Verbose("Waiting for 4 minute for generating result file");
            //############ wait for 5 mnt to generate result file ############
            Thread.Sleep((60 * 5) * 1000);

            Process axeProcess = Process.GetProcesses().Where(p => p.ProcessName.ToLower().Contains("al")).FirstOrDefault();
            if (axeProcess != null)
            {
                Log.Verbose("Exiting from Axe Process");
                KillProcess("axe");
            }

            Process alProcess = Process.GetProcesses().Where(p => p.ProcessName.ToLower().Contains("al")).FirstOrDefault();
            Thread.Sleep(5000);
            if (alProcess != null)
            {
                Log.Verbose("Exiting from Al process");
                KillProcess("al");
            }
            Thread.Sleep(2000);
        }

        private void KillProcess(string processName)
        {
            Process[] processList = Process.GetProcessesByName(processName);
            foreach (Process eachProcess in processList)
            {
                eachProcess.Kill();
                Log.Verbose("Exiting from {0} process successfully", processName);
            }
        }

        private void ConvertDatatoExcel(ADK_Parser parser)
        {
            XMLWriter xmlWriter = new XMLWriter();
            xmlWriter.CreateXML(parser, base.MachineInfo);
            OpenXMLOffice objTest = new OpenXMLOffice();
            objTest.XMLToExcel(Directory.GetCurrentDirectory() + @"\ADKResult.xml");
            File.Delete(Directory.GetCurrentDirectory() + @"\ADKResult.xml");
            if (Directory.GetFiles(Directory.GetCurrentDirectory(), "*.xlsx").Length != 0)
                Log.Message("Excel file generated successfully.");
            Log.Message("************************** ADK Test End **************************");

        }

        private DateTime DeSerialize()
        {
            XmlSerializer serializer = new
            XmlSerializer(typeof(DateTime));
            FileStream fs = new FileStream(dir, FileMode.Open);
            XmlReader reader = XmlReader.Create(fs);
            DateTime currentTime = (DateTime)serializer.Deserialize(reader);
            fs.Close();
            return currentTime;
        }

        private void CreateRegistry()
        {
            RegistryKey softwareKey = Registry.CurrentUser.CreateSubKey("ADK", RegistryKeyPermissionCheck.ReadWriteSubTree);
            softwareKey.SetValue("ADKData", 1, RegistryValueKind.DWord);
            Thread.Sleep(2000);
            if (!ReadRegistry())
                Log.Abort("Unable to create ADK registry");

            Log.Verbose("Create Timer for ADK process");
            File.Delete(dir);
            DateTime current = DateTime.Now;
            XmlSerializer writer =
                new XmlSerializer(typeof(DateTime));
            System.IO.StreamWriter file = new System.IO.StreamWriter(dir);
            writer.Serialize(file, current);
            file.Close();
        }

        private bool ReadRegistry()
        {
            RegistryKey softwareKey = Registry.CurrentUser.OpenSubKey("ADK", true);
            if (softwareKey != null)
            {
                object value = softwareKey.GetValue("ADKData");
                return Convert.ToBoolean(value);
            }
            return false;
        }

        private void DeleteRegistry()
        {
            File.Delete(dir);
            RegistryKey softwareKey = Registry.CurrentUser.OpenSubKey("ADK", true);
            if (softwareKey != null)
                Registry.CurrentUser.DeleteSubKey("ADK", true);
        }
    }
}
