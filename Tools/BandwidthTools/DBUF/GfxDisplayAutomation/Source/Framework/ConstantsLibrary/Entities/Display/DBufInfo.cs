namespace Intel.VPG.Display.Automation
{
    public class DBufInfo
    {
        public uint DisplaySurfaceWidth { get; set; }
        public bool Enabled { get; set; }
        public uint DbufAllocated { get; set; }
        public string SourcePixelFormat { get; set; }
        public TileFormat TileFormat { get; set; }
        public string RotationAngle { get; set; }
        public uint PlaneBufCFGTotalBlock { get; set; }
        public bool HWCursorEnable { get; set; }
        public bool OverlayEnable { get; set; }
        public string CursorMode { get; set; }
        public uint CursorBufTotalBlock { get; set; }
        public bool NVBuf { get; set; }
    }
}
