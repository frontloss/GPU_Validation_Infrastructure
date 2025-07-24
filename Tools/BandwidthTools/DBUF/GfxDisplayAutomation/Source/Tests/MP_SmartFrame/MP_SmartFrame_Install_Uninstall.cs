namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_SmartFrame_Install_Uninstall : MP_SmartFrame_Base
    {
        private PowerParams _powerParams = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set config SD {0} via OS", base.GetInternalDisplay());
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.SD;
            config.PrimaryDisplay = base.GetInternalDisplay();
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, config))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Uninstall Driver and Reboot");
            Log.Message(true, "3. Uninstall the graphics driver");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "4. The graphics driver should get uninstalled and OS should switch to VGA mode.");
            for (int i = 0; i < 5; i++)
            {
                if (!base.MachineInfo.Driver.Name.ToLower().Contains("intel"))
                    break;
                else
                    TestStep3();
            }
            base.GetOSDriverVersionNStatus(CommonExtensions.StandardDriverStringList, true);
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Install Driver and Reboot");
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.ProdDriverPath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
            {
                Log.Success("Driver successfully installed");
            }
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
            Log.Message(true, "Verify Smart Frame is enabled");
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Verify Smart Frame is disabled");
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
        }

    }
}