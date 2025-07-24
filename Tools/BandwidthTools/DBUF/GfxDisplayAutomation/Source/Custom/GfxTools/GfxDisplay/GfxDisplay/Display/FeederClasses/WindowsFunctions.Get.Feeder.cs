namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using System.Runtime.InteropServices;

    internal static partial class WindowsFunctions
    {
        private const int DISPLAY_DEVICE_MIRRORING_DRIVER = 8;

        private static Dictionary<DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY, string> _displayTypeMap = null;

        private static void AddDisplay(uint argWinMonID, string argDisplayType, List<DisplayInfo> argDisplaysList, uint argIsActive)
        {
            int count = argDisplaysList.Count(dI => dI.DisplayType.StartsWith(argDisplayType));
            DisplayInfo displayInfo = new DisplayInfo() { DisplayType = argDisplayType, WindowsMonitorID = argWinMonID, IsActive = Convert.ToBoolean(argIsActive) };
            if (!count.Equals(0))
                displayInfo.DisplayType += string.Concat("_", count + 1);
            displayInfo.AdapterName = GetDeviceAdapterName(argWinMonID);
            argDisplaysList.Add(displayInfo);
        }
        private static Dictionary<DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY, string> DisplayTypeMap
        {
            get
            {
                if (null == _displayTypeMap)
                {
                    _displayTypeMap = new Dictionary<DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY, string>();
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15, "CRT");
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL, "EDP");
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI, "HDMI");
                    _displayTypeMap.Add(DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL, "DP");
                }
                return _displayTypeMap;
            }
        }
        private static string GetDeviceAdapterName(uint argWindowsMonitorID)
        {
            string deviceName = string.Empty;
            List<DisplayInfoFromDevMngr> dispDriverKeyInfo = GetDriverKeyInfo();
            DisplayInfoFromDevMngr displayDevInfo = dispDriverKeyInfo.Where(dInfo => dInfo.DeviceInstanceId.Contains(argWindowsMonitorID.ToString())).FirstOrDefault();
            if (!string.IsNullOrEmpty(displayDevInfo.DriverKey))
            {
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
                            if (monitorName.DeviceID.Contains(displayDevInfo.DriverKey))
                                return displayDevice.DeviceName;
                            monitorName.cb = Marshal.SizeOf(monitorName);
                        }
                    }
                    displayDevice.cb = Marshal.SizeOf(displayDevice);
                }
            }
            return deviceName;
        }
        private static List<DisplayInfoFromDevMngr> GetDriverKeyInfo()
        {
            const int SPDRP_DRIVER = 0x00000009;  // Driver (R/W)
            const int SPDRP_ADDRESS = 0x0000001C;  // Device Address (R)

            List<DisplayInfoFromDevMngr> DispDevInfo = new List<DisplayInfoFromDevMngr>();
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

                    displayInfoFrmDevMngr.DeviceInstanceId = DeviceInstanceId.ToString();
                    displayInfoFrmDevMngr.DriverKey = PropertyBuffer.ToString();
                    DispDevInfo.Add(displayInfoFrmDevMngr);
                }
            }
            lastError = Marshal.GetLastWin32Error();
            return DispDevInfo;
        }
    }
}