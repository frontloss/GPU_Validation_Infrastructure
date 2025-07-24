namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Xml.Linq;
    using System.Diagnostics;

    [Test(Type = TestType.HasReboot)]
    class MP_SwitchableGraphics_Driver_Install_Uninstall : MP_SwitchableGraphics_Base
    {
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            string path = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, base.MachineInfo.OS.Type.ToString());
            if (!Directory.Exists(path)
                || Directory.GetFiles(path).Count().Equals(0))
                Log.Abort("Setup file(s) in {0} path not found!", path);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Set config via OS call");
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
            Log.Message(true, "Disabling Driver Signature Enforcement");
            base.SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Uninstall ATI and then Intel Driver");
            Log.Message("Uninstall ATI Adapter");
            InstallUnInstallParams uninstallParams = new InstallUnInstallParams();
            uninstallParams.AdapterType = DriverAdapterType.ATI;
            uninstallParams.ProdPath = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, base.MachineInfo.OS.Type.ToString());
            bool ret = AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, uninstallParams);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message("Verify ATI Adapter Uninstalled");
            DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.ATI);
            if (driverInfo == null)
                Log.Success("ATI adapter got uninstalled successfully");
            else
            {
                InstallUnInstallParams uninstallParams = new InstallUnInstallParams();
                uninstallParams.AdapterType = DriverAdapterType.ATI;
                uninstallParams.ProdPath = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, base.MachineInfo.OS.Type.ToString());
                bool ret = AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, uninstallParams);
            }
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message("Uninstall Intel Adapter");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Failed to UnInstall driver package");
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Install Intel and then ATI Adapter");
            Log.Message("Installing Intel Adapter");
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
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message("Installing ATI Adapter");
            InstallUnInstallParams installParams = new InstallUnInstallParams();
            installParams.ProdPath = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, base.MachineInfo.OS.Type.ToString());
            installParams.AdapterType = DriverAdapterType.ATI;
            bool retInstall = AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, installParams);
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message("Verify ATI Adapter Installed");
            DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.ATI);
            if (driverInfo.Status.ToLower().Equals(DriverState.Running.ToString().ToLower()))
                Log.Success("ATI adapter installed successfully");
            else
                Log.Abort("ATI adapter installation failed.");
        }
        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            //Log.Message(true, "Uninstall Intel and then ATI Driver");
            Log.Message("Uninstall Intel Adapter");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Failed to UnInstall driver package");
        }
        [Test(Type = TestType.Method, Order = 11)]
        public void TestStep11()
        {
            Log.Message("Uninstall ATI Adapter");
            InstallUnInstallParams uninstallParams = new InstallUnInstallParams();
            uninstallParams.AdapterType = DriverAdapterType.ATI;
            uninstallParams.ProdPath = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, base.MachineInfo.OS.Type.ToString());
            bool ret = AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, uninstallParams);
        }
        [Test(Type = TestType.Method, Order = 12)]
        public void TestStep12()
        {
            Log.Message("Verify ATI Adapter Uninstalled");
            DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.ATI);
            if (driverInfo == null)
                Log.Success("ATI adapter got uninstalled successfully");
            else
            {
                InstallUnInstallParams uninstallParams = new InstallUnInstallParams();
                uninstallParams.AdapterType = DriverAdapterType.ATI;
                uninstallParams.ProdPath = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, base.MachineInfo.OS.Type.ToString());
                bool ret = AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, uninstallParams);
            }
        }
        [Test(Type = TestType.Method, Order = 13)]
        public void TestStep13()
        {
            Log.Message(true, "Install Intel and then ATI Adapter");
            Log.Message("Installing Intel Adapter");
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
        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
        {
            Log.Message("Installing ATI Adapter");
            InstallUnInstallParams installParams = new InstallUnInstallParams();
            installParams.ProdPath = string.Format(@"{0}\{1}", base.ApplicationManager.ApplicationSettings.SwitchableGraphicsDriverPath, base.MachineInfo.OS.Type.ToString());
            installParams.AdapterType = DriverAdapterType.ATI;
            bool retInstall = AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, installParams);
        }
        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            Log.Message("Verify ATI Adapter Installed");
            DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.ATI);
            if (driverInfo.Status.ToLower().Equals(DriverState.Running.ToString().ToLower()))
                Log.Success("ATI adapter installed successfully");
            else
                Log.Abort("ATI adapter installation failed.");
        }

    }
}
