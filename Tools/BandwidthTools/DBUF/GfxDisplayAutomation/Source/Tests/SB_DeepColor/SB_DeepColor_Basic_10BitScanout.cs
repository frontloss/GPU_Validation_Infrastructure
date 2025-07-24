namespace Intel.VPG.Display.Automation
{
    using System;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_Basic_10BitScanout : SB_DeepColor_Basic_FP16
    {
        public SB_DeepColor_Basic_10BitScanout()
            : base(DeepColorAppType.N10BitScanOut)
        {}

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestPreCondition()
        {
            base.TestPreCondition();
            base.InstallDirectX();
        }
    }
}