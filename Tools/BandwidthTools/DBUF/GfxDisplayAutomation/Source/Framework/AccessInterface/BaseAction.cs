namespace Intel.VPG.Display.Automation
{
    internal class BaseAction
    {
        protected object GetCaptureInstance(Message argMessage)
        {
            object functionalObj = argMessage.Feature.Activate(argMessage.Source);
            FunctionalBase funcBase = functionalObj as FunctionalBase;
            funcBase.AppManager = argMessage.AppManager;
            funcBase.AppSettings = argMessage.AppManager.ApplicationSettings;
            funcBase.EnumeratedDisplays = argMessage.EnumeratedDisplays;
            funcBase.CurrentMethodIndex = argMessage.CurrentMethodIndex;
            funcBase.OverrideMethodIndex = argMessage.OverrideMethodIndex;
            funcBase.CurrentConfig = argMessage.CurrentConfig;
            return functionalObj;
        }
    }
}