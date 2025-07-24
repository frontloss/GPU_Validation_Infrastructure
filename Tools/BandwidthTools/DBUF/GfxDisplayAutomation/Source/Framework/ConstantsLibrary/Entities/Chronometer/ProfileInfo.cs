namespace Intel.VPG.Display.Automation
{
    public class ProfileInfo
    {
        public string EventName;
        public double benchMarkValue;
    }

    public class ChronometerResult
    {
        public bool chronometerStatus;
        public int cycle;
        public string EventName;
        public double benchMarkValue;
        public double actualValue;
        public string DDI_Name;
        public int noOfTimesCalled;
        public int totalDDIExecutionTime;
        public string status;
    }
}
