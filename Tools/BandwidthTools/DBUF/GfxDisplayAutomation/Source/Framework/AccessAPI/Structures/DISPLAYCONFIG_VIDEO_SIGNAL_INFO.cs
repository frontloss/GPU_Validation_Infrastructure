namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;

    internal struct DISPLAYCONFIG_VIDEO_SIGNAL_INFO
    {
        public UInt64 pixelRate;
        public DISPLAYCONFIG_RATIONAL hSyncFreq;
        public DISPLAYCONFIG_RATIONAL vSyncFreq;
        public DISPLAYCONFIG_2DREGION activeSize;
        public DISPLAYCONFIG_2DREGION totalSize;
        public UInt32 videoStandard;
        public DISPLAYCONFIG_SCANLINE_ORDERING scanLineOrdering;

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append("DISPLAYCONFIG_VIDEO_SIGNAL_INFO: pixelRate:" + pixelRate + " ");
            PrintConfig.Append("hSyncFreq num:" + hSyncFreq.Numerator + " Denom:" + hSyncFreq.Denominator + " ");
            PrintConfig.Append("vSyncFreq Num:" + vSyncFreq + " Denom:" + vSyncFreq.Denominator + " ");
            PrintConfig.Append("activeSize cx:" + activeSize.cx + " cy:" + activeSize.cy + " ");
            PrintConfig.Append("totalSize cx:" + totalSize.cx + " cy:" + totalSize.cy + " ");
            PrintConfig.Append("videoStandard:" + videoStandard + " ");
            PrintConfig.Append("scanLineOrdering:" + scanLineOrdering + "\n");
           
            return PrintConfig.ToString();
        }
    }
}
