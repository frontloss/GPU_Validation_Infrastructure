namespace Intel.VPG.Display.Automation
{   
    using System.Linq;
    using System.Collections.Generic;

    internal class XvYcc : FunctionalBase, ISetMethod, IGetMethod
    {
        public bool SetMethod(object argMessage)
        {
            XvYccYcbXr args = argMessage as XvYccYcbXr;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkXvYcc = sdkExtn.GetSDKHandle(SDKServices.XvYcc);
            return (bool)sdkXvYcc.Set(args);
        }
        public object GetMethod(object argMessage)
        {
            XvYccYcbXr args = argMessage as XvYccYcbXr;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkXvYcc = sdkExtn.GetSDKHandle(SDKServices.XvYcc);
            return (XvYccYcbXr)sdkXvYcc.Get(args);
        }
    }
}