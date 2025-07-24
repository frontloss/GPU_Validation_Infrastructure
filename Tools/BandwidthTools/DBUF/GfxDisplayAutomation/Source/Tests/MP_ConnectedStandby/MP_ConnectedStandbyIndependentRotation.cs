namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Windows.Forms;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_ConnectedStandbyIndependentRotation : MP_ConnectedStandbyBase
    {
        #region Test

        protected PowerParams _powerParams = null;
        protected Dictionary<DisplayConfigType, uint[,]> _myDictionary = null;
        private int _retryIndex = 0;
        private string _infPath = string.Empty;
        private List<List<ScreenOrientation>> _angleGroups = null;

        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            DisplayUnifiedConfig unifiedConfig = DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType);
            if (unifiedConfig == DisplayUnifiedConfig.Clone)
                Log.Success("The configType passed is Clone...Test continues");
            else
            {
                this.CleanUP();
                Log.Abort("Pass Config Type as Clone");
            }

            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ProdDriverPath)
                || Directory.GetFiles(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "Setup.exe").Count().Equals(0))
            {
                this.CleanUP();
                Log.Abort("Setup file(s) in {0} path not found!", base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            }

            this._infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            if (!Directory.Exists(this._infPath) || Directory.GetFiles(this._infPath, "*.inf").Count().Equals(0))
            {
                this.CleanUP();
                Log.Abort("INF file in {0} path not found", this._infPath);
            }
        }
        [Test(Type = TestType.PreCondition, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Disabling Driver Signature Enforcement");
            SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON");
        }
        [Test(Type = TestType.PreCondition, Order = 3)]
        public void TestStep3()
        {
            Log.Message("Verify Disabling Driver Signature Enforcement");
            CheckBCDEditOptions("loadoptions DDISABLE_INTEGRITY_CHECKS", "testSigning Yes");

            Log.Message(true, "Make changes in INF file & Install driver");
            this._infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            infFileChanges(this._infPath, "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x00", "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x01");

            AccessInterface.SetFeature(Features.InstallDriver, Action.Set, base.ApplicationManager.ApplicationSettings.ProdDriverPath);
        }
        [Test(Type = TestType.PreCondition, Order = 4)]
        public void TestStep4()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail(false, "Config not applied!");
                base.SkipToMethod(5);
            }

            Log.Message(true, "Check if Independent Rotation enabled after installing changed driver through CUI");
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
            {
                Log.Fail(false, "Unable to launch CUI!");
                base.SkipToMethod(5);
            }

            Dictionary<DisplayType, uint> listDisplayType = new Dictionary<DisplayType, uint>();
            base.CurrentConfig.CustomDisplayList.ForEach(dT => listDisplayType.Add(dT, 0));
            if (CheckIndependentRotation(listDisplayType, false))
                Log.Success("Independent Rotation verified through CUI");
            else
            {
                this.CleanUP();
                Log.Abort("Reinstall Driver...Independent Rotation Could not be verified");
            }
        }
        [Test(Type = TestType.PreCondition, Order = 5)]
        public void TestStep5()
        {
            _myDictionary = new Dictionary<DisplayConfigType, uint[,]>()
            {
                 { DisplayConfigType.DDC, new uint[,] {{0,180},{270,90},{180,0}}},
                 { DisplayConfigType.TDC, new uint[,] {{180,0,180},{270,90,90}}}    
            };
            uint[,] workingAngles = _myDictionary[base.CurrentConfig.ConfigType];
            Log.Message(true, "Apply the independent rotation angles and perform Sleep");
            List<string> allModes = AccessInterface.GetFeature<List<string>>(Features.Modes, Action.GetAll, Source.AccessUI);

            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, base.CurrentConfig.PrimaryDisplay);
            AccessInterface.SetFeature(Features.Modes, Action.Set, Source.AccessUI, allModes.Last());
            if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);

            for (int idx = 0; idx <= workingAngles.GetUpperBound(0); idx++)
            {
                for (int dispIdx = 0; dispIdx < base.CurrentConfig.CustomDisplayList.Count; dispIdx++)
                {
                    Log.Message(true, "Apply the independent rotation angle {0} to {1} for mode {2}", workingAngles[idx, dispIdx], base.CurrentConfig.CustomDisplayList[dispIdx], allModes.Last());
                    ApplyNVerifyRotation(base.CurrentConfig.CustomDisplayList[dispIdx], workingAngles[idx, dispIdx]);
                }

                this.S0ixCall();
                if (!GetListEnumeratedDisplays())
                    Log.Fail("Display enumeration mismatch after comming from S0ix");
                else
                    Log.Message("Connected displays are enumerated properly");
            }
        }
        [Test(Type = TestType.PreCondition, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Revert changes in INF file to Production version");
            this._infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            infFileChanges(this._infPath, "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x01", "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x00");

            Log.Message(true, "Uninstalling the Graphics Driver.");
            AccessInterface.SetFeature<bool>(Features.UnInstallDriver, Action.SetNoArgs);
        }
        [Test(Type = TestType.PostCondition, Order = 7)]
        public void TestStep7()
        {
            File.Delete(CommonExtensions.UninstallFile);
            Log.Message(true, "Install the driver");
            AccessInterface.SetFeature(Features.InstallDriver, Action.Set, base.ApplicationManager.ApplicationSettings.ProdDriverPath);
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

            Log.Message(true, "Check if Independent Rotation is disabled after reverting to original driver through CUI");
            AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No);

            if (revertFromIndependent(base.CurrentConfig.CustomDisplayList))
                Log.Success("Independent Rotation Disabled...System returned to original state");
            else
                Log.Fail("Error in Disabling Independent Rotation");

            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }

        private bool CheckIndependentRotation(Dictionary<DisplayType, uint> argDispAngleList, bool argCheckSelection)
        {
            bool validity = true;
            AccessInterface.Navigate(Features.SelectDisplay);
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, argDispAngleList.First().Key);
            List<ScreenOrientation> allRotations = AccessInterface.GetFeature<List<ScreenOrientation>>(Features.Rotation, Action.GetAll, Source.AccessUI);
            ScreenOrientation primaryRotation = AccessInterface.GetFeature<ScreenOrientation>(Features.Rotation, Action.Get, Source.AccessUI);
            if (!allRotations.Count.Equals(4))
            {
                Log.Fail("Primary angles for {0} not listed appropriately!", argDispAngleList.First().Key);
                validity = false;
            }
            if (argCheckSelection && this.getScreenOrientation(argDispAngleList.First().Value) != primaryRotation)
            {
                Log.Fail("{0} not retained for {1}! Current is {2}", this.getScreenOrientation(argDispAngleList.First().Value), argDispAngleList.First().Key, primaryRotation);
                validity = false;
            }
            else
                Log.Success("{0} retained for {1}", this.getScreenOrientation(argDispAngleList.First().Value), argDispAngleList.First().Key);

            foreach (KeyValuePair<DisplayType, uint> kV in argDispAngleList.Skip(1).ToList())
            {
                AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, kV.Key);
                allRotations = AccessInterface.GetFeature<List<ScreenOrientation>>(Features.Rotation, Action.GetAll, Source.AccessUI);
                ScreenOrientation rotation = AccessInterface.GetFeature<ScreenOrientation>(Features.Rotation, Action.Get, Source.AccessUI);

                if (!allRotations.Count.Equals(2) || !this.GetGroup(primaryRotation).Except(allRotations).Count().Equals(0))
                {
                    Log.Fail("Angles for {0} not listed appropriately!", kV.Key);
                    validity = false;
                }
                if (argCheckSelection && this.getScreenOrientation(kV.Value) != rotation)
                {
                    Log.Fail("{0} not retained for {1}! Current is {2}", this.getScreenOrientation(kV.Value), kV.Key, rotation);
                    validity = false;
                }
                else
                    Log.Success("{0} retained for {1}", this.getScreenOrientation(kV.Value), kV.Key);
            }
            return validity;
        }
        private void infFileChanges(string infPath, string toBeReplaced, string toBeChanged)
        {
            string fileName = "\\igdlh64.inf";
            StringBuilder newfile = new StringBuilder();
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            Log.Verbose("{0}", string.Concat(infPath, fileName));
            string[] file = File.ReadAllLines(string.Concat(infPath, fileName));

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
            File.WriteAllText(string.Concat(infPath, fileName), newfile.ToString());
        }
        private bool revertFromIndependent(List<DisplayType> argDisplays)
        {
            AccessInterface.Navigate(Features.SelectDisplay);
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, argDisplays.First());
            bool rotationOptions = AccessInterface.GetFeature<List<ScreenOrientation>>(Features.Rotation, Action.GetAll, Source.AccessUI).Count.Equals(4);
            argDisplays.Skip(1).ToList().ForEach(dT =>
            {
                AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, dT);
                rotationOptions &= AccessInterface.GetFeature<List<ScreenOrientation>>(Features.Rotation, Action.GetAll, Source.AccessUI).Count.Equals(0);
            });

            return rotationOptions;
        }
        private ScreenOrientation getScreenOrientation(uint angle)
        {
            return (ScreenOrientation)Enum.Parse(typeof(ScreenOrientation), string.Concat("Angle", angle), true);
        }
        protected void ApplyNVerifyRotation(DisplayType DT, uint angle)
        {
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, DT);
            ScreenOrientation angleToBeSet = getScreenOrientation(angle);

            AccessInterface.SetFeature<ScreenOrientation>(Features.Rotation, Action.Set, Source.AccessUI, angleToBeSet);
            if (AccessInterface.SetFeature<bool, AppBarOptions>(Features.AppBar, Action.SetMethod, AppBarOptions.Apply))
                AccessInterface.SetFeature(Features.ConfirmationPopup, Action.Set, DecisionActions.Yes);

            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, DT);
            ScreenOrientation returnedangle = AccessInterface.GetFeature<ScreenOrientation>(Features.Rotation, Action.Get, Source.AccessUI);
            if (String.Equals(returnedangle.ToString(), string.Concat("Angle", angle)))
                Log.Success("Rotation {0} Applied on {1} and Verified", angle, DT);
            else
            {
                Log.Sporadic(true, "{0} Display is set to {1} Rotation instead of {2}. Try setting again", DT, returnedangle, angle);
                if (this._retryIndex < 1)
                {
                    this._retryIndex++;
                    ApplyNVerifyRotation(DT, angle);
                }
                else
                    Log.Fail(true, "{0} Display is set to {1} Rotation instead of {2}. Try setting again", DT, returnedangle, angle);
            }
        }

        private List<List<ScreenOrientation>> AngleGroups
        {
            get
            {
                if (null == this._angleGroups)
                {
                    this._angleGroups = new List<List<ScreenOrientation>>();
                    this._angleGroups.Add(new List<ScreenOrientation>() { ScreenOrientation.Angle0, ScreenOrientation.Angle180 });
                    this._angleGroups.Add(new List<ScreenOrientation>() { ScreenOrientation.Angle90, ScreenOrientation.Angle270 });
                }
                return this._angleGroups;
            }
        }
        private List<ScreenOrientation> GetGroup(ScreenOrientation argCurrentAngle)
        {
            return this.AngleGroups.Where(lSO => lSO.Contains(argCurrentAngle)).FirstOrDefault();
        }

        #endregion

        #region PostCondition
        [Test(Type = TestType.PostCondition, Order = 9)]
        public void TestPostCondition()
        {
            this.CleanUP();
        }
        #endregion

    }
}
