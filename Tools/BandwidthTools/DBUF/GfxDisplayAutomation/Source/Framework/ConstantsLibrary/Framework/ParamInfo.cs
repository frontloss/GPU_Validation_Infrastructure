namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class ParamInfo : Dictionary<ArgumentType, object>
    {
        public U Get<U>(ArgumentType argType)
        {
            if (this.ContainsKey(argType) && null != this[argType])
                return (U)this[argType];
            return default(U);
        }
    }
}
