namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    internal struct DisplayMode
    {
        internal uint Angle;
        internal uint HzRes;
        internal uint VtRes;
        internal uint RR;
        internal uint Bpp;
        internal uint InterlacedFlag;
        internal List<uint> ScalingOptions;
        internal uint PixelClk;
        internal uint HTotalVTotal;

        public override string ToString()
        {
            return string.Format("{0}x{1} {2}Bit {3}{4}Hz {5}Deg {6}", HzRes, VtRes, Bpp, RR,
                InterlacedFlag.Equals(0) ? "p" : "i", Angle,
                (null != this.ScalingOptions) ? (DISPLAYCONFIG_SCALING)this.ScalingOptions.FirstOrDefault() : DISPLAYCONFIG_SCALING.None);
        }
        internal DisplayMode Clone()
        {
            DisplayMode newMode = new DisplayMode()
            {
                Angle = this.Angle,
                Bpp = this.Bpp,
                HzRes = this.HzRes,
                InterlacedFlag = this.InterlacedFlag,
                RR = this.RR,
                VtRes = this.VtRes,
                PixelClk = this.PixelClk,
                HTotalVTotal = this.HTotalVTotal
            };
            if (null != this.ScalingOptions)
            {
                newMode.ScalingOptions = new List<uint>();
                newMode.ScalingOptions.AddRange(this.ScalingOptions);
            }
            return newMode;
        }
    }
}