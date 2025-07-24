namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Runtime.InteropServices;

    using Ranorex;

    class DTCMShowDesktop : FunctionalBase, ISet
    {
        bool retryAttemptSet = false;
        [DllImport("user32.dll")]
        static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);

        public object Set
        {
            set
            {
                const int FORCE_MINIMIZE = 11;
                CUIHeaderOptions cuiHeaderOptions = new CUIHeaderOptions();
                cuiHeaderOptions.Set = CUIWindowOptions.Minimize;
                Process.GetProcesses()
                    .Where(p => p.ProcessName.ToLower().Contains("cmd") || p.ProcessName.ToLower().Contains("execute"))
                    .ToList()
                    .ForEach(p => ShowWindowAsync(p.MainWindowHandle, FORCE_MINIMIZE));

                Log.Verbose("Launching DTCM menu");
                Keyboard.Press("{LWin down}d{LWin up}");
                Delay.Seconds(2);
                int xPos = Screen.PrimaryScreen.Bounds.Width / 2;
                int yPos = Screen.PrimaryScreen.Bounds.Height / 8;
                Log.Verbose("XxY:: {0}x{1}", xPos, yPos);
                Mouse.MoveTo(xPos, yPos);
                Mouse.ButtonDown(MouseButtons.Left);
                Mouse.ButtonUp(MouseButtons.Left);
                Keyboard.Press("{LShiftKey down}{F10}{LShiftKey up}");
                Delay.Seconds(2);

                try
                {
                    if (DTCMRepo.Instance.ContextMenuExplorer.Self.Visible)
                        Log.Verbose("Context menu is visible!");
                }
                catch (Exception ex)
                {
                    Log.Sporadic("{0}{1}Retry Attempt {2}", ex.Message, Environment.NewLine, this.retryAttemptSet);
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
    }
}