namespace Intel.VPG.Display.Automation
{
    using System;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_CS_DPApplet : SB_DeepColor_S3_DPApplet
    {
        public SB_DeepColor_CS_DPApplet()
            : base(PowerStates.CS)
        {} 
    }
}