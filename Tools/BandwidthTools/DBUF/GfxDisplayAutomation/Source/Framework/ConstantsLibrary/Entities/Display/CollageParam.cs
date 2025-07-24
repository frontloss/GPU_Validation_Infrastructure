namespace Intel.VPG.Display.Automation
{
    public class CollageParam
    {
        public CollageOption option;
        public DisplayConfig config;
        public bool isCollageSupported;
        public CollageParam()
        {
            config = new DisplayConfig();
        }
    }
}
