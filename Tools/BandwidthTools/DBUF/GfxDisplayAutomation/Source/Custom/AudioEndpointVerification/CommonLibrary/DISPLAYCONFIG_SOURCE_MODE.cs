namespace AudioEndpointVerification
{
    using System;

    internal struct POINTL
    {
        public int px;
        public int py;
    }

    internal struct DISPLAYCONFIG_SOURCE_MODE
    {
        public UInt32 width;
        public UInt32 height;
        public DISPLAYCONFIG_PIXELFORMAT pixelFormat;
        public POINTL position;
    }
}
