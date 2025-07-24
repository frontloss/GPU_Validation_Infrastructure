namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    public struct D3DKMT_ESCAPE
    {
        public UInt32 hAdapter;
        public UInt32 hDevice;
        public UInt32 Type;
        public UInt32 Flags;
        public IntPtr pPrivateDriverData;
        public UInt32 PrivateDriverDataSize;
        public UInt32 hContext;
    }
}
