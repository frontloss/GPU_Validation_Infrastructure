namespace Intel.VPG.Display.Automation
{
    public class DeepColorParams
    {
        public DeepColorParams()
        {
            Bpc = 10;
        }
        public string DeepColorApplication { get; set; }

        public DeepColorAppType DeepColorAppType { get; set; }
        public DeepColorOptions DeepColorOptions { get; set; }
        public DisplayHierarchy DisplayHierarchy { get; set; }
        public DisplayConfig CurrentConfig { get; set; }
        public uint Bpc { get; set; }
    }
}
