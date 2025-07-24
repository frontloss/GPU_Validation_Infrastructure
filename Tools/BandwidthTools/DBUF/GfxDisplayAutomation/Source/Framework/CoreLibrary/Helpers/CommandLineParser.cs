namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    public class CommandLineParser
    {
        private Dictionary<ArgumentType, Func<string[], object>> _commands = null;
        public ParamInfo ParamInfo { get; private set; }

        public CommandLineParser()
        {
            this.ParamInfo = new ParamInfo();
            this._commands = new Dictionary<ArgumentType, Func<string[], object>>();
            this._commands.Add(ArgumentType.TestName, this.ParseTestName);
            this._commands.Add(ArgumentType.Config, this.ParseConfig);
            this._commands.Add(ArgumentType.Display, this.ParseDisplays);
        }
        public void Parse<U>(string[] args, ArgumentType argType)
        {
            this.ParamInfo.Add(argType, this._commands[argType](args));
        }

        private string ParseTestName(string[] args)
        {
            string testName = string.Empty;
            if (this.IsInList(ArgumentType.TestName, args))
            {
                testName = args[(int)ArgumentType.TestName];
                testName = testName.Replace(".dll", string.Empty).Replace(".DLL", string.Empty);
            }
            return testName;
        }
        private DisplayConfigList ParseConfig(string[] args)
        {
            DisplayConfigList displayModeList = null;
            string entry = args.Skip(1).FirstOrDefault();
            if (this.IsEntryConfigType(entry))
            {
                displayModeList = new DisplayConfigList();
                entry.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries).ToList().ForEach(dM => displayModeList.Add(dM));
            }
            return displayModeList;
        }
        private DisplayList ParseDisplays(string[] args)
        {
            DisplayList displayList = null;
            string entry = string.Empty;
            if (this.IsInList(ArgumentType.Display, args))
                entry = args[(int)ArgumentType.Display];
            else if (this.IsEntryDisplayType(args.LastOrDefault()))
                entry = args.LastOrDefault();
            if (!string.IsNullOrEmpty(entry))
            {
                displayList = new DisplayList();
                entry.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries).ToList().ForEach(d => displayList.Add(d));
                //displayList.Add(DisplayType.None);
            }
            return displayList;
        }
        private bool IsInList(ArgumentType argType, string[] args)
        {
            return ((args.Length - 1) >= (int)argType);
        }
        private bool IsEntryConfigType(string argEntry)
        {
            if (string.IsNullOrEmpty(argEntry))
                return false;
            DisplayConfigType displayConfigType;
            return Enum.TryParse<DisplayConfigType>(argEntry.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries).FirstOrDefault(), true, out displayConfigType);
        }
        private bool IsEntryDisplayType(string argEntry)
        {
            if (string.IsNullOrEmpty(argEntry))
                return false;
            DisplayType displayType;
            return Enum.TryParse<DisplayType>(argEntry.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries).FirstOrDefault(), true, out displayType);
        }
    }
}