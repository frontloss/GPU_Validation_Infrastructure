using System.IO;
namespace Intel.VPG.Display.Automation
{
    public class HotPlugUnplug
    {
        public const short DEFAULT_DELAY = 2;

        private string edidFilePath;
        private string dpcdFilePath;
        public HotPlugUnplug()
        {
            this.Port = DVMU_PORT.None;
        }
        public HotPlugUnplug(FunctionName argFuncName, DisplayType dispType, DVMU_PORT argPort)
            : this(argFuncName, argPort,  "HDMI_DELL.EDID")
        {

        }
        public HotPlugUnplug(FunctionName argFuncName, DVMU_PORT argPort, string argEdid, short delay = DEFAULT_DELAY)
            : this()
        {
            this.FunctionName = argFuncName;
            this.Port = argPort;
            this.EdidFilePath = argEdid ;
            this.Delay = delay;
        }
        public HotPlugStates HotPlugStates { get; set; }
        public FunctionName FunctionName { get; set; }
        public string EdidFilePath 
        {
            get { return edidFilePath; }
            set { edidFilePath = string.Concat(Directory.GetCurrentDirectory(), @"\EDIDFiles\", value); } 
        }
        public string DpcdFilePath
        {
            get { return dpcdFilePath; }
            set { dpcdFilePath = value == "" ? "" : string.Concat(Directory.GetCurrentDirectory(), @"\EDIDFiles\", value); }
        }
        public DVMU_PORT Port { get; set; }
        public short Delay { get; set; }
        public string FrameFileName { get; set; }
        public bool SkipDisplayEnumeration { get; set; }

        public bool InLowPowerState { get; set; }
        public DisplayType display { get; set; }
        public bool UseWindowsMonitorID { get; set; }
        public uint WindowsMonitorID { get; set; }
        public HotPlugUnplug(FunctionName argFuncName, DisplayType display, string argEdid, bool lowPower = false)
            : this()
        {
            this.display = display;
            this.FunctionName = argFuncName;
            this.EdidFilePath = argEdid;
            this.InLowPowerState = lowPower;
        }
        public HotPlugUnplug(FunctionName argFuncName, DisplayType display, bool useWindowsMonitorID, uint windowsMonitorID, string argEdid, bool lowPower = false, string argDpcd = "")
            : this()
        {
            this.display = display;
            this.UseWindowsMonitorID = useWindowsMonitorID;
            this.WindowsMonitorID = windowsMonitorID;
            this.FunctionName = argFuncName;
            this.EdidFilePath = argEdid;
            this.DpcdFilePath = argDpcd;
            this.InLowPowerState = lowPower;
        }

        public bool Status { get; set; }
        public HotPlugUnplug(FunctionName argFuncName, bool status)
            : this()
        {
            this.FunctionName = argFuncName;
            this.Status = status;
        }
    }
}
