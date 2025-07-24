namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using System.Runtime.InteropServices;

    internal static partial class WindowsFunctions
    {
        private const int PRECISION3DEC = 1000;
        private const uint SDC_APPLY = 0x00000080;
        private const uint SDC_USE_SUPPLIED_DISPLAY_CONFIG = 0x00000020;
        private const uint SDC_SAVE_TO_DATABASE = 0x00000200;
        private const uint SDC_ALLOW_CHANGES = 0x00000400;
        private const uint SDC_NO_OPTIMIZATION = 0x00000100;


        private static List<string> GetDisplayAdapters()
        {
            List<string> displayAdaptersList = new List<string>();
            DISPLAY_DEVICE deviceName = new DISPLAY_DEVICE();
            deviceName.cb = Marshal.SizeOf(deviceName);
            uint devId = 0;
            while (Interop.EnumDisplayDevices(null, devId++, ref deviceName, 0))
                displayAdaptersList.Add(deviceName.DeviceName);
            return displayAdaptersList;
        }
        private static void ConvertRRtoRational(ulong ulXRes, ulong ulYRes, ulong ulRRate, bool bProgressiveMode, out uint pixelClock, out uint HtotalVtotal)
        {
            //fixed defines as per VESA spec
            //double flMarginPerct = 1.80;//size of top and bottom overscan margin as percentage of active vertical image
            double flCellGran = 8.0;  //cell granularity
            ulong ulMinPorch = 1;    // 1 line/char cell
            ulong ulVSyncRqd = 3;    //width of vsync in lines
            float flHSynchPerct = 8.0F;//width of hsync as a percentage of total line period
            float flMin_Vsync_BP = 550.0F;//Minimum time of vertical sync + back porch interval (us).
            double flBlankingGradient_M = 600.0;//The blanking formula gradient 
            double flBlankingOffset_C = 40.0;//The blanking formula offset
            double flBlankingScaling_K = 128.0;//The blanking formula scaling factor
            double flBlankingScalWeighing_J = 20.0;//The blanking formula scaling factor weighting
            //Spec defination ends here

            //Calculation of C',M'
            //C' = Basic offset constant
            //M' = Basic gradient constant
            double flCPrime = (flBlankingOffset_C - flBlankingScalWeighing_J) * (flBlankingScaling_K) / 256.0
                            + flBlankingScalWeighing_J;
            double flMPrime = flBlankingScaling_K / 256 * flBlankingGradient_M;

            bool bInterLaced = !bProgressiveMode;

            //calculation of timing paramters
            // Step 1: Round the Horizontal Resolution to nearest 8 pixel
            ulong ulHPixels = ulXRes;
            ulong ulHPixelsRnd = (ulong)(((int)((ulHPixels / flCellGran) + (0.5))) * flCellGran);

            // Step 2: Calculate Vertical line rounded to nearest integer   
            float flVLines = (float)ulYRes;
            ulong ulVLinesRnd = (ulong)((int)((bInterLaced ? flVLines / 2 : flVLines) + 0.5));

            // Step 3: Find the field rate required (only useful for interlaced)
            float flVFieldRateRqd = (float)(bInterLaced ? ulRRate * 2 : ulRRate);

            // Step 4 and 5: Calculate top and bottom margins, we assumed zero for now
            //assumption top/bottom margins are unused, if a requirement comes for use of
            //margin then it has to added as function input parameter
            ulong ulTopMargin = 0;
            ulong ulBottomMargin = 0;

            // Step 6: If Interlaced set this value which is used in the other calculations 
            float flInterLaced = (float)(bInterLaced ? 0.5 : 0);

            // Step 7: Estimate the Horizontal period in usec per line
            float flHPeriodEst = ((1 / flVFieldRateRqd) - (flMin_Vsync_BP / 1000000)) /
                                    (ulVLinesRnd + 2 * ulTopMargin + ulMinPorch + flInterLaced) * 1000000;

            // Step 8: Find the number of lines in V sync + back porch
            ulong ulVSync_BP = (ulong)((int)((flMin_Vsync_BP / flHPeriodEst) + 0.5));

            // Step 9: Find the number of lines in V back porch alone
            ulong ulVBackPorch = ulVSync_BP - ulVSyncRqd;

            // Step 10: Find the total number of lines in vertical field
            float flTotalVLines = ulVLinesRnd + ulTopMargin + ulBottomMargin + ulVSync_BP + flInterLaced
                                  + ulMinPorch;

            // Step 11: Estimate the vertical field frequency
            float flVFieldRateEst = 1 / flHPeriodEst / flTotalVLines * 1000000;

            // Step 12: Find actual horizontal period
            float flHPeriod = flHPeriodEst / (flVFieldRateRqd / flVFieldRateEst);

            // Step 13: Find the actual vertical field frequency
            float flVFieldRate = (1 / flHPeriod / flTotalVLines) * 1000000;

            // Step 14: Find the actual vertical frame frequency
            float flVFrameRate = bInterLaced ? flVFieldRate / 2 : flVFieldRate;

            // Step 15,16: Find the number of pixels in the left, right margins, we assume they are zero 
            ulong ulLeftMargin = 0, ulRightMargin = 0;

            // Step 17: Find total number of active pixels in one line plus the margins 
            ulong ulTotalActivePixels = ulHPixelsRnd + ulRightMargin + ulLeftMargin;

            // Step 18: Find the ideal blanking duty cycle form blanking duty cycle equation
            float flIdealDutyCycle = (float)(flCPrime - (flMPrime * flHPeriod / 1000));

            // Step 19: Find the number of pixels in the blanking time to the nearest double charactr cell
            ulong ulHBlankPixels = (ulong)(((int)((ulTotalActivePixels * flIdealDutyCycle / (100 - flIdealDutyCycle) / (2 * flCellGran)) + 0.5)) * (2 * flCellGran));

            // Step 20: Find total number of pixels in one line
            ulong ulTotalPixels = ulTotalActivePixels + ulHBlankPixels;

            // Step 21: Find pixel clock frequency
            //currently we are taking value till 3 places after decimal
            //If the precision need to be increased to 4 places of decimal replace the
            //PRECISION3DEC by PRECISION4DEC
            ulong ulDecPrecisonPoint = PRECISION3DEC;
            //Get the pixel clcok till 3 places of decimals
            ulong ulPixelClock = (ulong)((int)((ulTotalPixels / flHPeriod) * ulDecPrecisonPoint) + 0.5);

            // Step 22:  Get the horizontal frequency
            float flHFreq = (1000 / flHPeriod) * 1000;

            ulong ulHSyncPixles = (ulong)(((int)(((ulTotalPixels / flCellGran) * (flHSynchPerct / 100)) + 0.5)) * flCellGran);
            ulong ulHSyncStart = ulTotalActivePixels + (ulHBlankPixels / 2) - ulHSyncPixles;
            ulong ulHSyncEnd = ulTotalActivePixels + (ulHBlankPixels / 2) - 1;
            //Gtf calculations ends here

            //This is the per frame total no of vertical lines
            ulong ulTotalVLines = (ulong)((int)((bInterLaced ? 2 * flTotalVLines : flTotalVLines) + 0.5));

            //This is done to get the pixel clock in Hz
            ulong dwDotClock = ulPixelClock * (1000000 / ulDecPrecisonPoint);    // from step 21
            ulong dwHTotal = ulTotalPixels;          // from step 20

            //calculate in case of interlaced the frame based parameters
            //instead of per field basis
            ulong dwVTotal = ulTotalVLines;  // from step 10

            pixelClock = (uint)dwDotClock;
            HtotalVtotal = (uint)(dwHTotal * dwVTotal);
            if (!bProgressiveMode)
            {
                HtotalVtotal = HtotalVtotal / 2;
            }
        }
        private static DISPLAYCONFIG_PIXELFORMAT GetPixelFormat(uint bpp)
        {
            switch (bpp)
            {
                case 8:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_8BPP;
                case 16:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_16BPP;
                case 24:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_24BPP;
                case 32:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_32BPP;
                default:
                    return DISPLAYCONFIG_PIXELFORMAT.DISPLAYCONFIG_PIXELFORMAT_FORCE_UINT32;
            }
        }
        private static int GetDispHierarchy(string argAdapterName)
        {
            List<string> allDispAdapters = GetDisplayAdapters();
            List<int> allDispAdapterNum = new List<int>();
            allDispAdapters.ForEach(dA => allDispAdapterNum.Add(Convert.ToInt32(Regex.Match(dA, @"\d+").Value)));
            int displayDeviceNum = (Convert.ToInt32(Regex.Match(argAdapterName, @"\d+").Value) - (allDispAdapterNum.Min() - 1));
            string newAdapterStr = Regex.Replace(argAdapterName, "[0-9]+", Convert.ToString(displayDeviceNum));
            return Convert.ToInt32(Regex.Match(newAdapterStr, @"\d+").Value);
        }
        private static DISPLAYCONFIG_ROTATION GetGetOrientation(uint ori)
        {
            switch (ori)
            {
                case 0:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_IDENTITY;
                case 90:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE90;
                case 180:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE180;
                case 270:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_ROTATE270;
                default:
                    return DISPLAYCONFIG_ROTATION.DISPLAYCONFIG_ROTATION_IDENTITY;
            }
        }
        private static void FillModeInfoPathInfo(ref DISPLAYCONFIG_PATH_INFO[] pathInfo, ref DISPLAYCONFIG_MODE_INFO[] modeInfo,
           DisplayMode mode, DisplayConfigType argConfig, string argAdapterName, uint argWinMonID, List<DisplayInfo> argEnumeratedDisplays)
        {
            int sourceModeIndex = GetDispHierarchy(argAdapterName) - 1;
            for (int eachPathInfo = 0; eachPathInfo < pathInfo.Length; eachPathInfo++)
            {
                switch (argConfig)
                {
                    case DisplayConfigType.SD:
                    case DisplayConfigType.ED:
                    case DisplayConfigType.TED:
                        if (pathInfo[eachPathInfo].targetInfo.id == argWinMonID)
                            FillPathInfo(ref pathInfo[eachPathInfo], mode, out mode.PixelClk, out mode.HTotalVTotal);
                        break;
                    case DisplayConfigType.DDC:
                    case DisplayConfigType.TDC:
                        if (pathInfo[eachPathInfo].targetInfo.id == argWinMonID)
                            FillPathInfo(ref pathInfo[eachPathInfo], mode, out mode.PixelClk, out mode.HTotalVTotal);
                        else
                        {
                            DisplayMode currentMode = argEnumeratedDisplays.GetCurrentDisplayMode(pathInfo[eachPathInfo].targetInfo.id);
                            currentMode = currentMode.PrepareSetMode(mode.HzRes, mode.VtRes, mode.Angle);
                            FillPathInfo(ref pathInfo[eachPathInfo], currentMode, out currentMode.PixelClk, out currentMode.HTotalVTotal);
                        }
                        break;
                }
            }
            for (int eachModeInfo = 0; eachModeInfo < modeInfo.Length; eachModeInfo++)
            {
                DisplayMode optimalMode = argEnumeratedDisplays.GetOptimalDisplayMode(modeInfo[eachModeInfo].id);
                if (optimalMode.HzRes.Equals(0))
                    optimalMode = argEnumeratedDisplays.GetOptimalDisplayMode(argWinMonID);
                switch (argConfig)
                {
                    case DisplayConfigType.SD:
                        FillModeInfo(ref modeInfo[eachModeInfo], mode, argWinMonID, mode.PixelClk, mode.HTotalVTotal, optimalMode);
                        break;
                    case DisplayConfigType.DDC:
                    case DisplayConfigType.TDC:
                        FillModeInfo(ref modeInfo[eachModeInfo], mode, argWinMonID, mode.PixelClk, mode.HTotalVTotal, optimalMode);
                        break;
                    case DisplayConfigType.ED:
                    case DisplayConfigType.TED:
                        if (modeInfo[eachModeInfo].infoType == DISPLAYCONFIG_MODE_INFO_TYPE.DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE && modeInfo[eachModeInfo].id == sourceModeIndex)
                            FillModeInfo(ref modeInfo[eachModeInfo], mode, argWinMonID, mode.PixelClk, mode.HTotalVTotal, optimalMode);
                        else if (modeInfo[eachModeInfo].infoType == DISPLAYCONFIG_MODE_INFO_TYPE.DISPLAYCONFIG_MODE_INFO_TYPE_TARGET)
                            FillModeInfo(ref modeInfo[eachModeInfo], mode, argWinMonID, mode.PixelClk, mode.HTotalVTotal, optimalMode);
                        break;
                }
            }
        }
        private static void FillPathInfo(ref DISPLAYCONFIG_PATH_INFO pathInfo, DisplayMode mode, out uint pixelClk, out uint htotalVtotal)
        {
            if (Convert.ToBoolean(mode.InterlacedFlag))
            {
                ConvertRRtoRational((ulong)mode.HzRes, (ulong)mode.VtRes, (ulong)mode.RR, false, out pixelClk, out htotalVtotal);
                pathInfo.targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
            }
            else
            {
                ConvertRRtoRational((ulong)mode.HzRes, (ulong)mode.VtRes, (ulong)mode.RR, true, out pixelClk, out htotalVtotal);
                pathInfo.targetInfo.scanlineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
            }
            pathInfo.targetInfo.rotation = GetGetOrientation(mode.Angle);
            pathInfo.targetInfo.refreshRate.Numerator = pixelClk;
            pathInfo.targetInfo.refreshRate.Denominator = htotalVtotal;
            pathInfo.targetInfo.scaling = (DISPLAYCONFIG_SCALING)mode.ScalingOptions.First();
        }
        private static void FillModeInfo(ref DISPLAYCONFIG_MODE_INFO modeInfo, DisplayMode mode, uint argWinMonID, uint pixelClk, uint htotalVtotal, DisplayMode argOptimalMode)
        {
            if (modeInfo.id == argWinMonID)
            {
                if (Convert.ToBoolean(mode.InterlacedFlag))
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED;
                }
                else
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.scanLineOrdering = DISPLAYCONFIG_SCANLINE_ORDERING.DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE;
                }
                modeInfo.mode.sourceMode.width = pixelClk;
                modeInfo.mode.sourceMode.position.py = (int)pixelClk;

                modeInfo.mode.targetMode.targetVideoSignalInfo.vSyncFreq.Numerator = pixelClk;
                modeInfo.mode.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator = htotalVtotal;
                if (mode.ScalingOptions.First() == (uint)DISPLAYCONFIG_SCALING.DISPLAYCONFIG_SCALING_IDENTITY)
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cx = mode.HzRes;
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cy = mode.VtRes;
                }
                else
                {
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cx = argOptimalMode.HzRes;
                    modeInfo.mode.targetMode.targetVideoSignalInfo.activeSize.cy = argOptimalMode.VtRes;
                }
                modeInfo.mode.targetMode.targetVideoSignalInfo.pixelRate = pixelClk;
                modeInfo.mode.sourceMode.pixelFormat = GetPixelFormat(mode.Bpp);
            }
            if (modeInfo.infoType == DISPLAYCONFIG_MODE_INFO_TYPE.DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE)
            {
                modeInfo.mode.sourceMode.width = mode.HzRes;
                modeInfo.mode.sourceMode.height = mode.VtRes;
                modeInfo.mode.sourceMode.pixelFormat = GetPixelFormat(mode.Bpp);
            }
        }
    }
}