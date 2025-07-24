namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Threading;

    /*  Set independent rotation through CUI SDK 7.0 */
    class SdkIndependentRotation_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
        private string errorDesc = "";

        public object Set(object args)
        {
            List<DisplayMode> modeList = (List<DisplayMode>)args;
            IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfig = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkConfig = sdkExtn.GetSDKHandle(SDKServices.Config);
            DisplayConfig currentConfig = (DisplayConfig)sdkConfig.Get(null);

            APIExtensions.DisplayUtil.GetSystemConfigDataNViews(ref sysConfig, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Fail("Unable to get system configuration data through SDK");
                return false;
            }
            if (modeList.Count < 2)
            {
                Log.Verbose("Minimum two mode list required to set independent rotation");
                return false;
            }

            IGFX_DISPLAY_RESOLUTION_EX dispRes = new IGFX_DISPLAY_RESOLUTION_EX();
            dispRes.dwHzRes = modeList.First().HzRes;
            dispRes.dwVtRes = modeList.First().VtRes;
            dispRes.dwRR = modeList.First().RR;
            dispRes.dwBPP = modeList.First().Bpp;
            dispRes.InterlaceFlag = (ushort)modeList.First().InterlacedFlag;

            int currentIndex = (int)DisplayExtensions.GetDispHierarchy(currentConfig, modeList.First().display);
            if (SdkExtensions.IsColageEnabled(sysConfig))
            {
                for (int indexIn = 0; indexIn < sysConfig.uiNDisplays; indexIn++)
                {
                    sysConfig.DispCfg[indexIn].Resolution = dispRes;
                    sysConfig.DispCfg[indexIn].dwScaling = modeList[indexIn].ScalingOptions.First();
                    sysConfig.DispCfg[indexIn].dwOrientation = SdkExtensions.GetSDKOrientation_v1(modeList[indexIn].Angle);
                    if (DisplayExtensions.CanFlip(modeList[indexIn]))
                        DisplayExtensions.SwapValue(ref sysConfig.DispCfg[indexIn].Resolution.dwHzRes, ref sysConfig.DispCfg[indexIn].Resolution.dwVtRes);
                }
            }
            else
            {
                for (int displayIndex = 0; displayIndex < sysConfig.uiNDisplays; displayIndex++)
                {
                    sysConfig.DispCfg[displayIndex].Resolution.dwHzRes = modeList[displayIndex].HzRes;
                    sysConfig.DispCfg[displayIndex].Resolution.dwVtRes = modeList[displayIndex].VtRes;
                    sysConfig.DispCfg[displayIndex].Resolution.dwBPP = modeList[displayIndex].Bpp;
                    sysConfig.DispCfg[displayIndex].dwOrientation = SdkExtensions.GetSDKOrientation_v1(modeList[displayIndex].Angle);
                    sysConfig.DispCfg[displayIndex].Resolution.dwRR = modeList[displayIndex].RR;
                    sysConfig.DispCfg[displayIndex].Resolution.InterlaceFlag = (ushort)modeList[displayIndex].InterlacedFlag;
                    sysConfig.DispCfg[displayIndex].dwScaling = modeList[displayIndex].ScalingOptions.First();
                    if (DisplayExtensions.CanFlip(modeList[displayIndex]))
                        DisplayExtensions.SwapValue(ref sysConfig.DispCfg[displayIndex].Resolution.dwHzRes, ref sysConfig.DispCfg[displayIndex].Resolution.dwVtRes);
                    Log.Message("Mode to be applied in display {0}: HRes - {1}, VRes - {2}, bpp - {3}, RR - {4}{5}, Angle: {6} Scaling - {7} ",
                                modeList[displayIndex].display, modeList[displayIndex].HzRes, modeList[displayIndex].VtRes, modeList[displayIndex].Bpp, modeList[displayIndex].RR,
                                (Convert.ToBoolean(modeList[displayIndex].InterlacedFlag) ? "i" : "p"), modeList[displayIndex].Angle, (PanelFit)modeList[displayIndex].ScalingOptions.First());
                }
            }

            APIExtensions.DisplayUtil.SetSystemConfigDataNViews(ref sysConfig, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Thread.Sleep(6000);
                return true;
            }
            return false;
        }

        public object Get(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
