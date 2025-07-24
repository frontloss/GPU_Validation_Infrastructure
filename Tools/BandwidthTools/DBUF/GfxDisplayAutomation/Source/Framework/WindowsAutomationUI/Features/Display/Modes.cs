namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;
    using System.Windows.Automation;

    public class Modes : FunctionalBase, ISet, IGet, IGetAll
    {
        private AutomationElement element, innerelement = null;
        private AutomationElementCollection elementColn = null;
        private ControlType controlType;
        private int _retryIdx = 0;
        private List<string> resolutionList = new List<string>();
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        public Modes()
        {
            Log.Verbose("In Modes (Windows Automation UI)");
            System.Threading.Thread.Sleep(200);
            controlType = ControlType.ComboBox;
            while (element == null && _retryIdx < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.Modes].AutomationId, ControlType.ComboBox);
                if (element == null) Log.Verbose("Failed to fetch the Combo Feature,{0} at {1} attempt, Trying again", Features.Modes.ToString(), ++_retryIdx);
                System.Threading.Thread.Sleep(1000);
            }
        }

        public object Set
        {
            set
            {
                string resolution = value as string;            
                Log.Verbose("ComboBoxResolution:: Setting to {0}", resolution);
                ExpandCollapsePattern exPattern = element.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                exPattern.Expand();
                System.Threading.Thread.Sleep(300);
                elementColn = element.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                foreach (AutomationElement e in elementColn)
                {
                    if (e.Current.Name.Replace(" ","").Equals(resolution) || e.Current.Name.Equals(resolution))
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
                    resolutionList.Add(e.Current.Name);
                }
                return resolutionList;
            }
        }
    }
}
