using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Automation;
using System.Windows.Forms;

namespace Intel.VPG.Display.Automation
{
    public enum Service
    {
        Undefined,
        Disable,
        Enable,
        Status,
        InstanceID
    }

    class NonPnPDriverRoutine : FunctionalBase, ISetMethod
    {
        PanelDeviceDriverParam DriverData;
        string DriverInstanceID;
        string DriverFilePath = @"C:\Windows\System32\drivers";
        private Dictionary<Service, string> Patterns;

        public NonPnPDriverRoutine()
        {
            Patterns = new Dictionary<Service, string>();

            Patterns.Add(Service.Disable, "disabled");
            Patterns.Add(Service.Enable, "enabled");
            Patterns.Add(Service.Status, "running");
        }

        public bool SetMethod(object argMessage)
        {
            DriverData = (PanelDeviceDriverParam)argMessage;
            switch (DriverData.ServiceType)
            {
                case NonPnPDriverService.Install:
                    return PanelBLCInstallDriver();

                case NonPnPDriverService.UnInstall:
                    return PanelBLCUnInstallDriver();

                case NonPnPDriverService.Disable:
                    return PanelBLCDisableDriver();

                case NonPnPDriverService.Enable:
                    return PanelBLCEnableDriver();

                case NonPnPDriverService.Status:
                    return PanelBLCDriverStatus();

                case NonPnPDriverService.VerifyDriverUpdate:
                    return VerifyDriverUpdate();

                default:
                    Console.WriteLine("Wrong Input Parameter");
                    return false;
            }
        }

        private bool PanelBLCInstallDriver()
        {
            if (DriverData.InstallParam == null)
                return false;
            AddRegistryService();
            CommonExtensions.StartProcess("Hdwwiz.exe", string.Empty, 3);
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

        public bool PanelBLCUnInstallDriver()
        {
            if (DriverData.InstallParam == null)
                return false;

            CommonExtensions.StartProcess("dpinst.exe", " /s /u " + DriverData.InstallParam.DriverpackagePath + "\\" + DriverData.InstallParam.INFFileName);
            Thread.Sleep(5000);
            File.Delete(DriverFilePath + "\\" + DriverData.InstallParam.DriverBinaryName);
            return true;
        }

        public bool PanelBLCDisableDriver()
        {
            PanelBLCGetInstanceID();
            if (string.IsNullOrEmpty(DriverInstanceID))
                return false;
            return PanelBLCDevconHelper(Service.Disable);
        }

        public bool PanelBLCEnableDriver()
        {
            PanelBLCGetInstanceID();
            if (string.IsNullOrEmpty(DriverInstanceID))
                return false;
            return PanelBLCDevconHelper(Service.Enable);
        }

        public bool PanelBLCDriverStatus()
        {
            PanelBLCGetInstanceID();
            if (string.IsNullOrEmpty(DriverInstanceID))
                return false;
            return PanelBLCDevconHelper(Service.Status);
        }

        private void PanelBLCGetInstanceID()
        {
            if (DriverData.AccessParam == null)
                return;
            string ResultString = string.Empty;
            Process statusProcess = CommonExtensions.StartProcess("devcon.exe", GetCMDString(Service.InstanceID));
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

        private bool PanelBLCDevconHelper(Service argServices)
        {
            string ResultString = string.Empty;
            string outString = string.Empty;
            Process statusProcess = CommonExtensions.StartProcess("devcon.exe", GetCMDString(argServices));
            Patterns.TryGetValue(argServices, out outString);

            while (!statusProcess.StandardOutput.EndOfStream)
            {
                ResultString = statusProcess.StandardOutput.ReadLine();
                if (ResultString.ToLower().Contains(outString.ToLower()))
                {
                    Log.Verbose("Panel Driver is {0}", (argServices == Service.Status) ? "Running" : argServices.ToString());
                    Thread.Sleep(5000);
                    return true;
                }
            }
            Log.Verbose("Panel Driver is not functional");
            return false;
        }

        private string GetCMDString(Service argService)
        {
            switch (argService)
            {
                case Service.Disable:
                    return "disable " + "\"" + DriverInstanceID + "\"";
                case Service.Enable:
                    return "enable " + "\"" + DriverInstanceID + "\"";
                case Service.Status:
                    return "status " + "\"" + DriverInstanceID + "\""; ;
                case Service.InstanceID:
                    return "find @root\\system*";
                case Service.Undefined:
                    return string.Empty;
                default:
                    return string.Empty;
            }
        }

        private void AddRegistryService()
        {
            CommonExtensions.StartProcess("regedit", " /s " + DriverData.InstallParam.RegKeyName, 3, DriverData.InstallParam.DriverpackagePath);
            Thread.Sleep(3000);
        }

        private bool VerifyDriverUpdate()
        {
            if (!File.Exists(@"C:\Windows\System32\drivers\\" + DriverData.InstallParam.DriverBinaryName))
                return false;
            if (DriverData.InstallParam == null)
            {
                Console.WriteLine("Wrong Input");
                return false;
            }
            DateTime driverVersion = File.GetLastWriteTime(DriverData.InstallParam.DriverpackagePath + "\\" + DriverData.InstallParam.DriverBinaryName);
            DateTime installedVersion = File.GetLastWriteTime(@"C:\Windows\System32\drivers\\" + DriverData.InstallParam.DriverBinaryName);
            if (driverVersion == installedVersion)
            {
                Log.Verbose("Panel Driver time stamp is same");
                return true;
            }
            else
            {
                return false;
            }
        }
    }
}
