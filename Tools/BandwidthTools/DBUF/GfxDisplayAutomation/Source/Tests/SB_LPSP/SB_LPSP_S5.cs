namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class SB_LPSP_S5 : SB_LPSP_S3
    {        
        public SB_LPSP_S5() 
        {            
            _PowerState = PowerStates.S5;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            ApplyNativeMode();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {            
            Log.Message(true, "Power Event {0}", _PowerState);
            _PowerEvent();
         
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Verfiy LPSP Register");
            LPSPRegisterVerify(true);

        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            ApplyNonNativeMode();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5() 
        {
            Log.Message(true, "Power Event {0}", _PowerState);
            _PowerEvent();
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6() 
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (base.CurrentConfig.GetCurrentConfigStr().Equals(currentConfig.GetCurrentConfigStr()))
                Log.Success("Expcted {0} is retained", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Expected: {0} , Current {1}",base.CurrentConfig.GetCurrentConfigStr() , currentConfig.GetCurrentConfigStr());

            Log.Message(true, "Verfiy LPSP Register");
            LPSPRegisterVerify();
        }
    }
}