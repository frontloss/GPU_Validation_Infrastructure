namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    [Test(Type = TestType.HasReboot)]
    class MP_CI_SmoothRotation : TestBase
    {
        private PowerParams _powerParams = null;
        private string _infPath = string.Empty;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ProdDriverPath)
                || Directory.GetFiles(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "Setup.exe").Count().Equals(0))
                Log.Abort("Setup file(s) in {0} path not found!", base.ApplicationManager.ApplicationSettings.ProdDriverPath);
        }
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Make changes in INF file & Install driver");
            this._infPath = CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            INFFileChanges(this._infPath, "HKR,,   SmoothRotationSupport,    %REG_DWORD%,    0x00", "HKR,,   SmoothRotationSupport,    %REG_DWORD%,    0x01");

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
        [Test(Type = TestType.PreCondition, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Restart the system");
            PowerStates powerState = PowerStates.S5;
            this._powerParams = new PowerParams() { Delay = 30, rebootReason = RebootReason.DriverModify };
            base.EventResult(powerState, base.InvokePowerEvent(this._powerParams, powerState));
        }
        [Test(Type = TestType.PreCondition, Order = 3)]
        public void TestStep3()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail(false, "Config not applied!");
                base.SkipToMethod(5);
            }
        }
        [Test(Type = TestType.PreCondition, Order = 4)]
        public void TestStep4()
        {
            bool status_set = false;
            List<string> angleList = Enum.GetNames(typeof(ScreenOrientation)).ToList();
            angleList.Add(angleList.First());

            List<DisplayType> displayTypeList = null;
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
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
                angleList.ForEach(angle =>
                {
                    Log.Message(true, "Setting rotation {0} for {1}", angle, dT);
                    currentMode.Angle = Convert.ToUInt32(angle.Replace("Angle", string.Empty));
                    status_set = AccessInterface.SetFeature<bool, DisplayMode>(Features.Rotation, Action.SetMethod, currentMode);
                    targetMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, displayInfo);
                    if (status_set && targetMode.Angle.Equals(currentMode.Angle))
                        Log.Success("Rotation {0} successfully set for {1}", targetMode.Angle, dT);
                    else
                        Log.Fail("Unable to set rotation {0} for {1}", angle, dT);
                });
            });         
        }
        [Test(Type = TestType.PreCondition, Order = 5)]
        public void TestStep5()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            Log.Message(true, "Revert changes in INF file to Production version");
            this._infPath = CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            INFFileChanges(this._infPath, "HKR,,   SmoothRotationSupport,    %REG_DWORD%,    0x01", "HKR,,   SmoothRotationSupport,    %REG_DWORD%,    0x00");
        }
        [Test(Type = TestType.PostCondition, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Install the driver");
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
        [Test(Type = TestType.PostCondition, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Restart the system");
            PowerStates powerState = PowerStates.S5;
            this._powerParams = new PowerParams() { Delay = 30, rebootReason = RebootReason.DriverModify };
            base.EventResult(powerState, base.InvokePowerEvent(this._powerParams, powerState));
        }
        [Test(Type = TestType.PostCondition, Order = 8)]
        public void TestStep8()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail(false, "Config not applied!");
            }
        }
       
        private void INFFileChanges(string infPath, string toBeReplaced, string toBeChanged)
        {
            StringBuilder newfile = new StringBuilder();
            Log.Verbose("Inf Path is {0}", infPath);
            string[] file = File.ReadAllLines(infPath);

            string temp = "";
            foreach (string line in file)
            {
                if (line.Contains(toBeReplaced))
                {
                    temp = line.Replace(toBeReplaced, toBeChanged);
                    newfile.Append(temp + "\r\n");
                    continue;
                }
                newfile.Append(line + "\r\n");
            }
            File.WriteAllText(infPath, newfile.ToString());
        }
    }
}