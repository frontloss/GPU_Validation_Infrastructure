using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading;
using System.Windows.Automation;
using System.Windows.Forms;

namespace PackageInstaller
{
    class NonPnPDriverRoutine
    {
        StubDriverParam DriverData;
        string DriverInstanceID;
        string DriverFilePath = @"C:\Windows\System32\drivers";
        private Dictionary<StubDriverService, string> Patterns;

        public NonPnPDriverRoutine()
        {
            Patterns = new Dictionary<StubDriverService, string>();

            Patterns.Add(StubDriverService.Disable, "disabled");
            Patterns.Add(StubDriverService.Enable, "enabled");
            Patterns.Add(StubDriverService.Status, "running");
        }

        public bool SetMethod(object argMessage)
        {
            DriverData = (StubDriverParam)argMessage;
            switch (DriverData.ServiceType)
            {
                case NonPnPDriverService.Install:
                    return InstallDriver();

                case NonPnPDriverService.UnInstall:
                    return UnInstallDriver();

                case NonPnPDriverService.Disable:
                    return DisableDriver();

                case NonPnPDriverService.Enable:
                    return EnableDriver();

                case NonPnPDriverService.Status:
                    return DriverStatus();

                case NonPnPDriverService.VerifyDriverUpdate:
                    return VerifyDriverUpdate();

                default:
                    Log.Fail("Wrong Input Parameter");
                    return false;
            }
        }

        private bool InstallDriver()
        {
            if (DriverData.InstallParam == null)
                return false;
            AddRegistryService();
            CommonRoutine.StartProcess("Hdwwiz.exe");
            Thread.Sleep(3000);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Next >", ControlType.Button));
            Thread.Sleep(3000);
            UIABaseHandler.Select(UIABaseHandler.SelectElementAutomationIdControlType("317", ControlType.RadioButton));
            Thread.Sleep(7000);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Next >", ControlType.Button));
            Thread.Sleep(1000);
            for (int DK = 0; DK <= 35; DK++)
            {
                SendKeys.SendWait("{DOWN}");
                AutomationElement AE = UIABaseHandler.SelectElementNameControlType("System devices", ControlType.Text);
                if (AE.Current.IsOffscreen == false && AE.Current.IsEnabled == true)
                {
                    SendKeys.SendWait("{DOWN}");
                    break;
                }
            }
            Thread.Sleep(1000);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Next >", ControlType.Button));
            Thread.Sleep(3000);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Have Disk...", ControlType.Button));
            SendKeys.SendWait(DriverData.InstallParam.DriverpackagePath);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("OK", ControlType.Button));
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Next >", ControlType.Button));
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Next >", ControlType.Button));
            Thread.Sleep(10000);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Finish", ControlType.Button));
            Thread.Sleep(10000);
            return false;
        }

        public bool UnInstallDriver()
        {
            if (DriverData.InstallParam == null)
                return false;

            CommonRoutine.StartProcess("dpinst.exe", " /s /u " + DriverData.InstallParam.DriverpackagePath + "\\" + DriverData.InstallParam.INFFileName);
            Thread.Sleep(5000);
            File.Delete(DriverFilePath + "\\" + DriverData.InstallParam.DriverBinaryName);
            return true;
        }

        public bool DisableDriver()
        {
            GetInstanceID();
            if (string.IsNullOrEmpty(DriverInstanceID))
                return false;
            return DevconHelper(StubDriverService.Disable);
        }

        public bool EnableDriver()
        {
            GetInstanceID();
            if (string.IsNullOrEmpty(DriverInstanceID))
                return false;
            return DevconHelper(StubDriverService.Enable);
        }

        public bool DriverStatus()
        {
            GetInstanceID();
            if (string.IsNullOrEmpty(DriverInstanceID))
                return false;
            return DevconHelper(StubDriverService.Status);
        }

        private void GetInstanceID()
        {
            if (DriverData.AccessParam == null)
                return;
            string ResultString = string.Empty;
            Process statusProcess = CommonRoutine.StartProcess("devcon.exe", GetCMDString(StubDriverService.InstanceID));
            while (!statusProcess.StandardOutput.EndOfStream)
            {
                ResultString = statusProcess.StandardOutput.ReadLine();
                if (ResultString.ToLower().Contains(DriverData.AccessParam.DriverStringPattern.ToLower()))
                {
                    DriverInstanceID = "@" + ResultString.Split(':').First().Trim();
                    break;
                }
            }
        }

        private bool DevconHelper(StubDriverService argServices)
        {
            string ResultString = string.Empty;
            string outString = string.Empty;
            Process statusProcess = CommonRoutine.StartProcess("devcon.exe", GetCMDString(argServices));
            Patterns.TryGetValue(argServices, out outString);

            while (!statusProcess.StandardOutput.EndOfStream)
            {
                ResultString = statusProcess.StandardOutput.ReadLine();
                if (ResultString.ToLower().Contains(outString.ToLower()))
                {
                    Log.Messege("Stub Driver is {0}", (argServices == StubDriverService.Status) ? "Running" : argServices.ToString());
                    Thread.Sleep(5000);
                    return true;
                }
            }
            Log.Messege("Stub Driver is not functional");
            return false;
        }

        private string GetCMDString(StubDriverService argService)
        {
            switch (argService)
            {
                case StubDriverService.Disable:
                    return "disable " + "\"" + DriverInstanceID + "\"";
                case StubDriverService.Enable:
                    return "enable " + "\"" + DriverInstanceID + "\"";
                case StubDriverService.Status:
                    return "status " + "\"" + DriverInstanceID + "\""; ;
                case StubDriverService.InstanceID:
                    return "find @root\\system*";
                case StubDriverService.Undefined:
                    return string.Empty;
                default:
                    return string.Empty;
            }
        }

        private void AddRegistryService()
        {
            CommonRoutine.StartProcess("regedit", " /s " + DriverData.InstallParam.RegKeyName, DriverData.InstallParam.DriverpackagePath);
            Thread.Sleep(6000);
        }

        private bool VerifyDriverUpdate()
        {
            if (!File.Exists(@"C:\Windows\System32\drivers\\" + DriverData.InstallParam.DriverBinaryName))
                return false;
            if (DriverData.InstallParam == null)
            {
                Log.Fail("Wrong Input");
                return false;
            }
            DateTime driverVersion = File.GetLastWriteTime(DriverData.InstallParam.DriverpackagePath + "\\" + DriverData.InstallParam.DriverBinaryName);
            DateTime installedVersion = File.GetLastWriteTime(@"C:\Windows\System32\drivers\\" + DriverData.InstallParam.DriverBinaryName);
            if (driverVersion == installedVersion)
            {
                Log.Messege("Stub Driver time stamp is same.");
                return true;
            }
            else
            {
                return false;
            }
        }
    }
}
