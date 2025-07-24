namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;

    internal struct DISPLAYCONFIG_SOURCE_MODE
    {
        public UInt32 width;
        public UInt32 height;
        public DISPLAYCONFIG_PIXELFORMAT pixelFormat;
        public POINTL position;

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append("DISPLAYCONFIG_SOURCE_MODE: width:" + width + " ");
            PrintConfig.Append("height:" + height + " ");
            PrintConfig.Append("pixelFormat:" + pixelFormat + " ");
            PrintConfig.Append("position:" + position.px + " " + position.py + "\n");
            
            return PrintConfig.ToString();
        }
    }
}
