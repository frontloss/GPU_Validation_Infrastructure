namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    public class ApplicationManager : IApplicationManager
    {
        public ParamInfo ParamInfo { get; private set; }
        public IApplicationSettings ApplicationSettings { get; private set; }
        public IAccessInterface AccessInterface { get; private set; }
        public MachineInfo MachineInfo { get; set; }
        public List<TestType> ListTestTypeAttribute { get; set; }
        public HotPlugUnPlugContext HotplugUnplugCntx { get; set; }
        public bool VerifyTDR { get; set; }
        private TestBase _context = null;
        public bool Dvmu4DeviceStatus { get; private set; }

        public ApplicationManager(ParamInfo argParamInfo, IApplicationSettings argApplicationSettings)
        {
            this.ParamInfo = argParamInfo;
            _context = _context.Load(ParamInfo[ArgumentType.TestName] as string);
            this.ApplicationSettings = argApplicationSettings;
            this.AccessInterface = new AccessInterface(this, new StandaloneCache(argApplicationSettings.EnableCaching));
            this.MachineInfo = this.AccessInterface.GetFeature<MachineInfo>(Features.WinSystemInformation, Action.Get);
            this.ListTestTypeAttribute = AssemblyLoader.GetAllTestTypeAttribute(_context);
            this.HotplugUnplugCntx = new HotPlugUnPlugContext();
            this.VerifyTDR = true;
            this.Dvmu4DeviceStatus = this.AccessInterface.GetFeature<bool, string>(Features.DeviceStatus, Action.GetMethod, Source.AccessAPI, "usb*vid_8087*pid_f021*");
        }
    }
}