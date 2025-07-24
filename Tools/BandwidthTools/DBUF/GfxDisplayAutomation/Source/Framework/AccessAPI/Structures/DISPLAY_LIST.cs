namespace Intel.VPG.Display.Automation
{
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential, Pack = 1 /*To allocate 1 byte for char/bool*/)]
    public struct DISPLAY_LIST
    {
        public uint nDisplays;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
        public uint[] DisplayUID;
        public uint DeviceConfig;
        public char ConnectorIndex;
    };
}
