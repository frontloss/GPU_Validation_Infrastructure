namespace AudioEndpointVerification
{
    using System;
    using System.Text;
    using System.Runtime.InteropServices;
    using System.Drawing;

    internal static class Interop
    {
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplaySettings(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode);

        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplayDevices(string lpDevice, uint iDevNum, ref DISPLAY_DEVICE lpDisplayDevice, uint dwFlags);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int GetDisplayConfigBufferSizes(UInt32 Flags, ref UInt32 pNumPathArrayElements, ref UInt32 pNumModeInfoArrayElements);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int QueryDisplayConfig(UInt32 Flags, ref UInt32 pNumPathArrayElements, [Out] DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, ref UInt32 pNumModeInfoArrayElements, [Out] DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, DISPLAYCONFIG_TOPOLOGY_ID pCurrentTopologyId);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int SetDisplayConfig(UInt32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, UInt32 numModeInfoArrayElements, DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, UInt32 Flags);

        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int ChangeDisplaySettingsEx(
            string deviceName,
            ref DEVMODE lpDevmode,
            string hwnd,
            uint dwFlags,
            string lParam
            );

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern void SetCursorPos(int X, int Y);

        [DllImport("setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern IntPtr SetupDiGetClassDevs(           // 1st form using a ClassGUID
           ref Guid ClassGuid,
           StringBuilder Enumerator,
           IntPtr hwndParent,
           int Flags
        );

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
        public static extern int ExtEscape(
            IntPtr hdc,
            int nEscape,
            int cbInput,
            IntPtr lpszInData,
            int cbOutput,
            IntPtr lpszOutData
        );
        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTOpenAdapterFromHdc(
            [In, Out] ref D3DKMT_OPENADAPTERFROMHDC openAdapterData
        );
        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTEscape(
             ref D3DKMT_ESCAPE escapeData
        );
        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern int D3DKMTCloseAdapter(
            ref D3DKMT_CLOSEADAPTER closeAdapter
        );

    }
}
