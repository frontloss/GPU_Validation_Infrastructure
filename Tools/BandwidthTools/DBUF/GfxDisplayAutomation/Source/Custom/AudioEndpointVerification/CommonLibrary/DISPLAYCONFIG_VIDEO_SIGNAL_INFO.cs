namespace AudioEndpointVerification
{
    using System;

    internal struct DISPLAYCONFIG_2DREGION
    {
        public UInt32 cx;
        public UInt32 cy;
    }

    internal struct DISPLAYCONFIG_VIDEO_SIGNAL_INFO
    {
        public UInt64 pixelRate;
        public DISPLAYCONFIG_RATIONAL hSyncFreq;
        public DISPLAYCONFIG_RATIONAL vSyncFreq;
        public DISPLAYCONFIG_2DREGION activeSize;
        public DISPLAYCONFIG_2DREGION totalSize;
        public UInt32 videoStandard;
        public DISPLAYCONFIG_SCANLINE_ORDERING scanLineOrdering;
    }
}
