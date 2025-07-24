namespace Intel.VPG.Display.Automation
{
    using IgfxExtBridge_DotNet;
    using System.Threading;
    using System.Linq;

    /*  Get set display config through CUI SDK 7.0 */
    class SdkConfig_v1 : FunctionalBase, ISDK
    {
        private DisplayConfig argDispConfig;
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = "";

        public object Get(object args)
        {
            DisplayConfig dispConfig = new DisplayConfig();
            dispConfig.EnumeratedDisplays = base.EnumeratedDisplays;

            igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
            errorDesc = "";
            IGFX_SYSTEM_CONFIG_DATA_N_VIEWS getSystemCfgData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
            APIExtensions.DisplayUtil.GetSystemConfigDataNViews(ref getSystemCfgData, out igfxErrorCode, out errorDesc);

            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Verbose("Query Display Config through CUI SDK is {0}, No of active display {1}", (DISPLAY_DEVICE_CONFIG_FLAG)getSystemCfgData.dwOpMode, getSystemCfgData.uiNDisplays);
                if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_SINGLE && getSystemCfgData.uiNDisplays == 1)
                {
                    dispConfig.ConfigType = DisplayConfigType.SD;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = DisplayType.None;
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }
                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE && getSystemCfgData.uiNDisplays == 2)
                {
                    dispConfig.ConfigType = DisplayConfigType.DDC;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }

                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE && getSystemCfgData.uiNDisplays == 3)
                {
                    dispConfig.ConfigType = DisplayConfigType.TDC;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[2].dwDisplayUID)).DisplayType;
                }

                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD && getSystemCfgData.uiNDisplays == 2)
                {
                    dispConfig.ConfigType = DisplayConfigType.ED;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }

                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD && getSystemCfgData.uiNDisplays == 3)
                {
                    dispConfig.ConfigType = DisplayConfigType.TED;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[2].dwDisplayUID)).DisplayType;
                }

                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE && getSystemCfgData.uiNDisplays == 2)
                {
                    dispConfig.ConfigType = DisplayConfigType.Horizontal;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }

                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE && getSystemCfgData.uiNDisplays == 3)
                {
                    dispConfig.ConfigType = DisplayConfigType.Horizontal;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[2].dwDisplayUID)).DisplayType;
                }

                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE && getSystemCfgData.uiNDisplays == 2)
                {
                    dispConfig.ConfigType = DisplayConfigType.Vertical;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }

                else if (getSystemCfgData.dwOpMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_VERTCOLLAGE && getSystemCfgData.uiNDisplays == 3)
                {
                    dispConfig.ConfigType = DisplayConfigType.Vertical;
                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[0].dwDisplayUID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[1].dwDisplayUID)).DisplayType;
                    dispConfig.TertiaryDisplay = dispConfig.EnumeratedDisplays.Find(DUID => DUID.CUIMonitorID.Equals(getSystemCfgData.DispCfg[2].dwDisplayUID)).DisplayType;
                }

            }
            else
            {
                Log.Fail("Failed to GetConfiguration through CUI SDK -> ErrorCode: {0} ", igfxErrorCode);
            }
            return dispConfig;
        }

        public object Set(object args)
        {
            argDispConfig = args as DisplayConfig;
            if (argDispConfig.EnumeratedDisplays == null)
            {
                argDispConfig.EnumeratedDisplays = base.EnumeratedDisplays;
            }
            IGFX_CONFIG_DATA_EX DisplayConfig = new IGFX_CONFIG_DATA_EX();
            FillOpmode(ref DisplayConfig);
            return SwitchToConfig(DisplayConfig, argDispConfig);
        }

        private void FillOpmode(ref IGFX_CONFIG_DATA_EX sdkDispConfig)
        {
            switch (argDispConfig.ConfigType)
            {
                case DisplayConfigType.SD:
                    sdkDispConfig.dwOperatingMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_SINGLE;
                    sdkDispConfig.dwNDisplays = 1;
                    sdkDispConfig.dwPriDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).CUIMonitorID;
                    break;
                case DisplayConfigType.DDC:
                    sdkDispConfig.dwNDisplays = 2;
                    sdkDispConfig.dwOperatingMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE;
                    sdkDispConfig.dwPriDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwSecDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.SecondaryDisplay)).CUIMonitorID;
                    break;
                case DisplayConfigType.TDC:
                    sdkDispConfig.dwNDisplays = 3;
                    sdkDispConfig.dwOperatingMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE;
                    sdkDispConfig.dwPriDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwSecDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.SecondaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwThirdDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.TertiaryDisplay)).CUIMonitorID;
                    break;
                case DisplayConfigType.ED:
                    sdkDispConfig.dwNDisplays = 2;
                    sdkDispConfig.dwOperatingMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD;
                    sdkDispConfig.dwPriDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwSecDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.SecondaryDisplay)).CUIMonitorID;
                    break;
                case DisplayConfigType.TED:
                    sdkDispConfig.dwNDisplays = 3;
                    sdkDispConfig.dwOperatingMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD;
                    sdkDispConfig.dwPriDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwSecDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.SecondaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwThirdDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.TertiaryDisplay)).CUIMonitorID;
                    break;
                case DisplayConfigType.Horizontal:
                    sdkDispConfig.dwNDisplays = (uint)argDispConfig.DisplayList.Count;
                    sdkDispConfig.dwOperatingMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE;
                    sdkDispConfig.dwPriDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwSecDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.SecondaryDisplay)).CUIMonitorID;
                    if(argDispConfig.DisplayList.Count == 3)
                        sdkDispConfig.dwThirdDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.TertiaryDisplay)).CUIMonitorID;
                    break;
                case DisplayConfigType.Vertical:
                    sdkDispConfig.dwNDisplays = (uint)argDispConfig.DisplayList.Count;
                    sdkDispConfig.dwOperatingMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE;
                    sdkDispConfig.dwPriDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).CUIMonitorID;
                    sdkDispConfig.dwSecDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.SecondaryDisplay)).CUIMonitorID;
                    if (argDispConfig.DisplayList.Count == 3)
                        sdkDispConfig.dwThirdDevUID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.TertiaryDisplay)).CUIMonitorID;
                    break;
            }
        }

        public bool SwitchToConfig(IGFX_CONFIG_DATA_EX sdkDispConfig, DisplayConfig argDispConfig)
        {
            IGFX_SYSTEM_CONFIG_DATA_N_VIEWS setsystemCfgData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
            setsystemCfgData.DispCfg = new IGFX_DISPLAY_CONFIG_DATA_EX[6];
            FillOpmodeSizeDeviceIds(ref setsystemCfgData, sdkDispConfig);
            
            DisplayInfo priDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == argDispConfig.PrimaryDisplay).FirstOrDefault();

            if ( argDispConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone
                && base.MachineInfo.PlatformDetails.IsLowpower
                && priDisplayInfo.IsPortraitPanel == true
                && (!base.AppManager.MachineInfo.OS.IsGreaterThan(OSType.WINTHRESHOLD))
                && priDisplayInfo.displayExtnInformation.Equals(DisplayExtensionInfo.Internal))
            {
                Log.Alert("{0} This Configuration Is Not Applicable",argDispConfig);
                return true;
            }
            APIExtensions.DisplayUtil.SetSystemConfigDataNViews(ref setsystemCfgData, out igfxErrorCode, out errorDesc);
            Thread.Sleep(5000);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                DisplayConfig currentDispConfig = new DisplayConfig();
                currentDispConfig = (DisplayConfig)Get(null);
                Log.Verbose("Currect Display Config through CUI SDK is {0}", currentDispConfig.ToString());
                if (argDispConfig.ConfigType == currentDispConfig.ConfigType &&
                    argDispConfig.PrimaryDisplay == currentDispConfig.PrimaryDisplay &&
                    argDispConfig.SecondaryDisplay == currentDispConfig.SecondaryDisplay &&
                    argDispConfig.TertiaryDisplay == currentDispConfig.TertiaryDisplay)
                {
                    Log.Message("Config {0} applied Successfully through SDK", argDispConfig.GetCurrentConfigStr());
                }
                else
                {
                    Log.Fail("Failed to applied config {0} through SDK", argDispConfig.GetCurrentConfigStr());
                    return false;
                }
            }
            else
            {
                Log.Fail("Failed Switch to config through SDK - Error Code: {0}  ErrorDec: {1}", igfxErrorCode, errorDesc);
                return false;
            }
            return true;
        }

        private void FillOpmodeSizeDeviceIds(ref IGFX_SYSTEM_CONFIG_DATA_N_VIEWS systemCfgData, IGFX_CONFIG_DATA_EX sdkDispConfig)
        {
            systemCfgData.dwOpMode = sdkDispConfig.dwOperatingMode;
            systemCfgData.uiNDisplays = sdkDispConfig.dwNDisplays;

            systemCfgData.DispCfg[0].dwDisplayUID = sdkDispConfig.dwPriDevUID;

            if ((sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE
                || sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD
                || sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_HORZCOLLAGE
                || sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DUAL_VERTCOLLAGE)
                && sdkDispConfig.dwNDisplays == 2)
            {
                systemCfgData.uiSize = 152;
                systemCfgData.DispCfg[1].dwDisplayUID = sdkDispConfig.dwSecDevUID;

            }
            else if ((sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE
                    || sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD
                    || sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_HORZCOLLAGE
                    || sdkDispConfig.dwOperatingMode == (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_TRI_VERTCOLLAGE)
                    && sdkDispConfig.dwNDisplays == 3)
                {
                    systemCfgData.uiSize = 220;
                    systemCfgData.DispCfg[1].dwDisplayUID = sdkDispConfig.dwSecDevUID;
                    systemCfgData.DispCfg[2].dwDisplayUID = sdkDispConfig.dwThirdDevUID;
                }
                else
                {
                    systemCfgData.uiSize = 84;
                }
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new System.NotImplementedException();
        }
    }
}
