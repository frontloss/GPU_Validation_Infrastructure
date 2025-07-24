namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    public interface IApplicationManager
    {
        ParamInfo ParamInfo { get; }
        IApplicationSettings ApplicationSettings { get; }
        IAccessInterface AccessInterface { get; }
        MachineInfo MachineInfo { get; set; }
        List<TestType> ListTestTypeAttribute { get; set; }
        HotPlugUnPlugContext HotplugUnplugCntx { get; set; }
        bool VerifyTDR { get; set; }
        bool Dvmu4DeviceStatus { get; }
    }
}
