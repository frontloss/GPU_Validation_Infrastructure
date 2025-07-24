namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Configuration;

    public class CaptureSettingsFeatureConfigurationElement : ConfigurationElement
    {
        [ConfigurationProperty("feature", IsRequired = false)]
        public string Feature 
        { 
            get 
            {
                return (string)this["feature"]; 
            } 
            set 
            {
                this["feature"] = value; 
            } 
        }

        [ConfigurationProperty("automationId", IsRequired = false)]
        public string AutomationId
        {
            get
            {
                return (string)this["automationId"];
            }
            set
            {
                this["automationId"] = value;
            }
        }

        [ConfigurationProperty("options", IsRequired = false)]
        public string options
        {
            get
            {
                return (string)this["options"];
            }
            set
            {
                this["options"] = value;
            }
        }
    }
}
