namespace AudioEndpointVerification
{
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    public struct GFX_ESCAPE_HEADER
    {
        public uint Size;
        public uint CheckSum;
        public uint EscapeCode;
        public uint Reserved;
    }
}
