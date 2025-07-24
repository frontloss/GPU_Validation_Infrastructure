namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Reflection;
    using System.Collections.Generic;

    public class StandaloneCache : SortedList<string, CacheCollection>, ICacheWrapper
    {
        private bool _enableCaching = true;

        public StandaloneCache(bool argEnableCaching)
        {
            this._enableCaching = argEnableCaching;
        }
        public void Add(Message argMessage)
        {
            if (this._enableCaching)
            {
                if (!base.ContainsKey(argMessage.Name))
                    base.Add(argMessage.Name, new CacheCollection());
                base[argMessage.Name].Add(argMessage);
            }
        }
        public MethodInfo Get(Message argMessage)
        {
            if (this._enableCaching && !string.IsNullOrEmpty(argMessage.Name) && base.ContainsKey(argMessage.Name) && base[argMessage.Name].ContainsKey(argMessage.Action))
                return base[argMessage.Name][argMessage.Action];
            return null;
        }
        public void Purge()
        {
            if (this._enableCaching)
            {
                base.Keys.ToList().ForEach(k => base[k].Clear());
                base.Clear();
            }
        }
    }
}