namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasUpgrade)]
    class MP_InstallUninstall_UpgradeWithRotation : TestBase
    {
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
            Log.Verbose("Current driver version {0}", base.MachineInfo.Driver.GetDriverInfoStr());
            Log.Message(true, "Install an older driver using device manager and reboot the system");
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
            Log.Message(true, "Set possible display configuration.");
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
            Log.Message(true, "Rotate the display(s) to 180 angle");
            List<int> angle = new List<int> { 180 };
            RotateDisplay(angle, false);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
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
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Rotate the displays back to 0 degree, in case rotation performed in step 4 still exists.");
            List<int> angle = new List<int> { 0 };
            RotateDisplay(angle, true);

            Log.Message(true, "Apply other valid display configuration and set not-optimal resolution.");
            List<DisplayModeList> allSupportedModes = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.Default, base.CurrentConfig.DisplayList);
            base.CurrentConfig.DisplayList.ForEach(dT =>
            {
                Log.Verbose("Retrieving supported modes for {0}", dT);
                List<DisplayMode> supportedMode = allSupportedModes.Where(dML => dML.display == dT).Select(dML => dML.supportedModes).First();
                if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, supportedMode.ElementAt(supportedMode.Count / 2)))
                {
                    Log.Success("Mode set successful.");
                }
                else
                    Log.Fail("Mode set failed!");
            });
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Rotate the display to 90/180/270.");
            List<int> angle = new List<int> { 90, 180, 270, 0 };
            RotateDisplay(angle, false);
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
            Log.Message(true, "Re-install the older driver.");
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
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message(true, "Randomly switch across the connected displays");
            List<DisplayConfig> switchPatternList = new List<DisplayConfig>();

            if (base.CurrentConfig.DisplayList.Count == 2)
                this.GetSwitchPatternForDualDisplayMode(switchPatternList);
            else if (base.CurrentConfig.DisplayList.Count > 2)
                this.GetSwitchPatternForTriDisplayMode(switchPatternList);
            else
                Log.Abort("Display Switching requires atleast 2 displays connected!");

            switchPatternList.ForEach(DC =>
            {
                Log.Verbose("Set display switch configurations : {0}", DC.GetCurrentConfigStr());
                AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, DC);

            });
        }
        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            Log.Message(true, "Connect all displays planned in grid");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }

        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
        }
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");

            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay });
            argList.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });

        }
        private void RotateDisplay(List<int> argAngle, bool IsPreviousRotationChk)
        {
            bool status_set = false;
            List<DisplayType> displayTypeList = null;
            if (base.CurrentConfig.ConfigType == DisplayConfigType.ED || base.CurrentConfig.ConfigType == DisplayConfigType.TED)
                displayTypeList = base.CurrentConfig.CustomDisplayList;
            else
                displayTypeList = new List<DisplayType>() { base.CurrentConfig.PrimaryDisplay };

            DisplayInfo displayInfo = null;
            DisplayMode targetMode;
            DisplayMode currentMode;
            displayTypeList.ForEach(dT =>
            {
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dT).First();
                currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                argAngle.ForEach(angle =>
                {
                    Log.Verbose("Setting rotation {0} for {1}", angle, dT);
                    currentMode.Angle = Convert.ToUInt32(angle);
                    if (IsPreviousRotationChk && angle != 0)
                        currentMode.Angle = 0;
                    status_set = AccessInterface.SetFeature<bool, DisplayMode>(Features.Rotation, Action.SetMethod, currentMode);
                    targetMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, displayInfo);
                    if (status_set && targetMode.Angle.Equals(currentMode.Angle))
                        Log.Success("Rotation {0} successfully set for {1}", targetMode.Angle, dT);
                    else
                        Log.Fail("Unable to set rotation {0} for {1}", angle, dT);
                });
            });
        }

    }
}