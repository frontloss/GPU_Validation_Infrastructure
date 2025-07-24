namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Windows.Automation;
    class ChangeAudioSource : FunctionalBase, ISet
    {
        private AutomationElement element, innerelement = null;
        private AutomationElementCollection elementColn = null;
        private Dictionary<string, AutomationElement> _options = new Dictionary<string, AutomationElement>();
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();
        public ChangeAudioSource()
        {
            element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ChangeAudioSource].AutomationId, ControlType.Custom);
            if (element != null)
            {
                Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                    new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                elementColn = element.FindAll(TreeScope.Descendants, condition);
                foreach (AutomationElement ele in elementColn)
                {
                    innerelement = TreeWalker.ControlViewWalker.GetFirstChild(ele);
                    if (ele.Current.IsKeyboardFocusable)
                        _options.Add(UIABaseHandler.Value(innerelement).Split(' ').First().ToLower(), ele);
                }
            }
        }

        public object Set
        {
            set 
            {
                AudioInputSource source = (AudioInputSource)value;
                Log.Verbose("Setting audio input source as {0} source", source.ToString());
                if (_options.ContainsKey(source.ToString().ToLower()))
                    uiaBaseHandler.SendKey(_options[source.ToString().ToLower()]);
            }
        }
    }
}
