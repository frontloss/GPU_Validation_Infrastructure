using System.Collections.Generic;
namespace Intel.VPG.Display.Automation
{
    class SB_CDClock_DisplaySwitch_Advanced : SB_CDClock_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPrerequisite()
        {
            if (base.CurrentConfig.ConfigType == DisplayConfigType.SD)
                Log.Abort("This test not applicable for {0}", base.CurrentConfig.GetCurrentConfigStr());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            List<DisplayConfig> allConfigs = GetAllPossibleConfigForSwitch();
            foreach(DisplayConfig config in allConfigs)
            {
                base.ApplyConfig(config);
                base.VerifyCDClockRegisters();
            }
        }

        private List<DisplayConfig> GetAllPossibleConfigForSwitch()
        {
            List<DisplayConfig> dispSwitchOrder = null;

            DisplayConfig dispSwitch1 = base.CurrentConfig;
            DisplayConfig dispSwitch2 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay};
            DisplayConfig dispSwitch3 = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch4 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig dispSwitch5 = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            
            dispSwitchOrder = new List<DisplayConfig>() {dispSwitch1, dispSwitch2, dispSwitch3, dispSwitch4, dispSwitch5};

            if(base.CurrentConfig.ConfigType == DisplayConfigType.TDC || base.CurrentConfig.ConfigType == DisplayConfigType.TED)
            {
                DisplayConfig dispSwitch6 = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                DisplayConfig dispSwitch7 = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay };
                DisplayConfig dispSwitch8 = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };

                dispSwitchOrder.Add(dispSwitch6);
                dispSwitchOrder.Add(dispSwitch7);
                dispSwitchOrder.Add(dispSwitch8);
            }

            return dispSwitchOrder;
        }
    }
}
