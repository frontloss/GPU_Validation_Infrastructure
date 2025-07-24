namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;
    using System.Windows.Automation;


    public class SelectDisplay : FunctionalBase, ISet, IGet
    {
        public AutomationElement element, innerelement = null;
        public AutomationElementCollection elementColn = null;
        public ControlType controlType;
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();
        private int _retryIdx = 0;

        public SelectDisplay()
            : base()
        {
            Log.Verbose("In Select Display (Windows Automation UI)");
            controlType = ControlType.ComboBox;
            while (element == null && _retryIdx < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.SelectDisplay].AutomationId, ControlType.ComboBox);
                if (element == null) Log.Verbose("Failed to fetch the Combo Feature,{0} at {1} attempt, Trying again",Features.SelectDisplay.ToString(), ++_retryIdx);
                System.Threading.Thread.Sleep(1000);
            }
        }
        public SelectDisplay(AutomationElement argElement)
            : base()
        {         
            this.element = argElement;
            if (element == null) Log.Verbose("Failed to fetch the Combo Feature,{0} at {1} attempt, Trying again", Features.SelectDisplayInfo.ToString(), ++_retryIdx);
            System.Threading.Thread.Sleep(1000);
        }
        public object Set
        {
            set
            {
                 DisplayType displayType = (DisplayType)value;
                 string actualDisplayName = base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).Select(dI => dI.CompleteDisplayName).FirstOrDefault();
                 Log.Verbose("ComboBoxChooseDisplay:: Setting to {0}", actualDisplayName);
                 ExpandCollapsePattern exPattern = element.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                 exPattern.Expand();
                 System.Threading.Thread.Sleep(300);
                 elementColn = element.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                 foreach (AutomationElement e in elementColn)
                 {
                     if (e.Current.Name.ToString().Equals(actualDisplayName))
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
                return base.EnumeratedDisplays.Where(dI => !string.IsNullOrEmpty(dI.CompleteDisplayName) && dI.CompleteDisplayName.Equals(pattern.Current.GetSelection().First().Current.Name)).Select(dI => dI.DisplayType).FirstOrDefault();
            }
        }

    }
}


