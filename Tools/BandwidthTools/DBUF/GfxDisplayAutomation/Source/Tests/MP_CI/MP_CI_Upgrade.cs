namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasUpgrade)]
    [Test(Type = TestType.HasINFModify)]
    class MP_CI_Upgrade : TestBase
    {
        private string ciCurrDriver = string.Concat(Directory.GetCurrentDirectory(), @"\CI_CurrDriver.ver");

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.CustomDriverPath)
                || Directory.GetFiles(base.ApplicationManager.ApplicationSettings.CustomDriverPath, "Setup.exe").Count().Equals(0))
                Log.Abort("Setup file(s) in {0} path not found!", base.ApplicationManager.ApplicationSettings.CustomDriverPath);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Upgrade the driver with different version and reboot the system.");
            Log.Verbose("Writing {0} to {1}", base.MachineInfo.Driver.Version, ciCurrDriver);
            File.WriteAllText(ciCurrDriver, base.MachineInfo.Driver.Version);
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.CustomDriverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UpgradeDriver, Action.SetMethod, param))
                Log.Success("Driver successfully installed");
            else
            {
                Log.Message("Installing through UI approach");
                if (!base.InstallThruUI(base.ApplicationManager.ApplicationSettings.CustomDriverPath))
                    Log.Fail("Driver Installation failed");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            string prevDriverVer = string.Empty;
            if (File.Exists(this.ciCurrDriver))
            {
                prevDriverVer = File.ReadAllText(ciCurrDriver);
                File.Delete(ciCurrDriver);
                if (!prevDriverVer.Equals(base.MachineInfo.Driver.Version))
                    Log.Success("Driver successfully upgraded to {0}", base.MachineInfo.Driver.Version);
                else
                    Log.Alert("Driver upgrade unsuccessful! Driver remains at {0}", base.MachineInfo.Driver.Version);
            }
            else
                Log.Alert("Stored driver file {0} not found!", ciCurrDriver);

            Log.Message("Uninstall the current graphics driver");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
            {
                Log.Message("UnInstall driver through UI approach");
                base.UninstallThruUI();
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Upgrade the driver to previous version.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.ProdDriverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                Log.Success("Driver successfully installed");
            else
            {
                Log.Message("Installing through UI approach");
                if (!base.InstallThruUI(base.ApplicationManager.ApplicationSettings.ProdDriverPath))
                    Log.Fail("Driver Installation failed");
            }
        }
        [Test(Type = TestType.PostCondition, Order = 5)]
        public void TestPostCondition()
        {
            Log.Verbose("Test cleanup");
            base.GetOSDriverVersionNStatus(CommonExtensions.IntelDriverStringList);
        }
    }
}