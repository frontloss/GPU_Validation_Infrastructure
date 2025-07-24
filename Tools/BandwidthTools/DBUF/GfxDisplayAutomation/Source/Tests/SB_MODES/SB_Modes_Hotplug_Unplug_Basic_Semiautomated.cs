namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class SB_Modes_Hotplug_Unplug_Basic_Semiautomated:SB_modes_Hotplug_Unplug_Basic
    {
        protected override void PerformHotplugUnplug()
        {
            base.PerformHotplugUnplug();
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            List<DisplayType> _semiAutomatedDisplayList = currentConfig.CustomDisplayList.Where(dI => base._semiAutomatedDispList.Contains(dI)).ToList();
          _semiAutomatedDisplayList.ForEach(curDisp=>
          {
              base.UnplugSemiautomated("Unplug and plug back "+ curDisp.ToString());
          });
        }
      
    }
}
