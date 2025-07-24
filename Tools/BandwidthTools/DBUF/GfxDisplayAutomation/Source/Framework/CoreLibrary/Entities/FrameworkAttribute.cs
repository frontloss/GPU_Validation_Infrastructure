namespace Intel.VPG.Display.Automation
{
    using System;

    [AttributeUsage(AttributeTargets.Method, AllowMultiple = false)]
    internal class FrameworkAttribute : Attribute
    {
        internal ComponentType Type { get; private set; }
        internal FrameworkAttribute(ComponentType argType)
        {
            this.Type = argType;
        }
    }
}
