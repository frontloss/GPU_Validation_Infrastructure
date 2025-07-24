namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Forms;
    using System.Threading;
    using System;
    using Microsoft.Win32;
    
    [Test(Type = TestType.HasReboot)]
    class MP_NativeCollage_Independent : MP_NativeCollage_BAT
    {
        private Dictionary<int, uint[,]> _myDictionary = null;        
        protected Dictionary<DisplayType, uint> dispAngleList = new Dictionary<DisplayType, uint>();
        private RegistryParams registryParams = new RegistryParams();
     
        public MP_NativeCollage_Independent()
        {
            base._performAction = this.PerformAction;
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal,
                DisplayConfigType.Vertical
            };
            this._myDictionary = new Dictionary<int, uint[,]>()
            {
                { 2, new uint[,] {{0,180},{90,270},{270,90},{180,0}}},  
                { 3, new uint[,] {{90,270,90},{0,180,0},{180,180,0},{90,90,270},{270,270,90}}}
            };
        }
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            Log.Message(true, "Make changes in registry to enable Independent Rotation");            
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "Display1_IndependentRotation";
            registryParams.value = 1;
            registryParams.infChanges = InfChanges.ModifyInf;
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);

            // Get displays passed from the commandline, plug the displays back as DFT doesn't know how many displays are present after disable the driver.
            // Note:Ignore plugging if it is LFP display

            foreach (DisplayType displayType in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("After disable the driver, {0} is not plugged back ", displayType);
                if ((displayType != DisplayType.None))
                {
                    if (base.HotPlug(displayType) == true)
                        Log.Message("After disable the driver, {0} is plugged back ", displayType);
                    else
                        Log.Message("After disable the driver, {0} is not plugged back ", displayType);
                }
            }
            base.TestStep1();
        }        
        private void PerformAction()
        {
            Log.Message(true, "Perform Independent Rotation");
            uint[,] workingAngles = _myDictionary[base.CurrentConfig.ConfigTypeCount];
            for (uint idx = 0; idx <= workingAngles.GetUpperBound(0); idx++)
            {
                PerformIndependentRotation(idx);
            }            
        }
        [Test(Type = TestType.PostCondition, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Revert the changes in Registry to disable Independent Rotation");
            registryParams.value = 0;
            registryParams.infChanges = InfChanges.RevertInf;
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        [Test(Type = TestType.PostCondition, Order = 5)]
        public void TestStep5()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail(false, "Config not applied!");
            }
        }        
        
        protected List<DisplayMode> PerformIndependentRotation(uint argIndex)
        {
            uint[,] workingAngles = _myDictionary[base.CurrentConfig.ConfigTypeCount];
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
            if (AccessInterface.SetFeature<bool, List<DisplayMode>>(Features.SdkIndependentRotation, Action.SetMethod, Source.AccessAPI, argMode))
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