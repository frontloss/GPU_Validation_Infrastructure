namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class SB_PND_Max_Fifo_DisplaySwap : SB_PND_Base
    {
        private const string PND_Max_FIFO_ENABLE = "PND_Max_FIFO_ENABLE";
        protected List<DisplayConfig> _dispSwitchOrder = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            DisplayConfig sdConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig sdConfigSecondary = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig ddcConfigSwap = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            DisplayConfig edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig edConfigSwap = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };

            if (base.CurrentConfig.DisplayList.Count == 2)
            {
                _dispSwitchOrder = new List<DisplayConfig>() { sdConfig, ddcConfig,sdConfigSecondary,ddcConfigSwap,
                    sdConfigSecondary, edConfig,sdConfig,edConfigSwap};
            }
            else if (base.CurrentConfig.DisplayList.Count == 3)
            {
                DisplayConfig sdConfigThird = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay };
                DisplayConfig tdcConfig312 = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
                DisplayConfig tdcConfig213 = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                DisplayConfig tdcConfig132 = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
                DisplayConfig tedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                DisplayConfig tedConfig231 = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
                DisplayConfig tedConfig312 = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
                _dispSwitchOrder = new List<DisplayConfig>() { sdConfig, ddcConfig, sdConfigSecondary, ddcConfigSwap, sdConfigSecondary,
                    edConfig, sdConfig, edConfigSwap,sdConfigThird, tdcConfig312, sdConfigSecondary, tdcConfig213, sdConfig,tdcConfig132, 
                    sdConfigSecondary, tedConfig,sdConfig,tedConfig231,sdConfigThird, tedConfig312, sdConfig};
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
                TestMaxFifo(curConfig);
            });
        }

       
    }
}
