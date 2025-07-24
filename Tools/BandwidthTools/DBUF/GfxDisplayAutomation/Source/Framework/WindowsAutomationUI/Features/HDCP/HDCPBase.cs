namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;

    internal abstract class HDCPBase
    {
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll", SetLastError= true, CallingConvention= CallingConvention.StdCall)]
        private static extern IntPtr MoveWindow(IntPtr handle, int x, int y, int width, int height, bool rePaint);
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool GetWindowRect(IntPtr hwnd, ref Rect rectangle);

        internal HDCPParams HDCPParams { get; set; }
        internal Func<DisplayType, DisplayMode> GetMode { get; set; }
        internal IApplicationSettings AppSettings = null;

        internal abstract Process Instance(HDCPPlayerInstance HDCPPlayerInstance);
        internal abstract void ActivateHDCP(Process argProcess);
        internal abstract void DeactivateHDCP(Process argProcess);
        internal abstract void QueryGlobalProtectionLevel(Process argProcess);
        internal abstract void QueryLocalProtectionLevel(Process argProcess);
        internal abstract void SetSRM(Process argProcess);
        internal abstract void GetSRMVersion(Process argProcess);
        internal abstract void ActivateACP(Process argProcess);
        internal abstract void ActivateCGMSA(Process argProcess);

        internal virtual void Close(Process argProcess)
        {
            if (null != argProcess)
            {
                Log.Verbose("Closing {0}", this.HDCPParams.HDCPAppName);
                argProcess.Kill();
            }
        }
        internal virtual void Move(Process argProcess)
        {
            Rect appRect = new Rect();
            int displayHierarchyType = (int)this.HDCPParams.DisplayHierarchy;
            DisplayType display = this.HDCPParams.CurrentConfig.CustomDisplayList.ElementAt((int)this.HDCPParams.DisplayHierarchy);
            DisplayMode mode = this.GetMode(display);
            uint left = (mode.HzRes / 4);
            for (int i = 0; i < displayHierarchyType; i++)
                left += this.GetMode(this.HDCPParams.CurrentConfig.CustomDisplayList.ElementAt(i)).HzRes;
            Log.Verbose("Moving Application to {0}x{1} for {2} - {3}", left, ((int)mode.VtRes / 2), this.HDCPParams.DisplayHierarchy, display);
            this.SetWindowFocus(argProcess);
            GetWindowRect(argProcess.MainWindowHandle, ref appRect);
            MoveWindow(argProcess.MainWindowHandle, (int)left, ((int)mode.VtRes / 4), (appRect.Right - appRect.Left), (appRect.Bottom - appRect.Top), false);
        }
        protected void SetWindowFocus(Process argProcess)
        {
            Thread.Sleep(1000);
            Log.Verbose("Bringing {0} to focus", this.HDCPParams.HDCPAppName);
            SetForegroundWindow(argProcess.MainWindowHandle);
        }
        protected bool IsMoveApplicable()
        {
            if (this.HDCPParams.CurrentConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Extended)
            {
                Log.Verbose("Not moving HDCP Application for {0} - {1}", this.HDCPParams.DisplayHierarchy, this.HDCPParams.CurrentConfig.ConfigType);
                return false;
            }
            return true;
        }

    }
}