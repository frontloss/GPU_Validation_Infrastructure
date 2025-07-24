namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    public class DisplayConfigList : List<DisplayConfigType>
    {
        public void Add(string argDisplayMode)
        {
            DisplayConfigType displayModeType;
            if (!Enum.TryParse<DisplayConfigType>(argDisplayMode, true, out displayModeType))
                Log.Abort("{0} is not a valid Display Config!", argDisplayMode);
            base.Add(displayModeType);
        }
    }
}