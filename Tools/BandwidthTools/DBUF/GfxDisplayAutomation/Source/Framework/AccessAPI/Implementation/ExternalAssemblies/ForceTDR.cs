namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Windows.Automation;

    internal class ForceTDR : FunctionalBase, ISetNoArgs
    {
        [ParseAttribute(InterfaceName = InterfaceType.ISetNoArgs, Comment = "Generate Force TDR")]
        public void Parse(string[] args)
        {
            Log.Verbose("In Test");
            if (args[0].ToLower().Contains("set"))
            {
                if (this.SetNoArgs())
                    Log.Success("TDR success");
                else
                    Log.Fail("Failed TDR");
            }
        }
        public bool SetNoArgs()
        {
            CommonExtensions.StartProcess("ForceTDR.exe", string.Empty, 2);
            Thread.Sleep(10000);

            AutomationElement rootElement = AutomationElement.RootElement;
            if (null != rootElement)
            {
                Condition regCondition = new PropertyCondition(AutomationElement.NameProperty, "well,", PropertyConditionFlags.IgnoreCase);
                AutomationElement appElement = rootElement.FindFirst(TreeScope.Children, regCondition);

                if (null != appElement)
                {
                    Condition textPatternAvailable = new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Text);
                    AutomationElement txtElement = appElement.FindFirst(TreeScope.Descendants, textPatternAvailable);

                    if (txtElement != null)
                    {
                        Log.Verbose("{0}", txtElement.Current.Name);

                        if (txtElement.Current.Name.ToLower().Contains("d3dkmtescape success"))
                        {
                            Log.Verbose("TDR successful");
                            CommonExtensions.KillProcess("ForceTDR");
                            Thread.Sleep(1000);
                            if (Directory.Exists(CommonExtensions.DumpPaths[DumpCategory.WatchDogdump]))
                            {
                                string[] files = Directory.GetFiles(CommonExtensions.DumpPaths[DumpCategory.WatchDogdump], "*.dmp");
                                if (files.Count() > 0)
                                {
                                    Log.Alert("TDR dump file {0}", files.First());
                                    File.Delete(files.First());
                                }
                            }
                            CommonExtensions.ClearRetryThruRebootFile();
                            ClearTDRWatch();
                            return true;
                        }
                    }
                }
            }
            ClearTDRWatch();
            CommonExtensions.KillProcess("ForceTDR");
            Thread.Sleep(1000);
            return false;
        }

        private void ClearTDRWatch()
        {
            string path = string.Empty;
            foreach (DriveInfo d in DriveInfo.GetDrives().Where(x => x.IsReady == true).Where(T => T.DriveType == DriveType.Fixed))
            {
                if (d.RootDirectory.FullName != "C:\\")
                    path = GetTDRWatchPath(d.RootDirectory.FullName);
                if (path != string.Empty)
                    break;
            }
            if (!string.IsNullOrEmpty(path))
            {
                Log.Verbose("TDRWatch path: {0} ", path);
                Log.Verbose("Clearing TDR wach count for PAVE result");
                if (File.Exists(path))
                {
                    CommonExtensions.StartProcess(path, "/Get 123456", 3, Path.GetDirectoryName(path)).WaitForExit();
                    CommonExtensions.StartProcess(path, "/Set 123456", 3, Path.GetDirectoryName(path)).WaitForExit();
                }
            }
            else
                Log.Alert("Unable to find TDRWatch path");
        }
        private string GetTDRWatchPath(string srcDir)
        {
            try
            {
                foreach (string d in Directory.GetDirectories(srcDir))
                {
                    foreach (string f in Directory.GetFiles(d, "*TDRWatch.exe", SearchOption.AllDirectories))
                    {
                        if(base.MachineInfo.OS.Architecture.Contains("64") && f.ToLower().Contains("tdr64"))
                            return f;
                    }
                    GetTDRWatchPath(d);
                }
                return string.Empty;
            }
            catch { return string.Empty; }
        }
        
    }
}
