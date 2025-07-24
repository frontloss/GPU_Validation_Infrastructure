namespace Intel.VPG.Display.Automation
{  
    using System.Linq;
    using System.Collections.Generic;

    internal class YCbCr : FunctionalBase, ISetMethod, IGetMethod
    {
        public bool SetMethod(object argMessage)
        {
            XvYccYcbXr args = argMessage as XvYccYcbXr;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkYCbCr = sdkExtn.GetSDKHandle(SDKServices.YCbCr);
            return (bool)sdkYCbCr.Set(args);
        }
        public object GetMethod(object argMessage)
        {
            XvYccYcbXr args = argMessage as XvYccYcbXr;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkYCbCr = sdkExtn.GetSDKHandle(SDKServices.YCbCr);
            return (XvYccYcbXr)sdkYCbCr.Get(args);
        }
    }
}