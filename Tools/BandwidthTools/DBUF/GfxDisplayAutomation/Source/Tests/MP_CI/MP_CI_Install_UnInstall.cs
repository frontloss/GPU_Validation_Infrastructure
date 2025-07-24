namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;

    [Test(Type = TestType.HasReboot)]
    class MP_CI_Install_UnInstall : TestBase
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Uninstall the driver.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Driver unInstall Failed");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message("The graphics driver should get uninstalled and OS should switch to VGA mode.");
            base.GetOSDriverVersionNStatus(CommonExtensions.StandardDriverStringList);

            Log.Message(true, "Install Graphics Driver");
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
        [Test(Type = TestType.PostCondition, Order = 4)]
        public void TestPostCondition()
        {
            base.GetOSDriverVersionNStatus(CommonExtensions.IntelDriverStringList);
        }
    }
}