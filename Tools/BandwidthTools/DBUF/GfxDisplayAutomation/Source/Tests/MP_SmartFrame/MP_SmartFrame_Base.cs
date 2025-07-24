namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using Microsoft.Win32;

    class MP_SmartFrame_Base : TestBase
    {
        protected RegistryParams registryParams = new RegistryParams();
        protected string SmartFrameRegistryEvent = "SmartFrame_Enable";
        protected string SmartFrameMediaEvent = "SmartFrame_Media";

        protected void VerifySmartFrameStatus(bool enableDisable, string argSmartFrameEventName)
        {
            if (!(enableDisable))
                argSmartFrameEventName = "SmartFrame_Disable";
            PipePlaneParams pipePlaneObject = new PipePlaneParams(base.GetInternalDisplay());
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipePlaneParams.Pipe;
            eventInfo.plane = pipePlaneParams.Plane;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = argSmartFrameEventName;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                {
                    if (!CompareRegisters(driverData.output, reginfo))
                    {
                        Log.Fail("Register with offset {0} doesnot match required values", driverData.input.ToString("X"));
                    }
                    else
                    {
                        Log.Success("Register with offset {0} matches required values", driverData.input.ToString("X"));
                    }
                }
            }
        }
        protected void EnableRegistryForSF()
        {
            Log.Message(true, "Make changes in Registry to enable Smart Frame");
            registryParams.value = 1;
            registryParams.infChanges = InfChanges.ModifyInf;
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "Display_EnableSF";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        protected void EnableSF()
        {
            Log.Message(true, "Install Certificate");
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.SmartFrameApp))
            {
                Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.SmartFrameApp);
            }
            string certFileName = string.Concat(base.ApplicationManager.ApplicationSettings.SmartFrameApp, "\\certutil.exe");
            ProcessStartInfo processCert = new ProcessStartInfo(string.Concat(base.ApplicationManager.ApplicationSettings.SmartFrameApp, "\\certCmd.bat"));
            processCert.WorkingDirectory = this.ApplicationManager.ApplicationSettings.SmartFrameApp;
            processCert.CreateNoWindow = false;
            processCert.RedirectStandardOutput = true;
            processCert.UseShellExecute = false;
            Process certProcess = Process.Start(processCert);
            string msgs = certProcess.StandardOutput.ReadToEnd();
            certProcess.WaitForExit();
            if (msgs.Contains("completed successfully"))
                Log.Success("certutil.exe completed successfully");

            Log.Message("Run install.cmd");
            string filenameInstall = string.Concat(base.ApplicationManager.ApplicationSettings.SmartFrameApp, "\\install.cmd");
            ProcessStartInfo psi = new ProcessStartInfo(filenameInstall);  // Program name     
            psi.RedirectStandardOutput = true;  // Redirect msgs
            psi.CreateNoWindow = false;
            psi.UseShellExecute = false;
            Process installProcess = Process.Start(psi);
            msgs = installProcess.StandardOutput.ReadToEnd();
            installProcess.WaitForExit();
            if (msgs.Contains("ChangeServiceConfig SUCCESS"))
                Log.Success("install.cmd completed Successfully");

            Log.Message(true, "Run SFDisplay.exe /e /m=s");
            string filename = string.Concat(base.ApplicationManager.ApplicationSettings.SmartFrameApp, "\\SFDisplay.exe");
            string arguments = "/e /m=s";
            psi = new ProcessStartInfo(filename, arguments);  // Program name     
            psi.RedirectStandardOutput = true;  // Redirect msgs
            psi.CreateNoWindow = false;
            psi.UseShellExecute = false;
            Process installerProcess = Process.Start(psi);
            msgs = installerProcess.StandardOutput.ReadToEnd();
            installerProcess.WaitForExit();
            if (msgs.Contains("Operation succeeded"))
                Log.Success("SFDisplay.exe /e /m=s completed with {0}", msgs);
        }
        protected void DisableRegistryForSF()
        {
            Log.Message(true, "Make changes in Registry to disable Smart Frame");
            registryParams.value = 0;
            registryParams.infChanges = InfChanges.RevertInf;
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "Display_EnableSF";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        protected void DisableSF()
        {
            Log.Message(true, "Run SFDisplay.exe /d /m=s");
            string filename = string.Concat(base.ApplicationManager.ApplicationSettings.SmartFrameApp, "\\SFDisplay.exe");
            string arguments = "/d /m=s";
            ProcessStartInfo psi = new ProcessStartInfo(filename, arguments);  // Program name     
            psi.RedirectStandardOutput = true;  // Redirect msgs
            psi.CreateNoWindow = false;
            psi.UseShellExecute = false;
            Process installerProcess = Process.Start(psi);
            string msgs = installerProcess.StandardOutput.ReadToEnd();
            installerProcess.WaitForExit();
            if (msgs.Contains("Operation succeeded"))
                Log.Success("SFDisplay.exe /d /m=s completed with {0}", msgs);
        }

        //private bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        //{
        //    uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
        //    string binary = argDriverData.ToString("X");
        //    Log.Verbose("value from reg read in hex = {0}", binary);
        //    uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
        //    string valu = String.Format("{0:X}", hex & bit);
        //    Log.Verbose("after bitmap = {0}", valu);
        //    if (String.Equals(valu, argRegInfo.Value))
        //        return true;
        //    return false;
        //}

    }
}