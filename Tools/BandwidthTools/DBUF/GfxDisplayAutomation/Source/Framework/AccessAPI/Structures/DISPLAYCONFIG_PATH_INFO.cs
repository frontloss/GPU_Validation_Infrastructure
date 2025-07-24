namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;

    internal struct DISPLAYCONFIG_PATH_INFO
    {
        public DISPLAYCONFIG_PATH_SOURCE_INFO sourceInfo;
        public DISPLAYCONFIG_PATH_TARGET_INFO targetInfo;
        public UInt32 flags;

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append("DISPLAYCONFIG_PATH_INFO:");
            PrintConfig.Append("DISPLAYCONFIG_PATH_SOURCE_INFO:" + sourceInfo.ToString() + " ");
            PrintConfig.Append("DISPLAYCONFIG_PATH_TARGET_INFO:" + targetInfo.ToString() + " ");
            PrintConfig.Append("flags:" + flags + " \n");

            return PrintConfig.ToString();
        }
    }
}
