using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;
using System.Windows.Automation;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

namespace Intel.VPG.Display.Automation
{
    public class NavigationHandler : UIABaseHandler, INavigate
    {
        public string NavigationItem;  
        public NavigationHandler () { }
        public NavigationHandler(string argNavigation)
        {
            NavigationItem = argNavigation;
        }
        public void Navigate()
        {
            AutomationElement element;
            string PatternMethod = UIExtensions.NavigationDictionary[NavigationItem].PatternMethod;
            Log.Verbose("Navigating to {0}", NavigationItem);
            MethodInfo patternMethod = this.GetType().GetMethod(PatternMethod);
            if (UIExtensions.NavigationDictionary[NavigationItem].UiaName != "" ||
                UIExtensions.NavigationDictionary[NavigationItem].ControlType != "" ||
                UIExtensions.NavigationDictionary[NavigationItem].AutomationId != "")
            {
                element = base.SelectElement(AutomationElement.RootElement, NavigationItem); 
                if((NavigationItem.Equals("Enable") && (element.Current.IsEnabled == false)))
                    Log.Message("Hot Keys is already enabled");
                else
                    patternMethod.Invoke(this, new object[] { element });
            }
            else
            {
                patternMethod.Invoke(this, new object[] {  });
            }
        }    
    }
}
