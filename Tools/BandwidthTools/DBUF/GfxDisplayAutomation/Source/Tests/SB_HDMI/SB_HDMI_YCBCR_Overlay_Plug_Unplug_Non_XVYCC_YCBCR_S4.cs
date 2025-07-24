namespace Intel.VPG.Display.Automation
{

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HDMI_YCBCR_Overlay_Plug_Unplug_Non_XVYCC_YCBCR_S4 : SB_HDMI_YCBCR_Overlay_Plug_Unplug_Non_XVYCC_YCBCR_S3
    {
        public SB_HDMI_YCBCR_Overlay_Plug_Unplug_Non_XVYCC_YCBCR_S4()
            : base(PowerStates.S4)
        {}
    }
}
