namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    internal class ConsoleFormatter : Dictionary<LogType, ConsoleColor>
    {
        internal ConsoleFormatter()
        {
            this.Add(LogType.Alert, ConsoleColor.Yellow);
            this.Add(LogType.Fail, ConsoleColor.Red);
            this.Add(LogType.Message, ConsoleColor.White);
            this.Add(LogType.Success, ConsoleColor.Green);
            this.Add(LogType.Verbose, ConsoleColor.DarkGray);
            this.Add(LogType.Custom, ConsoleColor.Blue);
            this.Add(LogType.Sporadic, ConsoleColor.Magenta);
        }
        internal ConsoleColor GetColor(LogType argType)
        {
            if (this.ContainsKey(argType))
                return this[argType];
            return ConsoleColor.White;
        }
    }
}