namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    public class SB_Config_DisplaySwap : SB_Config_Base
    {
        Dictionary<int, System.Action> _displaySwap = null;
        public SB_Config_DisplaySwap()
        {
            _displaySwap = new Dictionary<int, System.Action>();
            _displaySwap.Add(1, SwapForSingleDisplay);
            _displaySwap.Add(2, SwapForDual);
            _displaySwap.Add(3, SwapForTri);
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            //if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
            //    Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
            //if (base.CurrentConfig.ConfigType == DisplayConfigType.SD)
            //    Log.Abort("Display switching cannot be applied to single display");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            base.ApplyConfigOS(base.CurrentConfig);
            _displaySwap[base.CurrentConfig.ConfigTypeCount]();
        }
        protected virtual void SwapForSingleDisplay()
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    DisplayConfig config = new DisplayConfig() 
                    {
                        ConfigType=DisplayConfigType.SD,
                        PrimaryDisplay=curDisp
                    };
                    ApplyConfigOS(config);
                    VerifyConfigOS(config);
                });
           
        }

        protected virtual void SwapForDual()
        {
            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = base.CurrentConfig.ConfigType;

            currentConfig.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            currentConfig.SecondaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigOS(currentConfig);
            VerifyConfigOS(currentConfig);

            ApplyConfigOS(base.CurrentConfig);
            VerifyConfigOS(base.CurrentConfig);
        }
        protected virtual void SwapForTri()
        {
            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = base.CurrentConfig.ConfigType;

            currentConfig.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            currentConfig.SecondaryDisplay = base.CurrentConfig.TertiaryDisplay;
            currentConfig.TertiaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigOS(currentConfig);
            VerifyConfigOS(currentConfig);

            DisplayConfig currentConfig1 = new DisplayConfig();
            currentConfig1.ConfigType = base.CurrentConfig.ConfigType;
            currentConfig1.PrimaryDisplay = base.CurrentConfig.TertiaryDisplay;
            currentConfig1.SecondaryDisplay = base.CurrentConfig.PrimaryDisplay;
            currentConfig1.TertiaryDisplay = base.CurrentConfig.SecondaryDisplay;

            ApplyConfigOS(currentConfig1);
            VerifyConfigOS(currentConfig1);

            ApplyConfigOS(base.CurrentConfig);
            VerifyConfigOS(base.CurrentConfig);
        }
    }
}
