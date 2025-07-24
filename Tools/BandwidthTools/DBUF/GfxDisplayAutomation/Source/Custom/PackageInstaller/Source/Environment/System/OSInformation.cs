using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PackageInstaller
{
    public class OSInformation
    {
        private Dictionary<string, OSType> _osTypeKeys = new Dictionary<string, OSType>();

        public OSInformation()
        {
            this._osTypeKeys.Add("6.1", OSType.WIN_7);
            this._osTypeKeys.Add("6.2", OSType.WIN_8);
            this._osTypeKeys.Add("6.3", OSType.WIN_BLUE);
            this._osTypeKeys.Add("6.4", OSType.WIN_TH);
            this._osTypeKeys.Add("10.0", OSType.WIN_TH);
        }

        public OSInfo Get()
        {
            OSInfo info = new OSInfo();
            info.Architecture = CommonRoutine.GetWin32Value("OSArchitecture", "SELECT * FROM Win32_OperatingSystem").ToLower().Contains("64") ? OSArchitecture.x64 : OSArchitecture.x86;
            info.OSType = GetOSType();
            info.Description = CommonRoutine.GetWin32Value("Caption", "SELECT * FROM Win32_OperatingSystem");
            return info;
        }

        private OSType GetOSType()
        {
            string build = CommonRoutine.GetWin32Value("Version", "SELECT * FROM Win32_OperatingSystem");
            return this._osTypeKeys[build.Substring(0, build.LastIndexOf('.'))];
        }
    }
}
