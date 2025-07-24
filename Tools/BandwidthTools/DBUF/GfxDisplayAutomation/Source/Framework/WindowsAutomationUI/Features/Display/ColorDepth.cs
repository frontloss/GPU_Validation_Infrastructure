namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Automation;

    public class ColorDepth : FunctionalBase, IGetAll
    {
        private AutomationElement element, innerelement = null;
        private AutomationElementCollection elementColn = null;
        int reTry = 0;
        private List<string> menuList = new List<string>();
        private Dictionary<ColorDepthOptions, AutomationElement> _options = new Dictionary<ColorDepthOptions, AutomationElement>();

        public ColorDepth()
        {
            Log.Verbose("In Color Depth (Windows Automation UI)");
            System.Threading.Thread.Sleep(200);
            while (element == null && reTry < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ColorDepth].AutomationId, ControlType.Custom);
                if (element == null) Log.Verbose("Failed to fetch the Feature,{0} at {1} attempt, Trying again", Features.Rotation, ++reTry);
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
                        ColorDepthOptions colorDepthOptions;
                        if (Enum.TryParse(String.Concat("_",txt.Replace(" ","_")), out colorDepthOptions))
                            _options.Add(colorDepthOptions, ele);
                    }
                }
            }
        }
        public object GetAll
        {
            get { return this._options.Keys.ToList(); }
        }
    }
}