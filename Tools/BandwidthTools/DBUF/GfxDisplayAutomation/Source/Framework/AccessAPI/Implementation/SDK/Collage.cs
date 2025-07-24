namespace Intel.VPG.Display.Automation
{
    class Collage : FunctionalBase, ISetMethod, IGetMethod
    {
        public bool SetMethod(object argMessage)
        {
            CollageParam args = argMessage as CollageParam;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkCollage = sdkExtn.GetSDKHandle(SDKServices.Collage);
            return (bool)sdkCollage.Set(argMessage);
        }

        public object GetMethod(object argMessage)
        {
            CollageParam args = argMessage as CollageParam;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkCollage = sdkExtn.GetSDKHandle(SDKServices.Collage);
            return (CollageParam)sdkCollage.Get(args);
        }
    }
}
