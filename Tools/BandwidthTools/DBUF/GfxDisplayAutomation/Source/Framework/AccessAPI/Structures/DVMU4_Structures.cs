namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    [StructLayoutAttribute(LayoutKind.Sequential)]
    public struct DVMU_SYNC_MEAS
    {
        /// unsigned int
        public uint frequency;

        /// unsigned int
        public uint pulse_width;

        /// unsigned int
        public uint front_porch;

        /// unsigned int
        public uint back_porch;
    }

    [StructLayoutAttribute(LayoutKind.Sequential)]
    public struct DVMU_RESOLUTION
    {
        /// unsigned int
        public uint height;

        /// unsigned int
        public uint width;
    }

    [StructLayoutAttribute(LayoutKind.Sequential)]
    public struct DVMU_MEASUREMENTS
    {
        /// unsigned int
        public uint pix_clk_freq;

        /// DVMU_SYNC_MEAS
        public DVMU_SYNC_MEAS vsync;

        /// DVMU_SYNC_MEAS
        public DVMU_SYNC_MEAS hsync;

        /// DVMU_RESOLUTION
        public DVMU_RESOLUTION res;

        /// BOOL->int
        [MarshalAsAttribute(UnmanagedType.Bool)]
        public bool interlaced;
    }

}
