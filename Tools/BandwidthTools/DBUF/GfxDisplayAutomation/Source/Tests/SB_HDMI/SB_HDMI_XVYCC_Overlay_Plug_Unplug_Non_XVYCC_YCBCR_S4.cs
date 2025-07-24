namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Xml.Linq;
    using System.IO;
    using System.Text;
    using System;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HDMI_XVYCC_Overlay_Plug_Unplug_Non_XVYCC_YCBCR_S4 : SB_HDMI_XVYCC_Overlay_Plug_Unplug_Non_XVYCC_YCBCR_S3
    {
        public SB_HDMI_XVYCC_Overlay_Plug_Unplug_Non_XVYCC_YCBCR_S4()
            : base(PowerStates.S4)
        {}
    }
}
