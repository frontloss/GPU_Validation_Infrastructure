namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;
    using System.Text;

    class Interop
    {
        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int GetDisplayConfigBufferSizes(UInt32 Flags, ref UInt32 pNumPathArrayElements, ref UInt32 pNumModeInfoArrayElements);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int QueryDisplayConfig(UInt32 Flags, ref UInt32 pNumPathArrayElements, [Out] DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, ref UInt32 pNumModeInfoArrayElements, [Out] DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, DISPLAYCONFIG_TOPOLOGY_ID pCurrentTopologyId);

        [DllImport("User32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool EnumDisplayDevices(string lpDevice, uint iDevNum, ref DISPLAY_DEVICE lpDisplayDevice, uint dwFlags);

        [DllImport("setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern IntPtr SetupDiGetClassDevs(ref Guid ClassGuid, StringBuilder Enumerator, IntPtr hwndParent, int Flags);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiEnumDeviceInfo(IntPtr hDevInfo, uint MemberIndex, ref DisplayInfoData devInfo);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiGetDeviceRegistryProperty(IntPtr hDevInfo, ref DisplayInfoData dispInfo, uint Property, ref uint PropertyRegDataType, StringBuilder PropertyBuffer, uint PropertyBufferSize, ref uint RequiredSize);

        [DllImport(@"setupapi.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool SetupDiGetDeviceInstanceId(IntPtr hDevInfo, ref DisplayInfoData dispInfo, StringBuilder DeviceInstanceId, uint DeviceInstanceIdSize, ref uint RequiredSize);

    }
}
