namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System;

    public class OSInfo
    {
        private Dictionary<string, string> _osTypeKeys = new Dictionary<string, string>();
        public OSInfo()
        {
            this._osTypeKeys.Add("6.1", "WIN7");
            this._osTypeKeys.Add("6.2", "WIN8");
            this._osTypeKeys.Add("6.3", "WINBLUE");
            this._osTypeKeys.Add("6.4", "WINTHRESHOLD");
            this._osTypeKeys.Add("10.0", "WINTHRESHOLD");
        }

        public string Description { get; set; }
        public string Build { get; set; }
        public string Architecture { get; set; }
        public OSType Type
        { 
            get { return (OSType)Enum.Parse(typeof(OSType), this._osTypeKeys[this.Build.Substring(0, this.Build.LastIndexOf('.'))], true); }
        }

        public bool IsGreaterThan(OSType baseType)
        {
            return this.Type >= baseType;
        }
    }
}