namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;

    class MP_InstallUninstall_Sanity : TestBase
    {
        DriverInfo drivInfo;
        protected List<DisplayModeList> allModeList = new List<DisplayModeList>();
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            string oemFilePath = "C:\\Windows\\Inf";
            string[] oemFiles = Directory.GetFiles(oemFilePath).ToArray().Select(f => Path.GetFileName(f)).ToArray();
            string[] driverOemFile = oemFiles.Where(dI => dI.StartsWith(base.MachineInfo.Driver.OEMFile.ToString().Split('.').First())).ToArray();
            string infFilePath = CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
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
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.CustomDisplayList);
            List<DisplayMode> modeList = null;

            allModeList.ForEach(dML =>
            {
                modeList = GetMinMaxInterModes(dML.supportedModes.ToList());
                modeList.ForEach(dM =>
                {
                    this.ApplyNVerifyModeOS(dM, dML.display);
                });
            });
        }


        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Disable driver");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 3});
            drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
            if (drivInfo.Status.ToLower().Equals("disabled"))
                Log.Success("IGD Disabled.");
            else
                Log.Fail("IGD not Disabled.");
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Enable the driver");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 4});
            drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
            if (drivInfo.Status.ToLower().Equals("running"))
            {
                Log.Success("IGD Enabled.");
                AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            }
            else
                Log.Fail("IGD not Enabled.");
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Uninstall the driver.");
            InstallUnInstallParams param = new InstallUnInstallParams();
            if (AccessInterface.SetFeature<bool, InstallUnInstallParams>(Features.UnInstallDriver, Action.SetMethod, param))
                Log.Success("Successfully unInstall driver package");
            else
                Log.Fail("Failed to UnInstall driver package");
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Installing the latest production driver through device manager");
            InstallUnInstallParams param = new InstallUnInstallParams();
            param.ProdPath = base.ApplicationManager.ApplicationSettings.ProdDriverPath;

                Log.Message("Installing through UI approach");
                if (!base.InstallThruUI(base.ApplicationManager.ApplicationSettings.ProdDriverPath))
                    Log.Fail("Driver Installation failed");
        }

        protected List<DisplayMode> GetMinMaxInterModes(List<DisplayMode> modeList)
        {
            List<DisplayMode> minMaxInterMode = new List<DisplayMode>();
            minMaxInterMode.Add(modeList.First());
            minMaxInterMode.Add(modeList[modeList.Count / 2]);
            minMaxInterMode.Add(modeList.Last());
            return minMaxInterMode;
        }

        protected void ApplyNVerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
            Log.Message("Verify the selected mode got applied for {0}", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
                Log.Success("Mode {0} is applied for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
    }
}
