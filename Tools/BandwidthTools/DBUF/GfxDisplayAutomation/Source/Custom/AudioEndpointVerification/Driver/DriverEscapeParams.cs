namespace AudioEndpointVerification
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
}