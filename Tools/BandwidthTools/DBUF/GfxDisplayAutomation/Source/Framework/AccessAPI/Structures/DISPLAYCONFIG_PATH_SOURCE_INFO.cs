namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;

    internal struct DISPLAYCONFIG_PATH_SOURCE_INFO
    {
        public LUID adapterId;
        public UInt32 id;
        public UInt32 modeInfoIdx;
        public UInt32 statusFlags;

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append("SourceInfo: adapterId Low:" + adapterId.LowPart + "  High:" + adapterId.HighPart);
            PrintConfig.Append(" ID:"+ id);
            PrintConfig.Append(" modeInfoIdx:"+ modeInfoIdx + " ");
            PrintConfig.Append("statusFlags:"+ statusFlags + "\n");
            return PrintConfig.ToString();
        }
    }
}
