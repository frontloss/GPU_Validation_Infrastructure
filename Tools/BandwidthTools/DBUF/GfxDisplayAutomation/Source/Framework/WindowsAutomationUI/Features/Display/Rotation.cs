namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Windows.Automation;
    using System.Collections.Generic;

    public class Rotation : FunctionalBase, IGetAll, ISet, IGet
    {
        private AutomationElement element, innerelement = null;
        private AutomationElementCollection elementColn = null;
        int reTry = 0;
        private List<string> menuList = new List<string>();
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        Dictionary<ScreenOrientation, AutomationElement> _options = new Dictionary<ScreenOrientation, AutomationElement>();
        public Rotation()
        {
            Log.Verbose("In Rotation (Windows Automation UI)");
            System.Threading.Thread.Sleep(200);
            while (element == null && reTry < 3)
            {
                element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.Rotation].AutomationId, ControlType.Custom);
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
                        ScreenOrientation screenorientoption;
                        if (Enum.TryParse(string.Concat("Angle", txt), out screenorientoption))
                            _options.Add(screenorientoption, ele);
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
                        ScreenOrientation screenorientoption;
                        if (Enum.TryParse(string.Concat("Angle", UIABaseHandler.Value(innerelement)), out screenorientoption))
                            return screenorientoption;
                    }
                } return null;
            }
        }
        public object Set
        {
            set
            {
                ScreenOrientation currOrientation = (ScreenOrientation)this.Get;
                if (currOrientation != (ScreenOrientation)value)
                {
                    if (_options.ContainsKey((ScreenOrientation)value))
                        uiaBaseHandler.SendKey(_options[(ScreenOrientation)value]);
                }
            }
        }
        public object GetAll
        {
            get { return this._options.Keys.ToList(); }
        }
    }
}