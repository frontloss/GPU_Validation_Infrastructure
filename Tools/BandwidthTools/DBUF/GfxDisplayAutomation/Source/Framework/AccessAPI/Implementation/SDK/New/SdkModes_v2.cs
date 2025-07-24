namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Threading;
    using System.Linq;
    using igfxSDKLib;

    /*  Get Set and Get all modes through CUI SDK 8.0 */
    class SdkModes_v2 : FunctionalBase, ISDK
    {
        private IDisplayModeList SDKMode;
        private DisplayConfiguration SDKConfig;
        public object Get(object args)
        {
            DisplayType display = (DisplayType)args;
            DisplayMode displayMode = new DisplayMode();

            GfxSDKClass sdk = new GfxSDKClass();
            SDKConfig = sdk.Display.Configuration;
            SDKConfig.Get();
            if (SDKConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                DisplayInfo dispInfo = base.EnumeratedDisplays.Find(DT => DT.DisplayType == display);
                IDisplayConfigDetails[] displayConfigList = (IDisplayConfigDetails[])SDKConfig.Displays;
                IDisplayConfigDetails displayConfig = Array.Find(displayConfigList, DT => DT.DisplayID == dispInfo.WindowsMonitorID);
                displayMode.ScalingOptions = new List<uint>();

                displayMode.display = display;
                displayMode.HzRes = displayConfig.Mode.ResolutionSourceX;
                displayMode.VtRes = displayConfig.Mode.ResolutionSourceY;
                displayMode.RR = displayConfig.Mode.RefreshRate;
                displayMode.InterlacedFlag = (uint)(displayConfig.Mode.IsInterlaced ? 2 : 0);
                displayMode.Bpp = (uint)displayConfig.Mode.ColorBPP;
                displayMode.ScalingOptions.Add(SdkExtensions.GetScaling(displayConfig.Scaling));
                switch (displayConfig.Rotation)
                {
                    case MODE_ROTATION.Landscape:
                        displayMode.Angle = 0;
                        break;
                    case MODE_ROTATION.Portrait:
                        displayMode.Angle = 90;
                        break;
                    case MODE_ROTATION.Landscape_Flipped:
                        displayMode.Angle = 180;
                        break;
                    case MODE_ROTATION.Portrait_Flipped:
                        displayMode.Angle = 270;
                        break;
                    default:
                        Log.Alert("Wrong Angle enumerated through SDK");
                        break;
                }

                if (DisplayExtensions.CanFlip(displayMode))
                    DisplayExtensions.SwapValue(ref displayMode.HzRes, ref displayMode.VtRes);
            }
            else
            {
                Log.Message("Fail to get current display config through SDK");
            }
            return displayMode;
        }

        public object Set(object args)
        {
            DisplayMode modeInfo = (DisplayMode)args;
            bool status = false;

            DisplayConfiguration SDKConfig;
            GfxSDKClass sdk = new GfxSDKClass();
            SDKConfig = sdk.Display.Configuration;

            if (modeInfo.ScalingOptions == null || modeInfo.ScalingOptions.Count == 0)
            {
                modeInfo.ScalingOptions = new List<uint>();

                SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
                ISDK sdkScaling = sdkExtn.GetSDKHandle(SDKServices.Scaling);
                List<uint> scalingOptions = (List<uint>)sdkScaling.GetAll(modeInfo);
                modeInfo.ScalingOptions.AddRange(scalingOptions);
                if (modeInfo.ScalingOptions.Count == 0)
                    Log.Abort("Unable to find scaling option through SDK");                    
            }

            DisplayConfiguration displayConfig = new DisplayConfiguration();
            FillOpmode(modeInfo, SDKConfig);
            SDKConfig.Set();
            if (displayConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                Log.Message("Mode applied Successfully through SDK");
                Thread.Sleep(4000);
                status = true;
            }
            else
            {
                Log.Message("Failed to apply mode through SDK");
                status = false;
            }
            return status;
        }

        public object GetAll(object args)
        {
            List<DisplayType> displayList = args as List<DisplayType>;
            List<DisplayModeList> allSupportedModes = new List<DisplayModeList>();
            uint supportedScaling = 0;
            GfxSDKClass sdk = new GfxSDKClass();
            SDKMode = sdk.Display.ModeList;
            SDKConfig = sdk.Display.Configuration;
            SDKConfig.Get();

            foreach (DisplayType display in displayList)
            {
                DisplayInfo dispInfo = base.EnumeratedDisplays.Find(DT => DT.DisplayType == display);
                sdk.Display.Configuration.Get();
                IDisplayModeDetails[] modeList = (IDisplayModeDetails[])SDKMode.GetSupportedModesInConfigFor(dispInfo.WindowsMonitorID, SDKConfig);

                if (SDKMode.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS && modeList != null && modeList.Count() >= 1)
                {
                    DisplayModeList displayMode = new DisplayModeList();
                    DisplayMode currentRes = new DisplayMode();
                    displayMode.display = display;
                    for (int eachMode = 0; eachMode < modeList.Count(); eachMode++)
                    {
                        supportedScaling = 0;
                        currentRes.display = display;
                        currentRes.HzRes = modeList[eachMode].BasicModeDetails.ResolutionSourceX;
                        currentRes.VtRes = modeList[eachMode].BasicModeDetails.ResolutionSourceY;
                        currentRes.RR = modeList[eachMode].BasicModeDetails.RefreshRate;
                        currentRes.Bpp = (uint)modeList[eachMode].BasicModeDetails.ColorBPP;
                        currentRes.InterlacedFlag = (uint)(modeList[eachMode].BasicModeDetails.IsInterlaced ? 2 : 0);

                        currentRes.ScalingOptions = new List<uint>();
                        supportedScaling = modeList[eachMode].SupportedScalings;
                        currentRes.ScalingOptions = SdkExtensions.ConvertToPanelFit_v2(currentRes, supportedScaling);
                        if (currentRes.ScalingOptions != null)
                        {
                            displayMode.supportedModes.Add(currentRes);
                        }
                    }
                    allSupportedModes.Add(displayMode);
                }
                else
                {
                    Log.Fail("Failed to Get Supporte dModes for display {0}: errorCode: {1}", dispInfo.DisplayType, SDKMode.Error);
                }

                
            }
            return allSupportedModes;
        }

        private void FillOpmode(DisplayMode modeInfo, DisplayConfiguration SDKConfig)
        {
            int dispCount = 0;
            SDKConfig.Get();

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkConfig = sdkExtn.GetSDKHandle(SDKServices.Config);
            DisplayConfig currentConfig = (DisplayConfig)sdkConfig.Get(null);

            if (SDKConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                dispCount = SDKConfig.Displays.Length;
                SDKConfig.PrimaryDisplayID = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(modeInfo.display)).WindowsMonitorID;
                int currentIndex = (int)DisplayExtensions.GetDispHierarchy(currentConfig, modeInfo.display);

                if (SDKConfig.IsCollage)
                {
                    if (SDKConfig.Collage.ArrangeDisplaysInCollageMatrix.GetUpperBound(0) <
                        SDKConfig.Collage.ArrangeDisplaysInCollageMatrix.GetUpperBound(1)) //Horizontal collage
                    {
                        var CollageDispList = new CollageBezelDetails[1, dispCount];
                        for (uint index = 0; index < dispCount; index++)
                        {
                            CollageDispList[0, index] = new CollageBezelDetails();
                            CollageDispList[0, index].IndexInDisplaysArray = index;
                        }
                        SDKConfig.Collage.ArrangeDisplaysInCollageMatrix = CollageDispList;
                    }
                    else //Vertical Collage
                    {
                        var CollageDispList = new CollageBezelDetails[dispCount, 1];
                        for (uint index = 0; index < dispCount; index++)
                        {
                            CollageDispList[index, 0] = new CollageBezelDetails();
                            CollageDispList[index, 0].IndexInDisplaysArray = index;
                        }
                        SDKConfig.Collage.ArrangeDisplaysInCollageMatrix = CollageDispList;
                    }

                    for (int indexIn = 0; indexIn < SDKConfig.Displays.Length; indexIn++)
                    {
                        DisplayInfo display = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(currentConfig.CustomDisplayList.ElementAt(indexIn)));
                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).DisplayID = display.WindowsMonitorID;

                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ResolutionSourceX = modeInfo.HzRes;
                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ResolutionSourceY = modeInfo.VtRes;
                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ColorBPP = (MODE_BPP)modeInfo.Bpp;
                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.RefreshRate = modeInfo.RR;
                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.IsInterlaced = modeInfo.InterlacedFlag == 0 ? false : true;

                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Scaling = SdkExtensions.GetSDKScaling_v2((ScalingOptions)modeInfo.ScalingOptions.First());
                        ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Rotation = SdkExtensions.GetSDKOrientation_v2(modeInfo.Angle);
                    }
                }
                else
                {
                    DisplayInfo display = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(currentConfig.CustomDisplayList.ElementAt(currentIndex)));
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).DisplayID = display.WindowsMonitorID;

                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).Mode.ResolutionSourceX = modeInfo.HzRes;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).Mode.ResolutionSourceY = modeInfo.VtRes;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).Mode.ColorBPP = (MODE_BPP)modeInfo.Bpp;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).Mode.RefreshRate = modeInfo.RR;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).Mode.IsInterlaced = modeInfo.InterlacedFlag == 0 ? false : true;

                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).Scaling = SdkExtensions.GetSDKScaling_v2((ScalingOptions)modeInfo.ScalingOptions.First());
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(currentIndex))).Rotation = SdkExtensions.GetSDKOrientation_v2(modeInfo.Angle);

                    
                }

                Log.Message("Mode to be applied in display {0}: HRes - {1}, VRes - {2}, bpp - {3}, RR - {4}{5}, Angle: {6} Scaling - {7} ",
                            modeInfo.display, modeInfo.HzRes, modeInfo.VtRes, modeInfo.Bpp, modeInfo.RR,
                            (Convert.ToBoolean(modeInfo.InterlacedFlag) ? "i" : "p"), modeInfo.Angle, (PanelFit)modeInfo.ScalingOptions.First());
                
                if (IsCloneDisplayConfig(SDKConfig))
                {
                    for (int indexIn = 0; indexIn < SDKConfig.Displays.Length; indexIn++)
                    {
                        if (currentIndex != indexIn)
                        {
                            DisplayInfo display = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(currentConfig.CustomDisplayList.ElementAt(indexIn)));
                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).DisplayID = display.WindowsMonitorID;

                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ResolutionSourceX = modeInfo.HzRes;
                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ResolutionSourceY = modeInfo.VtRes;
                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ColorBPP = (MODE_BPP)modeInfo.Bpp;
                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Rotation = SdkExtensions.GetSDKOrientation_v2(modeInfo.Angle);

                            DisplayMode TempModeInfo = modeInfo;
                            TempModeInfo.display = currentConfig.CustomDisplayList[indexIn];
                            RR_Scaling RrNScaling = GetSupportedRR(TempModeInfo);

                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.RefreshRate = RrNScaling.supportedRR;
                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.IsInterlaced = RrNScaling.InterlaceFlag == 0 ? false : true;

                            ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Scaling = SdkExtensions.GetSDKScaling_v2((ScalingOptions)RrNScaling.ScalingOption.First());

                            Log.Message("Mode to be applied in display {0}: HRes - {1}, VRes - {2}, bpp - {3}, RR - {4}{5}, Angle: {6} Scaling - {7} ",
                                        TempModeInfo.display, modeInfo.HzRes, modeInfo.VtRes, modeInfo.Bpp, RrNScaling.supportedRR,
                                        (Convert.ToBoolean(RrNScaling.InterlaceFlag) ? "i" : "p"), modeInfo.Angle, (PanelFit)RrNScaling.ScalingOption.First());
                        }
                    }
                }

            }
            else
            {
                Log.Fail("Failed to GetConfiguration through SDK ErrorCode: {0} ", SDKConfig.Error);
            }
        }

        private bool IsCloneDisplayConfig(DisplayConfiguration SDKConfig)
        {
            if (SDKConfig.IsCollage)
                return false;
            Array DisplayList = SDKConfig.Displays;
            bool status = true;
            if (SDKConfig.Displays.Length > 1)
            {
                for (int index = 0; index < SDKConfig.Displays.Length; index++)
                {
                    if (((DisplayConfigDetails)DisplayList.GetValue(index)).SourceID != 0)
                    {
                        status = false;
                        break;
                    }
                }
            }
            return status;
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
                        List<uint> scalingOptions = (List<uint>)sdkScaling.GetAll(argmode);
                        supportedRRNScaling.ScalingOption = scalingOptions;
                    }
                    break;
                }
            }

            return supportedRRNScaling;
        }
    }
}
