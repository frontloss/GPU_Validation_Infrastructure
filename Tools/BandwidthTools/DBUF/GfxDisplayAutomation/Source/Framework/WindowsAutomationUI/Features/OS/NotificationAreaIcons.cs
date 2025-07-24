namespace Intel.VPG.Display.Automation
{
    using System.Windows.Automation;
    using System.Windows.Forms;

    class NotificationAreaIcons : FunctionalBase, ISetMethod
    {
        UIABaseHandler uiaBaseHandler = new UIABaseHandler();
        public bool SetMethod(object argMessage)
        {
            Log.Verbose("In Notification Area Icons (Windows Automation UI)");
            Log.Verbose("Launching Notification Area Icons Control Panel");
            CommonExtensions.StartProcess("control", " /name Microsoft.NotificationAreaIcons");
            AutomationElement element = UIABaseHandler.SelectElementClassNameControlType(AutomationElement.RootElement, "CCCheckBox", ControlType.CheckBox);
            TogglePattern pattern = element.GetCurrentPattern(TogglePattern.Pattern) as TogglePattern;
            if (pattern.Current.ToggleState == ToggleState.Off)
                SendKeys.SendWait("%A");
            System.Threading.Thread.Sleep(1000);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType(AutomationElement.RootElement, "Close", ControlType.Button));
            return true;
        }
    }
}