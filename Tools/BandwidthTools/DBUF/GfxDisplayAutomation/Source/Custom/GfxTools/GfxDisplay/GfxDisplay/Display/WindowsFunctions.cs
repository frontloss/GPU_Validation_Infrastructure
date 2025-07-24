namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Threading;
    using System.Windows.Forms;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;

    internal static partial class WindowsFunctions
    {
        private const int ENUM_CURRENT_SETTINGS = -1;

        internal static List<DisplayInfo> GetAllDisplayList()
        {
            List<DisplayInfo> displaysList = new List<DisplayInfo>();
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, pathInfo, ref numModeInfoArrayElements, modeInfo, topologyId);
            if (!Convert.ToBoolean(returnVal))
            {
                foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                    if (!eachPath.targetInfo.id.Equals(0) && eachPath.targetInfo.targetAvailable)
                        if (DisplayTypeMap.ContainsKey(eachPath.targetInfo.outputTechnology) && !displaysList.Any(dI => dI.WindowsMonitorID == eachPath.targetInfo.id))
                            AddDisplay(eachPath.targetInfo.id, DisplayTypeMap[eachPath.targetInfo.outputTechnology], displaysList, eachPath.flags);
            }
            else
                Console.WriteLine("GetAllDisplayList::QDC Call Error! Return value {0}", returnVal);
            return displaysList;
        }
        internal static DisplayMode GetCurrentMode(uint argWinMonitorID, string argAdapterName)
        {
            DisplayMode currentMode = new DisplayMode();
            DEVMODE mode = new DEVMODE();
            mode.dmSize = (short)Marshal.SizeOf(mode);
            Interop.EnumDisplaySettings(argAdapterName, ENUM_CURRENT_SETTINGS, ref mode);

            currentMode.HzRes = (uint)mode.dmPelsWidth;
            currentMode.VtRes = (uint)mode.dmPelsHeight;
            currentMode.RR = (uint)mode.dmDisplayFrequency;
            currentMode.Bpp = (uint)mode.dmBitsPerPel;
            currentMode.InterlacedFlag = (uint)mode.dmDisplayFlags;
            currentMode.Angle = Convert.ToUInt32(mode.dmDisplayOrientation.ToString().ToLower().Replace("angle", string.Empty));

            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            if (Convert.ToBoolean(returnVal))
                Console.WriteLine("GetCurrentMode::GetDisplayConfigBufferSizes Call Error! Return value {0}", returnVal);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo, ref numModeInfoArrayElements, modeInfo, topologyId);

            if (!Convert.ToBoolean(returnVal))
            {

                for (int eachPathInfo = 0; eachPathInfo < pathInfo.Length; eachPathInfo++)
                {
                    if (pathInfo[eachPathInfo].targetInfo.id == argWinMonitorID)
                    {
                        currentMode.ScalingOptions = new List<uint>();
                        currentMode.ScalingOptions.Add((uint)pathInfo[eachPathInfo].targetInfo.scaling);
                    }
                }
            }
            else
                Console.WriteLine("GetCurrentMode::QDC Call Error! Return value {0}", returnVal);

            return currentMode;
        }
        internal static bool SetDisplayMode(DisplayMode argSetMode, DisplayInfo argDisplayInfo, List<DisplayInfo> argEnumeratedDisplays)
        {
            DisplayConfigType configType = DisplayConfigType.None;
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            if (Convert.ToBoolean(returnVal))
                Console.WriteLine("SetDisplayMode::GetDisplayConfigBufferSizes Call Error! Return value {0}", returnVal);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ONLY_ACTIVE_PATHS, ref numPathArrayElements, pathInfo, ref numModeInfoArrayElements, modeInfo, topologyId);
            if (Convert.ToBoolean(returnVal))
            {
                Console.WriteLine("SetDisplayMode::QDC Call Error! Return value {0}", returnVal);
                return false;
            }
            else
            {
                if (numModeInfoArrayElements == 2 && numPathArrayElements == 1)
                    configType = DisplayConfigType.SD;
                else if (numModeInfoArrayElements == 3 && numPathArrayElements == 2)
                    configType = DisplayConfigType.DDC;
                else if (numModeInfoArrayElements == 4 && numPathArrayElements == 3)
                    configType = DisplayConfigType.TDC;
                else if (numModeInfoArrayElements == 4 && numPathArrayElements == 2)
                    configType = DisplayConfigType.ED;
                else if (numModeInfoArrayElements == 6 && numPathArrayElements == 3)
                    configType = DisplayConfigType.TED;
                FillModeInfoPathInfo(ref pathInfo, ref modeInfo, argSetMode, configType, argDisplayInfo.AdapterName, argDisplayInfo.WindowsMonitorID, argEnumeratedDisplays);

                returnVal = Interop.SetDisplayConfig(numPathArrayElements, pathInfo, numModeInfoArrayElements, modeInfo, SDC_APPLY | SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_SAVE_TO_DATABASE | SDC_ALLOW_CHANGES | SDC_NO_OPTIMIZATION);
                if (Convert.ToBoolean(returnVal))
                {
                    Console.WriteLine("SetDisplayMode::SDC Call Error! Return value {0}", returnVal);
                    return false;
                }
                else
                    Thread.Sleep(5000);
            }
            return true;
        }
        internal static List<DisplayMode> GetSupportedModes(string argAdapterName)
        {
            DEVMODE mode = new DEVMODE();
            mode.dmSize = (short)Marshal.SizeOf(mode);
            List<DisplayMode> modeList = new List<DisplayMode>();

            int modeIndex = 0;
            DisplayMode currentRes = new DisplayMode();
            currentRes.ScalingOptions = new List<uint>();

            Interop.EnumDisplaySettings(argAdapterName, 0, ref mode);
            int minSupportedHzRes = 0;
            int minSupportedVtRes = 0;
            switch (mode.dmDisplayOrientation)
            {
                case ScreenOrientation.Angle0:
                case ScreenOrientation.Angle180:
                    minSupportedHzRes = 1024;
                    minSupportedVtRes = 768;
                    break;
                case ScreenOrientation.Angle90:
                case ScreenOrientation.Angle270:
                    minSupportedHzRes = 768;
                    minSupportedVtRes = 1024;
                    break;
            }

            while (Interop.EnumDisplaySettings(argAdapterName, modeIndex, ref mode))
            {
                if (mode.dmPelsWidth >= minSupportedHzRes && mode.dmPelsHeight >= minSupportedVtRes && mode.dmBitsPerPel >= 32)
                {
                    DisplayMode getMode = modeList.GetExistingMode(mode);
                    if (getMode.HzRes.Equals(0))
                    {
                        currentRes.ScalingOptions = new List<uint>();
                        currentRes.HzRes = (uint)mode.dmPelsWidth;
                        currentRes.VtRes = (uint)mode.dmPelsHeight;
                        currentRes.Bpp = (uint)mode.dmBitsPerPel;
                        currentRes.RR = (uint)mode.dmDisplayFrequency;
                        if (!mode.dmDisplayFlags.Equals(0))
                        {
                            currentRes.InterlacedFlag = 1;
                            //currentRes.RR *= 2;
                        }
                        else
                            currentRes.InterlacedFlag = (uint)mode.dmDisplayFlags;
                        currentRes.ScalingOptions.Add((uint)mode.dmDisplayFixedOutput + 1);
                        modeList.Add(currentRes);
                    }
                    else
                        getMode.ScalingOptions.Add((uint)mode.dmDisplayFixedOutput + 1);
                }
                modeIndex++;
            }
            return modeList;
        }
    }
}