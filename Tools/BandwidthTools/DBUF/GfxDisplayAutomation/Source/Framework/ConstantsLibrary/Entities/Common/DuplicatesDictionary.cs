namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class DuplicatesDictionary<K,V> : List<KeyValuePair<K, V>>
    {
        public void Add(K argKey, V argValue)
        {
            base.Add(new KeyValuePair<K, V>(argKey, argValue));
        }
    }
}