namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    public class DisplayList : List<DisplayType>
    {
        public void Add(string argDisplay)
        {
            DisplayType displayType;
            if (!Enum.TryParse<DisplayType>(argDisplay, true, out displayType))
                Log.Abort("{0} is not a valid Display!", argDisplay);
            base.Add(displayType);
        }
    }
}