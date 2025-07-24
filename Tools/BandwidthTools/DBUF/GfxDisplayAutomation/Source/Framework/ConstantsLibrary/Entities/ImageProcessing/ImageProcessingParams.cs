namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class PixelColorInfo
    {
        public int Red;
        public int Green;
        public int Blue;
        public int Alpha;
    }
    public class ImageProcessingParams
    {
        public string SourceImage { get; set; }
        public string TargetImage { get; set; }
        public ImageProcessOptions ImageProcessingOption { get; set; }

        public pointApi pixelPosition { get; set; }
        public PixelColorInfo pixelColorInfo { get; set; }
        
    }
}
