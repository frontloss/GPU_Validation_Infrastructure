namespace Intel.VPG.Display.Automation
{
    using System.Configuration;

    public class FeatureSection : ConfigurationSection
    {        
        [ConfigurationProperty("captureSettings", IsRequired = true)]
        [ConfigurationCollection(typeof(FeatureConfigurationElement), AddItemName = "add", ClearItemsName = "clear", RemoveItemName = "remove")]
        private GenericCaptureToolConfigElement<FeatureConfigurationElement> CaptureSettings 
        { 
            get 
            {
                return (GenericCaptureToolConfigElement<FeatureConfigurationElement>)this["captureSettings"]; 
            } 
        }

        public GenericCaptureToolConfigElement<FeatureConfigurationElement> GetCaptureSettings()
        {
            if (CaptureSettings == null)
            {
                return (GenericCaptureToolConfigElement<FeatureConfigurationElement>)this["captureSettings"];
            }
            else
            {
                return CaptureSettings;
            }
        }
    }
}
