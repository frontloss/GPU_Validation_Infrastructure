namespace Intel.VPG.Display.Automation
{
    public class SelectDisplayInfo : SelectDisplay
    {

        public SelectDisplayInfo()
            : base(DisplayInfoRepo.Instance.IntelRGraphics.ComboInfo) { }

        public override object Get
        {
            get
            {
                ConnectorType info = new ConnectorType();
                info.connectorType = OptionalDisplayInfoRepo.Instance.IntelRGraphicsControlPanel.ConnectorType.TextValue;
                info.deviceType = OptionalDisplayInfoRepo.Instance.IntelRGraphicsControlPanel.DeviceType.TextValue;
                return info;
            }
        }
    }
}
