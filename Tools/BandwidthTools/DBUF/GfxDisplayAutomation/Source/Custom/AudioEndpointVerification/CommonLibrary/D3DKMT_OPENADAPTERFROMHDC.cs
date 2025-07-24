namespace AudioEndpointVerification
{
    using System;
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    public struct D3DKMT_OPENADAPTERFROMHDC
    {
        public IntPtr hDc;
        public UInt32 hAdapter;
        public LUID AdapterLuid;
        public UInt32 VidPnSourceId;
    }
}
