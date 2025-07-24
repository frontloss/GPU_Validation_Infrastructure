namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Collections.Generic;

    class MP_CI_Rotation : TestBase
    {
        protected System.Action _powerStateAction = null;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set initial configuration to {0}", base.CurrentConfig.GetCurrentConfigStr());
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
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
                    if (null != this._powerStateAction)
                        this._powerStateAction();
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