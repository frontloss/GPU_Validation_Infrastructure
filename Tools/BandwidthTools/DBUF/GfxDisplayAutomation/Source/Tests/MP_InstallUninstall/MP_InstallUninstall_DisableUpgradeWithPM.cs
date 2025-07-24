namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasUpgrade)]
    class MP_InstallUninstall_DisableUpgradeWithPM : TestBase
    {
        private string ciCurrDriver = string.Concat(Directory.GetCurrentDirectory(), @"\CI_CurrDriver.ver");
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            List<string> installPaths = new List<string>()
            {
                base.ApplicationManager.ApplicationSettings.ProdDriverPath,
                base.ApplicationManager.ApplicationSettings.CustomDriverPath
            };
            installPaths.ForEach(path =>
            {
                CommonExtensions.IdentifyDriverFile(path);
            });
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Installing the previous working driver through device manager");
            Log.Verbose("Writing {0} to {1}", base.MachineInfo.Driver.Version, ciCurrDriver);
            File.WriteAllText(ciCurrDriver, base.MachineInfo.Driver.Version);
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.CustomDriverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UpgradeDriver, Action.SetMethod,param))
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
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Set possible display configuration.");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Disable the driver");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 5, 5 });
            Log.Verbose("Current driver version {0}", base.MachineInfo.Driver.GetDriverInfoStr());
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Upgrade the latest production driver under test using device manager and reboot the system.");
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
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Apply any other valid display configuration.");
            this.TestStep3();
            PowerParams powerParam = new PowerParams() { Delay = 30 };
            Log.Message(true, "Take the system to S3 and resume.");
            base.EventResult(PowerStates.S3, base.InvokePowerEvent(powerParam, PowerStates.S3));
            Log.Message(true, "Take the system to S4 and resume.");
            base.EventResult(PowerStates.S4, base.InvokePowerEvent(powerParam, PowerStates.S4));
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Disable and enable the driver again.");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 10, 10 });
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 10, 10 });
        }
        [Test(Type = TestType.PostCondition, Order = 8)]
        public void TestPostCondition()
        {
            Log.Verbose("Test cleanup");
            base.GetOSDriverVersionNStatus(CommonExtensions.IntelDriverStringList);
        }
    }
}