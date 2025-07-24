namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    class MP_InstallUninstall_Basic : TestBase
    {
       
        string proddriverpath;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            string oemFilePath = "C:\\Windows\\Inf";
            proddriverpath = GetDriverPath();
            string[] oemFiles = Directory.GetFiles(oemFilePath).ToArray().Select(f => Path.GetFileName(f)).ToArray();
            string[] driverOemFile = oemFiles.Where(dI => dI.StartsWith(base.MachineInfo.Driver.OEMFile.ToString().Split('.').First())).ToArray();
            string infFilePath = CommonExtensions.IdentifyDriverFile(proddriverpath);
            DirectoryInfo info = new DirectoryInfo(oemFilePath);
            if (driverOemFile.Length == 0)
            {
                Log.Message("oem files not present in {0}, Check if files exists in current directory", oemFilePath);
                oemFiles = Directory.GetFiles(Directory.GetCurrentDirectory()).ToArray().Select(f => Path.GetFileName(f)).ToArray();
                driverOemFile = oemFiles.Where(dI => dI.StartsWith("oem")).ToArray();
                if (driverOemFile.Length != 0)
                {
                    foreach (string oemFile in driverOemFile)
                    {
                        if (File.Exists(string.Concat(Directory.GetCurrentDirectory(), "\\", oemFile)))
                            File.Copy(string.Concat(Directory.GetCurrentDirectory(), "\\", oemFile), string.Concat(oemFilePath, "\\", oemFile), true);
                    }
                }
                else
                {
                    Log.Alert("Oem files not present in {0} and {1}", oemFilePath, Directory.GetCurrentDirectory());
                }
            }
            else
            {
                Log.Message("Copy the oem files from {0} to current directory {1}", oemFilePath, Directory.GetCurrentDirectory());
                foreach (string oemFile in driverOemFile)
                {
                    if (File.Exists(string.Concat(oemFilePath, "\\", oemFile)))
                        File.Copy(string.Concat(oemFilePath, "\\", oemFile), string.Concat(Directory.GetCurrentDirectory(), "\\", oemFile), true);
                }
            }
           
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set a valid display configuration using the displays planned in the grid");
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
            Log.Message(true, "Set maximum resolution on each of the display(s) using OS call");
            this.SetMode(this.GetLastMode);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Uninstall the driver.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Failed to UnInstall driver package");
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            proddriverpath = GetDriverPath();
            Log.Message(true, "Installing the latest production driver through device manager");
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = proddriverpath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                Log.Success("Driver successfully installed");
            else
            {
                Log.Message("Installing through UI approach");
                if (!base.InstallThruUI(proddriverpath))
                    Log.Fail("Driver Installation failed");
            }
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Set intermediate resolution on each of the display(s) using OS call");
            this.SetMode(this.GetIntermediateMode);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            if ((!(base.MachineInfo.PlatformDetails.Platform == Platform.CHV)) && (!(base.MachineInfo.PlatformDetails.Platform == Platform.SKL)))
            {
                PowerParams powerParam = new PowerParams() { Delay = 30 };
                Log.Message(true, "Take the system to S3 and Resume");
                base.EventResult(PowerStates.S3, base.InvokePowerEvent(powerParam, PowerStates.S3));
            }
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Uninstall the driver.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Failed to UnInstall driver package");
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Installing the latest production driver through device manager");
            proddriverpath = GetDriverPath();
            //CommonExtensions.CloneDirectory(base.ApplicationManager.ApplicationSettings.ProdDriverPath, base.ApplicationManager.ApplicationSettings.AlternatePAVEProdDriverPath);
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = proddriverpath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                Log.Success("Driver successfully installed");
            else
            {
                Log.Message("Installing through UI approach");
                if (!base.InstallThruUI(proddriverpath))
                    Log.Fail("Driver Installation failed");
            }
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            if ((!(base.MachineInfo.PlatformDetails.Platform == Platform.VLV)) && (!(base.MachineInfo.PlatformDetails.Platform == Platform.CHV))&& (!(base.MachineInfo.PlatformDetails.Platform == Platform.SKL)))
            {
                PowerParams powerParam = new PowerParams() { Delay = 30 };
                Log.Message(true, "Take the system to S4 and Resume");
                base.EventResult(PowerStates.S4, base.InvokePowerEvent(powerParam, PowerStates.S4));
            }
        }
        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            Log.Message(true, "Uninstall the driver.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Failed to UnInstall driver package");
        }
        [Test(Type = TestType.Method, Order = 11)]
        public void TestStep11()
        {
            Log.Message(true, "Installing the latest production driver through device manager");
            proddriverpath = GetDriverPath();
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = proddriverpath;
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.InstallDriver, Action.SetMethod, param))
                Log.Success("Driver successfully installed");
            else
            {
                Log.Message("Installing through UI approach");
                if (!base.InstallThruUI(proddriverpath))
                    Log.Fail("Driver Installation failed");
            }
        }
        [Test(Type = TestType.PostCondition, Order = 12)]
        public void TestStep12()
        {
            Log.Verbose("Test Cleanup");
            Log.Message(true, "Set maximum resolution on each of the display(s) using OS call");
            this.SetMode(this.GetLastMode);
            string[] oemFiles = Directory.GetFiles(Directory.GetCurrentDirectory()).ToArray().Select(f => Path.GetFileName(f)).ToArray();
            string[] driverOemFile = oemFiles.Where(dI => dI.StartsWith("oem")).ToArray();
            if (driverOemFile.Length != 0)
            {
                foreach (string oemFile in driverOemFile)
                {
                    File.SetAttributes(oemFile, FileAttributes.Normal);
                    Thread.Sleep(1000);
                    File.Delete(oemFile);
                }
            }
        }
        private void ApplyModes(DisplayMode argSelectedMode, DisplayType dT)
        {
            Log.Message("Set {0} on {1}", argSelectedMode.GetCurrentModeStr(false), dT);
            AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode);
        }
        private void SetMode(Func<List<DisplayMode>, DisplayMode> argReference)
        {
            List<DisplayModeList> allSupportedModes = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.Default, base.CurrentConfig.DisplayList);

            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                List<DisplayMode> commonModes = null;
                commonModes = allSupportedModes.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                allSupportedModes.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                if (commonModes.Count() > 0)
                    this.ApplyModes(argReference(commonModes), base.CurrentConfig.PrimaryDisplay);
            }
            else
            {
                base.CurrentConfig.CustomDisplayList.ForEach(dT =>
                {
                    List<DisplayMode> supportedModes = allSupportedModes.Where(dML => dML.display == dT).Select(dML => dML.supportedModes).First();
                    this.ApplyModes(argReference(supportedModes), dT);
                });
            }
        }
        private DisplayMode GetLastMode(List<DisplayMode> argModes)
        {
            return argModes.Last();
        }
        private DisplayMode GetIntermediateMode(List<DisplayMode> argModes)
        {
            return argModes[argModes.Count / 2];
        }
        private string GetDriverPath()
        {
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ProdDriverPath))
            {
               return base.ApplicationManager.ApplicationSettings.AlternatePAVEProdDriverPath;
            }
            else
            {
                return  base.ApplicationManager.ApplicationSettings.ProdDriverPath;
            }
        }
    }
}