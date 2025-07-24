namespace Intel.VPG.Display.Automation
{
    public class DisplayScaling
    {
        public DisplayType display;
        public ScalingOptions scaling;
        public uint customX;
        public uint customY;
        public DisplayScaling(DisplayType display, ScalingOptions scaling)
        {
            this.display = display;
            this.scaling = scaling;
        }
        public DisplayScaling(DisplayType display)
        {
            this.display = display;
        }

        public override string ToString()
        {
            string custom = scaling == ScalingOptions.Customize_Aspect_Ratio ? "(" + customX + "," + customY + ")" : "";
            string scalingStr = scaling + custom;
            return scalingStr;
        }

        public override bool Equals(object obj)
        {
            DisplayScaling dispScaling = obj as DisplayScaling;

            if ((this.scaling == dispScaling.scaling) && (this.customX == dispScaling.customX) && (this.customY == dispScaling.customY))
                return true;

            return false;
        }

    }
}
