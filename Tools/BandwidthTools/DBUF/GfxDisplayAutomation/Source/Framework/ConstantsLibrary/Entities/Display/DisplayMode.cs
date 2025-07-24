namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Text;
    public struct DisplayMode : IEqualityComparer<DisplayMode>
    {
        public uint Angle;
        public uint HzRes;
        public uint VtRes;
        public uint RR;
        public uint Bpp;
        public uint InterlacedFlag;
        public List<uint> ScalingOptions;
        public DisplayType display;
        public double pixelClock;

        public bool Equals(DisplayMode argDispMode1, DisplayMode argDispMode2)
        {
            if (argDispMode2.Angle == argDispMode1.Angle &&
                argDispMode2.HzRes == argDispMode1.HzRes &&
                argDispMode2.VtRes == argDispMode1.VtRes &&
                argDispMode2.RR == argDispMode1.RR &&
                argDispMode2.Bpp == argDispMode1.Bpp &&
                argDispMode2.InterlacedFlag == argDispMode1.InterlacedFlag &&
                argDispMode2.display == argDispMode1.display)
            {
                return true;
            }
            return false;
        }
        public int GetHashCode(DisplayMode argDispMode)
        {
            return argDispMode.HzRes.GetHashCode();
        }
        public void Copy(DisplayMode argDispMode1)
        {
            this.Angle = argDispMode1.Angle;
            this.Bpp = argDispMode1.Bpp;
            this.display = argDispMode1.display;
            this.HzRes = argDispMode1.HzRes;
            this.InterlacedFlag = argDispMode1.InterlacedFlag;
            this.RR = argDispMode1.RR;
            if (argDispMode1.ScalingOptions != null)
            {
                this.ScalingOptions = new List<uint>();
                foreach(uint currentScalingOption in argDispMode1.ScalingOptions)
                   this.ScalingOptions.Add(currentScalingOption);
            }
            this.VtRes = argDispMode1.VtRes;
        }
        public override string ToString()
        {
            StringBuilder displayModeStr = new StringBuilder();
            displayModeStr.Append(this.Angle.ToString()).Append("/");
            displayModeStr.Append(this.HzRes.ToString()).Append("/");
            displayModeStr.Append(this.VtRes.ToString()).Append("/");
            displayModeStr.Append(this.RR.ToString()).Append("/");
            displayModeStr.Append(this.Bpp.ToString()).Append("/");
            displayModeStr.Append(this.InterlacedFlag.ToString()).Append("/");

            displayModeStr.Append(display.ToString());
            return displayModeStr.ToString();
        }
    }
}