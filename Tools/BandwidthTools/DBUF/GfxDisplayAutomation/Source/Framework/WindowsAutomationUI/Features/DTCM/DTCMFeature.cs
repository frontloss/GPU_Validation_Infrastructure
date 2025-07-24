namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Automation;
    using System.Reflection;
    using System;

    public class DTCMFeature : FunctionalBase,ISetMethod, IGetMethod
    {
        public AutomationElementCollection elementColn = null;
        public object GetMethod(object argMessage)
        {
            Log.Verbose("In DTCMFeature GetMethod (Windows Automation UI)");
            string NavFeatureName = argMessage as string;
            Features feature;
            Enum.TryParse<Features>(NavFeatureName, out feature);
            Dictionary<string, string> navigationList = feature.GetNavigationList();
            navigationList.ToList().ForEach(kV =>
            {
                UIExtensions.setUIAEntity(kV.Key);
            });
            if (UIABaseHandler.SelectElementNameControlType(navigationList[feature.ToString()].Replace("_", " "), ControlType.MenuItem) != null)
            {
                Log.Message("{0} found in DTCM", NavFeatureName);
                return true;
            }
            else
            {
                Log.Message("{0} not found in DTCM", NavFeatureName);
                return false;
            }
        }

        public bool SetMethod(object argMessage)
        {
            Log.Verbose("In DTCMFeature SetMethod (Windows Automation UI)");
            string dtcmOption = argMessage as string;
            NavigationHandler nav = new NavigationHandler() { NavigationItem = dtcmOption.Replace("_", " ") };
            nav.Navigate();
            return true;
        }
    }
}