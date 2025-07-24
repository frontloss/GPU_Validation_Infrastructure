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
    class MP_CI_IndependentRotation : TestBase
    {
        private Dictionary<DisplayConfigType, uint[,]> _myDictionary = null;
        private string _infPath = string.Empty;
        private Dictionary<DisplayType, uint> dispAngleList = new Dictionary<DisplayType, uint>();
        private RegistryParams registryParams = new RegistryParams();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            DisplayUnifiedConfig unifiedConfig = DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType);
            if (unifiedConfig == DisplayUnifiedConfig.Clone)
                Log.Success("The configType passed is Clone...Test continues");
            else
                Log.Abort("Pass Config Type as Clone");
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "Display1_IndependentRotation";
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

            Log.Message(true, "Make changes in Registry for Enabling Independent rotation");
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
            }

        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            this._myDictionary = new Dictionary<DisplayConfigType, uint[,]>()
            {
                { DisplayConfigType.DDC, new uint[,] {{180,0},{90,270}}},  
                { DisplayConfigType.TDC, new uint[,] {{0,180,0},{270,90,90}}}
            };
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
    }
}