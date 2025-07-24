namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;
    using System.Windows.Forms;

    [Test(Type = TestType.HasReboot)]
    class MP_SmartFrame_Rotation : MP_SmartFrame_Base
    {
        private List<string> angleList = new List<string>();
        List<DisplayType> displayTypeList = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set config SD {0} via OS", base.GetInternalDisplay());
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.SD;
            config.PrimaryDisplay = base.GetInternalDisplay();
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, config))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            angleList = Enum.GetNames(typeof(ScreenOrientation)).ToList();
            angleList.Add(angleList.First());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            bool status_set = false;

            displayTypeList = new List<DisplayType>() { base.GetInternalDisplay() };
            DisplayInfo displayInfo = null;
            DisplayMode targetMode;
            DisplayMode currentMode;
            displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.GetInternalDisplay()).First();
            currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            angleList.ForEach(angle =>
            {
                Log.Message(true, "Setting rotation {0} for {1}", angle, base.GetInternalDisplay());
                currentMode.Angle = Convert.ToUInt32(angle.Replace("Angle", string.Empty));
                status_set = AccessInterface.SetFeature<bool, DisplayMode>(Features.Rotation, Action.SetMethod, currentMode);
                targetMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Rotation, Action.GetMethod, Source.AccessAPI, displayInfo);
                if (status_set && targetMode.Angle.Equals(currentMode.Angle))
                    Log.Success("Rotation {0} successfully set for {1}", targetMode.Angle, base.GetInternalDisplay());
                else
                    Log.Fail("Unable to set rotation {0} for {1}", angle, base.GetInternalDisplay());
                Log.Message(true, "Disable Smart Frame");
                base.DisableSF();
                base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
                this.VerifyRotationPersistance(angle);
                Log.Message(true, "Enable Smart Frame");
                base.EnableSF();
                base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
                this.VerifyRotationPersistance(angle);
            });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
        }
        private void VerifyRotationPersistance(string argAngle)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.GetInternalDisplay()).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (currentMode.Angle == Convert.ToUInt32(argAngle.Replace("Angle", string.Empty)))
                Log.Success("Rotation on {0} is persistant", base.GetInternalDisplay());
            else
                Log.Fail("Resolution on {0} not persisting, expected rotation {1}, actual rotation {2}", base.GetInternalDisplay(), argAngle, currentMode.Angle);
        }
    }
}