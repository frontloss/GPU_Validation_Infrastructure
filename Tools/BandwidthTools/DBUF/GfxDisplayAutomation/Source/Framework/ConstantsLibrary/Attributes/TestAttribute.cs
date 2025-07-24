namespace Intel.VPG.Display.Automation
{
    using System;

    [AttributeUsage(AttributeTargets.Method | AttributeTargets.Class, AllowMultiple = true)]
    public class TestAttribute : Attribute
    {
        public TestType Type { get; set; }
        public int Order { get; set; }
    }
}
