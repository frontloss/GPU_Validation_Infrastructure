namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_PowerWell_DisplaySwitch_Advanced_All_PG_ON : SB_Config_DisplaySwitch_Advanced
    {
        public override void VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            base.VerifyConfigOS(argDisplayConfig);

            if (VerifyRegisters("PWR_WELL_CTL2_Register_ALL_ON", PIPE.NONE, PLANE.NONE, PORT.NONE, false))
                Log.Success("All PG's are ON as expected.");
            else
                Log.Fail("All PG's are not ON as expected.");

            if (VerifyRegisters("PWR_WELL_CTL_DDI2_ALL_ON", PIPE.NONE, PLANE.NONE, PORT.NONE, false))
                Log.Success("All PwrWell DDI's are ON as expected.");
            else
                Log.Fail("All PwrWell DDI's are not ON as expected.");
        }
    }
}