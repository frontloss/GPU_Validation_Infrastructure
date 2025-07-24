namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;

    class SB_EDP_LinkRate_7 : SB_EDP_LR_LC_All
    {
        public SB_EDP_LinkRate_7()
        {
            Link_Rate = UI_Link_Rate.UI_Rate_7;
            FilterConfigurationsByLinkRate();
        }
    }
}
