namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Drawing;
    using System.Runtime.InteropServices;

    internal static class Interop
    {
        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int GetDisplayConfigBufferSizes(UInt32 Flags, ref UInt32 pNumPathArrayElements, ref UInt32 pNumModeInfoArrayElements);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int QueryDisplayConfig(UInt32 Flags, ref UInt32 pNumPathArrayElements, [Out] DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, ref UInt32 pNumModeInfoArrayElements, [Out] DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, DISPLAYCONFIG_TOPOLOGY_ID pCurrentTopologyId);

        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplayDevices(string lpDevice, uint iDevNum, ref DISPLAY_DEVICE lpDisplayDevice, uint dwFlags);

        [DllImport("setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        public static extern IntPtr SetupDiGetClassDevs(ref Guid ClassGuid, StringBuilder Enumerator, IntPtr hwndParent, int Flags);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiEnumDeviceInfo(IntPtr hDevInfo, uint MemberIndex, ref DisplayInfoData devInfo);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiGetDeviceRegistryProperty(IntPtr hDevInfo, ref DisplayInfoData dispInfo, uint Property, ref uint PropertyRegDataType, StringBuilder PropertyBuffer, uint PropertyBufferSize, ref uint RequiredSize);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiGetDeviceInstanceId(IntPtr hDevInfo, ref DisplayInfoData dispInfo, StringBuilder DeviceInstanceId, uint DeviceInstanceIdSize, ref uint RequiredSize);

        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplaySettings(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int SetDisplayConfig(UInt32 numPathArrayElements, DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, UInt32 numModeInfoArrayElements, DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, UInt32 Flags);

        //[DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        //internal static extern int ChangeDisplaySettingsEx(
        //    string deviceName,
        //    ref DEVMODE lpDevmode,
        //    string hwnd,
        //    uint dwFlags,
        //    string lParam
        //    );
    }
}