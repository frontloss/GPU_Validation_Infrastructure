 namespace Intel.VPG.Display.Automation
{
    using System.Windows.Automation;

    public class SelectDisplayInfo : SelectDisplay
    {

        public SelectDisplayInfo()
            : base(
            UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, UIExtensions.FeaturesDictionary[Features.SelectDisplayInfo].AutomationId, ControlType.ComboBox)
            ) { }

        public override object Get
        {
            get
            {
                Log.Verbose("In SelectDisplayInfo Get (Windows Automation UI)");
                ConnectorType info = new ConnectorType();
                info.connectorType = UIABaseHandler.SelectElementAutomationIdControlType(UIExtensions.FeaturesDictionary[Features.ConnectorType].AutomationId, ControlType.Text).Current.Name;
                info.deviceType = UIABaseHandler.SelectElementAutomationIdControlType(UIExtensions.FeaturesDictionary[Features.DeviceType].AutomationId, ControlType.Text).Current.Name;
                return info;
            }
        }
    }
}
