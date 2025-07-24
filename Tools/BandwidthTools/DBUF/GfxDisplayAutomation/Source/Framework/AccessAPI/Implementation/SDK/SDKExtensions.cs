namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Threading;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using igfxSDKLib;

    public class SdkExtensions : FunctionalBase
    {
        private Dictionary<SDKServices, ISDK> FeaturesTable = null;
        private static DisplayUtil lDisplayUtil = null;
        private static double driverBase = 15.48;
        private static bool useSdkType = false;

        public ISDK GetSDKHandle(SDKServices argService)
        {
            SDKType sdkType = (SDKType)Enum.Parse(typeof(SDKType), base.AppSettings.UseSDKType, true);
            if (sdkType == SDKType.Default)
            {
                if (Convert.ToDouble(base.MachineInfo.Driver.DriverBaseLine) > driverBase)
                    sdkType = SDKType.New;
                else
                    sdkType = SDKType.Old;
            }
            if (false == useSdkType)
            {
                useSdkType = true;
                Log.Message("SDK Service type is {0}", sdkType);
            }
            
            FeaturesTable = new Dictionary<SDKServices, ISDK>();
            if (sdkType == SDKType.New)
            {
                FeaturesTable.Add(SDKServices.DisplayType, base.CreateInstance<SdkDisplayType_v2>(new SdkDisplayType_v2()));
                FeaturesTable.Add(SDKServices.EDID, base.CreateInstance<EDID_v2>(new EDID_v2()));
                FeaturesTable.Add(SDKServices.DpcdRegister, base.CreateInstance<DpcdRegister_v2>(new DpcdRegister_v2()));
                FeaturesTable.Add(SDKServices.Audio, base.CreateInstance<Audio_v2>(new Audio_v2()));
                FeaturesTable.Add(SDKServices.XvYcc, base.CreateInstance<XvYcc_v2>(new XvYcc_v2()));
                FeaturesTable.Add(SDKServices.YCbCr, base.CreateInstance<YCbCr_v2>(new YCbCr_v2()));
                FeaturesTable.Add(SDKServices.NarrowGamut, base.CreateInstance<NarrowGamut_v2>(new NarrowGamut_v2()));
                FeaturesTable.Add(SDKServices.WideGamut, base.CreateInstance<WideGamut_v2>(new WideGamut_v2()));
                FeaturesTable.Add(SDKServices.Config, base.CreateInstance<SdkConfig_v2>(new SdkConfig_v2()));
                FeaturesTable.Add(SDKServices.Scaling, base.CreateInstance<SdkScaling_v2>(new SdkScaling_v2()));
                FeaturesTable.Add(SDKServices.Mode, base.CreateInstance<SdkModes_v2>(new SdkModes_v2()));
                FeaturesTable.Add(SDKServices.Collage, base.CreateInstance<Collage_v2>(new Collage_v2()));
                FeaturesTable.Add(SDKServices.IndependentRotation, base.CreateInstance<SdkIndependentRotation_v2>(new SdkIndependentRotation_v2()));
                FeaturesTable.Add(SDKServices.QuantizationRange, base.CreateInstance<QuantizationRange_v2>(new QuantizationRange_v2())); 
            }
            else
            {
                FeaturesTable.Add(SDKServices.DisplayType, base.CreateInstance<SdkDisplayType_v1>(new SdkDisplayType_v1()));
                FeaturesTable.Add(SDKServices.EDID, base.CreateInstance<EDID_v1>(new EDID_v1()));
                FeaturesTable.Add(SDKServices.DpcdRegister, base.CreateInstance<DpcdRegister_v1>(new DpcdRegister_v1()));
                FeaturesTable.Add(SDKServices.Audio, base.CreateInstance<Audio_v1>(new Audio_v1()));
                FeaturesTable.Add(SDKServices.XvYcc, base.CreateInstance<XvYcc_v1>(new XvYcc_v1()));
                FeaturesTable.Add(SDKServices.YCbCr, base.CreateInstance<YCbCr_v1>(new YCbCr_v1()));
                FeaturesTable.Add(SDKServices.NarrowGamut, base.CreateInstance<NarrowGamut_v1>(new NarrowGamut_v1()));
                FeaturesTable.Add(SDKServices.WideGamut, base.CreateInstance<WideGamut_v1>(new WideGamut_v1()));
                FeaturesTable.Add(SDKServices.Config, base.CreateInstance<SdkConfig_v1>(new SdkConfig_v1()));
                FeaturesTable.Add(SDKServices.Scaling, base.CreateInstance<SdkScaling_v1>(new SdkScaling_v1()));
                FeaturesTable.Add(SDKServices.Mode, base.CreateInstance<SdkModes_v1>(new SdkModes_v1()));
                FeaturesTable.Add(SDKServices.Collage, base.CreateInstance<Collage_v1>(new Collage_v1()));
                FeaturesTable.Add(SDKServices.IndependentRotation, base.CreateInstance<SdkIndependentRotation_v1>(new SdkIndependentRotation_v1()));
                FeaturesTable.Add(SDKServices.QuantizationRange, base.CreateInstance<QuantizationRange_v1>(new QuantizationRange_v1()));
            }
            return FeaturesTable[argService];
        }
        public static DisplayUtil LDisplayUtil
        {
            get
            {
                if (null == lDisplayUtil)
                {
                    CommonExtensions.RegisterDll("IgfxExtBridge.dll");
                    Thread.Sleep(3000);
                    RegDispUtil();
                }
                return lDisplayUtil;
            }
        }

        private static void RegDispUtil()
        {
            Log.Verbose("Creating DisplayUtil reference");
            lDisplayUtil = new DisplayUtil();
            if (null == lDisplayUtil)
            {
                Log.Sporadic(false, "DisplayUtil instance not created! A reboot might be required");
                PowerEvent powerEvent = new PowerEvent();
                powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 5 });
            }
            else
            {
                Log.Verbose("DisplayUtil instance created");
                string pErrorDescription = "";
                IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfig = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
                IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
                lDisplayUtil.GetSystemConfigDataNViews(ref sysConfig, out igfxErrorCode, out pErrorDescription);

                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Alert(String.Format("{0}:Unable to get system configuration data-{1}", igfxErrorCode.ToString(), pErrorDescription));
                }
                else
                {
                    if (sysConfig.uiNDisplays != 0)
                        Log.Message("{0} no of display active", sysConfig.uiNDisplays);
                    else
                        Log.Message("GetSystemConfiguration Returned 0 displays");
                }
            }
        }

        internal static GENERIC GetSDKScaling_v1(ScalingOptions scaling)
        {
            switch (scaling)
            {
                case ScalingOptions.Maintain_Aspect_Ratio:
                    return GENERIC.IGFX_ASPECT_SCALING;
                case ScalingOptions.Center_Image:
                    return GENERIC.IGFX_CENTERING;
                case ScalingOptions.Maintain_Display_Scaling:
                    return GENERIC.IGFX_MAINTAIN_DISPLAY_SCALING;
                case ScalingOptions.Customize_Aspect_Ratio:
                    return GENERIC.IGFX_SCALING_CUSTOM;
                case ScalingOptions.Scale_Full_Screen:
                    return GENERIC.IGFX_PANEL_FITTING;
            }
            return GENERIC.IGFX_MAINTAIN_DISPLAY_SCALING;
        }

        internal static MODE_SCALING GetSDKScaling_v2(ScalingOptions scaling)
        {
            switch (scaling)
            {
                case ScalingOptions.Center_Image:
                    return MODE_SCALING.Center_Screen;
                case ScalingOptions.Scale_Full_Screen:
                    return MODE_SCALING.Full_Screen;
                case ScalingOptions.Maintain_Aspect_Ratio:
                    return MODE_SCALING.Maintain_Aspect_Ratio;
                case ScalingOptions.Customize_Aspect_Ratio:
                    return MODE_SCALING.Custom_Scaling;
                case ScalingOptions.Maintain_Display_Scaling:
                    return MODE_SCALING.Maintain_Display_Scaling;
                default:
                    return MODE_SCALING.Maintain_Display_Scaling;
            }
        }

        internal static List<uint> ConvertToPanelFit_v1(DisplayMode mode, uint availableScaling)
        {
            List<uint> scalingOptions = new List<uint>();
            if ((availableScaling & (uint)GENERIC.IGFX_MAINTAIN_DISPLAY_SCALING) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.MaintainDisplayScaling));
            }
            if ((availableScaling & (uint)GENERIC.IGFX_CENTERING) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.CenterImage));
            }
            if ((availableScaling & (uint)GENERIC.IGFX_PANEL_FITTING) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.ScaleFullScreen));
            }
            if ((availableScaling & (uint)GENERIC.IGFX_ASPECT_SCALING) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.MaintainAspectRatio));
            }
            if ((availableScaling & (uint)GENERIC.IGFX_SCALING_CUSTOM) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.CustomAspectRatio));
            }

            return scalingOptions;
        }

        internal static List<uint> ConvertToPanelFit_v2(DisplayMode mode, uint availableScaling)
        {
            List<uint> scalingOptions = new List<uint>();
            if ((availableScaling & (uint)MODE_SCALING.Maintain_Display_Scaling) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.MaintainDisplayScaling));
            }
            if ((availableScaling & (uint)MODE_SCALING.Center_Screen) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.CenterImage));
            }
            if ((availableScaling & (uint)MODE_SCALING.Full_Screen) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.ScaleFullScreen));
            }
            if ((availableScaling & (uint)MODE_SCALING.Maintain_Aspect_Ratio) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.MaintainAspectRatio));
            }
            if ((availableScaling & (uint)MODE_SCALING.Custom_Scaling) != 0)
            {
                scalingOptions.Add(Convert.ToUInt32(PanelFit.CustomAspectRatio));
            }
            return scalingOptions;
        }

        internal static bool IsColageEnabled(IGFX_SYSTEM_CONFIG_DATA_N_VIEWS currentSysConfig)
        {
            if (currentSysConfig.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE ||
                currentSysConfig.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE ||
                currentSysConfig.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE ||
                currentSysConfig.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_VERTCOLLAGE)
                return true;
            else
                return false;
        }

        internal static uint GetSDKOrientation_v1(uint angle)
        {
            switch (angle)
            {
                case 0:
                    return 0;
                case 90:
                    return 1;
                case 180:
                    return 2;
                case 270:
                    return 3;
                default:
                    Log.Alert("Wrong Angle passed in mode information");
                    return 0;
            }
        }

        internal static MODE_ROTATION GetSDKOrientation_v2(uint angle)
        {
            switch (angle)
            {
                case 0:
                    return MODE_ROTATION.Landscape;
                case 180:
                    return MODE_ROTATION.Landscape_Flipped;
                case 90:
                    return MODE_ROTATION.Portrait;
                case 270:
                    return MODE_ROTATION.Portrait_Flipped;
                default:
                    Log.Alert("Wrong Angle passed in mode information");
                    return MODE_ROTATION.Landscape;
            }
        }

        internal static uint GetScaling(MODE_SCALING scaling)
        {
            switch (scaling)
            {
                case MODE_SCALING.Center_Screen:
                    return 1;
                case MODE_SCALING.Full_Screen:
                    return 2;
                case MODE_SCALING.Maintain_Aspect_Ratio:
                    return 4;
                case MODE_SCALING.Custom_Scaling:
                    return 8;
                case MODE_SCALING.Maintain_Display_Scaling:
                    return 64;
                default:
                    return 64;
            }
        }

    }
}
