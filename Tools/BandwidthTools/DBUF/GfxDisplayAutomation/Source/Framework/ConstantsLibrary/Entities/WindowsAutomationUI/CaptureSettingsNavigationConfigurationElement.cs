namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Configuration;

    public class CaptureSettingsNavigationConfigurationElement : ConfigurationElement
    {
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

        [ConfigurationProperty("uiaName", IsRequired = false)]
        public string UiaName
        {
            get
            {
                return (string)this["uiaName"];
            }
            set
            {
                this["uiaName"] = value;
            }
        }

        [ConfigurationProperty("controlType", IsRequired = false)]
        public string ControlType
        {
            get
            {
                return (string)this["controlType"];
            }
            set
            {
                this["controlType"] = value;
            }
        }

        [ConfigurationProperty("patternMethod", IsRequired = false)]
        public string PatternMethod
        {
            get
            {
                return (string)this["patternMethod"];
            }
            set
            {
                this["patternMethod"] = value;
            }
        }

        [ConfigurationProperty("cAutomationId", IsRequired = false)]
        public string ChildAutomationId
        {
            get
            {
                return (string)this["cAutomationId"];
            }
            set
            {
                this["cAutomationId"] = value;
            }
        }
    }
}
