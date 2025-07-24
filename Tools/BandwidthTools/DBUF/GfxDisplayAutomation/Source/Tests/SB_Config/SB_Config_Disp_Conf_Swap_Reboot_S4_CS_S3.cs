using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Config_Disp_Conf_Swap_Reboot_S4_CS_S3:SB_Config_Base
    {
        Dictionary<DisplayConfigType, DisplayConfigType> _SwapDisplay = new Dictionary<DisplayConfigType, DisplayConfigType>()
        {
            {DisplayConfigType.DDC,DisplayConfigType.ED},
            {DisplayConfigType.ED,DisplayConfigType.DDC},
            {DisplayConfigType.TDC,DisplayConfigType.TED},
            {DisplayConfigType.TED,DisplayConfigType.TDC},
        };
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
           
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            base.PlugDisplays();
            base.ApplyConfigOS(base.CurrentConfig);
            InvokePowerEvent(PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            InitializeHotplugFramework();
            base.PlugDisplays();
            base.ApplyConfigOS(base.CurrentConfig);
            base.VerifyConfigOS(base.CurrentConfig);
            InvokePowerEvent(PowerStates.S4);            
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            base.VerifyConfigOS(base.CurrentConfig);
            InvokePowerEvent(PowerStates.S3);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            base.VerifyConfigOS(base.CurrentConfig);
            SwapDisplay();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();
        }
        protected void SwapDisplay()
        {
            if (_SwapDisplay.Keys.Contains(base.CurrentConfig.ConfigType))
            {
                DisplayConfigType configType = _SwapDisplay[base.CurrentConfig.ConfigType];
                Log.Message("The config to be applied is {0}",configType);
                DisplayConfig config = new DisplayConfig()
                {
                    ConfigType = configType,
                    PrimaryDisplay=base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay=base.CurrentConfig.SecondaryDisplay,
                    TertiaryDisplay=base.CurrentConfig.TertiaryDisplay
                };
                base.ApplyConfigOS(config);
                InvokePowerEvent(PowerStates.S3);
                base.VerifyConfigOS(config);
            }
        }
        protected virtual void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            powerParams.Delay = 30;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }

    }
}
