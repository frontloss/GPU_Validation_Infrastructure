namespace Intel.VPG.Display.Automation
{
    internal class EnableDriver : DisableDriver
    {
        public EnableDriver()
            : base("enable =", 10000)
        { }
    }
}