namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Runtime.InteropServices;
    using System.Drawing;

    internal static class Interop
    {
        const string WiGig = "WiGig.dll";
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplaySettings(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode);

        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplaySettingsEx(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode, int dwFlags);

        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplayDevices(string lpDevice, uint iDevNum, ref DISPLAY_DEVICE lpDisplayDevice, uint dwFlags);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int GetDisplayConfigBufferSizes(UInt32 Flags, ref UInt32 pNumPathArrayElements, ref UInt32 pNumModeInfoArrayElements);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int QueryDisplayConfig(UInt32 Flags, ref UInt32 pNumPathArrayElements, [Out] DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, ref UInt32 pNumModeInfoArrayElements, [Out] DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, DISPLAYCONFIG_TOPOLOGY_ID pCurrentTopologyId);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int QueryDisplayConfig(UInt32 Flags, ref UInt32 pNumPathArrayElements, [Out] DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, ref UInt32 pNumModeInfoArrayElements, [Out] DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, ref DISPLAYCONFIG_TOPOLOGY_ID pCurrentTopologyId);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int SetDisplayConfig(UInt32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, UInt32 numModeInfoArrayElements, DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, UInt32 Flags);

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuEnableLID", CallingConvention = CallingConvention.Cdecl)]
        public static extern DVMU4_STATUS EnableLID(byte p, byte Delay, bool seconds, bool Connect); 

        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int ChangeDisplaySettingsEx(
            string deviceName,
            ref DEVMODE lpDevmode,
            string hwnd,
            uint dwFlags,
            string lParam
            );

        [DllImport("user32.dll", EntryPoint = "SendMessage", SetLastError = true)]
        internal static extern IntPtr SendMessage(IntPtr hWnd, Int32 Msg, IntPtr wParam, IntPtr lParam);
        
        [DllImport("user32.dll", EntryPoint = "SystemParametersInfo")]
        internal static extern bool SystemParametersInfo(uint uiAction, uint uiParam, string pvParam, uint fWinIni);

        [DllImport("user32.dll")]
        internal static extern int ShowWindow(IntPtr hwnd, int command);
        
        [DllImport("user32.dll", SetLastError = true)]
        internal static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
        
        [DllImport("user32.dll", SetLastError = true)]
        internal static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);

        internal delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
        [DllImport("user32.dll")]
        internal static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        internal static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);

        [DllImport("user32.dll")]
        internal static extern IntPtr LoadCursorFromFile(string lpFileName);

        [DllImport("user32.dll")]
        internal static extern bool SetSystemCursor(IntPtr hcur, uint id);
        
        [DllImport("user32.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
        internal static extern void mouse_event(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern void SetCursorPos(int X, int Y);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern bool GetCursorPos(out Point pt);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool GetCursorInfo(out cursorInfo pci);
        [DllImport("User32.dll")]
        public static extern int SetForegroundWindow(IntPtr point);

        [DllImport("setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern IntPtr SetupDiGetClassDevs(           // 1st form using a ClassGUID
           ref Guid ClassGuid,
           StringBuilder Enumerator,
           IntPtr hwndParent,
           int Flags
        );

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiEnumDeviceInfo(
            IntPtr hDevInfo,
            uint MemberIndex,
            ref DisplayInfoData devInfo);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiGetDeviceRegistryProperty(
            IntPtr hDevInfo,
            ref DisplayInfoData dispInfo,
            uint Property,
            ref uint PropertyRegDataType,
            StringBuilder PropertyBuffer,
            uint PropertyBufferSize,
            ref uint RequiredSize);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiGetDeviceInstanceId(
            IntPtr hDevInfo,
            ref DisplayInfoData dispInfo,
            StringBuilder DeviceInstanceId,
            uint DeviceInstanceIdSize,
            ref uint RequiredSize);

        [DllImport("kernel32.dll", CallingConvention = CallingConvention.StdCall)]
        public static extern int GetLastError();

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern IntPtr CreateDC(
            string lpszDriver,
            string lpszDevice,
            string lpszOutput,
            IntPtr lpInitData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern bool DeleteDC(IntPtr hdc);

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTOpenAdapterFromHdc(
            [In, Out] ref D3DKMT_OPENADAPTERFROMHDC openAdapterData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTEscape(
             ref D3DKMT_ESCAPE escapeData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int ExtEscape(
            IntPtr hdc,
            int nEscape,
            int cbInput,
            IntPtr lpszInData,
            int cbOutput,
            IntPtr lpszOutData
        );

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTCloseAdapter(
            ref D3DKMT_CLOSEADAPTER closeAdapter
        );

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuOpen", CallingConvention = CallingConvention.Cdecl)]
        public static extern DVMU4_STATUS Open(Int32 num);

        //Entry Point to Get all the DVMu DEVICE id's Connected
        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuGetAllDevices", CallingConvention = CallingConvention.Cdecl)]
        public static extern DVMU4_STATUS DvmuGetAllDevices();

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuProgramEdid", CallingConvention = CallingConvention.Cdecl)]
        public static extern DVMU4_STATUS ProgramEdid(DVMU_PORT edid, byte[] data, ushort size, [System.Runtime.InteropServices.MarshalAsAttribute(System.Runtime.InteropServices.UnmanagedType.I1)] bool reset);

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuEnableHPD", CallingConvention = CallingConvention.Cdecl)]
        public static extern DVMU4_STATUS EnableHPD(DVMU_PORT port, Int16 delay, [MarshalAsAttribute(UnmanagedType.I1)] bool seconds, [MarshalAsAttribute(UnmanagedType.I1)] bool connect);

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuGetLastErrorStr", CallingConvention = CallingConvention.Cdecl)]
        public static extern System.IntPtr GetLastErrorStr_IntPtr();

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuSelectActivePort", CallingConvention = CallingConvention.Cdecl)]
        public static extern DVMU4_STATUS SelectActivePort(DVMU_PORT input);

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuReadHdmiByte", CallingConvention = CallingConvention.Cdecl)]
        public static extern DVMU4_STATUS ReadHdmiRegistry(byte address, byte offset, out byte value);

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuFetchVideoData")]
        public static extern DVMU4_STATUS FetchVideoData(DVMU_PORT port, [InAttribute()] [MarshalAsAttribute(UnmanagedType.LPStr)] string filename, int frameCount);

        /// Return Type: DVMU_STATUS
        ///input: DVMU_SOURCE
        ///meas: DVMU_MEASUREMENTS*
        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuGetPortTimings")]
        public static extern DVMU4_STATUS GetPortMeasurements(DVMU_PORT input, out DVMU_MEASUREMENTS meas);

        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "GetBmpFromFrame")]
        public static extern DVMU4_STATUS GetBmpFromFrame([InAttribute()] [MarshalAsAttribute(UnmanagedType.LPStr)] string filename, [InAttribute()] [MarshalAsAttribute(UnmanagedType.LPStr)] string filename1, int hieght, int width);

        /// Return Type: DVMU4_STATUS
        ///input: DVMU_SOURCE
        ///crc: DVMU_CRC*
        [DllImportAttribute("Dvmu4Api.dll", EntryPoint = "DvmuGetCRC")]
        public static extern DVMU4_STATUS GetCRC(DVMU_PORT input, out uint crc, bool check_valid_video);

        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int SetVxdWNICReceiverArival(WiGigEdidDetails argEdidInfo);
        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int SetVxdWNICRFKill();
        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int SetVxdWNICRFLinkLost();
        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int readMMIOReg(UInt32 offset, ref UInt32 value);
        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int CaptureTFDForDecode();
        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int SetFrameSizeAdjustment(UInt32 TargetFrameAdj);
        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int GetCurrentDisplayConfig();

        [DllImport(WiGig, SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int DLLExit();

        [DllImport("kernel32.dll")]
        public static extern IntPtr LoadLibrary(string dllToLoad);
        [DllImport("kernel32.dll")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procedureName);
        [DllImport("kernel32.dll")]
        public static extern bool FreeLibrary(IntPtr hModule);
    }
}
