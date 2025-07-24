namespace Intel.VPG.Display.Automation
{
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    public struct GFX_ESCAPE_HEADER_T
    {
        public uint ulReserved;
        public uint ulMinorInterfaceVersion;
        public uint uiMajorEscapeCode;
        public uint uiMinorEscapeCode;
    }
}
