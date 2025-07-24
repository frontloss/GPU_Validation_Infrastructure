namespace Intel.VPG.Display.Automation
{
    public class OverlayParams
    {
        private string _videoFile = "Wildlife.wmv";

        public string Player { get; set; }
        public string VideoFile 
        {
            get { return this._videoFile; }
            set { this._videoFile = value; }
        }
        public OverlayPlaybackOptions PlaybackOptions { get; set; }
        public DisplayHierarchy DisplayHierarchy { get; set; }
        public DisplayConfig CurrentConfig { get; set; }
        public ColorFormat colorFormat { get; set; }
        public OverlayApp overlayApp { get; set; }
    }
}
