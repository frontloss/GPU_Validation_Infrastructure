namespace Intel.VPG.Display.Automation
{
    using System;

    [AttributeUsage(AttributeTargets.Method, AllowMultiple = false)]
    public class ActionTargetAttribute : Attribute
    {
        public Action Target { get; private set; }
        public ActionTargetAttribute(Action argTarget)
        {
            this.Target = argTarget;
        }
    }
}
