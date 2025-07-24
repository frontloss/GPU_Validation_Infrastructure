namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct DisplayInfoData
    {
        public int Size;
        public Guid ClassGuid;
        public IntPtr DevInst;
        public int Reserved;
    }
}