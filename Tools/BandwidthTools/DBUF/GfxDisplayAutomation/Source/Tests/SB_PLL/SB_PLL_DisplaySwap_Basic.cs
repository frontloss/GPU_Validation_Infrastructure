namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_PLL_DisplaySwap_Basic : SB_PLL_Base_Chv
    {
        protected Dictionary<int, System.Action> _dispSwapMap = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            _dispSwapMap = new Dictionary<int, System.Action>() { { 2, SwapDualDispaly }, { 3, SwapTriDisplay } };

            if (base.CurrentConfig.DisplayList.Count() < 2)
                Log.Abort("Display Config test requires atleast 2 displays, current display count: {0}", base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            ApplyConfig(base.CurrentConfig);
            _dispSwapMap[base.CurrentConfig.DisplayList.Count()]();
        }
        protected void SwapDualDispaly()
        {
            DisplayConfig config = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfig(config);
            base.VerifyPLLRegister(config);

            base.ApplyConfig(base.CurrentConfig);
            base.VerifyPLLRegister(base.CurrentConfig);
        }
        protected void SwapTriDisplay()
        {
            DisplayConfig config = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfig(config);
            base.VerifyPLLRegister(config);

            config = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            base.ApplyConfig(config);
            base.VerifyPLLRegister(config);

            base.ApplyConfig(base.CurrentConfig);
            base.VerifyPLLRegister(base.CurrentConfig);
        }
    }
}
