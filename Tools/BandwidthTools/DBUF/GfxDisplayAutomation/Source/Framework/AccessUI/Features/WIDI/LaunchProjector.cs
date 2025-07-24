namespace Intel.VPG.Display.Automation
{
    using Ranorex;
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.Text;
    using System.Text.RegularExpressions;
    using System.Threading;
    using System.Threading.Tasks;
    using System.Windows.Forms;

    internal class LaunchProjector
    {
        List<uint> monID;
        GetMonitorList monList = new GetMonitorList();
        public bool SetWiDiDisplayAdapter()
        {
            monID = monList.ListofActiveMonitor();
            if (monID.Count > 1)
            {
                return MuxLaunchDispProjector();
            }
            else
            {
                LaunchDispProjector();
                Enter();
                Thread.Sleep(10000);
                List<uint> nextmonID = monList.ListofActiveMonitor();
                if (nextmonID.Count > monID.Count)
                    return true;
                else
                {
                    if (Retry())
                        return true;
                }
            }
            return false;
        }
        internal void LaunchDispProjector()
        {
            Log.Verbose("Sending WinP+ shift + ctrl + F21 command");
            Keyboard.Press("{LWin down}");
            Keyboard.Press("{ShiftKey down}");
            Keyboard.Press("{ControlKey down}");
            Keyboard.Press("{F21 down}");
            Keyboard.Press("{F21 up}");
            Keyboard.Press("{ControlKey up}");
            Keyboard.Press("{ShiftKey up}");
            Keyboard.Press("{LWin up}");
            Thread.Sleep(1000);
        }
        private void Tab()
        {
            Log.Verbose("Sending TAB command");
            SendKeys.SendWait("{TAB}");
            Thread.Sleep(1000);
        }
        private void Enter()
        {
            Log.Verbose("Sending Enter command");
            SendKeys.SendWait("~");
            Thread.Sleep(1000);
        }

        private bool Retry()
        {
            PressTab(4);
            Enter();
            PressTab(2);
            Enter();
            Thread.Sleep(10000);
            List<uint> nextmonID = monList.ListofActiveMonitor();
            if (nextmonID.Count > monID.Count)
                return true;
            else
                return false;
        }

        private void PressTab(int tabCount)
        {
            for (int idx = 0; idx < tabCount; idx++)
            {
                this.Tab();
                Thread.Sleep(1000);
            }
        }

        private bool MuxLaunchDispProjector()
        {
            int tabCount = 0;
            LaunchDispProjector();
            PressTab(4);
            this.Enter();
            Thread.Sleep(4000);
            Process monitorID_process = CommonExtensions.StartProcess("devcon.exe", "find = port *miracast*");
            while (!monitorID_process.StandardOutput.EndOfStream)
            {
                string line = monitorID_process.StandardOutput.ReadLine().ToLower();
                if (line.Contains(":"))
                {
                    tabCount++;
                }
            }
            if (tabCount > 1)
            {
                Log.Abort("Multiple WiDi display found please remove one and run the test");
            }
            Enter();
            Thread.Sleep(20000);
            List<uint> nextmonID = monList.ListofActiveMonitor();
            if (nextmonID.Count > monID.Count)
                return true;
            else
            {
                if (Retry())
                    return true;
            }
            return false;
        }
    }
}
