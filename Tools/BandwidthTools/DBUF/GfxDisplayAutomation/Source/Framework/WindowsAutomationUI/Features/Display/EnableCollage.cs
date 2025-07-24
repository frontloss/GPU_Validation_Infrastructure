namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Automation;
    using System;

    class EnableCollage : FunctionalBase, IGet, ISet
    {
        AutomationElement element, innerelement = null;
        AutomationElement comboElement;
        private AutomationElementCollection elementColn = null;
        private AutomationElementCollection comboElementColn = null;
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();

        public EnableCollage()
        {
            Log.Verbose("In Enable Collage (Windows Automation UI)");
            Config configObject = new Config();
            configObject.SetConfigType(DisplayUnifiedConfig.Collage);
            element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.EnableCollage].AutomationId, ControlType.Custom);
            comboElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ComboBoxEnableDisableCollage].AutomationId, ControlType.ComboBox);
        }
        public EnableCollage(Features argFeature)
        {
            Log.Verbose("In Ennable collage(Feature) (Windows Automation UI)");
            Config configObject = new Config(Features.DisplayConfig);
            configObject.SetConfigType(DisplayUnifiedConfig.Collage);
            element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.EnableDisableCollage].AutomationId, ControlType.Custom);
            comboElement = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.ComboBoxEnableDisableCollage].AutomationId, ControlType.ComboBox);
        }
        public object Get
        {
            get
            {
                if ((null == comboElement) || (this.comboElement.Current.IsOffscreen))
                {
                    Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                        new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                    elementColn = element.FindAll(TreeScope.Descendants, condition);
                    string text = "";
                    foreach (AutomationElement e in elementColn)
                    {
                        if (e.Current.ItemStatus == "Selected")
                        {
                            innerelement = TreeWalker.ControlViewWalker.GetFirstChild(e);
                            break;
                        }

                    }
                    text = UIABaseHandler.Value(innerelement);
                    CollageOptions collageOption;
                    if (Enum.TryParse(text, out collageOption))
                        return collageOption;
                    else
                        return default(CollageOptions);
                }
                else
                {
                    SelectionPattern pattern = comboElement.GetCurrentPattern(SelectionPattern.Pattern) as SelectionPattern;
                    string text = pattern.Current.GetSelection().First().Current.Name;
                    DisplayUnifiedConfig unifiedConfigOption;
                    if (Enum.TryParse(text, out unifiedConfigOption))
                        return unifiedConfigOption;
                }
                return default(CollageOptions);
            }
        }
        public object Set
        {
            set
            {
                CollageOptions collageOption = (CollageOptions)value;
                if ((null == comboElement) || (this.comboElement.Current.IsOffscreen))
                {
                    Condition condition = new AndCondition(new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Custom),
                        new NotCondition(new PropertyCondition(AutomationElement.ClassNameProperty, "IntelLabelControl")));
                    elementColn = element.FindAll(TreeScope.Descendants, condition);
                    string text = "";
                    foreach (AutomationElement ele in elementColn)
                    {
                        innerelement = TreeWalker.ControlViewWalker.GetFirstChild(ele);
                        text = UIABaseHandler.Value(innerelement);
                        if (text.Equals(collageOption.ToString()))
                            uiaBaseHandler.SendKey(ele);
                    }
                }
                else
                {
                    ExpandCollapsePattern exPattern = comboElement.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                    exPattern.Expand();
                    System.Threading.Thread.Sleep(300);
                    comboElementColn = comboElement.FindAll(TreeScope.Children, new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ListItem));
                    Log.Message("collageoption = {0}", collageOption);
                    foreach (AutomationElement e in comboElementColn)
                    {
                        Log.Message("e.current.name = {0}", e.Current.Name.ToString());

                        if (e.Current.Name.ToString().Equals(collageOption.ToString()))
                        {
                            innerelement = e;
                            break;
                        }
                    }
                    uiaBaseHandler.SelectionItem(innerelement);
                    exPattern.Collapse();
                }
            }
        }
    }
}