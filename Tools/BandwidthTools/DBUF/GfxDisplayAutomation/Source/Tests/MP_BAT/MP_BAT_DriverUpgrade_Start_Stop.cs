namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Threading;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasUpgrade)]
    class MP_BAT_DriverUpgrade_Start_Stop : TestBase
    {
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            Log.Message(true, "2. Set any possible display configuration.");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Repeat steps 3 to 5 for 3 times");
            for (int idx = 0; idx < 3; idx++)
            {
                base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 3, 4 });
                if (this.AssertDriverEnabled())
                {
                    Log.Success("IGD Enabled. CUI Launched");
                    AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
                    Thread.Sleep(1000);
                }
                else
                    Log.Abort("IGD not Enabled!");
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            List<DisplayModeList> allSupportedModes = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.Default, base.CurrentConfig.DisplayList);
            Log.Verbose("Retrieving supported modes for {0}", base.CurrentConfig.PrimaryDisplay);
            List<DisplayMode> supportedModes = allSupportedModes.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).First();

            Log.Message(true, "7. set different mode and verify no corruption is seen while setting the mode");
            DisplayMode displayMode = supportedModes.ElementAt(supportedModes.Count / 2);
            displayMode.display = base.CurrentConfig.PrimaryDisplay;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayMode))
                Log.Success("Mode set successful");
            else
                Log.Abort("Mode set failed!");

            this.TestStep3();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            PowerParams powerParam = new PowerParams() { Delay = 30 };
            Log.Message(true, "9. Take the system to S3 and Resume");
            base.EventResult(PowerStates.S3, base.InvokePowerEvent(powerParam, PowerStates.S3));
            Log.Message(true, "9. Take the system to S4 and Resume");
            base.EventResult(PowerStates.S4, base.InvokePowerEvent(powerParam, PowerStates.S4));
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 11, 11 });
            Log.Verbose("Current driver version {0}", base.MachineInfo.Driver.GetDriverInfoStr());

            Log.Message(true, "11. Upgrade the driver with different version and reboot the system.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.CustomDriverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UpgradeDriver, Action.SetMethod, param))
            {
                Log.Success("Driver updated successfully");
                Log.Verbose("Current driver version is {0}", base.MachineInfo.Driver.Version);
            }
            else
            {
                Log.Message("Trying to update driver through UI approach");
                if (!base.InstallThruUI(base.ApplicationManager.ApplicationSettings.CustomDriverPath))
                    Log.Fail("Driver Update Failed");
            }
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 12, 12 });
            if (base.MachineInfo.Driver.Version.Equals(this.GetDriverVersionFromLog()))
                Log.Abort("Driver not upgraded, remains @ {0}", base.MachineInfo.Driver.Version);
            else
                Log.Success("Driver upgraded to {0}", base.MachineInfo.Driver.GetDriverInfoStr());

            Log.Message("Uninstall the current graphics driver");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
            {
                base.UninstallThruUI();
            }
        }
        [Test(Type = TestType.PostCondition, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "13. Upgrade the driver to previous version.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.ProdDriverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UpgradeDriver, Action.SetMethod, param))
                Log.Success("Driver Successfully updated");
            else
            {
                Log.Message("Trying to update driver through UI approach");
                if (!base.InstallThruUI(base.ApplicationManager.ApplicationSettings.ProdDriverPath))
                Log.Fail("Driver Updation failed");
            }
        }
        [Test(Type = TestType.PostCondition, Order = 9)]
        public void TestPostCondition()
        {
            Log.Verbose("Test cleanup");
            string driverVersion = base.MachineInfo.Driver.Version;
            string driverVersionFromLog = this.GetDriverVersionFromLog();
            if (!string.IsNullOrEmpty(driverVersionFromLog))
                driverVersion = driverVersionFromLog;
            base.GetOSDriverVersionNStatus(CommonExtensions.IntelDriverStringList, driverVersion);
        }

        private string GetDriverVersionFromLog()
        {
            XDocument xDoc = XDocument.Load(Log.XmlLogDocPath);
            XElement xElement = xDoc.Root.Element(Log.LogReportText).Elements("Log").Where(e => e.Element("Data").Value.Contains("Driver.Version")).FirstOrDefault();
            if (null != xElement)
                return xElement.Element("Data").Value.Split(' ').LastOrDefault();
            return string.Empty;
        }
        private bool AssertDriverEnabled()
        {
            if (base.ChangeDriverState(Features.EnableDriver, DriverState.Running, new[] { 5, 5 }))
            {
                Log.Message(true, "5. Ensure that IGD is enabled by launching CUI");
                return AccessInterface.SetFeature<bool>(Features.LaunchCUI, Action.SetNoArgs);
            }
            return false;
        }
    }
}