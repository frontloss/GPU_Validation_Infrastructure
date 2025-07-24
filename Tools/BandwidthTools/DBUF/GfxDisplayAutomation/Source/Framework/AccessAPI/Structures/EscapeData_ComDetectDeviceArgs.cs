namespace Intel.VPG.Display.Automation
{
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    public class EscapeData_ComDetectDeviceArgs
    {
        public GFX_ESCAPE_HEADER header;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 145 /*Size of escape data structure*/)]
        public byte[] dataBytes;
    }
}
