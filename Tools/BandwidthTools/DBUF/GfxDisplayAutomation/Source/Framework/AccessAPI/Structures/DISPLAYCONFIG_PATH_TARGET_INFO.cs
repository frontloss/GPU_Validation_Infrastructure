namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;

    internal struct DISPLAYCONFIG_PATH_TARGET_INFO
    {
        public LUID adapterId;
        public UInt32 id;
        public UInt32 modeInfoIdx;
        public DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY outputTechnology;
        public DISPLAYCONFIG_ROTATION rotation;
        public DISPLAYCONFIG_SCALING scaling;
        public DISPLAYCONFIG_RATIONAL refreshRate;
        public DISPLAYCONFIG_SCANLINE_ORDERING scanlineOrdering;
        public bool targetAvailable;
        public UInt32 statusFlags;

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append("adapterId: Low:" + adapterId.LowPart + " High:" + adapterId.HighPart);
            PrintConfig.Append(" ID:" + id);
            PrintConfig.Append(" modeInfoIdx:" + modeInfoIdx);
            PrintConfig.Append(" outputTechnology:" + outputTechnology);
            PrintConfig.Append(" rotation:" + rotation);
            PrintConfig.Append(" scaling:" + scaling);
            PrintConfig.Append(" refreshRate: Num:" + refreshRate.Numerator + " refreshRate: Deno:" + refreshRate.Denominator);
            PrintConfig.Append(" scanlineOrdering:" + scanlineOrdering);
            PrintConfig.Append(" targetAvailable:" + targetAvailable);
            PrintConfig.Append(" statusFlags:" + statusFlags + "\n");
            return PrintConfig.ToString();
        }
    }
}
