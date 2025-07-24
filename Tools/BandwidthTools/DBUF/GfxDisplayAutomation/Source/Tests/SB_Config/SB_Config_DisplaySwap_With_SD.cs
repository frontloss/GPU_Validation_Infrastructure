namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_Config_DisplaySwap_With_SD : SB_Config_DisplaySwap
    {
        protected override void SwapForDual()
        {
            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = base.CurrentConfig.ConfigType;

            currentConfig.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            currentConfig.SecondaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigOS(currentConfig);
            VerifyConfigOS(currentConfig);

            //SD- Primary Display
            DisplayConfig sdConfig = new DisplayConfig();
            sdConfig.ConfigType = DisplayConfigType.SD;
            sdConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigOS(sdConfig);
            VerifyConfigOS(sdConfig);

            //SD- Secondary Display
            DisplayConfig sdConfig2 = new DisplayConfig();
            sdConfig2.ConfigType = DisplayConfigType.SD;
            sdConfig2.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            ApplyConfigOS(sdConfig2);
            VerifyConfigOS(sdConfig2);


            ApplyConfigOS(base.CurrentConfig);
            VerifyConfigOS(base.CurrentConfig);
        }
        protected override void SwapForTri()
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

            //SD- Primary Display
            DisplayConfig sdConfig = new DisplayConfig();
            sdConfig.ConfigType = DisplayConfigType.SD;
            sdConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigOS(sdConfig);
            VerifyConfigOS(sdConfig);

            //SD- Secondary Display
            DisplayConfig sdConfig2 = new DisplayConfig();
            sdConfig2.ConfigType = DisplayConfigType.SD;
            sdConfig2.PrimaryDisplay = base.CurrentConfig.SecondaryDisplay;
            ApplyConfigOS(sdConfig2);
            VerifyConfigOS(sdConfig2);


            ApplyConfigOS(base.CurrentConfig);
            VerifyConfigOS(base.CurrentConfig);
        }
    }
}
