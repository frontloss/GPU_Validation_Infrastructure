namespace AudioEndpointVerification
{
    public class DisplayUIDMapper
    {
        uint winDowsMonID;
        public uint WinDowsMonID
        {
            get { return winDowsMonID; }
            set { winDowsMonID = value; }
        }
        uint cuiMonID;
        public uint CuiMonID
        {
            get { return cuiMonID; }
            set { cuiMonID = value; }
        }
        PORT portType;
        public PORT PortType
        {
            get { return portType; }
            set { portType = value; }
        }
    }
}
