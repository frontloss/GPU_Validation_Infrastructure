namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Forms;
    using System;

    public class MP_Rotation_OSPage : TestBase
    {
        int[,] _rotationSequence = new int[3, 6] { { 90, 180, 270, 0, 90, 90 }, 
                                                    { 270, 90, 180, 90, 270, 0 }, 
                                                    { 180, 180, 90, 0, 180, 270 } };
        int _retry = 0;

        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                this.EnumeratedDisplaysHandler();
                Log.Abort("Config not applied!");
            }
           // this.OpenCUI();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void RotationMethod()
        {
            List<DisplayModeList> displayModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                this.RotationOnExtendedDisplay(displayModeList);
            else
                this.RotationOnPrimaryDisplay(displayModeList);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void CleanUp()
        {
           // this.CloseCUI();
            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig);
        }

        private void RotationOnPrimaryDisplay(List<DisplayModeList> displayModeList)
        {
            List<DisplayMode> filteredModes = TestModes(displayModeList.First().supportedModes);
            foreach (DisplayMode eachSingleMode in filteredModes)
                for (int eachAngle = 0; eachAngle < _rotationSequence.GetLength(1); eachAngle++)
                    this.RotateNVerify(eachSingleMode, (uint)_rotationSequence[1, eachAngle]);
        }
        private void RotationOnExtendedDisplay(List<DisplayModeList> displayModeList)
        {
            List<DisplayMode> primaryFilteredModes = TestModes(displayModeList.First().supportedModes);
            List<DisplayMode> SecondaryFilteredModes = TestModes(displayModeList.Skip(1).First().supportedModes);
            List<DisplayMode> thirdFilteredModes = null;
            if (base.CurrentConfig.ConfigType.GetDisplaysCount().Equals(3))
                thirdFilteredModes = TestModes(displayModeList.Last().supportedModes);
            for (int modeIndex = 0; modeIndex < primaryFilteredModes.Count; modeIndex++)
            {
                for (int eachAngle = 0; eachAngle < _rotationSequence.GetLength(1); eachAngle++)
                {
                    this.RotateNVerify(primaryFilteredModes[modeIndex], (uint)_rotationSequence[0, eachAngle]);
                    this.RotateNVerify(SecondaryFilteredModes[modeIndex], (uint)_rotationSequence[1, eachAngle]);
                    if (null != thirdFilteredModes)
                        this.RotateNVerify(thirdFilteredModes[modeIndex], (uint)_rotationSequence[2, eachAngle]);
                }
            }
        }
        private void RotateNVerify(DisplayMode argMode, uint argAngle)
        {
            DisplayMode actualMode;
            argMode.Angle = argAngle;
            Log.Message(true, "Rotating the display {0} through OS call to {1}, {2} Deg", argMode.display, argMode.GetCurrentModeStr(true), argAngle);
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argMode))
            {
                actualMode = VerifyRotation(argMode.display, argMode);
                if (actualMode.HzRes != argMode.HzRes ||
                    actualMode.VtRes != argMode.VtRes ||
                    actualMode.Bpp != argMode.Bpp ||
                    actualMode.RR != argMode.RR ||
                    actualMode.Angle != argMode.Angle ||
                    actualMode.InterlacedFlag != argMode.InterlacedFlag)
                {
                    Log.Fail(false, "Mode set failed for display {0}: SetMode - {1}, CurrentMode - {2}. Trying again!", actualMode.display, argMode.GetCurrentModeStr(false), actualMode.GetCurrentModeStr(false));
                }
                else
                    Log.Success("Mode is set Successfully for display {0}: {1}", actualMode.display, actualMode.GetCurrentModeStr(false));
                //VerifyRotationUsingCUI(modeToSet.display, modeToSet.Angle);
            }
            else
                Log.Fail(false, "Desired mode is not set !!!");
        }
        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            return testModes;
        }
        private DisplayMode VerifyRotation(DisplayType argDisplay, DisplayMode argSetMode)
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
        private void VerifyRotationUsingCUI(DisplayType argDisplay, uint argAngle)
        {
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, argDisplay);
            ScreenOrientation argAngleToBeVerified;
            ScreenOrientation getRotation = AccessInterface.GetFeature<ScreenOrientation>(Features.Rotation, Action.Get, Source.AccessUI);
            if (Enum.TryParse(string.Concat("Angle", argAngle), out argAngleToBeVerified))
                if (argAngleToBeVerified == getRotation)
                    Log.Success("The Rotation is verified through CUI");
                else
                    Log.Fail("The CUI shows display {0} at angle {1}, expected angle is {1}", argDisplay, getRotation, argAngleToBeVerified);
        }
        private void EnumeratedDisplaysHandler()
        {
            List<uint> winMonitorIDList = base.ListEnumeratedDisplays();
            List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
            if (!enumeratedWinMonIDList.Count.Equals(winMonitorIDList.Count) && !CommonExtensions.HasRetryThruRebootFile())
            {
                Log.Verbose("Currently enumerated displays mismatch! A reboot is required.");
                CommonExtensions.WriteRetryThruRebootInfo();
                base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5}, PowerStates.S5);
            }
            else
                CommonExtensions.ClearRetryThruRebootFile();
        }
    }
}