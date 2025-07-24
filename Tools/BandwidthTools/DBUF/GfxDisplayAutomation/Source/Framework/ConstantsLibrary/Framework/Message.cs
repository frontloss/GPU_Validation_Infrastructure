namespace Intel.VPG.Display.Automation
{
    using System.Reflection;
    using System.Collections.Generic;

    public class Message : IMessage
    {
        public string Name { get; set; }
        public object Value { get; set; }
        public Features Feature { get; set; }
        public Action Action { get; set; }
        public MethodInfo Target { get; set; }
        public Source Source { get; set; }
        public object Data { get; set; }
        public string[] Args { get; set; }
        public object Context { get; set; }
        public List<DisplayInfo> EnumeratedDisplays { get; set; }
        public IApplicationManager AppManager { get; set; }
        public int CurrentMethodIndex { get; set; }
        public int OverrideMethodIndex { get; set; }
        public DisplayConfig CurrentConfig { get; set; }
    }
}
