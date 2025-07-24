namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Collections.Generic;

    class MP_48Hz_Base : TestBase
    {
        protected string GetCurrentRRFromCUIandOS()
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.GetInternalDisplay()).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            string osRR = string.Concat(actualMode.RR.ToString(), actualMode.InterlacedFlag.Equals(0) ? "p" : "i");
            Log.Verbose("Refresh Rate from OS = {0}", osRR);
            return osRR;
        }
    }
}