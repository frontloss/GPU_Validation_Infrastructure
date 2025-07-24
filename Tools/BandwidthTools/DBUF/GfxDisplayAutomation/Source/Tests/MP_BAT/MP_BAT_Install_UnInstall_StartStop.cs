namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_BAT_Install_UnInstall_StartStop : TestBase
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            string infFilePath = CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Connect all the displays planned in the grid.");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "2. The driver version in CUI should match with the installed graphics driver.");
            AccessInterface.SetFeature<bool>(Features.LaunchCUI, Action.SetNoArgs);
            AccessInterface.Navigate(Features.SystemInfo);
            string cuiDriverVer = AccessInterface.GetFeature<string, CUISysInfo>(Features.SystemInfo, Action.GetMethod, Source.Default, CUISysInfo.DriverVersion);
            if (base.MachineInfo.Driver.Version == cuiDriverVer)
                Log.Success("Driver installed is {0}", base.MachineInfo.Driver.Version);
            else
                Log.Abort("Driver version mismatched! OS lists {0}, while CUI lists {1}", base.MachineInfo.Driver.Version, cuiDriverVer);
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "3. Disable and enable the driver from Device manager.");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 3, 3 });
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 3, 3 });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            RebootAnalysysInfo rebootData = CommonExtensions._rebootAnalysysInfo;
            rebootData.IsBasicDisplayAdapter = true;
            Log.Message(true, "3. Uninstall the graphics driver");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
            {
                base.UninstallThruUI();
            }
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            //File.Delete(CommonExtensions.UninstallFile);
            Log.Message(true, "4. The graphics driver should get uninstalled and OS should switch to VGA mode.");
            for (int i = 0; i < 5; i++)
            {
                if (!base.MachineInfo.Driver.Name.ToLower().Contains("intel"))
                    break;
                else
                    TestStep4();
            }
            base.GetOSDriverVersionNStatus(CommonExtensions.StandardDriverStringList, true);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Verbose("Test cleanup");
            //CommonExtensions.CloneDirectory(base.ApplicationManager.ApplicationSettings.ProdDriverPath, base.ApplicationManager.ApplicationSettings.AlternatePAVEProdDriverPath);
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.ProdDriverPath;
            if (!AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
            {
                Log.Message("Installing Driver through UI approach");
                base.InstallThruUI(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            }
        }
        [Test(Type = TestType.PostCondition, Order = 7)]
        public void TestPostCondition()
        {
            base.GetOSDriverVersionNStatus(CommonExtensions.IntelDriverStringList);
        }
    }
}