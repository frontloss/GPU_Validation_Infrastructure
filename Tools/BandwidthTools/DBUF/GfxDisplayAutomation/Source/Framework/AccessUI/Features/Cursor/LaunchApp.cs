namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;
    using System.Drawing;

    using Ranorex;

    public class LaunchApp : FunctionalBase, ISetMethod, IGetMethod
    {
        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool GetWindowRect(IntPtr hwnd, ref Rect rectangle);

        [DllImport("user32.dll")]
        public static extern IntPtr SetWindowPos(IntPtr hwnd, int hwndInsertAfter, int x, int y, int cx, int cy, int wFlags);

        [DllImport("user32.dll")]
        public static extern IntPtr FindWindowEx(IntPtr parentHandle, IntPtr childAfter, string lClassName, string windowTitle);

        public bool SetMethod(object argMessage)
        {
            string processName = (string)argMessage;
            Log.Message("Kill any instance of process {0}", processName);
            foreach (Process proc in Process.GetProcessesByName(processName))
                proc.Kill();           
            Log.Message("Launch {0}", processName);
            Process app = Process.Start(new ProcessStartInfo(processName));
            app.WaitForInputIdle();
            Process[] process = Process.GetProcessesByName(processName);
            if (process.Count() != 0)
                return true;
            else
                return false;
        }
        public object GetMethod(object argMessage)
        {
            uint left = 0;
            AppDetail appDetail = argMessage as AppDetail;
            
            Rect AppRect = new Rect();
            Rect EditRect = new Rect();
            AppHandle appHandle = new AppHandle();
           
            if ((appDetail.handle == (IntPtr)null) && (appDetail.className == null))
            {
                DisplayHierarchy dH = appDetail.displayHierarchy;
                DisplayConfig displayconfig = appDetail.displayConfig;
                DisplayUnifiedConfig unifiedConfigType = DisplayExtensions.GetUnifiedConfig(displayconfig.ConfigType);

                Process[] processes = Process.GetProcessesByName(appDetail.processName);
                Process process = processes[0];
                process.WaitForInputIdle();

                Log.Verbose("Get the coordinates of app..");
                if (process.MainWindowHandle == (IntPtr)null)
                    Log.Fail("MainWindowHandle is showing null");
                else
                    Log.Message("MainWindowHandle is {0}", process.MainWindowHandle);
                GetWindowRect(process.MainWindowHandle, ref AppRect);

                Log.Message("Resizing window of app");
                SetWindowPos(process.MainWindowHandle, 0, 10, 10, 400, 400, 0);

                int displayHierarchyType = (int)Convert.ChangeType(dH, dH.GetTypeCode());
                if ((displayHierarchyType > 1) && (unifiedConfigType == DisplayUnifiedConfig.Extended))
                {
                    for (int i = 0; i < displayHierarchyType ; i++)
                    {
                        left += base.GetDisplayModeByDisplayType(displayconfig.CustomDisplayList.ElementAt(i)).HzRes;
                    }
                    SetWindowPos(process.MainWindowHandle, 0, 10 + (int)left, 10, 400, 400, 0);
                }
                GetWindowRect(process.MainWindowHandle, ref AppRect);
                appHandle.handle = process.MainWindowHandle;
                appHandle.rectCoordinate = AppRect;
                return (object)appHandle;
            }
            else
            {
                Log.Message("Get the coordinates of {0} ", appDetail.className);
                IntPtr editHandle = FindWindowEx(appDetail.handle, IntPtr.Zero, appDetail.className, "");
                Log.Message("edit handle = {0} ", editHandle);
                GetWindowRect(editHandle, ref EditRect);
                appHandle.handle = editHandle;
                appHandle.rectCoordinate = EditRect;
                return (object)appHandle;
            }
        }      
    }
}
