namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class MP_TDR_Basic : MP_TDR_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.RunTDRNVerify(true);
        }
    }
}