namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    public class SB_modes_DisplaySwap_Basic : SB_Modes_ApplyModes_Basic
    {
        protected Dictionary<int, System.Action> _swapDisplays = null;
        protected List<DisplayModeList> _modeList = null;
        public SB_modes_DisplaySwap_Basic()
        {
            _swapDisplays = new Dictionary<int, System.Action>();
            _swapDisplays.Add(2, PerformSwapForDual);
            _swapDisplays.Add(3, PerformSwapForTri);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            _modeList = new List<DisplayModeList>();
            _modeList = base.GetMinModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(_modeList);            
            //VerifyMode(_modeList);
            _modeList = base.GetMaxModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(_modeList);
            //VerifyMode(_modeList);
        }
        protected override void ApplyMode(List<DisplayModeList> argDispModeList)
        {
            base.ApplyMode(argDispModeList);
            _swapDisplays[base.CurrentConfig.ConfigTypeCount]();
        }
        protected void PerformSwapForDual()
        {
            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = base.CurrentConfig.ConfigType;

            currentConfig.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            currentConfig.SecondaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigCUI(currentConfig);

            //VerifyMode(_modeList);

            ApplyConfigCUI(base.CurrentConfig);
        }
        protected void PerformSwapForTri()
        {
            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = base.CurrentConfig.ConfigType;

            currentConfig.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            currentConfig.SecondaryDisplay = base.CurrentConfig.TertiaryDisplay;
            currentConfig.TertiaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigCUI(currentConfig);
            //VerifyMode(_modeList);

            DisplayConfig currentConfig1 = new DisplayConfig();
            currentConfig1.ConfigType = base.CurrentConfig.ConfigType;
            currentConfig1.PrimaryDisplay = base.CurrentConfig.TertiaryDisplay;
            currentConfig1.SecondaryDisplay = base.CurrentConfig.PrimaryDisplay;
            currentConfig1.TertiaryDisplay = base.CurrentConfig.SecondaryDisplay;

            ApplyConfigCUI(currentConfig1);
            //VerifyMode(_modeList);
            ApplyConfigCUI(base.CurrentConfig);
        }
    }
}
