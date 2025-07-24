namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    internal struct D3DKMT_CLOSEADAPTER
    {
        public UInt32 hAdapter;
    }
}
