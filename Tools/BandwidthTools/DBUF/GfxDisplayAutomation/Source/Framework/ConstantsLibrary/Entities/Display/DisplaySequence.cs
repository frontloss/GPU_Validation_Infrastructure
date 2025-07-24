using System.Collections.Generic;

namespace Intel.VPG.Display.Automation
{
    public class DisplaySequence : Dictionary<int, DisplayType>
    {
        public DisplayType GetDisplayType(int key)
        {
            if (this.ContainsKey(key))
                return  this[key];
            return DisplayType.None;
        }
        public List<DisplayType> PluggableDisplayList;
        public DisplaySequence()
        {
            PluggableDisplayList = new List<DisplayType>();
        }
    }
}
