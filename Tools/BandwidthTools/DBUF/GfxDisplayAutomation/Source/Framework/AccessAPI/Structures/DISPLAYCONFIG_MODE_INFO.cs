namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;

    internal struct DISPLAYCONFIG_MODE_INFO
    {
        public DISPLAYCONFIG_MODE_INFO_TYPE infoType;
        public UInt32 id;
        public LUID adapterId;
        public ModeUnion mode;

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append("DISPLAYCONFIG_MODE_INFO:");
            PrintConfig.Append("DISPLAYCONFIG_MODE_INFO_TYPE:" + infoType + " ");
            PrintConfig.Append("id:" + id + " ");
            PrintConfig.Append("adapterId Low:" + adapterId.LowPart + ", High:" + adapterId.HighPart + " \n");
            PrintConfig.Append("ModeUnion:" + mode.ToString() + " ");

            return PrintConfig.ToString();
        }
    }
}
