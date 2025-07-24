namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class SB_Modes_DisplaySwap_Hotplug_Unplug_Semiautomated:SB_modes_DisplaySwap_Hotplug_Unplug
    {
        protected override void VerifyMode(List<DisplayModeList> argDispModeList)
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            List<DisplayType> semiAutomatedPlugUnplugDisplays = currentConfig.CustomDisplayList.Where(dI => base._semiAutomatedDispList.Contains(dI)).ToList();
          semiAutomatedPlugUnplugDisplays.ForEach(curDisp=>
          {
              base.UnplugSemiautomated("Unplug and plug back " + curDisp.ToString());
          });
          base.VerifyMode(argDispModeList);
        }      
    }
}
