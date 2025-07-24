namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;
    using System.Windows.Automation;

    public class RefreshRate : FunctionalBase, ISet, IGet, IGetAll
    {
        private AutomationElement element, innerelement = null;
        private AutomationElementCollection elementColn = null;
        private ControlType controlType;
        private int _retryIdx = 0;
        List<string> refreshRateList = new List<string>();
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        public RefreshRate()
        {
            Log.Verbose("In refresh Rate (Windows Automation UI)");
            System.Threading.Thread.Sleep(200);
            controlType = ControlType.ComboBox;
            while (element == null && _retryIdx < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.RefreshRate].AutomationId, ControlType.ComboBox);
                element = UIABaseHandler.selectChildElement(UIABaseHandler.SelectElementAutomationIdControlType("refreshRateControl", ControlType.Custom), ControlType.ComboBox);
                if (element == null) Log.Verbose("Failed to fetch the Combo Feature,{0} at {1} attempt, Trying again", Features.RefreshRate.ToString(), ++_retryIdx);
                System.Threading.Thread.Sleep(1000);
            }
        }
        public object Set
        {
            set
            {
                string refreshRate = value as string;
                Log.Verbose("ComboBoxResolution:: Setting to {0}", refreshRate);
                ExpandCollapsePattern exPattern = element.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                exPattern.Expand();
                System.Threading.Thread.Sleep(300);
                elementColn = element.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                foreach (AutomationElement e in elementColn)
                {
                    Log.Verbose("{0} - {1}", e.Current.Name, refreshRate);
                    if (e.Current.Name.Contains(refreshRate))
                    {
                        innerelement = e;
                        break;
                    }
                }
                uiaBaseHandler.SelectionItem(innerelement);
                exPattern.Collapse();
            }
        }
        public virtual object Get
        {
            get
            {
                SelectionPattern pattern = element.GetCurrentPattern(SelectionPattern.Pattern) as SelectionPattern;
                return pattern.Current.GetSelection().First().Current.Name;
            }
        }
        public object GetAll
        {
            get
            {
                elementColn = element.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                foreach (AutomationElement e in elementColn)
                {
                    refreshRateList.Add(e.Current.Name);
                }
                return refreshRateList;
            }
        }
    }
}
