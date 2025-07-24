namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    internal static class Interop
    {
        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int GetDisplayConfigBufferSizes(UInt32 Flags, ref UInt32 pNumPathArrayElements, ref UInt32 pNumModeInfoArrayElements);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern int QueryDisplayConfig(UInt32 Flags, ref UInt32 pNumPathArrayElements, [Out] DISPLAYCONFIG_PATH_INFO[] pPathInfoArray, ref UInt32 pNumModeInfoArrayElements, [Out] DISPLAYCONFIG_MODE_INFO[] pModeInfoArray, DISPLAYCONFIG_TOPOLOGY_ID pCurrentTopologyId);
 }
}