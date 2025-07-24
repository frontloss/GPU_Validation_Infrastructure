namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using igfxSDKLib;
    using System.Threading;

    /*  Get Set and Get all supported scaling through CUI SDK 8.0 */
    class SdkScaling_v2 : FunctionalBase, ISDK
    {
        private DisplayConfiguration SDKConfig;
        private IDisplayModeList SDKMode;

        public object Get(object args)
        {
            DisplayMode mode = (DisplayMode)args;
            GfxSDKClass sdk = new GfxSDKClass();
            DisplayScaling scalingOptions = new DisplayScaling(mode.display);
            SDKConfig = sdk.Display.Configuration;
            SDKConfig.Get();
            if (SDKConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                Array DisplayList = SDKConfig.Displays;
                uint windowsID = base.EnumeratedDisplays.Find(DT => DT.DisplayType == mode.display).WindowsMonitorID;
                for (int eachDisplay = 0; eachDisplay < SDKConfig.Displays.Length; eachDisplay++)
                {
                    if (((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).DisplayID == windowsID)
                    {
                        scalingOptions.scaling = (ScalingOptions)SdkExtensions.GetScaling(((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).Scaling);
                        scalingOptions.customX = ((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).CustomScalingX;
                        scalingOptions.customY = ((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).CustomScalingY;
                        scalingOptions.display = mode.display;
                        break;
                    }
                }
            }
            else
            {
                Log.Fail("Failed to Get Configuration through SDK ErrorCode: {0} ", SDKConfig.Error);
            }
            return scalingOptions;
        }

        public object Set(object args)
        {
            DisplayScaling scalingParam = (DisplayScaling)args;
            GfxSDKClass sdk = new GfxSDKClass();
            bool status = false;
            SDKConfig = sdk.Display.Configuration;
            SDKConfig.Get();

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkModes = sdkExtn.GetSDKHandle(SDKServices.Mode);
            DisplayMode mode = (DisplayMode)sdkModes.Get(scalingParam.display);

            if (SDKConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                Array DisplayList = SDKConfig.Displays;
                uint windowsID = base.EnumeratedDisplays.Find(DT => DT.DisplayType == scalingParam.display).WindowsMonitorID;
                for (int eachDisplay = 0; eachDisplay < SDKConfig.Displays.Length; eachDisplay++)
                {
                    if (((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).DisplayID == windowsID)
                    {
                        ((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).Mode.ResolutionSourceX = mode.HzRes;
                        ((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).Mode.ResolutionSourceY = mode.VtRes;
                        ((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).Mode.RefreshRate = mode.RR;
                        ((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).Mode.ColorBPP = (MODE_BPP)mode.Bpp;
                        ((DisplayConfigDetails)DisplayList.GetValue(eachDisplay)).Mode.IsInterlaced = (mode.InterlacedFlag == 0) ? false : true;
                        ((DisplayConfigDetails)(DisplayList.GetValue(eachDisplay))).Scaling = SdkExtensions.GetSDKScaling_v2(scalingParam.scaling);

                        if (ScalingOptions.Customize_Aspect_Ratio == scalingParam.scaling)
                        {
                            ((DisplayConfigDetails)(DisplayList.GetValue(eachDisplay))).CustomScalingX = scalingParam.customX;
                            ((DisplayConfigDetails)(DisplayList.GetValue(eachDisplay))).CustomScalingY = scalingParam.customY;
                        }
                    }
                }

                SDKConfig.Set();
                if (SDKConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
                {
                    Thread.Sleep(4000);
                    status = true;
                }
                else
                    Log.Fail("Unable to set Scaling {0} on display {1} error code: {3}", scalingParam.scaling, scalingParam.display, SDKConfig.Error);
            }
            else
            {
                Log.Fail("Failed to Get Configuration through SDK ErrorCode: {0} ", SDKConfig.Error);
            }
            return status;
        }

        public object GetAll(object args)
        {
            DisplayMode mode = (DisplayMode)args;
            GfxSDKClass sdk = new GfxSDKClass();
            List<uint> scalingOptions = new List<uint>();

            SDKMode = sdk.Display.ModeList;
            SDKConfig = sdk.Display.Configuration;

            SDKConfig.Get();
            uint supportedScaling = 0;
            DisplayInfo dispInfo = base.EnumeratedDisplays.Find(DT => DT.DisplayType == mode.display);
            IDisplayModeDetails[] modeList = (IDisplayModeDetails[])SDKMode.GetSupportedModesInConfigFor(dispInfo.WindowsMonitorID, SDKConfig);
            if (SDKMode.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS && modeList != null && modeList.Count() >= 1)
            {
                for (int eachMode = 0; eachMode < modeList.Count(); eachMode++)
                {
                    if ((modeList[eachMode].BasicModeDetails.ResolutionSourceX) == mode.HzRes &&
                        (modeList[eachMode].BasicModeDetails.ResolutionSourceY) == mode.VtRes &&
                        (modeList[eachMode].BasicModeDetails.ColorBPP) == (MODE_BPP)mode.Bpp &&
                        (modeList[eachMode].BasicModeDetails.RefreshRate) == mode.RR &&
                        (modeList[eachMode].BasicModeDetails.IsInterlaced == (mode.InterlacedFlag == 0) ? false : true))
                    {
                        supportedScaling = modeList[eachMode].SupportedScalings;
                        scalingOptions = SdkExtensions.ConvertToPanelFit_v2(mode, supportedScaling);
                        break;
                    }
                }
            }
            else
            {
                Log.Fail("Failed to Get Configuration through SDK ErrorCode: {0} ", SDKConfig.Error);
            }
            return scalingOptions;
        }
    }
}
