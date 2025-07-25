﻿namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.IO;
    using System.Threading;
    using System.Text.RegularExpressions;
    using System.Collections.Generic;
    using System.Diagnostics;

    internal class SocWatch : FunctionalBase,ISetMethod
    {
        private const int WM_COMMAND = 0x111;
        private const int MIN_ALL = 419;
        private const int MIN_ALL_UNDO = 416;
        private static Process SocWatchProcess;

        public bool SetMethod(object argMessage)
        {
            CSParam PowerParam = argMessage as CSParam;
            if (PowerParam == null || string.IsNullOrEmpty(PowerParam.Command))
            {
                Log.Fail("Command line parameter is not specified to run SocWatch Application.");
                return false;
            }
            IntPtr LhWND = Interop.FindWindow("Shell_TrayWnd", null);
            Interop.SendMessage(LhWND, WM_COMMAND, (IntPtr)MIN_ALL, IntPtr.Zero);
            string SocWatchApp = string.Concat(base.AppSettings.DisplayToolsPath, @"\SocWatch\socwatch.exe");
            if (!File.Exists(SocWatchApp))
            {
                Log.Abort("Unable to find SocWatch Application in {0}.", SocWatchApp);
            }            
            CleanupLogFile();
            int resumetime = PowerParam.Delay + 5;
            Log.Message("Running SocWatch Application with command: {0} for platform {1}", PowerParam.Command, base.AppManager.MachineInfo.PlatformDetails.Platform);
            SocWatchProcess = CommonExtensions.StartProcess(SocWatchApp, PowerParam.Command, resumetime);
            return true;
        }

        internal bool GetCPUState(CPU_C_STATE state)
        {
            // Read CSV file generated by SocWatch
            SocWatchProcess.WaitForExit();
            if(!File.Exists("CPUStateLogger.csv"))
            {
                Log.Fail("CPUStateLogger.csv file not present to parse CPU State");
                return false;
            }
            string[] lines = File.ReadAllLines("CPUStateLogger.csv");
            string[] container = lines.Where(pkgStr => pkgStr.Contains(state.ToString())).FirstOrDefault().Split(new[] { ',', '\t' });
            if (container == null)
                Log.Verbose("CPU has't entered into {0} state. ", state.ToString());
            else
            {
                string[] resValues = container[1].Split('%');
                string cStateValue = resValues[0].Trim();
                if (Convert.ToDouble(cStateValue) == 0)
                    Log.Verbose("CPU {0} recedency value is: 0", state.ToString());
                else
                {
                    Log.Verbose("CPU entered into {0} state, and recedency value is: {1}", state.ToString(), cStateValue);
                    return true;
                }
            }
            IntPtr LhWND = Interop.FindWindow("Shell_TrayWnd", null);
            Interop.SendMessage(LhWND, WM_COMMAND, (IntPtr)MIN_ALL_UNDO, IntPtr.Zero);
            return false;            
        }

        private void CleanupLogFile()
        {
            List<string> fileInfos = new List<string>();
            List<string> searchPattern = new List<string> { "*.csv", "*.wpf", "*.etl" };
            foreach (string eachSearchString in searchPattern)
            {
                fileInfos.AddRange(Directory.EnumerateFiles(Directory.GetCurrentDirectory(), eachSearchString).ToList());
            }
            foreach (string file in fileInfos)
                File.Delete(file);
        }  
    }
}
