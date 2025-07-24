namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Collections.Generic;

    class SystemInfo : FunctionalBase, IGetMethod, IParse
    {
        private Dictionary<CUISysInfo, Func<string>> _featureFuncMappings = new Dictionary<CUISysInfo, Func<string>>();

        public SystemInfo()
            : base()
        {
            this._featureFuncMappings.Add(CUISysInfo.DriverVersion, () => SystemInfoRepo.Instance.FormIntelLParenRRParen_Graph.DriverVersion.TextValue);
        }
        public object GetMethod(object argMessage)
        {
            CUISysInfo sysInfo;
            if (Enum.TryParse(argMessage.ToString(), true, out sysInfo) && this._featureFuncMappings.ContainsKey(sysInfo))
                return this._featureFuncMappings[sysInfo]();
            return string.Empty;
        }
        public void Parse(string[] args)
        {
            if (args.Length > 0 && args[0].Equals("get"))
                Log.Verbose("{0} in CUI Information Page is {1}", args[1], this.GetMethod(args[1]));
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(@"..\>Execute SystemInfo get DriverVersion").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
    }
}