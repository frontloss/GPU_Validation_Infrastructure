namespace Intel.VPG.Display.Automation
{
    class SDKConfig : FunctionalBase, ISetMethod, IGet
    {
        public bool SetMethod(object argMessage)
        {
            DisplayConfig args = argMessage as DisplayConfig;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkConfig = sdkExtn.GetSDKHandle(SDKServices.Config);
            return (bool)sdkConfig.Set(args);
        }

        public object Get
        {
            get 
            {
                SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
                ISDK sdkConfig = sdkExtn.GetSDKHandle(SDKServices.Config);
                return (DisplayConfig)sdkConfig.Get(null);
            }
        }
    }
}
