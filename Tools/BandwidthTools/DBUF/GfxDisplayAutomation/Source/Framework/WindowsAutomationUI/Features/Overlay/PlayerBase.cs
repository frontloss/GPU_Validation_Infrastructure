namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;
    internal abstract class PlayerBase
    {
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll", SetLastError= true, CallingConvention= CallingConvention.StdCall)]
        private static extern IntPtr MoveWindow(IntPtr handle, int x, int y, int width, int height, bool rePaint);
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool GetWindowRect(IntPtr hwnd, ref Rect rectangle);

        internal OverlayParams OverlayParams { get; set; }
        internal Func<DisplayType, DisplayMode> GetMode { get; set; }

        internal IApplicationSettings AppSettings = null;
        internal int CurrMethodIdx = -1;

        internal virtual void Close(Process argProcess)
        {
            if (null != argProcess)
            {
                Log.Verbose("Closing {0}", this.OverlayParams.Player);
				
				try
				{
					argProcess.Kill();
				}
				catch(Exception e)
				{
					Log.Alert("Fail to close Overlay Player : {0}",e.Message);
					Log.Alert("{0}",e.StackTrace);
					
					Thread.Sleep(5000);
					argProcess.Kill();
				}
					
            }
        }
        internal virtual void Play(Process argProcess)
        {
            this.SetWindowFocus(argProcess);
            Thread.Sleep(1000);
            Log.Verbose("Running {0}", this.OverlayParams.VideoFile);
            argProcess.StartInfo.Arguments = string.Format("{0}\\{1}", this.AppSettings.DisplayToolsPath, this.OverlayParams.VideoFile);
            this.CheckVideoFileExists();
            argProcess.Start();
        }
        internal virtual void Pause(Process argProcess)
        {
            this.SetWindowFocus(argProcess);
            Thread.Sleep(1000);
            Log.Verbose("Pausing {0}", this.OverlayParams.VideoFile);
            SendKeys.SendWait("{Space}");
        }
        internal abstract void Stop(Process argProcess);
        internal virtual void ChangeFormat(Process argProcess)
        {
            this.SetWindowFocus(argProcess);
        }
        internal virtual void Move(Process argProcess)
        {
            Rect appRect = new Rect();
            int displayHierarchyType = (int)this.OverlayParams.DisplayHierarchy;
            DisplayType display = this.OverlayParams.CurrentConfig.CustomDisplayList.ElementAt((int)this.OverlayParams.DisplayHierarchy);
            DisplayMode mode = this.GetMode(display);
            uint left = (mode.HzRes / 4);
            for (int i = 0; i < displayHierarchyType; i++)
                left += this.GetMode(this.OverlayParams.CurrentConfig.CustomDisplayList.ElementAt(i)).HzRes;
            Log.Verbose("Moving player to {0}x{1} for {2} - {3}", left, ((int)mode.VtRes / 2), this.OverlayParams.DisplayHierarchy, display);
            this.SetWindowFocus(argProcess);
            GetWindowRect(argProcess.MainWindowHandle, ref appRect);
            MoveWindow(argProcess.MainWindowHandle, (int)left, ((int)mode.VtRes / 4), (appRect.Right - appRect.Left), (appRect.Bottom - appRect.Top), false);
        }
        internal virtual void Maximize(Process argProcess)
        {
            this.PlayerWindowOptions(argProcess, CUIWindowOptions.Maximize);
        }
        internal virtual void Minimize(Process argProcess)
        {
            this.PlayerWindowOptions(argProcess, CUIWindowOptions.Minimize);
        }
        internal virtual void Restore(Process argProcess)
        {
            this.PlayerWindowOptions(argProcess, CUIWindowOptions.Restore);
            Thread.Sleep(1000);
            SendKeys.SendWait("{Escape}");
        }
        internal abstract void FullScreen(Process argProcess);
        internal abstract Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx);

        protected void SetWindowFocus(Process argProcess)
        {
            Thread.Sleep(1000);
            Log.Verbose("Bringing {0} to focus", this.OverlayParams.Player);
            SetForegroundWindow(argProcess.MainWindowHandle);
        }
        protected void StopPlayback(Process argProcess, string argKey)
        {
            this.SetWindowFocus(argProcess);
            Thread.Sleep(1000);
            Log.Verbose("Stopping playback on {0}", this.OverlayParams.VideoFile);
            SendKeys.SendWait(argKey);
        }
        protected void FullScreenPlayback(Process argProcess, string argKey)
        {
            this.SetWindowFocus(argProcess);
            Thread.Sleep(1000);
            Log.Verbose("Running {0} in FullScreen mode", this.OverlayParams.VideoFile);
            SendKeys.SendWait(argKey);
        }
        protected bool IsMoveApplicable()
        {
            if (!((int)this.OverlayParams.DisplayHierarchy > 0 && this.OverlayParams.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended))
            {
                Log.Verbose("Not moving player for {0} - {1}", this.OverlayParams.DisplayHierarchy, this.OverlayParams.CurrentConfig.ConfigType);
                return false;
            }
            return true;
        }
        protected void CheckVideoFileExists(string argFileName)
        {
            if (!File.Exists(argFileName))
                Log.Abort("{0} does not exist!", argFileName);
        }

        private void CheckVideoFileExists()
        {
            this.CheckVideoFileExists(string.Format("{0}\\{1}", this.AppSettings.DisplayToolsPath, this.OverlayParams.VideoFile));
        }
        private void PlayerWindowOptions(Process argProcess, CUIWindowOptions argOption)
        {
            Log.Verbose("{0} {1}", argOption, this.OverlayParams.Player);
            ShowWindowAsync(argProcess.MainWindowHandle, (int)argOption);
        }
    }
}