namespace Intel.VPG.Display.Automation
{
    using System.Configuration;

    public class FeatureConfigurationElement : ConfigurationElement
    {
        [ConfigurationProperty("feature", IsRequired = true)]
        public string Feature
        {
            get { return (string)this["feature"]; }
            set { this["feature"] = value; }
        }
        [ConfigurationProperty("actionClass", IsRequired = true)]
        public string ActionClass
        {
            get { return (string)this["actionClass"]; }
            set { this["actionClass"] = value; }
        }
        [ConfigurationProperty("source", IsRequired = true)]
        public string Source
        {
            get { return (string)this["source"]; }
            set { this["source"] = value; }
        }
    }
}
