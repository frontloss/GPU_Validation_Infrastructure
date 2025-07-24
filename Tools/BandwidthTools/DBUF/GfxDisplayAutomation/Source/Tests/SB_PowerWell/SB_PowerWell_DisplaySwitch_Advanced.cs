namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_PowerWell_DisplaySwitch_Advanced : SB_Config_DisplaySwitch_Advanced
    {
        public override void VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            base.VerifyConfigOS(argDisplayConfig);
            AccessInterface.GetFeature<bool>(Features.PowerWell, Action.Get);
        }
    }
}