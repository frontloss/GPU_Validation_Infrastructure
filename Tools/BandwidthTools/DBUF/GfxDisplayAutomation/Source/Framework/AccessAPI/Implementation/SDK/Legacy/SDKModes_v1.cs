namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    using IgfxExtBridge_DotNet;

    /*  Get Set and Get all modes through CUI SDK 7.0 */
    class SdkModes_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = "";

        public object Get(object args)
        {
            DisplayType display = (DisplayType)args;
            DisplayMode displayMode = new DisplayMode();
            IGFX_DISPLAY_RESOLUTION_EX DisplayRes = new IGFX_DISPLAY_RESOLUTION_EX();
            IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfigData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();

            DisplayInfo obj = base.EnumeratedDisplays.Find(Di => Di.DisplayType.Equals(display));
            APIExtensions.DisplayUtil.GetSystemConfigDataNViews(ref sysConfigData, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                DisplayRes = Array.Find(sysConfigData.DispCfg, dispConfig => dispConfig.dwDisplayUID.Equals(obj.CUIMonitorID)).Resolution;
                displayMode.display = display;
                displayMode.HzRes = DisplayRes.dwHzRes;
                displayMode.VtRes = DisplayRes.dwVtRes;
                displayMode.RR = DisplayRes.dwRR;
                displayMode.InterlacedFlag = DisplayRes.InterlaceFlag;
                displayMode.Bpp = DisplayRes.dwBPP;
                uint uAngle = Array.Find(sysConfigData.DispCfg, dispConfig => dispConfig.dwDisplayUID.Equals(obj.CUIMonitorID)).dwOrientation;
                switch (uAngle)
                {
                    case 0:
                        displayMode.Angle = 0;
                        break;
                    case 1:
                        displayMode.Angle = 90;
                        break;
                    case 2:
                        displayMode.Angle = 180;
                        break;
                    case 3:
                        displayMode.Angle = 270;
                        break;
                    default:
                        Log.Alert("Wrong Angle enumerated through SDK");
                        break;
                }
            }
            else
            {
                Log.Fail(false, String.Format("Unable to fetch resolution for {0}. Error code={1}, desc: {2}", display, igfxErrorCode.ToString(), errorDesc));
            }
            return displayMode;
        }

        public object Set(object args)
        {
            bool status = false;
            DisplayMode modeInfo = (DisplayMode)args;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());

            if (modeInfo.ScalingOptions == null || modeInfo.ScalingOptions.Count == 0)
            {
                modeInfo.ScalingOptions = new List<uint>();
                ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                List<uint> scalingOptions = (List<uint>)sdkScaling.GetAll(modeInfo);
                modeInfo.ScalingOptions.AddRange(scalingOptions);
                if (modeInfo.ScalingOptions.Count == 0)
                    Log.Abort("Unable to find scaling option through SDK");
            }

            ISDK sdkConfig = sdkExtn.GetSDKHandle(SDKServices.Config);
            DisplayConfig currentCfg = (DisplayConfig)sdkConfig.Get(null);

            IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfig = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
            APIExtensions.DisplayUtil.GetSystemConfigDataNViews(ref sysConfig, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Fail("Unable to get system configuration data through SDK");
                return false;
            }
            IGFX_DISPLAY_RESOLUTION_EX dispRes = new IGFX_DISPLAY_RESOLUTION_EX();
            dispRes.dwHzRes = modeInfo.HzRes;
            dispRes.dwVtRes = modeInfo.VtRes;
            dispRes.dwRR = modeInfo.RR;
            dispRes.dwBPP = modeInfo.Bpp;
            dispRes.InterlaceFlag = (ushort)modeInfo.InterlacedFlag;

            int currentIndex = (int)DisplayExtensions.GetDispHierarchy(currentCfg, modeInfo.display);
            if (SdkExtensions.IsColageEnabled(sysConfig))
            {
                for (int indexIn = 0; indexIn < sysConfig.uiNDisplays; indexIn++)
                {
                    sysConfig.DispCfg[indexIn].Resolution = dispRes;
                    sysConfig.DispCfg[indexIn].dwOrientation = SdkExtensions.GetSDKOrientation_v1(modeInfo.Angle);
                    sysConfig.DispCfg[indexIn].dwScaling = modeInfo.ScalingOptions.First();
                    if (DisplayExtensions.CanFlip(modeInfo))
                        DisplayExtensions.SwapValue(ref sysConfig.DispCfg[indexIn].Resolution.dwHzRes, ref sysConfig.DispCfg[indexIn].Resolution.dwVtRes);
                }
            }
            else
            {
                sysConfig.DispCfg[currentIndex].Resolution = dispRes;
                sysConfig.DispCfg[currentIndex].dwScaling = modeInfo.ScalingOptions.First();
                sysConfig.DispCfg[currentIndex].dwOrientation = SdkExtensions.GetSDKOrientation_v1(modeInfo.Angle);
                if (DisplayExtensions.CanFlip(modeInfo))
                    DisplayExtensions.SwapValue(ref sysConfig.DispCfg[currentIndex].Resolution.dwHzRes, ref sysConfig.DispCfg[currentIndex].Resolution.dwVtRes);
            }

            Log.Message("Mode to be applied in display {0}: HRes - {1}, VRes - {2}, bpp - {3}, RR - {4}{5}, Angle: {6} Scaling - {7} ",
            modeInfo.display, modeInfo.HzRes, modeInfo.VtRes, modeInfo.Bpp, modeInfo.RR,
            (Convert.ToBoolean(modeInfo.InterlacedFlag) ? "i" : "p"), modeInfo.Angle, (PanelFit)modeInfo.ScalingOptions.First());

            if (sysConfig.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE)
            {
                for(int displayIndex = 0; displayIndex < sysConfig.uiNDisplays; displayIndex++)
                {
                    if (currentIndex != displayIndex)
                    {
                        sysConfig.DispCfg[displayIndex].Resolution.dwHzRes = dispRes.dwHzRes;
                        sysConfig.DispCfg[displayIndex].Resolution.dwVtRes = dispRes.dwVtRes;
                        sysConfig.DispCfg[displayIndex].Resolution.dwBPP = dispRes.dwBPP;
                        sysConfig.DispCfg[displayIndex].dwOrientation = SdkExtensions.GetSDKOrientation_v1(modeInfo.Angle);

                        if (DisplayExtensions.CanFlip(modeInfo))
                            DisplayExtensions.SwapValue(ref sysConfig.DispCfg[displayIndex].Resolution.dwHzRes, ref sysConfig.DispCfg[displayIndex].Resolution.dwVtRes);

                        DisplayMode TempModeInfo = modeInfo;
                        TempModeInfo.display = currentCfg.CustomDisplayList[displayIndex];
                        RR_Scaling RrNScaling = GetSupportedRR(TempModeInfo);

                        sysConfig.DispCfg[displayIndex].Resolution.dwRR = RrNScaling.supportedRR;
                        sysConfig.DispCfg[displayIndex].Resolution.InterlaceFlag = RrNScaling.InterlaceFlag;
                        sysConfig.DispCfg[displayIndex].dwScaling = RrNScaling.ScalingOption.First();

                        Log.Message("Mode to be applied in display {0}: HRes - {1}, VRes - {2}, bpp - {3}, RR - {4}{5}, Angle: {6} Scaling - {7} ",
                        TempModeInfo.display, modeInfo.HzRes, modeInfo.VtRes, modeInfo.Bpp, RrNScaling.supportedRR,
                        (Convert.ToBoolean(RrNScaling.InterlaceFlag) ? "i" : "p"), modeInfo.Angle, (PanelFit)RrNScaling.ScalingOption.First());
                    }
                }
            }

            APIExtensions.DisplayUtil.SetSystemConfigDataNViews(ref sysConfig, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Thread.Sleep(4000);
                status = true;
            }
            return status;
        }

        public object GetAll(object args)
        {
            List<DisplayType> displayList = args as List<DisplayType>;
            List<DisplayModeList> allSupportedModes = new List<DisplayModeList>();
            foreach (DisplayType eachDisplay in displayList)
            {
                IGFX_VIDEO_MODE_LIST_EX modesListEx = new IGFX_VIDEO_MODE_LIST_EX();
                IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfigData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
                DisplayModeList displayMode = new DisplayModeList();
                DisplayMode currentRes = new DisplayMode();
                displayMode.display = eachDisplay;
                if (GetSystemConfiguration(ref sysConfigData))
                {
                    modesListEx.DispCfg = sysConfigData.DispCfg;
                    modesListEx.dwOpMode = sysConfigData.dwOpMode;
                    modesListEx.uiNDisplays = sysConfigData.uiNDisplays;
                    modesListEx.dwDeviceID = base.EnumeratedDisplays.Find(DT => DT.DisplayType == eachDisplay).CUIMonitorID;
                }
                else
                {
                    Log.Abort("Unable to fetch supported modes through SDK");
                    return allSupportedModes;
                }
                //First get the size of modes list
                APIExtensions.DisplayUtil.QueryforVideoModeList(ref modesListEx, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    for (uint eachModeIndex = 0; eachModeIndex < modesListEx.vmlNumModes; eachModeIndex++)
                    {
                        IGFX_DISPLAY_RESOLUTION_EX dispResolution = new IGFX_DISPLAY_RESOLUTION_EX();
                        APIExtensions.DisplayUtil.GetIndividualVideoMode(ref dispResolution, eachModeIndex, out igfxErrorCode, out errorDesc);
                        if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                        {
                            currentRes.display = eachDisplay;
                            currentRes.HzRes = dispResolution.dwHzRes;
                            currentRes.VtRes = dispResolution.dwVtRes;
                            currentRes.RR = dispResolution.dwRR;
                            currentRes.Bpp = dispResolution.dwBPP;
                            currentRes.InterlacedFlag = dispResolution.InterlaceFlag;
                            currentRes.ScalingOptions = new List<uint>();

                            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
                            ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                            List<uint> scalingOptions = (List<uint>)sdkScaling.GetAll(currentRes);
                            if (scalingOptions != null)
                            {
                                currentRes.ScalingOptions.AddRange(scalingOptions);
                                displayMode.supportedModes.Add(currentRes);
                            }
                        }
                        else
                        {
                            Log.Alert("Unable to fetch mode - Index = {0}", eachModeIndex);
                        }
                    }
                    allSupportedModes.Add(displayMode);
                }
            }
            return allSupportedModes;
        }

        private bool GetSystemConfiguration(ref IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfigData)
        {
            APIExtensions.DisplayUtil.GetSystemConfigDataNViews(ref sysConfigData, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Fail("Unable to get system configuration data through SDK - Error Code: {0}  ErrorDec: {1}", igfxErrorCode, errorDesc);
                return false;
            }
            else
            {
                Log.Verbose("System configuration data obtained successfully through SDK");
                return true;
            }
        }

        private RR_Scaling GetSupportedRR(DisplayMode argmode)
        {
            RR_Scaling supportedRRNScaling = new RR_Scaling();
            List<DisplayType> displayList = new List<DisplayType>();
            displayList.Add(argmode.display);

            List<DisplayModeList> modelist = (List<DisplayModeList>)this.GetAll(displayList);
            foreach (DisplayMode eachMode in modelist.First().supportedModes)
            {
                if (eachMode.HzRes == argmode.HzRes && eachMode.VtRes == argmode.VtRes &&
                    eachMode.Bpp == argmode.Bpp)
                {
                    supportedRRNScaling.supportedRR = eachMode.RR;
                    supportedRRNScaling.InterlaceFlag = (ushort)eachMode.InterlacedFlag;

                    if (eachMode.ScalingOptions != null)
                        supportedRRNScaling.ScalingOption = eachMode.ScalingOptions;
                    else
                    {

                        argmode.RR = eachMode.RR;
                        argmode.InterlacedFlag = (ushort)eachMode.InterlacedFlag;
                        SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
                        ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                        supportedRRNScaling.ScalingOption = (List<uint>)sdkScaling.GetAll(argmode);
                    }
                    break;
                }
            }
            return supportedRRNScaling;
        }

    }
}
