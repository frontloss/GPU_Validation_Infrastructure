namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Xml.Serialization;
    using System.IO;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using Microsoft.Win32;
    using System.Windows.Automation;
    using System.Windows.Forms;

    internal class SetUpDesktop : FunctionalBase, ISetMethod, IParse
    {
        private const int SW_HIDE = 0;
        private const int SW_SHOW = 1;
        public static List<IntPtr> TaskBarHandles = new List<IntPtr>();
        const uint OCR_NORMAL = 32512;
        const uint SPI_SETCURSORS = 0X0057;
        private int LaunchDTCMCount = 0;
        // constants for the mouse_input() API function
        private const int MOUSEEVENTF_LEFTDOWN = 0x02;
        private const int MOUSEEVENTF_LEFTUP = 0x04;
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        public bool SetMethod(object argMessage)
        {           
            bool status = true;

            SetUpDesktopArgs desktopArgs = argMessage as SetUpDesktopArgs;
            Log.Message("Setting desktop to {0}", desktopArgs.FunctionName);

            if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.ChangeDesktopBackground)
            {
                ChangeDesktopBackground(desktopArgs.ImageFilePath);
            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.ShowTaskBar)
            {
                ShowOrHideTaskBar(true);
            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.HideTaskBar)
            {
                ShowOrHideTaskBar(false);
            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.ShowCursor)
            {
                ShowCursor();
            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.HideCursor)
            {
                HideCursorFromDesktop();
            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop)
            {
                LaunchTenPlayerFullScreen(desktopArgs);
               // //ChangeDesktopBackground(desktopArgs.ImageFilePath);
               // //ShowOrHideDesktopIcons(false);
               // ShowOrHideTaskBar(false);
               // //DisableNotification();
               // //DisableBallonNotifications();
               //// HideCursorFromDesktop();
               // ShowStaticForm(true, desktopArgs.currentConfig, desktopArgs.display);
               // Cursor.Hide();
                Thread.Sleep(5000);
            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop)
            {
                CloseTenPlayerFullScreen();
                //Cursor.Show();
                //ShowStaticForm(false, desktopArgs.currentConfig, desktopArgs.display);
                ////ShowCursor();
                //ShowOrHideTaskBar(true);
                ////ShowOrHideDesktopIcons(true);
                Thread.Sleep(1000);
            }
            else if(desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.TenPlayerHDR)
            {
                LaunchTenPlayerFullScreenHDR(desktopArgs);
            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.ShowMMIOFlip)
            {
                IntPtr pUserVirtualAddress = default(IntPtr);
                UInt64 pGmmBlock = 0, surfaceSize = 0;

                EnableULT(true);

                EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);

                ULT_FW_Create_Resource(desktopArgs.displayMode.HzRes, desktopArgs.displayMode.VtRes, ULT_PIXELFORMAT.SB_B8G8R8A8, ULT_TILE_FORMATS.ULT_TILE_FORMAT_X, 0, ref pGmmBlock, ref pUserVirtualAddress, ref  surfaceSize);
                desktopArgs.pGmmBlock = pGmmBlock;

                uint sourceID = (uint)desktopArgs.currentConfig.CustomDisplayList.IndexOf(desktopArgs.displayMode.display);
                if (DisplayExtensions.GetUnifiedConfig(desktopArgs.currentConfig.ConfigType) == DisplayUnifiedConfig.Clone)
                    sourceID = 0;

                ULT_FW_Set_Source_Address(pGmmBlock, sourceID, 0, ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync);

            }
            else if (desktopArgs.FunctionName == SetUpDesktopArgs.SetUpDesktopOperation.HideMMIOFlip)
            {
                ULT_FW_Free_Resource(desktopArgs.pGmmBlock);
                EnableFeature(false, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);
            }
            return status;
        }

        private void LaunchTenPlayerFullScreen(SetUpDesktopArgs desktopArgs)
        {
            
            Screen[] screens = Screen.AllScreens;
            //Initialize Size object for form
            int Width = screens[0].Bounds.Width;
            int Height = screens[0].Bounds.Height;

            //if (desktopArgs.currentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
            //{
            //    int displayHierarchy = (int)desktopArgs.currentConfig.GetDispHierarchy(desktopArgs.displayType);

            //    for (int i = 0; i < displayHierarchy; i++)
            //        formPosition += screens[i].Bounds.Width;

            //    size.Width = screens[displayHierarchy].Bounds.Width;
            //    size.Height = screens[displayHierarchy].Bounds.Height;
            //}

            Log.Verbose("Launching TenPlayer in fullscreen mode.");
            string argument = string.Format("-w {0} -h {1} -b {2} -p {3} -hide_cursor -i GoldenImage.jpg ", desktopArgs.displayMode.HzRes, desktopArgs.displayMode.VtRes, 8, "primary");
            Log.Message("Command is: " + argument);
            Process.Start("tenplayer.exe", argument);
        }


        private void LaunchTenPlayerFullScreenHDR(SetUpDesktopArgs desktopArgs)
        {
            Log.Verbose("Launching TenPlayer in fullscreen mode.");
            //string argument = string.Format("-set_mode -f 24 -i {0} -static_metadata {1}",desktopArgs.ImageFilePath,desktopArgs.MetadataFilePath);
            string argument = string.Format("-w {0} -h {1} -b {2} -i {3} -m {4}", desktopArgs.displayMode.HzRes,desktopArgs.displayMode.VtRes,desktopArgs.BPC,desktopArgs.ImageFilePath, desktopArgs.MetadataFilePath);
            string executable = String.Concat(base.AppSettings.DisplayToolsPath, "\\HDR\\tenplayer.exe");
            Log.Message("Command is: " + argument);
            Process.Start(executable, argument);
          
            
        }

        private bool CloseTenPlayerFullScreen()
        {
            int WM_CLOSE = 0x0010;
            IntPtr sf = Interop.FindWindow(null, "tenplayer");
            if (sf != IntPtr.Zero)
            {
                Interop.SendMessage(sf, WM_CLOSE, IntPtr.Zero, IntPtr.Zero);
            }
            else
            {
                return false;
            }
            return true;
        }

        public uint ReadRegistryEntry()
        {
            RegistryHive hive = RegistryHive.CurrentUser;
            uint result = Convert.ToUInt32(GetKeyFromHive(hive).OpenSubKey("Software").OpenSubKey("Microsoft").OpenSubKey("Windows").OpenSubKey("CurrentVersion").OpenSubKey("Explorer").OpenSubKey("Advanced").GetValue("HideIcons"));
            return result;
        }

        private RegistryKey GetKeyFromHive(RegistryHive Hive)
        {
            switch (Hive)
            {
                case RegistryHive.ClassesRoot: return Registry.ClassesRoot;
                case RegistryHive.CurrentConfig: return Registry.CurrentConfig;
                case RegistryHive.CurrentUser: return Registry.CurrentUser;
                case RegistryHive.LocalMachine: return Registry.LocalMachine;
                //  case RegistryHive.DynData: return Registry.DynData;
                case RegistryHive.PerformanceData: return Registry.PerformanceData;
                case RegistryHive.Users: return Registry.Users;
                default: throw new Exception("Unsupported hive passed as parameter");
            }
        }
        bool ShowOrHideDesktopIcons(bool ShowIcons)
        {
            uint desktopIconStatus = ReadRegistryEntry();
            switch (ShowIcons)
            {
                case true:
                    if (desktopIconStatus == 0)
                    {
                        Log.Message("Desktop Icons are already Visible.");
                        MinimizeAllWindow();
                        return true;
                    }
                    else
                    {
                        Log.Message("Showing the Desktop Icons");
                        break;
                    }
                case false: if (desktopIconStatus == 1)
                    {
                        Log.Message("Desktop Icon are already Hidden");
                        MinimizeAllWindow();
                        return true;
                    }
                    else
                    {
                        Log.Message("Hiding the Desktop Icons");
                        break;
                    }
            }

            if (!DTCM_DesktopIcons())
                return false;
            else
                return true;

            ////get a handle to the desktop ("Progman")
            //IntPtr winHandle = Interop.FindWindowEx(IntPtr.Zero, IntPtr.Zero, "Progman", null);

            ////determine if we're showing or hiding
            //switch (ShowIcons)
            //{
            //    case true:
            //        Interop.ShowWindow(winHandle, 0);
            //        break;
            //    case false:
            //        Interop.ShowWindow(winHandle, 5);
            //        break;
            //}
        }
        private void ShowCursor()
        {
            string tempStr = null;
            Interop.SystemParametersInfo(SPI_SETCURSORS, 0, tempStr, 0);
        }
        private void HideCursorFromDesktop()
        {
            //Overwrite the current normal cursor with a blank cursor to "hide" it.
            IntPtr cursor = Interop.LoadCursorFromFile(Path.Combine(Directory.GetCurrentDirectory(), "blank.cur"));
            Interop.SetSystemCursor(cursor, OCR_NORMAL);
        }

        public void ShowStaticForm(bool ShowForm, DisplayConfig currentConfig, DisplayType currentDisplay)
        {
            StaticForm staticForm = base.CreateInstance<StaticForm>(new StaticForm());
            StaticFormArgs staticFormArgs = new StaticFormArgs(ShowForm);
            staticFormArgs.currentConfig = currentConfig;
            staticFormArgs.displayType = currentDisplay;

            staticForm.SetMethod(staticFormArgs);
        }

        public void ChangeDesktopBackground(string fileName)
        {
            uint SPI_SETDESKWALLPAPER = 0x14;
            uint SPIF_UPDATEINIFILE = 0x01;
            uint SPIF_SENDWININICHANGE = 0x02;
            int WM_COMMAND = 0x111;
            int MIN_ALL = 419;

            string tempPath = Path.Combine(Path.Combine(Directory.GetCurrentDirectory(), fileName));

            RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Control Panel\Desktop", true);

            key.SetValue(@"WallpaperStyle", 2.ToString());
            key.SetValue(@"TileWallpaper", 0.ToString());

            Interop.SystemParametersInfo(SPI_SETDESKWALLPAPER,
                0,
                tempPath,
                SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE);

            IntPtr lHwnd = Interop.FindWindow("Shell_TrayWnd", null);
            Interop.SendMessage(lHwnd, WM_COMMAND, (IntPtr)MIN_ALL, IntPtr.Zero);

            //SendKeys.SendWait("{F5}");

            System.Threading.Thread.Sleep(5000);
        }

        static void ShowOrHideTaskBar(bool ShowTaskbar)
        {
            Interop.EnumWindows(new Interop.EnumWindowsProc(GetWindowHandles), IntPtr.Zero);

            if (TaskBarHandles.Count == 0)
            {
                Log.Fail("Unable to hide/Show TaskBar. zero taskbar window Handles found.");
            }

            foreach (IntPtr temp in TaskBarHandles)
            {
                Interop.ShowWindow(temp, ShowTaskbar ? SW_SHOW : SW_HIDE);
            }
        }
        private static bool GetWindowHandles(IntPtr hWnd, IntPtr lParam)
        {
            StringBuilder ClassName = new StringBuilder(100);
            //Get the window class name
            Interop.GetClassName(hWnd, ClassName, ClassName.Capacity);

            if ((ClassName.ToString().Contains("Shell") && ClassName.ToString().Contains("TrayWnd")) || ClassName.ToString().Contains("Button"))
            {
                Log.Verbose("Captured Window handle: " + hWnd + " " + ClassName.ToString());

                if (ClassName.ToString().Contains("Shell_TrayWnd"))
                    TaskBarHandles.Insert(0, hWnd);
                else
                    TaskBarHandles.Add(hWnd);
            }

            return true;
        }

        private bool DTCM_DesktopIcons()
        {
            if (LaunchDTCMCount > 3)
            {
                Log.Fail("Failed to Launch DTCM");
                return false;
            }
            LaunchDTCM();
            AutomationElement element = UIABaseHandler.SelectElementNameControlType("View", ControlType.MenuItem);
            if (element != null)
            {
                Log.Message("element name is {0}", element.Current.Name);
                uiaBaseHandler.ExpandCollapse(element);
                AutomationElement element2 = UIABaseHandler.SelectElementNameControlType("Show desktop icons", ControlType.MenuItem);

                if (element2 != null)
                {
                    Log.Message("element2 name is {0}", element2.Current.Name);
                        uiaBaseHandler.Invoke(element2);
                }
                else
                {
                    DTCM_DesktopIcons();
                }
            }
            else
            {
                DTCM_DesktopIcons();
            }
            return true;
        }
        private void MinimizeAllWindow()
        {
            const int FORCE_MINIMIZE = 11;
            Thread.Sleep(2000);
            // Process.GetProcesses().Where(p => p.ProcessName.StartsWith("Gfx")).ToList().ForEach(p => ShowWindow(p.MainWindowHandle, FORCE_MINIMIZE));
            Process[] processList = Process.GetProcesses();
            foreach (Process p in processList)
            {
                Interop.ShowWindow(p.MainWindowHandle, FORCE_MINIMIZE);
            }

            Thread.Sleep(2000);
        }
        private void LaunchDTCM()
        {
            MinimizeAllWindow();
            Thread.Sleep(2000);
            Interop.SetCursorPos(Screen.PrimaryScreen.WorkingArea.Width / 2, Screen.PrimaryScreen.WorkingArea.Height / 8);
            Interop.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
            Interop.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
            Thread.Sleep(1000);
            SendKeys.SendWait("+{F10}");
            Thread.Sleep(1000);
            LaunchDTCMCount++;
        }
        public void Parse(string[] args)
        {
            //ImageProcessingParams imageProcessParams = new ImageProcessingParams();
            //ImageProcessOptions optionSelected;
            //if (args.Length == 4 && args[0].ToLower().Contains("set") && Enum.TryParse<ImageProcessOptions>(args[1], true, out optionSelected))
            //{
            //    imageProcessParams.ImageProcessingOption = optionSelected;
            //    imageProcessParams.SourceImage = args[2];
            //    imageProcessParams.TargetImage = args[3];

            //    SetMethod(imageProcessParams);
            //}
            //else if (args.Length == 2 && args[0].ToLower().Contains("get"))
            //{

            //}
            //else
            //    this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe ImageProcessing set/get ImageProcessOptions FileName1 <FileName2> <pixelInfo>").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe ImageProcessing set CompareImages sourceFileName TargetFileName");
            Log.Message(sb.ToString());
        }
        private void DisableNotification()
        {
            Log.Verbose("Launching Notification Area Icons Control Panel");
            CommonExtensions.StartProcess("control", " /name Microsoft.NotificationAreaIcons");
            AutomationElement element = UIABaseHandler.SelectElementClassNameControlType(AutomationElement.RootElement, "CCCheckBox", ControlType.CheckBox);
            TogglePattern pattern = element.GetCurrentPattern(TogglePattern.Pattern) as TogglePattern;
            if (pattern.Current.ToggleState == ToggleState.On)
                SendKeys.SendWait("%A");
            System.Threading.Thread.Sleep(1000);
            uiaBaseHandler.Invoke(UIABaseHandler.SelectElementNameControlType(AutomationElement.RootElement, "Close", ControlType.Button));
        }
        private void DisableBallonNotifications()
        {
            if (LaunchDTCMCount > 3)
            {
                Log.Message("Failed to Launch DTCM");
                return;
            }
            LaunchDTCM();
            AutomationElement element = UIABaseHandler.SelectElementNameControlType("Graphics Options", ControlType.MenuItem);
            if (element != null)
            {
                Log.Message("element name is {0}", element.Current.Name);
                uiaBaseHandler.ExpandCollapse(element);

                element = UIABaseHandler.SelectElementNameControlType("Balloon Notifications", ControlType.MenuItem);
                if (element != null)
                {
                    Log.Message("element name is {0}", element.Current.Name);
                    uiaBaseHandler.ExpandCollapse(element);

                    element = UIABaseHandler.SelectElementNameControlType("Optimal Resolution Notification", ControlType.MenuItem);
                    if (element != null)
                    {
                        Log.Message("element name is {0}", element.Current.Name);
                        uiaBaseHandler.ExpandCollapse(element);

                        element = UIABaseHandler.SelectElementNameControlType("Disable", ControlType.MenuItem);
                        if (element != null && element.Current.IsEnabled)
                        {
                            Log.Message("element name is {0}", element.Current.Name);
                            uiaBaseHandler.Invoke(element);
                        }
                    }
                }
            }
            Thread.Sleep(2000);
            Interop.SetCursorPos(Screen.PrimaryScreen.WorkingArea.Width / 2, Screen.PrimaryScreen.WorkingArea.Height / 8);
            Interop.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
            Interop.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
            Thread.Sleep(1000);
        }
        private bool EnableULT(bool enable)
        {
            bool status = true;
            ULT_ESC_ENABLE_ULT_ARG ult_Esc_Args = new ULT_ESC_ENABLE_ULT_ARG();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.bEnableULT = enable;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args))
            {
                status= false;
            }

            if (ult_Esc_Args.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                status = false;
            }
            return status;
        }
        private bool EnableFeature(bool enable, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE featureType)
        {
            bool status = true;
            Log.Message(true, "Set Status of feature {0} to {1}", featureType, enable);
            ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS ult_Esc_Args = new ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE;
            ult_Esc_Args.bEnableFeature = enable;
            ult_Esc_Args.eFeatureEnable = featureType;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE, ult_Esc_Args))
            {
                status= false;
            }
            if (ult_Esc_Args.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                status = false;
            }
            return status;
        }
        private bool ULT_FW_Create_Resource(uint x, uint y, ULT_PIXELFORMAT SRC_Pixel_Format, ULT_TILE_FORMATS Tile_Format, uint AuxSurf, ref UInt64 pGmmBlock, ref IntPtr pUserVirtualAddress, ref UInt64 surfaceSize)
        {
            bool status = true;
            ULT_CREATE_RES_ARGS ult_Esc_Args = new ULT_CREATE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.ulBaseWidth = x;
            ult_Esc_Args.ulBaseHeight = y;
            ult_Esc_Args.Format = SRC_Pixel_Format;
            ult_Esc_Args.TileFormat = Tile_Format;
            ult_Esc_Args.AuxSurf = false;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE, ult_Esc_Args))
            {
                status = false;
            }
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    status = false;
                }
                else
                {
                    pGmmBlock = ult_Esc_Args.pGmmBlock;
                    pUserVirtualAddress = (IntPtr)ult_Esc_Args.pUserVirtualAddress;
                    surfaceSize = ult_Esc_Args.u64SurfaceSize;

                    string filepath = base.AppSettings.GoldenCRCPath + "\\GoldenCRCImage\\" + "Blue.bin";
                    byte[] array = File.ReadAllBytes(filepath);

                    int arrLength = Math.Min(array.Length, (int)surfaceSize);
                    Marshal.Copy(array, 0, pUserVirtualAddress, arrLength);
                }
            }
            return status;
        }

        private bool ULT_FW_Free_Resource(UInt64 pGmmBlock)
        {
            bool status = true;
            ULT_FREE_RES_ARGS ult_Esc_Args = new ULT_FREE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_FREE_RESOURCE;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.pGmmBlock = pGmmBlock;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_FREE_RESOURCE, ult_Esc_Args))
            {
                status = false;
            }

            if (ult_Esc_Args.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                status = false;
            }
            return status;
        }
        private bool ULT_FW_Set_Source_Address(UInt64 pGmmBlock, uint sourceID, uint dataSize, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag)
        {
            bool status = true;
            ULT_ESC_SET_SRC_ADD_ARGS ult_Esc_Args = new ULT_ESC_SET_SRC_ADD_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            ult_Esc_Args.ulSrcID = sourceID;
            ult_Esc_Args.ulDataSize = dataSize;
            ult_Esc_Args.Flags = Flag;

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS, ult_Esc_Args))
            {
                status = false;
            }

            if (ult_Esc_Args.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                status = false;
            }
           
            return status;
        }

        private bool DoULTEscape(ULT_ESCAPE_CODE escapeCode, object Ult_Esc_Args)
        {
            bool status = true;

            ULT_Framework u = new ULT_Framework();
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(escapeCode, Ult_Esc_Args);
            if (!u.SetMethod(escapeParams))
            {
                Log.Fail(String.Format("Failed to perform: {0}", escapeParams.ULT_Escape_Type));
                status = false;
            }

            return status;
        }
    }
}