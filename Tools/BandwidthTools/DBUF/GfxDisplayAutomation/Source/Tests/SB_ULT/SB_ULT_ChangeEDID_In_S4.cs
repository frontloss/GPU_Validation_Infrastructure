namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_ULT_ChangeEDID_In_S4 : SB_ULT_ChangeEDID_In_S3
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            InvokePowerEvent(PowerStates.S4);
        }
    }
}
