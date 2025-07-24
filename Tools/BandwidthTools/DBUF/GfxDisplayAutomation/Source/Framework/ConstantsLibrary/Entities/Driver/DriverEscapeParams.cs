namespace Intel.VPG.Display.Automation
{
    public class DriverEscapeData<I, R>
    {
        public I input { get; set; }
        public R output { get; set; }
    }

    public class DriverEscapeParams
    {
        public DriverEscapeType driverEscapeType { get; set; }
        public object driverEscapeData{ get; set; }

        public DriverEscapeParams(DriverEscapeType EscapeType, object EscapeData)
        {
            driverEscapeType = EscapeType;
            driverEscapeData = EscapeData;
        }
    }

    public class SBRegisterData
    {
        public uint DSP_SS_PM_REG;
        public uint PUNIT_PORT_ID;
    }
}