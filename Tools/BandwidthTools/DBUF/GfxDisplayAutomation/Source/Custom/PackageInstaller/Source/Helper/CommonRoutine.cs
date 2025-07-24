using System;
using System.Diagnostics;
using System.Threading;
using System.IO;
using System.Management;

namespace PackageInstaller
{
    public static class CommonRoutine
    {
        private static string XPath = string.Empty;
        public static Process StartProcess(string argFileName)
        {
            return StartProcess(argFileName, null);
        }
        public static Process StartProcess(string argFileName, string arguments)
        {
            return StartProcess(argFileName, arguments, null);
        }
        public static Process StartProcess(string argFileName, string arguments, string argWorkingDir)
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
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();
            return process;
        }
        public static void Wait(int timeInSec)
        {
            Log.Messege("Wait for {0} sec", timeInSec);
            Thread.Sleep(1000 * timeInSec);
        }
        public static void Exit(ErrorCode exitCode)
        {
            Log.Messege("Exit Code {0}", (int)exitCode);
            CommonRoutine.ClearRebootFile();
            Environment.Exit((int)exitCode);
        }
        public static void Reboot()
        {
            Log.Messege("Rebooting System...");
            File.Create("Reboot.txt");
            Process process = CommonRoutine.StartProcess("shutdown", string.Format("/f /r /t 5"));
            process.WaitForExit();
            Thread.Sleep(60000);
        }
        public static bool IsSystemRebooted()
        {
            return File.Exists("Reboot.txt");
        }
        public static void ClearRebootFile()
        {
            File.Delete("Reboot.txt");
        }

        public static string GetWin32Value(string argColumn, string argQuery)
        {
            string outputString = string.Empty;
            ObjectQuery mgmtQuery = new ObjectQuery(argQuery);
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(mgmtQuery);
            ManagementObjectCollection queryCollection = searcher.Get();
            if (queryCollection.Count != 0)//workaround kept after discussing with vijayan regarding BIOS version not populated for CHV.
            {
                Object value = new Object();
                foreach (ManagementObject obj in queryCollection)
                    value = obj[argColumn];
                searcher.Dispose();
                queryCollection.Dispose();
                outputString = (null == value) ? string.Empty : value.ToString();
            }
            else
                Log.Fail("queryCollection for query {0} is zero", argColumn);

            return outputString;
        }
    }
}
