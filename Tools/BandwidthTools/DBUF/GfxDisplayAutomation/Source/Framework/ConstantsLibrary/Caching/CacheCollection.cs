namespace Intel.VPG.Display.Automation
{
    using System.Reflection;
    using System.Collections.Generic;

    public class CacheCollection : SortedList<Action, MethodInfo>
    {
        public void Add(Message argMessage)
        {
            if (!base.ContainsKey(argMessage.Action))
                base.Add(argMessage.Action, argMessage.Target);
        }
    }
}