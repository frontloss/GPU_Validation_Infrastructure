namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Automation;

    public class Scaling : FunctionalBase, IGetAll, IGet, ISet
    {
        private AutomationElement element, innerelement = null;
        private AutomationElementCollection elementColn = null;
        int reTry = 0;
        private List<string> menuList = new List<string>();
        private Dictionary<ScalingOptions, AutomationElement> _options = new Dictionary<ScalingOptions, AutomationElement>();
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        public Scaling()
        {
            Log.Verbose("In Scaling (Windows Automation UI)");
            System.Threading.Thread.Sleep(200);
            while (element == null && reTry < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.Scaling].AutomationId, ControlType.Custom);
                if (element == null) Log.Verbose("Failed to fetch the Feature,{0} at {1} attempt, Trying again", Features.Scaling, ++reTry);
                System.Threading.Thread.Sleep(1000);
            }

            if (element != null)
            {
                Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                    new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                elementColn = element.FindAll(TreeScope.Descendants, condition);             
                string txt = "";
                foreach (AutomationElement ele in elementColn)
                {
                    innerelement = TreeWalker.ControlViewWalker.GetFirstChild(ele);         
                    if (ele.Current.IsKeyboardFocusable)
                    {
                        txt = UIABaseHandler.Value(innerelement);
                        ScalingOptions scalingOption;
                        if (Enum.TryParse(txt.Replace(" ","_"), out scalingOption))
                            _options.Add(scalingOption, ele);
                    }
                }
            }
        }
        public object Get
        {
            get
            {
                foreach (AutomationElement e in elementColn)
                {
                    if (e.Current.ItemStatus == "Selected")
                    {
                        innerelement = TreeWalker.ControlViewWalker.GetFirstChild(e);
                        ScalingOptions scalingOptions;
                        if (Enum.TryParse(UIABaseHandler.Value(innerelement).Replace(" ","_"), out scalingOptions))
                            return scalingOptions;
                    }
                } return null;
            }
        }
        public object Set
        {
            set
            {
                ScalingOptions currOrientation = (ScalingOptions)this.Get;
                if (currOrientation != (ScalingOptions)value)
                {
                    if (_options.ContainsKey((ScalingOptions)value))
                        uiaBaseHandler.SendKey(_options[(ScalingOptions)value]);
                }
            }
        }
        public object GetAll
        {
            get { return this._options.Keys.ToList(); }
        }
    }
}