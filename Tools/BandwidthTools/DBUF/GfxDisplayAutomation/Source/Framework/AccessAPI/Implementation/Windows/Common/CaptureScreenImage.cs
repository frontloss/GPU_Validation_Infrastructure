namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Drawing;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Drawing.Imaging;
    using System.Runtime.InteropServices;
    using System.IO;
    using System.Collections.Generic;

    class CaptureScreenImage : FunctionalBase, IGet
    {
        // P/Invoke declarations
        [DllImport("gdi32.dll")]
        static extern bool BitBlt(IntPtr hdcDest, int xDest, int yDest, int
        wDest, int hDest, IntPtr hdcSource, int xSrc, int ySrc, CopyPixelOperation rop);
        [DllImport("user32.dll")]
        static extern bool ReleaseDC(IntPtr hWnd, IntPtr hDc);
        [DllImport("gdi32.dll")]
        static extern IntPtr DeleteDC(IntPtr hDc);
        [DllImport("gdi32.dll")]
        static extern IntPtr DeleteObject(IntPtr hDc);
        [DllImport("gdi32.dll")]
        static extern IntPtr CreateCompatibleBitmap(IntPtr hdc, int nWidth, int nHeight);
        [DllImport("gdi32.dll")]
        static extern IntPtr CreateCompatibleDC(IntPtr hdc);
        [DllImport("gdi32.dll")]
        static extern IntPtr SelectObject(IntPtr hdc, IntPtr bmp);
        [DllImport("user32.dll")]
        public static extern IntPtr GetDesktopWindow();
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindowDC(IntPtr ptr);
        [DllImport("user32.dll")]
        static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        public object Get
        {
            get
            {
                string filename;
                int width = 0;
                int height = 0;
                const int FORCE_MINIMIZE = 11;
                const int SW_RESTORE = 9;
                List<Process> RunningProcesses = Process.GetProcesses().Where(p => p.ProcessName.Equals("cmd")).ToList();
                RunningProcesses.ForEach(p => ShowWindow(p.MainWindowHandle, FORCE_MINIMIZE));
                
                foreach (var screen in Screen.AllScreens)
                {
                    width += screen.Bounds.Width;
                    height = screen.Bounds.Height > height ? screen.Bounds.Height : height;
                }

                IntPtr hDesk = GetDesktopWindow();
                IntPtr hSrce = GetWindowDC(hDesk);
                IntPtr hDest = CreateCompatibleDC(hSrce);
                IntPtr hBmp = CreateCompatibleBitmap(hSrce, width, height);
                IntPtr hOldBmp = SelectObject(hDest, hBmp);
                bool b = BitBlt(hDest, 0, 0, width, height, hSrce, 0, 0, CopyPixelOperation.SourceCopy | CopyPixelOperation.CaptureBlt);

                using (Bitmap bmp = Bitmap.FromHbitmap(hBmp))
                {
                    SelectObject(hDest, hOldBmp);
                    DeleteObject(hBmp);
                    DeleteDC(hDest);
                    ReleaseDC(hDesk, hSrce);

                    filename = String.Format("screenshot_{0}.jpg", DateTime.Now.ToFileTime());
                    bmp.Save(filename, ImageFormat.Jpeg);
                }

                RunningProcesses.ForEach(p => 
                    {
                        if (p.HasExited != true)
                            ShowWindow(p.MainWindowHandle, SW_RESTORE);
                    });
                return filename;
            }
        }
    }
}