namespace Intel.VPG.Display.Automation
{
    using System;

    internal struct DISPLAYCONFIG_MODE_INFO
    {
        public DISPLAYCONFIG_MODE_INFO_TYPE infoType;
        public UInt32 id;
        public LUID adapterId;
        public ModeUnion mode;
    }
}
