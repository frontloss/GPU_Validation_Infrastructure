namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.Text;
    using System.Text.RegularExpressions;
    using System.Threading;
    using System.Threading.Tasks;
    using System.Windows.Forms;
    using System.Runtime.InteropServices;

    internal class LaunchProjector
    {
        List<uint> monID;
        List<int> tabCountList;
        GetMonitorList monList = new GetMonitorList();
        private List<KeyCode> listKeyCode = new List<KeyCode>();
        KeyPress keyPress = new KeyPress();
        [DllImport("user32.dll")]
        private static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);
        private const int KEYEVENTF_EXTENDEDKEY = 1;
        private const int KEYEVENTF_KEYUP = 2;

        public bool SetWiDiDisplayAdapter()
        {
            tabCountList = new List<int>();
            monID = monList.ListofActiveMonitor();
            Log.Verbose("No of display device connected is {0} ", monID.Count());
            if (monID.Count() > 1)
            {
                tabCountList.Add(4);
                tabCountList.Add(2);
            }
            else
            {
                tabCountList.Add(2);
                tabCountList.Add(2);
            }
            return MuxLaunchDispProjector();
        }
        internal void LaunchDispProjector()
        {
            Log.Verbose("In LaunchProjector (Windows Automation UI)");
            Log.Verbose("Sending WinP+ shift + ctrl + F21 command");
            listKeyCode.Add(KeyCode.LWIN);
            listKeyCode.Add(KeyCode.SHIFT);
            listKeyCode.Add(KeyCode.CONTROL);
            listKeyCode.Add(KeyCode.F21);
            keyPress.SetMethod(listKeyCode);
            Thread.Sleep(1000);
        }
        private void Tab()
        {
            Log.Verbose("Sending TAB command");
            SendKeys.SendWait("{TAB}");
            Thread.Sleep(1000);
        }
        public void Enter()
        {
            Log.Verbose("Sending Enter command");
            SendKeys.SendWait("~");
            Thread.Sleep(1000);
        }

        public void PressTab(int tabCount)
        {
            for (int idx = 0; idx < tabCount; idx++)
            {
                this.Tab();
                Thread.Sleep(1000);
            }
        }

        private bool MuxLaunchDispProjector()
        {
            int widiDeviceCount = 0;
            LaunchDispProjector();
            if (monID.Count == 1)
                PressTab(1);
            else 
                PressTab(tabCountList.First());
            this.Enter();
            if (monID.Count == 1)
                Thread.Sleep(20000);
            Thread.Sleep(2000);
            Process monitorID_process = CommonExtensions.StartProcess("devcon.exe", "find = port *miracast*", 4);
            while (!monitorID_process.StandardOutput.EndOfStream)
            {
                string line = monitorID_process.StandardOutput.ReadLine().ToLower();
                if (line.Contains(":"))
                {
                    widiDeviceCount++;
                }
            }
            if (widiDeviceCount > 1)
            {
                Log.Abort("Multiple WiDi display found please remove one and run the test");
            }
            if (monID.Count > 1)
            {
                Enter();
                Thread.Sleep(20000);
            }
            if (VerifyWiDiMonitor())
                return true;
            else
            {
                if (monID.Count > 1)
                {
                    PressTab(tabCountList[0]);
                    Enter();
                    PressTab(tabCountList[1]);
                    Enter();
                }
                else
                {
                    PressTab(tabCountList.Last());
                    this.Enter();
                }
                Thread.Sleep(20000);
                return VerifyWiDiMonitor();
            }
        }

        private bool VerifyWiDiMonitor()
        {
            List<uint> nextmonID = monList.ListofActiveMonitor();
            if (nextmonID.Count > monID.Count)
                return true;
            return false;
        }

        public static void KeyDown(Keys vKey)
        {
            keybd_event((byte)vKey, 0, KEYEVENTF_EXTENDEDKEY, 0);
        }

        private static void KeyUp(Keys vKey)
        {
            keybd_event((byte)vKey, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0);
        }
    }
}
