namespace Intel.VPG.Display.Automation
{
    using System.Windows.Forms;
    using System.Collections.Generic;
    using System.Threading;
    using System.Linq;
    using System;

    [Test(Type = TestType.HasReboot)]
    class MP_SwitchableGraphics_Lid_Switch : MP_SwitchableGraphics_Base
    {
        private LidSwitchParams _lidSwitchParams = null;
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            //HotPlugUnplug _HotPlugUnplug = new HotPlugUnplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA);
            //bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, _HotPlugUnplug);
            Log.Message(true, "Set config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Set Do-Nothing on Lid switch and Restart the system");
            if (AccessInterface.SetFeature<bool, LidSwitchAction>(Features.LidSwitch, Action.SetMethod, LidSwitchAction.DoNothing))
                base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
            else
                Log.Fail("Unable to set Lid Switch Action to Do-Nothing");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Close the lid and Do-nothing for 20 secs");
            _lidSwitchParams = new LidSwitchParams() { LidSwitchAction = LidSwitchAction.DoNothing, Delay = 20 };
            AccessInterface.SetFeature<LidSwitchParams>(Features.LidSwitch, Action.Set, _lidSwitchParams);
            if (this.VerifyEDPNotEnumerated())
                Log.Success("EDP not enumerated");
            else
                Log.Fail("EDP still enumerated, lid switch failed");
            Thread.Sleep(20000);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Set Sleep on Lid switch and Restart the system");
            if (AccessInterface.SetFeature<bool, LidSwitchAction>(Features.LidSwitch, Action.SetMethod, LidSwitchAction.Sleep))
                base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
            else
                Log.Fail("Unable to set Lid Switch Action to Sleep");
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Close the lid and Sleep for 20 secs");
            _lidSwitchParams = new LidSwitchParams() { LidSwitchAction = LidSwitchAction.Sleep, Delay = 20 };
            AccessInterface.SetFeature<LidSwitchParams>(Features.LidSwitch, Action.Set, _lidSwitchParams);
            Thread.Sleep(20000);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Set Hibernate on Lid switch and Restart the system");
            if (AccessInterface.SetFeature<bool, LidSwitchAction>(Features.LidSwitch, Action.SetMethod, LidSwitchAction.Hibernate))
                base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
            else
                Log.Fail("Unable to set Lid Switch Action to Hibernate");
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Close the lid and goto Hibernate for 20 secs");
            _lidSwitchParams = new LidSwitchParams() { LidSwitchAction = LidSwitchAction.Hibernate, Delay = 20 };
            AccessInterface.SetFeature<LidSwitchParams>(Features.LidSwitch, Action.Set, _lidSwitchParams);
            Thread.Sleep(20000);
        }
        private bool VerifyEDPNotEnumerated()
        {
            List<DisplayInfo> enumeratedDisplay = AccessInterface.SetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            return (enumeratedDisplay.Where(dI => dI.DisplayType == DisplayType.EDP).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None);
        }
    }
}