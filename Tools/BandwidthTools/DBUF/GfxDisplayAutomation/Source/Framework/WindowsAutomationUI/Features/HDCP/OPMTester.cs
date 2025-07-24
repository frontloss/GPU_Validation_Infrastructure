namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Automation;
    using System.Collections.Generic;
    using System.Windows.Forms;
    using System;
    using System.Security.AccessControl;

    internal class OPMTester : HDCPBase
    {
        private static Dictionary<HDCPPlayerInstance, OPMData> _opmInstanceList = null;
        private HDCPPlayerInstance currentInstanceId;
        private const string OPM_Folder = "\\OPMTester";
        private const string videoFileName = "\\baseball.mpeg";

        private class OPMData
        {
            public Process Process;
            public string PlayerPath;

            public OPMData()
            {
            }

            public OPMData(Process process, string playerPath)
            {
                Process = process;
                PlayerPath = playerPath;
            }
        }

        internal override Process Instance(HDCPPlayerInstance instanceId)
        {
            string playerName = "OPMTester.exe";
            Process playerProcess = default(Process);
            currentInstanceId = instanceId;

            if (_opmInstanceList == null)
                _opmInstanceList = new Dictionary<HDCPPlayerInstance, OPMData>();
            if (_opmInstanceList.ContainsKey(instanceId))
            {
                playerProcess = _opmInstanceList[instanceId].Process;
            }
            else
            {
                //Copying the OPMTester folder
                string sourcePath = base.AppSettings.DisplayToolsPath + OPM_Folder;
                string destinationPath = Directory.GetCurrentDirectory() + OPM_Folder + "_" + instanceId; //OPMTester_Player_x
                base.HDCPParams.HDCPAppName = playerName;
                string playerPath = destinationPath + "\\" + playerName;

                //Fetch the source & destination directory
                if (!Directory.Exists(sourcePath))
                    Log.Abort("OPMTester directory not found");
                DirectoryInfo sourceDirectory = new DirectoryInfo(sourcePath);
                DirectoryInfo destinationDirectory = null;
                if (!Directory.Exists(destinationPath))
                {
                    destinationDirectory = Directory.CreateDirectory(destinationPath);
                    if (destinationDirectory == null)
                        Log.Abort("Failed to create \\OPMTester_Player_x directory");
                }
                else
                {
                    destinationDirectory = new DirectoryInfo(destinationPath);
                    //Clean up the destination directory contents
                    Thread.Sleep(2000);

                    foreach (FileInfo file in destinationDirectory.GetFiles())
                    {
                        file.Delete();
                    }
                }
                //Copy files from source to destination
                foreach (FileInfo tempFile in sourceDirectory.GetFiles())
                {
                    FileInfo destinationFile = tempFile.CopyTo(Path.Combine(destinationPath, tempFile.Name), true);
                    if (destinationFile == null)
                        Log.Abort("Failed to copy the tester file/s.");
                }

                if (!File.Exists(playerPath))
                    Log.Abort("{0} does not exist!", playerPath);

                Log.Verbose("Launching {0}", playerPath);
                playerProcess = CommonExtensions.StartProcess(playerPath, "-manual", 0);

                _opmInstanceList.Add(instanceId, new OPMData(playerProcess, destinationPath));
                Move(playerProcess);
                Open(playerProcess, destinationPath + videoFileName);
            }
            return playerProcess;
        }
        private void Open(Process processId, string path)
        {
            PropertyCondition condition1 = new PropertyCondition(AutomationElement.AutomationIdProperty, "1148");
            PropertyCondition condition2 = new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Edit);
            AndCondition condition = new AndCondition(condition1, condition2);

            SetWindowFocus(processId);
            Thread.Sleep(2000);
            SendKeys.SendWait("%{F}{O}");
            Thread.Sleep(2000);

            ValuePattern valPattern = AutomationElement.RootElement.FindFirst(TreeScope.Descendants, condition).GetCurrentPattern(ValuePattern.Pattern) as ValuePattern;
            valPattern.SetValue(path);

            Thread.Sleep(2000);
            SendKeys.SendWait("%{O}");
            Thread.Sleep(100000);
        }
        internal override void Move(Process argProcess)
        {
            if (base.IsMoveApplicable())
            {
                base.Move(argProcess);
            }
        }
        internal override void Close(Process argProcess)
        {
            base.Close(argProcess);
            string[] files = Directory.GetFiles(_opmInstanceList[currentInstanceId].PlayerPath);
            foreach (string g in files)
            {
                File.SetAttributes(g, FileAttributes.Normal);
                Thread.Sleep(1000);
                File.Delete(g);
            }
            _opmInstanceList.Remove(currentInstanceId);
        }
        internal override void ActivateHDCP(Process argProcess)
        {
            Log.Verbose("Activating HDCP");
            SetWindowFocus(argProcess);
            Thread.Sleep(5000);
            SendKeys.SendWait("%{O}{C}{H}{A}");
            Thread.Sleep(5000);
            Log.Verbose("HDCP Activated on OPMTester " + currentInstanceId);
        }
        internal override void DeactivateHDCP(Process processId)
        {
            Log.Verbose("Deactivating HDCP");
            SetWindowFocus(processId);
            Thread.Sleep(5000);
            SendKeys.SendWait("%{O}{C}{H}{D}");
            Thread.Sleep(5000);
            Log.Verbose("HDCP Deactivated on OPMTester " + currentInstanceId);
        }

        internal override void QueryGlobalProtectionLevel(Process processId)
        {
            SetWindowFocus(processId);
            Thread.Sleep(2000);
            SendKeys.SendWait("{Alt}{O}{Q}{G}");
            Thread.Sleep(2000);
            Log.Verbose("Global Protection Level Queried for OPM Tester " + currentInstanceId);
        }

        internal override void QueryLocalProtectionLevel(Process processId)
        {
            SetWindowFocus(processId);
            Thread.Sleep(2000);
            SendKeys.SendWait("%{O}{Q}{L}");
            Thread.Sleep(2000);
            Log.Verbose("Local Protection Level Queried  for OPM Tester " + currentInstanceId);
        }

        internal override void SetSRM(Process processId)
        {
            SetWindowFocus(processId);
            Thread.Sleep(2000);
            SendKeys.SendWait("%{O}{C}{H}{S}");
            Thread.Sleep(2000);
            Log.Verbose("SRM Level is been set for OPM Tester" + currentInstanceId);
        }

        internal override void GetSRMVersion(Process processId)
        {
            SetWindowFocus(processId);
            Thread.Sleep(2000);
            SendKeys.SendWait("%{O}{Q}{S}");
            Thread.Sleep(2000);
            Log.Verbose("Queried SRM Version for OPM Tester " + currentInstanceId);
        }

        internal override void ActivateACP(Process processId)
        {
            SetWindowFocus(processId);
            Thread.Sleep(2000);
            SendKeys.SendWait("%{O}{C}{A}{1}");
            Thread.Sleep(2000);
            Log.Verbose(" Activated ACP for OPM Tester " + currentInstanceId);
        }

        internal override void ActivateCGMSA(Process processId)
        {
            SetWindowFocus(processId);
            Thread.Sleep(2000);
            SendKeys.SendWait("%{O}{C}{C}{F}");
            Thread.Sleep(2000);
            Log.Verbose(" Activated CGMS-A for OPM Tester " + currentInstanceId);
        }
    }
}