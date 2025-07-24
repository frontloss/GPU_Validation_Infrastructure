namespace Intel.VPG.Display.Automation
{
    using System;
    public class RebootDataProvider
    {
        public string jobID { get; set; }
        public string identifier { get; set; }
        public int count { get; set; }
        public DateTime osCreationTime { get; set; }
        public DateTime dateTimeInfo { get; set; }
    }
}
