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
    using Microsoft.Win32;

    [Test(Type = TestType.HasReboot)]
    class MP_Rotation_Independent_Basic : TestBase
    {
        protected PowerParams _powerParams = null;
        protected Dictionary<DisplayConfigType, uint[,]> _myDictionary = null;
        private int _retryIndex = 0;
        private string _infPath = string.Empty;
        private List<List<ScreenOrientation>> _angleGroups = null;
        protected Dictionary<DisplayType, uint> dispAngleList = new Dictionary<DisplayType, uint>();
        protected RegistryParams registryParams = new RegistryParams();

        public MP_Rotation_Independent_Basic()
        {
            this._myDictionary = new Dictionary<DisplayConfigType, uint[,]>()
            {
                 { DisplayConfigType.DDC, new uint[,] {{180,0},{90,270},{0,180},{270,90},{180,180}}},  
                { DisplayConfigType.TDC, new uint[,] {{180,0,180},{0,180,180},{0,180,0},{0,0,0},{270,90,90},{270,270,90},{90,90,270}}}
            };
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "Display1_IndependentRotation";
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            DisplayUnifiedConfig unifiedConfig = DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType);
            if (unifiedConfig == DisplayUnifiedConfig.Clone)
                Log.Success("The configType passed is Clone...Test continues");
            else
                Log.Abort("Pass Config Type as Clone");
        }
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            DisplayConfig configParam = new DisplayConfig
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = base.GetInternalDisplay()
            };
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, configParam);
            Log.Message(true, "Make changes in Registry to enable Independent Rotation");
            registryParams.value = 1;
            registryParams.infChanges = InfChanges.ModifyInf;
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "Display1_IndependentRotation";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Verbose("Display {0} is not enumerated after enabling Gfx Driver, plugging it back", DT);
                base.HotPlug(DT);
            }

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail(false, "Config not applied!");
                base.SkipToMethod(4);
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            uint[,] workingAngles = _myDictionary[base.CurrentConfig.ConfigType];

            for (uint idx = 0; idx <= workingAngles.GetUpperBound(0); idx++)
            {
                PerformIndependentRotation(idx);
            }
        }
        [Test(Type = TestType.PostCondition, Order = 4)]
        public void TestStep4()
        {
            DisplayConfig configParam = new DisplayConfig
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = base.GetInternalDisplay()
            };
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, configParam);

            Log.Message(true, "Make changes in Registry to disable Independent Rotation");
            registryParams.value = 0;
            registryParams.infChanges = InfChanges.RevertInf;
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "Display1_IndependentRotation";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        protected List<DisplayMode> PerformIndependentRotation(uint argIndex)
        {
            uint[,] workingAngles = _myDictionary[base.CurrentConfig.ConfigType];
            List<DisplayMode> modeList = new List<DisplayMode>();
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.DisplayList.First()).First();
            DisplayMode Mode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            Log.Message("Rotate primary {0} by {1}", base.CurrentConfig.PrimaryDisplay, workingAngles[argIndex, 0]);
            uint primaryAngle = workingAngles[argIndex, 0];
            Mode.Angle = primaryAngle;
            modeList.Add(Mode);

            Log.Message("Rotate secondary {0} by {1}", base.CurrentConfig.SecondaryDisplay, workingAngles[argIndex, 1]);
            DisplayInfo SecDisplayInfo = this.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.SecondaryDisplay).First();
            DisplayMode secMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, SecDisplayInfo);
            uint secondaryAngle = workingAngles[argIndex, 1];
            secMode.Angle = secondaryAngle;
            modeList.Add(secMode);

            uint tertiaryAngle = 0;
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                Log.Message("Rotate tertiary {0} by {1}", base.CurrentConfig.TertiaryDisplay, workingAngles[argIndex, 2]);
                DisplayInfo terDisplayInfo = this.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.TertiaryDisplay).First();
                DisplayMode terMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, terDisplayInfo);
                tertiaryAngle = workingAngles[argIndex, 2];
                terMode.Angle = tertiaryAngle;
                modeList.Add(terMode);
            }
            this.RotateNVerify(modeList, modeList.First().Angle);
            return modeList;
        }
        protected void RotateNVerify(List<DisplayMode> argMode, uint argAngle)
        {
            DisplayMode actualMode;

            Log.Message(true, "Rotating the displays");
            argMode.ForEach(curMode =>
            {
                Log.Message(true, "Rotating the display {0} through OS call to {1}, {2} Deg", curMode.display, curMode.GetCurrentModeStr(true), curMode.Angle);

            });
            if (AccessInterface.SetFeature<bool, List<DisplayMode>>(Features.SdkIndependentRotation, Action.SetMethod, argMode))
            {
                argMode.ForEach(curMode =>
                {
                    actualMode = VerifyRotation(curMode.display, curMode);
                    if (actualMode.Angle != curMode.Angle)
                    {
                        Log.Fail(false, "Mode set failed for display {0}: SetMode - {1}, CurrentMode - {2}. Trying again!", actualMode.display, curMode.GetCurrentModeStr(false), actualMode.GetCurrentModeStr(false));
                    }
                    else
                        Log.Success("Mode is set Successfully for display {0}: {1}", actualMode.display, actualMode.GetCurrentModeStr(false));

                });
            }
            else
                Log.Fail(false, "Desired mode is not set !!!");
        }
        protected DisplayMode VerifyRotation(DisplayType argDisplay, DisplayMode argSetMode)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplay).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (currentMode.CanFlip())
            {
                uint temp = currentMode.HzRes;
                currentMode.HzRes = currentMode.VtRes;
                currentMode.VtRes = temp;
            }
            return currentMode;
        }
        private void SetInitialConfig()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail(false, "Config not applied!");
            }
        }
        private bool NewAngles(uint[,] argWorkingAngles, uint argIdx)
        {
            if (argIdx == 0)
                return false;
            else
            {
                uint angleToBeChecked = argWorkingAngles[argIdx, 1];
                for (int dispIdx = 0; dispIdx < base.CurrentConfig.CustomDisplayList.Count; dispIdx++)
                {
                    if (angleToBeChecked == argWorkingAngles[argIdx - 1, dispIdx])
                        return false;
                }
                return true;
            }
        }
        private void ApplyNVerifyMode(DisplayMode argMode)
        {
            bool result = AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argMode);
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
        private void LogFailMessage(string argMessage, bool argCaptureScreenshot, int argNewIndex)
        {
            Log.Fail(argCaptureScreenshot, argMessage);
            base.SkipToMethod(argNewIndex);
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
    }
}