namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Xml;

    public class CSParam
    {
        public PowerStates PowerStates { get; set; }
        public int Delay { get; set; }
        public int Cycle { get; set; }
        public CPU_C_STATE cState { get; set; }
        public CSVerificationTool VerificationTool { get; set; }
        public string Command { get; set; }
        public CSParam()
        {
            PowerStates = PowerStates.CS;
            Cycle = 10;
            Delay = 45;
            Command = string.Empty;
        }
    }
}