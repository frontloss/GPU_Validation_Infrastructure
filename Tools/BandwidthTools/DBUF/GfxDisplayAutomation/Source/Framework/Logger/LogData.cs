namespace Intel.VPG.Display.Automation
{
    using System;

    internal class LogData
    {
        internal LogType Type { get; set; }
        internal string Screenshot { get; set; }
        internal string Preview { get; set; }
        internal DateTime Timestamp { get; set; }
        internal bool Transformable { get; set; }
        internal string Name { get; set; }
        internal bool IsParent { get; set; }
        internal LogData(string argData)
        {
            this.Name = argData;
        }
    }
}