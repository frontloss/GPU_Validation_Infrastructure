namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    public struct RR_Scaling
    {
        public uint supportedRR;
        public ushort InterlaceFlag;
        public List<uint> ScalingOption;
    };
}
