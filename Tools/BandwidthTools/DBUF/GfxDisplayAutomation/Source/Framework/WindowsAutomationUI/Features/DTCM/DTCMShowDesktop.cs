namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Windows.Automation;
    using System.Threading;
    using System.Runtime.InteropServices;

    class DTCMShowDesktop : FunctionalBase, ISet
    {
        bool retryAttemptSet = false;
        [DllImport("user32.dll")]
        static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll")]
        public static extern bool SetCursorPos(int x, int y);
        [DllImport("user32.dll")]
        public static extern bool mouse_event(int dwFlags, int dx, int dy, int cButtons, int dwExtraInfo);
        [DllImport("user32.dll")]
        private static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);
        private const int KEYEVENTF_EXTENDEDKEY = 1;
        private const int KEYEVENTF_KEYUP = 2;
        public const int MOUSEEVENTF_LEFTDOWN = 0x02;
        public const int MOUSEEVENTF_LEFTUP = 0x04;
        public object Set
        {
            set
            {
                Log.Verbose("In DTCMShowDesktop Set (Windows Automation UI)");
                const int FORCE_MINIMIZE = 11;
                CUIHeaderOptions cuiHeaderOptions = new CUIHeaderOptions();
                cuiHeaderOptions.Set = CUIWindowOptions.Minimize;
                Process.GetProcesses()
                    .Where(p => p.ProcessName.ToLower().Contains("cmd") || p.ProcessName.ToLower().Contains("execute"))
                    .ToList()
                    .ForEach(p => ShowWindowAsync(p.MainWindowHandle, FORCE_MINIMIZE));

                Log.Verbose("Launching DTCM menu");
                KeyDown(Keys.LWin);
                KeyUp(Keys.LWin);
                KeyDown(Keys.LWin);
                KeyUp(Keys.LWin);
                Thread.Sleep(2000);
                int xPos = Screen.PrimaryScreen.Bounds.Width / 2;
                int yPos = Screen.PrimaryScreen.Bounds.Height / 8;
                Log.Verbose("XxY:: {0}x{1}", xPos, yPos);
                SetCursorPos(xPos, yPos);
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                SendKeys.SendWait("+{F10}");
                Thread.Sleep(2000);
                AutomationElement element = UIABaseHandler.SelectElementNameControlType("View", ControlType.MenuItem);
                if (element == null)
                {
                    Log.Sporadic("Retry launcing DTCM Menu Attempt {0}", this.retryAttemptSet);
                    if (!this.retryAttemptSet)
                    {
                        this.retryAttemptSet = true;
                        Log.Verbose("Launching AutoIt Notepad to skip metro!");
                        CommonExtensions.StartProcess("AutoIt3.exe", "GoToDesktop.au3");
                        Log.Verbose("Performing DTCM menu launch again!");
                        this.Set = "LAUNCHAGAIN!";
                    }
                }
            }      
        }
        private static void KeyDown(Keys vKey)
        {
            keybd_event((byte)vKey, 0, KEYEVENTF_EXTENDEDKEY, 0);
        }
        private static void KeyUp(Keys vKey)
        {
            keybd_event((byte)vKey, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0);
        }
    }
}