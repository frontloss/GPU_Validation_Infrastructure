namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    public class DTD
    {
        private int HActive;
        private int HBlank;
        private int VActive;
        private int VBlank;
        private bool IsInterlaced;

        public DisplayMode DisplayMode;

        public DTD(byte[] EDIDData, DisplayType argDisplayType)
        {
            NativeDTD tempDTD = new NativeDTD(EDIDData);
            initializeDTD(tempDTD, argDisplayType);
        }

        private void initializeDTD(NativeDTD tempDTD, DisplayType argDisplayType)
        {
            //Pixel Clock
            int tempClock = tempDTD.PixelClock_MSB;
            tempClock = tempClock << 8;
            tempClock = tempClock | tempDTD.PixelClock_LSB;

            //Horizontal Active
            HActive = tempDTD.HActive_MSB;
            HActive = HActive << 4;
            HActive = HActive | tempDTD.HActive_LSB;

            //Horizontal Blanking
            HBlank = tempDTD.HBlank_MSB;
            HBlank = HBlank << 8;
            HBlank = HBlank | tempDTD.HBlank_LSB;

            //Vertical Active
            VActive = tempDTD.VActive_MSB;
            VActive = VActive << 4;
            VActive = VActive | tempDTD.VActive_LSB;

            //Vertical Blanking
            VBlank = tempDTD.VBlank_MSB;
            VBlank = VBlank << 8;
            VBlank = VBlank | tempDTD.VBlank_LSB;

            //Interlaced
            IsInterlaced = (tempDTD.Interlaced == 0x80);

            int HTotal = HActive + HBlank;
            int VTotal = VActive + VBlank;

            //Refresh Rate
            int refreshRate = ((tempClock * 10000) + (HTotal * VTotal)/2) / (HTotal * VTotal);

            DisplayMode = new DisplayMode();
            DisplayMode.Angle = 0;
            DisplayMode.Bpp = 32;
            DisplayMode.HzRes = Convert.ToUInt32(HActive);
            DisplayMode.InterlacedFlag = Convert.ToUInt32(IsInterlaced);
            DisplayMode.RR = (uint)refreshRate;
            DisplayMode.VtRes = IsInterlaced ? Convert.ToUInt32(2 * VActive) : Convert.ToUInt32(VActive);
            DisplayMode.display = argDisplayType;
            DisplayMode.pixelClock = tempClock / 100;
            DisplayMode.ScalingOptions = new List<uint> { (uint)ScalingOptions.Maintain_Display_Scaling };
        }
    }
}