namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class SdkIndependentRotation : FunctionalBase, ISetMethod
    {
        public bool SetMethod(object argMessage)
        {
            List<DisplayMode> args = (List<DisplayMode>)argMessage;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkIndependentRotation = sdkExtn.GetSDKHandle(SDKServices.IndependentRotation);
            return (bool)sdkIndependentRotation.Set(args);
        }
    }
}

