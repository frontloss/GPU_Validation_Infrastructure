namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Windows.Forms;
    using System.Threading;

    [Test(Type = TestType.WiDi)]
    [Test(Type = TestType.HasReboot)]
    class MP_WIDI_IndependentRotation : MP_WIDIBase
    {
        private string _infPath = string.Empty;
        private List<List<ScreenOrientation>> _angleGroups = null;
        protected Dictionary<DisplayConfigType, uint[,]> _myDictionary = null;
        private int _retryIndex = 0;

        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            DisplayUnifiedConfig unifiedConfig = DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType);
            if (unifiedConfig == DisplayUnifiedConfig.Clone)
                Log.Success("The configType passed is Clone...Test continues");
            else
                Log.Abort("Pass Config Type as Clone");
            CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
        }

        [Test(Type = TestType.PreCondition, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Make changes in INF file & Install driver");
            this._infPath = CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            INFFileChanges(this._infPath, "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x00", "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x01");
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
        [Test(Type = TestType.PreCondition, Order = 3)]
        public void TestStep3()
        {
            if (!WiDiReConnect(true))
                CheckWiDiStatus();
            if (!this.SetNValidateConfig(this.CurrentConfig))
            {
                base.ListEnumeratedDisplays();
                Log.Fail(false, "Config not applied!");
                base.SkipToMethod(6);
            }

            Log.Message(true, "Check if Independent Rotation enabled after installing changed driver through CUI");
            if (!AccessInterface.SetFeature<bool, DecisionActions>(Features.LaunchCUI, Action.SetMethod, DecisionActions.No))
            {
                Log.Fail(false, "Unable to launch CUI!");
                base.SkipToMethod(6);
            }

            Dictionary<DisplayType, uint> listDisplayType = new Dictionary<DisplayType, uint>();
            base.CurrentConfig.CustomDisplayList.ForEach(dT => listDisplayType.Add(dT, 0));
            if (CheckIndependentRotation(listDisplayType, false))
                Log.Success("Independent Rotation verified through CUI");
            else
            {
                Log.Fail("Independent Rotation Could not be verified");
                base.SkipToMethod(6);
            }
            if (base.CurrentConfig.ConfigType == DisplayConfigType.DDC && base.CurrentConfig.CustomDisplayList.Contains(DisplayType.WIDI))
                base.SkipToMethod(6);
        }
        [Test(Type = TestType.PreCondition, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message("Disconnect WIDI to check whether independent rotation enabled or not");
            Log.Message("Set display to clone config to check whether independent rotation is enabled or not.");
            DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC };
            if (base.WiDIDisconnect())
            {
                base.CurrentConfig.CustomDisplayList.Sort();
                displayConfig.PrimaryDisplay = base.CurrentConfig.CustomDisplayList.First();
                displayConfig.SecondaryDisplay = base.CurrentConfig.CustomDisplayList.Skip(1).First();
                displayConfig.DisplayList = base.CurrentConfig.CustomDisplayList;
                displayConfig.DisplayList.Remove(DisplayType.WIDI);
                displayConfig.EnumeratedDisplays = base.CurrentConfig.EnumeratedDisplays;
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                    Log.Message("Config {0} {1} + {2} applied successfully", displayConfig.ConfigType, displayConfig.PrimaryDisplay, displayConfig.SecondaryDisplay);
                else
                    Log.Abort("Config {0} {1} + {2} failed", displayConfig.ConfigType, displayConfig.PrimaryDisplay, displayConfig.SecondaryDisplay);
            }

            Log.Message(true, "Check if Independent Rotation enabled after installing changed driver through CUI");
            AccessInterface.Navigate(Features.SelectDisplay);

            this._myDictionary = new Dictionary<DisplayConfigType, uint[,]>()
            {
                 { DisplayConfigType.DDC, new uint[,] {{180,0},{90,270}}},  
            };
            uint[,] workingAngles = _myDictionary[displayConfig.ConfigType];
            Dictionary<DisplayType, uint> dispAngleList = new Dictionary<DisplayType, uint>();

            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, displayConfig.DisplayList);
            List<DisplayMode> commonModes = base.FilterModeLists(displayModeList_OSPage.Where(dML => dML.display == displayConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault());
            displayModeList_OSPage.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
            if (commonModes.Count() > 0)
            {
                this.ApplyModeAndVerify(commonModes.Last(), false);
                for (uint idx = 0; idx <= workingAngles.GetUpperBound(0); idx++)
                {
                    this._retryIndex = 0;
                    for (int dispIdx = 0; dispIdx < displayConfig.CustomDisplayList.Count; dispIdx++)
                    {
                        Log.Message(true, "Apply the independent rotation angle {0} to {1} for mode {2}", workingAngles[idx, dispIdx], displayConfig.CustomDisplayList[dispIdx], commonModes.Last().GetCurrentModeStr(true));
                        dispAngleList.Add(displayConfig.CustomDisplayList[dispIdx], workingAngles[idx, dispIdx]);
                        this.ApplyNVerifyRotation(displayConfig.CustomDisplayList[dispIdx], workingAngles[idx, dispIdx]);
                    }
                    CheckIndependentRotation(dispAngleList, true);
                    dispAngleList.Clear();
                }
            }
            else
                Log.Fail("Common mode list is not found");

        }

        [Test(Type = TestType.PreCondition, Order = 5)]
        public void TestStep5()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            Log.Message(true, "Revert changes in INF file to Production version");
            this._infPath = CommonExtensions.IdentifyDriverFile(base.ApplicationManager.ApplicationSettings.ProdDriverPath);
            INFFileChanges(this._infPath, "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x01", "HKR,,   Display1_IndependentRotation,    %REG_DWORD%,    0x00");
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
            if (!base.IsWiDiConnected())
                base.WiDiReConnect(true);
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
                try
                {
                    AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, kV.Key);
                }
                catch
                {
                    Log.Message("Unable to set Display {0}", kV.Key);
                    base.WiDiReConnect(true);
                    Thread.Sleep(3000);
                    AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, kV.Key);
                }
                allRotations = AccessInterface.GetFeature<List<ScreenOrientation>>(Features.Rotation, Action.GetAll, Source.AccessUI);
                ScreenOrientation rotation = AccessInterface.GetFeature<ScreenOrientation>(Features.Rotation, Action.Get, Source.AccessUI);
                if (!IsWiDiConnected())
                {
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
                else
                {
                    if (!allRotations.Count.Equals(2) || !this.GetGroup(primaryRotation).Except(allRotations).Count().Equals(0))
                    {
                        Log.Success("Angles for {0} not listed as expected", kV.Key);
                        validity = true;
                    }
                    else
                        Log.Fail("{0} retained for {1}", this.getScreenOrientation(kV.Value), kV.Key);
                }
            }
            return validity;
        }
        private ScreenOrientation getScreenOrientation(uint angle)
        {
            return (ScreenOrientation)Enum.Parse(typeof(ScreenOrientation), string.Concat("Angle", angle), true);
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
