namespace Intel.VPG.Display.Automation
{
    public class HDCPParams
    {
        public HDCPPlayerInstance HDCPPlayerInstance { get; set; }
        public string HDCPAppName { get; set; }
        public HDCPOptions HDCPOptions { get; set; }
        public HDCPApplication HDCPApplication { get; set; }
        public DisplayHierarchy DisplayHierarchy { get; set; }
        public DisplayConfig CurrentConfig { get; set; }
    }
}
