namespace Intel.VPG.Display.Automation
{
    using System;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_Basic_DPApplet : SB_DeepColor_Basic_FP16
    {
        public SB_DeepColor_Basic_DPApplet()
            : base(DeepColorAppType.DPApplet)
        {}

    }
}