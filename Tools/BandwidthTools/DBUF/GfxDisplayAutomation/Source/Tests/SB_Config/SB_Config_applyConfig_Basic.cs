namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    public class SB_Config_applyConfig_Basic : SB_Config_Base
    {
        protected List<DisplayConfig> _dispSwitchOrder = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount() != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount(), base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig sdConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            if (base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount() == 3)
            {
                DisplayConfig tdcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                DisplayConfig tedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                _dispSwitchOrder = new List<DisplayConfig>() { sdConfig, ddcConfig, edConfig, tdcConfig, tedConfig, sdConfig };
            }
            else
            {
                _dispSwitchOrder = new List<DisplayConfig>() { sdConfig, ddcConfig, edConfig, sdConfig };
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
                _dispSwitchOrder.ForEach(curConfig =>
                {
                    ApplyConfigOS(curConfig);
                    VerifyConfigOS(curConfig);
                });
        }
    }
}
