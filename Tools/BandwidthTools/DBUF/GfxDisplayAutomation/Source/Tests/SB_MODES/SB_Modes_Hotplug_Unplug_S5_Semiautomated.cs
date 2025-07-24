namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_Modes_Hotplug_Unplug_S5_Semiautomated:SB_Modes_Hotplug_Unplug_S5
    {
        protected override void PerformHotplugUnplug()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            List<DisplayType> semiAutomatedPlugUnplugDisplays = currentConfig.CustomDisplayList.Where(dI => base._semiAutomatedDispList.Contains(dI)).ToList();
            semiAutomatedPlugUnplugDisplays.ForEach(curDisp =>
            {
                base.UnplugSemiautomated("Unplug " + curDisp + " and plug while the system is in S5");
            });

            base.PerformHotplugUnplug();
        }
    }
}
