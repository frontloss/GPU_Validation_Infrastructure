namespace Intel.VPG.Display.Automation
{
    using System;

    internal class NativeDTD
    {
        internal byte PixelClock_LSB;//LSB Of Pixel Clock Value
        internal byte PixelClock_MSB;//MSB Of Pixel Clock Value, Actual Value=Value/10000 MHz

        internal byte HActive_LSB;//LSB of Horizontal Active
        internal byte HBlank_LSB;//LSB of Horizontal Blanking
        internal byte HBlank_MSB;//MSB of Hozrizontal Blanking
        internal byte HActive_MSB;//MSB of Horizontal Active

        internal byte VActive_LSB;//LSB of Vertical Active
        internal byte VBlank_LSB;//LSB of Vertical Blanking
        internal byte VBlank_MSB;//MSB of Vertical Blanking
        internal byte VActive_MSB;//MSB of Vertical Active

        internal byte Interlaced;//0 Non Interlaced
        //1 Interlaced

        internal NativeDTD(byte[] DTD_Data)
        {
            byte UpperNibble_Mask = 240;//"F0"
            byte LowerNibble_Mask = 15;//"0F"

            PixelClock_LSB = DTD_Data[0];
            PixelClock_MSB = DTD_Data[1];
            HActive_LSB = DTD_Data[2];
            HBlank_LSB = DTD_Data[3];

            HActive_MSB = Convert.ToByte((DTD_Data[4] & UpperNibble_Mask));
            HBlank_MSB = Convert.ToByte(DTD_Data[4] & LowerNibble_Mask);

            VActive_LSB = DTD_Data[5];
            VBlank_LSB = DTD_Data[6];

            VActive_MSB = Convert.ToByte((DTD_Data[7] & UpperNibble_Mask));
            VBlank_MSB = Convert.ToByte(DTD_Data[7] & LowerNibble_Mask);

            Interlaced = Convert.ToByte(DTD_Data[17] & 0x80);
        }
    }
}