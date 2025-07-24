namespace Intel.VPG.Display.Automation
{
    using igfxSDKLib;

    /*  Get set collage through CUI SDK 8.0 */
    class Collage_v2 : FunctionalBase, ISDK
    {
        DisplayConfiguration Config;

        public object Get(object args)
        {
            CollageParam collageOption = args as CollageParam;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            Config = GfxSDK.Display.Configuration;
            Config.Get();

            if (collageOption.option == CollageOption.IsCollageSupported)
                collageOption.isCollageSupported = Config.Collage.IsSupported;
            else if (collageOption.option == CollageOption.GetConfig)
                collageOption.config = GetDisplayConfig();
            else
                Log.Fail("Wrong Input Parameter");
            return collageOption;
        }

        public object Set(object args)
        {
            CollageParam collageOption = args as CollageParam;
            GfxSDKClass GfxSDK = new GfxSDKClass();
            bool status = false;
            Config = GfxSDK.Display.Configuration;

            if (collageOption.option == CollageOption.Enable)
            {
                status = DisableEnableCollage(true);
            }
            else if (collageOption.option == CollageOption.Disable)
            {
                status = DisableEnableCollage(false);
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

        private DisplayConfig GetDisplayConfig()
        {
            SDKConfig sdkConfig = base.CreateInstance<SDKConfig>(new SDKConfig());
            return (DisplayConfig)sdkConfig.Get;
        }

        private bool DisableEnableCollage(bool isEnable)
        {
            if (false == Config.Collage.IsSupported)
            {
                Log.Fail("Collage is not supported");
                return false;
            }
            Log.Verbose("{0} Collage through SDK", (isEnable == true) ? "Enabling" : "Disabling");
            if(true == isEnable)
                Config.Collage.ENABLE();
            else
                Config.Collage.DISABLE();

            if (Config.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                Log.Success("Successfully {0} collage through SDK", (isEnable == true) ? "Enable" : "Disable");
                return true;
            }
            else
            {
                Log.Fail("Failed to {0} collage through SDK", (isEnable == true) ? "Enable" : "Disable");
                return false;
            }
        }

        private bool SetCollage(object argMessage)
        {
            DisplayConfig argDispConfig  = argMessage as DisplayConfig;
            if (argDispConfig.EnumeratedDisplays == null)
            {
                argDispConfig.EnumeratedDisplays = base.EnumeratedDisplays;
            }
            SDKConfig sdkConfig = base.CreateInstance<SDKConfig>(new SDKConfig());
            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
                DisableEnableCollage(true);
            return sdkConfig.SetMethod(argDispConfig);
        }


        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new System.NotImplementedException();
        }
    }
}
