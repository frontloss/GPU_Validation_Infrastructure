using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PackageInstaller
{
    public class StubDriverInstallUnInstallParam
    {
        public string DriverpackagePath;
        public string RegKeyName;
        public string DriverBinaryName;
        public string INFFileName;
    }

    public class StubDriverAccessParam
    {
        public string DriverStringPattern;
    }

    public class StubDriverParam
    {
        public NonPnPDriverService ServiceType;
        public StubDriverInstallUnInstallParam InstallParam;
        public StubDriverAccessParam AccessParam;
    }
}
