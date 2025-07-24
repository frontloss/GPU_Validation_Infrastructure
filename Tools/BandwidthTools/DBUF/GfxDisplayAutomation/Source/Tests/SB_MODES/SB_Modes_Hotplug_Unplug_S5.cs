namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Threading;
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_Modes_Hotplug_Unplug_S5 : SB_MODES_Base
    {
        PowerParams _powerParams = null;
        protected List<DisplayModeList> _ModeList = null;
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA, 4);
            Hotplug(FunctionName.PLUG, DisplayType.HDMI, DVMU_PORT.PORTA, 4);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
                base.CurrentConfig.DisplayList.ForEach(disp => CheckWatermark(disp));
            }
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            _ModeList = base.GetMinModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(_ModeList);
            PerformHotplugUnplug();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            PerformTestAfterS5();
            _ModeList = base.GetMinModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            VerifyMode(_ModeList);
            _ModeList = base.GetMaxModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(_ModeList);
            PerformHotplugUnplug();
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            PerformTestAfterS5();
            _ModeList = base.GetMaxModeForConfig(base.CurrentConfig.DisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            VerifyMode(_ModeList);
        }

        protected void PerformTestAfterS5()
        {
            Hotplug(FunctionName.OPEN, DisplayType.HDMI, DVMU_PORT.PORTA, 4);
        }

        protected virtual void PerformHotplugUnplug()
        {
            Log.Message(true, "Performing unplug of HDMI and will be plugged back in S5");
            Hotplug(FunctionName.UNPLUG, DisplayType.HDMI, DVMU_PORT.PORTA, 4);
            Thread.Sleep(5000);
            Hotplug(FunctionName.PLUG, DisplayType.HDMI, DVMU_PORT.PORTA, 20);
            this.InvokePowerEvent(PowerStates.S5);
            base.CurrentConfig.DisplayList.ForEach(disp => CheckWatermark(disp));
        }
        protected void Hotplug(FunctionName FuncArg, DisplayType DisTypeArg, DVMU_PORT PortArg, short argDelay)
        {
            HotPlugUnplug obj = new HotPlugUnplug(FuncArg, DisTypeArg, PortArg);
            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, obj);
        }
        private void InvokePowerEvent(PowerStates State)
        {
            Log.Message(true, "Invoking power event S5");
            this._powerParams = new PowerParams() { Delay = 30 };
            _powerParams.PowerStates = State;
            _powerParams.Delay = 30;
            base.EventResult(_powerParams.PowerStates, base.InvokePowerEvent(_powerParams, _powerParams.PowerStates));
        }
        protected virtual void ApplyMode(List<DisplayModeList> argDispModeList)
        {
            argDispModeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    base.ApplyModeOS(curMode, curMode.display);
                    //CheckWatermark(curMode.display);
                });
            });
        }
        protected virtual void VerifyMode(List<DisplayModeList> argDispModeList)
        {
            argDispModeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    base.VerifyModeOS(curMode, curMode.display);
                });
            });
        }
    }
}
