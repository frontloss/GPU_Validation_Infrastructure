namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Threading;
    using System.Reflection;
    using System.Diagnostics;
    using System.Windows.Automation;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using System.Security;
    using System.Xml.Serialization;
    using System.Xml;
    using System.Net.NetworkInformation;
    using System.Text;
    using System.Net;

    public static class UIExtensions
    {
        private static XDocument _featuresMap = null;
        private static XDocument _navigationsMap = null;

        public static Dictionary<string, CaptureSettingsNavigationConfigurationElement> NavigationDictionary = new Dictionary<string, CaptureSettingsNavigationConfigurationElement>();
        public static Dictionary<Features, CaptureSettingsFeatureConfigurationElement> FeaturesDictionary = new Dictionary<Features, CaptureSettingsFeatureConfigurationElement>();
        private static CaptureSettingsNavigationConfigurationElement navigationElement;
        private static CaptureSettingsFeatureConfigurationElement featureElement;
        public static void Load(IApplicationSettings argAppSettings)
        {
            _featuresMap = XDocument.Load("Mapper\\WindowsUIFeaturesConfiguration.map");
            _navigationsMap = XDocument.Load("Mapper\\WindowsUINavigationConfiguration.map");
        }
        public static void Load(IApplicationSettings argAppSettings, string args)
        {
            if (args.Equals("15.36"))
            {
                Log.Verbose("Loading mapper for {0} baseline driver", args);
                _featuresMap = XDocument.Load("Mapper\\WindowsUIFeaturesConfiguration.map");
                _navigationsMap = XDocument.Load("Mapper\\WindowsUINavigationConfiguration.map");
            }
            else if (args.Equals("15.33"))
            {
                Log.Verbose("Loading mapper for {0} baseline driver", args);
                _featuresMap = XDocument.Load("Mapper\\15.33\\WindowsUIFeaturesConfiguration.map");
                _navigationsMap = XDocument.Load("Mapper\\15.33\\WindowsUINavigationConfiguration.map");
            }
            else
            {
                Log.Verbose("Loading mapper for {0} baseline driver", args);
                _featuresMap = XDocument.Load("Mapper\\15.40\\WindowsUIFeaturesConfiguration.map");
                _navigationsMap = XDocument.Load("Mapper\\15.40\\WindowsUINavigationConfiguration.map");
            }

        }
        public static void setUIAEntity(Features feature)
        {
            if (FeaturesDictionary.Count == 0)
                FeaturesDictionary = new Dictionary<Features, CaptureSettingsFeatureConfigurationElement>();
            XElement featureElement = (from c in _featuresMap.Elements("Features").Descendants("feature")
                                       where ((string)c.Attribute("name") == feature.ToString() && String.Compare(c.Attribute("source").Value, "AccessAPI") != 0)
                                       select c).FirstOrDefault();
            if (featureElement != null)
            {
                CaptureSettingsFeatureConfigurationElement captureSettings = GetCaptureSettingsForFeatureElement(featureElement);
                if (!(FeaturesDictionary.ContainsKey(feature)))
                    FeaturesDictionary.Add(feature, captureSettings);
            }
            if (featureElement != null && featureElement.HasElements)
            {
                IEnumerable<XElement> allSubFeatures = featureElement.Elements();
                foreach (XElement subElement in allSubFeatures)
                {
                    if (subElement != null)
                    {
                        CaptureSettingsFeatureConfigurationElement captureSettings = GetCaptureSettingsForFeatureElement(subElement);
                        XAttribute subFeature = subElement.Attribute("name");
                        Features subFeatures;
                        if (Enum.TryParse(subFeature.Value, out subFeatures))
                        {
                            if (!(FeaturesDictionary.ContainsKey(subFeatures)))
                                FeaturesDictionary.Add(subFeatures, captureSettings);
                        }
                    }
                }
            }
        }
        public static void setUIAEntity(string Navigation)
        {
            List<XElement> landscapeElements = new List<XElement>(); ;
            bool landscape = Orientation.Landscape();
            if (NavigationDictionary.Count == 0)
                NavigationDictionary = new Dictionary<string, CaptureSettingsNavigationConfigurationElement>();
            landscapeElements = (from c in _navigationsMap.Root.Descendants("Landscape") select c).ToList();
            if (landscapeElements.Count == 0)
            {
                XElement navigationElement = (from c in _navigationsMap.Descendants(Navigation) select c).FirstOrDefault();
                if (navigationElement != null)
                {
                    CaptureSettingsNavigationConfigurationElement captureSettings = GetCaptureSettingsForNavigationElement(navigationElement);
                    if (!(NavigationDictionary.ContainsKey(Navigation.Replace("_", " "))))
                        NavigationDictionary.Add(Navigation.Replace("_", " "), captureSettings);
                }
            }
            else
            {
                foreach (XElement landscapeElement in landscapeElements)
                {
                    XAttribute subFeature = landscapeElement.Attribute("value");
                    if (String.Equals(subFeature.Value.ToString().ToLower(), landscape.ToString().ToLower()))
                    {
                        XElement navigationElement = (from c in landscapeElement.Descendants(Navigation) select c).FirstOrDefault();
                        if (navigationElement != null)
                        {
                            CaptureSettingsNavigationConfigurationElement captureSettings = GetCaptureSettingsForNavigationElement(navigationElement);
                            if (NavigationDictionary.ContainsKey(Navigation.Replace("_", " ")))
                                NavigationDictionary.Remove(Navigation.Replace("_", " "));
                            NavigationDictionary.Add(Navigation.Replace("_", " "), captureSettings);
                        }
                    }
                    if (NavigationDictionary.ContainsKey("Landscape")) NavigationDictionary.Remove("Landscape");
                }
            }
        }
        private static CaptureSettingsNavigationConfigurationElement GetCaptureSettingsForNavigationElement(XElement argElementNavigation)
        {
            navigationElement = new CaptureSettingsNavigationConfigurationElement()
            {
                AutomationId = argElementNavigation.Attribute("automationId") != null ? argElementNavigation.Attribute("automationId").Value : string.Empty,
                UiaName = argElementNavigation.Attribute("uiaName") != null ? argElementNavigation.Attribute("uiaName").Value : string.Empty,
                ControlType = argElementNavigation.Attribute("controlType") != null ? argElementNavigation.Attribute("controlType").Value : string.Empty,
                PatternMethod = argElementNavigation.Attribute("patternMethod") != null ? argElementNavigation.Attribute("patternMethod").Value : string.Empty,
                ChildAutomationId = argElementNavigation.Attribute("cAutomationId") != null ? argElementNavigation.Attribute("cAutomationId").Value : string.Empty
            };
            return navigationElement;
        }
        private static CaptureSettingsFeatureConfigurationElement GetCaptureSettingsForFeatureElement(XElement argElementFeature)
        {
            featureElement = new CaptureSettingsFeatureConfigurationElement()
            {
                AutomationId = argElementFeature.Attribute("automationId") != null ? argElementFeature.Attribute("automationId").Value : string.Empty,
                Feature = argElementFeature.Attribute("feature") != null ? argElementFeature.Attribute("feature").Value : string.Empty,
                options = argElementFeature.Attribute("options") != null ? argElementFeature.Attribute("options").Value : string.Empty
            };
            return featureElement;
        }
    }
}
