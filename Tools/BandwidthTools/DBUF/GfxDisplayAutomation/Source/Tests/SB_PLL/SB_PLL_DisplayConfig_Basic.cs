namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_PLL_DisplayConfig_Basic : SB_PLL_Base_Chv
    {
        protected List<DisplayConfig> _displayConfigSequence = null;
        protected Dictionary<int, System.Action> _dispCountConfigMap = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            _displayConfigSequence = new List<DisplayConfig>() { new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay } };
            _dispCountConfigMap = new Dictionary<int, System.Action>() { { 2, AddDualConfig }, { 3, AddTriConfig } };

            if (base.CurrentConfig.DisplayList.Count() < 2)
                Log.Abort("Display Config test requires atleast 2 displays, current display count: {0}", base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            _dispCountConfigMap[base.CurrentConfig.DisplayList.Count()]();

            _displayConfigSequence.ForEach(curConfig =>
            {
                base.ApplyConfig(curConfig);
                base.VerifyPLLRegister(curConfig);
            });

        }
        protected void AddDualConfig()
        {
            _displayConfigSequence.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            _displayConfigSequence.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
        }
        protected void AddTriConfig()
        {
            AddDualConfig();
            _displayConfigSequence.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            _displayConfigSequence.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
        }
    }
}
