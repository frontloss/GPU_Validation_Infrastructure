namespace Intel.VPG.Display.Automation
{
    public class PowerParams
    {
        public PowerStates PowerStates { get; set; }
        public RebootReason rebootReason { get; set; }
        public int Delay { get; set; }
        public PowerParams()
        {
            this.Delay = 30;
        }
    }
    public class MonitorTurnOffParam
    {
        public int waitingTime { get; set; }
        public MonitorOnOff onOffParam { get; set; }
        public MonitorTurnOffParam()
        {
            this.waitingTime = 30;
        }
    }
}