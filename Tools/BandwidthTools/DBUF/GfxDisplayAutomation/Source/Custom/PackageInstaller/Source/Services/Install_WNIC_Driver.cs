using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace PackageInstaller
{
    class Install_WNIC_Driver : InitEnvironment
    {
        private StubDriverParam WNICStubDriverParam;
        private StubDriverInstallUnInstallParam InstallUnInstallParam;
        private StubDriverAccessParam WNICStubAccessParam;
        private NonPnPDriverRoutine DriverRoutine;
        public override bool Run()
        {
            return InstallWNICDriver();
        }
        public bool InstallWNICDriver()
        {
            WNICStubDriverParam = new StubDriverParam();
            InstallUnInstallParam = new StubDriverInstallUnInstallParam();
            WNICStubAccessParam = new StubDriverAccessParam();
            DriverRoutine = new NonPnPDriverRoutine();
            WNICStubAccessParam.DriverStringPattern = "WNIC Stub Driver";

            UpdateWNICStubDriverProperty();

            Log.Messege("Pre Condition to install WNIC Stub Driver");

            if (VerifyDriverUpdateStatus() && WNICStubDriverStatus())
            {
                Log.Messege("WNIC Stub Driver already installed and Running");
                return true;
            }
            else
            {
                if (InstallWNICStubDriver())
                {
                    Log.Success("Successfully Installed WNIC Stub Driver");
                    return true;
                }
                else
                {
                    Log.Fail("Unable to install WNIC Stub Driver");
                    return false;
                }
            }

        }

        /// <summary>
        /// Function to install the WNIC Stub Driver
        /// </summary>
        /// <returns>bool</returns>
        internal bool InstallWNICStubDriver()
        {
            WNICStubDriverParam.ServiceType = NonPnPDriverService.Install;
            Log.Messege("Installing Wigig Stub Driver");
            DriverRoutine.SetMethod(WNICStubDriverParam);
            return true;
        }

        /// <summary>
        /// Function to verify the upgrade status of WNIC Stub Driver 
        /// </summary>
        /// <returns></returns>
        internal bool VerifyDriverUpdateStatus()
        {
            Log.Messege("Verify WNIC Driver Upgrade Status");
            WNICStubDriverParam.ServiceType = NonPnPDriverService.VerifyDriverUpdate;
            return DriverRoutine.SetMethod(WNICStubDriverParam);
        }

        /// <summary>
        /// Function to get the current status of WNIC Stub Driver 
        /// </summary>
        /// <returns></returns>
        internal bool WNICStubDriverStatus()
        {
            WNICStubDriverParam.ServiceType = NonPnPDriverService.Status;
            Log.Messege("Get Wigig Driver Status");
            return DriverRoutine.SetMethod(WNICStubDriverParam);
        }

        /// <summary>
        /// Function to assign to all the files which are required for installation of WNIC Stub Driver 
        /// </summary>
        private void UpdateWNICStubDriverProperty()
        {
            InstallUnInstallParam.DriverpackagePath = Directory.GetCurrentDirectory() + @"\WiGig";
            InstallUnInstallParam.RegKeyName = "wnic_reg.reg";
            InstallUnInstallParam.DriverBinaryName = "WNICStub.sys";
            InstallUnInstallParam.INFFileName = base.SystemInfo.OS.Architecture.Equals("x64") ? "WNICStub64.inf" : "WNICStub.inf";
            WNICStubDriverParam.InstallParam = InstallUnInstallParam;
            WNICStubDriverParam.AccessParam = WNICStubAccessParam;
        }
    }
}
