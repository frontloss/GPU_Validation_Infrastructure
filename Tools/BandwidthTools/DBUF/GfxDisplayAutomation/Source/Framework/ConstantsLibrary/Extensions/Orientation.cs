namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.Runtime.InteropServices;
    using System.Text;
    using System.Threading.Tasks;
    using System.Windows.Forms;

    public static class Orientation
    {
        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        public static extern IntPtr FindWindow(string strClassName, string strWindowName);

        [DllImport("user32.dll")]
        public static extern bool GetWindowRect(IntPtr hwnd, ref Rect rectangle);

        public struct Rect
        {
            public int Left { get; set; }
            public int Top { get; set; }
            public int Right { get; set; }
            public int Bottom { get; set; }
        }

        //Returns true for Landscape & False for Potrait
        public static bool Landscape()
        {
            Process[] processes = Process.GetProcesses();
            Process cui = null;

            foreach (Process p in processes)
                if (p.ToString().Contains("Gfxv"))
                    cui = p;
            Screen s = GetScreen();
            bool landscape = false;
            int width = s.WorkingArea.Right - s.WorkingArea.Left;
            int height = s.WorkingArea.Bottom - s.WorkingArea.Top;
            if (width > height)
                landscape = true;
            return landscape;
        }

        private static Screen GetScreen()
        {
            Screen[] screens = Screen.AllScreens;
            Process[] processes = Process.GetProcesses();
            Process cui = null;
            foreach (Process p in processes)
            {
                if (p.ToString().Contains("Gfxv"))
                {
                    cui = p;
                }
            }
            if (cui == null)
                return screens[0];
            IntPtr ptr = cui.MainWindowHandle;
            Rect CUIRect = new Rect();
            GetWindowRect(ptr, ref CUIRect);

            var mainWindowActualWidth = CUIRect.Bottom - CUIRect.Top;
            var mainWindowActualHeight = CUIRect.Right - CUIRect.Left;

            var minWidthScreen = 1024;
            var minHeightScreen = 768;
            foreach (var screen in screens)
            {
                var isScreenLandscape = screen.WorkingArea.Width > screen.WorkingArea.Height;
                var screenWidth = isScreenLandscape ? screen.WorkingArea.Width : screen.WorkingArea.Height;
                var screenHeight = isScreenLandscape ? screen.WorkingArea.Height : screen.WorkingArea.Width;

                if (screenWidth < minWidthScreen) minWidthScreen = screenWidth;
                if (screenHeight < minHeightScreen) minHeightScreen = screenHeight;
            }
            double widthUsedToCalcArea;
            double heightUsedToCalcArea;

            bool isAppLandscape = mainWindowActualWidth > mainWindowActualHeight;
            if (isAppLandscape)
            {
                widthUsedToCalcArea = (mainWindowActualWidth < minWidthScreen) ? mainWindowActualWidth : minWidthScreen;
                heightUsedToCalcArea = (mainWindowActualHeight < minHeightScreen) ? mainWindowActualHeight : minHeightScreen;
            }
            else
            {
                //compare height and width here
                widthUsedToCalcArea = (mainWindowActualWidth < minHeightScreen) ? mainWindowActualWidth : minHeightScreen;
                heightUsedToCalcArea = (mainWindowActualHeight < minWidthScreen) ? mainWindowActualHeight : minWidthScreen;
            }

            double appWidth = isAppLandscape ? widthUsedToCalcArea : heightUsedToCalcArea;
            double appHeight = isAppLandscape ? heightUsedToCalcArea : widthUsedToCalcArea;

            double aleft = CUIRect.Left;
            double aright = aleft + appWidth;
            double atop = (CUIRect.Top);
            double abottom = atop + appHeight;
            double aHMid = aleft + (aright - aleft) / 2;
            double aVMid = atop + (abottom - atop) / 2;

            double maxArea = 0;
            int screenIndex = 0;

            //Take the layout of the Monitor where the max area of UI lies
            for (int index = 0; index < screens.Length; index++)
            {
                double tempArea = 0;
                bool isAreaCalculated = false;
                var screenRight = screens[index].WorkingArea.Right;
                var screenLeft = screens[index].WorkingArea.Left;
                var screenBottom = screens[index].WorkingArea.Bottom;
                var screenTop = screens[index].WorkingArea.Top;

                var areaRight = aright < screenRight ? aright : screenRight;
                var areaBottom = abottom < screenBottom ? abottom : screenBottom;
                var areaLeft = aleft > screenLeft ? aleft : screenLeft;
                var areaTop = atop > screenTop ? atop : screenTop;

                if (aleft >= screenLeft && aleft <= screenRight && atop >= screenTop && atop <= screenBottom)//LeftLop is inside this screen?
                {
                    isAreaCalculated = true;
                    tempArea = (areaRight - aleft) * (areaBottom - atop);
                    if (tempArea > maxArea)
                    {
                        maxArea = tempArea;
                        screenIndex = index;
                    }
                }

                if (!isAreaCalculated && aright >= screenLeft && aright <= screenRight && atop >= screenTop && atop <= screenBottom)//RightTop is inside this screen?
                {
                    isAreaCalculated = true;
                    tempArea = (aright - areaLeft) * (areaBottom - atop);
                    if (tempArea > maxArea)
                    {
                        maxArea = tempArea;
                        screenIndex = index;
                    }
                }

                if (!isAreaCalculated && aleft >= screenLeft && aleft <= screenRight && abottom >= screenTop && abottom <= screenBottom)//LeftBottom is inside this screen?
                {
                    isAreaCalculated = true;
                    tempArea = (areaRight - aleft) * (abottom - areaTop);
                    if (tempArea > maxArea)
                    {
                        maxArea = tempArea;
                        screenIndex = index;
                    }
                }

                if (!isAreaCalculated && aright >= screenLeft && aright <= screenRight && abottom >= screenTop && abottom <= screenBottom)//RightBottom is inside this screen?
                {
                    isAreaCalculated = true;
                    tempArea = (aright - areaLeft) * (abottom - areaTop);
                    if (tempArea > maxArea)
                    {
                        maxArea = tempArea;
                        screenIndex = index;
                    }
                }
                //HMidTop/HMidBottom/VMidLeft/VMidRight/HMidVMid
                if ((!isAreaCalculated && aHMid >= screenLeft && aHMid <= screenRight && atop >= screenTop && atop <= screenBottom) ||
                    (!isAreaCalculated && aHMid >= screenLeft && aHMid <= screenRight && abottom >= screenTop && abottom <= screenBottom) ||
                    (!isAreaCalculated && aVMid >= screenLeft && aVMid <= screenRight && aleft >= screenTop && aleft <= screenBottom) ||
                    (!isAreaCalculated && aVMid >= screenLeft && aVMid <= screenRight && aright >= screenTop && aright <= screenBottom) ||
                    (!isAreaCalculated && aHMid >= screenLeft && aHMid <= screenRight && aVMid >= screenTop && aVMid <= screenBottom))
                {
                    tempArea = (areaRight - areaLeft) * (areaBottom - areaTop);
                    if (tempArea > maxArea)
                    {
                        maxArea = tempArea;
                        screenIndex = index;
                    }
                }
            }

            return screens[screenIndex];
        }
    }
}
