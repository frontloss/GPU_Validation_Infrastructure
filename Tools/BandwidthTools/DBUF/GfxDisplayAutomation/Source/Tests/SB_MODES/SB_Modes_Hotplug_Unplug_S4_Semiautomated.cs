namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_Modes_Hotplug_Unplug_S4_Semiautomated:SB_Modes_Hotplug_Unplug_S4
    {
        protected override void PerformHotplugUnplug()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            List<DisplayType> semiAutomatedPlugUnplugDisplays = currentConfig.CustomDisplayList.Where(dI => base._semiAutomatedDispList.Contains(dI)).ToList();
            semiAutomatedPlugUnplugDisplays.ForEach(curDisp =>
            {
                base.UnplugSemiautomated("Unplug " + curDisp + " and plug while the system is in S4");
            });

            base.PerformHotplugUnplug();

            List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            base.CurrentConfig.EnumeratedDisplays.Clear();
            base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
        }
    }
}
