namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Windows.Automation;
    using System;

    public class AppBar : FunctionalBase, ISetMethod, IEnabledMethod
    {
        private Dictionary<AppBarOptions, AutomationElement> _buttonList = new Dictionary<AppBarOptions, AutomationElement>();
        private AutomationElement element, buttonElement = null;
        public AutomationElementCollection elementColn = null;
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();
        AutomationElement appBarElement;

        public AppBar()
        {
            Log.Verbose("In AppBar (Windows Automation UI)");
            element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.AppBar].AutomationId, ControlType.Custom);
            elementColn = element.FindAll(TreeScope.Descendants, new PropertyCondition(AutomationElement.ClassNameProperty, "AppBarButton"));
            foreach (AutomationElement e in elementColn)
            {
                buttonElement = TreeWalker.ControlViewWalker.GetFirstChild(e);
                AppBarOptions appBarOptions;
                if (Enum.TryParse( buttonElement.Current.Name.Replace(" ", ""), out appBarOptions))
                    _buttonList.Add(appBarOptions, buttonElement);
            }
        }
        public bool EnabledMethod(object argMessage)
        {
            return this._buttonList[(AppBarOptions)argMessage].Current.IsEnabled;
        }
        public bool SetMethod(object argMessage)
        {
            AppBarOptions option = (AppBarOptions)argMessage;
            if (this._buttonList.ContainsKey((AppBarOptions)argMessage) && this._buttonList[(AppBarOptions)argMessage].Current.IsEnabled)
            {
                appBarElement = this._buttonList[option];
                
                UIABaseHandler.InvokeElement(appBarElement);
              // System.Threading.Thread.Sleep(100);
               return true;
            }
            return false;
        }
    }
}