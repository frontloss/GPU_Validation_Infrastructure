namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class InitEnumerateDisplays : InitEnvironment
    {
        public InitEnumerateDisplays(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            if (!CommonExtensions._rebootAnalysysInfo.IsBasicDisplayAdapter)
            {
                List<DisplayInfo> enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                if (AccessInterface.SetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.SetMethod, enumeratedDisplays))
                {
                    AccessInterface.GetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetMethod, Source.AccessAPI, enumeratedDisplays);
                }
                if (!base.Manager.ParamInfo.ContainsKey(ArgumentType.Enumeration))
                {
                    base.Manager.ParamInfo.Add(ArgumentType.Enumeration, enumeratedDisplays);
                }
            }
        }
    }
}
