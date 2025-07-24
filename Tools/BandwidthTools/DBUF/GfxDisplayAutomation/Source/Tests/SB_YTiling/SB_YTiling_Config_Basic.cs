namespace Intel.VPG.Display.Automation
{
    class SB_YTiling_Config_Basic:SB_YTiling_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.ApplyConfigVerifyRegister(base.CurrentConfig);
        }
    }
}
