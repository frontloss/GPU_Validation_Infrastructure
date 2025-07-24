namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class MP_Audio_DisplaySwitchAfter_S4 : MP_Audio_DisplaySwitchAfter_S3
    {
        public MP_Audio_DisplaySwitchAfter_S4()
        {
            powerParams.PowerStates = PowerStates.S4;
        }
    }
}
