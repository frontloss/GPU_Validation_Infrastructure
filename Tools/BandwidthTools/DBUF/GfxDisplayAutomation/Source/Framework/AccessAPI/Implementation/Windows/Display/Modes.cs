namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Runtime.InteropServices;
    using System.Text;
    using System.Text.RegularExpressions;
    using System.Threading;
    using System.Threading.Tasks;
    using System.Windows.Forms;

    public class Modes : FunctionalBase, ISetMethod, IGetAllMethod, IGetMethod, IParse
    {
        int returnVal;
        const uint SDC_APPLY = 0x00000080;
        const uint SDC_USE_SUPPLIED_DISPLAY_CONFIG = 0x00000020;
        const uint SDC_SAVE_TO_DATABASE = 0x00000200;
        const uint SDC_ALLOW_CHANGES = 0x00000400;
        const uint SDC_NO_OPTIMIZATION = 0x00000100;
        const int PRECISION3DEC = 1000;
        private const int DISPLAY_DEVICE_MIRRORING_DRIVER = 8;
        private const int ENUM_CURRENT_SETTINGS = -1;
        uint pixelClk = 0, htotalVtotal = 0;
        DisplayConfigType _currentConfig;

        private List<DisplayInfoFromDevMngr> DispDevInfo = new List<DisplayInfoFromDevMngr>();
        public Modes()
        {
            returnVal = -1;
        }

        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "DisplayType:DisplayType:sp", "HZres:Horizontal Res:x", "VtRes:Vertical Res:x", "Bpp:Bpp:x", "RefreshRate:RefreshRate:x", "Scaling:Scaling" }, Comment = "Sets the mode for a display")]
        [ParseAttribute(InterfaceName = InterfaceType.IGetMethod, InterfaceData = new string[] { "DisplayType:DisplayType" }, Comment = "Gets the mode for a display")]
        [ParseAttribute(InterfaceName = InterfaceType.IGetAllMethod, InterfaceData = new string[] { "DisplayType:PrimaryDisplay:+", "DisplayType:SecondaryDisplay:+", "DisplayType:TertiaryDisplay" }, Comment = "Gets the modes for a list of displays")]
        public void Parse(string[] args)
        {
            if (args.IsHelpCall())
                this.HelpText();

            else if (args[0].ToLower().Equals("get"))
            {
                #region GET CALL
                DisplayType displayType = base.EnumeratedDisplays.Select(dI => dI.DisplayType).First();
                if (args.Length.Equals(2) && !string.IsNullOrEmpty(args[1]))
                    Enum.TryParse(args[1], true, out displayType);
                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).First();
                DisplayMode currentMode = (DisplayMode)this.GetMethod(displayInfo);
                Log.Message("Current Resolution on Display {0}", currentMode.display);
                Log.Message("HRes:{0} VRes:{1} Bpp:{2} RR:{3}{4} Scaling {5}", currentMode.HzRes, currentMode.VtRes, currentMode.Bpp, currentMode.RR, Convert.ToBoolean(currentMode.InterlacedFlag) ? "i" : "p", (ScalingOptions)currentMode.ScalingOptions.First());
                #endregion
            }
            else if (args[0].ToLower().Equals("getall"))
            {
                #region GETALL CALL
                List<DisplayType> displayList = new List<DisplayType>();
                try
                {
                    DisplayType tempDisplayType;
                    args[1].Split(new[] { '+', ',' }, StringSplitOptions.RemoveEmptyEntries).ToList().ForEach(d =>
                    {
                        Enum.TryParse<DisplayType>(d, true, out tempDisplayType);
                        displayList.Add(tempDisplayType);
                    });
                }
                catch
                {
                    this.HelpText();
                }
                List<DisplayModeList> supportedModes = (List<DisplayModeList>)this.GetAllMethod(displayList);
                foreach (DisplayModeList eachModeList in supportedModes)
                {
                    Console.WriteLine();
                    Log.Message("Mode list supported by {0} : ", eachModeList.display);
                    foreach (DisplayMode eachRes in eachModeList.supportedModes)
                    {
                        Log.Message("HRes:{0} VRes:{1} Bpp:{2} RR:{3}{4}", eachRes.HzRes, eachRes.VtRes, eachRes.Bpp, eachRes.RR, Convert.ToBoolean(eachRes.InterlacedFlag) ? "i" : "p");
                        eachRes.ScalingOptions.ForEach(sO => Log.Message("{0}", (ScalingOptions)sO));
                    }
                }
                #endregion
            }
            else if (args[0].ToLower().Contains("set"))
            {
                #region SET CALL
                args = args.Skip(1).ToArray();
                try
                {
                    string[] res = null;
                    DisplayMode mode = new DisplayMode();
                    mode.display = (DisplayType)Enum.Parse(typeof(DisplayType), args[0], true);
                    res = args[1].Split(new[] { 'x' }, StringSplitOptions.RemoveEmptyEntries);
                    mode.HzRes = Convert.ToUInt32(res[0]);
                    mode.VtRes = Convert.ToUInt32(res[1]);
                    mode.Bpp = Convert.ToUInt32(res[2]);
                    if (res[3].ToLower().Contains("i"))
                        mode.InterlacedFlag = Convert.ToUInt32(DisplayFlag.Interlaced);
                    else
                        mode.InterlacedFlag = Convert.ToUInt32(DisplayFlag.Progressive);
                    mode.RR = Convert.ToUInt32(Regex.Match(res[3], @"\d+").Value);
                    if (res.Length == 5)
                    {
                        mode.ScalingOptions = new List<uint>();
                        switch (res[4].ToUpper())
                        {
                            case "MDS":
                                mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Maintain_Display_Scaling));
                                break;
                            case "FULL":
                                mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Scale_Full_Screen));
                                break;
                            case "CENTER":
                                mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Center_Image));
                                break;
                            case "MAR":
                                mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Maintain_Aspect_Ratio));
                                break;
                            default:
                                Log.Alert("Invalid Scaling Option");
                                break;
                        }
                    }
                    if (this.SetMethod(mode))
                        Log.Success("Set display mode was success");
                    else
                        Log.Fail("Failed to set the mode");
                }
                catch
                {
                    this.HelpText();
                }
                #endregion
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("Usage for a GETALL Operation::").Append(Environment.NewLine);
            sb.Append("..\\>Execute Modes getall|get [Displays]").Append(Environment.NewLine);
            sb.Append("[Displays = CRT EDP DP HDMI.....] Each display should be , seperated").Append(Environment.NewLine).Append(Environment.NewLine);
            sb.Append("Example 1: Execute Modes GetSupportedModes EDP").Append(Environment.NewLine);
            sb.Append("Note: EDP should Active.").Append(Environment.NewLine).Append(Environment.NewLine);
            sb.Append("Example 2: Execute Modes getall|get EDP,HDMI").Append(Environment.NewLine);
            sb.Append("Note: EDP and HDMI should Active.").Append(Environment.NewLine).Append(Environment.NewLine).Append(Environment.NewLine);

            sb.Append("Usage for a SET Operation::").Append(Environment.NewLine);
            sb.Append("..\\>Execute Modes set [Display] [Resolutions]").Append(Environment.NewLine);
            sb.Append("[Displays = CRT/EDP/DP/HDMI.....] Display should be Active").Append(Environment.NewLine);
            sb.Append("[Resolutions = HRes x VRes x Bpp x RR[i/p] x Scaling]").Append(Environment.NewLine).Append(Environment.NewLine);
            sb.Append("[Scaling = MDS | FULL | CENTER | MAR ]").Append(Environment.NewLine).Append(Environment.NewLine);

            sb.Append("Example 1: Execute Modes SetMode EDP 1600x900x32x60pxMDS").Append(Environment.NewLine);
            sb.Append("Note: EDP should Active.").Append(Environment.NewLine).Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }

        public object GetMethod(object argMessage)
        {
            DisplayInfo displayInfo = argMessage as DisplayInfo;
            return GetCurrentMode(displayInfo.DisplayType, displayInfo.WindowsMonitorID);
        }

        public DisplayMode GetCurrentMode(DisplayType display, uint argWinMonitorID)
        {
            string adapter = "";
            GetDeviceNameForDisplay(argWinMonitorID, display, ref adapter);
            return GetCurrentMode(display, argWinMonitorID, adapter);
        }

        private DisplayMode GetCurrentMode(DisplayType display, uint argWinMonitorID, string argAdapterName)
        {
            DisplayMode currentMode = new DisplayMode();

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkModes = sdkExtn.GetSDKHandle(SDKServices.Mode);

            currentMode = (DisplayMode)sdkModes.Get(display);
            currentMode.display = display;

            if (currentMode.ScalingOptions == null || currentMode.ScalingOptions.Count == 0)
            {
                ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                currentMode.ScalingOptions = new List<uint>();
                DisplayScaling scaling = (DisplayScaling)sdkScaling.Get(currentMode);
                currentMode.ScalingOptions.Add((uint)scaling.scaling);
            }

            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);
            Log.Verbose("Return value of QDC call : {0}", returnVal);
            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode!");
                return currentMode;
            }

            for (int eachModeInfo = 0; eachModeInfo < modeInfo.Length; eachModeInfo++)
            {//workaround for Threshold OS issue for Windows ID.
                if (CommonExtensions.DoesWindowsIdMatched(modeInfo[eachModeInfo].id, base.GetWinMonitorIDByDisplayType(display)))
                {
                    currentMode.pixelClock = (double)modeInfo[eachModeInfo].mode.targetMode.targetVideoSignalInfo.pixelRate / 1000000;
                    break;
                }
            }              

            return currentMode;
        }

        private uint GetOrientation(ScreenOrientation argScreenOrientation)
        {
            switch (argScreenOrientation)
            {
                case ScreenOrientation.Angle0:
                    return 0;
                case ScreenOrientation.Angle180:
                    return 180;
                case ScreenOrientation.Angle270:
                    return 270;
                case ScreenOrientation.Angle90:
                    return 90;
                default:
                    return 0;
            }
        }

        private DISPLAYCONFIG_ROTATION GetGetOrientation(uint ori)
        {
            switch (ori)
            {
                case 0:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_IDENTITY;
                case 90:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE90;
                case 180:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE180;
                case 270:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE270;
                default:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_IDENTITY;
            }
        }


        public object GetAllMethod(object argMessage)
        {
            Log.Verbose("Getting all Supported Modes");
            List<DisplayType> displayList = (List<DisplayType>)argMessage;      

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkModes = sdkExtn.GetSDKHandle(SDKServices.Mode);
            return (List<DisplayModeList>)sdkModes.GetAll(displayList);
        }

	    private int GetBaseBpp()
        {
            if (base.MachineInfo.OS.Type == OSType.WIN7)
                return 16;
            else
                return 32;
        }

        private List<DisplayModeList> GetSupportedModes(List<DisplayType> displayList, int[] argRes)
        {
            List<DisplayModeList> allSupportedModes = new List<DisplayModeList>();
            DEVMODE mode = new DEVMODE();
            mode.dmSize = (short)Marshal.SizeOf(mode);

            String deviceName = "";
            foreach (DisplayType eachDisplay in displayList)
            {
                int modeIndex = 0;
                DisplayModeList modeList = new DisplayModeList();
                bool duplicate = false;
                DisplayMode currentRes = new DisplayMode();
                currentRes.ScalingOptions = new List<uint>();
                modeList.display = eachDisplay;

                #region change Hz resolution and vt resolution based on current Orientation


                if (!GetDeviceNameForDisplay(base.GetWinMonitorIDByDisplayType(eachDisplay), eachDisplay, ref deviceName))
                    return null;
                Interop.EnumDisplaySettings(deviceName, 0, ref mode);
                int HzRes = 0;
                int VtRes = 0;
                switch (mode.dmDisplayOrientation)
                {
                    case ScreenOrientation.Angle0:
                    case ScreenOrientation.Angle180:
                        HzRes = argRes.First();
                        VtRes = argRes.Last();
                        break;
                    case ScreenOrientation.Angle90:
                    case ScreenOrientation.Angle270:
                        HzRes = argRes.Last();
                        VtRes = argRes.First();
                        break;
                }
                #endregion


                while (Interop.EnumDisplaySettings(deviceName, modeIndex, ref mode))
                {
                    if (mode.dmPelsWidth >= HzRes && mode.dmPelsHeight >= VtRes && mode.dmBitsPerPel >= GetBaseBpp())
                    {
                        duplicate = false;
                        foreach (DisplayMode res in modeList.supportedModes)
                        {
                            if (res.HzRes == mode.dmPelsWidth &&
                                res.VtRes == mode.dmPelsHeight &&
                                res.RR == mode.dmDisplayFrequency &&
                                res.Bpp == mode.dmBitsPerPel &&
                                res.InterlacedFlag == mode.dmDisplayFlags)
                            {
                                duplicate = true;
                                break;
                            }
                        }
                        if (!duplicate)
                        {
                            currentRes.display = eachDisplay;
                            currentRes.ScalingOptions = new List<uint>();
                            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
                            ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                           
                            currentRes.HzRes = (uint)mode.dmPelsWidth;
                            currentRes.VtRes = (uint)mode.dmPelsHeight;
                            currentRes.Bpp = (uint)mode.dmBitsPerPel;
                            currentRes.RR = (uint)mode.dmDisplayFrequency;
                            currentRes.InterlacedFlag = (uint)mode.dmDisplayFlags;

                            List<uint> scalingOptions = (List<uint>)sdkScaling.GetAll(currentRes);
                            currentRes.ScalingOptions.AddRange(scalingOptions);
                            if (currentRes.ScalingOptions.Count != 0 && currentRes.ScalingOptions != null)
                            {
                                modeList.supportedModes.Add(currentRes);
                            }
                        }
                    }
                    modeIndex++;
                }
                allSupportedModes.Add(modeList);
            }
            return allSupportedModes;
        }

        private List<uint> OSScalingOption(DisplayMode mode)
        {
            List<uint> supportedScaling = new List<uint>();
            DEVMODE dvmode = new DEVMODE();
            dvmode.dmSize = (short)Marshal.SizeOf(dvmode);
            int modeIndex = 0;
            string adapter = "";
            GetDeviceNameForDisplay(base.EnumeratedDisplays.Where(DT => DT.DisplayType == mode.display).First().WindowsMonitorID, mode.display, ref adapter);
            while (Interop.EnumDisplaySettingsEx(adapter, modeIndex, ref dvmode, 0))
            {
                if (mode.HzRes == dvmode.dmPelsWidth && mode.VtRes == dvmode.dmPelsHeight &&
                     mode.RR == dvmode.dmDisplayFrequency && mode.Bpp == dvmode.dmBitsPerPel && mode.InterlacedFlag == dvmode.dmDisplayFlags)
                {
                    switch (dvmode.dmDisplayFixedOutput)
                    {
                        case 0:
                            supportedScaling.Add(Convert.ToUInt32(ScalingOptions.Maintain_Display_Scaling));
                            break;
                        case 1:
                            supportedScaling.Add(Convert.ToUInt32(ScalingOptions.Center_Image));
                            break;
                        case 2:
                            supportedScaling.Add(Convert.ToUInt32(ScalingOptions.Maintain_Aspect_Ratio));
                            break;

                    }
                }
                modeIndex++;
            }
            return supportedScaling;
        }

        private bool GetDeviceNameForDisplay(uint argWindowsMonitorID, DisplayType display, ref string deviceName)
        {
            //workaround for Threshold OS issue for Windows ID.
            uint tempWinID = argWindowsMonitorID & 0xFFFFFFF;

            if (0 == argWindowsMonitorID)
            {
                Log.Verbose("Windows Monitor ID not found for the display {0}", display.ToString());
                return false;
            }
            UpdateDevInfo();
            string DriverKey = string.Empty;
            foreach (DisplayInfoFromDevMngr DisplayDevInfo in DispDevInfo)
            {
                //Log.Message("WinMonid from QDC:{0},WinMonid from SetupDI:{1}, DriverKey:{2}", argWindowsMonitorID.ToString("X"),DisplayDevInfo.DeviceInstanceId, DisplayDevInfo.DriverKey);
                if (DisplayDevInfo.DeviceInstanceId.Contains(argWindowsMonitorID.ToString()) || DisplayDevInfo.DeviceInstanceId.Contains(tempWinID.ToString()))
                {
                    DriverKey = DisplayDevInfo.DriverKey;
                    break;
                }
            }
            if (0 == DriverKey.Length)
            {
                Log.Verbose("Driver key not found for the display {0}", display.ToString());
                return false;
            }
            DISPLAY_DEVICE displayDevice = new DISPLAY_DEVICE();
            DISPLAY_DEVICE monitorName = new DISPLAY_DEVICE();

            displayDevice.cb = Marshal.SizeOf(displayDevice);
            monitorName.cb = Marshal.SizeOf(monitorName);

            uint monId = 0;
            for (uint devId = 0; Interop.EnumDisplayDevices(null, devId, ref displayDevice, 0); devId++)
            {
                monId = 0;
                if (displayDevice.StateFlags != DISPLAY_DEVICE_MIRRORING_DRIVER)
                {
                    while (Interop.EnumDisplayDevices(displayDevice.DeviceName, monId++, ref monitorName, 0)) //Loop to get monitor names
                    {
                        if (monitorName.DeviceID.Contains(DriverKey))
                        {
                            //Log.Verbose("Display {0} driven by {1}", display, displayDevice.DeviceName);
                            deviceName = displayDevice.DeviceName;
                            return true;
                        }
                        monitorName.cb = Marshal.SizeOf(monitorName);
                    }
                }
                displayDevice.cb = Marshal.SizeOf(displayDevice);
            }

            Log.Verbose("Unable to find device name for display {0}", display);
            return false;
        }

        private void UpdateDevInfo()
        {
            const int SPDRP_DRIVER = 0x00000009;  // Driver (R/W)
            const int SPDRP_ADDRESS = 0x0000001C;  // Device Address (R)

            DispDevInfo = new List<DisplayInfoFromDevMngr>();
            Guid GUID_DEVINTERFACE_DISPLAY = new Guid(0x4D36E96E, 0xE325, 0x11CE, 0xBF, 0xC1, 0x08, 0x00, 0x2B, 0xE1, 0x03, 0x18);
            StringBuilder Enumerator = new StringBuilder("DISPLAY");
            DisplayInfoData displayInfoData = new DisplayInfoData();
            displayInfoData.Size = Marshal.SizeOf(displayInfoData);
            uint MemberIndex = 0;
            int lastError = 0;

            uint PropertyDataType = 0;
            StringBuilder PropertyBuffer = new StringBuilder(256);
            StringBuilder DeviceInstanceId = new StringBuilder(256);
            uint RequiredSize = 0;
            IntPtr DeviceInfoSet = new IntPtr();

            DisplayInfoFromDevMngr displayInfoFrmDevMngr = new DisplayInfoFromDevMngr();

            DeviceInfoSet = Interop.SetupDiGetClassDevs(ref GUID_DEVINTERFACE_DISPLAY, Enumerator, IntPtr.Zero, 0x04);
            lastError = Marshal.GetLastWin32Error();

            for (; Interop.SetupDiEnumDeviceInfo(DeviceInfoSet, MemberIndex++, ref displayInfoData); )
            {
                Interop.SetupDiGetDeviceInstanceId(DeviceInfoSet, ref displayInfoData, DeviceInstanceId, 1000, ref RequiredSize);
                lastError = Marshal.GetLastWin32Error();

                RequiredSize = 0;
                Interop.SetupDiGetDeviceRegistryProperty(DeviceInfoSet, ref displayInfoData, SPDRP_ADDRESS, ref PropertyDataType, PropertyBuffer, 1000, ref RequiredSize);
                lastError = Marshal.GetLastWin32Error();
                if (lastError == 0)
                {
                    RequiredSize = 0;
                    Interop.SetupDiGetDeviceRegistryProperty(DeviceInfoSet, ref displayInfoData, SPDRP_DRIVER, ref PropertyDataType, PropertyBuffer, 1000, ref RequiredSize);
                    lastError = Marshal.GetLastWin32Error();
                  
                    if (lastError == 0)
                    {
                        displayInfoFrmDevMngr.DeviceInstanceId = DeviceInstanceId.ToString();
                        displayInfoFrmDevMngr.DriverKey = PropertyBuffer.ToString();
                        DispDevInfo.Add(displayInfoFrmDevMngr);
                    }
                }
            }
            lastError = Marshal.GetLastWin32Error();
        }

        public bool SetMethod(object argMessage)
        {
            DisplayMode mode = (DisplayMode)argMessage;
            bool result = this.SetModeCUISDK(mode);
            return result;
        }

        private bool SetModeCUISDK(DisplayMode mode)
        {
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkModes = sdkExtn.GetSDKHandle(SDKServices.Mode);

            if (mode.ScalingOptions == null || mode.ScalingOptions.Count == 0)
            {
                mode.ScalingOptions = new List<uint>();
                ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                List<uint> scalingOptions = (List<uint>)sdkScaling.GetAll(mode);
                mode.ScalingOptions.AddRange(scalingOptions);
                if (mode.ScalingOptions.Count == 0)
                    Log.Abort("Unable to find scaling option through SDK");
            }

            if ((bool)sdkModes.Set(mode))
            {
                bool SetDisplayModeStatus = true;
                bool validRR = false;
                bool validScaling = false;
                Log.Verbose("Mode applied Successfully.");
                DisplayMode currentMode = GetCurrentMode(mode.display, GetWinMonitorIDByDisplayType(mode.display));

                if (currentMode.RR == mode.RR || Math.Abs(currentMode.RR - mode.RR) == 1)
                    validRR = true;
                if (currentMode.ScalingOptions[0] == mode.ScalingOptions[0])
                    validScaling = true;
                if (validRR && validScaling && currentMode.Bpp == mode.Bpp && currentMode.Angle == mode.Angle)
                {
                    if (mode.Angle == 0 || mode.Angle == 180)
                    {
                        if (!(currentMode.HzRes == mode.HzRes && currentMode.VtRes == mode.VtRes))
                            SetDisplayModeStatus = false;
                    }
                    else if (!(currentMode.HzRes == mode.VtRes && currentMode.VtRes == mode.HzRes))
                        SetDisplayModeStatus = false;
                }
                else
                    SetDisplayModeStatus = false;

                if (SetDisplayModeStatus == false)
                {
                    Log.Alert("Mismatch in resolution Applied. Expected: {0}, Current: {1}", mode.GetCurrentModeStr(false), currentMode.GetCurrentModeStr(false));
                }
                return SetDisplayModeStatus;
            }
            else
            {
                Log.Alert("Error in applying Mode through CUI SDK!!!! ");
            }
            return false;
        }

        private bool ModeSet(DisplayMode modeInfo)
        {
            #region If scaling option dosnt pass as DisplayMode parameter enumerate supported scaling option for the current mode
            if (null == modeInfo.ScalingOptions || modeInfo.ScalingOptions.Count == 0)
            {
                SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
                ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                List<uint> scalingOptions = (List<uint>)sdkScaling.GetAll(modeInfo);
                modeInfo.ScalingOptions.AddRange(scalingOptions);
            }
            #endregion

            if (modeInfo.ScalingOptions == null || modeInfo.ScalingOptions.Count.Equals(0))
            {
                Log.Alert("Scaling option return none for {0}", modeInfo.GetCurrentModeStr(true));
                return false;
            }
            Log.Message("Mode to be applied in display {0}: HRes - {1}, VRes - {2}, bpp - {3}, RR - {4}{5}, Angle: {6} Scaling - {7} ",
            modeInfo.display, modeInfo.HzRes, modeInfo.VtRes, modeInfo.Bpp, modeInfo.RR,
            (Convert.ToBoolean(modeInfo.InterlacedFlag) ? "i" : "p"), modeInfo.Angle, (ScalingOptions)modeInfo.ScalingOptions.First());
            return SetDisplayMode(modeInfo);
        }

        private bool SetDisplayMode(DisplayMode mode)
        {
            bool SetDisplayModeStatus=true;
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, topologyId);
            Log.Verbose("Return value of QDC call : {0}", returnVal);
            if (returnVal != (int)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Failed to fetch mode!");
                SetDisplayModeStatus = false;
                return SetDisplayModeStatus;
            }
            if (numModeInfoArrayElements == 2 && numPathArrayElements == 1)
                _currentConfig = DisplayConfigType.SD;
            else if (numModeInfoArrayElements == 3 && numPathArrayElements == 2)
                _currentConfig = DisplayConfigType.DDC;
            else if (numModeInfoArrayElements == 4 && numPathArrayElements == 3)
                _currentConfig = DisplayConfigType.TDC;
            else if (numModeInfoArrayElements == 4 && numPathArrayElements == 2)
                _currentConfig = DisplayConfigType.ED;
            else if (numModeInfoArrayElements == 6 && numPathArrayElements == 3)
                _currentConfig = DisplayConfigType.TED;
            FillModeInfoPathInfo(ref pathInfo, ref modeInfo, mode);

            returnVal = Interop.SetDisplayConfig(numPathArrayElements, pathInfo, numModeInfoArrayElements, modeInfo,
            SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE | SDC_ALLOW_CHANGES | SDC_NO_OPTIMIZATION);
            bool validRR = false;
            bool validScaling = false;

            if (returnVal == (long)QDC_SDC_StatusCode.SUCCESS)
            {
                Log.Verbose("Mode applied.");
                Log.Verbose("Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);
                Thread.Sleep(5000);

                DisplayMode currentMode = GetCurrentMode(mode.display, GetWinMonitorIDByDisplayType(mode.display));

                if (currentMode.RR == mode.RR || Math.Abs(currentMode.RR - mode.RR) == 1)
                    validRR = true;
                if(currentMode.ScalingOptions[0] == mode.ScalingOptions[0])
                    validScaling = true;
                else
                    validScaling = VerifyNativeModeScalingOption(mode);

                if (validRR && validScaling  && currentMode.Bpp == mode.Bpp && currentMode.Angle == mode.Angle)
                {
                    if (mode.Angle == 0 || mode.Angle == 180)
                    {
                        if (!(currentMode.HzRes == mode.HzRes && currentMode.VtRes == mode.VtRes))
                            SetDisplayModeStatus = false;
                    }
                    else if (!(currentMode.HzRes == mode.VtRes && currentMode.VtRes == mode.HzRes))
                        SetDisplayModeStatus = false;
                }
                else
                    SetDisplayModeStatus = false;

                if (SetDisplayModeStatus == false)
                {
                    Log.Alert("Mismatch in resolution Applied. Expected: {0}, Current: {1}", mode.GetCurrentModeStr(false), currentMode.GetCurrentModeStr(false));

                    PrintPathAndModeInfo(numPathArrayElements, pathInfo, numModeInfoArrayElements, modeInfo);
                    Log.Verbose("Flags" + " " + SDC_APPLY.ToString() + " " + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() + " " +
                            SDC_SAVE_TO_DATABASE.ToString() + " " + SDC_ALLOW_CHANGES.ToString() + " " + SDC_NO_OPTIMIZATION.ToString());
                }
            }
            else
            {
                SetDisplayModeStatus = false;
                Log.Alert("Error in applying Mode!!!! Return value of SDC call : {0}", (QDC_SDC_StatusCode)returnVal);

                PrintPathAndModeInfo(numPathArrayElements, pathInfo, numModeInfoArrayElements, modeInfo);
                Log.Verbose("Flags" + " " + SDC_APPLY.ToString() + " " + SDC_USE_SUPPLIED_DISPLAY_CONFIG.ToString() + " " +
                        SDC_SAVE_TO_DATABASE.ToString() + " " + SDC_ALLOW_CHANGES.ToString() + " " + SDC_NO_OPTIMIZATION.ToString());
            }
            return SetDisplayModeStatus;
        }

        private bool VerifyNativeModeScalingOption(DisplayMode mode)
        {
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_INTERNAL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_DATABASE_CURRENT, ref numPathArrayElements, pathInfo,
            ref numModeInfoArrayElements, modeInfo, ref topologyId);
            Log.Verbose("Return value of QDC call : {0}", returnVal);
            DisplayInfo Display = base.EnumeratedDisplays.Where(DT => DT.DisplayMode.display == mode.display).First();
            if (returnVal == (int)QDC_SDC_StatusCode.SUCCESS)
            {
                if (Display.DisplayMode.HzRes == mode.HzRes && Display.DisplayMode.VtRes == mode.VtRes)
                {
                    DISPLAYCONFIG_PATH_INFO displayPathinfo = pathInfo.Where(AID => CommonExtensions.DoesWindowsIdMatched(AID.targetInfo.id, Display.WindowsMonitorID)).First(); //workaround for Threshold OS issue for Windows ID.
                    if (mode.ScalingOptions.First() == (uint)displayPathinfo.targetInfo.scaling)
                    {
                        Log.Verbose("Scaling option for display {0} in QDC Database current is {1}", mode.display, (ScalingOptions)displayPathinfo.targetInfo.scaling);

                        string adapter = "";
                        List<uint> supportedScaling = new List<uint>();
                        GetDeviceNameForDisplay(Display.WindowsMonitorID, mode.display, ref adapter);
                        Log.Verbose("Verify {0} scaling supported by EDS", (ScalingOptions)mode.ScalingOptions.First());

                        DEVMODE dvmode = new DEVMODE();
                        dvmode.dmSize = (short)Marshal.SizeOf(dvmode);

                        int modeIndex = 0;
                        while (Interop.EnumDisplaySettingsEx(adapter, modeIndex, ref dvmode, 0))
                        {
                            if (mode.HzRes == dvmode.dmPelsWidth && mode.VtRes == dvmode.dmPelsHeight &&
                                 mode.RR == dvmode.dmDisplayFrequency && mode.Bpp == dvmode.dmBitsPerPel && mode.InterlacedFlag == dvmode.dmDisplayFlags)
                            {
                                supportedScaling.Add((uint)dvmode.dmDisplayFixedOutput);
                            }
                            modeIndex++;
                        }

                        if (supportedScaling.Any(S => S.Equals(mode.ScalingOptions[0])))
                        {
                            Log.Verbose("{0} Scaling supported by EDS for display {1}", (ScalingOptions)mode.ScalingOptions.First(), mode.display);
                            return false;
                        }
                        else
                        {
                            Log.Verbose("{0} Scaling doesn't supported by EDS for dispaly {1}", (ScalingOptions)mode.ScalingOptions.First(), mode.display);
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        private void PrintPathAndModeInfo(UInt32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO[] SDC_pathArray, UInt32 numModeInfoArrayElements, DISPLAYCONFIG_MODE_INFO[] SDC_modeInfoArray)
        {
            Log.Verbose("DumpData for Setmode");
            Log.Verbose("numPathArrayElements: {0},numModeInfoArrayElements:{1}",numPathArrayElements,numModeInfoArrayElements);
            for (int i = 0; i < SDC_pathArray.Length; i++)
            {
                DISPLAYCONFIG_PATH_INFO eachPath = SDC_pathArray[i];
                Log.Verbose(eachPath.ToString());
                Log.Verbose("--------------------------------------------------------");
            }

            for (int i = 0; i < SDC_modeInfoArray.Length; i++)
            {
                DISPLAYCONFIG_MODE_INFO eachPath = SDC_modeInfoArray[i];
                Log.Verbose(eachPath.ToString());
                Log.Verbose("--------------------------------------------------------");
            }
        }
        private void FillModeInfoPathInfo(ref DISPLAYCONFIG_PATH_INFO[] pathInfo, ref DISPLAYCONFIG_MODE_INFO[] modeInfo, DisplayMode mode)
        {
            int sourceModeIndex = (int)GetDispHierarchy(mode.display);
            for (int eachPathInfo = 0; eachPathInfo < pathInfo.Length; eachPathInfo++)
            {
                switch (_currentConfig)
                {
                    case DisplayConfigType.SD:
                    case DisplayConfigType.ED:
                    case DisplayConfigType.TED:
                        if (CommonExtensions.DoesWindowsIdMatched(pathInfo[eachPathInfo].targetInfo.id, base.GetWinMonitorIDByDisplayType(mode.display)))
                            FillPathInfo(ref pathInfo[eachPathInfo], mode);
                        break;
                    case DisplayConfigType.DDC:
                    case DisplayConfigType.TDC:
                        FillPathInfo(ref pathInfo[eachPathInfo], mode);
                        break;
                }
            }
            for (int eachModeInfo = 0; eachModeInfo < modeInfo.Length; eachModeInfo++)
            {
                switch (_currentConfig)
                {
                    case DisplayConfigType.SD:
                        FillModeInfo(ref modeInfo[eachModeInfo], mode);
                        break;
                    case DisplayConfigType.DDC:
                    case DisplayConfigType.TDC:
                        FillModeInfo(ref modeInfo[eachModeInfo], mode);
                        break;
                    case DisplayConfigType.ED:
                    case DisplayConfigType.TED:
                        if (modeInfo[eachModeInfo].infoType == DISPLAYCONFIG_MODE_INFO_TYPE.DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE && modeInfo[eachModeInfo].id == sourceModeIndex)
                            FillModeInfo(ref modeInfo[eachModeInfo], mode);
                        else if (modeInfo[eachModeInfo].infoType == DISPLAYCONFIG_MODE_INFO_TYPE.DISPLAYCONFIG_MODE_INFO_TYPE_TARGET)
                            FillModeInfo(ref modeInfo[eachModeInfo], mode);
                        break;
                }
            }
        }

        private void FillPathInfo(ref DISPLAYCONFIG_PATH_INFO pathInfo, DisplayMode mode)
        {
            if (Convert.ToBoolean(mode.InterlacedFlag))
            {
                ConvertRRtoRational((ulong)mode.HzRes, (ulong)mode.VtRes, (ulong)mode.RR, false, out pixelClk, out htotalVtotal);
                pathInfo.targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            else
            {
                ConvertRRtoRational((ulong)mode.HzRes, (ulong)mode.VtRes, (ulong)mode.RR, true, out pixelClk, out htotalVtotal);
                pathInfo.targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
            }
            pathInfo.targetInfo.rotation = GetGetOrientation(mode.Angle);
            pathInfo.targetInfo.refreshRate.Numerator = pixelClk;
            pathInfo.targetInfo.refreshRate.Denominator = htotalVtotal;
            pathInfo.targetInfo.scaling = (DISPLAYCONFIG_SCALING)mode.ScalingOptions.First();
        }

        private void FillModeInfo(ref DISPLAYCONFIG_MODE_INFO modeInfo, DisplayMode mode)
        {//workaround for Threshold OS issue for Windows ID.
            if (CommonExtensions.DoesWindowsIdMatched(modeInfo.id, base.GetWinMonitorIDByDisplayType(mode.display)))
            {
                if (Convert.ToBoolean(mode.InterlacedFlag))
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                }
                else
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
                }
                modeInfo.mode.sourceMode.width = pixelClk;
                modeInfo.mode.sourceMode.position.py = (int)pixelClk;

                modeInfo.mode.targetMode.targetVideoSignalInfo.vSyncFreq.Numerator = pixelClk;
                modeInfo.mode.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = htotalVtotal;
                if (mode.ScalingOptions.First() == (uint)ScalingOptions.Maintain_Display_Scaling)
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cx = mode.HzRes;
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cy = mode.VtRes;
                }
                else
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cx = base.EnumeratedDisplays.Find(Di => Di.DisplayType == mode.display).DisplayMode.HzRes;
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cy = base.EnumeratedDisplays.Find(Di => Di.DisplayType == mode.display).DisplayMode.VtRes;
                }
                modeInfo.mode.targetMode.targetVideoSignalInfo.pixelRate = pixelClk;
                modeInfo.mode.sourceMode.pixelFormat = GetPixelFormat(mode.Bpp);
            }
            if (modeInfo.infoType == DISPLAYCONFIG_MODE_INFO_TYPE.DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE)
            {
                modeInfo.mode.sourceMode.width = mode.HzRes;
                modeInfo.mode.sourceMode.height = mode.VtRes;
                modeInfo.mode.sourceMode.pixelFormat = GetPixelFormat(mode.Bpp);
            }
        }

        /// <summary>
        /// Converts RR to Rational format (x/y i.e., pixelclock/htotal*vtotal)
        /// </summary>
        /// CAUTION!! The following code for calculating the pixel clock, vtotal & htotal is taken from the SB driver code
        /// If SDC call fails because of RR value, make sure this code is in sync with SB driver code
        private void ConvertRRtoRational(ulong ulXRes, ulong ulYRes, ulong ulRRate, bool bProgressiveMode,
            out uint pixelClock, out uint HtotalVtotal)
        {
            //fixed defines as per VESA spec
            //double flMarginPerct = 1.80;//size of top and bottom overscan margin as percentage of active vertical image
            double flCellGran = 8.0;  //cell granularity
            ulong ulMinPorch = 1;    // 1 line/char cell
            ulong ulVSyncRqd = 3;    //width of vsync in lines
            float flHSynchPerct = 8.0F;//width of hsync as a percentage of total line period
            float flMin_Vsync_BP = 550.0F;//Minimum time of vertical sync + back porch interval (us).
            double flBlankingGradient_M = 600.0;//The blanking formula gradient 
            double flBlankingOffset_C = 40.0;//The blanking formula offset
            double flBlankingScaling_K = 128.0;//The blanking formula scaling factor
            double flBlankingScalWeighing_J = 20.0;//The blanking formula scaling factor weighting
            //Spec defination ends here

            //Calculation of C',M'
            //C' = Basic offset constant
            //M' = Basic gradient constant
            double flCPrime = (flBlankingOffset_C - flBlankingScalWeighing_J) * (flBlankingScaling_K) / 256.0
                            + flBlankingScalWeighing_J;
            double flMPrime = flBlankingScaling_K / 256 * flBlankingGradient_M;

            bool bInterLaced = !bProgressiveMode;

            //calculation of timing paramters
            // Step 1: Round the Horizontal Resolution to nearest 8 pixel
            ulong ulHPixels = ulXRes;
            ulong ulHPixelsRnd = (ulong)(((int)((ulHPixels / flCellGran) + (0.5))) * flCellGran);

            // Step 2: Calculate Vertical line rounded to nearest integer   
            float flVLines = (float)ulYRes;
            ulong ulVLinesRnd = (ulong)((int)((bInterLaced ? flVLines / 2 : flVLines) + 0.5));

            // Step 3: Find the field rate required (only useful for interlaced)
            float flVFieldRateRqd = (float)(bInterLaced ? ulRRate * 2 : ulRRate);

            // Step 4 and 5: Calculate top and bottom margins, we assumed zero for now
            //assumption top/bottom margins are unused, if a requirement comes for use of
            //margin then it has to added as function input parameter
            ulong ulTopMargin = 0;
            ulong ulBottomMargin = 0;

            // Step 6: If Interlaced set this value which is used in the other calculations 
            float flInterLaced = (float)(bInterLaced ? 0.5 : 0);

            // Step 7: Estimate the Horizontal period in usec per line
            float flHPeriodEst = ((1 / flVFieldRateRqd) - (flMin_Vsync_BP / 1000000)) /
                                    (ulVLinesRnd + 2 * ulTopMargin + ulMinPorch + flInterLaced) * 1000000;

            // Step 8: Find the number of lines in V sync + back porch
            ulong ulVSync_BP = (ulong)((int)((flMin_Vsync_BP / flHPeriodEst) + 0.5));

            // Step 9: Find the number of lines in V back porch alone
            ulong ulVBackPorch = ulVSync_BP - ulVSyncRqd;

            // Step 10: Find the total number of lines in vertical field
            float flTotalVLines = ulVLinesRnd + ulTopMargin + ulBottomMargin + ulVSync_BP + flInterLaced
                                  + ulMinPorch;

            // Step 11: Estimate the vertical field frequency
            float flVFieldRateEst = 1 / flHPeriodEst / flTotalVLines * 1000000;

            // Step 12: Find actual horizontal period
            float flHPeriod = flHPeriodEst / (flVFieldRateRqd / flVFieldRateEst);

            // Step 13: Find the actual vertical field frequency
            float flVFieldRate = (1 / flHPeriod / flTotalVLines) * 1000000;

            // Step 14: Find the actual vertical frame frequency
            float flVFrameRate = bInterLaced ? flVFieldRate / 2 : flVFieldRate;

            // Step 15,16: Find the number of pixels in the left, right margins, we assume they are zero 
            ulong ulLeftMargin = 0, ulRightMargin = 0;

            // Step 17: Find total number of active pixels in one line plus the margins 
            ulong ulTotalActivePixels = ulHPixelsRnd + ulRightMargin + ulLeftMargin;

            // Step 18: Find the ideal blanking duty cycle form blanking duty cycle equation
            float flIdealDutyCycle = (float)(flCPrime - (flMPrime * flHPeriod / 1000));

            // Step 19: Find the number of pixels in the blanking time to the nearest double charactr cell
            ulong ulHBlankPixels = (ulong)(((int)((ulTotalActivePixels * flIdealDutyCycle / (100 - flIdealDutyCycle) / (2 * flCellGran)) + 0.5)) * (2 * flCellGran));

            // Step 20: Find total number of pixels in one line
            ulong ulTotalPixels = ulTotalActivePixels + ulHBlankPixels;

            // Step 21: Find pixel clock frequency
            //currently we are taking value till 3 places after decimal
            //If the precision need to be increased to 4 places of decimal replace the
            //PRECISION3DEC by PRECISION4DEC
            ulong ulDecPrecisonPoint = PRECISION3DEC;
            //Get the pixel clcok till 3 places of decimals
            ulong ulPixelClock = (ulong)((int)((ulTotalPixels / flHPeriod) * ulDecPrecisonPoint) + 0.5);

            // Step 22:  Get the horizontal frequency
            float flHFreq = (1000 / flHPeriod) * 1000;

            ulong ulHSyncPixles = (ulong)(((int)(((ulTotalPixels / flCellGran) * (flHSynchPerct / 100)) + 0.5)) * flCellGran);
            ulong ulHSyncStart = ulTotalActivePixels + (ulHBlankPixels / 2) - ulHSyncPixles;
            ulong ulHSyncEnd = ulTotalActivePixels + (ulHBlankPixels / 2) - 1;
            //Gtf calculations ends here

            //This is the per frame total no of vertical lines
            ulong ulTotalVLines = (ulong)((int)((bInterLaced ? 2 * flTotalVLines : flTotalVLines) + 0.5));

            //This is done to get the pixel clock in Hz
            ulong dwDotClock = bInterLaced ? ((ulPixelClock * (1000000 / ulDecPrecisonPoint)) / 2) : ulPixelClock * (1000000 / ulDecPrecisonPoint);    // from step 21
            ulong dwHTotal = ulTotalPixels;          // from step 20

            //calculate in case of interlaced the frame based parameters
            //instead of per field basis
            ulong dwVTotal = ulTotalVLines;  // from step 10

            pixelClock = (uint)dwDotClock;
            HtotalVtotal = (uint)(dwHTotal * dwVTotal);
            if (!bProgressiveMode)
            {
                HtotalVtotal = HtotalVtotal / 2;
            }
        }

        private DISPLAYCONFIG_PIXELFORMAT GetPixelFormat(uint bpp)
        {
            switch (bpp)
            {
                case 8:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_8BPP;
                case 16:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_16BPP;
                case 24:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_24BPP;
                case 32:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_32BPP;
                default:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_FORCE_UINT32;
            }
        }

        private DisplayHierarchy GetDispHierarchy(DisplayType disp)
        {
            //string adapter = "";
            //GetDeviceNameForDisplay(base.GetWinMonitorIDByDisplayType(disp), disp, ref adapter);
            Config config = base.CreateInstance<Config>(new Config());
            DisplayConfig currentConfig = config.Get as DisplayConfig;
            Log.Verbose("Primary disp:{0}", currentConfig.PrimaryDisplay);
            Log.Verbose("SecondaryDisplay:{0}", currentConfig.SecondaryDisplay);
            Log.Verbose("TertiaryDisplay:{0}", currentConfig.TertiaryDisplay);
            if (disp == currentConfig.PrimaryDisplay)
                return DisplayHierarchy.Display_1;
            else if (disp == currentConfig.SecondaryDisplay)
                return DisplayHierarchy.Display_2;
            else if (disp == currentConfig.TertiaryDisplay)
                return DisplayHierarchy.Display_3;

            Log.Alert("Display Hierarchy not found for {0}", disp);
            return DisplayHierarchy.Unsupported;
        }
    }
}
