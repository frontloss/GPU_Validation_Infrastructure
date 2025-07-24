namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_SmartFrame_Reboot : MP_SmartFrame_Base
    {
        private PowerParams _powerParams = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set config SD {0} via OS", base.GetInternalDisplay());
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.SD;
            config.PrimaryDisplay = base.GetInternalDisplay();
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, config))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Restart Machine");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Verify Smart Frame Enabled after restart");
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Restart Machine");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Verify Smart Frame Disabled after restart");
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
        }
    }
}