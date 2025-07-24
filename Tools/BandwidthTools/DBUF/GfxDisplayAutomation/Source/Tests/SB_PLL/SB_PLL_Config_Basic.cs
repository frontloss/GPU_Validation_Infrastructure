namespace Intel.VPG.Display.Automation
{
    class SB_PLL_Config_Basic : SB_PLL_Base_Chv
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.ApplyConfig(base.CurrentConfig);
            base.VerifyPLLRegister(base.CurrentConfig);
        }
    }
}
