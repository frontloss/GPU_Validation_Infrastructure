namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_LPSP_DisplayConfig : SB_LPSP_Base
    {
        [Test(Type = TestType.Method, Order = 0)]
        public override void TestStep0()
        {
            if (!CurrentConfig.CustomDisplayList.Contains(DisplayType.EDP))
                Log.Abort("EDP must be connected to run the Test");

            if (CurrentConfig.ConfigType == DisplayConfigType.SD)
                Log.Abort("SD Mode not Supported for this Test");

            Log.Message("Config to be applied : {0}", CurrentConfig.GetCurrentConfigStr());

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, CurrentConfig))
                Log.Success("Config Applied Successfully");
            else
                Log.Abort("Fail to apply Config");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig))
                Log.Success("Config SET : SD - EDP");
            else
                Log.Fail("Failed to set Config : SD - EDP");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            ApplyNonNativeMode();            
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Verify LPSP Registers");
           // LPSPRegisterVerify(false);
            LPSPRegisterVerify();
        }      

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            ApplyNativeMode();            
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Verify LPSP Registers");
            LPSPRegisterVerify(true);
           // LPSPRegisterVerify();
        }

    }
}