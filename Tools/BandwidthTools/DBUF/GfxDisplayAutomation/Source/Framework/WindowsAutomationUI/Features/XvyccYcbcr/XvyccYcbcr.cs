namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Automation;
    using System.Threading;

    public class XvyccYcbcr :FunctionalBase, ISet, IGet, IGetMethod
    {
        private AutomationElement element = null;
        private AutomationElementCollection elementColn = null;
        private List<string> menuList = new List<string>();
        int reTry = 0;
        private List<AutomationElement> _enableDisable = new List<AutomationElement>();
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        public XvyccYcbcr()
        {
            Log.Verbose("In XvyccYcbcr (Windows Automation UI)");
            Thread.Sleep(200);
            while (element == null && reTry < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.XvyccYcbcr].AutomationId, ControlType.Custom);
                if (element == null) Log.Verbose("Failed to fetch the Feature,{0} at {1} attempt, Trying again", Features.XvyccYcbcr.ToString(), ++reTry);
                System.Threading.Thread.Sleep(1000);
            }
            if (element != null)
            {
                Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                    new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                elementColn = element.FindAll(TreeScope.Descendants, condition);
                foreach (AutomationElement ele in elementColn)
                    _enableDisable.Add(ele);
            }
        }
        public object GetMethod(object argMessage)
        {
            if (!(_enableDisable.Count == 0))
                return PanelType.XVYCC_YCBCR;
            else
                return PanelType.RGB;
        }
        public object Get
        {
            get 
            {
                foreach (AutomationElement e in elementColn)
                {
                    if (e.Current.ItemStatus == "Selected")
                    {
                        int idx = Convert.ToInt32(e.Current.AutomationId.Split('_')[1]);
                        Log.Message("{0}", idx);
                        return ((DecisionActions)(idx));
                    }
                } return null;
            }
        }
        public object Set
        {
            set
            {
                int argValue = (int)Enum.Parse(typeof(DecisionActions), value.ToString());
                uiaBaseHandler.SendKey(_enableDisable.ElementAt((int)Enum.Parse(typeof(DecisionActions), value.ToString())));
            }
        }
    }
}
