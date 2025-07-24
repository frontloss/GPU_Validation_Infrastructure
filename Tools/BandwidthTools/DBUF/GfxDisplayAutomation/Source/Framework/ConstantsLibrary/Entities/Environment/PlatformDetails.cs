namespace Intel.VPG.Display.Automation
{
    public class PlatformDetails
    {
        public Platform Platform { get; set; }
        public FormFactor FormFactor { get; set; }
        public bool IsLowpower
        {
            get
            {
                switch (this.Platform)
                {
                    case Platform.CHV:
                    case Platform.VLV:
                        return true;
                    default:
                        return false;
                }
            }
        }

        public bool IsGreaterThan(Automation.Platform platform)
        {
            return this.Platform >= platform;
        }
    }
}