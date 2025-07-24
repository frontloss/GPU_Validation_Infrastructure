namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using IgfxExtBridge_DotNet;
    using System.Threading;
    using System.Text;
    using System.Text.RegularExpressions;
    using System.IO;
    using System.Diagnostics;
    using System.Runtime.InteropServices;

    internal static class DisplayActions
    {
        private static DisplayUtil _displayUtil = null;
        private const int TOTAL_DESCRIPTOR_BLOCK_SIZE = 18;
        private const byte MONITOR_NAME_EXISTS = 252;

        internal static List<DisplayInfo> EnumerateAllDisplays()
        {
            List<DisplayInfo> monIDList = new List<DisplayInfo>();
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, pathInfo, ref numModeInfoArrayElements, modeInfo, topologyId);
            if (!Convert.ToBoolean(returnVal))
            {
                foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                {
                    uint tempWinMonID = eachPath.targetInfo.id & 0x0FFFFFFF; //workaround for Threshold OS issue for Windows ID.

                    if (!tempWinMonID.Equals(0) && eachPath.targetInfo.targetAvailable && !monIDList.Any(UID => UID.WindowsMonitorID.Equals(tempWinMonID)))
                    {
                        DisplayInfo displayInfo = new DisplayInfo();
                        DriverEscape escapeData = new DriverEscape();
                        DriverEscapeData<uint, PORT> PortData = new DriverEscapeData<uint, PORT>() { input = tempWinMonID };
                        displayInfo.PortValue = escapeData.ParsePortName(PortData);
                        displayInfo.Port = PortData.output;
                        displayInfo.WindowsMonitorID = tempWinMonID;
                        displayInfo.DisplayType = GetWindowsDisplayType(eachPath);
                        displayInfo.IsActive = Convert.ToBoolean(eachPath.flags);
                        if (displayInfo.DisplayType == DisplayType.EDP)
                        {
                            DriverEscapeData<uint, DisplayType> PortType = new DriverEscapeData<uint, DisplayType>() { input = tempWinMonID };
                            escapeData.ParseConnectorType(PortType);
                            if (PortType.output == DisplayType.MIPI)
                                displayInfo.DisplayType = DisplayType.MIPI;
                        }
                        monIDList.Add(displayInfo);
                        monIDList.Sort((x, y) => x.Port.CompareTo(y.Port));
                    }
                }
                AssignCUIMonitorID(monIDList);
                monIDList.ForEach(dI =>
                    {
                        byte[] edidData = GetEDID(dI);
                        if (null != edidData)
                            AssignDisplayDataFromEDID(dI, edidData);
                        else
                            Console.WriteLine("EDID for {0} returned null!", dI.DisplayType);
                    });
                return monIDList;
            }
            return null;
        }
        internal static string GetDriverKey()
        {
            const int SPDRP_DRIVER = 0x00000009;  // Driver (R/W)
            const int SPDRP_ADDRESS = 0x0000001C;  // Device Address (R)

            Guid GUID_DEVINTERFACE_DISPLAY = new Guid(0x4D36E968, 0xE325, 0x11CE, 0xBF, 0xC1, 0x08, 0x00, 0x2B, 0xE1, 0x03, 0x18);
            StringBuilder Enumerator = new StringBuilder(@"PCI");
            DisplayInfoData displayInfoData = new DisplayInfoData();
            displayInfoData.Size = Marshal.SizeOf(displayInfoData);
            uint MemberIndex = 0;
            int lastError = 0;

            uint PropertyDataType = 0;
            StringBuilder PropertyBuffer = new StringBuilder(256);
            StringBuilder DeviceInstanceId = new StringBuilder(256);
            uint RequiredSize = 0;
            IntPtr DeviceInfoSet = new IntPtr();
            DeviceInfoSet = Interop.SetupDiGetClassDevs(ref GUID_DEVINTERFACE_DISPLAY, Enumerator, IntPtr.Zero, 0x04);
            lastError = Marshal.GetLastWin32Error();
            string driverHWID = GetDriverHWID();

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

                    if (driverHWID.Equals(DeviceInstanceId.ToString()))
                        return PropertyBuffer.ToString();
                }
            }
            lastError = Marshal.GetLastWin32Error();
            return string.Empty;
        }

        private static void AssignCUIMonitorID(List<DisplayInfo> argDisplayInfoList)
        {
            int DigitalDisplayCount = 0;
            foreach (DisplayInfo displayInfo in argDisplayInfoList)
            {
                //workaround for Threshold OS issue for Windows ID.
                uint tempWinID = displayInfo.WindowsMonitorID & 0x0FFFFFFF;

                switch (tempWinID >> ((tempWinID.ToString().Length) == 8 ? 24 : 16))
                {
                    case 1: // VGA
                        displayInfo.CUIMonitorID = 1;
                        break;
                    case 2: // TV
                    case 3: // DFP
                        displayInfo.CUIMonitorID = (uint)Math.Pow(2, 8 + DigitalDisplayCount++);
                        break;
                    case 4: // LFP
                        displayInfo.CUIMonitorID = 4096;
                        break;
                    default:
                        Console.WriteLine("Cannot find CUI UID for display " + displayInfo);
                        displayInfo.CUIMonitorID = 0;
                        break;
                }
            }
        }
        private static DisplayType GetWindowsDisplayType(DISPLAYCONFIG_PATH_INFO eachPath)
        {
            switch (eachPath.targetInfo.outputTechnology)
            {
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15:
                    return DisplayType.CRT;
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL:
                    return DisplayType.EDP;
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI:
                    return DisplayType.HDMI;
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL:
                    return DisplayType.DP;
                default:
                    return DisplayType.None;
            }
        }
        private static DisplayUtil DisplayUtil
        {
            get
            {
                if (null == _displayUtil)
                {
                    CommonExtensions.StartProcess("regsvr32", string.Concat(@"/s ", @"""", Directory.GetCurrentDirectory(), "\\", "IgfxExtBridge.dll", @""""));
                    Thread.Sleep(2000);
                    _displayUtil = new DisplayUtil();
                    Thread.Sleep(3000);
                    if (null == _displayUtil)
                        Console.WriteLine("SDK:: DisplayUtil instance not created! A reboot might be required.{0}", Environment.NewLine);
                }
                return _displayUtil;
            }
        }
        private static byte[] GetEDID(DisplayInfo argDisplayInfo)
        {
            byte[] EDIDData = new byte[256];
            IGFX_EDID_1_0 displayEDIDData = new IGFX_EDID_1_0();
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
            string errorDesc = "";

            displayEDIDData.dwDisplayDevice = argDisplayInfo.CUIMonitorID;
            DisplayUtil.GetEDIDData(ref displayEDIDData, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Console.WriteLine("SDK:{0}:Unable to get base EDID-{1}", igfxErrorCode, errorDesc);
                return null;
            }
            argDisplayInfo.BaseEDIDBlock = displayEDIDData.EDID_Data.Take(128).ToArray();

            IGFX_EDID_1_0 ceaEDIDData = new IGFX_EDID_1_0();
            for (uint i = 0; i < displayEDIDData.EDID_Data[126]; i++)
            {
                ceaEDIDData.dwDisplayDevice = argDisplayInfo.CUIMonitorID;
                ceaEDIDData.dwEDIDBlock = i + 1;
                DisplayUtil.GetEDIDData(ref ceaEDIDData, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Console.WriteLine("SDK:{0}:Unable to get CEA extn EDID-{1}", igfxErrorCode, errorDesc);
                    return null;
                }
                for (uint j = (i * 128); j < ((i + 1) * 128); j++)
                    displayEDIDData.EDID_Data[j + 128] = ceaEDIDData.EDID_Data[j];
            }
            if (null != ceaEDIDData.EDID_Data)
                argDisplayInfo.CEAExtnBlock = ceaEDIDData.EDID_Data.Take(128).ToArray();
            displayEDIDData.EDID_Data.CopyTo(EDIDData, 0);
            return EDIDData;
        }
        private static void AssignDisplayDataFromEDID(DisplayInfo argDisplayInfo, byte[] argEDIDData)
        {
            Dictionary<DTDCategory, byte[]> dtdBlockData = new Dictionary<DTDCategory, byte[]>();
            byte[] blockData = new byte[TOTAL_DESCRIPTOR_BLOCK_SIZE];
            bool hasMachineInfo = false;
            Enum.GetValues(typeof(DTDBlockInit)).Cast<DTDBlockInit>().ToList().ForEach(dtdEnum =>
            {
                blockData = GetDTDBlock(argEDIDData, dtdEnum, out hasMachineInfo);
                if (hasMachineInfo && !dtdBlockData.ContainsKey(DTDCategory.MachineName))
                    dtdBlockData.Add(DTDCategory.MachineName, blockData);
            });
            argDisplayInfo.DisplayName = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argDisplayInfo.DisplayType).Select(dI => dI.DisplayName).FirstOrDefault();
            if (argDisplayInfo.DisplayType != DisplayType.EDP || argDisplayInfo.DisplayType != DisplayType.MIPI)
            {
                if (dtdBlockData.ContainsKey(DTDCategory.MachineName))
                    argDisplayInfo.CompleteDisplayName = GetMachineName(dtdBlockData[DTDCategory.MachineName], argDisplayInfo.DisplayType);
                else
                    Console.WriteLine("EDID for {0} does not have machine name block!", argDisplayInfo.DisplayType);
            }

            if (string.IsNullOrEmpty(argDisplayInfo.CompleteDisplayName))
                argDisplayInfo.CompleteDisplayName = argDisplayInfo.DisplayName;

            argDisplayInfo.ManufacturerInfo = new byte[] { argEDIDData[8], argEDIDData[9] };
            argDisplayInfo.ManufacturerName = string.Concat(argEDIDData[9].ToHex(), argEDIDData[8].ToHex());
            argDisplayInfo.ProductInfo = new byte[] { argEDIDData[10], argEDIDData[11] };
            argDisplayInfo.ProductCode = string.Concat(argEDIDData[11].ToHex(), argEDIDData[10].ToHex());
        }
        private static string ToHex(this byte argByte)
        {
            return argByte.ToString("X").PadLeft(2, '0');
        }
        private static byte[] GetDTDBlock(byte[] argEdidRaw, DTDBlockInit argStart, out bool argHasMachineInfo)
        {
            byte[] dtdBlock = argEdidRaw.Skip((int)argStart).Take(TOTAL_DESCRIPTOR_BLOCK_SIZE).ToArray();
            argHasMachineInfo = dtdBlock.Contains(MONITOR_NAME_EXISTS);
            return dtdBlock;
        }
        private static string GetMachineName(byte[] argDTDData, DisplayType argDisplayType)
        {
            string machineName = string.Concat(
                 DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argDisplayType).Select(dI => dI.DisplayName).FirstOrDefault(),
                 " ",
                 ASCIIEncoding.ASCII.GetString(argDTDData.Skip(5).Take(13).ToArray())).Trim();
            return new Regex("\\n").Replace(machineName, string.Empty).Trim();
        }
        private static string GetDriverHWID()
        {
            Process process = CommonExtensions.StartProcess("devcon.exe", "find =display");
            process.WaitForExit();
            return process.StandardOutput.ReadToEnd().Split(':').FirstOrDefault();
        }
    }
}