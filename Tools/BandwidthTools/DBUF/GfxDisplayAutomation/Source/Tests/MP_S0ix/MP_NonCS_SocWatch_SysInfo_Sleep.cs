
namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Xml;
    using System.Threading;

    class MP_NonCS_SocWatch_SysInfo_Sleep : MP_NonCS_SocWatch_SysInfo
    {
        CSParam csParam = new CSParam();
        public MP_NonCS_SocWatch_SysInfo_Sleep()
        {
            nonCS_PackageC8PlushState = true;
            NonCSInputOption = NonCSPowerOption.Sleep;
        }
    
    }
}
