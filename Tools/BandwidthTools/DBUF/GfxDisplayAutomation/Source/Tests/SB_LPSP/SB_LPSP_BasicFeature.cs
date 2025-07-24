namespace Intel.VPG.Display.Automation
{
    class SB_LPSP_BasicFeature : SB_LPSP_Base
    {                
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            ApplyNativeMode();            
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Verify LPSP Registers");
            LPSPRegisterVerify(true);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3() 
        {
            ApplyNonNativeMode();            
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Verify LPSP Registers");
            LPSPRegisterVerify();
        }
    } 
}