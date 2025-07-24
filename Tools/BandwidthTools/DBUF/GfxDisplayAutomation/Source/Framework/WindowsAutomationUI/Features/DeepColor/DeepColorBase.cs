namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;

    internal abstract class DeepColorBase
    {
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll", SetLastError= true, CallingConvention= CallingConvention.StdCall)]
        private static extern IntPtr MoveWindow(IntPtr handle, int x, int y, int width, int height, bool rePaint);
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool GetWindowRect(IntPtr hwnd, ref Rect rectangle);

        internal DeepColorParams DeepcolorParams { get; set; }
        internal Func<DisplayType, DisplayMode> GetMode { get; set; }

        internal IApplicationSettings AppSettings = null;
        internal int CurrMethodIdx = -1;

        internal virtual void Close(Process argProcess)
        {
            if (null != argProcess)
            {
                Log.Verbose("Closing {0}", this.DeepcolorParams.DeepColorApplication);
                argProcess.Kill();
            }
        }
        
        internal virtual void Move(Process argProcess)
        {
            Rect appRect = new Rect();
            int displayHierarchyType = (int)this.DeepcolorParams.DisplayHierarchy;
            DisplayType display = this.DeepcolorParams.CurrentConfig.CustomDisplayList.ElementAt((int)this.DeepcolorParams.DisplayHierarchy);
            DisplayMode mode = this.GetMode(display);
            uint left = (mode.HzRes / 4);
            for (int i = 0; i < displayHierarchyType; i++)
                left += this.GetMode(this.DeepcolorParams.CurrentConfig.CustomDisplayList.ElementAt(i)).HzRes;
            Log.Verbose("Moving Applciation to {0}x{1} for {2} - {3}", left, ((int)mode.VtRes / 2), this.DeepcolorParams.DisplayHierarchy, display);
            this.SetWindowFocus(argProcess);
            GetWindowRect(argProcess.MainWindowHandle, ref appRect);
            MoveWindow(argProcess.MainWindowHandle, (int)left, ((int)mode.VtRes / 4), (appRect.Right - appRect.Left), (appRect.Bottom - appRect.Top), false);
        }
        
        internal abstract Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx);

        internal virtual void EnableDeepColor(Process argProcess)
        {
            Log.Verbose("Enabling DeepColor");
            FullScreen(argProcess);
        }

        internal virtual void DisableDeepColor(Process argProcess)
        {
            Log.Verbose("Disabling DeepColor");
            FullScreen(argProcess);
        }
        private void SetWindowFocus(Process argProcess)
        {
            Thread.Sleep(1000);
            Log.Verbose("Bringing {0} to focus", this.DeepcolorParams.DeepColorApplication);
            SetForegroundWindow(argProcess.MainWindowHandle);
        }
        
        private void FullScreen(Process argProcess)
        {
            this.SetWindowFocus(argProcess);
            Thread.Sleep(2000);
            Log.Verbose("Clicking Alt+Enter for {0}", this.DeepcolorParams.DeepColorApplication);
            SendKeys.SendWait("%{ENTER}");
        }
        protected bool IsMoveApplicable()
        {
            if (this.DeepcolorParams.CurrentConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Extended)
            {
                Log.Verbose("Not moving DeepColor Application for {0} - {1}", this.DeepcolorParams.DisplayHierarchy, this.DeepcolorParams.CurrentConfig.ConfigType);
                return false;
            }
            return true;
        }

    }
}