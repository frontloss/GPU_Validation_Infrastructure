namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class SB_Overlay_S4 : SB_Overlay_S3
    {
        public SB_Overlay_S4()
            : base()
        {
            _PowerState = PowerStates.S4;
        }    
    }
}