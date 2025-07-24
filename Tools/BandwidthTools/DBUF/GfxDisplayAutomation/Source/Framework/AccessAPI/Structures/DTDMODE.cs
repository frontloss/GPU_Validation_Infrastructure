namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    internal struct DTDMODE
    {
        public UInt16 wPixelClock;

        byte ucHA_low;        // horiz. addresabel active w/o border
        byte ucHBL_low;       // horiz blank time w/ border
        byte ucHAHBL_high;

        byte ucVA_low;        // vert. addresabel active w/o border
        byte ucVBL_low;       // vert. blank time w/ border
        byte ucVAVBL_high;

        byte ucHSO_low;
        byte ucHSPW_low;
        byte ucVSOVSPW_low;
        byte ucHSVS_high;

        byte ucHIS_low;
        byte ucVIS_low;
        byte ucHISVIS_high;

        byte ucHBorder;
        byte ucVBorder;

        byte ucFlags;       // hsync & vsync polarity flags
        /*
           public UInt16 wReserved;
           public UInt32 pKgHALMode; */
        // corresponding KgHAL mode
        public UInt16 GetActiveWidth()
        {
            //for issue 3800027 - Unsupported modes shown in CUI Information Page
            // ANDing with 0x7FF is not required (it removes the 1st bit and hence returns wrong values)
            return (UInt16)(((ucHAHBL_high >> 4) << 8) | ucHA_low);// & 0x7FF);
        }
        public UInt16 GetActiveHeight()
        {
            return (UInt16)(((ucVAVBL_high >> 4) << 8) | ucVA_low);// & 0x7FF);
        }
        public UInt16 GetTotalWidth()
        {
            //#define EDID_TOTAL_WIDTH(_p) (((_p->ucHBL_high<<8) | (_p->ucHBL_low)) + (EDID_ACTIVE_WIDTH(_p)))
            return (UInt16)((((ucHAHBL_high & 0xF) << 8) | ucHBL_low) + GetActiveWidth());
        }
        public UInt16 GetTotalHeight()
        {
            //#define EDID_TOTAL_HEIGHT(_p) (((_p->ucVBL_high<<8) | (_p->ucVBL_low)) + (EDID_ACTIVE_HEIGHT(_p)))
            return (UInt16)((((ucVAVBL_high & 0xF) << 8) | ucVBL_low) + GetActiveHeight());
        }
        public double GetRefreshRate()
        {
            //#define EDID_REFRESH_RATE(_p) ((double)(_p->wPixelClock*10000)/(double)((EDID_TOTAL_WIDTH(_p) * EDID_TOTAL_HEIGHT(_p))))
            return (((double)(wPixelClock * 10000)) / (double)(GetTotalWidth() * GetTotalHeight()));
        }
    }
}