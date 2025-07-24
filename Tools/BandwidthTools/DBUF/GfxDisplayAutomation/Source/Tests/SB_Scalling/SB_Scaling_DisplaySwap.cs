using System.Collections.Generic;
namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_DisplaySwap : SB_Scaling_DisplayConfig
    {
        Dictionary<DisplayConfigType, System.Action> _peformSwap = null;
        List<DisplayConfig> _configList = null;
        public SB_Scaling_DisplaySwap()
        {
            _peformSwap = new Dictionary<DisplayConfigType, System.Action>();
            _peformSwap.Add(DisplayConfigType.SD, SwapForSingle);
            _peformSwap.Add(DisplayConfigType.DDC, SwapForDual);
            _peformSwap.Add(DisplayConfigType.ED, SwapForDual);
            _peformSwap.Add(DisplayConfigType.TDC, SwapForTri);
            _peformSwap.Add(DisplayConfigType.TED, SwapForTri);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            // For DDC and TDC Mode only first time Mode will be applied
            bool applyMode = base.CurrentConfig.ConfigType == DisplayConfigType.DDC || base.CurrentConfig.ConfigType == DisplayConfigType.TDC ? false : true;
            _peformSwap[base.CurrentConfig.ConfigType]();

            _configList.ForEach(curConfig =>
                {
                    if (ApplyConfigOS(curConfig))
                    {
                        Log.Message(true, "Apply and Verify Scaling for Display - {0}", curConfig.PrimaryDisplay);
                        ApplyAndVerifyScalling(curConfig.PrimaryDisplay, true);

                        if (curConfig.CustomDisplayList.Count >= 2)
                        {
                            Log.Message(true, "Apply and Verify Scaling for Display - {0}", curConfig.SecondaryDisplay);
                            ApplyAndVerifyScalling(curConfig.SecondaryDisplay, applyMode);
                        }

                        if (curConfig.CustomDisplayList.Count == 3)
                        {
                            Log.Message(true, "Apply and Verify Scaling for Display - {0}", curConfig.TertiaryDisplay);
                            ApplyAndVerifyScalling(curConfig.TertiaryDisplay, applyMode);
                        }
                    }
                });            
        }
        protected void SwapForSingle()
        {
            _configList = new List<DisplayConfig>();

            base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    DisplayConfig config = new DisplayConfig()
                    {
                        ConfigType = base.CurrentConfig.ConfigType,
                        PrimaryDisplay = curDisp
                    };
                    _configList.Add(config);
                });
        }
        protected void SwapForDual()
        {
            _configList = new List<DisplayConfig>();
            DisplayConfig currentConfig = new DisplayConfig()
            {
                ConfigType = base.CurrentConfig.ConfigType,
                PrimaryDisplay = base.CurrentConfig.SecondaryDisplay,
                SecondaryDisplay = base.CurrentConfig.PrimaryDisplay
            };
            _configList.Add(currentConfig);
            _configList.Add(base.CurrentConfig);
        }
        protected void SwapForTri()
        {
            _configList = new List<DisplayConfig>();
            DisplayConfig currentConfig = new DisplayConfig()
            {
                ConfigType = base.CurrentConfig.ConfigType,
                PrimaryDisplay = base.CurrentConfig.SecondaryDisplay,
                SecondaryDisplay = base.CurrentConfig.TertiaryDisplay,
                TertiaryDisplay = base.CurrentConfig.PrimaryDisplay
            };
            _configList.Add(currentConfig);

            DisplayConfig currentConfig1 = new DisplayConfig()
            {
                ConfigType = base.CurrentConfig.ConfigType,
                PrimaryDisplay = base.CurrentConfig.TertiaryDisplay,
                SecondaryDisplay = base.CurrentConfig.PrimaryDisplay,
                TertiaryDisplay = base.CurrentConfig.SecondaryDisplay
            };
            _configList.Add(currentConfig1);
            _configList.Add(base.CurrentConfig);
        }
    }
}
