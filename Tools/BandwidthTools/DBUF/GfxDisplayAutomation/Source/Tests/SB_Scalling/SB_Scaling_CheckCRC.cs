using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using System.IO;
using System;
using System.Windows.Forms;
using System.Drawing;

namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_CheckCRC : SB_Scaling_CaptureCRC
    {
        protected override void CRCComputation(DisplayType display, PORT port, DisplayInfo dispInfo, DisplayMode curMode)
        {
            string stPlatform = base.MachineInfo.PlatformDetails.Platform.ToString();
            CrcGoldenDataWrapper wrapper = new CrcGoldenDataWrapper(stPlatform, dispInfo, base.MachineInfo.OS.Type);

            uint currentCRC = 0;
            if (GetCRC(display, port, ref currentCRC) == true)
            {
                ModeCRC modeCRC = ConvertToCRCMode(curMode);

                uint tempCRC = wrapper.GetCRCFromFile(modeCRC);

                if (currentCRC == tempCRC)
                {
                    Log.Success("CRC Matched for {0}", curMode.GetCurrentModeStr(false));
                }
                else
                {
                    Log.Fail("CRC Not Matched. Expected:{0}, Current CRC:{1} for {2}: {3}",tempCRC,currentCRC, curMode.display, curMode.GetCurrentModeStr(false));
                }
            }
        }
        private ModeCRC ConvertToCRCMode(DisplayMode displayMode)
        {
            ModeCRC modeCRC = new ModeCRC();

            modeCRC.resolution = displayMode.HzRes + "x" + displayMode.VtRes;
            modeCRC.refreshRate = displayMode.RR;
            modeCRC.IsInterlaced = displayMode.InterlacedFlag;
            modeCRC.colorDepth = displayMode.Bpp;
            modeCRC.scaling = ((ScalingOptions)displayMode.ScalingOptions.First()).ToString();
            modeCRC.customHorizontalScaling = 0;
            modeCRC.customVerticalScaling = 0;
         
            return modeCRC;
        }
        private bool GetCRC(DisplayType display, PORT port, ref uint tempCRC)
        {
            bool status = true;
            CRCArgs obj = new CRCArgs();
            obj.displayType = display;
            obj.port = port;
            obj = AccessInterface.GetFeature<CRCArgs, CRCArgs>(Features.CRC, Action.GetMethod, Source.AccessAPI, obj);

            tempCRC = obj.CRCValue;

            if (tempCRC == 0)
                status = false;

            return status;
        }
    }
}
