namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.ConnectedStandby)]
    class MP_S0ix_Rotation : MP_S0ixBase
    {
        int[] _rotationSequence = new int[] { 90, 270, 180, 0 };
        private List<DisplayMode> verifyModesList = new List<DisplayMode>();
        #region Test

        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
                Log.Message("Set the maximum display mode on all the active displays");
            }
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void RotationMethod()
        {
            Log.Message(true, "Rotate all active display as per test grid");
            List<DisplayModeList> displayModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                this.RotationOnExtendedDisplay(displayModeList);
            else
                this.RotationOnPrimaryDisplay(displayModeList);
        }

        private void RotationOnPrimaryDisplay(List<DisplayModeList> displayModeList)
        {
            for (int eachAngle = 0; eachAngle < _rotationSequence.GetLength(0); eachAngle++)
            {
                this.RotateNVerify(displayModeList.First().supportedModes.Last(), (uint)_rotationSequence[eachAngle]);
                base.CSCall();
                Verify_RA_ResumeFromS0ix();
            }
        }

        private void RotationOnExtendedDisplay(List<DisplayModeList> displayModeList)
        {
            for (int eachAngle = 0; eachAngle < _rotationSequence.GetLength(0); eachAngle++)
            {
                this.RotateNVerify(displayModeList.First().supportedModes.Last(), (uint)_rotationSequence[eachAngle]);
                this.RotateNVerify(displayModeList.Skip(1).First().supportedModes.Last(), (uint)_rotationSequence[eachAngle]);
                if (base.CurrentConfig.ConfigType.GetDisplaysCount().Equals(3))
                    this.RotateNVerify(displayModeList.Last().supportedModes.Last(), (uint)_rotationSequence[eachAngle]);
                base.CSCall();
                Verify_RA_ResumeFromS0ix();
            }
        }

        private void Verify_RA_ResumeFromS0ix()
        {
            verifyModesList.ForEach(MI =>
            {
                if (VerifyRotation(MI))
                    Log.Success("Display {0} config same after resume from S0ix, SetMode - {1}.", MI.display, MI.GetCurrentModeStr(false));
                else
                    Log.Fail("Display {0} config changed after resume from S0ix, SetMode - {1}.", MI.display, MI.GetCurrentModeStr(false));
            });
        }

        private void RotateNVerify(DisplayMode argMode, uint argAngle)
        {
            argMode.Angle = argAngle;
            Log.Message(true, "Rotating the display {0} through OS call to {1}, {2} Deg", argMode.display, argMode.GetCurrentModeStr(true), argAngle);
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argMode))
            {
                if (!VerifyRotation(argMode))
                {
                    Log.Fail("Mode set failed for display {0}: SetMode - {1}, CurrentMode - {2}.", argMode.display, argMode.GetCurrentModeStr(false));
                }
                else
                {
                    if (verifyModesList.Any(DT => DT.display == argMode.display))
                        verifyModesList.Remove(verifyModesList.Where(DT => DT.display == argMode.display).First());
                    verifyModesList.Add(argMode);
                    Log.Success("Mode is set Successfully for display {0}: {1}", argMode.display, argMode.GetCurrentModeStr(false));
                }
            }
            else
                Log.Fail("Desired mode is not set !!!");
        }

        private bool VerifyRotation(DisplayMode argSetMode)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argSetMode.display).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (currentMode.CanFlip())
            {
                uint temp = currentMode.HzRes;
                currentMode.HzRes = currentMode.VtRes;
                currentMode.VtRes = temp;
            }

            if (argSetMode.HzRes != currentMode.HzRes ||
                    argSetMode.VtRes != currentMode.VtRes ||
                    argSetMode.Bpp != currentMode.Bpp ||
                    argSetMode.RR != currentMode.RR ||
                    argSetMode.Angle != currentMode.Angle ||
                    argSetMode.InterlacedFlag != currentMode.InterlacedFlag)
                return false;
            else
                return true;
        }

        #endregion

    }
}
