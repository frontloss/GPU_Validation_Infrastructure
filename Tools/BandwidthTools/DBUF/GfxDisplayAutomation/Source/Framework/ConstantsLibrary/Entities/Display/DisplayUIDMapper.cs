namespace Intel.VPG.Display.Automation
{
    public class DisplayUIDMapper
    {
        uint windowsID;
        public uint WindowsID
        {
            get { return windowsID; }
            set { windowsID = value; }
        }
        uint cuiID;
        public uint CuiID
        {
            get { return cuiID; }
            set { cuiID = value; }
        }
        PORT portType;
        public PORT PortType
        {
            get { return portType; }
            set { portType = value; }
        }
    }
}
