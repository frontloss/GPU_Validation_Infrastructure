namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    class DriverInterop
    {
        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int D3DKMTOpenAdapterFromHdc([In, Out] ref D3DKMT_OPENADAPTERFROMHDC openAdapterData);

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int D3DKMTCloseAdapter(ref D3DKMT_CLOSEADAPTER closeAdapter);

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern int D3DKMTEscape(ref D3DKMT_ESCAPE escapeData);

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern bool DeleteDC(IntPtr hdc);

        [DllImport("gdi32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        internal static extern IntPtr CreateDC(string lpszDriver, string lpszDevice, string lpszOutput, IntPtr lpInitData);

        [DllImport("kernel32.dll", CallingConvention = CallingConvention.StdCall)]
        internal static extern int GetLastError();
    }
}
