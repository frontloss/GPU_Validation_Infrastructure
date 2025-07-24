namespace Intel.VPG.Display.Automation
{
    using System;
    using IgfxExtBridge_DotNet;
    using System.Threading;

    /*  Get set collage through CUI SDK 7.0 */
    class Collage_v1 : FunctionalBase, ISDK
    {
        private DisplayConfig argDispConfig;
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private String errorDesc = "";

        public object Get(object args)
        {
            CollageParam collageOption = args as CollageParam;
            if (collageOption.option == CollageOption.IsCollageSupported)
                collageOption.isCollageSupported = IsCollageSupported();
            else if (collageOption.option == CollageOption.GetConfig)
                collageOption.config = GetDisplayConfig();
            else
                Log.Fail("Wrong Input Parameter");
            return collageOption;
        }

        public object Set(object args)
        {
            CollageParam collageOption = args as CollageParam;
            bool status = false;
            if (collageOption.option == CollageOption.Enable)
            {
                status = EnableCollage();
            }
            else if (collageOption.option == CollageOption.Disable)
            {
                status = DisableCollage();
            }
            else if (collageOption.option == CollageOption.SetConfig)
            {
                if (collageOption.config.ConfigType == DisplayConfigType.Horizontal ||
                    collageOption.config.ConfigType == DisplayConfigType.Vertical)
                {
                    status = SetCollage(collageOption.config);
                }
                else
                    Log.Fail("Wrong Config type {0} has passed for collage config", collageOption.config.ConfigType);
            }
            else
                Log.Fail("Wrong Input Parameter for Collage Config");
            return status;
        }

        private bool IsCollageSupported()
        {
            IGFX_COLLAGE_STATUS collageStatus = new IGFX_COLLAGE_STATUS();
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
            String errorDesc = "";
            collageStatus.versionHeader.dwVersion = 1;
            APIExtensions.DisplayUtil.GetCollageStatus(ref collageStatus, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                return collageStatus.bIsCollageModeSupported == 1;
            else
            {
                Log.Fail("Failed to Get Collage Status");
                return false;
            }
        }

        private DisplayConfig GetDisplayConfig()
        {
            SDKConfig sdkConfig = base.CreateInstance<SDKConfig>(new SDKConfig());
            return (DisplayConfig)sdkConfig.Get;
        }

        private bool EnableCollage()
        {
            IGFX_COLLAGE_STATUS collageStatus = new IGFX_COLLAGE_STATUS();
            collageStatus.versionHeader.dwVersion = 1;
            APIExtensions.DisplayUtil.GetCollageStatus(ref collageStatus, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                if (collageStatus.bIsCollageModeSupported == 1)
                {
                    if (collageStatus.bIsCollageModeEnabled == 1)
                    {
                        Log.Message("Collage is Enabled");
                        return true;
                    }
                    else
                    {
                        collageStatus.bIsCollageModeEnabled = 1;
                        APIExtensions.DisplayUtil.SetCollageStatus(ref collageStatus, out igfxErrorCode, out errorDesc);
                        if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                        {
                            Log.Success("Collage successfully enabled through SDK");
                            Thread.Sleep(5000);
                            return true;
                        }
                        else
                            Log.Fail("Failed to enable collage through SDK - Error Code: {0}  Error Dec: {1}", igfxErrorCode, errorDesc);
                    }
                }
                else
                    Log.Fail("Collage is not Supported - Error Code: {0}  ErrorDec: {1}", igfxErrorCode, errorDesc);
            }
            else
                Log.Fail("Failed to Get Collage Status - Error Code: {0}  ErrorDec: {1}", igfxErrorCode, errorDesc);
            return false;
        }

        private bool DisableCollage()
        {
            IGFX_COLLAGE_STATUS collageStatus = new IGFX_COLLAGE_STATUS();
            collageStatus.versionHeader.dwVersion = 1;
            APIExtensions.DisplayUtil.GetCollageStatus(ref collageStatus, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                if (collageStatus.bIsCollageModeSupported == 1)
                {
                    if (collageStatus.bIsCollageModeEnabled == 0)
                    {
                        Log.Message("Collage is disabled");
                        return true;
                    }
                    else
                    {
                        collageStatus.bIsCollageModeEnabled = 0;
                        APIExtensions.DisplayUtil.SetCollageStatus(ref collageStatus, out igfxErrorCode, out errorDesc);
                        if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                        {
                            Log.Success("Successfully disable collage through SDK");
                            Thread.Sleep(5000);
                            return true;
                        }
                        else
                            Log.Fail("Failed to disable collage through SDK - Error Code : {0}  ErrorDec : {1}", igfxErrorCode, errorDesc);
                    }
                }
                else
                    Log.Fail("Collage not supported - Error Code: {0}  ErrorDec: {1}", igfxErrorCode, errorDesc);
            }
            else
                Log.Fail("Failed to get collage status through SDK - Error Code: {0}  ErrorDec: {1}", igfxErrorCode, errorDesc);
            return false;
        }

        private bool SetCollage(object argMessage)
        {
            argDispConfig = argMessage as DisplayConfig;
            if (argDispConfig.EnumeratedDisplays == null)
            {
                argDispConfig.EnumeratedDisplays = base.EnumeratedDisplays;
            }
            SDKConfig sdkConfig = base.CreateInstance<SDKConfig>(new SDKConfig());
            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
            {
                EnableCollage();
            }
            return sdkConfig.SetMethod(argDispConfig);
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
