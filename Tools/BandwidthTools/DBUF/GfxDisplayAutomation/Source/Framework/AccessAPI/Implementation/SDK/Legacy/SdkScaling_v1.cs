namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using IgfxExtBridge_DotNet;

    /*  Get Set and Get all supported scaling through CUI SDK 7.0 */
    class SdkScaling_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = "";

        public object Get(object args)
        {
            DisplayMode mode = (DisplayMode)args;
            DisplayScaling scalingOptions = new DisplayScaling(mode.display);
            IGFX_SCALING_2_0 scaling_2_0 = new IGFX_SCALING_2_0();
            IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfigData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
            DisplayInfo displayInfo = base.EnumeratedDisplays.Find(Di => Di.DisplayType.Equals(mode.display));

            APIExtensions.DisplayUtil.GetSystemConfigDataNViews(ref sysConfigData, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                scalingOptions.scaling = (ScalingOptions)Array.Find(sysConfigData.DispCfg, dispConfig => dispConfig.dwDisplayUID.Equals(displayInfo.CUIMonitorID)).dwScaling;
                scalingOptions.display = mode.display;
            }
            else
            {
                Log.Fail("Unable to fetch scaling for {0}. Error code={1}, desc: {2}", mode.display, igfxErrorCode.ToString(), errorDesc);
            }
            if (scalingOptions.scaling == ScalingOptions.Customize_Aspect_Ratio)
            {
                scaling_2_0.Resolution.dwHzRes = mode.HzRes;
                scaling_2_0.Resolution.dwVtRes = mode.VtRes;
                scaling_2_0.Resolution.dwRR = mode.RR;
                scaling_2_0.Resolution.dwBPP = mode.Bpp;
                scaling_2_0.Resolution.InterlaceFlag = (ushort)mode.InterlacedFlag;
                scaling_2_0.dwDeviceID = base.EnumeratedDisplays.Find(Di => Di.DisplayType.Equals(mode.display)).CUIMonitorID;
                APIExtensions.DisplayUtil.GetScaling(ref scaling_2_0, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    scalingOptions.customX = scaling_2_0.customScalingX.dwCustomScalingCurrent;
                    scalingOptions.customY = scaling_2_0.customScalingY.dwCustomScalingCurrent;
                }
            }

            return scalingOptions;
        }

        public object Set(object args)
        {
            DisplayScaling scalingParam = (DisplayScaling)args;
            IGFX_SCALING_2_0 scaling_2_0 = new IGFX_SCALING_2_0();
            bool status = false;

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkModes = sdkExtn.GetSDKHandle(SDKServices.Mode);
            DisplayMode mode = (DisplayMode)sdkModes.Get(scalingParam.display);

            scaling_2_0.Resolution.dwHzRes = mode.HzRes;
            scaling_2_0.Resolution.dwVtRes = mode.VtRes;
            scaling_2_0.Resolution.dwRR = mode.RR;
            scaling_2_0.Resolution.dwBPP = mode.Bpp;
            scaling_2_0.Resolution.InterlaceFlag = (ushort)mode.InterlacedFlag;
            DisplayInfo displayInfo = base.EnumeratedDisplays.Find(Di => Di.DisplayType.Equals(mode.display));
            scaling_2_0.dwDeviceID = displayInfo.CUIMonitorID;
            scaling_2_0.dwCurrentAspectOption = Convert.ToUInt32(SdkExtensions.GetSDKScaling_v1(scalingParam.scaling));

            if (ScalingOptions.Customize_Aspect_Ratio == scalingParam.scaling)
            {
                scaling_2_0.customScalingX.dwCustomScalingCurrent = scalingParam.customX;
                scaling_2_0.customScalingY.dwCustomScalingCurrent = scalingParam.customY;
            }

            APIExtensions.DisplayUtil.SetScaling(ref scaling_2_0, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                status = true;
            }
            else
            {
                Log.Fail("Unable to set scaling:{0} on {1}. Error code={2}, desc: {3}", scalingParam.scaling.ToString(), scalingParam.display, igfxErrorCode.ToString(), errorDesc);
                status = false;
            }
            return status;
        }

        public object GetAll(object args)
        {
            DisplayMode mode = (DisplayMode)args;
            List<uint> scalingOptions = new List<uint>();
            uint supportedScaling = 0;

            IGFX_SCALING_2_0 scaling_2_0 = new IGFX_SCALING_2_0();
            scaling_2_0.Resolution.dwHzRes = mode.HzRes;
            scaling_2_0.Resolution.dwVtRes = mode.VtRes;
            scaling_2_0.Resolution.dwRR = mode.RR;
            scaling_2_0.Resolution.dwBPP = mode.Bpp;
            scaling_2_0.Resolution.InterlaceFlag = (ushort)mode.InterlacedFlag;
            scaling_2_0.dwDeviceID = base.EnumeratedDisplays.Find(Di => Di.DisplayType.Equals(mode.display)).CUIMonitorID;
            APIExtensions.DisplayUtil.GetScaling(ref scaling_2_0, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                supportedScaling = scaling_2_0.dwSupportedAspectOption;
                scalingOptions = SdkExtensions.ConvertToPanelFit_v1(mode, supportedScaling);
            }
            else
            {
                Log.Fail("Unable to fetch scaling options on {0}. Error code={1}, desc: {2}", mode.display, igfxErrorCode.ToString(), errorDesc);
            }
            return scalingOptions;
        }
    }
}
