namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_Modes_DisplayConfiguration_Hotplug_Unplug_Semiautomated:SB_modes_DisplayConfig_Hotplug_Unplug
    {
        protected override void PerformHotplugUnplug(DisplayConfig argDispConfig)
        {
            List<DisplayType> semiAutomatedDisplays = argDispConfig.DisplayList.Where(dI => base._semiAutomatedDispList.Contains(dI)).ToList();
           semiAutomatedDisplays.ForEach(curDisp=>
           {
               base.UnplugSemiautomated("Unplug and plug back " + curDisp.ToString());
           });
            base.PerformHotplugUnplug(argDispConfig);


        }      
    }
}
