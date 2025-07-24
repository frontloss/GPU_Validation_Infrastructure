namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Threading;
    using System.Collections.Generic;
    using System.Threading.Tasks;
    using System.Net.NetworkInformation;
    using System.Windows.Automation;
    using System.Xml;
    using System.Diagnostics;
    using System;

    public class WiDiDisplayConnection : FunctionalBase, ISetNoArgs
    {
        bool isNewAppFound = false;
        string app = @"C:\Program Files\Intel Corporation\Intel WiDi\WiDiApp.exe";
        string WiDiAppResourcePath = @"C:\Program Files\Intel Corporation\Intel WiDi\en\WiDiApp.resources.dll";
        public bool SetNoArgs()
        {
            Log.Message("Connecting WiDi Display.... it will take some time to connect");
            if (base.MachineInfo.OS.Type == OSType.WINBLUE)
            {
                if (AddWirelessDisplay.ScanNAddWirelessDisplayDevice(base.EnumeratedDisplays.Count))
                    return true;
                Log.Verbose("Launch projector to connect WIDI display");
                LaunchProjector projector = new LaunchProjector();
                return projector.SetWiDiDisplayAdapter();
            }
            else
            {
                KillProcess("WiDiApp");
                if (!Directory.Exists(AppSettings.WIDiAppPath))
                    Log.Abort("WiDi APP not found in {0}", AppSettings.WIDiAppPath);
                InstallApplication();
                if (File.Exists(app))
                {
                    if (AppConnection(app, isNewAppFound))
                    {
                        Log.Message("Successfully connected to WiDi display");
                        return true;
                    }
                    else
                    {
                        KillProcess("WiDiApp");
                        Log.Verbose("Unable to connect, trying again...");
                        if (AppConnection(app, isNewAppFound, 50))
                        {
                            Log.Message("Successfully connected to WiDi display");
                            return true;
                        }
                        else
                            Log.Fail("Unable to connect WiDi display");
                    }
                }
                else
                    Log.Abort("WiDi app is not installed in test system");
            }
            return false;
        }

        private bool AppConnection(string app, bool isNewApp, int time = 35)
        {
            GetMonitorList monList = new GetMonitorList();
            List<uint> currentMonList = monList.ListofActiveMonitor();
            CommonExtensions.StartProcess(app, string.Empty, time);
            if (isNewApp)
            {
                WiDiAPPInstaller installer = new WiDiAPPInstaller();
                installer.LicenseAgrement();
            }  
            List<uint> newMonList = monList.ListofActiveMonitor();
            if (newMonList.Count > currentMonList.Count)
                return true;
            return false;
        }
        private void InstallApplication()
        {
            string path = string.Empty;
            foreach (string appPath in Directory.GetFiles(AppSettings.WIDiAppPath))
            {
                if (base.MachineInfo.OS.Architecture.Contains("64") && appPath.ToLower().Contains("x64app"))
                {
                    path = appPath;
                    break;
                }
                else
                    path = appPath;
            }
            if (File.Exists(WiDiAppResourcePath))
            {
                if (!path.Contains(GetWiDiAppVersion()))
                {
                    Log.Verbose("Installing WiDi application to run the test");
                    Log.Verbose("Running WiDi app from {0}", path);
                    CommonExtensions.StartProcess(path, string.Empty, 50);
                    WiDiAPPInstaller installer = new WiDiAPPInstaller();
                    if (installer.Install())
                        Log.Message("Installation complete");
                    else
                        Log.Abort("Installation failed");
                    isNewAppFound = true;
                    Log.Verbose("WiDi App version is {0}", GetWiDiAppVersion());
                }
                else
                    Log.Message("WIDI App with same version {0} already installed in test system", GetWiDiAppVersion());
            }
            else
                Log.Abort("Please mannually connect once to give the security key");

        }
        private string GetWiDiAppVersion()
        {
            var versionInfo = FileVersionInfo.GetVersionInfo(WiDiAppResourcePath);
            return versionInfo.ProductVersion;
        }
        private bool GetWLANStatus()
        {
            Thread.Sleep(2000);
            bool status = false;
            NetworkInterface[] nic = NetworkInterface.GetAllNetworkInterfaces();
            foreach (NetworkInterface adapter in nic)
            {
                if (NetworkInterfaceType.Wireless80211 == adapter.NetworkInterfaceType
                    && adapter.OperationalStatus == OperationalStatus.Up)
                {
                    status = true;
                    break;
                }
            }
            return status;
        }
        private void KillProcess(string processName)
        {
            Process[] processList = Process.GetProcessesByName(processName);
            if (processList.Length >= 1)
            {
                Log.Verbose("Found {0} WiDi app running in test system", processList.Length);
            }
            foreach (Process eachProcess in processList)
            {
                eachProcess.Kill();
                Log.Verbose("Exiting from {0} process successfully", processName);
                Thread.Sleep(8000);
            }
        }
    }
}
