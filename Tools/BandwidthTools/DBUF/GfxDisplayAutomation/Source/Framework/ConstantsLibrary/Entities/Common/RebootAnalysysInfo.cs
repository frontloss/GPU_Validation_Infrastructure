namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    public class RebootAnalysysInfo
    {
        public int currentMethodIdx { get; set; }
        public string identifier { get; set; }
        public bool IsBasicDisplayAdapter { get; set; }
        public DateTime dateTimeInfo { get; set; }
        public string path { get; set; }
        public string jobID { get; set; }
        public string rebootJobID { get; set; }
        public RebootReason rebootReason { get; set; }
        public bool retryThroughReboot { get; set; }
        public List<DisplayType> pluggedDisplayList { get; set; }
    }
}
