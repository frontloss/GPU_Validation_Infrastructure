namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class SB_PND_Latency_Modes_Basic : SB_PND_Latency_Modes_All
    {
        protected override List<DisplayModeList> GetModes(List<DisplayType> argCustomDisplayList)
        {
            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argCustomDisplayList);

            foreach (DisplayModeList lst in allModeList)
            {
                listDisplayMode.Add(new DisplayModeList() { display = lst.display, supportedModes = { lst.supportedModes.First(), lst.supportedModes[lst.supportedModes.Count / 2], lst.supportedModes.Last() } });
            }

            return listDisplayMode;
        }
    }
}
