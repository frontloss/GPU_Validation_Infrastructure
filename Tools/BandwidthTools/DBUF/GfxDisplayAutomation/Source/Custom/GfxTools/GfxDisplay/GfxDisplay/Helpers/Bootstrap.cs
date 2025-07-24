namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    internal static class Bootstrap
    {
        internal static List<DisplayInfo> EnumerateDisplaysAndModes()
        {
            List<DisplayInfo> enumeratedDisplays = WindowsFunctions.GetAllDisplayList();
            enumeratedDisplays.ForEach(dI =>
                {
                    if (dI.IsActive)
                    {
                        dI.CurrentMode = WindowsFunctions.GetCurrentMode(dI.WindowsMonitorID, dI.AdapterName);
                        dI.SupportedModes = WindowsFunctions.GetSupportedModes(dI.AdapterName);
                    }
                });
            return enumeratedDisplays;
        }
    }
}
