namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class CrcGoldenDataArgs
    {
        public DisplayInfo displayInfo { get; set; }
        public DisplayMode displayMode { get; set; }
        public uint CRCValue { get; set; }
        public bool IsCRCPresent { get; set; }
        public bool IsPipeCRC { get; set; }
        public bool IsHDRContent { get; set; }
        public bool IsHDREnable { get; set; }

    }
}
