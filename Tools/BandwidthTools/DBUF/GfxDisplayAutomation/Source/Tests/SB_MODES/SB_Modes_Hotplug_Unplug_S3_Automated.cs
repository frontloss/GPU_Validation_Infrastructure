using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Modes_Hotplug_Unplug_S3_Automated:SB_Modes_Hotplug_Unplug_S3
    {        
        protected override void PerformHotplugUnplug()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            List<DisplayType> semiAutomatedPlugUnplugDisplays = currentConfig.CustomDisplayList.Where(dI => base._semiAutomatedDispList.Contains(dI)).ToList();
            semiAutomatedPlugUnplugDisplays.ForEach(curDisp =>
            {
                base.UnplugSemiautomated("Unplug " + curDisp + " and plug while the system is in S3");
            });
           
            base.PerformHotplugUnplug();

            List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            base.CurrentConfig.EnumeratedDisplays.Clear();
            base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
        }
       
    }
}
